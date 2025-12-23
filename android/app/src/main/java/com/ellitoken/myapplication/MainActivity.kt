package com.ellitoken.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.ellitoken.myapplication.presentation.navigation.AppNavigation
import com.ellitoken.myapplication.presentation.navigation.Screen
import com.ellitoken.myapplication.ui.theme.Ellitoken_appTheme
import com.google.firebase.FirebaseApp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        FirebaseApp.initializeApp(this)

        enableEdgeToEdge()
        setContent {
            Ellitoken_appTheme {
                AppNavigation(startDestination = Screen.HomeScreen.route)
            }
        }
    }
}