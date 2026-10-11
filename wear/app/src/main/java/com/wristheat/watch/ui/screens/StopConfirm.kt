package com.wristheat.watch.ui.screens

import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wristheat.watch.ui.theme.WhRed

@Composable
fun StopConfirmScreen(onYes: () -> Unit, onNo: () -> Unit) {
    RoundColumn {
        CText("End session?", size = 22.sp, weight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))
        Chip("Yes, end", onYes, container = WhRed)
        Spacer(Modifier.height(6.dp))
        Chip("No", onNo, container = Color(0xFF3A3A3A))
    }
}
