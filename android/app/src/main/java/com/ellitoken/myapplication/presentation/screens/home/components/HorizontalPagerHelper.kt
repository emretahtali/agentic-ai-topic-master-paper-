package com.ellitoken.myapplication.presentation.screens.home.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlack
import com.ellitoken.myapplication.ui.theme.appBlue

@Composable
fun HealthInfoPage(
    question: String,
    isChecked: Boolean,
    description: String,
    onCheckedChanged: (Boolean) -> Unit,
    onDescriptionChanged: (String) -> Unit
) {
    val selectedButtonColor = Color(0xFF34C759)
    val selectedTextColor = Color.White
    val unselectedButtonColor = Color.LightGray.copy(alpha = 0.6f)
    val unselectedTextColor = appBlack

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp, vertical = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Top
    ) {
        Text(
            text = question,
            color = appBlack,
            fontSize = 20.sp,
            fontWeight = FontWeight.Normal,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(24.dp))

        Row(
            modifier = Modifier.fillMaxWidth(0.9f),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            DefaultIconButton(
                text = "Evet",
                onClick = { onCheckedChanged(true) },
                modifier = Modifier.weight(1f),
                buttonColor = if (isChecked) selectedButtonColor else unselectedButtonColor,
                textColor = if (isChecked) selectedTextColor else unselectedTextColor
            )

            DefaultIconButton(
                text = "Hayır",
                onClick = { onCheckedChanged(false) },
                modifier = Modifier.weight(1f),
                buttonColor = if (!isChecked) selectedButtonColor else unselectedButtonColor,
                textColor = if (!isChecked) selectedTextColor else unselectedTextColor,
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (isChecked) {
            OutlinedTextField(
                value = description,
                onValueChange = onDescriptionChanged,
                placeholder = { Text(text = "Lütfen detay sağlayın.", fontWeight = FontWeight.Normal, fontSize = 16.sp) },
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .height(90.dp),
                shape = RoundedCornerShape(14.dp),
                maxLines = 3,
                textStyle = TextStyle(
                    fontWeight = FontWeight.Normal,
                    fontSize = 16.sp
                )
            )
        }
    }
}

@Composable
private fun DefaultIconButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    buttonColor: Color = Color(0xFF34C759),
    textColor: Color = Color.White,
    topPadding: Int = 8,
    bottomPadding: Int = 8,
    enabled: Boolean = true,
    isLoading: Boolean = false
) {
    Button(
        enabled = enabled,
        onClick = onClick,
        modifier = modifier
            .padding(top = topPadding.dp, bottom = bottomPadding.dp)
            .height(56.dp),
        shape = RoundedCornerShape(14.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = buttonColor,
            disabledContainerColor = buttonColor.copy(alpha = 0.5f)
        )
    ) {
        if (isLoading){
            CircularProgressIndicator(
                modifier = Modifier.size(12.dp),
                color = Color.White,
                strokeWidth = 2.dp
            )
        }
        else{
            Row(
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = text,
                    color = textColor,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}


@Composable
fun PagerIndicator(pageCount: Int, currentPage: Int) {
    Row(
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 16.dp)
    ) {
        repeat(pageCount) { iteration ->
            val color = if (currentPage == iteration) appBlue else Color.LightGray
            Box(
                modifier = Modifier
                    .padding(4.dp)
                    .clip(CircleShape)
                    .background(color)
                    .size(10.dp)
            )
        }
    }
}