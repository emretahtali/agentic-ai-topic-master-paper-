package com.alpermelkeli.sorugram.presentation.screens.aichatscreen.components

import android.annotation.SuppressLint
import androidx.compose.foundation.layout.Row
import androidx.compose.runtime.Composable
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import dev.jeziellago.compose.markdowntext.MarkdownText


@SuppressLint("UnusedBoxWithConstraintsScope")
@Composable
fun AiMessageItem(
    aiMessage: AiMessage
) {

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp, vertical = 6.dp),
        horizontalArrangement = if (!aiMessage.fromAi) Arrangement.End else Arrangement.Start
    ) {

        BoxWithConstraints {
            val maxBubbleWidth = maxWidth * 0.80f

            val mineColor = Color(0xFFD5E5D6)
            val otherColor = Color(0xFFF3FBF6)


            Box(
                modifier = Modifier
                    .requiredWidthIn(max = maxBubbleWidth)
                    .background(
                        color = if (!aiMessage.fromAi) mineColor else otherColor,
                        shape = RoundedCornerShape(12.dp)
                    )
                    .padding(horizontal = 8.dp, vertical = 8.dp)
            ) {
                MarkdownText(
                    markdown = aiMessage.message,
                    style = TextStyle(
                        fontSize = 18.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Medium
                    )
                )
            }
        }
    }
}