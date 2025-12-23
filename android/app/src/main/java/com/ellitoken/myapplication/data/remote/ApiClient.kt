package com.ellitoken.myapplication.data.remote

import com.ellitoken.myapplication.utils.NetworkError
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.utils.io.ByteReadChannel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.serialization.SerializationException
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.nio.channels.UnresolvedAddressException
import com.ellitoken.myapplication.utils.Result

class ApiClient(
    private val httpClient: HttpClient,
    private val userManager: UserManager
) {
    private val refreshMutex = Mutex()
    private var isRefreshingToken = false

    private val json = Json { ignoreUnknownKeys = true }

    suspend fun handleApiRequest(
        requestType: RequestType,
        authType: AuthType,
        url: String,
        body: Any? = null,
        isRetry: Boolean = false
    ): Result<HttpResponse, NetworkError> {
        return try {
            val response = makeRequest(requestType, authType, url, body)

            when (response.status.value) {
                in 200..299 -> Result.Success(response)
                401 -> {
                    if (authType == AuthType.ACCESS && !isRetry) {
                        val refreshResult = refreshAccessToken()
                        if (refreshResult is Result.Success) {
                            return handleApiRequest(requestType, authType, url, body, true)
                        } else {
                            userManager.clearAccessToken()
                            userManager.clearRefreshToken()
                            return Result.Error(NetworkError("Oturum süresi doldu, tekrar giriş yapın."))
                        }
                    } else {
                        userManager.clearAccessToken()
                        userManager.clearRefreshToken()
                        return Result.Error(NetworkError("Yetkisiz erişim."))
                    }
                }
                else -> {
                    val errorMessage = try {
                         response.body<ErrorDto>().message
                    } catch (e: Exception) {
                        "Beklenmeyen bir hata oluştu: ${response.status}"
                    }
                    return Result.Error(NetworkError(errorMessage))
                }
            }
        } catch (e: UnresolvedAddressException) {
            Result.Error(NetworkError("İnternet bağlantınızı kontrol edin."))
        } catch (e: SerializationException) {
            Result.Error(NetworkError("Veri işleme hatası."))
        } catch (e: Exception) {
            Result.Error(NetworkError(e.localizedMessage ?: "Bilinmeyen hata."))
        }
    }

    suspend fun <T> streamJsonAsFlow(
        endpoint: String,
        authType: AuthType,
        requestType: RequestType = RequestType.POST,
        body: Any? = null,
        serializer: (String) -> T,
        isRetry: Boolean = false
    ): Flow<Result<T, NetworkError>> = flow {
        try {
            val response = httpClient.request("/api/$endpoint") {
                method = when (requestType) {
                    RequestType.GET -> HttpMethod.Get
                    RequestType.POST -> HttpMethod.Post
                    RequestType.PUT -> HttpMethod.Put
                    RequestType.DELETE -> HttpMethod.Delete
                    RequestType.PATCH -> HttpMethod.Patch
                }

                when (authType) {
                    AuthType.ACCESS -> {
                        userManager.getAccessToken()?.let {
                            header(HttpHeaders.Authorization, "Bearer $it")
                        } ?: throw Exception("Access Token yok")
                    }
                    AuthType.REFRESH -> {
                        userManager.getRefreshToken()?.let {
                            header(HttpHeaders.Authorization, "Bearer $it")
                        } ?: throw Exception("Refresh Token yok")
                    }
                    AuthType.NONE -> {}
                }

                header(HttpHeaders.Accept, "text/event-stream")

                if (body != null) {
                    contentType(ContentType.Application.Json)
                    setBody(body)
                }
            }

            if (response.status == HttpStatusCode.Unauthorized) {
                if (authType == AuthType.ACCESS && !isRetry) {
                    val refreshResult = refreshAccessToken()
                    if (refreshResult is Result.Success) {
                        streamJsonAsFlow(endpoint, authType, requestType, body, serializer, true)
                            .collect { emit(it) }
                        return@flow
                    }
                }
                emit(Result.Error(NetworkError("Yetkisiz erişim (401).")))
                return@flow
            }

            val channel: ByteReadChannel = response.bodyAsChannel()

            while (!channel.isClosedForRead) {
                val line = channel.readUTF8Line(limit = 10000)
                if (!line.isNullOrBlank()) {
                    try {
                        val dataLine = line.substringAfter("data:", "").trim()
                        if (dataLine.isNotEmpty()) {
                            val data = serializer(dataLine)
                            emit(Result.Success(data))
                        }
                    } catch (e: Exception) {
                        emit(Result.Error(NetworkError("Parse hatası")))
                    }
                }
            }

        } catch (e: UnresolvedAddressException) {
            emit(Result.Error(NetworkError("İnternet bağlantısı yok.")))
        } catch (e: SerializationException) {
            emit(Result.Error(NetworkError("Veri formatı hatalı.")))
        } catch (e: Exception) {
            emit(Result.Error(NetworkError(e.localizedMessage ?: "Bilinmeyen hata")))
        }
    }

    private suspend fun makeRequest(
        requestType: RequestType,
        authType: AuthType,
        url: String,
        body: Any?
    ): HttpResponse {
        val apiPath = if (url.startsWith("/")) url else "/$url"
        val fullUrl = "/api$apiPath" // Base URL httpClient config'inde tanımlı varsayıyoruz

        return httpClient.request(fullUrl) {
            method = when (requestType) {
                RequestType.GET -> HttpMethod.Get
                RequestType.POST -> HttpMethod.Post
                RequestType.PUT -> HttpMethod.Put
                RequestType.DELETE -> HttpMethod.Delete
                RequestType.PATCH -> HttpMethod.Patch
            }

            when (authType) {
                AuthType.ACCESS -> {
                    userManager.getAccessToken()?.let {
                        header(HttpHeaders.Authorization, "Bearer $it")
                    }
                }
                AuthType.REFRESH -> {
                    userManager.getRefreshToken()?.let {
                        header(HttpHeaders.Authorization, "Bearer $it")
                    }
                }
                AuthType.NONE -> {}
            }

            contentType(ContentType.Application.Json)
            if (body != null) setBody(body)
        }
    }

    private suspend fun refreshAccessToken(): Result<Unit, NetworkError> {
        return refreshMutex.withLock {
            if (isRefreshingToken) {
                return@withLock Result.Error(NetworkError("Token yenileme sürüyor."))
            }

            try {
                isRefreshingToken = true
                
                val response = makeRequest(
                    RequestType.POST,
                    AuthType.REFRESH,
                    "/auth/refresh-token",
                    null
                )

                isRefreshingToken = false

                if (response.status.value in 200..299) {
                    val bodyText = response.bodyAsText()
                    val authResponse = json.decodeFromString<AuthResponseDto>(bodyText)
                    
                    if (authResponse.accessToken != null && authResponse.refreshToken != null) {
                        userManager.saveAccessToken(authResponse.accessToken)
                        userManager.saveRefreshToken(authResponse.refreshToken)
                        return@withLock Result.Success(Unit)
                    }
                }
                return@withLock Result.Error(NetworkError("Token yenilenemedi."))
            } catch (e: Exception) {
                isRefreshingToken = false
                return@withLock Result.Error(NetworkError("Token yenileme hatası: ${e.message}"))
            }
        }
    }
}


interface UserManager {
    fun getAccessToken(): String?
    fun getRefreshToken(): String?
    fun saveAccessToken(token: String)
    fun saveRefreshToken(token: String)
    fun clearAccessToken()
    fun clearRefreshToken()
}

enum class RequestType { GET, POST, PUT, DELETE, PATCH }
enum class AuthType { NONE, ACCESS, REFRESH }

@Serializable
data class AuthResponseDto(
    val accessToken: String?,
    val refreshToken: String?
)

@Serializable
data class ErrorDto(
    val message: String
)