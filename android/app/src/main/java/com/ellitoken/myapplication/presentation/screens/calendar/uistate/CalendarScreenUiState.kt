package com.ellitoken.myapplication.presentation.screens.calendar.uistate

import com.ellitoken.myapplication.data.remote.model.AppointmentData

data class CalendarScreenUiState(
    val isLoading: Boolean = false,
    val upcomingAppointments: List<AppointmentData> = emptyList(),
    val pastAppointments: List<AppointmentData> = emptyList(),
    val selectedTab: AppointmentTab = AppointmentTab.UPCOMING
)

enum class AppointmentTab {
    UPCOMING, PAST
}