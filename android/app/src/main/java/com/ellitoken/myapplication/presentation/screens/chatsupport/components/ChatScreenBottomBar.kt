package com.ellitoken.myapplication.presentation.screens.chatsupport.components

import androidx.compose.runtime.Composable
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.ui.theme.appBlack

@Composable
fun ChatScreenBottomBar(
    inputText: TextFieldValue,
    onInputChange: (TextFieldValue) -> Unit,
    onSendClick: () -> Unit,
    onAttachClick: () -> Unit,
    onMicClick: () -> Unit,
    isSendButtonActive: Boolean = true
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .padding(horizontal = 7.dp, vertical = 6.dp)
            .padding(bottom = 10.dp),
        verticalAlignment = Alignment.Bottom
    ) {
        IconButton(onClick = onAttachClick) {
            Icon(
                painter = painterResource(R.drawable.ic_attach),
                contentDescription = "Attach",
                tint = appBlack,
                modifier = Modifier.size(24.dp)
            )
        }

        ChatTextField(
            value        = inputText,
            onValueChange= onInputChange,
            onSend       = onSendClick,
            modifier     = Modifier
                .weight(1f)
                .padding(horizontal = 4.dp),
            textFontSize       = 16,
            placeholderFontSize= 14
        )

        Spacer(Modifier.width(4.dp))


        //Bu doğru olanı ama şu anda daha mesaja ses gönderme olmayacağı için şuanlık kapatıyoruz.
        /*
        if (inputText.text.isNotBlank()) {
            IconButton(onClick = onSendClick) {
                Icon(
                    imageVector = Icons.Default.Send,
                    contentDescription = "Send",
                    tint = green700,
                    modifier = Modifier.size(28.dp)
                )
            }
        } else {
            IconButton(onClick = onMicClick) {
                Icon(
                    painter = painterResource(R.drawable.ic_microphone),
                    contentDescription = "Mic",
                    tint = green700,
                    modifier = Modifier.size(30.dp)
                )
            }
        }
        */

        IconButton(onClick = onSendClick,
            enabled = isSendButtonActive) {
            Icon(
                imageVector = Icons.Default.Send,
                contentDescription = "Send",
                tint = if(isSendButtonActive) appBlack else Color.Gray,
                modifier = Modifier.size(28.dp)
            )
        }

    }
}