package com.ellitoken.myapplication.presentation.screens.home.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.ui.theme.appBlack
import com.ellitoken.myapplication.ui.theme.appFirstGray
import com.ellitoken.myapplication.ui.theme.appWhite

@Composable
fun HomeScreenTopBar(
    userName: String,
    profileImageUrl: String?,
    onClickProfile: () -> Unit,
    modifier: Modifier = Modifier,
    placeholderResId: Int = R.drawable.ic_profile_placeholder
) {
    Row(
        modifier = modifier
            .fillMaxWidth().background(appWhite)
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(end = 12.dp)
        ) {
            Text(
                text = "Merhaba, $userName",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = appBlack,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = "Size nasıl yardımcı olabilirim?",
                fontSize = 16.sp,
                fontWeight = FontWeight.Normal,
                color = appFirstGray,
                maxLines = 1
            )
        }

        IconButton(modifier = Modifier.size(48.dp), onClick = onClickProfile, ) {
            if (profileImageUrl.isNullOrBlank()) {
                Icon(
                    painter = painterResource(id = placeholderResId),
                    contentDescription = "Profil",
                    tint = Color.Unspecified,
                    modifier = Modifier.fillMaxSize(),
                )
            } else {
                AsyncImage(
                    model = profileImageUrl,
                    contentDescription = "Profil",
                    placeholder = painterResource(id = placeholderResId),
                    error = painterResource(id = placeholderResId),
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    }
}
