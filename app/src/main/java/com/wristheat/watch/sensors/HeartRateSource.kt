package com.wristheat.watch.sensors

import android.Manifest
import android.content.Context
import android.os.Build
import android.os.SystemClock
import android.util.Log
import androidx.concurrent.futures.await
import androidx.health.services.client.ExerciseUpdateCallback
import androidx.health.services.client.HealthServices
import androidx.health.services.client.MeasureCallback
import androidx.health.services.client.data.Availability
import androidx.health.services.client.data.DataPointContainer
import androidx.health.services.client.data.DataType
import androidx.health.services.client.data.DeltaDataType
import androidx.health.services.client.data.ExerciseConfig
import androidx.health.services.client.data.ExerciseLapSummary
import androidx.health.services.client.data.ExerciseTrackedStatus
import androidx.health.services.client.data.ExerciseType
import androidx.health.services.client.data.ExerciseUpdate
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.time.Instant
import kotlin.math.roundToInt
import kotlin.random.Random

data class HrSample(val tMs: Long, val bpm: Int)

interface HeartRateSource {
    suspend fun start(onSample: (HrSample) -> Unit, onError: (String) -> Unit)
    suspend fun stop()
}

private const val TAG = "WristHeatHR"

/** android.health.connect.HealthPermissions.READ_HEART_RATE (API 36+). */
const val READ_HEART_RATE = "android.permission.health.READ_HEART_RATE"

/** Runtime permissions for HR (Wear OS 6 guidance) plus notifications for the foreground service. */
fun heartRatePermissions(): Array<String> = buildList {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.BAKLAVA) add(READ_HEART_RATE)
    else add(Manifest.permission.BODY_SENSORS)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) add(Manifest.permission.POST_NOTIFICATIONS)
}.toTypedArray()

/** Converts Health Services' boot-relative sample times to epoch ms. */
private fun emitHr(data: DataPointContainer, onSample: (HrSample) -> Unit) {
    val bootInstant = Instant.ofEpochMilli(System.currentTimeMillis() - SystemClock.elapsedRealtime())
    data.getData(DataType.HEART_RATE_BPM).forEach { dp ->
        val bpm = dp.value.roundToInt()
        if (bpm > 0) onSample(HrSample(dp.getTimeInstant(bootInstant).toEpochMilli(), bpm))
    }
}

/** HR from a Health Services exercise session; keeps running with the screen off. */
class ExerciseHeartRateSource(context: Context) : HeartRateSource {
    private val client = HealthServices.getClient(context.applicationContext).exerciseClient
    private var callback: ExerciseUpdateCallback? = null
    @Volatile private var stopRequested = false

    override suspend fun start(onSample: (HrSample) -> Unit, onError: (String) -> Unit) {
        stopRequested = false
        try {
            val caps = client.getCapabilitiesAsync().await()
            val supported = ExerciseType.RUNNING in caps.supportedExerciseTypes &&
                DataType.HEART_RATE_BPM in caps.getExerciseTypeCapabilities(ExerciseType.RUNNING).supportedDataTypes
            if (!supported) {
                onError("hr_unsupported"); return
            }
            val info = client.getCurrentExerciseInfoAsync().await()
            if (info.exerciseTrackedStatus == ExerciseTrackedStatus.OTHER_APP_IN_PROGRESS) {
                onError("exercise_in_use"); return
            }
            val cb = object : ExerciseUpdateCallback {
                override fun onExerciseUpdateReceived(update: ExerciseUpdate) {
                    emitHr(update.latestMetrics, onSample)
                    val state = update.exerciseStateInfo.state
                    if (state.isEnded && !stopRequested) {
                        Log.w(TAG, "exercise ended: $state reason=${update.exerciseStateInfo.endReason}")
                        onError("exercise_ended")
                    }
                }
                override fun onLapSummaryReceived(lapSummary: ExerciseLapSummary) = Unit
                override fun onRegistered() = Unit
                override fun onRegistrationFailed(throwable: Throwable) {
                    Log.e(TAG, "callback registration failed", throwable)
                    onError("hr_registration_failed")
                }
                override fun onAvailabilityChanged(dataType: DataType<*, *>, availability: Availability) {
                    Log.i(TAG, "availability $dataType: $availability")
                }
            }
            callback = cb
            client.setUpdateCallback(cb)
            val config = ExerciseConfig.builder(ExerciseType.RUNNING)
                .setDataTypes(setOf(DataType.HEART_RATE_BPM))
                .setIsAutoPauseAndResumeEnabled(false)
                .setIsGpsEnabled(false)
                .build()
            client.startExerciseAsync(config).await()
            Log.i(TAG, "exercise started")
        } catch (e: SecurityException) {
            Log.e(TAG, "start exercise: missing permission", e)
            onError("permission_denied")
        } catch (e: Exception) {
            Log.e(TAG, "start exercise failed", e)
            onError("hr_start_failed")
        }
    }

