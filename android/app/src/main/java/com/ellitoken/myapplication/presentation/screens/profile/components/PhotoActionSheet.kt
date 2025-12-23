package com.ellitoken.myapplication.presentation.screens.profile.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddAPhoto
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.ui.theme.appBlue
import com.ellitoken.myapplication.ui.theme.appWhite

@Composable
fun PhotoActionSheet(
    onDismissRequest: () -> Unit,
    onPickFromGallery: () -> Unit,
    onTakePhoto: () -> Unit
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp)),
        color = Color.White,
        shadowElevation = 8.dp,
        tonalElevation = 4.dp
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            DefaultIconButton(
                text = "Galeriden Seç",
                iconVector = Icons.Default.AddAPhoto,
                onClick = {
                    onPickFromGallery()
                    onDismissRequest()
                },
                modifier = Modifier.fillMaxWidth(0.9f)
            )

            DefaultIconButton(
                text = "Fotoğraf Çek",
                iconVector = Icons.Default.AddAPhoto,
                onClick = {
                    onTakePhoto()
                    onDismissRequest()
                },
                modifier = Modifier.fillMaxWidth(0.9f)
            )

            Spacer(modifier = Modifier.height(8.dp))
        }
    }
}

@Composable
fun DefaultIconButton(
    modifier: Modifier = Modifier,
            text: String,
    iconRes: Int? = null,
    iconVector: ImageVector? = null,
    onClick: () -> Unit,
) {
    OutlinedButton(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp)
            .height(56.dp),
        shape = RoundedCornerShape(14.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = appBlue,
            disabledContainerColor = appWhite,
            contentColor = appWhite
        )
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {

            when {
                iconRes != null -> {
                    Icon(
                        painter = painterResource(id = iconRes),
                        contentDescription = null,
                        modifier = Modifier.size(24.dp),
                        tint = Color.Unspecified
                    )
                }
                iconVector != null -> {
                    Icon(
                        imageVector = iconVector,
                        contentDescription = null,
                        modifier = Modifier.size(24.dp),
                        tint = Color.Unspecified
                    )
                }
            }

            Spacer(modifier = Modifier.width(10.dp))

            Text(
                text = text,
                color = Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium
            )
        }
    }
}
