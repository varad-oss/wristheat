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
    ap.add_argument("--wearer-username", help="Cognito username for the solo wearer T1 (e.g. varad)")
    ap.add_argument("--wearer-email")
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
        create_user(out, "supervisor", args.supervisor_email, "supervisors")
    if args.wearer_username:
        create_user(out, args.wearer_username, args.wearer_email or args.supervisor_email, "wearers")
        upsert(trainees, {"trainee_id": "T1"}, {"owner_username": args.wearer_username})
        upsert(trainees, {"trainee_id": "R1"}, {"owner_username": args.wearer_username})
        print(f"Linked T1 and R1 to wearer login '{args.wearer_username}'")


def create_user(out: dict, username: str, email: str | None, group: str):
    """Creates the Cognito user (temporary password printed once) and adds it to its group."""
    idp = boto3.client("cognito-idp", region_name=REGION)
    alphabet = string.ascii_letters + string.digits
    temp = "Wh-" + "".join(secrets.choice(alphabet) for _ in range(10)) + "9a!"
    attrs = [{"Name": "email", "Value": email}, {"Name": "email_verified", "Value": "true"}] if email else []
    try:
        idp.admin_create_user(UserPoolId=out["UserPoolId"], Username=username, TemporaryPassword=temp,
                              MessageAction="SUPPRESS", UserAttributes=attrs)
        print(f"User '{username}' created. Temporary password (shown once): {temp}")
    except idp.exceptions.UsernameExistsException:
        print(f"User '{username}' already exists; password unchanged.")
    except idp.exceptions.AliasExistsException:
        idp.admin_create_user(UserPoolId=out["UserPoolId"], Username=username, TemporaryPassword=temp,
                              MessageAction="SUPPRESS")
        print(f"User '{username}' created without email (address already used). Temporary password (shown once): {temp}")
    idp.admin_add_user_to_group(UserPoolId=out["UserPoolId"], Username=username, GroupName=group)
    print(f"'{username}' is in group '{group}'")


if __name__ == "__main__":
    main()
