package com.wristheat.watch.ui.theme

import androidx.compose.ui.graphics.Color

val WhGreen = Color(0xFF1F7A4D)
val WhAmber = Color(0xFFB26A00)
val WhRed = Color(0xFFB42318)
val WhRecovering = Color(0xFF1D5FA8)
val WhGrey = Color(0xFF5F6368)
val WhTrack = Color(0xFF2A2A2A)

fun stateColor(state: String?): Color = when (state) {
    "GREEN" -> WhGreen
    "AMBER" -> WhAmber
    "RED" -> WhRed
    "RECOVERING" -> WhRecovering
    else -> WhGrey
}
