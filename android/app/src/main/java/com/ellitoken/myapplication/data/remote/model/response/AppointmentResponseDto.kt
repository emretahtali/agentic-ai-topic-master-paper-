package com.ellitoken.myapplication.data.remote.model.response

import com.ellitoken.myapplication.data.remote.model.AppointmentData
import kotlinx.serialization.Serializable

@Serializable
data class RawAppointmentResponse(
    val respond: String
)

@Serializable
data class SingleAppointmentDto(
    val appointment_id: String,
    val date: String,
    val time: String,
    val doctor: String,
    val hospital: String,
    val status: String
)