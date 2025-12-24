package com.ellitoken.myapplication.data.remote.model.response

import kotlinx.serialization.Serializable


@Serializable
data class AiResponseDto(
    val response: String
)