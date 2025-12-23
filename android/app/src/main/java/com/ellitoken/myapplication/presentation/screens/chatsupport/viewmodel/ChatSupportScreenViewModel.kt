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
            val messages = _uiState.value.messages.toMutableList()

            val userMessage = AiMessage(
                id = UUID.randomUUID().toString(),
                createdAt = Clock.System.now(),
                message = prompt,
                fromAi = false
            )

            messages.add(0, userMessage)

            _uiState.update {
                it.copy(messages = messages, textFieldValue = TextFieldValue(), isLoading = true)
            }

            aiChatRepository.streamAiMessage(prompt).collect { result ->

                result.onSuccess { receivedAiMessage ->

                    _uiState.update { currentState ->
                        val updatedMessages = currentState.messages.toMutableList()

                        val index = updatedMessages.indexOfFirst { it.id == receivedAiMessage.id }

                        if (index != -1) {
                            val existingAiMessage = updatedMessages[index]
                            updatedMessages[index] = existingAiMessage.copy(
                                message = existingAiMessage.message + receivedAiMessage.message
                            )
                        } else {
                            updatedMessages.add(0, receivedAiMessage)
                        }

                        currentState.copy(messages = updatedMessages, isLoading = false)
                    }

                }.onError { networkError ->

                    val errorMessage = AiMessage(
                        id = UUID.randomUUID().toString(),
                        createdAt = Clock.System.now(),
                        message = "Hata: ${networkError.message}",
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