package com.wristheat.watch.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class SampleBufferTest {
    @Test
    fun dropsNonIncreasing() {
        val b = SampleBuffer()
        assertTrue(b.add(Sample(1000, 80)))
        assertTrue(b.add(Sample(2000, 81)))
        assertFalse(b.add(Sample(2000, 82)))
        assertFalse(b.add(Sample(1500, 83)))
        assertTrue(b.add(Sample(3000, 84)))
        assertEquals(3, b.size)
        assertEquals(listOf(1000L, 2000L, 3000L), b.peek(10).map { it.t })
    }

    @Test
    fun capsAt900DropsOldest() {
        val b = SampleBuffer()
        for (i in 1..950) b.add(Sample(i * 1000L, 90))
        assertEquals(900, b.size)
        assertEquals(51_000L, b.oldestT())
    }

    @Test
    fun rejectsSampleOlderThanEvictedOne() {
        val b = SampleBuffer(cap = 2)
        b.add(Sample(1000, 80)); b.add(Sample(2000, 80)); b.add(Sample(3000, 80))
        assertFalse(b.add(Sample(1500, 80)))
        assertEquals(listOf(2000L, 3000L), b.peek(5).map { it.t })
    }

    @Test
    fun peekAndRemove() {
        val b = SampleBuffer()
        assertNull(b.oldestT())
        for (i in 1..5) b.add(Sample(i * 1000L, 90))
        assertEquals(3, b.peek(3).size)
        b.remove(2)
        assertEquals(3_000L, b.oldestT())
        b.removeThrough(4_000L)
        assertEquals(listOf(5_000L), b.peek(10).map { it.t })
        b.remove(10)
        assertEquals(0, b.size)
    }
}
