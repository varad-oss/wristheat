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
import com.wristheat.watch.ui.theme.WhGreen

@Composable
fun StartScreen(traineeId: String, error: String?, onStart: () -> Unit) {
    RoundColumn {
        CText("WristHeat", size = 26.sp, weight = FontWeight.Bold)
        CText("Heat-strain early warning", size = 14.sp, color = Color(0xFFBDBDBD))
        Spacer(Modifier.height(12.dp))
        if (error != null) {
            CText(errorText(error), size = 13.sp, color = WhAmber, weight = FontWeight.SemiBold)
            Spacer(Modifier.height(8.dp))
        }
        Chip(if (error == "permission_denied") "Retry" else "Start session", onStart, container = WhGreen)
        Spacer(Modifier.height(10.dp))
        CText("Trainee $traineeId · prototype, not a medical device", size = 11.sp, color = Color(0xFF9E9E9E))
    }
}
