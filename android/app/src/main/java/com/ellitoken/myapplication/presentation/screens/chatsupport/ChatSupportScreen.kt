package com.ellitoken.myapplication.presentation.screens.chatsupport

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.navigation.NavController
import com.alpermelkeli.sorugram.presentation.screens.aichatscreen.components.AiMessageItem
import com.alpermelkeli.sorugram.presentation.screens.aichatscreen.components.AiMessageLoadingItem
import com.ellitoken.myapplication.presentation.screens.chatsupport.components.AiChatScreenTopBar
import com.ellitoken.myapplication.presentation.screens.chatsupport.components.ChatScreenBottomBar
import com.ellitoken.myapplication.presentation.screens.chatsupport.viewmodel.ChatSupportScreenViewModel
import org.koin.androidx.compose.getViewModel

@Composable
fun ChatSupportScreen(
    navController: NavController,
    viewModel: ChatSupportScreenViewModel = getViewModel()
) {
    val uiState = viewModel.uiState.collectAsState().value
    val listState = rememberLazyListState()

    LaunchedEffect(uiState.messages.size) {
        if (uiState.messages.isNotEmpty()) {
            listState.animateScrollToItem(0)
        }
    }

    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .imePadding(),
        topBar = {
            AiChatScreenTopBar(onBackClick = { navController.popBackStack() })
        },
        bottomBar = {
            ChatScreenBottomBar(
                inputText = uiState.textFieldValue,
                onInputChange = { viewModel.onTextValueChanged(it) },
                onSendClick = { viewModel.sendMessage() },
                onAttachClick = {},
                onMicClick = {},
                isSendButtonActive = uiState.textFieldValue.text.isNotBlank() && !uiState.isLoading
            )
        }
    ) { padding ->
        LazyColumn(
            reverseLayout = true,
            state = listState,
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color.White),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (uiState.isLoading) {
                item { AiMessageLoadingItem() }
            }

            items(
                items = uiState.messages,
                key = { it.id }
            ) { msg ->
                AiMessageItem(aiMessage = msg)
            }
        }
    }
}