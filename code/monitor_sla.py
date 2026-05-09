#!/usr/bin/env python3
# =============================================================
# monitor_sla.py - SLA Supervision Script
# Project: Cloud & Edge Computing
# Author:  LAHLAIBI Ayoub
# =============================================================

import openstack
import json
import datetime

CONFIG = {
    "auth_url":            "http://192.168.56.102/identity/v3",
    "username":            "admin",
    "password":            "admin",
    "project_name":        "admin",
    "user_domain_name":    "Default",
    "project_domain_name": "Default",
}

SLA_TARGET = 99.5


def connect_openstack():
    return openstack.connect(
        auth_url=CONFIG["auth_url"],
        username=CONFIG["username"],
        password=CONFIG["password"],
        project_name=CONFIG["project_name"],
        user_domain_name=CONFIG["user_domain_name"],
        project_domain_name=CONFIG["project_domain_name"],
    )


def monitor_instances(conn):
    instances = []
    for server in conn.compute.servers():
        available = server.status == "ACTIVE"
        instances.append({
            "name":      server.name,
            "status":    server.status,
            "available": available,
            "timestamp": datetime.datetime.now().isoformat(),
        })
        state = "OK" if available else "DOWN"
        print(f"  {server.name:30} | {server.status:10} | {state}")
    return instances


def calculate_availability(instances):
    if not instances:
        return 0.0, 0, 0
    total  = len(instances)
    active = sum(1 for i in instances if i["available"])
    rate   = round((active / total) * 100, 2)
    return rate, active, total


def generate_report(instances, rate, active, total):
    compliant = rate >= SLA_TARGET
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "sla": {
            "target":    SLA_TARGET,
            "measured":  rate,
            "compliant": compliant,
            "status":    "CONFORME" if compliant else "NON CONFORME",
        },
        "instances": {
            "total":  total,
            "active": active,
            "detail": instances,
        },
    }
    with open("rapport_sla.json", "w") as f:
        json.dump(report, f, indent=2)
    return report, compliant


def main():
    print("=" * 55)
    print("  SLA Supervision - OpenStack")
    print(f"  Target: {SLA_TARGET}%")
    print("=" * 55)
    conn = connect_openstack()
    instances = monitor_instances(conn)
    rate, active, total = calculate_availability(instances)
    report, ok = generate_report(instances, rate, active, total)
    print()
    print(f"  Availability : {rate}%")
    print(f"  SLA Target   : {SLA_TARGET}%")
    print(f"  Status       : {'CONFORME' if ok else 'NON CONFORME'}")
    print(f"  Report saved : rapport_sla.json")
    print("=" * 55)


if __name__ == "__main__":
    main()
