package com.ellitoken.myapplication.data.remote.repository

import com.ellitoken.myapplication.data.remote.model.AppointmentData
import com.ellitoken.myapplication.utils.NetworkError
import com.ellitoken.myapplication.utils.Result

interface CalendarChatRepository {
    suspend fun getAppointments(): Result<List<AppointmentData>, NetworkError>
}