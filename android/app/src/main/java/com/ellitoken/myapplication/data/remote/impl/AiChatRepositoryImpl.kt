package com.ellitoken.myapplication.data.remote.impl

import com.ellitoken.myapplication.data.remote.ApiClient
import com.ellitoken.myapplication.data.remote.repository.AiChatRepository
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import com.ellitoken.myapplication.utils.NetworkError
import kotlinx.coroutines.flow.Flow
import com.ellitoken.myapplication.utils.Result
import kotlinx.serialization.json.Json

class AiChatRepositoryImpl(
    private val apiClient: ApiClient
) : AiChatRepository {

    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun streamAiMessage(prompt: String): Flow<Result<AiMessage, NetworkError>> {
        val requestBody = mapOf("prompt" to prompt)

        return apiClient.streamJsonAsFlow(
            endpoint = "genai/send-message",
            authType = com.ellitoken.myapplication.data.remote.AuthType.ACCESS,
            requestType = com.ellitoken.myapplication.data.remote.RequestType.POST,
            body = requestBody,
            serializer = { line -> json.decodeFromString<AiMessage>(line) }
        )
    }
}