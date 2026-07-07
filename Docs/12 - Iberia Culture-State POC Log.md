# Project Crown: Iberia Culture-State POC Log

**Date:** 2026-07-07
**Status:** Phase 2A implemented for Iberia only. Phase 2A.1 polish added a southern Portuguese Muslim rival and cleaned up Caceres. Phase 2A.2 fixed Al-Gharb localisation and Evora religion after visual QA. Phase 2A.3 fixed Catalonia's country-selection occupation preview. Phase 2A.4 removed a tiny Catalonia/Pyrenees visual sliver.

## Scope

This phase implements the first playable Culture-State World region: Iberia. It uses vanilla reuse tags where available, one Project Crown custom tag for the southern Portuguese rival, and Project Crown history-file overrides. Phase 2A.4 makes one targeted four-pixel `provinces.bmp` cleanup at the Pyrenees/Catalonia/Foix boundary; no province IDs, `definition.csv`, imported flags, non-Iberian province histories, hostile intervention mechanics, rare dynastic unification events, or colonial proxy-war systems were implemented.

## Pre-Flight

- Working folder confirmed: `/Users/roman/Desktop/Project Crown`
- Phase 2A branch confirmed: `iberia-poc`
- Phase 2A.1 polish branch confirmed: `iberia-poc-polish`
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
| `AGH` | Al-Gharb / southern Portuguese Muslim rival | `portugese` | Algarve (`230`) |

## Province Ownership Approach

Ownership follows the Phase 1B Iberia culture audit for all Iberian land provinces except Caceres and the Phase 2A.1 southern Portuguese split. Each Iberian province history override preserves vanilla development, trade goods, discovery, and future dated bookmark history while replacing the 1444 top-level `owner`, `controller`, and core setup where needed.

Summary:

| Tag | Province count | Province IDs |
|---|---:|---|
| `AGH` | 3 | 229, 230, 4150 |
| `CAS` | 13 | 215, 217, 219, 1745, 1746, 1747, 2751, 2754, 2755, 2989, 4551, 4552, 4789 |
| `ARA` | 4 | 211, 214, 2990, 4557 |
| `CAT` | 12 | 197, 212, 213, 220, 333, 1750, 2987, 2988, 4549, 4550, 4559, 4560 |
| `LON` | 5 | 207, 208, 216, 4553, 4788 |
| `GAL` | 4 | 206, 4554, 4555, 4558 |
| `NAV` | 2 | 209, 210 |
| `GRA` | 12 | 218, 221, 222, 223, 224, 225, 226, 1748, 1749, 4546, 4547, 4548 |
| `POR` | 7 | 227, 228, 231, 232, 1851, 4556, 4787 |

## Cores and Claims

Each culture-state has 1444 cores on its starting provinces. Caceres (`1747`) is owned and cored by Castile and no longer carries a Leon core. Al-Gharb (`AGH`) cores Beja (`229`), Algarve (`230`), and Evora (`4150`). Portugal keeps cores on Lisboa and northern Portugal, but not on the southern rival block.

Restrained regular claims were added only for the Portuguese split: Portugal has claims on Beja, Algarve, and Evora; Al-Gharb has a single claim on Lisboa and no claims on northern Portugal. No broad permanent-claim layer, mission ladder, contested-region system, or group-claim system was implemented in this phase. Spain formation grants permanent claims on the vanilla `iberia_region` except `alentejo_area` and `beieras_area`, preserving the owner rule that Portugal is not required for Spain and should not be casually absorbed.

Phase 2A.2 fixed the AGH country localisation so the tag displays as Al-Gharb with adjective Al-Gharbi. The Iberia localisation file uses the EU4-compatible `l_english:` header, one-space entries, and UTF-8 BOM encoding.

## Southern Portuguese Rival Decision

Vanilla was checked first. `ADU`, `GRA`, and `ALG` exist, but they represent Andalusia, Granada, and Algiers rather than a southern Portuguese Algarve/Gharb state. Project Crown therefore adds custom tag `AGH`, localized as Al-Gharb.

Al-Gharb is a Portuguese-culture Muslim rival, not a North African transplant:

- Primary culture: `portugese`
- Religion: `sunni`
- Capital: Algarve (`230`)
- Starting provinces: Beja (`229`), Algarve (`230`), Evora (`4150`)
- Religion in the southern block: Beja and Algarve are Sunni; Evora remains Catholic while owned and cored by Al-Gharb.
- Lisboa (`227`) remains Portuguese, Catholic, and owned by Portugal.
- Northern Portugal remains Catholic and owned by Portugal: Beira (`228`), Porto (`231`), Braganca (`232`), Coimbra (`1851`), Aviero (`4556`), Ribatejo (`4787`).

`AGH` and `POR` are seeded as historical rivals. `AGH` uses an original placeholder flag generated for this custom tag; no outside flag pack was imported.

## Aragon Primary Culture Decision

Vanilla `ARA - Aragon.txt` uses `primary_culture = catalan` and `capital = 213`. Project Crown overrides Aragon as the Aragonese staple:

- `primary_culture = aragonese`
- `capital = 214` (Zaragoza)
- `add_accepted_culture = catalan`

`CAT` remains the Catalan culture-state with Barcelona as capital.

## CAT Island Decision

Catalonia keeps the Balearic island provinces (`333`, `4559`, `4560`). The border validator reports them as disconnected land components, but this is accepted as an O7 island exception: the islands are Catalan-culture, historically/geographically reasonable, and do not create mainland border gore.

