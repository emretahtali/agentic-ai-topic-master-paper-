package com.ellitoken.myapplication.presentation.screens.home.viewmodel

import android.Manifest
import android.util.Log
import androidx.annotation.RequiresPermission
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ellitoken.myapplication.R // R.raw import'u GEREKLİ
import com.ellitoken.myapplication.presentation.screens.home.uistate.*
import com.ellitoken.myapplication.data.domain.VoiceRecorder
import com.ellitoken.myapplication.data.remote.api.VoiceApiService
import com.ellitoken.myapplication.data.remote.model.User
import com.ellitoken.myapplication.repository.UserRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.io.File

data class HealthSurveyItem(
    val key: String,
    val question: String,
    val isChecked: Boolean,
    val description: String
)

class HomeScreenViewModel(
    private val userRepository: UserRepository,
    private val recorder: VoiceRecorder,
    private val voiceApiService: VoiceApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeScreenUiState())
    val uiState: StateFlow<HomeScreenUiState> = _uiState.asStateFlow()

    // 1. Konuşma sırasını (1'den 5'e) tutan sayaç
    private var conversationStep = 0

    // 2. Çalınacak seslerin listesi
    private val audioResponses = listOf(
        R.raw.outputyav1,
        R.raw.outputyav2,
        R.raw.outputyav4,
        R.raw.outputyav5,
        R.raw.outputyav3
    )

    init {
        viewModelScope.launch {
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
            _uiState.update { it.copy(isLoading = false, user = mockUser) }
        }

        // --- Recorder (Kayıtçı) Sinyalleri ---
        recorder.onListeningStarted = {
            _uiState.update { it.copy(voiceState = VoiceState.Listening()) }
        }
        recorder.onEndpointDetected = {
            val recordedFile = recorder.getLastRecordedFile()
            if (recordedFile != null && recordedFile.exists()) {
                processRecordedAudio(recordedFile)
            } else {
                _uiState.update { it.copy(voiceState = VoiceState.Idle, isMicClicked = false) }
            }
        }
        recorder.onError = { _, _ ->
            _uiState.update {
                it.copy(
                    voiceState = VoiceState.Idle,
                    isMicClicked = false,
                    isSpeaking = false
                )
            }
        }

        // 3. VoiceApiService'in "TEK BİR OYNATMA BİTTİ" sinyalini dinle
        voiceApiService.onPlaybackFinished = {
            onSinglePlaybackFinished()
        }
    }

    fun updateHealthInfo(key: String, isChecked: Boolean, description: String) {
        // ... (Bu fonksiyonun içi aynı, değişiklik yok) ...
        _uiState.update { state ->
            val user = state.user ?: return@update state
            val finalDescription = if (isChecked) description else ""
            val updatedUser = when (key) {
                "chronicIllness" -> user.copy(hasChronicIllness = isChecked, chronicIllnessDescription = finalDescription)
                "surgeries" -> user.copy(hadSurgeries = isChecked, surgeriesDescription = finalDescription)
                "medications" -> user.copy(takingRegularMedications = isChecked, medicationsDescription = finalDescription)
                "smokes" -> user.copy(smokes = isChecked, smokingDescription = finalDescription)
                "alcohol" -> user.copy(drinksAlcohol = isChecked, alcoholDescription = finalDescription)
                "allergies" -> user.copy(hasAllergies = isChecked, allergiesDescription = finalDescription)
                else -> user
            }
            state.copy(user = updatedUser)
        }
    }

    fun getHealthSurveyItems(): List<HealthSurveyItem> {
        // ... (Bu fonksiyonun içi aynı, değişiklik yok) ...
        val user = _uiState.value.user ?: return emptyList()
        return listOf(
            HealthSurveyItem("chronicIllness", "Kronik bir hastalığınız var mı?", user.hasChronicIllness, user.chronicIllnessDescription),
            HealthSurveyItem("surgeries", "Daha önce ameliyat geçirdiniz mi?", user.hadSurgeries, user.surgeriesDescription),
            HealthSurveyItem("medications", "Düzenli ilaç kullanıyor musunuz?", user.takingRegularMedications, user.medicationsDescription),
            HealthSurveyItem("smokes", "Sigara kullanıyor musunuz?", user.smokes, user.smokingDescription),
            HealthSurveyItem("alcohol", "Alkol kullanıyor musunuz?", user.drinksAlcohol, user.alcoholDescription),
            HealthSurveyItem("allergies", "Bilinen bir alerjiniz var mı?", user.hasAllergies, user.allergiesDescription)
        )
    }

    fun openHealthSurveySheet() {
        _uiState.update { it.copy(isHealthSurveySheetOpen = true) }
    }

    fun closeHealthSurveySheet() {
        _uiState.update { it.copy(isHealthSurveySheetOpen = false) }
    }

    /**
     * Kaydedilen sesi işler (gibi yapar) ve sıradaki TEK BİR cevabı oynatır.
     */
    private fun processRecordedAudio(audioFile: File) {
        viewModelScope.launch {
            _uiState.update { it.copy(voiceState = VoiceState.Processing) }

            // --- API Simülasyonu ---
            voiceApiService.saveInputForDebugging(audioFile) // Kaydı kaydet
            delay(1500) // 1.5 saniye "düşünme" süresi

            // Konuşma sırasını bir artır
            conversationStep++

            // Konuşma bitti mi kontrol et (Eğer 5'ten fazla konuşursa)
            if (conversationStep > audioResponses.size) {
                Log.d("ViewModel", "Konuşma (5 adım) zaten bitti.")
                changeStateToIdle() // Konuşma bitti, boşa dön
                return@launch
            }

            // Sıradaki sesi al (index 0'dan başladığı için 'step - 1')
            val resourceIdToPlay = audioResponses[conversationStep - 1]

            _uiState.update {
                it.copy(
                    voiceState = VoiceState.Speaking,
                    isSpeaking = true,
                    processedAudioFile = null // Artık UI'a dosya vermiyoruz
                )
            }

            // Servise SADECE O sesi çalmasını söyle
            voiceApiService.playSingleAudio(resourceIdToPlay)
        }
    }

    /**
     * TEK BİR ses dosyası çalındıktan sonra tetiklenir.
     */
    fun onSinglePlaybackFinished() {
        viewModelScope.launch {
            // YENİ KONTROL: Eğer 5. sesi çaldıysak, DÖNGÜYÜ BİTİR.
            if (conversationStep == audioResponses.size) {
                Log.d("ViewModel", "Son ses (5/5) çalındı. Konuşma bitiyor.")
                changeStateToIdle() // Mikrofonu AÇMA, boşa dön
            } else {
                // Daha ses varsa (örn: 2. bitti), mikrofonu tekrar aç
                Log.d("ViewModel", "Ses $conversationStep/5 bitti. Mikrofon açılıyor.")
                _uiState.update {
                    it.copy(
                        isSpeaking = false,
                        processedAudioFile = null,
                        voiceState = VoiceState.Listening(),
                        isMicClicked = true
                    )
                }
                // Fiziksel olarak kaydı yeniden başlat
                recorder.startRecording()
            }
        }
    }

    @RequiresPermission(Manifest.permission.RECORD_AUDIO)
    fun startListening() {
        // Dinlemeyi başlatmak, konuşma sırasını SIFIRLAR.
        conversationStep = 0
        _uiState.update { it.copy(voiceState = VoiceState.Listening(), isMicClicked = true) }
        recorder.startRecording()
    }

    fun stopListeningAndProcess() {
        recorder.forceStopAndSend()
    }

    fun setMicClicked(clicked: Boolean) {
        _uiState.update { it.copy(isMicClicked = clicked) }
    }

    fun setSpeaking(value: Boolean) {
        _uiState.update { it.copy(isSpeaking = value) }
    }

    fun changeStateToIdle() {
        // Boşa dönerken sıfırla
        conversationStep = 0
        _uiState.update {
            it.copy(
                voiceState = VoiceState.Idle,
                isMicClicked = false,
                isSpeaking = false
            )
        }
    }

    fun stopAutoCycle() {
        recorder.forceStopAndSend()
        changeStateToIdle()
    }

    override fun onCleared() {
        voiceApiService.releasePlayer()
        super.onCleared()
    }
}