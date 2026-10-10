package com.wristheat.watch.ui.screens

import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wristheat.watch.ui.theme.WhAmber

@Composable
fun SetupErrorScreen(code: String?, onClose: () -> Unit) {
    val label = when (code) {
        "unauthorized" -> "unauthorized"
        "unknown_trainee" -> "unknown trainee"
        "missing_config" -> "missing API URL or token"
        null -> "unknown"
        else -> code.replace('_', ' ')
    }
    RoundColumn {
        CText("Setup error: $label", size = 18.sp, color = WhAmber, weight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        CText("Check token and trainee in local.properties", size = 13.sp, color = Color(0xFFBDBDBD))
        Spacer(Modifier.height(12.dp))
        Chip("Close", onClose, container = Color(0xFF3A3A3A))
    }
}
