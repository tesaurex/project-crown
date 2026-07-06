# Phase 1B.2 Resolution Log - Remaining Province IDs

**Date:** 2026-07-06
**Status:** Remaining missing vanilla-defined province colors resolved.

## Scope

This phase stayed within map foundation work. It investigated and resolved the nine vanilla-defined province colors still absent after importing Personalized Borders and restoring vanilla European impassables.

Updated files:

- `Mod Build/project_crown/map/provinces.bmp`
- `Tooling/validate_project_crown_map.py`
- `Tooling/project_crown_map_validation_summary.json`
- `Tooling/project_crown_remaining_missing_ids_audit.json`
- `Tooling/project_crown_remaining_missing_ids_restore_summary.json`
- `Docs/07 - Personalized Borders Import Log.md`
- `Docs/08 - Vanilla European Impassables Merge Log.md`
- `Docs/09 - Remaining Province ID Resolution Log.md`

Not changed:

- `definition.csv`
- `default.map`
- `terrain.txt`
- `climate.txt`
- `positions.txt`
- Province history
- Areas, regions, superregions
- Adjacencies or straits
- Any non-map gameplay mechanics

## Inputs

Vanilla EU4 v1.37.5 files were inspected read-only from:

`/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV`

Reference Personalized Borders files were inspected read-only from:

`/Users/roman/Library/Application Support/Steam/steamapps/workshop/content/236850/3418818231`

No base EU4 files and no Workshop/reference mod files were edited.

## Method

`Tooling/validate_project_crown_map.py` was extended to audit remaining missing IDs.

The audit now reports, for each target ID:

- Vanilla definition color and name.
- Vanilla type from `default.map` and `climate.txt`.
- Vanilla continent, area, region, and superregion where available.
- Terrain override from `terrain.txt` where available.
- Vanilla shape pixel count, bounding box, and centroid.
- The Project Crown province IDs currently covering the vanilla shape.
- The Personalized Borders reference province IDs covering the vanilla shape.
- Vanilla adjacent province IDs.

The restore command overlays exact vanilla province-color masks for explicit IDs only. It does not invent colors or shapes.

## Decision Criteria

The nine missing IDs were absent in both the Personalized Borders reference bitmap and the Project Crown bitmap, while Project Crown still inherits vanilla `definition.csv`, `default.map`, `climate.txt`, area/region data, and province history.

For normal land provinces, leaving them absent would keep vanilla province history and map metadata pointing at provinces with no map pixels. For impassable/wasteland provinces, leaving them absent would keep inherited vanilla impassable metadata pointing at provinces with no map pixels.

Because no matching Personalized Borders metadata import is in scope, the safe map-foundation choice was to restore exact vanilla shapes for all nine IDs.

## Per-ID Decisions

| ID | Name | Region | Type | Decision | Reason |
|---:|---|---|---|---|---|
| 214 | Zaragoza | `aragon_area`, `iberia_region`, `europe_superregion` | Normal land | Restore from vanilla | Vanilla history, area data, and definition still reference the province. Personalized Borders had merged the shape into Lleida, Pirineo, Urgell, and Teruel, but no matching metadata change exists in Project Crown. |
| 263 | Ratibor | `silesia_area`, `poland_region`, `eastern_europe_superregion` | Normal land | Restore from vanilla | Vanilla HRE/history metadata still references the province. Personalized Borders had merged the shape into Opole, Kalisz, Eger, Sadecki, and Ostrava. |
| 264 | Breslau | `silesia_area`, `poland_region`, `eastern_europe_superregion` | Normal land | Restore from vanilla | Vanilla HRE/history metadata still references the province. Personalized Borders had merged the shape mostly into Liegnitz and Opole. |
| 881 | Piro | `new_mexico_area`, `california_region`, `central_america_superregion` | Normal land | Restore from vanilla | Vanilla native and later colonial history still references the province. Personalized Borders had merged the shape into Acoma, Mescalero, Natahende, and small neighboring fragments. |
| 1088 | Wergaia | `southern_australia_area`, `australia_region`, `oceania_superregion` | Normal land | Restore from vanilla | Vanilla native province data still references the province. Personalized Borders had merged the shape into Woiworung and Waveroo. |
| 2292 | Moshi | `atacora_oueme_area`, `niger_region`, `africa_superregion` | Normal land | Restore from vanilla | Vanilla owner/core/history data still references the province. Personalized Borders had merged the shape into Oyo, Cape Coast, and Borgu. |
| 2936 | Guyana | South America, no vanilla area block | Impassable/wasteland | Restore from vanilla | Vanilla `climate.txt` marks the province impassable. Personalized Borders had merged the shape into surrounding Guiana/Amazon land provinces, but Project Crown still inherits the vanilla impassable ID. |
| 4328 | Chagai | Asia, no vanilla area block | Impassable/wasteland | Restore from vanilla | Vanilla `climate.txt` marks the province impassable. Personalized Borders had merged the shape into Kharan, Quhistan, Bust, Kandahar, Chakhansur, and Sistan. |
| 4922 | Pepikokia | `miami_river_area`, `great_lakes_region`, `north_america_superregion` | Normal land | Restore from vanilla | Vanilla native/history data still references the province. Personalized Borders had merged the shape mostly into Miami and Mascouten. |

## Restore Results

Restored exact vanilla shapes:

| ID | Name | Restored pixels |
|---:|---|---:|
| 214 | Zaragoza | 322 |
| 263 | Ratibor | 224 |
| 264 | Breslau | 301 |
| 881 | Piro | 899 |
| 1088 | Wergaia | 2,016 |
| 2292 | Moshi | 743 |
| 2936 | Guyana | 8,160 |
| 4328 | Chagai | 3,106 |
| 4922 | Pepikokia | 624 |

Total pixels changed: `16,395`.

No province IDs were intentionally left absent.

No province IDs require user visual review before continuing map-foundation work.

## Positions

`positions.txt` was not updated in this phase.

Validation found:

- Project Crown position blocks: `4,941`
- Vanilla position blocks: `4,941`
- Personalized Borders reference position blocks: `4,789`

Project Crown already had position blocks for all restored IDs from the existing Phase 1B merge strategy.

## Validation

Validation command:

```text
python3 Tooling/validate_project_crown_map.py --summary-json Tooling/project_crown_map_validation_summary.json
```

Results:

- Bitmap dimensions: `5632 x 2048`
- Undefined pixel count: `0`
- Imported unique colors: `3,925`
- Remaining missing vanilla-defined province IDs: none

## Remaining Risks

- Restoring exact vanilla shapes necessarily overwrote some Personalized Borders reshaping in Aragon, Silesia, New Mexico, southern Australia, Atacora/Oueme, Guyana, Chagai, and the Miami River area.
- This is intentional for Phase 1B.2 because Project Crown has not imported matching Personalized Borders `definition.csv`, province history, area/region, or climate metadata.
- Future phases that deliberately import broader Personalized Borders metadata may need to revisit these restored shapes.
- Launch testing should still inspect the restored regions in-game for visual seams, province clickability, labels, and map-cache warnings.

## Phase 1B.2 Non-Implementation Statement

No non-map gameplay mechanics were implemented. No development, colonial regions, subject types, missions, claims, events, ideas, forts, Back War Effort, assimilation, or straits were changed.

No base EU4 files were edited. No Workshop/reference mod files were edited. No Project Pace files were touched.
