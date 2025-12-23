package com.ellitoken.myapplication.presentation.screens.calendar.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ellitoken.myapplication.data.remote.model.AppointmentData
import com.ellitoken.myapplication.data.remote.model.upcomingAppointments
import com.ellitoken.myapplication.presentation.screens.calendar.uistate.AppointmentTab
import com.ellitoken.myapplication.presentation.screens.calendar.uistate.CalendarScreenUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class AppointmentWithStatus(
    val data: AppointmentData,
    val status: String
)

val dummyUpcomingAppointmentsWithStatus = listOf(
    AppointmentWithStatus(
        data = upcomingAppointments[0],
        status = "Onaylandı"
    ),
    AppointmentWithStatus(
        data = upcomingAppointments[1],
        status = "Beklemede"
    ),
    AppointmentWithStatus(
        data = upcomingAppointments[2],
        status = "Onaylandı"
    )
)

val dummyPastAppointmentsWithStatus = listOf(
    AppointmentWithStatus(
        data = AppointmentData(
            id = "4",
            dateTime = "10 Aralık 2024, 09:00",
            doctorName = "Göz Hastalıkları - Dr. Fatma Çelik",
            patientName = "Mehmet Kaya",
            hospitalName = "Etlik Şehir Hastanesi"
        ),
        status = "Tamamlandı"
    )
)

class CalendarScreenViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(CalendarScreenUiState())
    val uiState: StateFlow<CalendarScreenUiState> = _uiState.asStateFlow()

    init {
        fetchAppointments()
    }

    private fun fetchAppointments() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            delay(1000)
            _uiState.update {
                it.copy(
                    isLoading = false,
                    upcomingAppointments = dummyUpcomingAppointmentsWithStatus,
                    pastAppointments = dummyPastAppointmentsWithStatus
                )
            }
        }
    }

    fun selectTab(tab: AppointmentTab) {
        _uiState.update { it.copy(selectedTab = tab) }
    }
}