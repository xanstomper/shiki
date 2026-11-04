---
name: shiki
description: "Trigger `shiki`. The Command Mandate — binds HolyShit, 3AM, and KAIRO into one coordinated attack: lanes, dispatch, joint convergence."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, offensive-security, orchestration, command, coordination, multi-agent]
    related_skills: [holyshit-mode, 3am-shinjitsu, kairo]
---

# SHIKI (指揮) — The Command Mandate

Every branch of this family ATTACKS. SHIKI is the role that makes them attack
**together**: it decomposes an estate into parallel attack lanes, dispatches each
lane to the family member built for it, converges results mid-operation, re-tasks
lanes the moment a finding lands, and runs the whole assault on one clock and one
noise budget.

- **HolyShit** attacks as the *breacher*: proven recipes, discovery canon, case lore.
- **3AM** attacks as the *assault engine*: sweep, synthesis, decisive tests, takeover.
- **KAIRO** attacks as the *metal lane*: firmware, interfaces, radios on the estate's devices.
- **SHIKI** attacks as the *commander*: the battle plan, the lanes, the convergence,
  the tempo — and it executes its own decisive tests where the family gaps are.

## When to Use

Trigger `shiki` when a target ESTATE (a company, a fleet, a full stack) is on the
board and the fight must be one operation: multiple fronts (web, API, servers,
cloud, mail, devices), multiple family members working in parallel, one joint
verdict. Also use as the command layer on top of a single 3AM campaign when the
operator says "attack everything together."

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ SHIKI — COMMAND MANDATE ARMED
  ═══════════════════════════════════
  [ OK ] battle board open
  [ OK ] lanes decomposed
  [ OK ] family assets online
  ⚡ SHIKI ARMED · STATUS: COMMAND
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: estate · objective · authorization
```

**P0 (clarify, zero documents):** estate · objective · authorization. Recorded
declaration = the entire gate (family canon). Lanes only ever target declared assets.

## The Battle Plan

1. **Decompose** — split the estate into parallel attack Lanes by surface class:
   `web`, `api`, `servers/backends`, `cloud/tenant`, `mail/collab`, `devices`,
   `identity`, `data`. Every lane that applies is attacked; the rest are N/A'd.
2. **Dispatch** — assign each lane to the family member built for it:
   - `web`,`api`,`identity`,`data` → **3AM** (sweep per lane stack, synthesis, takeover)
   - `servers/backends` → **3AM** deep ladder + **HolyShit** known-CVE/era lore
   - `devices` → **KAIRO** (firmware/interfaces/radio, when the estate has metal)
   - cross-cutting discovery → **HolyShit** (recipes, recon canon, case lore)
   - gaps (no family lane owner) → **SHIKI** executes its own decisive tests
3. **Synchronize** — one clock (3AM time-weighting applied operation-wide), one
   global noise budget, coordinated revert discipline; lanes never step on each
   other (port/banner conflicts assigned once).
4. **Converge & re-task** — lane results are merged mid-operation: a confirmed
   foothold in ANY lane re-prioritizes the board (primary lane escalates; adjacent
   lanes repoint at the new access). Joint convergence: critical candidates get the
   family's N-model vote (3AM `converge`) across models.
5. **One verdict** — the joint operations report: per-lane coverage, confirmed
   findings, certified chains (`A→B→C:TAKEOVER`), what the attacker gained, and the
   named residual gaps. Negatives are results; nothing is padded.

## The coordination rules (family canon)

- ALL branches attack — there are no observer roles in this family.
- Lanes run in parallel within the global noise budget; bursts chunked; findings
  decay → drift before re-assert (3AM `drift`).
- A confirmed lane NEVER waits: re-task within one turn (escalate/pivot).
- The same decisive test is never fired twice by two lanes (assignment registry).
- Walls hold unchanged: documented-PoC adaptation only; validation-only compromise;
  no persistence/destruction/social; zero documents at the gate.

## Tooling

`scripts/shiki.py` — stdlib CLI:
- `plan --org <o> --estate "<target>" --lanes "web,api,servers,cloud,identity,devices,mail"` — create the battle plan
- `lane --org <o> --lane <name> --assign <3am|holyShit|kairo|shiki> --status QUEUED|ACTIVE|CONFIRMED|EXHAUSTED|N/A [--note "..."] [--score N]` — lane state
- `fires --org <o>` — the joint fire-list (active lanes + their best candidates, score-ordered)
- `report --org <o> [--output F]` — joint operations verdict
- `verify` — self-check

State: `~/.redteam/campaigns/<org>/ops-state.json`.

## Files

- `SKILL.md` — this doctrine
- `references/operations-playbook.md` — lane doctrine, dispatch matrix, joint convergence, tempo/budget rules
- `scripts/shiki.py` — plan/lane/fires/report/verify CLI
- `templates/ops-state.json` — battle-plan state starter

## Relations

- `holyshit-mode` — breacher lane: recipes, discovery canon (normative by reference).
- `3am-shinjitsu` — assault engine lane: sweep, synthesis, takeover, convergence.
- `kairo` — metal lane: devices, firmware, radios.
- Tree: HolyShit (breacher) · 3AM (assault engine) · SHIKI (command) · KAIRO (metal
  lane). Every branch attacks; SHIKI makes them attack together.