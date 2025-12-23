package com.ellitoken.myapplication.presentation.screens.home.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlack
import com.ellitoken.myapplication.ui.theme.appBlue
import com.ellitoken.myapplication.ui.theme.appFirstGray
import com.ellitoken.myapplication.ui.theme.appWhite

@Composable
fun AppointmentCard(
    dateTime: String,
    doctorName: String,
    patientName: String,
    hospitalName: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    ElevatedCard(
        onClick = onClick,
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        modifier = modifier
            .width(220.dp)
            .background(appWhite),

    ) {
        Column(
            modifier = Modifier
                .padding(12.dp)
                .fillMaxWidth(),
        ) {
            Text(
                text = dateTime,
                fontSize = 14.sp,
                color = appBlue,
                lineHeight = 24.sp,
                fontWeight = FontWeight.Normal
            )

            Text(
                text = doctorName,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                lineHeight = 24.sp,
                color = appBlack
            )

            Text(
                text = patientName,
                fontSize = 14.sp,
                fontWeight = FontWeight.Normal,
                lineHeight = 24.sp,
                color = appFirstGray
            )

            Text(
                text = hospitalName,
                fontSize = 14.sp,
                fontWeight = FontWeight.Normal,
                lineHeight = 24.sp,
                color = appFirstGray
            )
        }
    }
}