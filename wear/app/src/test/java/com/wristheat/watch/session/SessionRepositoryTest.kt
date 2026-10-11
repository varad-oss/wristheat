package com.wristheat.watch.session

import com.wristheat.watch.data.UploadStatus
import com.wristheat.watch.data.loadResponse
import com.wristheat.watch.sensors.HrSample
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

class SessionRepositoryTest {
    @Before fun reset() {
        SessionRepository.reset()
        SessionRepository.onPhase(Phase.RUNNING)
    }

    @Test
    fun reducesResponse() {
        SessionRepository.onResponse(loadResponse("amber_alert"))
        val ui = SessionRepository.ui.value
        assertEquals(Overlay.AMBER, ui.overlay)
        assertEquals(5.6, ui.psi!!, 1e-9)
        assertEquals("RED", ui.flag)
        assertEquals("AMBER", ui.state)
        assertEquals(163, ui.hrServer)
        assertEquals(37.78, ui.coreEst!!, 1e-9)
        assertEquals(0.6, ui.coreBand!!, 1e-9)
        assertEquals(7, ui.minutesToRed)
        assertEquals(31.4, ui.wbgt!!, 1e-9)
        assertEquals("Strain rising. Slow down and drink water.", ui.adviceEn)
    }

    @Test
    fun fatalShowsSetupError() {
        SessionRepository.onStatus(UploadStatus.Fatal("unauthorized"))
        val ui = SessionRepository.ui.value
        assertEquals(Phase.SETUP_ERROR, ui.phase)
        assertEquals("unauthorized", ui.error)
        assertEquals(UploadStatus.Fatal("unauthorized"), ui.upload)
    }

    @Test
    fun localSampleUpdatesHr() {
        SessionRepository.onLocalSample(HrSample(1, 101))
        assertEquals(101, SessionRepository.ui.value.hrLocal)
    }

    @Test
    fun noneAlertKeepsOverlayAndRedClearsWhenStateLeavesRed() {
        SessionRepository.onResponse(loadResponse("red_alert"))
        assertEquals(Overlay.RED, SessionRepository.ui.value.overlay)
        // A later NONE response while still RED keeps the overlay up.
        SessionRepository.onResponse(loadResponse("red_alert").copy(alert = "NONE"))
        assertEquals(Overlay.RED, SessionRepository.ui.value.overlay)
        // State leaves RED → RED overlay cleared.
        SessionRepository.onResponse(loadResponse("red_alert").copy(alert = "NONE", state = "RECOVERING"))
        assertNull(SessionRepository.ui.value.overlay)
    }

    @Test
    fun recoveredOverlayAndDismiss() {
        SessionRepository.onResponse(loadResponse("recovered_alert"))
        assertEquals(Overlay.RECOVERED, SessionRepository.ui.value.overlay)
        SessionRepository.dismissOverlay()
        assertNull(SessionRepository.ui.value.overlay)
    }

    @Test
    fun envMissingAndCalibrating() {
        SessionRepository.onResponse(loadResponse("env_missing"))
        assertNull(SessionRepository.ui.value.flag)
        assertNull(SessionRepository.ui.value.wbgt)
        SessionRepository.onResponse(loadResponse("calibrating"))
        val ui = SessionRepository.ui.value
        assertEquals("CALIBRATING", ui.state)
        assertEquals(95, ui.calibrationRemainingS)
        assertNull(ui.psi)
        assertNull(ui.overlay)
    }

    @Test
    fun hrErrorCodeSurfaced() {
        SessionRepository.onError("exercise_in_use")
        assertEquals("exercise_in_use", SessionRepository.ui.value.error)
        assertTrue(SessionRepository.ui.value.phase != Phase.SETUP_ERROR)
    }
}
