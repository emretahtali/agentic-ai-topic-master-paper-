package com.ellitoken.myapplication.presentation.screens.profile.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlack
import com.ellitoken.myapplication.ui.theme.appFirstGray

@Composable
fun LineDisaseInfo(modifier : Modifier = Modifier, text : String, onClick : () -> Unit) {
    Row (modifier = modifier, horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically ){
            Text(
                text = text,
                color = Color.Black,
                fontSize = 14.sp,
                fontWeight = FontWeight.Medium
            )


        IconButton(onClick = {onClick()}
        ) {
            Icon(
                imageVector = Icons.Filled.ArrowForward,
                contentDescription = "Add",
                tint = appBlack,
                modifier = Modifier.size(20.dp)
            )
        }

    }
}