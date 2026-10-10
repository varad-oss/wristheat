import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

// WristHeat config comes from local.properties (git-ignored, never committed).
val localProps = Properties().apply {
    val f = rootProject.file("local.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun prop(key: String, default: String): String =
    localProps.getProperty(key)?.substringBefore(" #")?.trim()?.takeIf { it.isNotEmpty() } ?: default

android {
    namespace = "com.wristheat.watch"
    // Only android-37 is installed locally; targetSdk follows the spec (36).
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.wristheat.watch"
        minSdk = 30
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"

        buildConfigField("String", "API_BASE_URL", "\"${prop("wristheat.apiBaseUrl", "")}\"")
        buildConfigField("String", "DEVICE_TOKEN", "\"${prop("wristheat.deviceToken", "")}\"")
        buildConfigField("String", "TRAINEE_ID", "\"${prop("wristheat.traineeId", "T1")}\"")
        buildConfigField("boolean", "FAKE_API", prop("wristheat.fakeApi", "false").toBoolean().toString())
        buildConfigField("String", "HR_SOURCE", "\"${prop("wristheat.hrSource", "exercise")}\"")
    }

    buildTypes {
        release {
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    useLibrary("wear-sdk")
    buildFeatures {
        buildConfig = true
        compose = true
    }
    testOptions {
        unitTests.isReturnDefaultValues = true
    }
}

dependencies {
    implementation(platform(libs.compose.bom))
    implementation(libs.activity.compose)
    implementation(libs.compose.foundation)
    implementation(libs.compose.material3)
    implementation(libs.compose.ui.tooling)
    implementation(libs.core.splashscreen)
    implementation(libs.play.services.wearable)
    implementation(libs.ui)
    implementation(libs.ui.graphics)
    implementation(libs.ui.tooling.preview)
    implementation(libs.wear.tooling.preview)
    implementation(libs.health.services)
    implementation(libs.concurrent.futures.ktx)
    implementation(libs.lifecycle.service)
    implementation(libs.lifecycle.runtime.compose)
    implementation(libs.okhttp)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.kotlinx.coroutines.android)
    testImplementation(libs.junit)
    testImplementation(libs.kotlinx.coroutines.test)
    testImplementation(libs.okhttp.mockwebserver)
    androidTestImplementation(platform(libs.compose.bom))
    androidTestImplementation(libs.ui.test.junit4)
    debugImplementation(libs.ui.test.manifest)
    debugImplementation(libs.ui.tooling)
}