    override suspend fun stop() {
        stopRequested = true
        runCatching { client.endExerciseAsync().await() }.onFailure { Log.w(TAG, "end exercise", it) }
        callback?.let { cb -> runCatching { client.clearUpdateCallbackAsync(cb).await() } }
        callback = null
    }
}

/** HR from MeasureClient; only delivers while the app is in the foreground (screen kept on). */
class MeasureHeartRateSource(context: Context) : HeartRateSource {
    private val client = HealthServices.getClient(context.applicationContext).measureClient
    private var callback: MeasureCallback? = null

    override suspend fun start(onSample: (HrSample) -> Unit, onError: (String) -> Unit) {
        try {
            val caps = client.getCapabilitiesAsync().await()
            if (DataType.HEART_RATE_BPM !in caps.supportedDataTypesMeasure) {
                onError("hr_unsupported"); return
            }
            val cb = object : MeasureCallback {
                override fun onAvailabilityChanged(dataType: DeltaDataType<*, *>, availability: Availability) {
                    Log.i(TAG, "measure availability: $availability")
                }
                override fun onDataReceived(data: DataPointContainer) = emitHr(data, onSample)
                override fun onRegistrationFailed(throwable: Throwable) {
                    Log.e(TAG, "measure registration failed", throwable)
                    onError("hr_registration_failed")
                }
            }
            callback = cb
            client.registerMeasureCallback(DataType.HEART_RATE_BPM, cb)
        } catch (e: SecurityException) {
            onError("permission_denied")
        } catch (e: Exception) {
            Log.e(TAG, "measure start failed", e)
            onError("hr_start_failed")
        }
    }

    override suspend fun stop() {
        callback?.let { cb -> runCatching { client.unregisterMeasureCallbackAsync(DataType.HEART_RATE_BPM, cb).await() } }
        callback = null
    }
}

/** 1 Hz synthetic HR: rest 72–75 for 150 s, ramp to 165 over 60 s, hold 600 s, decay to 95. */
class FakeHeartRateSource(private val scope: CoroutineScope) : HeartRateSource {
    private var job: Job? = null

    override suspend fun start(onSample: (HrSample) -> Unit, onError: (String) -> Unit) {
        job?.cancel()
        job = scope.launch {
            var sec = 0
            while (isActive) {
                onSample(HrSample(System.currentTimeMillis(), fakeBpm(sec)))
                sec++
                delay(1000)
            }
        }
    }

    override suspend fun stop() {
        job?.cancel(); job = null
    }

    companion object {
        fun fakeBpm(sec: Int, rnd: Random = Random): Int = when {
            sec < 150 -> 72 + rnd.nextInt(4)
            sec < 210 -> 74 + ((165 - 74) * (sec - 150) / 60.0).roundToInt()
            sec < 810 -> 163 + rnd.nextInt(5)
            else -> (95 + (165 - 95) * Math.exp(-(sec - 810) / 90.0)).roundToInt()
        }
    }
}
