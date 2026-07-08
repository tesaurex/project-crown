# Project Crown: Iberia QA and Balance Report

**Date:** 2026-07-08
**Branch:** `iberia-poc-polish`
**Scope:** Phase 2B structured QA and balance review of the Iberia Culture-State POC.

## Technical QA Result

Static QA passes. The Project Crown folder and branch were correct before work started, and the working tree was clean. This pass made documentation and audit-output changes only.

Validation results:

- Iberian owner/controller consistency: 62 province overrides checked, 0 mismatches.
- Starting owner cores: 62 province overrides checked, every starting owner has a core.
- EU4 text brace validation: 77 Project Crown `.txt` files checked, 0 brace-balance errors.
- Localisation: `crown_iberia_l_english.yml` has the expected `l_english:` header, UTF-8 BOM, one-space entries, and required `AGH` / `spanish_nation` keys.
- Audit JSON parse: 18 audit JSON files parsed successfully after the Phase 2B files were added.
- Map validator: passed with 0 undefined province pixels and no missing vanilla-defined province IDs.
- Border-cleanliness validator: passed with the documented Catalonia/Balearics exception. Nine countries checked, one disconnected owner (`CAT`) due only to accepted island components, and 0 province-snake warnings.

No technical issue justified a gameplay fix during this phase.

## Balance Summary By Country

| Tag | Country | Provinces | Dev | Manpower dev | Forts | Balance read |
|---|---:|---:|---:|---:|---:|---|
| `CAS` | Castile | 13 | 110 | 31 | 2 | Strong central contender, but not clearly dominant over Granada or Catalonia. |
| `GRA` | Granada | 12 | 109 | 28 | 1 | Strong southern pole; constrained by Muslim tech, Sunni state religion, and 8 Catholic provinces. |
| `CAT` | Catalonia | 12 | 101 | 26 | 2 | Major eastern contender; Balearics are the only accepted disconnected exception. |
| `POR` | Portugal | 7 | 89 | 21 | 1 | Still viable after Al-Gharb split, with Lisboa/Porto trade centers and Castile friendship. |
| `LON` | Leon | 5 | 46 | 12 | 0 | Playable minor, but exposed without an explicit fort. |
| `ARA` | Aragon | 4 | 36 | 10 | 1 | Compact and defensible, but much weaker than Catalonia. |
| `GAL` | Galicia | 4 | 28 | 7 | 0 | Coherent small state; survival needs observer confirmation. |
| `AGH` | Al-Gharb | 3 | 24 | 7 | 1 | Viable local spoiler, not overpowered. |
| `NAV` | Navarre | 2 | 13 | 4 | 0 | Fragile by design; watch early survival. |

Static balance does not prove Castile is too dominant. Castile has only 1 more development than Granada and 9 more than Catalonia. Its position, accepted cultures, and two forts may still make it the most reliable AI winner, but that needs observer evidence rather than a speculative rebalance.

Granada is intentionally strong enough to make southern Iberia matter. Its static development is high, but its religious mix and Muslim technology group are real constraints. If Granada collapses to unrest or becomes the repeat winner, tune after observer testing.

Portugal appears survivable with Al-Gharb added. It keeps 89 development, Lisboa and Porto trade centers, a Lisboa fort, and friendly history with Castile. Al-Gharb has 24 development, one fort, and restrained claims, so it should create local drama without making Portugal helpless.

Catalonia/Aragon is the main static watch item. Catalonia at 101 development greatly outweighs Aragon at 36 even though Aragon is the Aragonese staple. This is not a bug, but observer runs should verify that Aragon still has a meaningful role.

Leon, Galicia, and Navarre are intentionally minor starts. If they disappear too quickly, the safer first tuning levers are diplomacy, AI claim pacing, or a small defensive adjustment, not province redistribution.

## Spain Formation Review

`spanish_nation` is correctly scoped for the POC.

- Intended eligible tags: `CAS`, `ARA`, `CAT`, `LON`, `GAL`, `NAV`.
- Portugal is excluded.
- Granada and `ADU` are excluded, leaving Andalusian-to-Spain design deferred.
- The vanilla diplomatic Spain route is not present in the Project Crown override.
- Requirements are demanding but possible: adm tech 10, at peace, free/not nomad, and ownership/core control of ten key provinces across Galicia, Navarre, Catalonia, Aragon, Castile, Leon, Valencia, and Granada.
- Formation claims cover non-Portuguese Iberia only: `iberia_region` minus `alentejo_area` and `beieras_area`. That excludes all current Portugal and Al-Gharb starting provinces.
- The permanent-claim reward is broad enough for Spanish consolidation but not excessive for the owner rule excluding Portugal.

No Spain decision fix is recommended before observer testing.

## Diplomacy And Rivalry Review

Starting diplomacy is restrained and logical.

- `CAS` and `GRA` are mutual historical rivals, matching the Castile/Granada frontier.
- `CAS` and `POR` retain friendship, helping Portugal survive outside Spain.
- `POR` and `AGH` are mutual historical rivals, matching the southern Portuguese split.
- `POR` has historical friendship with `SPA`, which is harmless at 1444 because Spain does not exist and supports later Portugal-Spain friendliness if Spain forms.

There is no arbitrary total-chaos diplomacy layer.

## Known Issues

- Observer pacing is still untested in this pass.
- No EU4 launch or visual in-game pass was performed during Phase 2B.
- Spanish, Aragonese, Portuguese, and Granadan mission-tree assumptions remain known later-content risks from the Phase 1B/2A audit trail.
- Aragon may be underweight relative to Catalonia.
- Navarre, Galicia, and Leon may need survival help depending on observer results.

## Recommended Small Fixes

None for this phase. The static QA found no missing localisation, invalid JSON, owner/controller bug, missing owner core, obvious invalid decision condition, or brace issue that justified a gameplay edit.

## Wait For Observer Testing

- Iberia consolidation pace toward 2-4 states by about 1550.
- Spain formation frequency by about 1650.
- Whether Portugal usually survives outside Spain.
- Whether Al-Gharb survives long enough to matter without blocking Portugal too often.
- Whether Granada is stable and competitive without becoming the repeat winner.
- Whether Aragon, Leon, Galicia, and Navarre contribute meaningfully before consolidation.

## Intentionally Not Implemented

- No map edits.
- No flag imports.
- No non-Iberian overhaul.
- No hostile intervention.
- No rare dynastic or diplomatic unification events.
- No colonial proxy wars or parent escalation.
- No automatic province development.
- No major province redistribution or development rebalance.
