package com.wristheat.watch.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.wear.compose.foundation.lazy.TransformingLazyColumn
import androidx.wear.compose.foundation.lazy.rememberTransformingLazyColumnState
import androidx.wear.compose.material3.ScreenScaffold
import androidx.wear.compose.material3.Text
import com.wristheat.watch.data.UploadStatus
import com.wristheat.watch.session.UiState
import com.wristheat.watch.ui.theme.WhGreen
import com.wristheat.watch.ui.theme.WhGrey
import com.wristheat.watch.ui.theme.WhTrack
import com.wristheat.watch.ui.theme.stateColor
import java.util.Locale

/** Outer ring: PSI/10 progress in the state colour. */
@Composable
fun PsiRing(psi: Double?, color: Color, modifier: Modifier = Modifier) {
    val progress = ((psi ?: 0.0) / 10.0).coerceIn(0.0, 1.0).toFloat()
    Canvas(modifier.fillMaxSize().padding(4.dp)) {
        val stroke = 10.dp.toPx()
        val inset = stroke / 2
        val arcSize = Size(size.width - stroke, size.height - stroke)
        drawArc(WhTrack, -90f, 360f, false, Offset(inset, inset), arcSize, style = Stroke(stroke))
        if (progress > 0f) {
            drawArc(color, -90f, 360f * progress, false, Offset(inset, inset), arcSize, style = Stroke(stroke, cap = StrokeCap.Round))
        }
    }
}

@Composable
fun SyncLine(upload: UploadStatus) {
    val (dot, label) = when (upload) {
        is UploadStatus.Ok -> WhGreen to "Synced"
        is UploadStatus.Offline -> WhGrey to "Offline · buffering ${upload.bufferedSeconds} s"
        is UploadStatus.Fatal -> WhGrey to "Setup error"
    }
    Row(
        modifier = Modifier.fillMaxWidth().padding(top = 4.dp),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Box(Modifier.size(8.dp).background(dot, CircleShape))
        Spacer(Modifier.width(6.dp))
        Text(label, fontSize = 12.sp, color = Color(0xFFBDBDBD))
    }
}

fun coreLine(core: Double?, band: Double?): String? =
    core?.let { String.format(Locale.US, "Core ~%.1f ±%.1f°C", it, band ?: 0.6) }

fun envLine(wbgt: Double?, flag: String?, stale: Boolean): String? = when {
    stale -> "Heat data stale"
    wbgt != null && flag != null -> String.format(Locale.US, "WBGT %.1f · %s flag", wbgt, flag)
    wbgt != null -> String.format(Locale.US, "WBGT %.1f", wbgt)
    else -> null
}

@Composable
fun LiveScreen(ui: UiState, onStop: () -> Unit) {
    val color = stateColor(ui.state)
    val listState = rememberTransformingLazyColumnState()
    Box(Modifier.fillMaxSize()) {
        PsiRing(ui.psi, color)
        ScreenScaffold(scrollState = listState) { contentPadding ->
            TransformingLazyColumn(state = listState, contentPadding = contentPadding) {
                item {
                    Column(
                        Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                    ) {
                        CText(ui.state ?: "--", size = if ((ui.state?.length ?: 0) > 6) 19.sp else 24.sp, color = color, weight = FontWeight.Bold)
                        Text(
                            text = (ui.hrLocal ?: ui.hrServer)?.toString() ?: "--",
                            fontSize = 64.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center,
                        )
                        CText("bpm", size = 12.sp, color = Color(0xFFBDBDBD))
                        coreLine(ui.coreEst, ui.coreBand)?.let { CText(it, size = 15.sp) }
                    }
                }
                item {
                    Column(Modifier.fillMaxWidth().padding(horizontal = 32.dp)) {
                        envLine(ui.wbgt, ui.flag, ui.envStale)?.let { CText(it, size = 13.sp) }
                        ui.minutesToRed?.let { CText("~$it min to RED", size = 13.sp, weight = FontWeight.SemiBold) }
                        SyncLine(ui.upload)
                    }
                }
                ui.adviceEn?.let { advice ->
                    item {
                        CText(advice, size = 15.sp, modifier = Modifier.padding(horizontal = 30.dp, vertical = 8.dp))
                    }
                }
                item {
                    Column(Modifier.padding(horizontal = 40.dp)) {
                        Spacer(Modifier.height(6.dp))
                        Chip("Stop", onStop, container = Color(0xFF3A3A3A))
                    }
                }
            }
        }
    }
}
