#!/usr/bin/env python3
"""
check_configs.py - sanity-check the router configs in this repository.

What it checks
  1. Every router has a unique OSPFv3 router ID.
  2. Every IPv6 address is valid and sits inside one of the two ISP prefixes.
  3. Point-to-point links: both ends of each /52 are configured on two
     different routers (shows which routers peer over OSPFv3).
  4. LAN segments: /52s that appear on only one router (gateways for hosts).
  5. Every configured subnet exists in addressing/ipv6-addressing-plan.csv.

Usage
  python3 scripts/check_configs.py            # from the repository root
No third-party packages needed (Python 3.8+ standard library only).
"""
import csv
import ipaddress
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "configs" / "routers"
PLAN_CSV = ROOT / "addressing" / "ipv6-addressing-plan.csv"
ISP_PREFIXES = {
    "ISP 1": ipaddress.IPv6Network("20AD:1000:1000::/48"),
    "ISP 2": ipaddress.IPv6Network("30AD:1000:1000::/48"),
}


def parse_config(path):
    """Return (router_id, [(interface, IPv6Interface), ...]) for one config."""
    router_id, current_if, addresses = None, None, []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if line.startswith("!"):
            continue  # comments, including notes added during transcription
        m = re.match(r"interface (\S+)", line)
        if m:
            current_if = m.group(1)
            continue
        m = re.match(r"ipv6 address (\S+)", line)
        if m:
            addresses.append((current_if or "?", ipaddress.IPv6Interface(m.group(1))))
            continue
        m = re.match(r"router-id (\S+)", line)
        if m:
            router_id = m.group(1)
    return router_id, addresses


def main():
    problems = 0
    routers = {}
    for cfg in sorted(CONFIG_DIR.glob("*.cfg")):
        routers[cfg.stem] = parse_config(cfg)

    # 1. unique router IDs
    print("== Router IDs")
    seen = defaultdict(list)
    for name, (rid, _) in routers.items():
        seen[rid].append(name)
        print(f"  {name:<22} {rid}")
    for rid, names in seen.items():
        if rid is None or len(names) > 1:
            problems += 1
            print(f"  !! duplicate or missing router ID {rid}: {', '.join(names)}")

    # 2. addresses inside the ISP prefixes
    subnet_owners = defaultdict(list)
    for name, (_, addrs) in routers.items():
        for intf, addr in addrs:
            isp = next((k for k, p in ISP_PREFIXES.items() if addr.ip in p), None)
            if isp is None:
                problems += 1
                print(f"  !! {name} {intf} {addr} is outside both ISP prefixes")
            subnet_owners[addr.network].append(f"{name}:{intf}({addr.ip})")

    # 3 & 4. links vs LAN segments
    print("\n== Point-to-point links (same /52 on two routers -> OSPFv3 neighbours)")
    for net in sorted(subnet_owners):
        if len(subnet_owners[net]) >= 2:
            print(f"  {str(net):<26} " + "  <->  ".join(subnet_owners[net]))
    print("\n== LAN / VLAN gateways (only one router on the /52)")
    for net in sorted(subnet_owners):
        if len(subnet_owners[net]) == 1:
            print(f"  {str(net):<26} {subnet_owners[net][0]}")

    # 5. compare with the addressing plan
    planned = set()
    with PLAN_CSV.open() as f:
        for row in csv.DictReader(f):
            planned.add(ipaddress.IPv6Network(row["isp1_prefix"]))
            planned.add(ipaddress.IPv6Network(row["isp2_prefix"]))
    missing = [n for n in subnet_owners if n not in planned]
    print("\n== Addressing plan check")
    if missing:
        problems += len(missing)
        for n in missing:
            print(f"  !! {n} is configured but not in the addressing plan")
    else:
        print(f"  All {len(subnet_owners)} configured subnets are in the addressing plan.")

    print(f"\nRouters checked: {len(routers)}   Problems found: {problems}")
    print("Note: Manchester and London DMZ configs are partial (see configs/README.md).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
