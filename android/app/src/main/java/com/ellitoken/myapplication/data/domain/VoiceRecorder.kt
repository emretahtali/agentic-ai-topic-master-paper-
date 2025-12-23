package com.ellitoken.myapplication.data.domain

import android.Manifest
import android.content.Context
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.Handler
import android.os.Looper
import android.util.Log
import androidx.annotation.RequiresPermission
import java.io.ByteArrayOutputStream
import java.io.File
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.abs
import kotlin.math.max

class VoiceRecorder(private val context: Context) {

    // Arayüz aynı kalıyor, ViewModel bu sınıfın içini bilmek zorunda değil
    var onListeningStarted: (() -> Unit)? = null
    var onEndpointDetected: (() -> Unit)? = null
    var onError: ((String, Throwable?) -> Unit)? = null

    // --- AudioRecord ve Sessizlik Algılama için Gerekli Değişkenler ---
    private val sampleRate = 16000
    private val channelConfig = AudioFormat.CHANNEL_IN_MONO
    private val audioFormat = AudioFormat.ENCODING_PCM_16BIT
    private val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat)

    private var audioRecord: AudioRecord? = null
    private var isRecording = false
    private var audioDataStream = ByteArrayOutputStream()
    private val handler = Handler(Looper.getMainLooper())
    private var currentAudioFile: File? = null

    private val silenceThreshold = 26000L
    private val silenceDurationMs = 2000L
    private val checkIntervalMs = 200L
    private var silenceCounter = 0L

    /**
     * Kaydı başlatır ve sessizlik kontrol döngüsünü tetikler.
     */
    @RequiresPermission(Manifest.permission.RECORD_AUDIO)
    fun startRecording() {
        if (isRecording) return

        silenceCounter = 0L

        try {
            audioRecord = AudioRecord(
                MediaRecorder.AudioSource.MIC,
                sampleRate,
                channelConfig,
                audioFormat,
                bufferSize
            )

            currentAudioFile = File.createTempFile("recording_", ".wav", context.cacheDir)
            audioDataStream = ByteArrayOutputStream()

            audioRecord?.startRecording()
            isRecording = true
            onMain { onListeningStarted?.invoke() }
            Log.d("VoiceRecorder", "Kayıt başlatıldı ve sessizlik dinleniyor.")

            handler.post(silenceCheckRunnable)

        } catch (e: Exception) {
            onError?.invoke("AudioRecord başlatılamadı", e)
        }
    }

    /**
     * Hem manuel durdurma hem de otomatik durdurma tarafından çağrılan ana fonksiyon.
     * Kaydı bitirir, veriyi dosyaya yazar ve ViewModel'i bilgilendirir.
     */
    private fun stopRecording() {
        if (!isRecording) return
        isRecording = false
        handler.removeCallbacks(silenceCheckRunnable) // Döngüyü durdur

        try {
            audioRecord?.stop()
            audioRecord?.release()
            audioRecord = null

            val pcmData = audioDataStream.toByteArray()
            if (pcmData.isNotEmpty() && currentAudioFile != null) {
                // Ham PCM verisini standart bir WAV dosyasına çevirip kaydediyoruz
                val wavData = toWav(pcmData)
                currentAudioFile!!.writeBytes(wavData)
                Log.d("VoiceRecorder", "Kayıt durduruldu. WAV dosyası kaydedildi: ${currentAudioFile!!.name}")
            }
            // Kayıt bitti, dosyayı ViewModel'e bildirelim
            onMain { onEndpointDetected?.invoke() }

        } catch (e: Exception) {
            onError?.invoke("Kayıt durdurulurken hata oluştu", e)
        }
    }

    /**
     * UI'dan gelen manuel durdurma isteğini karşılar.
     */
    fun forceStopAndSend() {
        if (isRecording) {
            Log.d("VoiceRecorder", "Kayıt manuel olarak durduruldu.")
            stopRecording()
        }
    }

    /**
     * En son kaydedilen ses dosyasını ViewModel'e vermek için.
     */
    fun getLastRecordedFile(): File? {
        return currentAudioFile
    }

    // --- Sessizlik Algılama ve Yardımcı Fonksiyonlar ---

    private val silenceCheckRunnable = object : Runnable {
        override fun run() {
            if (!isRecording) return

            val buffer = ByteArray(bufferSize)
            val readSize = audioRecord?.read(buffer, 0, buffer.size) ?: 0

            if (readSize > 0) {
                audioDataStream.write(buffer, 0, readSize) // Gelen veriyi biriktir
                val maxAmplitude = getMaxAmplitude(buffer)

                if (maxAmplitude < silenceThreshold) {
                    silenceCounter += checkIntervalMs
                } else {
                    silenceCounter = 0 // Ses varsa sayacı sıfırla
                }

                if (silenceCounter >= silenceDurationMs) {
                    Log.d("VoiceRecorder", "Yeterli süre sessizlik algılandı, kayıt durduruluyor.")
                    stopRecording() // Kaydı otomatik durdur
                }
            }
            if (isRecording) {
                handler.postDelayed(this, checkIntervalMs) // Döngüye devam et
            }
        }
    }

    private fun getMaxAmplitude(data: ByteArray): Int {
        var max = 0
        for (i in 0 until data.size / 2) {
            val shortVal = (data[i * 2 + 1].toInt() shl 8) or (data[i * 2].toInt() and 0xFF)
            max = max(max, abs(shortVal.toInt()))
        }
        return max
    }

    private fun onMain(block: () -> Unit) {
        Handler(Looper.getMainLooper()).post(block)
    }

    // --- WAV Dönüştürme Fonksiyonları ---

    private fun toWav(pcm: ByteArray): ByteArray {
        val header = makeWavHeader(sampleRate, 1, 16, pcm.size)
        return header + pcm
    }

    private fun makeWavHeader(sampleRate: Int, channels: Int, bitsPerSample: Int, pcmSize: Int): ByteArray {
        val byteRate = sampleRate * channels * bitsPerSample / 8
        val blockAlign = channels * bitsPerSample / 8
        val dataSize = pcmSize
        val chunkSize = 36 + dataSize

        val bb = ByteBuffer.allocate(44).order(ByteOrder.LITTLE_ENDIAN)
        bb.put("RIFF".toByteArray())
        bb.putInt(chunkSize)
        bb.put("WAVE".toByteArray())
        bb.put("fmt ".toByteArray())
        bb.putInt(16)
        bb.putShort(1)
        bb.putShort(channels.toShort())
        bb.putInt(sampleRate)
        bb.putInt(byteRate)
        bb.putShort(blockAlign.toShort())
        bb.putShort(bitsPerSample.toShort())
        bb.put("data".toByteArray())
        bb.putInt(dataSize)
        return bb.array()
    }
}
//
//    private fun stopRecording() {
//        if (!isRecording) return
//        isRecording = false
//        handler.removeCallbacks(silenceCheckRunnable)
//
//        audioRecord?.run {
//            try { stop() } catch (_: Throwable) {}
//            try { release() } catch (_: Throwable) {}
//        }
//        audioRecord = null
//
//        Log.d("VoiceRecorder", "Kayıt durduruldu.")
//        onMain { onEndpointDetected?.invoke() }
//
//        val pcm = audioDataStream.toByteArray()
//        if (pcm.isNotEmpty()) {
//            sendAudioToServerTest(pcm)
//        }
//    }
//
//    private fun getMaxAmplitude(data: ByteArray, size: Int): Int {
//        var maxAmp = 0
//        var i = 0
//        while (i + 1 < size) {
//            val s = (data[i + 1].toInt() shl 8) or (data[i].toInt() and 0xFF)
//            val v = abs(s)
//            if (v > maxAmp) maxAmp = v
//            i += 2
//        }
//        return maxAmp
//    }
//    private fun sendAudioToServerTest(pcmBytes: ByteArray) {
//        CoroutineScope(Dispatchers.IO).launch {
//            try {
//                onMain { onUploadingStarted?.invoke() }
//
//                // WAV formatına dönüştür
//                val wavBytes = toWav16kMono(pcmBytes)
//
//                // Dosya ismini zaman damgası ile oluştur
//                val timestamp = System.currentTimeMillis()
//                val fileName = "voice_recording_${timestamp}.wav"
//
//                // Direkt Downloads klasörüne kaydet
//                val downloadDir = java.io.File("/storage/emulated/0/Download")
//                val file = java.io.File(downloadDir, fileName)
//
//                // Downloads klasörü yoksa oluştur
//                downloadDir.mkdirs()
//
//                file.outputStream().use { fileOut ->
//                    fileOut.write(wavBytes)
//                }
//
//                Log.d(
//                    "VoiceRecorder",
//                    "✅ Ses kaydı Downloads klasörüne kaydedildi: ${file.absolutePath}"
//                )
//                Log.d("VoiceRecorder", "📁 Dosya boyutu: ${file.length()} bytes")
//
//                // Kullanıcıya bildirim için Toast göster
//                onMain {
//                    try {
//                        android.widget.Toast.makeText(
//                            context,
//                            "Ses kaydı Downloads klasörüne kaydedildi:\n${fileName}",
//                            android.widget.Toast.LENGTH_LONG
//                        ).show()
//                    } catch (e: Exception) {
//                        Log.w("VoiceRecorder", "Toast gösterilemedi: ${e.message}")
//                    }
//                }
//
//                // Test amaçlı - 2 saniye bekleyip başarılı response simüle et
//                delay(2000)
//
//                // Test için dummy audio response (sessizlik) oluştur
//                val dummyResponseBytes = createSilentWav(2000) // 2 saniyelik sessizlik
//
//                onMain { onPlaybackStarted?.invoke() }
//                onMain { playAudio(dummyResponseBytes) }
//
//            } catch (e: Exception) {
//                Log.e("VoiceRecorder", "Dosya kaydetme başarısız: ${e.message}", e)
//                onMain { onError?.invoke(e.message ?: "Dosya kaydetme hatası", e) }
//            }
//        }
//    }

