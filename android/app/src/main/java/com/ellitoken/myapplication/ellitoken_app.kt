package com.ellitoken.myapplication

import android.app.Application
import com.ellitoken.myapplication.di.appModule
import org.koin.android.ext.koin.androidContext
import org.koin.core.context.startKoin

class ellitoken_app : Application() {
    override fun onCreate() {
        super.onCreate()
        //Dependency injection
        startKoin {
            androidContext(this@ellitoken_app)
            modules(appModule)
        }
    }
}