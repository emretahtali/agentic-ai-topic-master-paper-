package com.ellitoken.myapplication.presentation.screens.home.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ellitoken.myapplication.data.remote.model.AppointmentData

@Composable
fun UpcomingAppointmentsSection(
    appointments: List<AppointmentData>,
    onAppointmentClick: (AppointmentData) -> Unit
) {
    val sortedAppointments = remember(appointments) {
        appointments.sortedBy { it.dateTime }
    }

    val filteredAppointmets = remember(sortedAppointments) {
        sortedAppointments.filter { it.status != "CANCEL" }
    }

    Column(
        modifier = Modifier.fillMaxWidth()
    ) {
        Text(
            text = "Yaklaşan Randevularınız",
            fontWeight = FontWeight.Bold,
            fontSize = 16.sp,
            modifier = Modifier
                .padding(horizontal = 24.dp)
        )

        Spacer(modifier = Modifier.height(4.dp))

        LazyRow(
            contentPadding = PaddingValues(horizontal = 24.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(
                items = filteredAppointmets,
                key = { it.id }
            ) { appointment ->
                AppointmentCard(
                    dateTime = appointment.dateTime,
                    doctorName = appointment.doctorName,
                    patientName = appointment.patientName,
                    hospitalName = appointment.hospitalName,
                )
            }
        }
    }
}