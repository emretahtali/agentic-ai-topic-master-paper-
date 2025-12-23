package com.ellitoken.myapplication.data.remote.model

data class AppointmentData(
    val id: String,
    val dateTime: String,
    val doctorName: String,
    val patientName: String,
    val hospitalName: String

)

val upcomingAppointments = listOf(
    AppointmentData(
        id = "1",
        dateTime = "12 Ağustos 2025 - 14:30",
        doctorName = "Dr. Kerem Üzer",
        patientName = "Yusuf Asım Demirhan",
        hospitalName = "Acıbadem Hastanesi"
    ),
    AppointmentData(
        id = "2",
        dateTime = "15 Ağustos 2025 - 09:00",
        doctorName = "Dr. Zeynep Yorulmaz",
        patientName = "Yusuf Asım Demirhan",
        hospitalName = "Medicana"
    ),
    AppointmentData(
        id = "3",
        dateTime = "5 Ağustos 2025 - 09:40",
        doctorName = "Dr. Muhammed Taşkın",
        patientName = "Yusuf Asım Demirhan",
        hospitalName = "Bilkent Şehir Hastanesi"
    ),
)