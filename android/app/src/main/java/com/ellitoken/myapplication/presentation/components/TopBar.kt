package com.ellitoken.myapplication.presentation.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlack

@Composable
fun TopBar(
    title: String,
    onBackClick: () -> Unit
) {

    Box(
        Modifier.fillMaxWidth(),
        contentAlignment = Alignment.Center
    ){
        IconButton(
            onClick = onBackClick,
            modifier = Modifier.align(Alignment.CenterStart).offset(x = (-10).dp)
        ) {

            Icon(
                imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                tint = appBlack,
                contentDescription = "Geri",
                modifier = Modifier.size(24.dp)
            )
        }

        Text(
            modifier = Modifier.align(Alignment.Center),
            text = title,
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Black
        )
    }
}