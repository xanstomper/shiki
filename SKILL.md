---
name: shiki
description: "Trigger `shiki`. THE COMMAND — runs the whole family as one assault: barbican gate → holyshit recon/dossier → undercroft live descent → kairo forge → chains → joint verdict. One command."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, offensive-security, orchestration, command, multi-agent, authorized-testing]
    related_skills: [barbican, holyshit-mode, 3am-shinjitsu, undercroft, kairo]
---

# SHIKI — The Command Mandate

The family's conductor. Every branch attacks; SHIKI makes them attack **together,
in order, under the shield** — and it drives their REAL engines, not summaries:

```
barbican vantage check   (the gate: no verified exit → no assault)
   ↓
holyshit recon + dossier (the finder: domain checklist + everything known)
   ↓
undercroft run           (the descent: live auto-engagement, read-only)
   ↓
kairo forge --expand     (the synthesizer: every finding → attacks + variants)
   ↓
kairo chain --write      (the kill chains: BOUNDARY→REPLAY:TAKEOVER …)
   ↓
armory + joint verdict   (the war board: what's confirmed, what's armed, what's next)
```

One command — `shiki assault` — runs the entire family against a declared estate
and hands back the joint operations report. Read-only by construction (the descent
fires GETs only); everything state-changing stays behind explicit --confirm gates
in the consumer mandates.

## The Family Tree (roles)

```
   BARBICAN (first layer — the shield, the gate)
      ↓ posture verified
   HolyShit (finder) · 3AM (performer) · UNDERCROFT (descent) · KAIRO (synthesizer)
      ↓ findings relay to kairo, compiled attacks relay back
   SHIKI (command) — conducts the whole orchestra as one assault
```

## When to Use

Trigger `shiki` when a declared estate must be engaged as ONE operation — the
operator wants the family, not one member. Also the capstone after manual lanes:
`board` shows the war, `assault` fights it.

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ SHIKI — COMMAND ONLINE
  ═══════════════════════════════════
  [ OK ] family engines located
  [ OK ] war board open
  [ OK ] relay wired
  ⚡ SHIKI ARMED · STATUS: CONDUCTING
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: estate · objective · authorization
```

**P0 (clarify, zero documents):** estate · objective · authorization. Recorded
declaration = the entire gate. SHIKI refuses to conduct without a barbican posture
on the target — the shield goes up first, always.

## The Assault Sequence (what `assault` actually runs)

0. **GATE** — `barbican vantage check --target T`: posture exists + vantage live,
   or the assault aborts (rc=1) before a single packet.
1. **FIND** — `holyshit recon --domain D` + `dossier --target T`: the discovery
   checklist + everything the canon knows.
2. **DESCEND** — `undercroft run --target T --domain D --url U [--bundle B]
   [--boundary-url … --probe-ids …]`: the live read-only engagement.
3. **FORGE** — `kairo forge --target T --expand`: every finding → attack vectors
   + sibling variants, distributed to all consumers.
4. **CHAIN** — `kairo chain --target T --write`: the multi-hop kill chains
   (`BOUNDARY→REPLAY:TAKEOVER`).
5. **VERDICT** — `kairo armory` + the joint operations report: per-lane results,
   confirmed findings, armed chains, named gaps, next steps (3AM promote).

SHIKI executes its own decisive tests only where no family engine exists — and
says so in the report.

## Manual command layer (when the operator drives lane-by-lane)

- `plan --org <o> --estate "<target>" --lanes "web,api,servers,cloud,identity,devices,mail"`
- `lane --org <o> --lane <name> --assign <3am|holyShit|kairo|shiki> --status … [--note] [--score N]`
- `fires --org <o>` — the joint fire-list, score-ordered
- `board --org <o>` — the war board: all family states summarized in one view
- `report --org <o> [--output F]` — the joint operations verdict

## Coordination rules (family canon)

- The shield goes up first: no barbican posture, no assault.
- All branches attack — no observer roles; the same decisive test never fired twice
  (assignment registry); confirmed lanes re-task within one turn.
- Findings decay → drift before re-assert; bursts chunked within the global noise
  budget; the assault is read-only by construction.
- Walls unchanged: documented-PoC adaptation, validation-only compromise, no
  persistence/destruction/social, zero documents.

## Tooling

`scripts/shiki.py` — stdlib CLI:
- `assault --target T --url U --domain D [--bundle P] [--cookie k=v] [--boundary-url U2] [--probe-ids 1,2] [--skip gate|find|descend|forge|chain]` — the orchestrated assault
- `board --org <o>` — the war board (all family states, one view)
- `plan/lane/fires/report` — the manual battle plan (v1 layer)
- `verify` — self-check (incl. family engines located)

State: `~/.redteam/campaigns/<target>/ops-state.json`.

## Files

- `SKILL.md` — this doctrine
- `references/operations-playbook.md` — lane doctrine, dispatch matrix, convergence, tempo
- `scripts/shiki.py` — assault/board/plan/lane/fires/report/verify CLI
- `templates/ops-state.json` — battle-plan state starter

## Relations

- `barbican` — THE FIRST LAYER: its gate is SHIKI's step 0; no posture, no assault.
- `holyshit-mode` — the finder: recon + dossier are SHIKI's step 1.
- `undercroft` — the descent: its live `run` is SHIKI's step 2.
- `kairo` — the synthesizer: forge + chains are SHIKI's steps 3–4.
- `3am-shinjitsu` — the performer: the matrix the assault feeds (promote step).
- Tree: BARBICAN (shield) → HolyShit (finder) → UNDERCROFT (descent) → KAIRO
  (synthesizer) → 3AM (performer), conducted by SHIKI (command). One family,
  one gate, one command.