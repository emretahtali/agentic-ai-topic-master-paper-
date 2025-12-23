package com.ellitoken.myapplication.presentation.screens.calendar.uistate

import com.ellitoken.myapplication.presentation.screens.calendar.viewmodel.AppointmentWithStatus

data class CalendarScreenUiState(
    val isLoading: Boolean = false,
    val upcomingAppointments: List<AppointmentWithStatus> = emptyList(),
    val pastAppointments: List<AppointmentWithStatus> = emptyList(),
    val selectedTab: AppointmentTab = AppointmentTab.UPCOMING
)

enum class AppointmentTab {
    UPCOMING, PAST
}