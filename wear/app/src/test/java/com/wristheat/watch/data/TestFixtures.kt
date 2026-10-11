package com.wristheat.watch.data

fun loadContract(name: String): String =
    requireNotNull(object {}.javaClass.classLoader!!.getResource("contracts/$name")) { "missing $name" }
        .readText(Charsets.UTF_8)

fun loadResponse(kind: String): IngestResponse =
    WhJson.decodeFromString(IngestResponse.serializer(), loadContract("ingest_response.$kind.json"))
