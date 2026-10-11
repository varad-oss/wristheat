package com.wristheat.watch.data

import kotlinx.coroutines.test.runTest
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import okhttp3.mockwebserver.SocketPolicy
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

class OkHttpApiTest {
    private lateinit var server: MockWebServer
    private lateinit var api: OkHttpApi
    private val req = IngestRequest(traineeId = "T1", sessionId = "sess-1234", samples = listOf(Sample(1791700000000, 92)))

    @Before fun setUp() {
        server = MockWebServer().apply { start() }
        api = OkHttpApi(server.url("/").toString(), "tok-abc")
    }

    @After fun tearDown() = server.shutdown()

    private fun json(code: Int, body: String) =
        MockResponse().setResponseCode(code).setHeader("content-type", "application/json; charset=utf-8").setBody(body)

    @Test
    fun sendsHeaderPathAndJson() = runTest {
        server.enqueue(json(200, loadContract("ingest_response.amber_alert.json")))
        val r = api.ingest(req)
        assertTrue(r is ApiResult.Ok)
        val rec = server.takeRequest()
        assertEquals("/v1/ingest", rec.path)
        assertEquals("POST", rec.method)
        assertEquals("tok-abc", rec.getHeader("x-device-token"))
        assertTrue(rec.getHeader("content-type")!!.startsWith("application/json"))
        val body = rec.body.readUtf8()
        assertTrue(body, body.contains("\"trainee_id\":\"T1\""))
    }

    @Test
    fun mapsStatusCodes() = runTest {
        server.enqueue(json(200, loadContract("ingest_response.calibrating.json")))
        server.enqueue(json(401, """{"error":"unauthorized","message":"x"}"""))
        server.enqueue(json(404, """{"error":"unknown_trainee","message":"x"}"""))
        server.enqueue(json(400, """{"error":"source_mismatch","message":"x"}"""))
        server.enqueue(json(503, """{"message":"Service Unavailable"}"""))
        server.enqueue(json(401, "not json"))

        assertTrue(api.ingest(req) is ApiResult.Ok)
        assertEquals(ApiResult.Fatal("unauthorized"), api.ingest(req))
        assertEquals(ApiResult.Fatal("unknown_trainee"), api.ingest(req))
        assertEquals(ApiResult.BadRequest("source_mismatch"), api.ingest(req))
        assertTrue(api.ingest(req) is ApiResult.Retry)
        assertEquals(ApiResult.Fatal("unauthorized"), api.ingest(req))
    }

    @Test
    fun networkFailureIsRetry() = runTest {
        server.enqueue(MockResponse().setSocketPolicy(SocketPolicy.DISCONNECT_AT_START))
        assertTrue(api.ingest(req) is ApiResult.Retry)
    }

    @Test
    fun parsesHindiAdviceIntact() = runTest {
        server.enqueue(json(200, loadContract("ingest_response.amber_alert.json")))
        val r = api.ingest(req) as ApiResult.Ok
        assertEquals("तनाव बढ़ रहा है। गति धीमी करें और पानी पिएँ।", r.body.advice!!.hi)
    }

    @Test
    fun endSessionPostsToSessionPath() = runTest {
        server.enqueue(json(200, """{"ended": true}"""))
        assertTrue(api.endSession("sess-1234"))
        val rec = server.takeRequest()
        assertEquals("/v1/sessions/sess-1234/end", rec.path)
        assertEquals("tok-abc", rec.getHeader("x-device-token"))
    }

    @Test
    fun baseUrlWithoutTrailingSlash() = runTest {
        val noSlash = OkHttpApi(server.url("/").toString().trimEnd('/'), "t")
        server.enqueue(json(200, loadContract("ingest_response.calibrating.json")))
        noSlash.ingest(req)
        assertEquals("/v1/ingest", server.takeRequest().path)
    }
}
