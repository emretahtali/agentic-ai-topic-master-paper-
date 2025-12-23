package com.ellitoken.myapplication.presentation.screens.home.components

import android.media.MediaPlayer
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.presentation.screens.home.components.animations.ProcessingAnimation
import com.ellitoken.myapplication.presentation.screens.home.components.animations.ListeningLottie
import com.ellitoken.myapplication.presentation.screens.home.components.animations.SpeakingLottie
import com.ellitoken.myapplication.presentation.screens.home.uistate.VoiceState
import com.ellitoken.myapplication.ui.theme.appBlack
import androidx.compose.ui.platform.LocalContext

@Composable
fun VoiceInputCardFinal(
    isSpeaking: Boolean,
    setSpeaking: (Boolean) -> Unit,
    voiceState: VoiceState,
    onMicClick: () -> Unit,
    onStopListening: () -> Unit,
) {

    val mp = MediaPlayer.create(LocalContext.current, R.raw.statechange)

    DisposableEffect(Unit) {
        onDispose {
            mp.release()
        }
    }

    ElevatedCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .height(180.dp),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            when (voiceState) {

                is VoiceState.Idle -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            Modifier
                                .size(120.dp)
                                .clip(CircleShape)
                                .clickable {
                                    onMicClick()
                                }
                        ) {
                            Image(
                                painter = painterResource(id = R.drawable.homescreen_ic_voice),
                                contentDescription = "Dinlemeyi Başlat",
                                modifier = Modifier.fillMaxSize().offset(y = 8.dp)
                            )
                        }

                        Text(
                            text = "Konuşmayı Başlat",
                            color = appBlack,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Medium
                        )
                    }
                }

                is VoiceState.Listening -> {
                    Box(
                        modifier = Modifier
                            .size(120.dp)
                            .clip(CircleShape)
                            .clickable {
                                onStopListening()
                                mp.start()
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        ListeningLottie()
                    }
                }

                is VoiceState.Processing -> {
                    ProcessingAnimation()
                }

                is VoiceState.Speaking -> {
                    SpeakingLottie(
                        modifier = Modifier.size(160.dp),
                        isPlaying = isSpeaking,
                    )
                }
            }
        }
    }
}