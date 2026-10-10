package com.wristheat.watch.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlin.math.roundToInt

sealed interface ApiResult {
    data class Ok(val body: IngestResponse) : ApiResult
    data class Fatal(val code: String) : ApiResult        // 401, 404 → stop
    data class BadRequest(val code: String) : ApiResult   // 400 → drop this batch, continue
    data class Retry(val reason: String) : ApiResult      // IOException, 5xx, 429
}

interface Api {
    suspend fun ingest(req: IngestRequest): ApiResult
    suspend fun endSession(sessionId: String): Boolean
}

private val JSON_TYPE = "application/json; charset=utf-8".toMediaType()

fun defaultClient(): OkHttpClient = OkHttpClient.Builder()
    .connectTimeout(5, TimeUnit.SECONDS)
    .readTimeout(10, TimeUnit.SECONDS)
    .writeTimeout(10, TimeUnit.SECONDS)
    .build()

class OkHttpApi(
    baseUrl: String,
    private val token: String,
    private val client: OkHttpClient = defaultClient(),
) : Api {
    private val base = baseUrl.trimEnd('/')

    override suspend fun ingest(req: IngestRequest): ApiResult = withContext(Dispatchers.IO) {
        val body = WhJson.encodeToString(IngestRequest.serializer(), req).toRequestBody(JSON_TYPE)
        val request = Request.Builder()
            .url("$base/v1/ingest")
            .header("x-device-token", token)
            .post(body)
            .build()
        try {
            client.newCall(request).execute().use { resp ->
                val text = resp.body?.string().orEmpty()
                when (val code = resp.code) {
                    in 200..299 -> try {
                        ApiResult.Ok(WhJson.decodeFromString(IngestResponse.serializer(), text))
                    } catch (e: Exception) {
                        ApiResult.Retry("bad_response: ${e.message}")
                    }
                    401 -> ApiResult.Fatal(errorCode(text) ?: "unauthorized")
                    403 -> ApiResult.Fatal(errorCode(text) ?: "forbidden")
                    404 -> ApiResult.Fatal(errorCode(text) ?: "unknown_trainee")
                    400, 413, 422 -> ApiResult.BadRequest(errorCode(text) ?: "bad_request")
                    else -> ApiResult.Retry("http_$code")
                }
            }
        } catch (e: IOException) {
            ApiResult.Retry(e.javaClass.simpleName + ": " + e.message)
        }
    }

    override suspend fun endSession(sessionId: String): Boolean = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("$base/v1/sessions/$sessionId/end")
            .header("x-device-token", token)
            .post("{}".toRequestBody(JSON_TYPE))
            .build()
        try {
            client.newCall(request).execute().use { it.isSuccessful }
        } catch (e: IOException) {
            false
        }
    }

    private fun errorCode(text: String): String? = try {
        WhJson.decodeFromString(ApiError.serializer(), text).error.takeIf { it.isNotBlank() }
    } catch (e: Exception) {
        null
    }
}

/**
 * Offline stand-in for the cloud: one scripted step per call (5 s apart), walking
 * Calibrating → GREEN → AMBER → RED → RECOVERING → GREEN (recovered), then GREEN forever.
 */
class FakeApi(private val clock: Clock = SystemClock) : Api {
    private var step = 0
    private var lastHr: Int? = null

    private data class Step(
        val state: String, val alert: String = "NONE", val calib: Int = 0,
        val psi: Double? = null, val core: Double? = null, val mtr: Int? = null, val advice: String,
    )

    private val script: List<Step> = buildList {
        listOf(20, 15, 10, 5).forEach {
            add(Step("CALIBRATING", calib = it, advice = "Sit still — measuring your resting heart rate."))
        }
        add(Step("GREEN", psi = 1.2, core = 37.10, advice = "Strain low. Keep drinking water."))
        add(Step("AMBER", "AMBER", psi = 5.1, core = 37.70, mtr = 8, advice = "Strain rising. Slow down and drink water."))
        repeat(3) { add(Step("AMBER", psi = 5.4 + it * 0.2, core = 37.75 + it * 0.05, mtr = 7 - it, advice = "Strain rising. Slow down and drink water.")) }
        add(Step("RED", "RED", psi = 6.3, core = 38.06, advice = "Stop now. Rest in the shade and drink water."))
        repeat(3) { add(Step("RED", psi = 6.4, core = 38.10, advice = "Stop now. Rest in the shade and drink water.")) }
        repeat(3) { add(Step("RECOVERING", psi = 5.0 - it * 0.5, core = 38.0 - it * 0.03, advice = "Keep resting. Recovery in progress.")) }
        add(Step("GREEN", "RECOVERED", psi = 3.0, core = 37.95, advice = "Recovery confirmed. Resume only at an easier pace."))
    }
    private val steady = Step("GREEN", psi = 2.5, core = 37.80, advice = "Strain low. Keep drinking water.")

    override suspend fun ingest(req: IngestRequest): ApiResult {
        val s = script.getOrElse(step) { steady }
        step++
        if (req.samples.isNotEmpty()) lastHr = req.samples.map { it.bpm }.average().roundToInt()
        val now = clock.nowMs()
        val calibrating = s.state == "CALIBRATING"
        return ApiResult.Ok(
            IngestResponse(
                traineeId = req.traineeId, sessionId = req.sessionId,
                accepted = req.samples.size, dropped = 0,
                state = s.state, stateSince = now, calibrationRemainingS = s.calib,
                hrNow = lastHr, hr0 = if (calibrating) null else 74,
                coreEstC = s.core, coreBandC = 0.6, psi = s.psi, minutesToRed = s.mtr,
                env = Env(wbgtC = 31.4, flag = "RED", pm25 = 72.0, usAqi = 158, updatedAt = now, stale = false),
                advice = Advice(en = s.advice, hi = ""),
                alert = s.alert,
                incidentId = if (s.state == "RED" || s.alert == "RECOVERED") "inc-fake" else null,
                serverTime = now,
            )
        )
    }

    override suspend fun endSession(sessionId: String) = true
}
