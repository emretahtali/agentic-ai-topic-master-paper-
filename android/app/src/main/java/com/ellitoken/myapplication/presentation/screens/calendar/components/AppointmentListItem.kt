package com.ellitoken.myapplication.presentation.screens.calendar.components

import AppointmentStatusBadge
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.ui.theme.appBlue
import com.ellitoken.myapplication.presentation.screens.calendar.viewmodel.AppointmentWithStatus
import com.ellitoken.myapplication.ui.theme.appWhite

@Composable
fun AppointmentListItem(
    appointmentWithStatus: AppointmentWithStatus,
    onEditClick: () -> Unit,
    onCancelClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.DateRange,
                        contentDescription = "Randevu Zamanı",
                        tint = appBlue,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = appointmentWithStatus.data.dateTime,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.Black
                    )
                }
                AppointmentStatusBadge(status = appointmentWithStatus.status)
            }

            Spacer(modifier = Modifier.height(12.dp))
            Divider(
                color = Color(0xFFF0F0F0),
                thickness = 1.dp
            )
            Spacer(modifier = Modifier.height(12.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.LocationOn,
                    contentDescription = "Hastane",
                    tint = Color.Gray,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = appointmentWithStatus.data.hospitalName,
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = "Doktor",
                    tint = Color.Gray,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = appointmentWithStatus.data.doctorName,
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            if (appointmentWithStatus.status != "Tamamlandı") {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    ActionButton(
                        text = "Düzenle",
                        onClick = onEditClick,
                        isPrimary = true,
                        modifier = Modifier.weight(1f)
                    )
                    ActionButton(
                        text = "İptal Et",
                        onClick = onCancelClick,
                        isPrimary = false,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}


@Composable
fun ActionButton(
    text: String,
    onClick: () -> Unit,
    isPrimary: Boolean,
    modifier: Modifier = Modifier
) {
    val containerColor: Color
    val contentColor: Color
    val borderColor: Color
    val elevation = ButtonDefaults.buttonElevation(defaultElevation = 2.dp)

    if (isPrimary) {
        containerColor = appBlue
        contentColor = appWhite
        borderColor = Color.Transparent
    } else {
        containerColor = Color(0xFFFFCDD2)
        contentColor = Color(0xFFD32F2F)
        borderColor = Color.Transparent
    }

    Button(
        onClick = onClick,
        modifier = modifier.height(50.dp),
        shape = RoundedCornerShape(15.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = containerColor,
            contentColor = contentColor
        ),
        border = BorderStroke(1.dp, borderColor),
        elevation = elevation
    ) {
        Text(
            text = text,
            fontWeight = FontWeight.SemiBold,
            fontSize = 15.sp
        )
    }
}