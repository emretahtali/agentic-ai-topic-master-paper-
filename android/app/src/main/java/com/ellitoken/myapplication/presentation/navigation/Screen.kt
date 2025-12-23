package com.ellitoken.myapplication.presentation.navigation

sealed class Screen(val route: String) {
    object HomeScreen : Screen("home_screen")
    object CalendarScreen : Screen("calendar_screen")
    object ProfileScreen : Screen("profile_screen")
    object ChatSupportScreen : Screen("chatsupport_screen")
}