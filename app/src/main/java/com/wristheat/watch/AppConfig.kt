package com.wristheat.watch

/** Typed view of the BuildConfig fields generated from local.properties. */
object AppConfig {
    val apiBaseUrl: String = BuildConfig.API_BASE_URL
    val deviceToken: String = BuildConfig.DEVICE_TOKEN
    val traineeId: String = BuildConfig.TRAINEE_ID
    val fakeApi: Boolean = BuildConfig.FAKE_API
    val hrSource: String = BuildConfig.HR_SOURCE
}
