package com.ellitoken.myapplication.presentation.screens.home.uistate

import com.ellitoken.myapplication.data.remote.model.User
import java.io.File

data class HomeScreenUiState(
    val isLoading: Boolean = true,
    val user: User? = null,
    val isHealthSurveySheetOpen: Boolean = false,
    val voiceState: VoiceState = VoiceState.Idle,
    val isMicClicked: Boolean = false,
    val isSpeaking: Boolean = false,
    val processedAudioFile: File? = null
)


sealed class VoiceState {
    object Idle : VoiceState()
    data class Listening(var amplitude: Float = 0f) : VoiceState()
    object Processing : VoiceState()
    object Speaking : VoiceState()
}
