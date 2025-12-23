package com.ellitoken.myapplication.presentation.components.bottombar

import androidx.compose.material3.NavigationBar
import androidx.compose.runtime.Composable
import androidx.navigation.NavController
import androidx.compose.foundation.layout.size
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavGraph.Companion.findStartDestination
import com.ellitoken.myapplication.ui.theme.appBlue
import com.ellitoken.myapplication.ui.theme.appFirstGray
import com.ellitoken.myapplication.ui.theme.appWhite

@Composable
fun BottomNavBar(navController: NavController, currentRoute: String?, modifier: Modifier) {
    NavigationBar(
        modifier = modifier,
        containerColor = appWhite,
        contentColor = appFirstGray,
        tonalElevation = NavigationBarDefaults.Elevation,
    ) {
        bottomNavItems.forEach { item ->
            val selected = currentRoute == item.route
            NavigationBarItem(
                colors = NavigationBarItemDefaults.colors().copy(
                    selectedIconColor = appBlue,
                    unselectedIconColor = appFirstGray,
                    selectedTextColor = appBlue,
                    unselectedTextColor = appFirstGray,
                    selectedIndicatorColor = Color.Transparent,
                ),
                icon = {
                    Icon(
                        painter = painterResource(
                            id = if (selected) item.iconSelected else item.iconUnSelected
                        ),
                        modifier = Modifier.size(30.dp),
                        contentDescription = item.label,
                        tint = Color.Unspecified
                    )
                },
                label = {
                    Text(
                        item.label,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium
                    )
                },
                selected = selected,
                onClick = {
                    if (currentRoute != item.route) {
                        navController.navigate(item.route) {
                            popUpTo(navController.graph.findStartDestination().id) {
                                saveState = true
                            }
                            launchSingleTop = true
                            restoreState = true
                        }
                    }
                }
            )
        }
    }
}
