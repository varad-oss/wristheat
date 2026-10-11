"""Data access: DynamoRepo (boto3) and FakeRepo (in-memory) with the same interface (spec §6)."""
from __future__ import annotations

import copy
from decimal import Decimal
from typing import Protocol

from wristheat.engine import MinuteRow

DAY_S = 86_400
TTL_DAYS = {"sessions": 30, "readings": 30, "minutes": 30, "incidents": 90}
OPEN_STATUSES = ("NOTIFIED", "ESCALATED", "ACKNOWLEDGED")


class VersionConflict(Exception):
    """A conditional write lost a race; reload and retry."""


class ConditionFailed(Exception):
    """A conditional incident update did not match."""


def ttl_for(kind: str, now_ms: int) -> int:
    return now_ms // 1000 + TTL_DAYS[kind] * DAY_S


def to_dynamo(obj):
    if isinstance(obj, float):
        return Decimal(repr(obj))
    if isinstance(obj, dict):
        return {k: to_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_dynamo(v) for v in obj]
    return obj


def from_dynamo(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() and "." not in str(obj) and "E" not in str(obj) else float(obj)
    if isinstance(obj, dict):
        return {k: from_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [from_dynamo(v) for v in obj]
    return obj


def minute_item(sid: str, row: MinuteRow, now_ms: int) -> dict:
    return {"session_id": sid, "minute": row.minute, "hr": row.hr, "n": row.n, "core_est_c": row.core_est_c,
            "core_var": row.core_var, "psi": row.psi, "level": row.level, "state": row.state,
            "wbgt_c": row.wbgt_c, "flag": row.flag, "pm25": row.pm25, "ttl": ttl_for("minutes", now_ms)}


class Repo(Protocol):
    def get_trainee(self, tid: str) -> dict | None: ...
    def list_trainees(self) -> list[dict]: ...
    def put_trainee(self, item: dict) -> None: ...
    def get_session(self, sid: str) -> dict | None: ...
    def create_session(self, item: dict) -> None: ...
    def save_session(self, item: dict, expected_version: int) -> None: ...
    def end_session(self, sid: str, now_ms: int) -> None: ...
    def set_current_session(self, tid: str, sid: str) -> None: ...
    def put_readings(self, sid: str, samples: list[tuple[int, int]], now_ms: int) -> None: ...
    def put_minutes(self, sid: str, rows: list[MinuteRow], now_ms: int) -> None: ...
    def get_minutes(self, sid: str, since_minute: int | None = None) -> list[dict]: ...
    def get_readings(self, sid: str) -> list[tuple[int, int]]: ...
    def get_site(self, site_id: str) -> dict | None: ...
    def put_site(self, item: dict) -> None: ...
    def put_incident(self, item: dict) -> None: ...
    def get_incident(self, iid: str) -> dict | None: ...
    def list_incidents(self) -> list[dict]: ...
    def update_incident(self, iid: str, *, status_in: tuple[str, ...] | None = None, **fields) -> None: ...
    def append_incident_event(self, iid: str, event: dict) -> None: ...


class FakeRepo:
    def __init__(self):
        self.sites, self.trainees, self.sessions, self.incidents = {}, {}, {}, {}
        self.readings: dict[str, dict[int, int]] = {}
        self.minutes: dict[str, dict[int, dict]] = {}
        self.fail_next_save_with_conflict = 0

    def get_trainee(self, tid):
        return copy.deepcopy(self.trainees.get(tid))

    def list_trainees(self):
        return copy.deepcopy(list(self.trainees.values()))

    def put_trainee(self, item):
        self.trainees[item["trainee_id"]] = copy.deepcopy(item)

    def get_session(self, sid):
        return copy.deepcopy(self.sessions.get(sid))

    def create_session(self, item):
        if item["session_id"] in self.sessions:
            raise VersionConflict(item["session_id"])
        self.sessions[item["session_id"]] = copy.deepcopy(item)

    def save_session(self, item, expected_version):
        if self.fail_next_save_with_conflict > 0:
            self.fail_next_save_with_conflict -= 1
            raise VersionConflict(item["session_id"])
        cur = self.sessions.get(item["session_id"])
        if cur is None or cur.get("version") != expected_version:
            raise VersionConflict(item["session_id"])
        self.sessions[item["session_id"]] = copy.deepcopy({**item, "version": expected_version + 1})

    def end_session(self, sid, now_ms):
        self.sessions[sid].update(status="ENDED", ended_at=now_ms)

    def set_current_session(self, tid, sid):
        self.trainees[tid]["current_session_id"] = sid

    def put_readings(self, sid, samples, now_ms):
        self.readings.setdefault(sid, {}).update(dict(samples))

    def put_minutes(self, sid, rows, now_ms):
        for r in rows:
            self.minutes.setdefault(sid, {})[r.minute] = minute_item(sid, r, now_ms)

    def get_minutes(self, sid, since_minute=None):
        rows = sorted(self.minutes.get(sid, {}).values(), key=lambda r: r["minute"])
        return [copy.deepcopy(r) for r in rows if since_minute is None or r["minute"] >= since_minute]

    def get_readings(self, sid):
        return sorted(self.readings.get(sid, {}).items())

    def get_site(self, site_id):
        return copy.deepcopy(self.sites.get(site_id))

    def put_site(self, item):
        self.sites[item["site_id"]] = copy.deepcopy(item)

    def put_incident(self, item):
        self.incidents[item["incident_id"]] = copy.deepcopy(item)

    def get_incident(self, iid):
        return copy.deepcopy(self.incidents.get(iid))

    def list_incidents(self):
        return copy.deepcopy(list(self.incidents.values()))

    def update_incident(self, iid, *, status_in=None, **fields):
        inc = self.incidents.get(iid)
        if inc is None or (status_in is not None and inc.get("status") not in status_in):
            raise ConditionFailed(iid)
        inc.update(copy.deepcopy(fields))

    def append_incident_event(self, iid, event):
        self.incidents[iid].setdefault("events", []).append(copy.deepcopy(event))


class DynamoRepo:
    def __init__(self, table_names: dict[str, str], resource=None):
        import boto3
        self._ddb = resource or boto3.resource("dynamodb")
        self.t = {k: self._ddb.Table(v) for k, v in table_names.items() if v}

    @staticmethod
    def _conditional(exc) -> bool:
        return getattr(exc, "response", {}).get("Error", {}).get("Code") == "ConditionalCheckFailedException"

    def _get(self, table, key):
        item = self.t[table].get_item(Key=key, ConsistentRead=True).get("Item")
        return from_dynamo(item) if item else None

    def _scan(self, table):
        items, kwargs = [], {}
        while True:
            page = self.t[table].scan(**kwargs)
            items += page.get("Items", [])
            if "LastEvaluatedKey" not in page:
                return [from_dynamo(i) for i in items]
            kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]

    def get_trainee(self, tid):
        return self._get("trainees", {"trainee_id": tid})

    def list_trainees(self):
        return self._scan("trainees")

    def put_trainee(self, item):
        self.t["trainees"].put_item(Item=to_dynamo(item))

    def get_session(self, sid):
        return self._get("sessions", {"session_id": sid})

    def create_session(self, item):
        try:
            self.t["sessions"].put_item(Item=to_dynamo(item), ConditionExpression="attribute_not_exists(session_id)")
        except Exception as e:  # noqa: BLE001
            if self._conditional(e):
                raise VersionConflict(item["session_id"]) from e
            raise

    def save_session(self, item, expected_version):
        try:
            self.t["sessions"].put_item(Item=to_dynamo({**item, "version": expected_version + 1}),
                                        ConditionExpression="version = :v",
                                        ExpressionAttributeValues={":v": expected_version})
        except Exception as e:  # noqa: BLE001
            if self._conditional(e):
                raise VersionConflict(item["session_id"]) from e
            raise

    def end_session(self, sid, now_ms):
        self.t["sessions"].update_item(Key={"session_id": sid}, UpdateExpression="SET #s = :e, ended_at = :n",
                                       ExpressionAttributeNames={"#s": "status"},
                                       ExpressionAttributeValues={":e": "ENDED", ":n": now_ms})

    def set_current_session(self, tid, sid):
        self.t["trainees"].update_item(Key={"trainee_id": tid}, UpdateExpression="SET current_session_id = :s",
                                       ExpressionAttributeValues={":s": sid})

    def put_readings(self, sid, samples, now_ms):
        ttl = ttl_for("readings", now_ms)
        with self.t["readings"].batch_writer(overwrite_by_pkeys=["session_id", "t"]) as w:
            for t, bpm in samples:
                w.put_item(Item={"session_id": sid, "t": t, "bpm": bpm, "ttl": ttl})

    def put_minutes(self, sid, rows, now_ms):
        with self.t["minutes"].batch_writer(overwrite_by_pkeys=["session_id", "minute"]) as w:
            for r in rows:
                w.put_item(Item=to_dynamo(minute_item(sid, r, now_ms)))

    def _query(self, table, key_cond):
        items, kwargs = [], {"KeyConditionExpression": key_cond}
        while True:
            page = self.t[table].query(**kwargs)
            items += page.get("Items", [])
            if "LastEvaluatedKey" not in page:
                return [from_dynamo(i) for i in items]
            kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]

    def get_minutes(self, sid, since_minute=None):
        from boto3.dynamodb.conditions import Key
        cond = Key("session_id").eq(sid)
        if since_minute is not None:
            cond = cond & Key("minute").gte(since_minute)
        return self._query("minutes", cond)

    def get_readings(self, sid):
        from boto3.dynamodb.conditions import Key
        return [(r["t"], r["bpm"]) for r in self._query("readings", Key("session_id").eq(sid))]

    def get_site(self, site_id):
        return self._get("sites", {"site_id": site_id})

    def put_site(self, item):
        self.t["sites"].put_item(Item=to_dynamo(item))

    def put_incident(self, item):
        self.t["incidents"].put_item(Item=to_dynamo(item))

    def get_incident(self, iid):
        return self._get("incidents", {"incident_id": iid})

    def list_incidents(self):
        return self._scan("incidents")

    def update_incident(self, iid, *, status_in=None, **fields):
        names = {f"#f{i}": k for i, k in enumerate(fields)}
        values = {f":v{i}": to_dynamo(v) for i, v in enumerate(fields.values())}
        expr = "SET " + ", ".join(f"#f{i} = :v{i}" for i in range(len(fields)))
        kwargs = {"Key": {"incident_id": iid}, "UpdateExpression": expr,
                  "ExpressionAttributeNames": names, "ExpressionAttributeValues": values,
                  "ConditionExpression": "attribute_exists(incident_id)"}
        if status_in is not None:
            names["#st"] = "status"
            opts = {f":s{i}": s for i, s in enumerate(status_in)}
            values.update(opts)
            kwargs["ConditionExpression"] += f" AND #st IN ({', '.join(opts)})"
        try:
            self.t["incidents"].update_item(**kwargs)
        except Exception as e:  # noqa: BLE001
            if self._conditional(e):
                raise ConditionFailed(iid) from e
            raise

    def append_incident_event(self, iid, event):
        self.t["incidents"].update_item(
            Key={"incident_id": iid},
            UpdateExpression="SET events = list_append(if_not_exists(events, :empty), :e)",
            ExpressionAttributeValues={":e": [to_dynamo(event)], ":empty": []})
