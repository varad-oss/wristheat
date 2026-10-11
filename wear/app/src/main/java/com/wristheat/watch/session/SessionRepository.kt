package com.wristheat.watch.session

import com.wristheat.watch.data.Clock
import com.wristheat.watch.data.IngestResponse
import com.wristheat.watch.data.SystemClock
import com.wristheat.watch.data.UploadStatus
import com.wristheat.watch.sensors.HrSample
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

/** Single source of UI truth: reduces local samples, server responses and upload status. */
object SessionRepository {
    private const val AMBER_OVERLAY_MS = 5_000L
    private const val RECOVERED_OVERLAY_MS = 8_000L

    private val _ui = MutableStateFlow(UiState())
    val ui: StateFlow<UiState> = _ui.asStateFlow()

    var clock: Clock = SystemClock

    /** Set by the service so a tap on the RED overlay stops the repeat vibration. */
    @Volatile var onRedAcknowledged: (() -> Unit)? = null

    @Volatile private var overlayUntil: Long? = null

    fun reset(phase: Phase = Phase.IDLE, error: String? = null) {
        overlayUntil = null
        _ui.value = UiState(phase = phase, error = error)
    }

    fun startSession() {
        overlayUntil = null
        _ui.value = UiState(phase = Phase.STARTING, startedAtMs = clock.nowMs())
    }

    fun onPhase(phase: Phase) = _ui.update { it.copy(phase = phase) }

    fun onLocalSample(s: HrSample) = _ui.update { it.copy(hrLocal = s.bpm) }

    fun onResponse(r: IngestResponse) {
        val now = clock.nowMs()
        _ui.update { cur ->
            var overlay = cur.overlay
            // Leaving RED clears the RED overlay.
            if (overlay == Overlay.RED && r.state != "RED") overlay = null
            when (r.alert) {
                "AMBER" -> if (overlay != Overlay.RED) {
                    overlay = Overlay.AMBER; overlayUntil = now + AMBER_OVERLAY_MS
                }
                "RED" -> { overlay = Overlay.RED; overlayUntil = null }
                "RECOVERED" -> { overlay = Overlay.RECOVERED; overlayUntil = now + RECOVERED_OVERLAY_MS }
            }
            cur.copy(
                state = r.state,
                hrServer = r.hrNow,
                coreEst = r.coreEstC,
                coreBand = r.coreBandC,
                psi = r.psi,
                minutesToRed = r.minutesToRed,
                calibrationRemainingS = r.calibrationRemainingS,
                wbgt = r.env?.wbgtC,
                flag = r.env?.flag,
                envStale = r.env?.stale ?: false,
                adviceEn = r.advice?.en?.takeIf { it.isNotBlank() },
                overlay = overlay,
                gotResponse = true,
            )
        }
    }

    fun onStatus(u: UploadStatus) = _ui.update {
        if (u is UploadStatus.Fatal) it.copy(upload = u, phase = Phase.SETUP_ERROR, error = u.code)
        else it.copy(upload = u)
    }

    fun onError(code: String) = _ui.update { it.copy(error = code) }

    /** Called every second: expires timed overlays. */
    fun onTick() {
        val until = overlayUntil ?: return
        if (clock.nowMs() >= until) {
            overlayUntil = null
            _ui.update { if (it.overlay == Overlay.AMBER || it.overlay == Overlay.RECOVERED) it.copy(overlay = null) else it }
        }
    }

    fun dismissOverlay() {
        val was = _ui.value.overlay
        overlayUntil = null
        _ui.update { it.copy(overlay = null) }
        if (was == Overlay.RED) onRedAcknowledged?.invoke()
    }
}
