package com.ellitoken.myapplication.presentation.navigation

import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.layout.calculateEndPadding
import androidx.compose.foundation.layout.calculateStartPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.compose.composable
import com.ellitoken.myapplication.presentation.components.bottombar.BottomNavBar
import com.ellitoken.myapplication.presentation.screens.calendar.CalendarScreen
import com.ellitoken.myapplication.presentation.screens.chatsupport.ChatSupportScreen
import com.ellitoken.myapplication.presentation.screens.home.HomeScreen
import com.ellitoken.myapplication.presentation.screens.home.viewmodel.HomeScreenViewModel
import com.ellitoken.myapplication.presentation.screens.profile.ProfileScreen
import org.koin.androidx.compose.getViewModel

@Composable
fun AppNavigation(
    startDestination: String,
) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val homeViewModel: HomeScreenViewModel = getViewModel()
    val uiState by homeViewModel.uiState.collectAsStateWithLifecycle()

    val blurRadius by animateDpAsState(
        targetValue = if (uiState.isMicClicked) 16.dp else 0.dp,
        label = "blur"
    )

    val showBottomBar = when (currentRoute) {
        Screen.HomeScreen.route -> true
        Screen.CalendarScreen.route -> true
        Screen.ProfileScreen.route -> true
        else -> false
    }


    Scaffold(
        containerColor = Color.White,
        bottomBar = {
            AnimatedVisibility(
                visible = showBottomBar,
                enter = slideInVertically(initialOffsetY = { it }),
                exit = slideOutVertically(targetOffsetY = { it })
            ) {
                BottomNavBar(
                    navController = navController,
                    currentRoute = currentRoute,
                    modifier = Modifier.blur(blurRadius)
                )
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = startDestination,
            modifier = Modifier.padding(
                bottom = if (showBottomBar) innerPadding.calculateBottomPadding() else 0.dp,
                top = innerPadding.calculateTopPadding(),
                start = innerPadding.calculateStartPadding(LocalLayoutDirection.current),
                end = innerPadding.calculateEndPadding(LocalLayoutDirection.current)
            )
        ) {
            composable(
                route = Screen.HomeScreen.route,
            ) {
                HomeScreen(navController = navController)
            }

            composable(
                route = Screen.CalendarScreen.route,
            ) {
                CalendarScreen(navController = navController)
            }

            composable(
                route = Screen.ProfileScreen.route,
            ) {
                 ProfileScreen(navController = navController)
            }

            composable(
                route = Screen.ChatSupportScreen.route,
            ) {
                ChatSupportScreen(navController = navController)
            }
        }
    }
}