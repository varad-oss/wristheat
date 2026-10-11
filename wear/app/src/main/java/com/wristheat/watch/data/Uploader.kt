package com.wristheat.watch.data

interface Clock {
    fun nowMs(): Long
}

object SystemClock : Clock {
    override fun nowMs() = System.currentTimeMillis()
}

sealed interface UploadStatus {
    data object Ok : UploadStatus
    data class Offline(val bufferedSeconds: Int) : UploadStatus
    data class Fatal(val code: String) : UploadStatus
}

/**
 * Sends the buffered samples every 5 s (an empty list acts as a poll). Keeps samples
 * and backs off 2→4→8→16→30 s on retryable errors; stops for good on 401/404.
 * Pure Kotlin: the caller drives it with `tick(); delay(nextDelayMs())`.
 */
class Uploader(
    private val api: Api,
    private val buffer: SampleBuffer,
    private val clock: Clock,
    private val traineeId: String,
    private val sessionId: String,
    private val onResponse: (IngestResponse) -> Unit,
    private val onStatus: (UploadStatus) -> Unit,
    private val log: (String) -> Unit = {},
) {
    private var delayMs = 0L
    private var lastAttemptAt: Long? = null
    private var retries = 0
    var stopped = false
        private set

    suspend fun tick() {
        if (stopped) return
        val now = clock.nowMs()
        val last = lastAttemptAt
        // Due when the delay has elapsed (small slack for timer jitter), or the wall
        // clock jumped backwards.
        if (last != null && now >= last && now - last < delayMs - SLACK_MS) return
        lastAttemptAt = now

        val batch = buffer.peek(MAX_BATCH)
        val result = api.ingest(IngestRequest(traineeId = traineeId, sessionId = sessionId, samples = batch))
        when (result) {
            is ApiResult.Ok -> {
                batch.lastOrNull()?.let { buffer.removeThrough(it.t) }
                succeed()
                onResponse(result.body)
            }
            is ApiResult.BadRequest -> {
                log("ingest rejected (${result.code}); dropping ${batch.size} samples")
                batch.lastOrNull()?.let { buffer.removeThrough(it.t) }
                succeed()
            }
            is ApiResult.Retry -> {
                delayMs = BACKOFF[minOf(retries, BACKOFF.lastIndex)]
                retries++
                log("ingest retry in ${delayMs}ms (${result.reason})")
                onStatus(UploadStatus.Offline(bufferedSeconds()))
            }
            is ApiResult.Fatal -> {
                stopped = true
                log("ingest fatal (${result.code}); stopping")
                onStatus(UploadStatus.Fatal(result.code))
            }
        }
    }

    /**
     * Sends everything still buffered, ignoring backoff (used when the session stops).
     * Returns true when the buffer is empty; false when the network is still unreachable.
     */
    suspend fun flush(maxAttempts: Int = 10): Boolean {
        repeat(maxAttempts) {
            if (stopped) return false
            if (buffer.oldestT() == null) return true
            lastAttemptAt = null
            delayMs = 0
            val before = buffer.oldestT()
            tick()
            if (buffer.oldestT() == before) return false // not accepted: still offline
        }
        return buffer.oldestT() == null
    }

    fun nextDelayMs(): Long = if (lastAttemptAt == null) 0L else delayMs

    fun bufferedSeconds(): Int {
        val oldest = buffer.oldestT() ?: return 0
        return ((clock.nowMs() - oldest) / 1000).coerceAtLeast(0).toInt()
    }

    private fun succeed() {
        retries = 0
        delayMs = NORMAL_MS
        onStatus(UploadStatus.Ok)
    }

    companion object {
        const val NORMAL_MS = 5_000L
        const val MAX_BATCH = 600
        private const val SLACK_MS = 250L
        private val BACKOFF = longArrayOf(2_000, 4_000, 8_000, 16_000, 30_000)
    }
}
