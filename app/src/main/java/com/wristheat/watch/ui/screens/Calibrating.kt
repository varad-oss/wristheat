package com.wristheat.watch.ui.screens

import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wristheat.watch.session.UiState
import kotlinx.coroutines.delay

private const val LOCAL_CALIBRATION_S = 120

@Composable
fun CalibratingScreen(ui: UiState, onStop: () -> Unit) {
    var now by remember { mutableLongStateOf(System.currentTimeMillis()) }
    LaunchedEffect(Unit) {
        while (true) { delay(1000); now = System.currentTimeMillis() }
    }
    // Server value when we have one (ticked down locally between 5-s responses), else 2:00 from start.
    val serverValue = ui.calibrationRemainingS
    val anchor = remember(serverValue) { System.currentTimeMillis() }
    val remaining = if (ui.gotResponse && serverValue != null) {
        serverValue - ((now - anchor) / 1000).toInt()
    } else {
        LOCAL_CALIBRATION_S - ((now - (ui.startedAtMs ?: now)) / 1000).toInt()
    }

    RoundColumn {
        CText("Sit still", size = 22.sp, weight = FontWeight.Bold)
        CText(formatMmSs(remaining), size = 44.sp, weight = FontWeight.Bold)
        CText(ui.hrLocal?.let { "$it bpm" } ?: "-- bpm", size = 20.sp)
        Spacer(Modifier.height(4.dp))
        CText("Measuring your resting heart rate", size = 12.sp, color = Color(0xFFBDBDBD))
        SyncLine(ui.upload)
        Spacer(Modifier.height(6.dp))
        Chip("Stop", onStop, container = Color(0xFF3A3A3A))
    }
}
