package com.ellitoken.myapplication.utils
class NetworkError(override val message: String) : Error {
    companion object {
        val NO_INTERNET = NetworkError("No internet connection")
        val SERIALIZATION = NetworkError("Serialization error")
        val UNAUTHORIZED = NetworkError("Unauthorized")
        val UNKNOWN = NetworkError("Unknown error")
        val EMPTY_RESPONSE = NetworkError("Herhangi bir veri bulunamadı.")
    }
}
