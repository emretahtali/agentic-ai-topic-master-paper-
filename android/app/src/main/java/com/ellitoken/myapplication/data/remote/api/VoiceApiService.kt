package com.ellitoken.myapplication.data.remote.api

import android.content.Context
import android.media.MediaPlayer
import android.os.Environment
import com.ellitoken.myapplication.R
import java.io.File

/**
 * Bu sınıf artık bir "oynatma servisi"dir.
 * API simülasyonu (gecikme) ve mantığı ViewModel'e taşındı.
 * Sadece kendisine verilen TEK BİR sesi çalar.
 */
class VoiceApiService(private val context: Context) {

    private var mediaPlayer: MediaPlayer? = null

    // ViewModel'e "bitti" sinyali gönderecek callback
    var onPlaybackFinished: (() -> Unit)? = null // 'onPlaybackQueueFinished' değil

    /**
     * Kendisine verilen TEK BİR ses dosyasını (resource ID) oynatır.
     */
    fun playSingleAudio(resourceId: Int) {
        try {
            releasePlayer() // Önceki çaları temizle

            mediaPlayer = MediaPlayer.create(context, resourceId)

            mediaPlayer?.setOnCompletionListener {
                println("Oynatıldı (bitti): $resourceId")
                onPlaybackFinished?.invoke() // "Bitti" sinyali gönder
            }

            mediaPlayer?.setOnErrorListener { _, _, _ ->
                println("MediaPlayer Hatası: $resourceId")
                onPlaybackFinished?.invoke() // Hata olsa bile "Bitti" sinyali gönder
                true
            }

            println("Oynatılıyor: $resourceId")
            mediaPlayer?.start()
        } catch (e: Exception) {
            println("Hata (playSingleAudio): ${e.message}")
            onPlaybackFinished?.invoke() // Hata olsa bile "Bitti" sinyali gönder
        }
    }

    /**
     * MediaPlayer'ı serbest bırakır.
     */
    fun releasePlayer() {
        mediaPlayer?.stop()
        mediaPlayer?.release()
        mediaPlayer = null
    }

    /**
     * Bu fonksiyon artık sadece bir yardımcı,
     * API simülasyonu için ViewModel'de kullanılacak.
     */
    fun saveInputForDebugging(inputFile: File) {
        val downloadDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
        if (!downloadDir.exists()) {
            downloadDir.mkdirs()
        }
        val timestamp = System.currentTimeMillis()
        val debugFile = File(downloadDir, "recorded_input_${timestamp}.3gp")
        inputFile.copyTo(debugFile, overwrite = true)
        println("-> Gelen kayıt Downloads klasörüne kopyalandı: ${debugFile.name}")
    }
}