## Catalonia Starting Controller Fix

Phase 2A.3 fixed the country-selection preview where Catalonia appeared occupied by Aragon. The cause was not the top-level 1444 owner/controller lines, which already said `owner = CAT` and `controller = CAT`; it was pre-1444 dated vanilla history that reset the effective 1444 controller back to Aragon in five Catalan mainland provinces.

Fixed files:

- Roussillon (`197`)
- Girona (`212`)
- Barcelona (`213`)
- Urgell (`2987`)
- Tarragona (`2988`)

Each now resolves to `owner = CAT`, `controller = CAT`, and `add_core = CAT` at the 1444 start. The rest of the CAT-owned mainland provinces and Balearic island provinces were checked and already matched. A full Iberian owner/controller consistency check found 62 Iberian province history overrides and 0 remaining owner/controller mismatches at the 1444 start. No Iberian starting occupations are intentional in this POC.

## Pyrenees/Catalonia Sliver Fix

Phase 2A.4 visual QA found a tiny Catalonia-colored sliver north of the Pyrenees wasteland near the Foix/Urgell boundary. Programmatic bitmap inspection identified it as a detached four-pixel component of Urgell (`2987`, color `[220, 251, 47]`) at pixels `(2813,670)`, `(2814,670)`, `(2815,670)`, and `(2813,671)`.

Those exact pixels are Foix (`4694`, color `[172, 194, 112]`) in vanilla and sit on the French side of the Pyrenees barrier. The fix replaces only those four pixels with Foix. Urgell now has one bitmap component, Pyrenees (`4154`) remains unchanged at 259 pixels, and the immediate sliver neighborhood has no remaining differences from vanilla. No province IDs, `definition.csv`, country history, province history, diplomacy, or gameplay systems were changed.

The audit is saved at `Tooling/culture_state/audits/pyrenees_catalonia_sliver_fix.json`.

## Caceres Decision

Caceres (`1747`) is Leonese culture but creates an isolated Leonese component under raw culture ownership. The tested alternatives were:

- Leon ownership: disconnected Leonese start.
- Granada ownership: disconnected Granadan component.
- Castile ownership: all mainland Iberian countries connected except the accepted Catalan islands.

Phase 2A.1 keeps Caceres owned by Castile, changes its culture to `castillian`, and removes the Leon core. This is a border-cleanliness and culture-readability fix: Caceres does not border Leon in the current setup and should not imply a stranded Leonese component.

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

Diplomacy changes are intentionally minimal. Vanilla Castile-Granada rivalry and Castile-Portugal friendship are preserved through copied country history. Granada has `historical_rival = CAS` for a mutual Reconquista frontier rivalry. Phase 2A.1 adds only the local `POR`/`AGH` historical rivalry. No broader diplomacy system was added.

## Vanilla Content Risks

The Iberian Wedding event (`flavor_spa.3716`) is disabled in the Project Crown `events/FlavorSPA.txt` override because it is an early forced dynastic unification path and conflicts with the Phase 2A scope.

Spanish, Aragonese, Portuguese, and Granadan mission-tree assumptions remain a known risk from the Phase 1B audit. They were not overhauled in this phase.

## Validation Result

The implemented ownership table is saved at `Tooling/culture_state/audits/iberia_ownership_implemented.json` and mirrored in `Tooling/culture_state/audits/iberia_poc_ownership.json`.

Border-cleanliness validation of the implemented table reports:

- 9 countries checked.
- 1 country with disconnected ownership: `CAT`, due only to the accepted Balearic island exception.
- 0 province-snake warnings.
- `AGH`, `CAS`, `ARA`, `LON`, `GAL`, `NAV`, `GRA`, and `POR` are connected by land under the validator.

The Project Crown map validator was run after implementation and again after the Phase 2A.4 sliver cleanup. It reports zero undefined province pixels and no missing vanilla-defined province IDs in `provinces.bmp`.

All culture-state audit JSON files parsed successfully. Touched EU4 `.txt` files passed lightweight brace-balance validation. `crown_iberia_l_english.yml` passed localisation header and one-space indentation validation. Phase 2A.3 added and ran an Iberian owner/controller consistency check: 62 province history overrides checked, 0 remaining 1444 owner/controller mismatches.

## Intentionally Not Implemented

- No broad map edits; Phase 2A.4 changed only four `provinces.bmp` pixels at the Pyrenees/Catalonia/Foix boundary.
- No outside flag imports; `AGH` uses an original placeholder flag.
- No non-Iberian region overhaul.
- No Tier 1 culture-unification events or missions.
- No broad contested-province registry implementation.
- No broad diplomacy system.
- No diplomacy-history or active-war edits.
- No hostile intervention / Back War Effort.
- No rare dynastic or diplomatic unification events.
- No colonial proxy wars or parent-escalation system.
- No development rebalance.
- No colonial-region work.

## Test Plan

1. Run `python3 Tooling/validate_project_crown_map.py --summary-json Tooling/project_crown_map_validation_summary.json`.
2. Run `python3 Tooling/culture_state/validate_border_cleanliness.py --ownership-json Tooling/culture_state/audits/iberia_ownership_implemented.json --output Tooling/culture_state/audits/iberia_border_cleanliness_validation.json`.
3. Parse all JSON audit files under `Tooling/culture_state/audits/`.
4. Run lightweight brace validation for changed EU4 `.txt` files.
5. Launch EU4 with Project Crown and verify the 1444 Iberian map visually.
6. Run an observer game to check Iberian consolidation pace and vanilla-content misfires.
