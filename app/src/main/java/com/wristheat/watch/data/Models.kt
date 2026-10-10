package com.wristheat.watch.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

/** Shared JSON config. encodeDefaults so schema/source/device are always sent. */
val WhJson = Json {
    ignoreUnknownKeys = true
    explicitNulls = false
    encodeDefaults = true
}

@Serializable
data class Sample(val t: Long, val bpm: Int)

@Serializable
data class IngestRequest(
    val schema: Int = 1,
    @SerialName("trainee_id") val traineeId: String,
    @SerialName("session_id") val sessionId: String,
    val source: String = "live",
    val device: String = "SM-R920",
    val samples: List<Sample>,
)

@Serializable
data class Env(
    @SerialName("wbgt_c") val wbgtC: Double? = null,
    val flag: String = "NONE",
    val pm25: Double? = null,
    @SerialName("us_aqi") val usAqi: Int? = null,
    @SerialName("updated_at") val updatedAt: Long = 0,
    val stale: Boolean = false,
)

@Serializable
data class Advice(val en: String = "", val hi: String = "")

@Serializable
data class IngestResponse(
    val schema: Int = 1,
    @SerialName("trainee_id") val traineeId: String = "",
    @SerialName("session_id") val sessionId: String = "",
    val accepted: Int = 0,
    val dropped: Int = 0,
    val state: String,
    @SerialName("state_since") val stateSince: Long? = null,
    @SerialName("calibration_remaining_s") val calibrationRemainingS: Int? = null,
    @SerialName("hr_now") val hrNow: Int? = null,
    val hr0: Int? = null,
    @SerialName("core_est_c") val coreEstC: Double? = null,
    @SerialName("core_band_c") val coreBandC: Double? = null,
    val psi: Double? = null,
    @SerialName("minutes_to_red") val minutesToRed: Int? = null,
    val env: Env? = null,
    val advice: Advice? = null,
    val alert: String = "NONE",
    @SerialName("incident_id") val incidentId: String? = null,
    @SerialName("server_time") val serverTime: Long? = null,
)

@Serializable
data class ApiError(val error: String, val message: String = "")
