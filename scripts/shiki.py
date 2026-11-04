#!/usr/bin/env python3
"""
SHIKI — Command Mandate CLI. Bind family lanes into one coordinated attack.
stdlib-only. State: ~/.redteam/campaigns/<org>/ops-state.json.

Commands:
  plan    --org <o> --estate "<target>" --lanes "web,api,servers,cloud,identity,devices,mail,data"
  lane    --org <o> --lane <name> --assign 3am|holyShit|kairo|shiki
          --status QUEUED|ACTIVE|CONFIRMED|EXHAUSTED|N/A [--note "..."] [--score N]
  fires   --org <o>                     joint fire-list, score-ordered
  report  --org <o> [--output F]        joint operations verdict
  verify  self-check

Exit codes: 0 ok · 2 usage/state error.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LANE_OWNERS = ("3am", "holyShit", "kairo", "shiki")
LANE_STATUS = ("QUEUED", "ACTIVE", "CONFIRMED", "EXHAUSTED", "N/A")


def state_path(org):
    return Path.home() / ".redteam" / "campaigns" / org / "ops-state.json"


def load(org):
    p = state_path(org)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def save(org, st):
    p = state_path(org)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=2) + "\n")


def base(org, estate="", lanes=""):
    st = load(org)
    if st is None:
        st = {"org": org, "estate": estate, "lanes": {},
              "created": datetime.now(timezone.utc).isoformat()}
        save(org, st)
    return st


def cmd_plan(args):
    st = base(args.org, args.estate)
    st["estate"] = args.estate
    lanes = st.setdefault("lanes", {})
    added = 0
    for name in (args.lanes or "").split(","):
        name = name.strip()
        if not name:
            continue
        if name in lanes:
            continue
        lanes[name] = {"assign": "3am", "status": "QUEUED", "score": 0, "note": "",
                       "at": datetime.now(timezone.utc).isoformat()}
        added += 1
    save(args.org, st)
    print(f"▸ battle plan: {args.estate} — {len(lanes)} lanes ({added} new) → "
          f"{state_path(args.org)}")
    return 0


def cmd_lane(args):
    st = base(args.org)
    lanes = st.setdefault("lanes", {})
    if args.lane not in lanes:
        print(f"✗ lane '{args.lane}' not in plan — plan first", file=sys.stderr)
        return 2
    if args.assign is not None and args.assign not in LANE_OWNERS:
        print(f"✗ assign {LANE_OWNERS}", file=sys.stderr)
        return 2
    if args.status not in LANE_STATUS:
        print(f"✗ status {LANE_STATUS}", file=sys.stderr)
        return 2
    if args.assign:
        lanes[args.lane]["assign"] = args.assign  # preserve owner on re-task
    if lanes[args.lane]["status"] == "EXHAUSTED" and args.status != "EXHAUSTED":
        print("· lane EXHAUSTED — re-open only after a target change (canon)")
        return 0
    lanes[args.lane].update({"assign": args.assign, "status": args.status,
                             "note": args.note or "", "score": args.score or 0,
                             "at": datetime.now(timezone.utc).isoformat()})
    save(args.org, st)
    print(f"▸ lane {args.lane} [{args.assign}] {args.status}" + (f" — {args.note[:80]}" if args.note else ""))
    return 0


def cmd_fires(args):
    st = base(args.org)
    lanes = st.get("lanes", {})
    active = [l for l in lanes.values() if l["status"] in ("ACTIVE", "CONFIRMED")]
    active.sort(key=lambda l: -(l.get("score", 0) or 0))
    print(f"▸ JOINT FIRE-LIST — {len(active)} active lanes")
    for i, l in enumerate(active, 1):
        print(f"  {i:2d}. [{l['assign']:9s}] ({l.get('score', 0):3d}) {l['status']:9s} "
              f"{l.get('note', '')[:70]}")
    if not active:
        print("  (no active lanes — plan + dispatch first)")
    return 0


def cmd_report(args):
    st = base(args.org)
    out = args.output or f"{args.org}-shiki-report.md"
    lanes = st.get("lanes", {})
    L = [f"# SHIKI Joint Operations Report — {args.org}", "",
         f"Estate: {st.get('estate', '?')}", ""]
    L.append("## Lanes")
    for name in sorted(lanes):
        l = lanes[name]
        L.append(f"- **{name}** [{l['assign']}] {l['status']} ({(l.get('score') or 0)})"
                 + (f" — {l['note']}" if l.get("note") else ""))
    if not lanes:
        L.append("- (no lanes — plan first)")
    cnt = sum(1 for l in lanes.values() if l["status"] == "CONFIRMED")
    exh = sum(1 for l in lanes.values() if l["status"] == "EXHAUSTED")
    L += ["", f"## Verdict", f"- CONFIRMED lanes: {cnt} · EXHAUSTED: {exh} · "
          f"coverage: {len(lanes)} lanes planned"]
    if cnt:
        L.append("- SWEEP IMPACT: at least one lane holds control — escalate per "
                 "family takeover doctrine, then certify chains.")
    else:
        L.append("- no lane has confirmed control — named gaps per lane; "
                 "negatives are results (never padded).")
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ joint report written: {out}")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("plan", "lane", "fires", "report", "verify"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    tmpl = Path(__file__).resolve().parent.parent / "templates" / "ops-state.json"
    if tmpl.exists():
        try:
            json.loads(tmpl.read_text())
        except Exception:
            bad.append("template json")
    if bad:
        print(f"✗ SHIKI verify FAILED: {bad}")
        return 1
    print("✓ SHIKI verify: compile · subcommands · template — ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SHIKI — Command Mandate CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="create the battle plan")
    p.add_argument("--org", required=True)
    p.add_argument("--estate", required=True)
    p.add_argument("--lanes", required=True, help="comma lanes")
    l = sub.add_parser("lane", help="dispatch/update a lane")
    l.add_argument("--org", required=True)
    l.add_argument("--lane", required=True)
    l.add_argument("--assign", choices=LANE_OWNERS, help="defaults to current owner")
    l.add_argument("--status", required=True, choices=LANE_STATUS)
    l.add_argument("--note")
    l.add_argument("--score", type=int)
    f = sub.add_parser("fires", help="joint fire-list")
    f.add_argument("--org", required=True)
    r = sub.add_parser("report", help="joint operations verdict")
    r.add_argument("--org", required=True)
    r.add_argument("--output")
    v = sub.add_parser("verify", help="self-check")
    v.add_argument("--org")
    a = ap.parse_args()
    if a.cmd == "plan":
        return cmd_plan(a)
    if a.cmd == "lane":
        return cmd_lane(a)
    if a.cmd == "fires":
        return cmd_fires(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "verify":
        return cmd_verify(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())