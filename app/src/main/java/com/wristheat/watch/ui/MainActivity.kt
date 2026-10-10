package com.wristheat.watch.ui

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.wear.compose.material3.AppScaffold
import com.wristheat.watch.AppConfig
import com.wristheat.watch.sensors.READ_HEART_RATE
import com.wristheat.watch.sensors.heartRatePermissions
import com.wristheat.watch.session.Phase
import com.wristheat.watch.session.SessionRepository
import com.wristheat.watch.session.SessionService
import com.wristheat.watch.ui.screens.AlertOverlayScreen
import com.wristheat.watch.ui.screens.CText
import com.wristheat.watch.ui.screens.CalibratingScreen
import com.wristheat.watch.ui.screens.LiveScreen
import com.wristheat.watch.ui.screens.RoundColumn
import com.wristheat.watch.ui.screens.SetupErrorScreen
import com.wristheat.watch.ui.screens.StartScreen
import com.wristheat.watch.ui.screens.StopConfirmScreen
import com.wristheat.watch.ui.theme.WristHeatTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { WristHeatTheme { AppScaffold { WristHeatApp(::setKeepScreenOn) } } }
    }

    private fun setKeepScreenOn(on: Boolean) {
        if (on) window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        else window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
    }
}

/** True when the HR permission for this API level is granted (notifications are optional). */
fun hasHrPermission(context: Context): Boolean =
    heartRatePermissions().filter { it == READ_HEART_RATE || it == android.Manifest.permission.BODY_SENSORS }
        .all { ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED }

/** Requests HR permissions; [onGranted] runs once HR is allowed. Returns the trigger. */
@Composable
fun rememberHrPermissionRequest(onGranted: () -> Unit, onDenied: () -> Unit): () -> Unit {
    val context = LocalContext.current
    var denials by remember { mutableIntStateOf(0) }
    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) {
        if (hasHrPermission(context)) onGranted() else { denials++; onDenied() }
    }
    return {
        when {
            hasHrPermission(context) -> onGranted()
            // After two denials Android stops showing the dialog; send the wearer to app settings.
            denials >= 2 -> context.startActivity(
                Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", context.packageName, null))
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            )
            else -> launcher.launch(heartRatePermissions())
        }
    }
}

@Composable
fun WristHeatApp(keepScreenOn: (Boolean) -> Unit) {
    val context = LocalContext.current
    val ui by SessionRepository.ui.collectAsStateWithLifecycle()
    var confirmStop by remember { mutableStateOf(false) }

    val active = ui.phase == Phase.STARTING || ui.phase == Phase.RUNNING
    LaunchedEffect(active) { keepScreenOn(active) }
    LaunchedEffect(ui.phase) { if (!active) confirmStop = false }

    val start = rememberHrPermissionRequest(
        onGranted = { SessionRepository.onError(""); SessionService.start(context) },
        onDenied = { SessionRepository.reset(error = "permission_denied") },
    )
    val askStop = { confirmStop = true }

    val overlay = ui.overlay
    when {
        ui.phase == Phase.SETUP_ERROR -> SetupErrorScreen(ui.error) {
            SessionService.stop(context)
            SessionRepository.reset()
        }
        ui.phase == Phase.IDLE -> StartScreen(AppConfig.traineeId, ui.error?.takeIf { it.isNotBlank() }, start)
        ui.phase == Phase.ENDING -> RoundColumn { CText("Ending session…", size = 18.sp) }
        overlay != null -> AlertOverlayScreen(overlay, ui.adviceEn) { SessionRepository.dismissOverlay() }
        confirmStop -> StopConfirmScreen(
            onYes = { confirmStop = false; SessionService.stop(context) },
            onNo = { confirmStop = false },
        )
        ui.state == null || ui.state == "CALIBRATING" -> CalibratingScreen(ui, askStop)
        else -> LiveScreen(ui, askStop)
    }
}
