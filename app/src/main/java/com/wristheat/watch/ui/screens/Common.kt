package com.wristheat.watch.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.wear.compose.material3.Button
import androidx.wear.compose.material3.ButtonDefaults
import androidx.wear.compose.material3.Text

/** Centered column padded for the round 450×450 display. */
@Composable
fun RoundColumn(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) {
    Column(
        modifier = modifier.fillMaxSize().padding(horizontal = 28.dp, vertical = 24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
        content = content,
    )
}

@Composable
fun CText(
    text: String,
    size: TextUnit = 14.sp,
    color: Color = Color.White,
    weight: FontWeight = FontWeight.Normal,
    modifier: Modifier = Modifier,
) = Text(
    text = text, fontSize = size, color = color, fontWeight = weight,
    textAlign = TextAlign.Center, modifier = modifier.fillMaxWidth(),
)

@Composable
fun Chip(label: String, onClick: () -> Unit, container: Color? = null, modifier: Modifier = Modifier) {
    Button(
        onClick = onClick,
        modifier = modifier.fillMaxWidth(),
        colors = if (container != null) ButtonDefaults.buttonColors(containerColor = container, contentColor = Color.White)
        else ButtonDefaults.buttonColors(),
    ) {
        Text(label, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth())
    }
}

fun formatMmSs(totalSeconds: Int): String {
    val s = totalSeconds.coerceAtLeast(0)
    return "%d:%02d".format(s / 60, s % 60)
}

/** Short wearer-facing text for HR / setup error codes. */
fun errorText(code: String): String = when (code) {
    "exercise_in_use" -> "Stop the Samsung Health workout, then retry"
    "permission_denied" -> "Heart-rate permission needed"
    "hr_unsupported" -> "Heart rate not supported on this watch"
    "exercise_ended" -> "Heart-rate tracking was stopped by the watch"
    else -> "Heart-rate error: $code"
}
