import java.util.Properties
import java.io.FileInputStream

val localProperties = Properties()
val localPropertiesFile = rootProject.file("local.properties")
if (localPropertiesFile.exists()) {
    localProperties.load(FileInputStream(localPropertiesFile))
}

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    kotlin("plugin.serialization") version "1.9.0"
}

android {
    namespace = "com.ellitoken.myapplication"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.ellitoken.myapplication"
        minSdk = 30
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        // local.properties dosyasından anahtarı okuyoruz
        val apiKey = localProperties.getProperty("MY_API_KEY") ?: ""

        // --- DEĞİŞİKLİK BURADA ---
        // buildConfigField yerine resValue kullanıyoruz.
        // Bu işlem, şifreyi otomatik olarak R.string.my_api_key içine gömer.
        resValue("string", "my_api_key", apiKey)
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    implementation(platform(libs.androidx.compose.bom))
    implementation(platform(libs.firebase.bom))

    // Compose
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation(libs.androidx.foundation)
    implementation(libs.androidx.navigation.compose)
    implementation(libs.androidx.material.icons.extended)

    // Lifecycle + Compose
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.lifecycle.viewmodel.savedstate)

    // Koin
    implementation(libs.koin.core)
    implementation(libs.koin.android)
    implementation(libs.koin.compose)

    // Serialization
    implementation(libs.serialization.core)
    implementation(libs.serialization.json)
    implementation(libs.kotlinx.serialization.json.v151)

    // Ktor
    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.cio)
    implementation(libs.ktor.client.android)
    implementation(libs.ktor.client.logging)
    implementation(libs.ktor.client.content.negotiation)
    implementation(libs.ktor.serialization.json)

    // Retrofit/OkHttp
    implementation(libs.retrofit)
    implementation(libs.retrofit.converter.gson)
    implementation(libs.okhttp)
    implementation(libs.okhttp.logging)

    // Coil
    implementation(libs.coil.compose)

    // Google / Firebase
    implementation(libs.firebase.analytics)
    implementation(libs.firebase.auth.ktx)
    implementation(libs.play.services.location)
    implementation(libs.play.services.auth)
    implementation(libs.google.places)
    implementation(libs.google.identity.googleid)
    implementation(libs.google.material)

    // Permissions, Camera, ML Kit
    implementation(libs.google.accompanist.permissions)
    implementation(libs.androidx.camera.core)
    implementation(libs.androidx.camera.camera2)
    implementation(libs.androidx.camera.lifecycle)
    implementation(libs.androidx.camera.view)
    implementation(libs.barcode.scanning)

    // JSON
    implementation(libs.org.json)

    // DateTime
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.0")

    // Lottie
    implementation("com.airbnb.android:lottie-compose:6.6.7")

    // VAD (Silero)
    implementation("com.github.gkonovalov.android-vad:silero:2.0.3")

    // Opus
    implementation("io.github.jaredmdobson:concentus:1.0.2")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")

    implementation("com.github.jeziellago:compose-markdown:0.5.8")
}