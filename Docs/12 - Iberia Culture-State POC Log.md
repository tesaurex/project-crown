# Project Crown: Iberia Culture-State POC Log

**Date:** 2026-07-07
**Status:** Phase 2A implemented for Iberia only.

## Scope

This phase implements the first playable Culture-State World region: Iberia. It uses vanilla reuse tags and Project Crown history-file overrides only. No map files, flags, non-Iberian province histories, hostile intervention mechanics, rare dynastic unification events, or colonial proxy-war systems were implemented.

## Pre-Flight

- Working folder confirmed: `/Users/roman/Desktop/Project Crown`
- Branch confirmed: `iberia-poc`
- Git working tree was clean before work started.
- Vanilla EU4 was read read-only from `/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV`

## Iberian Countries Implemented

| Tag | Role | Primary culture | Capital |
|---|---|---|---|
| `CAS` | Castile / Castilian staple | `castillian` | Toledo (`219`) |
| `ARA` | Aragon / Aragonese staple | `aragonese` | Zaragoza (`214`) |
| `CAT` | Catalonia/Catalunya / Catalan state | `catalan` | Barcelona (`213`) |
| `LON` | Leon / Leonese state | `leonese` | Leon (`208`) |
| `GAL` | Galicia / Galician state | `galician` | Galicia (`206`) |
| `NAV` | Navarre / Basque state | `basque` | Navarra (`210`) |
| `GRA` | Granada / Andalusian state | `andalucian` | Granada (`223`) |
| `POR` | Portugal / Portuguese state | `portugese` | Lisboa (`227`) |

## Province Ownership Approach

Ownership follows the Phase 1B Iberia culture audit for all Iberian land provinces except Caceres. Each Iberian province history override preserves vanilla development, trade goods, religion, culture, discovery, and future dated bookmark history while replacing the 1444 top-level `owner`, `controller`, and core setup.

Summary:

| Tag | Province count | Province IDs |
|---|---:|---|
| `CAS` | 13 | 215, 217, 219, 1745, 1746, 1747, 2751, 2754, 2755, 2989, 4551, 4552, 4789 |
| `ARA` | 4 | 211, 214, 2990, 4557 |
| `CAT` | 12 | 197, 212, 213, 220, 333, 1750, 2987, 2988, 4549, 4550, 4559, 4560 |
| `LON` | 5 | 207, 208, 216, 4553, 4788 |
| `GAL` | 4 | 206, 4554, 4555, 4558 |
| `NAV` | 2 | 209, 210 |
| `GRA` | 12 | 218, 221, 222, 223, 224, 225, 226, 1748, 1749, 4546, 4547, 4548 |
| `POR` | 10 | 227, 228, 229, 230, 231, 232, 1851, 4150, 4556, 4787 |

## Cores and Claims

Each culture-state has 1444 cores on its starting provinces. Caceres (`1747`) is owned and cored by Castile but also keeps a Leonese core to represent the cultural dispute without creating a disconnected Leonese start.

No broad permanent-claim layer, mission ladder, contested-region system, or group-claim system was implemented in this phase. Spain formation grants permanent claims on the vanilla `iberia_region` except `alentejo_area` and `beieras_area`, preserving the owner rule that Portugal is not required for Spain and should not be casually absorbed.

## Aragon Primary Culture Decision

Vanilla `ARA - Aragon.txt` uses `primary_culture = catalan` and `capital = 213`. Project Crown overrides Aragon as the Aragonese staple:

- `primary_culture = aragonese`
- `capital = 214` (Zaragoza)
- `add_accepted_culture = catalan`

`CAT` remains the Catalan culture-state with Barcelona as capital.

## CAT Island Decision

Catalonia keeps the Balearic island provinces (`333`, `4559`, `4560`). The border validator reports them as disconnected land components, but this is accepted as an O7 island exception: the islands are Catalan-culture, historically/geographically reasonable, and do not create mainland border gore.

## Caceres Decision

Caceres (`1747`) is Leonese culture but creates an isolated Leonese component under raw culture ownership. The tested alternatives were:

- Leon ownership: disconnected Leonese start.
- Granada ownership: disconnected Granadan component.
- Castile ownership: all mainland Iberian countries connected except the accepted Catalan islands.

The POC assigns Caceres to Castile and gives Leon a core.

## Spain Formation Decision

The vanilla `SpanishNation.txt` decision is replaced. Project Crown keeps a conservative military `spanish_nation` path and removes the vanilla diplomatic formation path for now.

Eligible POC formers:

- `CAS`
- `ARA`
- `CAT`
- `LON`
- `GAL`
- `NAV`

Excluded/deferred:

- `POR` is excluded by owner rule.
- `GRA` / Andalusian-to-Spain is deferred. Granada keeps the Andalusian identity for now; an alternate Andalusian-to-Spain or Andalusia path needs later design.
- Rare dynastic Castile-Aragon union content is deferred.

Required key provinces:

- Galicia (`206`)
- Navarra (`210`)
- Barcelona (`213`)
- Zaragoza (`214`)
- Castilla La Vieja (`215`)
- Salamanca (`216`)
- Toledo (`219`)
- Valencia (`220`)
- Granada (`223`)
- Andalucia (`224`)

## Diplomacy

Diplomacy changes are intentionally minimal. Vanilla Castile-Granada rivalry and Castile-Portugal friendship are preserved through copied country history. Granada now has `historical_rival = CAS` for a mutual Reconquista frontier rivalry. No broader diplomacy system was added.

## Vanilla Content Risks

The Iberian Wedding event (`flavor_spa.3716`) is disabled in the Project Crown `events/FlavorSPA.txt` override because it is an early forced dynastic unification path and conflicts with the Phase 2A scope.

Spanish, Aragonese, Portuguese, and Granadan mission-tree assumptions remain a known risk from the Phase 1B audit. They were not overhauled in this phase.

## Validation Result

The implemented ownership table is saved at `Tooling/culture_state/audits/iberia_poc_ownership.json`.

Border-cleanliness validation of the implemented table reports:

- 8 countries checked.
- 1 country with disconnected ownership: `CAT`, due only to the accepted Balearic island exception.
- 0 province-snake warnings.
- `CAS`, `ARA`, `LON`, `GAL`, `NAV`, `GRA`, and `POR` are connected by land under the validator.

The Project Crown map validator was run after implementation. It still reports zero undefined province pixels and no missing province IDs in `provinces.bmp`.

JSON audit files were parsed successfully. EU4 text files received lightweight brace-balance validation.

## Intentionally Not Implemented

- No map edits.
- No flag import.
- No new tags.
- No non-Iberian region overhaul.
- No Tier 1 culture-unification events or missions.
- No broad contested-province registry implementation.
- No broad diplomacy system.
- No hostile intervention / Back War Effort.
- No rare dynastic or diplomatic unification events.
- No colonial proxy wars or parent-escalation system.
- No development rebalance.
- No colonial-region work.

## Test Plan

1. Run `python3 Tooling/validate_project_crown_map.py --summary-json Tooling/project_crown_map_validation_summary.json`.
2. Run `python3 Tooling/culture_state/validate_border_cleanliness.py --ownership-json Tooling/culture_state/audits/iberia_poc_ownership.json --output Tooling/culture_state/audits/iberia_poc_border_cleanliness_validation.json`.
3. Parse all JSON audit files under `Tooling/culture_state/audits/`.
4. Run lightweight brace validation for changed EU4 `.txt` files.
5. Launch EU4 with Project Crown and verify the 1444 Iberian map visually.
6. Run an observer game to check Iberian consolidation pace and vanilla-content misfires.
