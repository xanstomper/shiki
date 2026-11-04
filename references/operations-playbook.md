# SHIKI — Operations Playbook (lanes · dispatch · convergence · tempo)

## Lane decomposition

Split the estate by surface class. Every lane is ATTACKED or N/A'd with a reason:

| Lane | Attack owner | Primary play |
|---|---|---|
| web | 3AM | sweep stack fingerprints → fire-list → decisive tests (arsenal-02) |
| api | 3AM | schema mining, authz matrix, IDOR/coercion (arsenal-03) |
| servers/backends | 3AM + HolyShit | deep ladder: era-stack → CVE → RCE → harvest → lateral (KAISHA-style ladder lives here) |
| cloud/tenant | 3AM | bucket/object/IAM/SSRF/tenant tests (families 13, universal U07/U09) |
| identity | 3AM | OAuth/GoTrue/SSO/token chains (arsenal-04) |
| mail/collab | 3AM | SPF/DKIM/OAuth grants/sharing (universal U11) |
| devices | KAIRO | five planes: firmware/interfaces/radio/protocol/physical |
| data | 3AM | DB engines, backups, object stores (family 15, U09) |
| discovery | HolyShit | CT/passive-DNS/brand-grid feeding every lane's targets |
| gaps | SHIKI | executes its own decisive tests where no lane owner exists |

## Dispatch & assignment registry

- Every lane gets ONE owner and ONE primary test list; before firing, check the
  registry: the same endpoint/test is never assigned to two lanes.
- Port/banner conflicts: assign once (e.g. `:443` era-stack to lane web; `:22` to
  lane servers) — no double-touching.
- Lanes may request shared assets (a harvested key, a session) through the command
  board; the grant is recorded and revoked when the lane closes.

## Joint convergence

- Critical candidates (score ≥ 75 or post-foothold) get the family vote: 3AM
  `converge` with the family's model set; a BLOCKED vote stops that spend.
- Cross-lane chains: a CONFIRMED in lane A re-prioritizes lanes B/C that touch the
  same trust root (shared IdP, shared backend, shared keys). Re-task within one turn.
- Chain certification per 3AM style: `A→B→C:TAKEOVER` — final hop proof lands, then
  STOP (validation-only).

## Tempo & budget

- One clock: 3AM Score′ (time-weighted) re-scored per lane after every result.
- Global noise budget (3AM §12 ceilings × lanes), burst chunking, drift-before-
  re-assert on re-entry.
- Findings decay: a lane result older than one engagement session re-verifies before
  appearing in the joint report.

## The command rhythm

```
plan (decompose+dispatch) → lanes ACTIVE in parallel → fires (joint fire-list) →
per-lane results merge → convergence vote on criticals → re-task on CONFIRMED →
drift on re-entry → report (one joint verdict)
```

## Walls

Identical to the family: documented-PoC adaptation only; validation-only compromise
(one proof, then stop); no persistence/destruction/social; zero documents at P0;
all lanes restricted to the declared estate.