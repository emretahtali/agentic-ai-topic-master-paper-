package com.ellitoken.myapplication.repository

import android.net.Uri
import com.ellitoken.myapplication.data.remote.model.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class UserRepository {

    private val _userState = MutableStateFlow<User?>(null)
    val userState: StateFlow<User?> = _userState.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    suspend fun loadUser() {
        _isLoading.value = true
        kotlinx.coroutines.delay(500)
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
        _userState.value = mockUser
        _isLoading.value = false
    }

    fun updateHealthToggle(key: String, isChecked: Boolean) {
        val currentUser = _userState.value ?: return
        val currentDescription = when (key) {
            "chronicIllness" -> currentUser.chronicIllnessDescription
            "surgeries" -> currentUser.surgeriesDescription
            "medications" -> currentUser.medicationsDescription
            "smokes" -> currentUser.smokingDescription
            "alcohol" -> currentUser.alcoholDescription
            "allergies" -> currentUser.allergiesDescription
            else -> ""
        }
        val finalDescription = if (isChecked) currentDescription.ifBlank { "Lütfen detay sağlayın." } else ""
        updateHealthInfo(key, isChecked, finalDescription)
    }

    fun updateHealthDescription(key: String, description: String) {
        val currentUser = _userState.value ?: return
        val isChecked = when (key) {
            "chronicIllness" -> currentUser.hasChronicIllness
            "surgeries" -> currentUser.hadSurgeries
            "medications" -> currentUser.takingRegularMedications
            "smokes" -> currentUser.smokes
            "alcohol" -> currentUser.drinksAlcohol
            "allergies" -> currentUser.hasAllergies
            else -> false
        }
        updateHealthInfo(key, isChecked, description)
    }

    private fun updateHealthInfo(key: String, isChecked: Boolean, description: String) {
        val currentUser = _userState.value ?: return
        val updatedUser = when (key) {
            "chronicIllness" -> currentUser.copy(hasChronicIllness = isChecked, chronicIllnessDescription = description)
            "surgeries" -> currentUser.copy(hadSurgeries = isChecked, surgeriesDescription = description)
            "medications" -> currentUser.copy(takingRegularMedications = isChecked, medicationsDescription = description)
            "smokes" -> currentUser.copy(smokes = isChecked, smokingDescription = description)
            "alcohol" -> currentUser.copy(drinksAlcohol = isChecked, alcoholDescription = description)
            "allergies" -> currentUser.copy(hasAllergies = isChecked, allergiesDescription = description)
            else -> currentUser
        }
        _userState.value = updatedUser
    }

    fun onPhotoSelected(uri: Uri?) {
        val currentUser = _userState.value ?: return
        val updatedUser = currentUser.copy(imageUrl = uri?.toString().orEmpty())
        _userState.value = updatedUser
    }
}