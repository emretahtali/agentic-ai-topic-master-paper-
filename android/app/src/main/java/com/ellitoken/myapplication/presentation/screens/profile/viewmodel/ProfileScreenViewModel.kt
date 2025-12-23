package com.ellitoken.myapplication.presentation.screens.profile.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ellitoken.myapplication.data.remote.model.User
import com.ellitoken.myapplication.presentation.screens.profile.uistate.ProfileScreenUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class ProfileScreenViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileScreenUiState(isLoading = true))
    val uiState: StateFlow<ProfileScreenUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            delay(350)
            val mockUser = User(
                id = "111111111",
                imageUrl = "https://randomuser.me/api/portraits/men/1.jpg",
                fullName = "Yusuf Asım Demirhan",
                dateOfBirth = "15/06/1990",
                gender = "Male",
                email = "ahmet.yilmaz@example.com",

                hasChronicIllness = true,
                chronicIllnessDescription = "Hipertansiyon ve hafif astım",

                hadSurgeries = true,
                surgeriesDescription = "2015 yılında apandisit ameliyatı",

                takingRegularMedications = true,
                medicationsDescription = "Tansiyon ilacı ve vitamin takviyesi",

                smokes = false,
                smokingDescription = "",

                drinksAlcohol = true,
                alcoholDescription = "Sosyal ortamlarda ara sıra",

                hasAllergies = true,
                allergiesDescription = "Fıstık ve polen alerjisi"
            )

            _uiState.update {
                it.copy(
                    isLoading = false,
                    user = mockUser
                )
            }
        }
    }

    fun updateIsLoading(isLoading: Boolean) {
        _uiState.update { it.copy(isLoading = isLoading) }
    }

    fun onPhotoClick() {  }

    fun onEditClick(field: String) { }

    private fun updateUser(block: (User) -> User) {
        _uiState.update { s -> s.copy(user = s.user?.let(block)) }
    }
    fun setChronicIllness(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    hasChronicIllness = value,
                    chronicIllnessDescription = ensureDesc(state.user.chronicIllnessDescription, value)
                )
            )
        }
    }

    fun setHadSurgeries(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    hadSurgeries = value,
                    surgeriesDescription = ensureDesc(state.user.surgeriesDescription, value)
                )
            )
        }
    }

    fun setMedications(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    takingRegularMedications = value,
                    medicationsDescription = ensureDesc(state.user.medicationsDescription, value)
                )
            )
        }
    }

    fun setSmokes(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    smokes = value,
                    smokingDescription = ensureDesc(state.user.smokingDescription, value)
                )
            )
        }
    }

    fun setDrinksAlcohol(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    drinksAlcohol = value,
                    alcoholDescription = ensureDesc(state.user.alcoholDescription, value)
                )
            )
        }
    }

    fun setHasAllergies(value: Boolean) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(
                    hasAllergies = value,
                    allergiesDescription = ensureDesc(state.user.allergiesDescription, value)
                )
            )
        }
    }

    fun openDialog(fieldKey: String, initialText: String) {
        _uiState.update {
            it.copy(
                isDialogOpen = true,
                dialogFieldKey = fieldKey,
                dialogText = if (initialText == DEFAULT_DESC) "" else initialText
            )
        }
    }

    fun closeDialog() {
        _uiState.update {
            it.copy(
                isDialogOpen = false,
                dialogFieldKey = null,
                dialogText = ""
            )
        }
    }

    fun setDialogText(newText: String) {
        _uiState.update { it.copy(dialogText = newText) }
    }

    fun saveDialogDescription() {
        val state = _uiState.value
        val user = state.user ?: return
        val text = state.dialogText.ifBlank { DEFAULT_DESC }
        val updatedUser = when (state.dialogFieldKey) {
            "Chronic Illness" -> user.copy(chronicIllnessDescription = text)
            "Had Surgeries" -> user.copy(surgeriesDescription = text)
            "Taking Regular Medications" -> user.copy(medicationsDescription = text)
            "Smokes" -> user.copy(smokingDescription = text)
            "Drinks Alcohol" -> user.copy(alcoholDescription = text)
            "Has Allergies" -> user.copy(allergiesDescription = text)
            else -> user
        }
        _uiState.update { it.copy(user = updatedUser) }
        closeDialog()
    }

    fun openPhotoSheet() {
        _uiState.update { it.copy(isPhotoSheetOpen = true) }
    }

    fun closePhotoSheet() {
        _uiState.update { it.copy(isPhotoSheetOpen = false) }
    }

    fun onPhotoSelected(uri: android.net.Uri?) {
        _uiState.update { state ->
            state.copy(
                user = state.user?.copy(imageUrl = uri?.toString().orEmpty()),
                isPhotoSheetOpen = false
            )
        }
    }

    companion object {
        private const val DEFAULT_DESC = "Lütfen detay sağlayın"
    }

    private fun ensureDesc(current: String, enabled: Boolean): String =
        if (enabled) current.ifBlank { DEFAULT_DESC } else ""

}
