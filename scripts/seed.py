#!/usr/bin/env python3
"""Upserts the site and trainees (spec §6, plan Task 7). Optionally creates the supervisor user (Task 9).

    python scripts/seed.py --name "Varad" --age 21 [--supervisor-email you@example.com]
"""
import argparse
import secrets
import string

import boto3

from common import REGION, outputs

SITE = {"site_id": "kgp", "name": "IIT Kharagpur campus", "lat": "22.3149", "lon": "87.3105"}
SIMULATED = [("S1", "Arjun", 22, 72), ("S2", "Meera", 24, 68), ("S3", "Kabir", 21, 76), ("S4", "Ishaan", 23, 70)]


def upsert(table, key: dict, fields: dict):
    names = {f"#f{i}": k for i, k in enumerate(fields)}
    values = {f":v{i}": v for i, v in enumerate(fields.values())}
    table.update_item(Key=key, UpdateExpression="SET " + ", ".join(f"#f{i} = :v{i}" for i in range(len(fields))),
                      ExpressionAttributeNames=names, ExpressionAttributeValues=values)


def main():
    from decimal import Decimal
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--age", type=int, required=True)
    ap.add_argument("--supervisor-email")
    ap.add_argument("--outputs")
    args = ap.parse_args()
    out = outputs(args.outputs)
    ddb = boto3.resource("dynamodb", region_name=REGION)
    sites, trainees = ddb.Table(out["TableSites"]), ddb.Table(out["TableTrainees"])

    upsert(sites, {"site_id": SITE["site_id"]},
           {"name": SITE["name"], "lat": Decimal(SITE["lat"]), "lon": Decimal(SITE["lon"])})
    rows = [("T1", args.name, "real", args.age, None, False),
            ("R1", f"{args.name} — earlier run", "real", args.age, None, False)]
    rows += [(tid, name, "simulated", age, rest, False) for tid, name, age, rest in SIMULATED]
    rows.append(("S0", "Smoke test", "simulated", 30, 70, True))
    for tid, name, kind, age, rest, hidden in rows:
        fields = {"name": name, "kind": kind, "age": age, "site_id": SITE["site_id"], "hidden": hidden}
        if rest is not None:
            fields["rest_hr_override"] = rest
        fields["mode"] = "solo" if tid in ("T1", "R1") else "group"
        upsert(trainees, {"trainee_id": tid}, fields)
    print(f"Seeded site {SITE['site_id']} and trainees {', '.join(r[0] for r in rows)}")

    if args.supervisor_email:
        create_supervisor(out, args.supervisor_email)


def create_supervisor(out: dict, email: str):
    idp = boto3.client("cognito-idp", region_name=REGION)
    alphabet = string.ascii_letters + string.digits
    temp = "Wh-" + "".join(secrets.choice(alphabet) for _ in range(10)) + "9a!"
    try:
        idp.admin_create_user(UserPoolId=out["UserPoolId"], Username="supervisor", TemporaryPassword=temp,
                              MessageAction="SUPPRESS",
                              UserAttributes=[{"Name": "email", "Value": email},
                                              {"Name": "email_verified", "Value": "true"}])
        print(f"Supervisor user 'supervisor' ({email}) created. Temporary password (shown once): {temp}")
    except idp.exceptions.UsernameExistsException:
        print("Supervisor user already exists; leaving its password unchanged.")


if __name__ == "__main__":
    main()
