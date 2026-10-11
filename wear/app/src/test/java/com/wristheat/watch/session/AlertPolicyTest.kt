package com.wristheat.watch.session

import com.wristheat.watch.data.FakeClock
import org.junit.Assert.assertEquals
import org.junit.Test

class AlertPolicyTest {
    private val clock = FakeClock(0)
    private val policy = AlertPolicy(clock)

    @Test
    fun noneNeverBuzzes() {
        assertEquals(emptyList<Buzz>(), policy.onResponse("NONE", "GREEN"))
        assertEquals(emptyList<Buzz>(), policy.onResponse("NONE", "RED"))
        clock.advance(60_000)
        assertEquals(emptyList<Buzz>(), policy.onTick("RED"))
    }

    @Test
    fun amberBuzzesOnce() {
        assertEquals(listOf(Buzz.AMBER), policy.onResponse("AMBER", "AMBER"))
        assertEquals(emptyList<Buzz>(), policy.onResponse("NONE", "AMBER"))
        for (s in 1..30) {
            clock.advance(1000)
            assertEquals(emptyList<Buzz>(), policy.onTick("AMBER"))
        }
    }

    @Test
    fun redRepeatsUntilAcknowledgedOrStateChanges() {
        assertEquals(listOf(Buzz.RED), policy.onResponse("RED", "RED"))
        clock.now = 5_000
        assertEquals(emptyList<Buzz>(), policy.onTick("RED"))
        clock.now = 10_000
        assertEquals(listOf(Buzz.RED), policy.onTick("RED"))
        clock.now = 15_000
        assertEquals(emptyList<Buzz>(), policy.onTick("RED"))
        clock.now = 20_000
        assertEquals(listOf(Buzz.RED), policy.onTick("RED"))
        policy.acknowledgeRed()
        clock.now = 30_000
        assertEquals(emptyList<Buzz>(), policy.onTick("RED"))
        clock.now = 60_000
        assertEquals(emptyList<Buzz>(), policy.onTick("RED"))

        // Separately: leaving RED stops repeats.
        val p2 = AlertPolicy(clock)
        clock.now = 100_000
        p2.onResponse("RED", "RED")
        clock.now = 105_000
        assertEquals(emptyList<Buzz>(), p2.onResponse("NONE", "RECOVERING"))
        clock.now = 110_000
        assertEquals(emptyList<Buzz>(), p2.onTick("RECOVERING"))
        clock.now = 130_000
        assertEquals(emptyList<Buzz>(), p2.onTick("RED")) // only a new RED alert re-arms
    }

    @Test
    fun redRepeatsAreSpacedByTenSecondsWithOneSecondTicks() {
        policy.onResponse("RED", "RED")
        var buzzes = 0
        for (s in 1..30) {
            clock.advance(1000)
            buzzes += policy.onTick("RED").size
        }
        assertEquals(3, buzzes) // at 10, 20, 30 s
    }

    @Test
    fun recoveredBuzzesOnce() {
        assertEquals(listOf(Buzz.RECOVERED), policy.onResponse("RECOVERED", "GREEN"))
        clock.advance(20_000)
        assertEquals(emptyList<Buzz>(), policy.onTick("GREEN"))
        assertEquals(emptyList<Buzz>(), policy.onResponse("NONE", "GREEN"))
    }

    @Test
    fun unknownAlertIgnored() {
        assertEquals(emptyList<Buzz>(), policy.onResponse("PURPLE", "GREEN"))
    }
}
