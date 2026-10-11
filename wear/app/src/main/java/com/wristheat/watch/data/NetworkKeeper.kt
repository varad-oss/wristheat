package com.wristheat.watch.data

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.util.Log
import okhttp3.Dns
import okhttp3.OkHttpClient
import java.net.InetAddress
import java.net.Socket
import javax.net.SocketFactory

/**
 * Wear OS turns Wi-Fi off to save power unless an app asks for it, and then routes traffic
 * through the phone's Bluetooth proxy. For a session we ask for Wi-Fi (home network or a phone
 * hotspot) and keep it; when no Wi-Fi is available, requests fall back to the default network.
 */
class NetworkKeeper(context: Context) {
    private val cm = context.getSystemService(ConnectivityManager::class.java)
    @Volatile private var wifi: Network? = null

    private val callback = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) { wifi = network; Log.i(TAG, "wifi available") }
        override fun onLost(network: Network) { if (wifi == network) wifi = null; Log.i(TAG, "wifi lost") }
    }

    fun start() {
        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .build()
        runCatching { cm.requestNetwork(request, callback) }.onFailure { Log.w(TAG, "requestNetwork failed", it) }
    }

    fun stop() {
        runCatching { cm.unregisterNetworkCallback(callback) }
        wifi = null
    }

    /** OkHttp client that uses the held Wi-Fi network when there is one, else the default network. */
    fun client(): OkHttpClient = defaultClient().newBuilder()
        .socketFactory(object : SocketFactory() {
            private fun f(): SocketFactory = wifi?.socketFactory ?: getDefault()
            override fun createSocket(): Socket = f().createSocket()
            override fun createSocket(host: String?, port: Int) = f().createSocket(host, port)
            override fun createSocket(host: String?, port: Int, la: InetAddress?, lp: Int) = f().createSocket(host, port, la, lp)
            override fun createSocket(host: InetAddress?, port: Int) = f().createSocket(host, port)
            override fun createSocket(a: InetAddress?, port: Int, la: InetAddress?, lp: Int) = f().createSocket(a, port, la, lp)
        })
        .dns(object : Dns {
            override fun lookup(hostname: String): List<InetAddress> =
                wifi?.getAllByName(hostname)?.toList() ?: Dns.SYSTEM.lookup(hostname)
        })
        .build()

    private companion object { const val TAG = "WristHeat.net" }
}
