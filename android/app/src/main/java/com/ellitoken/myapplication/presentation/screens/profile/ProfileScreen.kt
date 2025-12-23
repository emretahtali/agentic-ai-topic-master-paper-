package com.ellitoken.myapplication.presentation.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavController
import com.ellitoken.myapplication.R
import com.ellitoken.myapplication.presentation.components.TopBar
import com.ellitoken.myapplication.presentation.screens.profile.components.LineDisaseInfo
import com.ellitoken.myapplication.presentation.screens.profile.components.LineInfo
import com.ellitoken.myapplication.presentation.screens.profile.components.LineInfoWithToggleBar
import com.ellitoken.myapplication.presentation.screens.profile.components.PhotoActionSheet
import com.ellitoken.myapplication.presentation.screens.profile.components.ProfilePhotoSection
import com.ellitoken.myapplication.presentation.screens.profile.utils.PhotoUtils
import com.ellitoken.myapplication.presentation.screens.profile.viewmodel.ProfileScreenViewModel
import com.ellitoken.myapplication.ui.theme.appBlack
import com.ellitoken.myapplication.ui.theme.appFirstGray
import org.koin.androidx.compose.getViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(navController: NavController, viewModel: ProfileScreenViewModel = getViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    val launchers = PhotoUtils.rememberPhotoLaunchers { uri ->
        viewModel.onPhotoSelected(uri)
    }

    if (uiState.isLoading) {
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
        return
    }

    val u = uiState.user!!
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
            .verticalScroll(scrollState)
            .padding(horizontal = 20.dp, vertical = 16.dp)
    ) {
        TopBar(title = "Profil") { navController.popBackStack() }

        Spacer(Modifier.height(16.dp))

        ProfilePhotoSection(
            modifier = Modifier.fillMaxWidth(),
            imageUrl = u.imageUrl.orEmpty(),
            onPhotoClick = { viewModel.openPhotoSheet() }
        )
        Spacer(Modifier.height(12.dp))

        Text(
            modifier = Modifier.fillMaxWidth(),
            text = "Kişisel Bilgiler",
            color = appBlack,
            fontSize = 16.sp,
            fontWeight = FontWeight.SemiBold
        )

        LineInfo(
            modifier = Modifier.fillMaxWidth(),
            textTitle = "Full Name",
            text = u.fullName,
            onClick = { viewModel.onEditClick("fullName") }
        )
        HorizontalDivider(color = appFirstGray.copy(alpha = 0.4f))

        LineInfo(
            modifier = Modifier.fillMaxWidth(),
            textTitle = "Date of Birth",
            text = u.dateOfBirth,
            onClick = { }
        )
        HorizontalDivider(color = appFirstGray.copy(alpha = 0.4f))

        LineInfo(
            modifier = Modifier.fillMaxWidth(),
            textTitle = "Gender",
            text = u.gender,
            onClick = { }
        )
        HorizontalDivider(color = appFirstGray.copy(alpha = 0.4f))

        LineInfo(
            modifier = Modifier.fillMaxWidth(),
            textTitle = "Email",
            text = u.email,
            onClick = { }
        )

        Text(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp, bottom = 8.dp),
            text = "Sağlık Bilgileri",
            color = appBlack,
            fontSize = 16.sp,
            fontWeight = FontWeight.SemiBold
        )

        val toggleItems = listOf(
            Triple("Chronic Illness", u.hasChronicIllness, u.chronicIllnessDescription),
            Triple("Had Surgeries", u.hadSurgeries, u.surgeriesDescription),
            Triple("Taking Regular Medications", u.takingRegularMedications, u.medicationsDescription),
            Triple("Smokes", u.smokes, u.smokingDescription),
            Triple("Drinks Alcohol", u.drinksAlcohol, u.alcoholDescription),
            Triple("Has Allergies", u.hasAllergies, u.allergiesDescription)
        )

        toggleItems.forEachIndexed { index, (label, checked, description) ->
            LineInfoWithToggleBar(
                modifier = Modifier.fillMaxWidth(),
                text = label,
                checked = checked,
                onCheckedChange = { newValue ->
                    when (index) {
                        0 -> viewModel.setChronicIllness(newValue)
                        1 -> viewModel.setHadSurgeries(newValue)
                        2 -> viewModel.setMedications(newValue)
                        3 -> viewModel.setSmokes(newValue)
                        4 -> viewModel.setDrinksAlcohol(newValue)
                        5 -> viewModel.setHasAllergies(newValue)
                    }
                },
                icon = R.drawable.homepageinfo_health
            )

            if (description.isNotBlank()) {
                LineDisaseInfo(
                    modifier = Modifier.fillMaxWidth(),
                    text = description,
                    onClick = { viewModel.openDialog(label, description) }
                )
            }

            if (index < toggleItems.lastIndex) {
                HorizontalDivider(color = appFirstGray.copy(alpha = 0.4f))
            }
        }
    }

    if (uiState.isPhotoSheetOpen) {
        ModalBottomSheet(
            onDismissRequest = { viewModel.closePhotoSheet() },
            sheetState = sheetState
        ) {
            PhotoActionSheet(
                onDismissRequest = { viewModel.closePhotoSheet() },
                onPickFromGallery = { launchers.pickFromGallery() },
                onTakePhoto = {
                    val uri = PhotoUtils.createImageUri(context)
                    launchers.takePhoto(uri)
                }
            )
        }
    }

    if (uiState.isDialogOpen) {
        AlertDialog(
            onDismissRequest = { viewModel.closeDialog() },
            title = { Text("Açıklamayı Düzenle") },
            text = {
                OutlinedTextField(
                    value = uiState.dialogText,
                    onValueChange = { viewModel.setDialogText(it) },
                    placeholder = { Text("Açıklama girin") },
                    modifier = Modifier.fillMaxWidth()
                )
            },
            confirmButton = {
                TextButton(onClick = { viewModel.saveDialogDescription() }) {
                    Text("Kaydet")
                }
            },
            dismissButton = {
                TextButton(onClick = { viewModel.closeDialog() }) {
                    Text("İptal")
                }
            }
        )
    }
}
