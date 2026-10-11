package com.wristheat.watch.data

import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class FakeClock(var now: Long = 1_791_700_000_000L) : Clock {
    override fun nowMs() = now
    fun advance(ms: Long) { now += ms }
}

/** Api double that replays scripted results and records requests. */
class ScriptedApi(vararg results: ApiResult) : Api {
    private val queue = ArrayDeque(results.toList())
    val requests = mutableListOf<IngestRequest>()
    var fallback: ApiResult = ApiResult.Ok(loadResponse("calibrating"))
    override suspend fun ingest(req: IngestRequest): ApiResult {
        requests += req
        return queue.removeFirstOrNull() ?: fallback
    }
    override suspend fun endSession(sessionId: String) = true
}

class UploaderTest {
    private val ok = ApiResult.Ok(loadResponse("calibrating"))

    private fun uploader(
        api: Api, buffer: SampleBuffer, clock: Clock,
        responses: MutableList<IngestResponse> = mutableListOf(),
        statuses: MutableList<UploadStatus> = mutableListOf(),
    ) = Uploader(api, buffer, clock, "T1", "sess-1234", { responses += it }, { statuses += it })

    @Test
    fun sendsBatchEvery5s() = runTest {
        val clock = FakeClock()
        val buf = SampleBuffer()
        val api = ScriptedApi()
        val responses = mutableListOf<IngestResponse>()
        val up = uploader(api, buf, clock, responses)
        for (i in 0 until 5) buf.add(Sample(clock.now - 5000 + i * 1000L, 90 + i))

        up.tick()
        assertEquals(1, api.requests.size)
        assertEquals(5, api.requests[0].samples.size)
        assertEquals("T1", api.requests[0].traineeId)
        assertEquals("sess-1234", api.requests[0].sessionId)
        assertEquals(0, buf.size)
        assertEquals(1, responses.size)
        assertEquals(5000L, up.nextDelayMs())

        clock.advance(1000)
        up.tick() // not due yet
        assertEquals(1, api.requests.size)

        buf.add(Sample(clock.now, 100))
        clock.advance(4000)
        up.tick()
        assertEquals(2, api.requests.size)
        assertEquals(1, api.requests[1].samples.size)
    }

    @Test
    fun capsBatchAt600() = runTest {
        val clock = FakeClock()
        val buf = SampleBuffer()
        for (i in 1..700) buf.add(Sample(i * 1000L, 90))
        val api = ScriptedApi()
        uploader(api, buf, clock).tick()
        assertEquals(600, api.requests[0].samples.size)
        assertEquals(100, buf.size)
    }

    @Test
    fun backoffSequence() = runTest {
        val clock = FakeClock()
        val buf = SampleBuffer()
        buf.add(Sample(clock.now - 45_000, 90))
        val api = ScriptedApi(*Array(6) { ApiResult.Retry("io") }, ok)
        val statuses = mutableListOf<UploadStatus>()
        val up = uploader(api, buf, clock, statuses = statuses)
        val delays = mutableListOf<Long>()
        repeat(6) {
            up.tick()
            delays += up.nextDelayMs()
            clock.advance(up.nextDelayMs())
        }
        assertEquals(listOf(2000L, 4000L, 8000L, 16000L, 30000L, 30000L), delays)
        assertEquals(6, api.requests.size)
        assertEquals(1, buf.size) // kept while retrying
        assertEquals(UploadStatus.Offline(45), statuses.first())
        up.tick()
        assertEquals(5000L, up.nextDelayMs())
        assertEquals(0, buf.size)
        assertEquals(UploadStatus.Ok, statuses.last())
    }

    @Test
    fun fatalOn401And404() = runTest {
        for (code in listOf("unauthorized", "unknown_trainee")) {
            val clock = FakeClock()
            val api = ScriptedApi(ApiResult.Fatal(code))
            val statuses = mutableListOf<UploadStatus>()
            val up = uploader(api, SampleBuffer(), clock, statuses = statuses)
            up.tick()
            assertEquals(UploadStatus.Fatal(code), statuses.last())
            repeat(3) { clock.advance(60_000); up.tick() }
            assertEquals(1, api.requests.size)
        }
    }

    @Test
    fun badRequestDropsBatch() = runTest {
        val clock = FakeClock()
        val buf = SampleBuffer()
        buf.add(Sample(1000, 90)); buf.add(Sample(2000, 91))
        val api = ScriptedApi(ApiResult.BadRequest("bad_request"))
        val up = uploader(api, buf, clock)
        up.tick()
        assertEquals(0, buf.size)
        assertEquals(5000L, up.nextDelayMs())
        clock.advance(5000)
        up.tick()
        assertEquals(2, api.requests.size)
    }

    @Test
    fun emptyPollWhenNoSamples() = runTest {
        val api = ScriptedApi()
        val responses = mutableListOf<IngestResponse>()
        uploader(api, SampleBuffer(), FakeClock(), responses).tick()
        assertEquals(1, api.requests.size)
        assertTrue(api.requests[0].samples.isEmpty())
        assertEquals(1, responses.size)
    }

    @Test
    fun samplesAddedDuringFlightAreKept() = runTest {
        val clock = FakeClock()
        val buf = SampleBuffer(cap = 3)
        buf.add(Sample(1000, 90)); buf.add(Sample(2000, 90))
        val api = object : Api {
            override suspend fun ingest(req: IngestRequest): ApiResult {
                // Two new samples arrive while in flight; cap evicts 1000.
                buf.add(Sample(3000, 90)); buf.add(Sample(4000, 90))
                return ApiResult.Ok(loadResponse("calibrating"))
            }
            override suspend fun endSession(sessionId: String) = true
        }
        uploader(api, buf, clock).tick()
        assertEquals(listOf(3000L, 4000L), buf.peek(10).map { it.t })
    }
}
