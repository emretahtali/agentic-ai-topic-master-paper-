package com.ellitoken.myapplication.presentation.screens.chatsupport.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.R

@Composable
fun AiChatScreenTopBar(
    onBackClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .padding(vertical = 5.dp).padding(start = 7.dp)
            .background(Color.White),
        verticalAlignment = Alignment.CenterVertically
    ) {

        IconButton(
            onClick = onBackClick
        ) {
            Icon(
                painter = painterResource(id = R.drawable.ic_button_back),
                contentDescription = "Geri",
                tint = Color.Black,
                modifier = Modifier
                    .padding(10.dp)
            )
        }
        Spacer(modifier = Modifier.width(5.dp))

        Image(
            painter = painterResource(R.drawable.ic_profile_placeholder),
            modifier = Modifier
                .size(50.dp)
                .clip(CircleShape),
            contentDescription = ""
        )

        Spacer(modifier = Modifier.width(12.dp))

        Text(
            text = "ARAT AI",
            fontWeight = FontWeight.SemiBold,
            fontSize = 19.sp,
            color = Color.Black,
        )
    }
}