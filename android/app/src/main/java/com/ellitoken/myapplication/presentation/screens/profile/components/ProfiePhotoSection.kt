package com.ellitoken.myapplication.presentation.screens.profile.components

import android.net.Uri
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.rememberAsyncImagePainter
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.ui.theme.appBlack
import androidx.core.net.toUri

@Composable
fun ProfilePhotoSection(
    modifier: Modifier = Modifier,
    imageUrl: String,
    onPhotoClick: () -> Unit = {}
) {
    Column(modifier = modifier, horizontalAlignment = Alignment.CenterHorizontally) {

        val model: Any =
            if (imageUrl.startsWith("content://")) imageUrl.toUri()
            else imageUrl

        val painter = if (imageUrl.isNotBlank()) {
            rememberAsyncImagePainter(
                model = model,
                placeholder = painterResource(R.drawable.ic_profile_placeholder),
                error       = painterResource(R.drawable.ic_profile_placeholder)
            )
        } else {
            painterResource(R.drawable.ic_profile_placeholder)
        }

        Box(
            modifier = Modifier
                .size(86.dp)
        ) {
            Image(
                painter = painter,
                contentDescription = "Profil Fotoğrafı",
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxSize()
                    .clip(CircleShape)
                    .clickable(onClick = onPhotoClick)
            )

            Image(
                painter = painterResource(R.drawable.ic_profilesettings_uploadphoto),
                contentDescription = "Fotoğraf Yükle",
                modifier = Modifier
                    .size(36.dp)
                    .align(Alignment.BottomEnd)
                    .offset(y = 5.dp, x = 5.dp).clickable(onClick = onPhotoClick),

            )
        }

        Spacer(Modifier.height(6.dp))

        Text(
            text = "Profil Fotoğrafını Değiştir",
            modifier = Modifier.clickable { onPhotoClick() },
            fontSize = 14.sp,
            fontWeight = FontWeight.Medium,
            color = appBlack,
        )
    }
}
