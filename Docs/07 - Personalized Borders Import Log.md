# Phase 1B Import Log - Personalized Borders Foundation

**Date:** 2026-07-06
**Status:** Map foundation imported into Project Crown. Launch testing still required.

## Scope

This phase imported only the province/border map foundation needed to test Project Crown against EU4 v1.37.5.0 Inca:

- `Mod Build/project_crown/map/provinces.bmp`
- `Mod Build/project_crown/map/positions.txt`

No `definition.csv`, `default.map`, `adjacencies.csv`, area/region/superregion files, history files, missions, decisions, events, ideas, subject types, colonial regions, claims, forts, Back War Effort, assimilation, or other non-map gameplay mechanics were implemented.

## Inputs

- Reference mod: Personalized Borders: Fixes & Historical Borders
- Workshop ID: `3418818231`
- Reference path: `/Users/roman/Library/Application Support/Steam/steamapps/workshop/content/236850/3418818231`
- Vanilla EU4 path: `/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV`
- Vanilla target: EU4 v1.37.5.0 Inca

The reference and vanilla files were read only. No base EU4 files and no Workshop/reference mod files were edited.

## Tooling

Created `Tooling/validate_project_crown_map.py`.

The tool:

- Reads EU4 24-bit `provinces.bmp` files without external Python packages.
- Loads vanilla `map/definition.csv` as the valid province color table.
- Detects colors in the imported bitmap that are not defined by vanilla.
- Replaces undefined pixels with the nearest valid neighboring province color.
- Reports vanilla province colors present in vanilla but absent from the imported bitmap.
- Parses and merges `positions.txt` province blocks.
- Preserves Personalized Borders position blocks where present.
- Uses vanilla EU4 v1.37.5 position blocks as fallback for missing IDs.

Generated audit outputs:

- `Tooling/project_crown_map_import_summary.json`
- `Tooling/project_crown_map_validation_summary.json`

## `provinces.bmp`

Import strategy:

1. Started from the reference `map/provinces.bmp`.
2. Kept vanilla EU4 `definition.csv` unchanged.
3. Fixed undefined pixels by replacing each undefined color with the nearest vanilla-defined neighboring province color.
4. Wrote the cleaned bitmap to `Mod Build/project_crown/map/provinces.bmp`.

Validation results:

- Reference dimensions: `5632 x 2048`
- Vanilla dimensions: `5632 x 2048`
- Undefined pixels before fix: `19`
- Undefined pixels after fix: `0`
- Imported unique colors after fix: `3911`

Undefined colors fixed:

| Undefined color | Pixel count |
|---|---:|
| `0,0,0` | 11 |
| `17,118,128` | 1 |
| `104,166,108` | 1 |
| `112,162,24` | 1 |
| `124,253,253` | 1 |
| `127,83,238` | 1 |
| `151,253,253` | 2 |
| `255,255,255` | 1 |

Replacement targets:

| Replacement province ID | Replacement name | Pixels |
|---:|---|---:|
| 767 | Wystruc | 1 |
| 1324 | Eastern Black Sea | 3 |
| 1561 | Coast of Alaska | 4 |
| 2196 | Guria | 6 |
| 2418 | Ukek | 2 |
| 4113 | Uleaborg | 1 |
| 4124 | Kexholm | 2 |

## Missing Vanilla Province Colors

The cleaned bitmap still omits 14 vanilla-defined province colors that are present in vanilla `provinces.bmp`.

These were not guessed back into the bitmap. Reintroducing them safely would require a verified reference shape or deliberate accompanying changes to map definitions and related map data. Adding one-pixel placeholders or inventing province shapes would make the map foundation less reliable.

Remaining absent IDs:

| ID | Name | Vanilla pixels |
|---:|---|---:|
| 214 | Zaragoza | 322 |
| 263 | Ratibor | 224 |
| 264 | Breslau | 301 |
| 881 | Piro | 899 |
| 1088 | Wergaia | 2016 |
| 2292 | Moshi | 743 |
| 2936 | Guyana | 8160 |
| 4156 | Caucasus | 633 |
| 4157 | The Alps | 130 |
| 4160 | Alps3 | 173 |
| 4161 | Alps4 | 178 |
| 4328 | Chagai | 3106 |
| 4763 | Alps6 | 69 |
| 4922 | Pepikokia | 624 |

This is the main remaining map-foundation risk to check in EU4 logs and in-game launch testing.

## `positions.txt`

Import strategy:

1. Started from the reference `map/positions.txt`.
2. Parsed province position blocks by province ID.
3. Preserved Personalized Borders blocks wherever the reference file provided them.
4. Filled missing IDs from vanilla EU4 v1.37.5 `map/positions.txt`.
5. Wrote the merged file to `Mod Build/project_crown/map/positions.txt`.

Merge results:

- Reference position blocks: `4789`
- Vanilla position blocks: `4941`
- Project Crown merged position blocks: `4941`
- Added from vanilla: `152`
- Added ID range: `4790-4941`
- Shared blocks that differ from vanilla and were preserved from Personalized Borders: `390`
- Merged line count: `59,292`

## `replace_path`

No `replace_path` entries were added.

The current import supplies direct map file overrides for `map/provinces.bmp` and `map/positions.txt`. If launch testing shows EU4 is not loading these overrides correctly, consider a targeted descriptor update only after documenting the exact launcher/load behavior.

## Deployment

The Project Crown mod folder was synced after this import to:

`/Users/roman/Documents/Paradox Interactive/Europa Universalis IV/mod/project_crown/`

The launcher descriptor was also synced to:

`/Users/roman/Documents/Paradox Interactive/Europa Universalis IV/mod/project_crown.mod`

## Next Test Steps

1. Launch EU4 v1.37.5.0 Inca with Project Crown enabled.
2. Confirm Project Crown loads with only this map foundation change active.
3. Review EU4 logs for unknown color, missing province, missing position, adjacency, and map-cache errors.
4. Start a 1444 game and inspect changed border regions.
5. Specifically check the 14 absent-ID areas listed above.
6. Do not proceed to no-straits, development rebalance, colonial regions, subjects, missions, claims, forts, Back War Effort, or assimilation until the map foundation loads correctly.

## Phase 1B Non-Implementation Statement

No non-map gameplay mechanics were implemented. No base EU4 files were edited. No Workshop/reference mod files were edited. No Project Pace files were touched.
