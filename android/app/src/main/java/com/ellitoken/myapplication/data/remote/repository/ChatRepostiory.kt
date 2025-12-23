package com.ellitoken.myapplication.data.remote.repository

import com.ellitoken.myapplication.data.remote.model.AppointmentData
import com.ellitoken.myapplication.presentation.screens.chatsupport.uistate.AiMessage
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.datetime.Clock
import java.util.Locale
import java.util.UUID

class ChatSupportRepository() {

    // Randevu listesi (Sıralama yok)
    private val upcomingAppointments = listOf(
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

    /**
     * Gelen kullanıcı mesajını analiz eder ve uygun cevabı bir Flow olarak döndürür.
     */
    fun sendMessage(userMessage: String): Flow<AiMessage> = flow {

        // --- İSTEDİĞİN DÜŞÜNME SÜRESİ ---
        // Cevap vermeden önce 1.5 saniye bekle
        delay(2200)

        // Gelen mesajı küçük harfe çevir (Türkçe karakterlere duyarlı)
        val normalizedMessage = userMessage.lowercase(Locale("tr", "TR"))

        val botResponse = when {
            // ----- SENARYO 1: Doktorları Listele (Sıralamasız) -----
            normalizedMessage.contains("doktorlar") || normalizedMessage.contains("randevular") -> {

                val doctorList = upcomingAppointments.joinToString(separator = "\n") {
                    "- ${it.doctorName}" // Sadece doktor isimlerini listele
                }

                "Tabi, aşağıda randevunuz olan doktorları sıralıyorum:\n$doctorList"
            }

            // ----- SENARYO 2: Spesifik Doktor Sorgulama (Zeynep) -----
            normalizedMessage.contains("zeynep yorulmaz") -> {

                val appointment = upcomingAppointments.find {
                    it.doctorName.lowercase(Locale("tr", "TR")).contains("zeynep yorulmaz")
                }

                if (appointment != null) {
                    "${appointment.doctorName} ile olan randevunuz ${appointment.dateTime} tarihindedir."
                } else {
                    "Dr. Zeynep Yorulmaz adına bir randevu bulunamadı."
                }
            }

            // ----- Varsayılan Cevap (Fallback) -----
            else -> {
                "Mesajınızı anlayamadım. Size randevularınız hakkında yardımcı olabilirim."
            }
        }

        // Analiz edilen cevabı emit et
        emit(
            AiMessage(
                id = UUID.randomUUID().toString(),
                createdAt = Clock.System.now(),
                message = botResponse,
                fromAi = true
            )
        )
    }
}