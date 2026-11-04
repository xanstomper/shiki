<div align="center">

```
   ███████╗██╗  ██╗██╗██╗  ██╗██╗
   ██╔════╝██║  ██║██║██║ ██╔╝██║
   ███████╗███████║██║█████╔╝ ██║
   ╚════██║██╔══██║██║██╔═██╗ ██║
   ███████║██║  ██║██║██║  ██╗██║
   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝
        THE COMMAND — 屋敷
```

# 🎖️ SHIKI

### *One command. The whole family, in order, under the shield.*

**The Command Mandate of the HolyShit family** — the conductor. Every branch
attacks; SHIKI makes them attack **together, in order, under the shield** — and it
drives their REAL engines, not summaries.

[![Version](https://img.shields.io/badge/version-2.0.0-blueviolet?style=for-the-badge)](#the-cli)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#quickstart)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#quickstart)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge)](#why-its-powerful)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://github.com/xanstomper/shiki/actions/workflows/verify.yml/badge.svg)](https://github.com/xanstomper/shiki/actions/workflows/verify.yml)
[![Use](https://img.shields.io/badge/use-AUTHORIZED%20TARGETS%20ONLY-crimson?style=for-the-badge)](#the-walls-non-negotiable)

**THE FAMILY** — six siblings and the dispatcher, one click each:

[![00 BARBICAN · the shield](https://img.shields.io/badge/00-BARBICAN%20·%20the%20shield-2E4057?style=for-the-badge)](https://github.com/xanstomper/barbican)
[![01 3AM · the performer](https://img.shields.io/badge/01-3AM%20·%20the%20performer-8B0000?style=for-the-badge)](https://github.com/xanstomper/3am-shinjitsu)
[![02 KAIRO · the synthesizer](https://img.shields.io/badge/02-KAIRO%20·%20the%20synthesizer-6B8E23?style=for-the-badge)](https://github.com/xanstomper/kairo)
[![03 UNDERCROFT · the descent](https://img.shields.io/badge/03-UNDERCROFT%20·%20the%20descent-4B0082?style=for-the-badge)](https://github.com/xanstomper/undercroft)
[![04 HOLYSHIT · the finder](https://img.shields.io/badge/04-HOLYSHIT%20·%20the%20finder-B8860B?style=for-the-badge)](https://github.com/xanstomper/HolyShit)
[![06 SHUKAKU · the harvester](https://img.shields.io/badge/06-SHUKAKU%20·%20the%20harvester-8B4513?style=for-the-badge)](https://github.com/xanstomper/shukaku)
[![SPYDERMONKEY · the dispatcher](https://img.shields.io/badge/🕷️-SPYDERMONKEY%20·%20the%20dispatcher-blueviolet?style=for-the-badge)](https://github.com/xanstomper/spydermonkey)

[How it works](#how-it-works) · [Why it's powerful](#why-its-powerful) ·
[Quickstart](#quickstart) · [The CLI](#the-cli) · [The Walls](#the-walls-non-negotiable)

</div>

---

## What is this?

SHIKI is the family's conductor. One command — `shiki assault` — runs the entire
family against a declared estate and hands back the joint operations report:

```
✓ SHIKI verify: compile · subcommands · template — ALL PASS
```

Read-only by construction (the descent fires GETs only); everything state-changing
stays behind explicit `--confirm` gates in the consumer mandates.

## How it works

### The assault sequence — what `assault` actually runs

```
0. GATE     barbican vantage check     no verified exit → the assault aborts (rc=1)
                                       before a single packet
1. FIND     holyshit recon + dossier   the discovery checklist + everything known
2. DESCEND  undercroft run             the live read-only engagement
3. FORGE    kairo forge --expand       every finding → attack vectors + variants
4. CHAIN    kairo chain --write        the multi-hop kill chains
5. VERDICT  kairo armory + report      per-lane results, confirmed findings,
                                       armed chains, named gaps, next steps
```

**Adaptive re-tasking:** lanes update from live results — the same decisive test
never fires twice (assignment registry), confirmed lanes re-task within one turn.

### The manual command layer (operator drives lane-by-lane)

```bash
shiki plan --org acme --estate "acme.com" --lanes "web,api,servers,cloud,identity,devices,mail"
shiki lane --org acme --lane web --assign 3am --status CONFIRMED --score 9
shiki fires --org acme          # the joint fire-list, score-ordered
shiki board --org acme          # the war board — all family states, one view
shiki report --org acme         # the joint operations verdict
```

## Why it's powerful

- **Real engines, not summaries.** SHIKI doesn't describe the pipeline — it
  *executes* barbican, holyshit, undercroft, and kairo CLIs in sequence and merges
  their live output into one verdict.
- **The gate is step 0.** No barbican posture, no assault — the shield goes up
  first, always, or the conductor refuses (rc=1) before a single packet.
- **All branches attack.** No observer roles; findings relay to kairo, compiled
  attacks relay back, and lanes re-task from live results within one turn.
- **Idempotent resume, clean close.** `--resume` re-enters an interrupted assault
  without double-firing; `--close` wipes the campaign when it's done.
- **The war board.** `board` summarizes every family state — one view of what's
  confirmed, what's armed, what's next.
- **Zero dependencies.** Pure Python stdlib. Clone and run.

## Quickstart

```bash
git clone https://github.com/xanstomper/shiki.git
python3 shiki/scripts/shiki.py verify     # → ALL PASS (locates the family engines)
python3 shiki/scripts/shiki.py assault --target t --url https://t.example \
    --domain t.example --parallel
```

## The CLI

| Command | What it does |
|---|---|
| `assault --target T --url U --domain D [--bundle P] [--boundary-url U2] [--probe-ids 1,2] [--skip gate\|find\|descend\|forge\|chain] [--plan-only]` | the orchestrated assault (steps 0–5); `--plan-only` = the full plan, nothing executes |
| `gate --target T` | standalone step-0 — the shield check (GATE OPEN/CLOSED) |
| `warroom --org O` | board + fires + family engine status, one dense view |
| `handoff --target T --to shukaku\|holyshit\|kairo` | the next mandate's exact command sequence from live state |
| `board --org O` | the war board — all family states in one view |
| `plan / lane / fires / report` | the manual battle plan layer |
| `verify` | self-check (incl. family engines located) |

## The Walls (non-negotiable)

Documented-PoC adaptation · validation-only compromise · no persistence, no
destruction, never social · zero documents · no barbican posture, no assault —
family canon at every layer.

## Files

```
shiki/
├── SKILL.md                        # the doctrine
├── scripts/
│   └── shiki.py                    # assault/board/plan/lane/fires/report/verify
├── references/
│   └── operations-playbook.md      # lane doctrine, dispatch matrix, convergence, tempo
└── templates/
    └── ops-state.json              # battle-plan state starter
```

## Relations

`spydermonkey` dispatches it · `barbican` gates it (step 0) · `holyshit-mode` finds
(step 1) · `undercroft` descends (step 2) · `kairo` forges and chains (steps 3–4) ·
`3am-shinjitsu` takes the promote step · `shukaku` prices the gain (P5 layer).

## License

[MIT](LICENSE) — conduct with it, build for it, route through it.

<div align="center">

*Every branch attacks. One command.*

</div>
