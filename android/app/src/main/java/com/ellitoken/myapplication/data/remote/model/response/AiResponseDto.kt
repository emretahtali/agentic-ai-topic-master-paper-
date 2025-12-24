package com.ellitoken.myapplication.data.remote.model.response

import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import kotlinx.datetime.Clock
import java.util.UUID
import kotlinx.serialization.Serializable


@Serializable
data class AiResponseWrapper(
    val response: List<AiResponseItem>
)

@Serializable
data class AiResponseItem(
    val type: String,
    val text: String
)

fun AiResponseWrapper.toDomain(): AiMessage {
    val messageText = this.response.firstOrNull { it.type == "text" }?.text ?: ""

    return AiMessage(
        id = UUID.randomUUID().toString(),
        message = messageText,
        createdAt = Clock.System.now(),
        fromAi = true
    )
}