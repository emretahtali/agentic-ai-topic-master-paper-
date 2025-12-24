package com.ellitoken.myapplication.presentation.screens.calendar.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ellitoken.myapplication.data.remote.repository.CalendarChatRepository
import com.ellitoken.myapplication.presentation.screens.calendar.uistate.AppointmentTab
import com.ellitoken.myapplication.presentation.screens.calendar.uistate.CalendarScreenUiState
import com.ellitoken.myapplication.utils.onError
import com.ellitoken.myapplication.utils.onSuccess
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class CalendarScreenViewModel(private val calendarChatRepository: CalendarChatRepository) : ViewModel() {

    private val _uiState = MutableStateFlow(CalendarScreenUiState())
    val uiState: StateFlow<CalendarScreenUiState> = _uiState.asStateFlow()

    fun fetchAppointments() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            val result = calendarChatRepository.getAppointments()

            result.onSuccess { appointments ->
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        upcomingAppointments = appointments.filter { app ->
                            app.status != "CANCEL"
                        },
                        pastAppointments = appointments.filter { app ->
                            app.status == "CANCEL"
                        }
                    )
                }
            }.onError { error ->
                android.util.Log.e("API_ERROR", "Randevular çekilemedi: ${error.message}")
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }

    fun selectTab(tab: AppointmentTab) {
        _uiState.update { it.copy(selectedTab = tab) }
    }
}