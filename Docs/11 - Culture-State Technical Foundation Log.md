# Project Crown: Culture-State Technical Foundation Log

**Date:** 2026-07-07
**Status:** Phase 1B technical foundation created. Tooling, schemas, and Iberia audit outputs only.

## Scope

This phase created culture-state tooling and audit data before the Iberia proof of concept. It did not implement the POC.

No countries, tags, claims, rivalries, friendships, events, missions, formables, province ownership, country history, province history, flags, map files, scripted triggers, scripted effects, or deployed EU4 user-mod files were changed.

## Pre-Flight

- Working folder confirmed: `/Users/roman/Desktop/Project Crown`
- Branch confirmed: `culture-state-world`
- Git working tree was clean before work started.
- Vanilla EU4 was read-only from `/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV`

## Tooling Created

- `Tooling/culture_state/eu4_data.py`
  - Shared EU4 parser and data readers for cultures, tags, country history, province history, map metadata, Project Crown bitmap presence, and bitmap adjacency.
- `Tooling/culture_state/extract_culture_state_data.py`
  - Extracts a province/culture table with province ID, name, culture, culture group, religion, vanilla owner/controller, cores, area, region, superregion, continent, terrain override where available, province type, and Project Crown map presence.
  - Generates the Iberia audit package.
- `Tooling/culture_state/validate_border_cleanliness.py`
  - Prototype validator that reads proposed ownership JSON or a mock Iberia culture-owner table.
  - Infers adjacency from `Mod Build/project_crown/map/provinces.bmp`.
  - Reports disconnected ownership, isolated components, rough province-snake warnings, and exception hints.
- `Tooling/culture_state/culture_state_schema.json`
- `Tooling/culture_state/contested_region_schema.json`
- `Tooling/culture_state/diplomacy_seed_schema.json`

## Vanilla Data Inspected

- `common/cultures/00_cultures.txt`
- `common/country_tags/00_countries.txt`
- `common/countries/` via country-tag references and relevant country-file existence checks
- `history/provinces/`
- `history/countries/`
- `decisions/SpanishNation.txt`
- `decisions/AndalusianNation.txt`
- Iberia-relevant mission files, including Spanish, Aragonese, Portuguese, and Granadan mission files
- `events/FlavorSPA.txt`
- `map/definition.csv`
- `map/default.map`
- `map/area.txt`
- `map/region.txt`
- `map/superregion.txt`
- `map/continent.txt`
- `map/climate.txt`
- `map/terrain.txt`
- `map/adjacencies.csv` was inspected for available sea/canal adjacency data; the prototype validator uses bitmap land adjacency instead.
- Project Crown `Mod Build/project_crown/map/provinces.bmp`

## Audit Files Created

- `Tooling/culture_state/audits/province_culture_table.json`
- `Tooling/culture_state/audits/province_culture_summary.json`
- `Tooling/culture_state/audits/iberia_province_culture_audit.json`
- `Tooling/culture_state/audits/iberia_tag_audit.json`
- `Tooling/culture_state/audits/iberia_formable_audit.json`
- `Tooling/culture_state/audits/iberia_border_cleanliness_stub.json`
- `Tooling/culture_state/audits/iberia_border_cleanliness_validation.json`
- `Tooling/culture_state/audits/iberia_contested_region_candidates.json`
- `Tooling/culture_state/audits/iberia_diplomacy_seed_candidates.json`
- `Tooling/culture_state/audits/iberia_vanilla_content_risk_audit.json`

## Iberia POC Readiness

- Iberia audit scope uses vanilla `iberia_region`.
- The audit found `62` Iberian land provinces.
- All `62` Iberian region province IDs are present in the current Project Crown `provinces.bmp`.
- Iberian cultures present from vanilla history: `andalucian`, `aragonese`, `basque`, `castillian`, `catalan`, `galician`, `leonese`, `portugese`.
- Culture group is inferred from `common/cultures/00_cultures.txt`.
- Terrain is reported where `terrain.txt` has province overrides; full terrain-bitmap classification is not implemented yet.

