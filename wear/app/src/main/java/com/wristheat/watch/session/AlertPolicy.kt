package com.wristheat.watch.session

import com.wristheat.watch.data.Clock

enum class Buzz { AMBER, RED, RECOVERED }

/**
 * Decides vibrations. Buzzes only on the server's one-shot `alert` field, never on `state`.
 * A RED alert repeats every 10 s until acknowledged or the state leaves RED.
 */
class AlertPolicy(private val clock: Clock) {
    private var redActive = false
    private var lastRedBuzzAt = 0L

    fun onResponse(alert: String, state: String): List<Buzz> {
        if (state != "RED") redActive = false
        return when (alert) {
            "AMBER" -> listOf(Buzz.AMBER)
            "RED" -> {
                redActive = true
                lastRedBuzzAt = clock.nowMs()
                listOf(Buzz.RED)
            }
            "RECOVERED" -> {
                redActive = false
                listOf(Buzz.RECOVERED)
            }
            else -> emptyList()
        }
    }

    fun onTick(state: String): List<Buzz> {
        if (state != "RED") redActive = false
        if (!redActive) return emptyList()
        val now = clock.nowMs()
        if (now - lastRedBuzzAt < REPEAT_MS) return emptyList()
        lastRedBuzzAt = now
        return listOf(Buzz.RED)
    }

    fun acknowledgeRed() {
        redActive = false
    }

    companion object {
        const val REPEAT_MS = 10_000L
    }
}
