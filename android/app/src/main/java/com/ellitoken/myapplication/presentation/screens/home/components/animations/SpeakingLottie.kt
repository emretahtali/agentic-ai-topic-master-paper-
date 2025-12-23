package com.ellitoken.myapplication.presentation.screens.home.components.animations

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.LottieConstants
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition
import com.ellitoken.myapplication.R

@Composable
fun SpeakingLottie(
    modifier: Modifier = Modifier,
    isPlaying: Boolean = true,
) {
    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(R.raw.voice_animation)
    )
    val progress by animateLottieCompositionAsState(
        composition = composition,
        iterations = LottieConstants.IterateForever,
        isPlaying = isPlaying,
        speed = 1f
    )
    LottieAnimation(
        composition = composition,
        progress = { progress },
        modifier = modifier
    )
}