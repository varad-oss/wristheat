package com.wristheat.watch.ui

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
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.wear.compose.material3.AppScaffold
import androidx.wear.compose.material3.Button
import androidx.wear.compose.material3.Text
import com.wristheat.watch.sensors.ExerciseHeartRateSource
import com.wristheat.watch.sensors.READ_HEART_RATE
import com.wristheat.watch.sensors.heartRatePermissions
import com.wristheat.watch.ui.theme.HeatwristappTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        setContent { HeatwristappTheme { AppScaffold { HrSpike() } } }
    }
}

/** True when the HR permission for this API level is granted (notifications are optional). */
fun hasHrPermission(context: android.content.Context): Boolean =
    heartRatePermissions().filter { it == READ_HEART_RATE || it == android.Manifest.permission.BODY_SENSORS }
        .all { ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED }

/** Requests HR permissions; [onGranted] runs once HR is allowed. Returns the launcher trigger. */
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

/** Temporary W4 device spike: live BPM and samples per minute from ExerciseHeartRateSource. */
@Composable
fun HrSpike() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val source = remember { ExerciseHeartRateSource(context) }
    var status by remember { mutableStateOf("Tap Start") }
    var bpm by remember { mutableIntStateOf(0) }
    var total by remember { mutableIntStateOf(0) }
    var perMin by remember { mutableIntStateOf(0) }
    var running by remember { mutableStateOf(false) }
    val times = remember { ArrayDeque<Long>() }

    val start = rememberHrPermissionRequest(
        onGranted = {
            running = true
            status = "Starting…"
            scope.launch {
                source.start(
                    onSample = { s ->
                        context.mainExecutor.execute {
                            bpm = s.bpm; total++
                            val now = System.currentTimeMillis()
                            times.addLast(now)
                            while (times.isNotEmpty() && times.first() < now - 60_000) times.removeFirst()
                            perMin = times.size
                            status = "Running"
                            android.util.Log.i("WristHeatSpike", "t=${s.tMs} bpm=${s.bpm} total=$total perMin=$perMin")
                        }
                    },
                    onError = { code -> context.mainExecutor.execute { status = "Error: $code"; running = false } },
                )
            }
        },
        onDenied = { status = "Heart-rate permission needed" },
    )

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text("HR spike", fontSize = 14.sp)
        Text(if (bpm > 0) "$bpm" else "--", fontSize = 48.sp)
        Text("$perMin /min · total $total", fontSize = 14.sp)
        Text(status, fontSize = 12.sp, textAlign = TextAlign.Center)
        Button(onClick = {
            if (running) scope.launch { source.stop(); running = false; status = "Stopped" } else start()
        }) { Text(if (running) "Stop" else if (status.startsWith("Heart")) "Retry" else "Start") }
    }
}
