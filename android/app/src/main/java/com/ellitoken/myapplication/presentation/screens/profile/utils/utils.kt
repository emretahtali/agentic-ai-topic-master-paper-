package com.ellitoken.myapplication.presentation.screens.profile.utils

import android.content.ContentResolver
import android.content.ContentValues
import android.content.Context
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

object PhotoUtils {

    fun createImageUri(context: Context): Uri {
        val resolver: ContentResolver = context.contentResolver
        val imageCollection =
            MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL_PRIMARY)
        val contentValues = ContentValues().apply {
            put(MediaStore.Images.Media.DISPLAY_NAME, "profile_${System.currentTimeMillis()}.jpg")
            put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
        }
        return resolver.insert(imageCollection, contentValues)
            ?: error("Uri oluşturulamadı")
    }

    data class Launchers(
        val pickFromGallery: () -> Unit,
        val takePhoto: (Uri) -> Unit
    )


    @Composable
    fun rememberPhotoLaunchers(
        onResult: (Uri?) -> Unit
    ): Launchers {
        // GALERİ
        val galleryLauncher =
            rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
                onResult(uri) // galeriden gelen uri
            }

        // KAMERA: son verdiğimiz URI’yi hatırla ve success olursa aynısını döndür
        var lastCameraUri by remember { mutableStateOf<Uri?>(null) }
        val cameraLauncher =
            rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { success ->
                onResult(if (success) lastCameraUri else null)
            }

        return remember {
            Launchers(
                pickFromGallery = {
                    galleryLauncher.launch(
                        PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                    )
                },
                takePhoto = { uri ->
                    lastCameraUri = uri
                    cameraLauncher.launch(uri)
                }
            )
        }
    }

}