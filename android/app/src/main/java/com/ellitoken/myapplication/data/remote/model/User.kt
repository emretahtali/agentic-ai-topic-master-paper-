package com.ellitoken.myapplication.data.remote.model

data class User(
    val id: String,
    val imageUrl: String,
    val fullName: String,
    val dateOfBirth: String,
    val gender: String,
    val email: String,

    val hasChronicIllness: Boolean,
    val chronicIllnessDescription: String,

    val hadSurgeries: Boolean,
    val surgeriesDescription: String,

    val takingRegularMedications: Boolean,
    val medicationsDescription: String,

    val smokes: Boolean,
    val smokingDescription: String,

    val drinksAlcohol: Boolean,
    val alcoholDescription: String,

    val hasAllergies: Boolean,
    val allergiesDescription: String
)