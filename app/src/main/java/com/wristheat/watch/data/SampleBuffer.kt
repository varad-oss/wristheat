package com.wristheat.watch.data

/**
 * In-memory queue of samples awaiting upload. Only strictly increasing `t` is accepted,
 * so duplicates and out-of-order points from Health Services never reach the server.
 * When full, the oldest sample is dropped. Thread-safe: the HR callback adds while
 * the uploader coroutine peeks and removes.
 */
class SampleBuffer(private val cap: Int = 900) {
    private val items = ArrayDeque<Sample>()
    private var lastT: Long = Long.MIN_VALUE

    @Synchronized
    fun add(s: Sample): Boolean {
        if (s.t <= lastT) return false
        lastT = s.t
        items.addLast(s)
        while (items.size > cap) items.removeFirst()
        return true
    }

    @Synchronized
    fun peek(max: Int): List<Sample> = items.take(max)

    @Synchronized
    fun remove(n: Int) {
        repeat(minOf(n, items.size)) { items.removeFirst() }
    }

    /** Removes every sample with t <= [t]. Safe even if the cap evicted some meanwhile. */
    @Synchronized
    fun removeThrough(t: Long) {
        while (items.isNotEmpty() && items.first().t <= t) items.removeFirst()
    }

    val size: Int
        @Synchronized get() = items.size

    @Synchronized
    fun oldestT(): Long? = items.firstOrNull()?.t
}