## Existing Tags Discovered

The audit found vanilla reuse tags for every current Iberia POC target:

| Culture target | Reuse tag | Audit note |
|---|---|---|
| Castilian / Castile | `CAS` | Usable vanilla tag found. |
| Aragonese / Aragon | `ARA` | Tag exists and vanilla culture primary tag points to `ARA`, but `history/countries/ARA - Aragon.txt` currently has `primary_culture = catalan`; Phase 2 must review/override this. |
| Catalan / Catalonia | `CAT` | Usable vanilla tag found: `common/country_tags/00_countries.txt` maps `CAT` to `countries/Catalunya.txt`, with `history/countries/CAT - Catalunya.txt`. No new Catalonia tag is needed from the vanilla audit. |
| Leonese / Leon | `LON` | Usable vanilla tag found. |
| Galician / Galicia | `GAL` | Usable vanilla tag found. |
| Basque / Navarra | `NAV` | Usable vanilla tag found. |
| Andalusian / Granada | `GRA` | Usable vanilla tag found. |
| Portuguese / Portugal | `POR` | Usable vanilla tag found. EU4 spells the culture key `portugese`. |

Related vanilla tags also exist: `SPA`, `ADU`, and `VAL`.

## Existing Formables Discovered

- `decisions/SpanishNation.txt`
  - `spanish_nation`
  - `spanish_nation_diplomatically`
- `decisions/AndalusianNation.txt`
  - `andalusian_nation`

These are references for Phase 2. They were not copied, edited, disabled, or reimplemented in Phase 1B.

## Border-Cleanliness Validator Status

The prototype validator ran against a mock Iberia culture-owner table generated from vanilla province culture.

Results:

- 8 mock countries checked.
- 2 mock countries had disconnected ownership warnings.
- 0 mock countries had province-snake warnings.

Warnings needing human review:

- `CAT`: disconnected because Balearic island provinces are separate components. The validator marks these as island exception candidates.
- `LON`: Caceres is an isolated one-province component under raw culture grouping and needs review.

These are audit findings only. They do not approve or implement any ownership layout.

## Contested-Region Registry Status

`iberia_contested_region_candidates.json` contains candidate entries only:

- Granada frontier
- Valencia-Murcia frontier
- Portuguese-Castilian border

No claims, cores, missions, or escalation rules were implemented.

## Diplomacy-Seed Table Status

`iberia_diplomacy_seed_candidates.json` contains candidate relationships only, with reasons and supporting basis. No historical rivals, friends, opinion modifiers, alliances, or threat hints were implemented.

## Vanilla Content Risks

The audit flags these Iberia POC review risks:

- Iberian Wedding in `events/FlavorSPA.txt` assumes the vanilla Castile-Aragon setup.
- Spanish and Aragonese missions branch on Catalan primary culture and vanilla Spain/Aragon assumptions.
- Vanilla Spain and Andalusia decisions are useful references but need Project Crown re-scope.
- Portugal's colonial mission identity should be preserved later without letting Spain absorb Portugal by default.

## Excluded From Iberia POC For Now

- No hostile intervention system.
- No Great Power intervention logic; future Great Power checks should use a Project Crown trigger such as `crown_is_great_power`, not Rights of Man assumptions.
- No rare dynastic/diplomatic unification package.
- No colonial proxy wars or parent escalation.
- No flag import.
- No final ownership proposal.
- No map edits.

## Recommended Next Step

Proceed to the owner review of the Iberia data package:

1. Review the `CAT` discovery and update the Iberia tag budget accordingly.
2. Decide how Phase 2 should handle `ARA`'s vanilla primary-culture mismatch.
3. Review the Catalan island exception and Leonese Caceres warning before any ownership proposal is generated.
4. Use the contested-region and diplomacy candidate files as review inputs, not implementation instructions.

