package com.ellitoken.myapplication.presentation.screens.home

import android.Manifest
import android.content.pm.PackageManager
// import android.media.MediaPlayer // <-- SİLİNDİ
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import androidx.navigation.NavGraph.Companion.findStartDestination
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.presentation.navigation.Screen
import com.ellitoken.myapplication.presentation.screens.home.components.*
import com.ellitoken.myapplication.presentation.screens.home.viewmodel.HomeScreenViewModel
import com.ellitoken.myapplication.ui.theme.appBackground
import com.ellitoken.myapplication.ui.theme.appBlue
import kotlinx.coroutines.launch
import org.koin.androidx.compose.getViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    viewModel: HomeScreenViewModel = getViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.fetchUpcomingAppointments()
    }

    val context = LocalContext.current
    val healthSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val coroutineScope = rememberCoroutineScope()

    val blurRadius by animateDpAsState(
        targetValue = if (uiState.isMicClicked) 16.dp else 0.dp,
        label = "blur"
    )

    // İzin isteme (Aynen kalıyor)
    val micPermissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            viewModel.startListening()
        } else {
            Toast.makeText(context, "Mikrofon izni gerekli", Toast.LENGTH_SHORT).show()
        }
    }

    fun requestMicAndStart() {
        val granted = ContextCompat.checkSelfPermission(
            context, Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED

        if (granted) {
            viewModel.startListening()
        } else {
            micPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        }
    }

    Scaffold(
        topBar = {
            HomeScreenTopBar(
                modifier = Modifier.blur(blurRadius),
                userName = uiState.user!!.fullName,
                profileImageUrl = uiState.user!!.imageUrl,
                onClickProfile = {
                    navController.navigate(Screen.ProfileScreen.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        },
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(appBackground)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(Modifier.height(24.dp))

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .blur(blurRadius)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp),
                ) {
                    Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        HomePageInfo(
                            iconRes = R.drawable.homepageinfo_calendar,
                            title = "Yaklaşan Randevular",
                            description = "3 randevu",
                            onClick = {       navController.navigate(Screen.CalendarScreen.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                            },
                            outerPadding = 0.dp,
                            modifier = Modifier.weight(1f)
                        )
                        HomePageInfo(
                            iconRes = R.drawable.homepageinfo_health,
                            title = "Sağlık Durumu",
                            description = "Anketi doldur",
                            onClick =  { viewModel.openHealthSurveySheet() },
                            outerPadding = 0.dp,
                            modifier = Modifier.weight(1f))
                    }

                    Spacer(Modifier.height(16.dp))

                    Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        HomePageInfo(
                            iconRes = R.drawable.homepageinfo_calendar,
                            title = "İlaçlarım",
                            description = "3 aktif",
                            onClick = { },
                            outerPadding = 0.dp,
                            modifier = Modifier.weight(1f)
                        )
                        HomePageInfo(
                            iconRes = R.drawable.homepageinfo_health,
                            title = "Tahliller",
                            description = "2 yeni sonuç",
                            onClick = { },
                            outerPadding = 0.dp,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }

                Spacer(Modifier.height(16.dp))

                if (uiState.isLoading) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(200.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator(color = appBlue)
                    }
                } else {
                    UpcomingAppointmentsSection(
                        appointments = uiState.upcomingAppointments,
                        onAppointmentClick = {
                        }
                    )
                }

                Spacer(Modifier.height(24.dp))
            }
        }
    }

    if (uiState.isHealthSurveySheetOpen) {
        val surveyItems = viewModel.getHealthSurveyItems()
        val pagerState = rememberPagerState(pageCount = { surveyItems.size })

        ModalBottomSheet(
            onDismissRequest = { viewModel.closeHealthSurveySheet() },
            sheetState = healthSheetState
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Sağlık Durumu Anketi", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))

                PagerIndicator(pageCount = pagerState.pageCount, currentPage = pagerState.currentPage)

                HorizontalPager(
                    state = pagerState,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(300.dp)
                ) { pageIndex ->
                    val item = surveyItems[pageIndex]
                    HealthInfoPage(
                        question = item.question,
                        isChecked = item.isChecked,
                        description = item.description,
                        onCheckedChanged = { newCheckedState ->
                            viewModel.updateHealthInfo(item.key, newCheckedState, item.description)
                        },
                        onDescriptionChanged = { newDescription ->
                            viewModel.updateHealthInfo(item.key, item.isChecked, newDescription)
                        }
                    )
                }

                Spacer(Modifier.height(16.dp))

                Button(
                    onClick = {
                        if (pagerState.currentPage < pagerState.pageCount - 1) {
                            coroutineScope.launch {
                                pagerState.animateScrollToPage(pagerState.currentPage + 1)
                            }
                        } else {
                            viewModel.closeHealthSurveySheet()
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(if (pagerState.currentPage < pagerState.pageCount - 1) "Sonraki" else "Bitir")
                }
                Spacer(Modifier.height(8.dp))
            }
        }
    }
}