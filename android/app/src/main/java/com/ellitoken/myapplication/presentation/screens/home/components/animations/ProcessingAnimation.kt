package com.ellitoken.myapplication.presentation.screens.home.components.animations

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.ellitoken.myapplication.ui.theme.appBlue

@Composable
fun ProcessingAnimation() {
    val transition = rememberInfiniteTransition()

    val alpha1 by transition.animateFloat(
        initialValue = 0.2f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse,
        )
    )
    val alpha2 by transition.animateFloat(
        initialValue = 0.2f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse,
            initialStartOffset = StartOffset(200) // 200ms sonra başla
        )
    )
    val alpha3 by transition.animateFloat(
        initialValue = 0.2f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse,
            initialStartOffset = StartOffset(400) // 400ms sonra başla
        )
    )

    Row(
        horizontalArrangement = Arrangement.spacedBy(12.dp) // Daireler arası boşluk
    ) {
        Canvas(modifier = Modifier.size(20.dp)) {
            drawCircle(color =  appBlue.copy(alpha = alpha1))
        }
        Canvas(modifier = Modifier.size(20.dp)) {
            drawCircle(color = appBlue.copy(alpha = alpha2))
        }
        Canvas(modifier = Modifier.size(20.dp)) {
            drawCircle(color = appBlue.copy(alpha = alpha3))
        }
    }
}