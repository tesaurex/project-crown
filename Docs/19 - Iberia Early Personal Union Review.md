# Iberia Early Personal Union Review

Date: 2026-07-09
Branch: iberia-poc-polish

## Purpose

Phase 2F reviews the observer report that Portugal held a personal union over Castile by 1497. Project Crown wants Iberia to stay aggressive and capable of consolidation, but not through random early Portugal-Castile or Castile-Portugal personal unions before the rare dynastic unification system is designed.

This pass does not implement the full rare dynastic system.

## Finding

No Project Crown diplomacy file seeds a Castile-Portugal royal marriage, alliance, or union. `history/diplomacy/project_crown_iberia.txt` only contains the Phase 2E Granada-Al-Gharb alliance.

The Project Crown Spanish flavor override still disables the Iberian Wedding with `always = no`. The later Spanish "Portuguese Crown" event remains, but it is a Spain-over-Portugal event after 1550 and does not explain Portugal over Castile by 1497.

Vanilla Spanish, Aragonese, and Navarrese missions contain restore-personal-union CB rewards, but they do not directly create a Portugal-over-Castile union and Project Crown has no mission overrides.

The most likely cause is ordinary EU4 dynastic succession after a natural AI royal marriage. Castile and Portugal are Catholic monarchies with mutual historical friendship, making an early royal marriage plausible. Castile also started the 1444 game with Enrique de Trastamara as heir and a forced `add_heir_personality = infertile_personality`, which is unsafe once the Iberian Wedding is deferred.

## Risk Review

| Tag | Early PU Risk | Notes |
| --- | --- | --- |
| CAS | High before patch, medium after patch | Catholic monarchy, historical friend with Portugal, valid heir Enrique. Forced heir infertility was the main amplifier. |
| POR | Medium | Catholic monarchy, valid Afonso heir, historical friend with Castile and Spain. |
| ARA | Medium | Catholic monarchy with valid Joan heir; shared Trastamara context and vanilla Naples union are watch items. |
| CAT | Medium | Sparse released-state history means generated dynasty/heir behavior. |
| LON | Medium | Sparse released-state history means generated dynasty/heir behavior. |
| GAL | Medium | Sparse released-state history means generated dynasty/heir behavior. |
| NAV | Medium-high | Catholic monarchy, Trastamara ruler, no explicit 1444 heir. Small size keeps it below the CAS/POR superpower risk. |
| GRA | Low | Sunni monarchy, so normal Catholic royal-marriage PU paths do not apply. |
| AGH | Low | Sunni monarchy with a valid heir. |

## Patch

Changed `Mod Build/project_crown/history/countries/CAS - Castile.txt`:

- Removed `add_heir_personality = infertile_personality` from the 1425.1.5 Enrique heir block.

Everything else was left intact: Enrique's dynasty, claim, stats, dates, Castile-Portugal historical friendship, Project Crown diplomacy, missions, events, decisions, claims, forts, development, ownership, and map files.

This preserves ordinary monarchy variance while removing the forced early no-heir pressure that could turn a friendly Portugal marriage into a 1490s superpower union.

## Deferred

- No full rare dynastic system.
- No scripted early `break_union` guardrail.
- No new starting royal marriages, alliances, or rivalries.
- No mission-tree override.
- No new heirs for CAT/LON/GAL/NAV in this pass.
- No map, ownership, controller, development, fort, claim, or non-Iberian overhaul.

## Validation

- JSON parse: passed for the Phase 2F audit files.
- EU4 brace check: passed for Castile history, the Spanish flavor override, and Project Crown Iberia diplomacy.
- Owner/controller: passed with a date-aware 1444.11.11 check over the 62 Iberian ownership provinces.
- Border cleanliness: passed with the known Catalan Balearic island exception.
- Map validator: passed with matching dimensions, zero undefined pixels, and zero missing vanilla-defined IDs.
- Localisation: not applicable; no localisation files changed.
- Map files changed: none.
- Deployment sync: copied the updated Castile history into the local EU4 mod deployment and verified the copy matches.

## Next Observer Focus

The next observer should specifically check whether Portugal or Castile still get an early mutual personal union before 1500. Also watch whether Navarre or the sparse Catholic minors become frequent unintended PU subjects, or whether their risk remains normal minor-state variance.
