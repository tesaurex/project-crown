# Phase 1B.1 Merge Log - Vanilla European Impassables

**Date:** 2026-07-06
**Status:** Vanilla European impassable/wasteland shapes restored into the Project Crown map foundation. Launch testing still required.

## Scope

This phase kept the Personalized Borders province/border foundation and restored vanilla EU4 impassable/wasteland land for Europe and European-adjacent barriers.

Updated file:

- `Mod Build/project_crown/map/provinces.bmp`

No `definition.csv`, `default.map`, `terrain.txt`, `climate.txt`, `positions.txt`, `adjacencies.csv`, history files, missions, decisions, events, ideas, subject types, colonial regions, claims, forts, Back War Effort, assimilation, or other non-map gameplay mechanics were changed.

## Identification Method

The vanilla EU4 v1.37.5 files were inspected read-only from:

`/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV`

The restored IDs were identified by intersecting:

- `map/continent.txt` block `europe`
- `map/climate.txt` block `impassable`
- Vanilla `map/definition.csv` province colors/names

This produced the vanilla European impassable/wasteland set used for the merge.

## Identified And Restored IDs

| ID | Name | Vanilla pixels | Project pixels before | Project pixels after |
|---:|---|---:|---:|---:|
| 2425 | Naryan-Mar | 34,781 | 35,305 | 34,781 |
| 4146 | Jotenheimen | 2,760 | 2,760 | 2,760 |
| 4153 | Scandes | 2,664 | 11 | 2,664 |
| 4154 | Pyrenees | 259 | 10 | 259 |
| 4155 | Carpathians | 563 | 13 | 563 |
| 4156 | Caucasus | 633 | 0 | 633 |
| 4157 | The Alps | 130 | 0 | 130 |
| 4159 | Alps2 | 119 | 13 | 119 |
| 4160 | Alps3 | 173 | 0 | 173 |
| 4161 | Alps4 | 178 | 0 | 178 |
| 4162 | Alps5 | 76 | 5 | 76 |
| 4178 | Pontic Mountains | 257 | 257 | 257 |
| 4763 | Alps6 | 69 | 0 | 69 |

All 13 identified IDs now match vanilla pixel counts in Project Crown.

## Merge Strategy

`Tooling/validate_project_crown_map.py` was extended with `--restore-vanilla-european-impassables`.

The tool:

1. Loads vanilla `definition.csv`.
2. Identifies European impassable IDs from vanilla `continent.txt` and `climate.txt`.
3. Compares vanilla `provinces.bmp` with Project Crown `provinces.bmp`.
4. For any pixel where either vanilla or Project Crown has one of the target impassable colors, writes the vanilla pixel color into Project Crown.
5. Leaves the rest of the Personalized Borders bitmap unchanged.

This restores the exact vanilla barrier masks rather than adding isolated placeholder pixels.

Pixels changed: `5,428`

Target barrier pixels restored:

| ID | Name | Pixels restored to target color |
|---:|---|---:|
| 4153 | Scandes | 2,664 |
| 4154 | Pyrenees | 259 |
| 4155 | Carpathians | 563 |
| 4156 | Caucasus | 633 |
| 4157 | The Alps | 130 |
| 4159 | Alps2 | 119 |
| 4160 | Alps3 | 173 |
| 4161 | Alps4 | 178 |
| 4162 | Alps5 | 76 |
| 4763 | Alps6 | 69 |

Some pixels that were extra Project Crown/PB impassable-color spillover were restored to their vanilla non-target neighboring colors:

| ID | Name | Pixels |
|---:|---|---:|
| 102 | Nice | 11 |
| 113 | Ferrara | 10 |
| 118 | Roma | 5 |
| 1873 | Chur | 13 |
| 2426 | Yamal | 524 |
| 4694 | Foix | 1 |

## Regional Results

- Pyrenees: restored. Province `4154 Pyrenees` now has the vanilla `259` pixels.
- Alps: restored. Provinces `4157 The Alps`, `4159 Alps2`, `4160 Alps3`, `4161 Alps4`, `4162 Alps5`, and `4763 Alps6` now match vanilla pixel counts.
- Caucasus: restored. Province `4156 Caucasus` now has the vanilla `633` pixels.
- Scandes/Jotenheimen: restored or verified. `4153 Scandes` was restored; `4146 Jotenheimen` already matched vanilla.
- Carpathians: restored. Province `4155 Carpathians` now has the vanilla `563` pixels.
- Pontic Mountains: verified. Province `4178 Pontic Mountains` already matched vanilla.
- Naryan-Mar/Yamal edge: restored to the vanilla Europe/Asia impassable boundary.

## Validation

Validation command:

```text
python3 Tooling/validate_project_crown_map.py --summary-json Tooling/project_crown_map_validation_summary.json
```

Audit command:

```text
python3 Tooling/validate_project_crown_map.py --restore-vanilla-european-impassables --summary-json Tooling/project_crown_european_impassables_summary.json
```

Results:

- Bitmap dimensions: `5632 x 2048`
- Undefined colors after restore: `0`
- Project position blocks: `4,941`
- Vanilla position blocks: `4,941`
- `positions.txt` update needed: no

## Remaining Missing Vanilla Province Colors

Remaining absent IDs after the restore:

| ID | Name | Status |
|---:|---|---|
| 214 | Zaragoza | European, not vanilla impassable. Left unchanged. |
| 263 | Ratibor | European, not vanilla impassable. Left unchanged. |
| 264 | Breslau | European, not vanilla impassable. Left unchanged. |
| 881 | Piro | Non-European, not vanilla impassable. Left unchanged. |
| 1088 | Wergaia | Non-European, not vanilla impassable. Left unchanged. |
| 2292 | Moshi | Non-European, not vanilla impassable. Left unchanged. |
| 2936 | Guyana | Non-European vanilla impassable. Left unchanged by this Europe-only phase. |
| 4328 | Chagai | Non-European vanilla impassable. Left unchanged by this Europe-only phase. |
| 4922 | Pepikokia | Non-European, not vanilla impassable. Left unchanged. |

The missing European Alps/Caucasus IDs from Phase 1B are resolved: `4156`, `4157`, `4160`, `4161`, and `4763` are no longer missing.

## Map Risks

- This merge intentionally restores vanilla barrier masks inside the affected regions, so some local Personalized Borders edits around those barriers are partially overwritten.
- Non-European missing impassables `2936 Guyana` and `4328 Chagai` remain unresolved because this phase was scoped to Europe and European-adjacent barriers.
- Launch testing should inspect the Pyrenees, Alps, Caucasus, Scandes, Carpathians, Pontic Mountains, and the Naryan-Mar/Yamal boundary.

## Deployment

The Project Crown mod folder was synced after this merge to:

`/Users/roman/Documents/Paradox Interactive/Europa Universalis IV/mod/project_crown/`

The launcher descriptor was also synced to:

`/Users/roman/Documents/Paradox Interactive/Europa Universalis IV/mod/project_crown.mod`

## Phase 1B.1 Non-Implementation Statement

No non-map gameplay mechanics were implemented. No base EU4 files were edited. No Workshop/reference mod files were edited. No Project Pace files were touched.
