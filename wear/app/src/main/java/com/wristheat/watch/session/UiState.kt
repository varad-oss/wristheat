package com.wristheat.watch.session

import com.wristheat.watch.data.UploadStatus

enum class Phase { IDLE, STARTING, RUNNING, ENDING, SETUP_ERROR }

enum class Overlay { AMBER, RED, RECOVERED }

data class UiState(
    val phase: Phase = Phase.IDLE,
    val state: String? = null,               // server state
    val hrLocal: Int? = null,                // last local sample (instant feedback)
    val hrServer: Int? = null,
    val coreEst: Double? = null,
    val coreBand: Double? = null,
    val psi: Double? = null,
    val minutesToRed: Int? = null,
    val calibrationRemainingS: Int? = null,
    val wbgt: Double? = null,
    val flag: String? = null,
    val envStale: Boolean = false,
    val adviceEn: String? = null,
    val upload: UploadStatus = UploadStatus.Ok,
    val overlay: Overlay? = null,
    val error: String? = null,
    val startedAtMs: Long? = null,           // for the local calibration countdown
    val gotResponse: Boolean = false,
)
