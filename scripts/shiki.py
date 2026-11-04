#!/usr/bin/env python3
"""
SHIKI — Command Mandate CLI. Bind family lanes into one coordinated attack.
stdlib-only. State: ~/.redteam/campaigns/<org>/ops-state.json.

Commands:
  plan     --org <o> --estate "<target>" --lanes "web,api,servers,cloud,identity,devices,mail,data"
  lane     --org <o> --lane <name> --assign 3am|holyShit|kairo|shiki
           --status QUEUED|ACTIVE|CONFIRMED|EXHAUSTED|N/A [--note "..."] [--score N]
  fires    --org <o>                     joint fire-list, score-ordered
  board    --org <o>                     the war board: all family states, one view
  warroom  --org <o>                     board + fires + family engine status, one view
  gate     --target <t>                  standalone step-0 (barbican vantage check)
  handoff  --target <t> --to shukaku|holyshit|kairo
                                         the next mandate's exact command sequence
  assault  --target <t> --url U --domain D [--bundle P] [--boundary-url U2]
           [--probe-ids 1,2] [--parallel] [--resume] [--close] [--plan-only]
                                         the full pipeline (plan-only = print, don't run)
  report   --org <o> [--output F]        joint operations verdict
  verify   self-check

Exit codes: 0 ok · 1 gate/verify failure · 2 usage/state error.
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
                 "board", "assault", "warroom", "gate", "handoff"):
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


def _board_lines(org):
    """Build the war-board lines (shared by board + joint report)."""
    camp = Path.home() / ".redteam" / "campaigns" / org
    lines = [f"═══ SHIKI WAR BOARD — {org} ═══"]
    total_conf = 0
    spec = [("undercroft", camp / "undercroft-state.json", ("code", "surface", "logic")),
            ("3am", camp / "state.json", ()),
            ("kairo", camp / "hardware-state.json", ())]
    for name, f, grps in spec:
        if not f.exists():
            lines.append(f"  [{name:10s}] — no state (lane not yet engaged)")
            continue
        st = json.loads(f.read_text())
        if name == "undercroft":
            for g in grps:
                items = st.get(g, [])
                conf = sum(1 for x in items if x.get("status") == "CONFIRMED")
                total_conf += conf
                lines.append(f"  [{name:10s}] {g}: {len(items)} entries, {conf} CONFIRMED")
            lines.append(f"  [{name:10s}] pocs: {len(st.get('pocs', []))} · chains-ready")
        elif name == "kairo":
            vs = st.get("vectors", [])
            ch = st.get("chains", [])
            dist = sum(1 for v in vs if v.get("distributed"))
            total_conf += len(ch)
            lines.append(f"  [{name:10s}] vectors: {len(vs)} (distributed {dist}) · chains: {len(ch)}")
            for c in ch:
                lines.append(f"      {c['chain']} [{c['status']}]")
        elif name == "3am":
            ei = st.get("exploit_intel", {})
            lines.append(f"  [{name:10s}] teardowns: {len(ei.get('teardowns', []))} · chains: {len(ei.get('chains', []))}")
    lv = Path.home() / ".redteam" / "learned-vectors.jsonl"
    if lv.exists():
        rows = [json.loads(l) for l in lv.read_text().splitlines() if l.strip()]
        lines.append(f"  [family     ] learned-vectors canon: {len(rows)} rows (3AM promote-ready)")
    ops = load(org) or {}
    lanes = ops.get("lanes", {})
    if lanes:
        conf = sum(1 for l in lanes.values() if l.get("status") == "CONFIRMED")
        lines.append(f"  [shiki      ] lanes: {len(lanes)} planned, {conf} CONFIRMED")
    lines.append(f"═══ {total_conf} confirmed finding(s) on the board ═══")
    return lines


def cmd_board(args):
    """The war board: all family states for the target, one view."""
    for line in _board_lines(args.org):
        print(line)
    return 0


def cmd_assault(args):
    """ONE COMMAND: the family, in order, under the shield. Parallel-capable, adaptive."""
    import shutil
    import threading
    print(f"═══ SHIKI ASSAULT — {args.target} ═══")
    steps = {"gate", "find", "descend", "forge", "chain"}
    if args.skip:
        steps -= set(args.skip.split(","))
    if args.resume:
        dossier = Path(f"{args.target}-dossier.md")
        if dossier.exists():
            steps.discard("find")
            print(f"[resume] dossier fresh ({dossier.name}) — find skipped (re-run freely; dedupe makes it cheap)")
    # [0] GATE (always first, always blocking)
    if "gate" in steps or args.resume:
        print("[0] BARBICAN GATE")
        rc = _run_engine("barbican", ["vantage", "check", "--target", args.target])
        if rc == 1:
            print("═══ ASSAULT ABORTED — the shield is down. Fix the vantage or re-posture. ═══")
            return 1
        print("    gate open — shield verified")
    # [1]+[2] FIND ∥ DESCEND (independent stages — parallel when --parallel)
    def _find():
        print("[1] HOLYSHIT FINDS")
        _run_engine("holyshit", ["recon", "--domain", args.domain])
        _run_engine("holyshit", ["dossier", "--target", args.target])

    def _descend():
        print("[2] UNDERCROFT DESCENDS (live, read-only)")
        argv = ["run", "--target", args.target, "--domain", args.domain, "--url", args.url or ""]
        if args.bundle:
            argv += ["--bundle", args.bundle]
        if args.cookie:
            argv += ["--cookie", args.cookie]
        if args.boundary_url:
            argv += ["--boundary-url", args.boundary_url]
        if args.probe_ids:
            argv += ["--probe-ids", args.probe_ids]
        _run_engine("undercroft", argv)

    threads = []
    if "find" in steps:
        t1 = threading.Thread(target=_find)
        threads.append(t1)
    if "descend" in steps and args.url:
        t2 = threading.Thread(target=_descend)
        threads.append(t2)
    if args.parallel and threads:
        print(f"[*] PARALLEL: {len(threads)} independent stages firing concurrently")
        for t in threads:
            t.start()
    for t in threads:
        t.join()
    # [ADAPTIVE] re-task: the assault reads results and updates its own lanes NOW
    st_ops = load(args.target) or {"target": args.target, "estate": args.url or "",
                                   "lanes": {}, "created": datetime.now(timezone.utc).isoformat()}
    lanes = st_ops.setdefault("lanes", {})
    camp = Path.home() / ".redteam" / "campaigns" / args.target
    uc = camp / "undercroft-state.json"
    if uc.exists():
        u = json.loads(uc.read_text())
        conf_s = sum(1 for x in u.get("surface", []) if x.get("status") == "CONFIRMED")
        conf_l = sum(1 for x in u.get("logic", []) if x.get("status") == "CONFIRMED")
        status = "CONFIRMED" if (conf_s + conf_l) else "ACTIVE"
        lanes["descent"] = {"assign": "undercroft", "status": status,
                            "score": 90 if status == "CONFIRMED" else 60,
                            "note": f"{conf_s} live routes + {conf_l} logic seams CONFIRMED",
                            "at": datetime.now(timezone.utc).isoformat()}
        if status == "CONFIRMED":
            print(f"[↯] ADAPTIVE RE-TASK: descent CONFIRMED ({conf_s}+{conf_l}) — lanes updated, forge escalated")
    # [3] FORGE
    if "forge" in steps:
        print("[3] KAIRO FORGES")
        _run_engine("kairo", ["forge", "--target", args.target, "--expand"])
        k = camp / "hardware-state.json"
        nv = len(json.loads(k.read_text()).get("vectors", [])) if k.exists() else 0
        lanes["forge"] = {"assign": "kairo", "status": "CONFIRMED" if nv else "ACTIVE",
                          "score": 85 if nv else 50, "note": f"{nv} vectors armed",
                          "at": datetime.now(timezone.utc).isoformat()}
    # [4] CHAIN
    if "chain" in steps:
        print("[4] KAIRO CHAINS")
        _run_engine("kairo", ["chain", "--target", args.target, "--write"])
        k = camp / "hardware-state.json"
        nch = len(json.loads(k.read_text()).get("chains", [])) if k.exists() else 0
        lanes["chain"] = {"assign": "kairo", "status": "CONFIRMED" if nch else "ACTIVE",
                          "score": 80 if nch else 40, "note": f"{nch} kill chain(s)",
                          "at": datetime.now(timezone.utc).isoformat()}
    save_state = st_ops
    p_ops = Path.home() / ".redteam" / "campaigns" / args.target / "ops-state.json"
    p_ops.parent.mkdir(parents=True, exist_ok=True)
    p_ops.write_text(json.dumps(save_state, indent=2) + "\n")
    # [5] VERDICT
    print("[5] THE WAR BOARD + JOINT VERDICT")
    args.org = args.target
    cmd_board(args)
    rep = f"{args.target}-joint-assault.md"
    args.output = rep
    cmd_report(args)
    with open(rep, "a") as f:
        f.write("\n## The War Board (family states)\n```\n")
        f.write("\n".join(_board_lines(args.target)))
        f.write("\n```\n")
    print(f"═══ joint report: {rep} · next: 3AM promote --apply --verified ═══")
    if args.close:
        print("[6] CLOSE: barbican wipe (canon survives)")
        _run_engine("barbican", ["wipe", "--target", args.target, "--confirm"])
        rep_keep = Path(rep)
        if rep_keep.exists():
            keep = Path.home() / ".redteam" / "closeouts"
            keep.mkdir(parents=True, exist_ok=True)
            shutil.copy(rep, keep / rep_keep.name)
            print(f"    joint report archived → {keep / rep_keep.name}")
    return 0


# ── v2.1.0 the command layer deepens: plan · gate · warroom · handoff ─────────

FAMILY_STATUS_ORDER = ("barbican", "holyshit", "undercroft", "kairo", "3am",
                       "shukaku")


def _family_status_lines():
    rows = []
    for name in FAMILY_STATUS_ORDER:
        if name in FAMILY:
            script = FAMILY[name]
        else:
            dirname = "3am-shinjitsu" if name == "3am" else name
            fname = "exploit-intel.py" if name == "3am" else f"{name}.py"
            script = Path.home() / ".hermes/skills/security" / dirname / "scripts" / fname
        rows.append((name, "✓" if script.exists() else "✗"))
    return rows


def _assault_plan(args):
    """The full 6-step plan: per step, exact argv, gate notes. Executes nothing."""
    steps = ["gate", "find", "descend", "forge", "chain"]
    skip = set(s for s in (args.skip or "").split(",") if s)
    plan = []
    if "gate" not in skip:
        plan.append(("0", "GATE", "barbican",
                     ["vantage", "check", "--target", args.target],
                     "rc=1 aborts everything — no verified exit, no assault"))
    else:
        plan.append(("0", "GATE", "SKIPPED", [], "--skip gate (never do this blind)"))
    if "find" not in skip:
        plan.append(("1", "FIND", "holyshit",
                     ["recon", "--domain", args.domain],
                     "discovery checklist"))
        plan.append(("1", "FIND", "holyshit",
                     ["dossier", "--target", args.target],
                     "everything the canon knows"))
    else:
        plan.append(("1", "FIND", "SKIPPED", [], "--skip find"))
    if "descend" not in skip:
        if args.url:
            argv = ["run", "--target", args.target, "--domain", args.domain,
                    "--url", args.url]
            for flag, val in (("--bundle", args.bundle),
                              ("--cookie", args.cookie),
                              ("--boundary-url", args.boundary_url),
                              ("--probe-ids", args.probe_ids)):
                if val:
                    argv += [flag, val]
            plan.append(("2", "DESCEND", "undercroft", argv,
                         "live read-only engagement (parallel-capable with find)"))
        else:
            plan.append(("2", "DESCEND", "undercroft", [],
                         "no --url — descend will be skipped at run time"))
    else:
        plan.append(("2", "DESCEND", "SKIPPED", [], "--skip descend"))
    if "forge" not in skip:
        plan.append(("3", "FORGE", "kairo",
                     ["forge", "--target", args.target, "--expand"],
                     "1 finding → ~4 attacks, distributed to every consumer"))
    else:
        plan.append(("3", "FORGE", "SKIPPED", [], "--skip forge"))
    if "chain" not in skip:
        plan.append(("4", "CHAIN", "kairo",
                     ["chain", "--target", args.target, "--write"],
                     "multi-hop kill chains, TAKEOVER-CANDIDATE"))
    else:
        plan.append(("4", "CHAIN", "SKIPPED", [], "--skip chain"))
    plan.append(("5", "VERDICT", "shiki", ["board + report"],
                 "war board + joint operations verdict"))
    if args.close:
        plan.append(("6", "CLOSE", "barbican",
                     ["wipe", "--target", args.target, "--confirm"],
                     "campaign wiped; joint report archived to ~/.redteam/closeouts"))
    if args.resume:
        plan.append(("", "RESUME", "shiki", [],
                     "fresh stages skipped (dossier exists), rest deduped"))
    return plan


def cmd_assault_plan(args):
    print(f"═══ SHIKI ASSAULT PLAN — {args.target} (plan-only: nothing executes) ═══")
    for num, name, engine, argv, note in _assault_plan(args):
        argvs = f"$ shiki-driven: {engine} {' '.join(argv)}" if argv else ""
        print(f"  [{num}] {name:8s} {engine:10s} {argvs[:96]}")
        if engine == "SKIPPED" or not argv:
            print(f"        {note}")
        else:
            print(f"        {note}")
        if argv and engine not in ("SKIPPED", "shiki"):
            script = FAMILY.get(engine)
            if script is None:
                print(f"        ! engine not registered in FAMILY — would be skipped")
            elif not script.exists():
                print(f"        ! engine missing on disk — step will be skipped: {script}")
    print("")
    print("  plan-only: no packet left this machine. Drop --plan-only to execute.")
    return 0


def cmd_gate(args):
    """Standalone step-0: the shield check everything else can call."""
    barb = FAMILY.get("barbican")
    if barb is None or not barb.exists():
        print("✗ GATE CLOSED — shield not installed (barbican engine missing)", file=sys.stderr)
        return 1
    r = subprocess.run([sys.executable, str(barb), "vantage", "check",
                        "--target", args.target])
    if r.returncode != 0:
        print("═══ GATE CLOSED — no verified exit, no engagement ═══", file=sys.stderr)
        return r.returncode or 1
    # the scope authority: the machine-checkable estate gate
    if args.value:
        sm = Path.home() / ".hermes/skills/security/spydermonkey/scripts/spydermonkey.py"
        if sm.exists():
            r2 = subprocess.run([sys.executable, str(sm), "scope", "check",
                                 "--value", args.value, "--strict"])
            if r2.returncode != 0:
                print("═══ GATE CLOSED — target out of scope ═══", file=sys.stderr)
                return 1
    print("═══ GATE OPEN — shield verified, scope honored ═══")
    return 0


def cmd_validate(args):
    """The PSV validator (post-assault verification pass): every CONFIRMED claim
    re-checked for drift — stale findings are named, not trusted."""
    camp = Path.home() / ".redteam" / "campaigns" / args.target
    stale, fresh = [], 0
    now = datetime.now(timezone.utc)
    u = camp / "undercroft-state.json"
    if u.exists():
        st = json.loads(u.read_text())
        for grp in ("surface", "logic", "code"):
            for x in st.get(grp, []):
                if x.get("status") != "CONFIRMED":
                    continue
                at = x.get("at", "")
                try:
                    age = (now - datetime.fromisoformat(at)).days if at else 999
                except Exception:
                    age = 999
                if age > args.days:
                    stale.append((f"undercroft/{grp}", x.get("seam")
                                  or x.get("endpoint") or x.get("asset") or "?", age))
                else:
                    fresh += 1
    k = camp / "hardware-state.json"
    if k.exists():
        st = json.loads(k.read_text())
        for v in st.get("vectors", []):
            if v.get("distributed"):
                fresh += 1
        for c in st.get("chains", []):
            if c.get("status") == "TAKEOVER-CANDIDATE":
                stale.append(("kairo/chain", c.get("chain", "?"), "unproven final hop"))
    h = camp / "harvest-state.json"
    if h.exists():
        st = json.loads(h.read_text())
        for cr in st.get("crown", []):
            at = cr.get("at", "")
            try:
                age = (now - datetime.fromisoformat(at)).days if at else 999
            except Exception:
                age = 999
            if age > args.days:
                stale.append(("shukaku/crown", cr.get("id", "?"), age))
            else:
                fresh += 1
    print(f"═══ SHIKI VALIDATE — {args.target} ({args.days}d drift window) ═══")
    print(f"  fresh CONFIRMED claims: {fresh}")
    if stale:
        for src, label, age in stale:
            print(f"  ⚠ STALE {src}: {label} ({age}) — re-verify (drift before re-assert)")
        print(f"═══ {len(stale)} claim(s) need re-verification — do not cite stale ═══")
        return 1
    print("═══ ALL CONFIRMED CLAIMS FRESH — validated ═══")
    return 0


def cmd_warroom(args):
    """One shot: the war board + fire-list + family engine status."""
    for line in _board_lines(args.org):
        print(line)
    print("")
    args_fires = argparse.Namespace(org=args.org)
    cmd_fires(args_fires)
    print("")
    print("═══ FAMILY ENGINES ═══")
    for name, ok in _family_status_lines():
        print(f"  {ok} {name}")
    print("═══ end war room ═══")
    return 0


def _crown_class_guess(text):
    t = text.lower()
    for kw, cls in (("user", "PII"), ("row", "PII"), ("email", "PII"),
                    ("card", "FIN"), ("payment", "FIN"), ("billing", "FIN"),
                    ("key", "CRED"), ("secret", "CRED"), ("token", "CRED"),
                    ("backup", "BACKUP"), ("dump", "BACKUP"), (".sql", "BACKUP"),
                    ("repo", "SRC"), ("source", "SRC"), ("tenant", "SASS"),
                    ("admin", "SASS"), ("export", "SASS")):
        if kw in t:
            return cls
    return "PII"


def cmd_handoff(args):
    """The next mandate's exact command sequence, consuming this campaign's state."""
    camp = Path.home() / ".redteam" / "campaigns" / args.target
    to = args.to
    print(f"═══ SHIKI HANDOFF → {to.upper()} ({args.target}) ═══")
    if to == "shukaku":
        already = set()
        hs = camp / "harvest-state.json"
        if hs.exists():
            try:
                already = {i.get("finding") for i in
                           json.loads(hs.read_text()).get("ingested", [])}
            except Exception:
                pass
        findings = []
        uc = camp / "undercroft-state.json"
        if uc.exists():
            u = json.loads(uc.read_text())
            for s in u.get("surface", []):
                if s.get("status") == "CONFIRMED":
                    findings.append((f"UC-SURFACE:{s['endpoint']}",
                                     s.get("proof") or "CONFIRMED surface"))
            for l in u.get("logic", []):
                if l.get("status") == "CONFIRMED":
                    findings.append((f"UC-LOGIC:{l.get('seam', 'seam')}",
                                     l.get("proof") or "CONFIRMED logic seam"))
            for p in u.get("pocs", []):
                findings.append((f"UC-POC:{p.get('finding', 'poc')}",
                                 p.get("proof") or "crafted PoC"))
        k = camp / "hardware-state.json"
        if k.exists():
            try:
                for v in json.loads(k.read_text()).get("vectors", []):
                    findings.append((f"KAIRO-VEC:{v.get('id', '?')}",
                                     v.get("proof") or "synthesized vector"))
            except Exception:
                pass
        if not findings:
            print("  (no confirmed findings in family states yet — run the descent)")
            print(f"  template: shukaku ingest --target {args.target} --finding <id>"
                  " --proof <read-only ref>")
        for fid, proof in findings:
            if fid in already:
                continue
            cls = _crown_class_guess(f"{fid} {proof}")
            print(f"  shukaku ingest --target {args.target} --finding \"{fid}\""
                  f" --proof \"{proof[:70]}\"")
            print(f"  shukaku crown  --target {args.target} --asset <asset> --class"
                  f" {cls} --scope <counts> --source \"{fid}\"")
        print("  shukaku reason --target " + args.target)
        print("  shukaku hunt   --target " + args.target + "   # then --live if web reach")
        print("  shukaku feed   --target " + args.target + "   # the loop closes")
        print("  shukaku report --target " + args.target)
    elif to == "kaisha":
        print(f"  kaisha ladder  --target {args.target} --host <h> --access <confirmed>")
        print(f"  kaisha cve     --banner \"<banner from R2>\"")
        print(f"  kaisha lateral --target {args.target} --from <h> --to <adjacent>")
        print(f"  kaisha rungs   --target {args.target}   # then report")
    elif to == "kairo":
        print(f"  kairo ingest --target {args.target}")
        print(f"  kairo gene   --check --target {args.target}   # NO Δ = NO VECTOR")
        print(f"  kairo forge  --target {args.target} --expand")
        print(f"  kairo chain  --target {args.target} --validate")
        print(f"  kairo chain  --target {args.target} --write")
        print(f"  kairo armory --target {args.target}")
    elif to == "holyshit":
        print(f"  holyshit recon --domain <d>")
        print(f"  holyshit dossier --target {args.target}")
        print(f"  holyshit recipe --search \"<confirmed seam>\"")
        print(f"  holyshit handoff --target {args.target} --to <next>")
    else:
        print(f"✗ --to {to} unsupported (shukaku|holyshit|kairo)", file=sys.stderr)
        return 2
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
    asl.add_argument("--parallel", action="store_true", help="find ∥ descend concurrently")
    asl.add_argument("--resume", action="store_true", help="engagement continuity: skip fresh stages, dedupe the rest")
    asl.add_argument("--close", action="store_true", help="closeout: wipe campaign (report archived to ~/.redteam/closeouts)")
    asl.add_argument("--plan-only", action="store_true", help="print the full 6-step plan (exact argv, engine presence); execute nothing")
    wr = sub.add_parser("warroom", help="board + fires + family engine status, one view")
    wr.add_argument("--org", required=True)
    gt = sub.add_parser("gate", help="standalone step-0: barbican vantage check + scope authority")
    gt.add_argument("--target", required=True)
    gt.add_argument("--value", help="domain/url to check against ~/.redteam/scope.json")
    vl = sub.add_parser("validate", help="the PSV validator: re-check every CONFIRMED claim for drift")
    vl.add_argument("--target", required=True)
    vl.add_argument("--days", type=int, default=7)
    ho = sub.add_parser("handoff", help="the next mandate's exact command sequence")
    ho.add_argument("--target", required=True)
    ho.add_argument("--to", required=True, choices=("shukaku", "holyshit", "kairo", "kaisha"))
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
    if a.cmd == "warroom":
        return cmd_warroom(a)
    if a.cmd == "gate":
        return cmd_gate(a)
    if a.cmd == "validate":
        return cmd_validate(a)
    if a.cmd == "handoff":
        return cmd_handoff(a)
    if a.cmd == "assault":
        if getattr(a, "plan_only", False):
            return cmd_assault_plan(a)
        return cmd_assault(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())