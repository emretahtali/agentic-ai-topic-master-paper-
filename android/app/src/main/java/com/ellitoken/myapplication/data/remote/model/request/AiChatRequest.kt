package com.ellitoken.myapplication.data.remote.model.request

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class AiChatRequest(
    val input: InputData,

    @SerialName("thread_id")
    val threadId: String,

    @SerialName("client_turn_id")
    val clientTurnId: String
)

@Serializable
data class InputData(
    val message: String
)