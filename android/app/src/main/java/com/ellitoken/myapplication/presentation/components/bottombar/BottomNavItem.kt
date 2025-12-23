package com.ellitoken.myapplication.presentation.components.bottombar

import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.presentation.navigation.Screen

data class BottomNavItem(
    val route: String,
    val iconUnSelected: Int,
    val iconSelected: Int,
    val label: String
)

val bottomNavItems = listOf(
    BottomNavItem(Screen.HomeScreen.route, R.drawable.bottombar_ic_home,R.drawable.bottombar_ic_home_filled, "Ana Sayfa"),
    BottomNavItem(Screen.CalendarScreen.route, R.drawable.bottombar_ic_calendar,R.drawable.bottombar_ic_calendar_filled, "Randevular"),
    BottomNavItem(Screen.ChatSupportScreen.route, R.drawable.bottombar_ic_support,R.drawable.bottombar_ic_support_filled, "Asistan"),
    BottomNavItem(Screen.ProfileScreen.route, R.drawable.bottombar_ic_profile,R.drawable.bottombar_ic_profile_filled, "Profil")
)