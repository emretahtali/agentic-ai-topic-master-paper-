package com.ellitoken.myapplication.di

import com.ellitoken.myapplication.data.domain.VoiceRecorder
import com.ellitoken.myapplication.data.remote.ApiClient
import com.ellitoken.myapplication.data.remote.api.VoiceApiService
import com.ellitoken.myapplication.data.remote.impl.AiChatRepositoryImpl
import com.ellitoken.myapplication.data.remote.repository.AiChatRepository
import com.ellitoken.myapplication.data.remote.repository.ChatSupportRepository
import com.ellitoken.myapplication.presentation.screens.calendar.viewmodel.CalendarScreenViewModel
import com.ellitoken.myapplication.presentation.screens.chatsupport.viewmodel.ChatSupportScreenViewModel
import com.ellitoken.myapplication.presentation.screens.home.viewmodel.HomeScreenViewModel
import com.ellitoken.myapplication.presentation.screens.profile.viewmodel.ProfileScreenViewModel
import com.ellitoken.myapplication.data.remote.repository.UserManager
import com.ellitoken.myapplication.data.remote.repository.UserRepository
import org.koin.android.ext.koin.androidContext
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.bind
import org.koin.dsl.module

val appModule = module {
    single { provideHttpClient() }
    single { UserRepository(androidContext()) } bind UserManager::class
    single { ChatSupportRepository() }
    single { VoiceApiService(androidContext()) }
    factory { VoiceRecorder(androidContext()) }
    single { HomeScreenViewModel(get(), get() , get()) }
    single { ApiClient(get(), get()) }
    single<AiChatRepository> { AiChatRepositoryImpl(get()) }
    viewModel{ CalendarScreenViewModel() }
    viewModel{ ChatSupportScreenViewModel(get()) }
    viewModel{ ProfileScreenViewModel() }

}