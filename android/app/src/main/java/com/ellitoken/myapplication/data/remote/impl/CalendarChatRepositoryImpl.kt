package com.ellitoken.myapplication.data.remote.impl

import com.ellitoken.myapplication.data.remote.ApiClient
import com.ellitoken.myapplication.data.remote.AuthType
import com.ellitoken.myapplication.data.remote.RequestType
import com.ellitoken.myapplication.data.remote.model.AppointmentData
import com.ellitoken.myapplication.data.remote.model.response.RawAppointmentResponse
import com.ellitoken.myapplication.data.remote.model.response.SingleAppointmentDto
import com.ellitoken.myapplication.data.remote.repository.CalendarChatRepository
import com.ellitoken.myapplication.utils.NetworkError
import com.ellitoken.myapplication.utils.Result
import io.ktor.client.call.body
import kotlinx.serialization.json.Json


class CalendarChatRepositoryImpl(private val apiClient: ApiClient) : CalendarChatRepository {

    override suspend fun getAppointments(): Result<List<AppointmentData>, NetworkError> {
        val result = apiClient.handleApiRequest(
            requestType = RequestType.GET,
            authType = AuthType.ACCESS,
            url = "get_appointments"
        )

        return when (result) {
            is Result.Success -> {
                try {
                    val outerResponse = result.data.body<RawAppointmentResponse>()

                    val jsonSerializer = Json { ignoreUnknownKeys = true }
                    val remoteList =
                        jsonSerializer.decodeFromString<List<SingleAppointmentDto>>(outerResponse.respond)

                    val domainList = remoteList.map { remote ->
                        AppointmentData(
                            id = remote.appointment_id,
                            dateTime = "${remote.date} ${remote.time}",
                            doctorName = remote.doctor,
                            patientName = "Yusuf Asım Demirhan",
                            hospitalName = remote.hospital,
                            status = remote.status
                        )
                    }
                    Result.Success(domainList)
                } catch (e: Exception) {
                    android.util.Log.e("API_PARSE", "Hata: ${e.message}")
                    Result.Error(NetworkError("Veri formatı uyumsuz: ${e.message}"))
                }
            }

            is Result.Error -> Result.Error(result.error)
        }
    }
}