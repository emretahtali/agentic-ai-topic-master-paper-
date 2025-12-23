package com.ellitoken.myapplication.presentation.screens.chatsupport.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ChatTextField(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    onSend: () -> Unit,
    modifier: Modifier = Modifier,
    textFontSize: Int = 16,
    placeholderText: String = "Mesaj yazın…",
    placeholderFontSize: Int = 14
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = 48.dp)
            .background(Color(0xFFF2F2F2), RoundedCornerShape(20.dp))
            .padding(horizontal = 12.dp, vertical = 8.dp),
        contentAlignment = Alignment.TopStart
    ) {
        /* Placeholder */
        if (value.text.isEmpty()) {
            Text(
                text = placeholderText,
                fontSize = placeholderFontSize.sp,
                color = Color.Gray.copy(alpha = 0.7f),
                textAlign = TextAlign.Start,
                modifier = Modifier.align(Alignment.CenterStart)
            )
        }

        BasicTextField(
            value = value,
            onValueChange = onValueChange,
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.CenterStart)
                .onPreviewKeyEvent { ev ->
                    if (ev.key == Key.Enter && ev.type == KeyEventType.KeyUp) {
                        onSend(); true
                    } else false
                },
            textStyle = TextStyle(
                color = Color.Black,
                fontSize = textFontSize.sp,
                lineHeight = (textFontSize + 4).sp,
                textAlign = TextAlign.Start
            ),
            cursorBrush = SolidColor(Color.Black),
            singleLine = false,
            maxLines = 6,

            //real klavye için enter bastığında gönderir
            keyboardOptions = KeyboardOptions(
                imeAction = ImeAction.Send
            ),
            keyboardActions = KeyboardActions(
                onSend = {
                    onSend()
                }
            )
        )
    }
}
