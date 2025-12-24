package com.ellitoken.myapplication.presentation.screens.chatsupport.viewmodel

import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ellitoken.myapplication.data.remote.repository.AiChatRepository
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.ChatSupportScreenUiState
import com.ellitoken.myapplication.utils.onError
import com.ellitoken.myapplication.utils.onSuccess
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.datetime.Clock
import java.util.UUID

class ChatSupportScreenViewModel(
    private val aiChatRepository: AiChatRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ChatSupportScreenUiState())
    val uiState = _uiState.asStateFlow()

    fun onTextValueChanged(value: TextFieldValue) {
        _uiState.update { it.copy(textFieldValue = value) }
    }

    fun sendMessage() {
        val prompt = uiState.value.textFieldValue.text
        if (prompt.isBlank()) return

        viewModelScope.launch {
            _uiState.update { currentState ->
                val messages = currentState.messages.toMutableList()
                val userMessage = AiMessage(
                    id = UUID.randomUUID().toString(),
                    createdAt = Clock.System.now(),
                    message = prompt,
                    fromAi = false
                )
                messages.add(0, userMessage)

                currentState.copy(
                    messages = messages,
                    textFieldValue = TextFieldValue(),
                    isLoading = true
                )
            }

            var currentAiMessageId: String? = null

            aiChatRepository.streamAiMessage(prompt).collect { result ->

                result.onSuccess { receivedAiMessage ->
                    android.util.Log.d("VIEWMODEL_DEBUG", "Veri Geldi: ${receivedAiMessage.message}")

                    _uiState.update { currentState ->
                        val updatedMessages = currentState.messages.toMutableList()

                        val index = if (currentAiMessageId != null) {
                            updatedMessages.indexOfFirst { it.id == currentAiMessageId }
                        } else {
                            -1
                        }

                        if (index != -1) {
                            val existingMessage = updatedMessages[index]
                            updatedMessages[index] = existingMessage.copy(

                                message = existingMessage.message + receivedAiMessage.message
                            )
                        } else {
                            currentAiMessageId = receivedAiMessage.id
                            updatedMessages.add(0, receivedAiMessage)
                        }

                            currentState.copy(messages = updatedMessages, isLoading = false)
                    }

                }.onError { networkError ->
                    android.util.Log.e("VIEWMODEL_DEBUG", "Hata: ${networkError.message}")

                    val errorMessage = AiMessage(
                        id = UUID.randomUUID().toString(),
                        createdAt = Clock.System.now(),
                        message = "⚠️ Hata: ${networkError.message}",
                        fromAi = true
                    )

                    _uiState.update { currentState ->
                        val updatedMessages = currentState.messages.toMutableList()
                        updatedMessages.add(0, errorMessage)
                        currentState.copy(messages = updatedMessages, isLoading = false)
                    }
                }
            }
        }
    }
}