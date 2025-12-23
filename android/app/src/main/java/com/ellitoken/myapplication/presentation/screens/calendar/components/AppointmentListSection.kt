package com.ellitoken.myapplication.presentation.screens.calendar.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.presentation.screens.calendar.viewmodel.AppointmentWithStatus

@Composable
fun AppointmentListSection(
    title: String,
    appointments: List<AppointmentWithStatus>
) {
    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
        Text(
            text = title,
            fontWeight = FontWeight.Bold,
            fontSize = 18.sp,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        LazyColumn(
            contentPadding = PaddingValues(vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(appointments, key = { it.data.id }) { appointmentWithStatus ->
                AppointmentListItem(
                    appointmentWithStatus = appointmentWithStatus,
                    onEditClick = { /* TODO:Appointment Edit Process */ },
                    onCancelClick = { /* TODO: Appointment Cancel Process */ }
                )
            }
        }
    }
}