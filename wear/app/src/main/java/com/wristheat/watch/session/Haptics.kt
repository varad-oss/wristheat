package com.wristheat.watch.session

import android.content.Context
import android.media.AudioAttributes
import android.os.Build
import android.os.VibrationAttributes
import android.os.VibrationEffect
import android.os.VibratorManager
import android.util.Log

/** Plays the alert vibration patterns from the spec (§10). */
class Haptics(context: Context) {
    private val vibrator = (context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager).defaultVibrator

    fun play(b: Buzz) {
        val timings = when (b) {
            Buzz.AMBER -> longArrayOf(0, 200, 150, 200)
            Buzz.RED -> longArrayOf(0, 600, 200, 600, 200, 600)
            Buzz.RECOVERED -> longArrayOf(0, 800)
        }
        Log.i("WristHeatBuzz", "buzz $b")
        val effect = VibrationEffect.createWaveform(timings, -1)
        // Alarm usage so the buzz still fires with the screen off or touch feedback disabled.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            vibrator.vibrate(effect, VibrationAttributes.createForUsage(VibrationAttributes.USAGE_ALARM))
        } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(effect, AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).build())
        }
    }
}