//    private fun createSilentWav(durationMs: Int): ByteArray {
//        val samplesCount = (sampleRate * durationMs / 1000) * 2 // 16-bit = 2 bytes per sample
//        val silentPcm = ByteArray(samplesCount) // Tüm değerler 0 (sessizlik)
//        return toWav16kMono(silentPcm)
//    }


//    private fun toWav16kMono(pcm: ByteArray): ByteArray {
//        val header = makeWavHeader(sampleRate, 1, 16, pcm.size)
//        return header + pcm
//    }

//    private fun makeWavHeader(sampleRate: Int, channels: Int, bitsPerSample: Int, pcmSize: Int): ByteArray {
//        val byteRate = sampleRate * channels * bitsPerSample / 8
//        val blockAlign = channels * bitsPerSample / 8
//        val dataSize = pcmSize
//        val chunkSize = 36 + dataSize
//
//        val bb = ByteBuffer.allocate(44).order(ByteOrder.LITTLE_ENDIAN)
//        bb.put("RIFF".toByteArray())
//        bb.putInt(chunkSize)
//        bb.put("WAVE".toByteArray())
//        bb.put("fmt ".toByteArray())
//        bb.putInt(16)
//        bb.putShort(1)
//        bb.putShort(channels.toShort())
//        bb.putInt(sampleRate)
//        bb.putInt(byteRate)
//        bb.putShort(blockAlign.toShort())
//        bb.putShort(bitsPerSample.toShort())
//        bb.put("data".toByteArray())
//        bb.putInt(dataSize)
//        return bb.array()
//    }

