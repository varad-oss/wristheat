package com.wristheat.watch.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wristheat.watch.session.Overlay
import com.wristheat.watch.ui.theme.WhAmber
import com.wristheat.watch.ui.theme.WhGreen
import com.wristheat.watch.ui.theme.WhRed

@Composable
fun AlertOverlayScreen(overlay: Overlay, advice: String?, onTap: () -> Unit) {
    val bg = when (overlay) {
        Overlay.RED -> WhRed
        Overlay.AMBER -> WhAmber
        Overlay.RECOVERED -> WhGreen
    }
    RoundColumn(Modifier.background(bg).clickable(onClick = onTap)) {
        when (overlay) {
            Overlay.RED -> {
                CText("STOP", size = 64.sp, weight = FontWeight.Black)
                advice?.let { CText(it, size = 15.sp) }
                Spacer(Modifier.height(10.dp))
                CText("Tap when you've stopped", size = 13.sp, weight = FontWeight.SemiBold)
            }
            Overlay.AMBER -> {
                CText("SLOW DOWN", size = 34.sp, weight = FontWeight.Black)
                advice?.let { CText(it, size = 15.sp) }
            }
            Overlay.RECOVERED -> {
                CText("Recovery confirmed", size = 26.sp, weight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                CText("Resume only at an easier pace", size = 15.sp)
            }
        }
    }
}
