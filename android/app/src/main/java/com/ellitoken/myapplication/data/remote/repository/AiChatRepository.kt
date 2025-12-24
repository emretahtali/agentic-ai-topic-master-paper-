package com.ellitoken.myapplication.data.remote.repository

import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import com.ellitoken.myapplication.utils.NetworkError
import kotlinx.coroutines.flow.Flow
import com.ellitoken.myapplication.utils.Result

interface AiChatRepository {
    suspend fun streamAiMessage(prompt: String, threadId: String, clientTurnId: String): Flow<Result<AiMessage, NetworkError>>
}