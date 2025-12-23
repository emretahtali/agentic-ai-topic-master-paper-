package com.ellitoken.myapplication.presentation.screens.profile.uistate

import com.ellitoken.myapplication.data.remote.model.User

data class ProfileScreenUiState(
    val isLoading: Boolean = false,
    val user: User? = null,

    val isDialogOpen: Boolean = false,
    val dialogFieldKey: String? = null,
    val dialogText: String = "",
    val isPhotoSheetOpen: Boolean = false
)