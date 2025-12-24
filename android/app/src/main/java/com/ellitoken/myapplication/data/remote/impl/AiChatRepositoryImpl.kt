package com.ellitoken.myapplication.data.remote.impl

import com.ellitoken.myapplication.data.remote.ApiClient
import com.ellitoken.myapplication.data.remote.AuthType
import com.ellitoken.myapplication.data.remote.RequestType
import com.ellitoken.myapplication.data.remote.model.request.AiChatRequest
import com.ellitoken.myapplication.data.remote.model.request.InputData
import com.ellitoken.myapplication.data.remote.repository.AiChatRepository
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import com.ellitoken.myapplication.utils.NetworkError
import com.ellitoken.myapplication.utils.Result
import kotlinx.coroutines.flow.Flow
import kotlinx.datetime.Clock
import kotlinx.serialization.json.Json
import org.json.JSONObject
import java.util.UUID

class AiChatRepositoryImpl(
    private val apiClient: ApiClient
) : AiChatRepository {

    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun streamAiMessage(prompt: String, threadId: String, clientTurnId: String ): Flow<Result<AiMessage, NetworkError>> {
        val requestObj = AiChatRequest(
            input = InputData(message = prompt),
            threadId = threadId,
            clientTurnId = clientTurnId
        )

        val requestJsonString = json.encodeToString(AiChatRequest.serializer(), requestObj)

        return apiClient.streamJsonAsFlow(
            endpoint = "invoke",
            authType = AuthType.ACCESS,
            requestType = RequestType.POST,
            body = requestJsonString,

            serializer = { jsonString ->
                try {
                    val rootObject = JSONObject(jsonString)
                    val responseArray = rootObject.optJSONArray("response")

                    if (responseArray != null && responseArray.length() > 0) {

                        val firstItem = responseArray.getJSONObject(0)
                        val messageText = firstItem.optString("text", "")

                        if (messageText.isNotEmpty()) {
                            AiMessage(
                                id = UUID.randomUUID().toString(),
                                message = messageText,
                                createdAt = Clock.System.now(),
                                fromAi = true
                            )
                        } else {
                            null
                        }

                    } else {
                        AiMessage(
                            id = UUID.randomUUID().toString(),
                            message = "Üzgünüm, şu an yardımcı olamıyorum.",
                            createdAt = Clock.System.now(),
                            fromAi = true
                        )
                    }

                } catch (e: Exception) {
                    android.util.Log.e("API_DEBUG", "MANUEL PARSE HATASI: $jsonString", e)
                    AiMessage(
                        id = UUID.randomUUID().toString(),
                        message = "Teknik bir sorun oluştu.",
                        createdAt = Clock.System.now(),
                        fromAi = true
                    )
                }
            }
        )
    }
}