//    private fun playAudio(bytes: ByteArray) {
//        if (isWav(bytes)) playWavWithMediaPlayer(bytes)
//        else playPcmWithAudioTrack(bytes, sampleRate)
//    }

//    private fun isWav(bytes: ByteArray): Boolean {
//        if (bytes.size < 12) return false
//        val riff = String(bytes.copyOfRange(0, 4))
//        val wave = String(bytes.copyOfRange(8, 12))
//        return riff == "RIFF" && wave == "WAVE"
//    }
//
//    private fun playWavWithMediaPlayer(wavBytes: ByteArray) {
//        try {
//            val tmp = java.io.File(context.cacheDir, "resp_${System.currentTimeMillis()}.wav")
//            tmp.outputStream().use { it.write(wavBytes) }
//
//            val mp = MediaPlayer()
//            mp.setDataSource(tmp.absolutePath)
//            mp.setOnCompletionListener {
//                try { it.release() } catch (_: Throwable) {}
//                tmp.delete()
//                onPlaybackCompleted?.invoke()
//            }
//            mp.setOnErrorListener { p, _, _ ->
//                try { p.release() } catch (_: Throwable) {}
//                tmp.delete()
//                onError?.invoke("WAV oynatma hatası", null)
//                true
//            }
//            mp.prepare()
//            mp.start()
//        } catch (t: Throwable) {
//            Log.e("VoiceRecorder", "WAV çalınamadı: ${t.message}", t)
//            onError?.invoke("WAV çalınamadı: ${t.message}", t)
//        }
//    }

//    private fun playPcmWithAudioTrack(pcmBytes: ByteArray, sampleRate: Int) {
//        try {
//            val attrs = AudioAttributes.Builder()
//                .setUsage(AudioAttributes.USAGE_MEDIA)
//                .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
//                .build()
//
//            val format = AudioFormat.Builder()
//                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
//                .setSampleRate(sampleRate)
//                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
//                .build()
//
//            val minBuf = AudioTrack.getMinBufferSize(
//                sampleRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT
//            )
//            val bufSize = max(minBuf, pcmBytes.size)
//
//            val track = AudioTrack(
//                attrs, format, bufSize, AudioTrack.MODE_STATIC, AudioManager.AUDIO_SESSION_ID_GENERATE
//            )
//
//            track.write(pcmBytes, 0, pcmBytes.size)
//            track.setNotificationMarkerPosition(pcmBytes.size / 2)
//            track.setPlaybackPositionUpdateListener(object :
//                AudioTrack.OnPlaybackPositionUpdateListener {
//                override fun onMarkerReached(t: AudioTrack?) {
//                    try { t?.release() } catch (_: Throwable) {}
//                    onPlaybackCompleted?.invoke()
//                }
//                override fun onPeriodicNotification(t: AudioTrack?) {}
//            })
//
//            track.play()
//        } catch (t: Throwable) {
//            Log.e("VoiceRecorder", "PCM çalınamadı: ${t.message}", t)
//            onError?.invoke("PCM çalınamadı: ${t.message}", t)
//        }
//    }

//    private fun onMain(block: () -> Unit) {
//        if (Looper.myLooper() == Looper.getMainLooper()) block()
//        else Handler(Looper.getMainLooper()).post { block() }
//    }

//    fun getLastRecordedFile(): File? {
//        return currentAudioFile
//    }

//}
