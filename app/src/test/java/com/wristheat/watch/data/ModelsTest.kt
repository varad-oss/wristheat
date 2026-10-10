package com.wristheat.watch.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class ModelsTest {
    @Test
    fun parsesAllExamples() {
        val amber = loadResponse("amber_alert")
        assertEquals("AMBER", amber.alert)
        assertEquals(5.6, amber.psi!!, 1e-9)
        assertEquals("RED", amber.env!!.flag)

        val calibrating = loadResponse("calibrating")
        assertNull(calibrating.hr0)
        assertEquals(95, calibrating.calibrationRemainingS)
        assertNull(calibrating.psi)

        assertNull(loadResponse("env_missing").env)
        assertNotNull(loadResponse("red_alert").incidentId)
        assertEquals("RECOVERED", loadResponse("recovered_alert").alert)

        val err = WhJson.decodeFromString(ApiError.serializer(), loadContract("error.unauthorized.json"))
        assertEquals("unauthorized", err.error)

        val req = WhJson.decodeFromString(IngestRequest.serializer(), loadContract("ingest_request.live.json"))
        assertEquals(5, req.samples.size)
    }

    @Test
    fun encodesRequestFieldNames() {
        val req = IngestRequest(
            traineeId = "T1",
            sessionId = "3f6c1e9a-0b7d-4a51-9a52-0c3c0d2f8e11",
            samples = listOf(Sample(1791700000000, 92)),
        )
        val json = WhJson.encodeToString(IngestRequest.serializer(), req)
        assertTrue(json, json.contains("\"trainee_id\""))
        assertTrue(json, json.contains("\"session_id\""))
        assertTrue(json, json.contains("\"samples\":[{\"t\":1791700000000,\"bpm\":92}]"))
        assertTrue(json, json.contains("\"schema\":1"))
        assertTrue(json, json.contains("\"source\":\"live\""))
        assertTrue(json, json.contains("\"device\":\"SM-R920\""))
    }
}
