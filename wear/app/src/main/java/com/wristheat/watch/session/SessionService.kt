package com.wristheat.watch.session

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.PowerManager
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.LifecycleService
import androidx.lifecycle.lifecycleScope
import com.wristheat.watch.AppConfig
import com.wristheat.watch.R
import com.wristheat.watch.data.Api
import com.wristheat.watch.data.FakeApi
import com.wristheat.watch.data.OkHttpApi
import com.wristheat.watch.data.Sample
import com.wristheat.watch.data.SampleBuffer
import com.wristheat.watch.data.SystemClock
import com.wristheat.watch.data.UploadStatus
import com.wristheat.watch.data.Uploader
import com.wristheat.watch.sensors.ExerciseHeartRateSource
import com.wristheat.watch.sensors.FakeHeartRateSource
import com.wristheat.watch.sensors.HeartRateSource
import com.wristheat.watch.sensors.MeasureHeartRateSource
import com.wristheat.watch.ui.MainActivity
import kotlinx.coroutines.Job
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import java.util.UUID

/**
 * Foreground service (type health) that owns one WristHeat session: HR source → buffer →
 * uploader every 5 s → repository + alert policy + haptics. Keeps running with the screen off.
 */
class SessionService : LifecycleService() {
    private var source: HeartRateSource? = null
    private var api: Api? = null
    private var sessionId: String? = null
    private var jobs = mutableListOf<Job>()
    private var wakeLock: PowerManager.WakeLock? = null
    private var stopping = false

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        super.onStartCommand(intent, flags, startId)
        when (intent?.action) {
            ACTION_START -> if (sessionId == null) startSession()
            ACTION_STOP -> if (sessionId != null) stopSession() else stopSelf()
            else -> if (sessionId == null) stopSelf()
        }
        return START_NOT_STICKY
    }

    private fun startSession() {
        SessionRepository.startSession()
        try {
            ServiceCompat.startForeground(this, NOTIFICATION_ID, buildNotification(), ServiceInfo.FOREGROUND_SERVICE_TYPE_HEALTH)
        } catch (e: Exception) {
            Log.e(TAG, "startForeground failed", e)
            SessionRepository.reset(error = "permission_denied")
            stopSelf()
            return
        }
        if (!AppConfig.fakeApi && (AppConfig.apiBaseUrl.isBlank() || AppConfig.deviceToken.isBlank())) {
            SessionRepository.reset(Phase.SETUP_ERROR, "missing_config")
            stopForegroundAndSelf()
            return
        }

        val id = UUID.randomUUID().toString()
        sessionId = id
        wakeLock = (getSystemService(POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "WristHeat:session")
            .apply { acquire(4 * 60 * 60 * 1000L) }

        val api: Api = if (AppConfig.fakeApi) FakeApi() else OkHttpApi(AppConfig.apiBaseUrl, AppConfig.deviceToken)
        this.api = api
        val source: HeartRateSource = when (AppConfig.hrSource) {
            "measure" -> MeasureHeartRateSource(this)
            "fake" -> FakeHeartRateSource(lifecycleScope)
            else -> ExerciseHeartRateSource(this)
        }
        this.source = source
        Log.i(TAG, "session $id start; api=${if (AppConfig.fakeApi) "fake" else "live"} hr=${AppConfig.hrSource}")

        val buffer = SampleBuffer()
        val haptics = Haptics(this)
        val policy = AlertPolicy(SystemClock)
        SessionRepository.onRedAcknowledged = { lifecycleScope.launch { policy.acknowledgeRed() } }

        val uploader = Uploader(
            api, buffer, SystemClock, AppConfig.traineeId, id,
            onResponse = { r ->
                Log.i(TAG, "ingest ok state=${r.state} accepted=${r.accepted} dropped=${r.dropped} alert=${r.alert}")
                policy.onResponse(r.alert, r.state).forEach(haptics::play)
                SessionRepository.onResponse(r)
            },
            onStatus = SessionRepository::onStatus,
            log = { Log.i(TAG, it) },
        )

        var lastSampleT = 0L
        jobs += lifecycleScope.launch {
            var hrFailed = false
            source.start(
                onSample = { s ->
                    if (lastSampleT > 0 && s.tMs - lastSampleT > 5_000) Log.w(TAG, "hr gap ${(s.tMs - lastSampleT) / 1000}s")
                    lastSampleT = maxOf(lastSampleT, s.tMs)
                    buffer.add(Sample(s.tMs, s.bpm))
                    SessionRepository.onLocalSample(s)
                },
                onError = { code ->
                    if (stopping || sessionId != id) return@start
                    hrFailed = true
                    Log.w(TAG, "hr error $code")
                    lifecycleScope.launch {
                        SessionRepository.onError(code)
                        stopSession(keepError = code)
                    }
                },
            )
            if (!hrFailed && !stopping) SessionRepository.onPhase(Phase.RUNNING)
        }
        jobs += lifecycleScope.launch {
            while (isActive && !uploader.stopped) {
                uploader.tick()
                delay(uploader.nextDelayMs().coerceAtLeast(250))
            }
        }
        jobs += lifecycleScope.launch {
            while (isActive) {
                delay(1000)
                val ui = SessionRepository.ui.value
                ui.state?.let { st -> policy.onTick(st).forEach(haptics::play) }
                SessionRepository.onTick()
                if (ui.upload is UploadStatus.Offline) {
                    SessionRepository.onStatus(UploadStatus.Offline(uploader.bufferedSeconds()))
                }
            }
        }
    }

    private fun stopSession(keepError: String? = null) {
        if (stopping) return
        stopping = true
        val id = sessionId
        SessionRepository.onPhase(Phase.ENDING)
        lifecycleScope.launch {
            withContext(NonCancellable) {
                jobs.forEach { it.cancel() }
                runCatching { source?.stop() }
                if (id != null) {
                    val ended = withTimeoutOrNull(3_000) { api?.endSession(id) }
                    Log.i(TAG, "session $id end: $ended")
                }
            }
            SessionRepository.reset(error = keepError)
            stopForegroundAndSelf()
        }
    }

    private fun stopForegroundAndSelf() {
        SessionRepository.onRedAcknowledged = null
        wakeLock?.takeIf { it.isHeld }?.release()
        wakeLock = null
        sessionId = null
        jobs.clear()
        stopping = false
        ServiceCompat.stopForeground(this, ServiceCompat.STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    override fun onDestroy() {
        wakeLock?.takeIf { it.isHeld }?.release()
        super.onDestroy()
    }

    private fun buildNotification(): Notification {
        val nm = getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(NotificationChannel(CHANNEL, "Session", NotificationManager.IMPORTANCE_LOW))
        val open = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP),
            PendingIntent.FLAG_IMMUTABLE,
        )
        return NotificationCompat.Builder(this, CHANNEL)
            .setContentTitle("WristHeat")
            .setContentText("WristHeat session running")
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setOngoing(true)
            .setCategory(NotificationCompat.CATEGORY_WORKOUT)
            .setContentIntent(open)
            .build()
    }

    companion object {
        private const val TAG = "WristHeatSession"
        private const val CHANNEL = "session"
        private const val NOTIFICATION_ID = 1
        const val ACTION_START = "com.wristheat.watch.START"
        const val ACTION_STOP = "com.wristheat.watch.STOP"

        fun start(context: Context) = ContextCompat.startForegroundService(
            context, Intent(context, SessionService::class.java).setAction(ACTION_START),
        )

        fun stop(context: Context) = context.startService(
            Intent(context, SessionService::class.java).setAction(ACTION_STOP),
        )
    }
}
