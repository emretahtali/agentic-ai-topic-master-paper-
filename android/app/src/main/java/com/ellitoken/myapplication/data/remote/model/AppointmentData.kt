package com.ellitoken.myapplication.data.remote.model

import kotlinx.serialization.Serializable

@Serializable
data class AppointmentData(
    val id: String,
    val dateTime: String,
    val doctorName: String,
    val patientName: String,
    val hospitalName: String,
    val status: String
)
