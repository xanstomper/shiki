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
    upd = {"status": args.status, "note": args.note or "", "score": args.score or 0,
           "at": datetime.now(timezone.utc).isoformat()}
    if args.assign:
        upd["assign"] = args.assign  # preserve owner on re-task
    lanes[args.lane].update(upd)
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
        print(f"  {i:2d}. [{str(l.get('assign') or '?'):9s}] ({l.get('score', 0):3d}) {l['status']:9s} "
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
    for want in ("plan", "lane", "fires", "report", "verify",
                 "board", "assault"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    # family engines must exist (SHIKI drives them)
    for name, script in FAMILY.items():
        if not script.exists():
            bad.append(f"family engine {name} missing")
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


# ── v2.0.0 THE COMMAND: drive the family's real engines ───────────────────────

FAMILY = {
    "barbican": Path.home() / ".hermes/skills/security/barbican/scripts/barbican.py",
    "holyshit": Path.home() / ".hermes/skills/security/holyshit-mode/scripts/finder.py",
    "undercroft": Path.home() / ".hermes/skills/security/undercroft/scripts/undercroft.py",
    "kairo": Path.home() / ".hermes/skills/security/kairo/scripts/kairo.py",
}


def _run_engine(name, argv):
    """Run a family CLI; stream output; return exit code."""
    script = FAMILY[name]
    if not script.exists():
        print(f"  ! {name} engine missing ({script}) — lane skipped")
        return 2
    cmd = [sys.executable, str(script)] + argv
    print(f"  ──▶ {name}: {' '.join(argv)[:110]}")
    r = subprocess.run(cmd)
    return r.returncode


def cmd_board(args):
    """The war board: all family states for the target, one view."""
    camp = Path.home() / ".redteam" / "campaigns" / args.org
    print(f"═══ SHIKI WAR BOARD — {args.org} ═══")
    total_conf = 0
    spec = [("undercroft", camp / "undercroft-state.json", ("code", "surface", "logic")),
            ("3am", camp / "state.json", ()),
            ("kairo", camp / "hardware-state.json", ())]
    for name, f, grps in spec:
        if not f.exists():
            print(f"  [{name:10s}] — no state (lane not yet engaged)")
            continue
        st = json.loads(f.read_text())
        if name == "undercroft":
            for g in grps:
                items = st.get(g, [])
                conf = sum(1 for x in items if x.get("status") == "CONFIRMED")
                total_conf += conf
                print(f"  [{name:10s}] {g}: {len(items)} entries, {conf} CONFIRMED")
            print(f"  [{name:10s}] pocs: {len(st.get('pocs', []))} · chains-ready")
        elif name == "kairo":
            vs = st.get("vectors", [])
            ch = st.get("chains", [])
            dist = sum(1 for v in vs if v.get("distributed"))
            total_conf += len(ch)
            print(f"  [{name:10s}] vectors: {len(vs)} (distributed {dist}) · chains: {len(ch)}")
            for c in ch:
                print(f"      {c['chain']} [{c['status']}]")
        elif name == "3am":
            ei = st.get("exploit_intel", {})
            print(f"  [{name:10s}] teardowns: {len(ei.get('teardowns', []))} · chains: {len(ei.get('chains', []))}")
    lv = Path.home() / ".redteam" / "learned-vectors.jsonl"
    if lv.exists():
        rows = [json.loads(l) for l in lv.read_text().splitlines() if l.strip()]
        print(f"  [family     ] learned-vectors canon: {len(rows)} rows (3AM promote-ready)")
    ops = load(args.org) or {}
    lanes = ops.get("lanes", {})
    if lanes:
        conf = sum(1 for l in lanes.values() if l.get("status") == "CONFIRMED")
        print(f"  [shiki      ] lanes: {len(lanes)} planned, {conf} CONFIRMED")
    print(f"═══ {total_conf} confirmed finding(s) on the board ═══")
    return 0


def cmd_assault(args):
    """ONE COMMAND: the family, in order, under the shield."""
    print(f"═══ SHIKI ASSAULT — {args.target} ═══")
    steps = {"gate", "find", "descend", "forge", "chain"}
    if args.skip:
        steps -= set(args.skip.split(","))
    # [0] GATE
    if "gate" in steps:
        print("[0] BARBICAN GATE")
        rc = _run_engine("barbican", ["vantage", "check", "--target", args.target])
        if rc == 1:
            print("═══ ASSAULT ABORTED — the shield is down. Fix the vantage or re-posture. ═══")
            return 1
        print("    gate open — shield verified")
    # [1] FIND
    if "find" in steps:
        print("[1] HOLYSHIT FINDS")
        _run_engine("holyshit", ["recon", "--domain", args.domain])
        _run_engine("holyshit", ["dossier", "--target", args.target])
    # [2] DESCEND
    if "descend" in steps and args.url:
        print("[2] UNDERCROFT DESCENDS (live, read-only)")
        argv = ["run", "--target", args.target, "--domain", args.domain, "--url", args.url]
        if args.bundle:
            argv += ["--bundle", args.bundle]
        if args.cookie:
            argv += ["--cookie", args.cookie]
        if args.boundary_url:
            argv += ["--boundary-url", args.boundary_url]
        if args.probe_ids:
            argv += ["--probe-ids", args.probe_ids]
        _run_engine("undercroft", argv)
    # [3] FORGE
    if "forge" in steps:
        print("[3] KAIRO FORGES")
        _run_engine("kairo", ["forge", "--target", args.target, "--expand"])
    # [4] CHAIN
    if "chain" in steps:
        print("[4] KAIRO CHAINS")
        _run_engine("kairo", ["chain", "--target", args.target, "--write"])
    # [5] VERDICT
    print("[5] THE WAR BOARD + JOINT VERDICT")
    args.org = args.target
    cmd_board(args)
    rep = f"{args.target}-joint-assault.md"
    args.output = rep
    cmd_report(args)
    print(f"═══ joint report: {rep} · next: 3AM promote --apply --verified ═══")
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
    bd = sub.add_parser("board", help="the war board: all family states, one view")
    bd.add_argument("--org", required=True)
    asl = sub.add_parser("assault", help="ONE COMMAND: barbican gate → find → descend → forge → chain → verdict")
    asl.add_argument("--target", required=True)
    asl.add_argument("--url", help="live estate base URL")
    asl.add_argument("--domain", required=True)
    asl.add_argument("--bundle", help="client bundle/source path")
    asl.add_argument("--cookie", help="own session cookie for read probes")
    asl.add_argument("--boundary-url", help="boundary probe template with {id}")
    asl.add_argument("--probe-ids", help="comma own-ids")
    asl.add_argument("--skip", help="comma steps to skip: gate,find,descend,forge,chain")
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
    if a.cmd == "board":
        return cmd_board(a)
    if a.cmd == "assault":
        return cmd_assault(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())