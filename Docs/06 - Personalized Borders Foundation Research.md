# Phase 1A Research - Personalized Borders Foundation

**Date:** 2026-07-06
**Status:** Research/documentation only. No import or gameplay implementation happened in this phase.

## Target

- **Reference mod:** Personalized Borders: Fixes & Historical Borders
- **Steam Workshop ID:** 3418818231
- **Workshop URL:** https://steamcommunity.com/sharedfiles/filedetails/?id=3418818231
- **Target EU4 version:** v1.37.5.0 Inca
- **Local path inspected:** `/Users/roman/Library/Application Support/Steam/steamapps/workshop/content/236850/3418818231`

## Found Status

The exact Steam Workshop item folder was found at the expected path.

`Reference Mods/` was also checked. It currently contains only `Reference Mods/README.md`; no manually provided copy of Personalized Borders was found there.

## Permission And Credit Note

Per the user's statement, the Project Crown owner knows the relevant mod developer and says permission exists from the relevant creator chain. Project Crown should still keep explicit credit/permission tracking before any publication or redistribution. This phase does not publish, redistribute, copy, or import the reference mod.

## Folder Structure

```text
3418818231/
  descriptor.mod
  thumbnail.png
  map/
    positions.txt
    provinces.bmp
```

## Descriptor

`descriptor.mod` contains:

```text
version="1.37.*"
tags={
	"Map"
	"Historical"
	"Fixes"
}
name="Personalized Borders: Fixes & Historical Borders"
supported_version="v1.37.5.0"
remote_file_id="3418818231"
```

No separate `.mod` launcher file was present inside the Workshop item folder.

## File Presence Checklist

| File or area | Modified by reference mod? | Notes |
|---|---:|---|
| `map/provinces.bmp` | Yes | Present; actual province bitmap override. |
| `map/definition.csv` | No | Not present; vanilla province ID/color definitions are inherited. |
| `map/default.map` | No | Not present; vanilla `max_provinces`, sea/lake lists, and map config are inherited. |
| `map/adjacencies.csv` | No | Not present; vanilla adjacencies are inherited. |
| `map/positions.txt` | Yes | Present; position override. |
| `map/terrain.txt` | No | Not present; vanilla terrain definitions are inherited. |
| `map/continent.txt` | No | Not present; vanilla continent membership is inherited. |
| `common/areas` or `map/area.txt` | No | No area overrides found. EU4 vanilla uses `map/area.txt`. |
| `common/regions` or `map/region.txt` | No | No region overrides found. EU4 vanilla uses `map/region.txt`. |
| `common/superregion` or `map/superregion.txt` | No | No superregion overrides found. EU4 vanilla uses `map/superregion.txt`. |
| `history/provinces` | No | No province-history overrides found. |
| `history/countries` | No | No country-history overrides found. |
| country tags/countries | No | No country/tag overrides found. |
| localisation | No | No localisation overrides found. |
| missions | No | No mission overrides found. |
| decisions | No | No decision overrides found. |
| events | No | No event overrides found. |
| interface | No | No interface overrides found. |

## Technical Findings

The reference mod is a narrow map foundation mod. It changes province shapes and map object placement, not ownership/history/gameplay systems.

### `map/provinces.bmp`

- Reference bitmap dimensions: `5632 x 2048 x 24`.
- Vanilla 1.37.5 bitmap dimensions: `5632 x 2048 x 24`.
- Pixel differences vs vanilla: `917,804 / 11,534,336` pixels, about `7.96%`.
- Reference unique colors: `3,919`.
- Vanilla unique colors: `3,925`.
- The reference mod does **not** include `definition.csv`, so it does not define new province IDs.
- All defined province colors used by the reference bitmap are vanilla-defined colors; no new defined province IDs were detected.
- 14 vanilla bitmap province IDs are present in vanilla `provinces.bmp` but absent from the reference bitmap:
  `214 Zaragoza`, `263 Ratibor`, `264 Breslau`, `881 Piro`, `1088 Wergaia`, `2292 Moshi`, `2936 Guyana`, `4156 Caucasus`, `4157 The Alps`, `4160 Alps3`, `4161 Alps4`, `4328 Chagai`, `4763 Alps6`, `4922 Pepikokia`.
- The reference bitmap contains 8 colors not present in vanilla `definition.csv`, totaling 19 pixels:
  `(0,0,0)` 11 pixels; `(151,253,253)` 2 pixels; `(17,118,128)` 1 pixel; `(127,83,238)` 1 pixel; `(104,166,108)` 1 pixel; `(112,162,24)` 1 pixel; `(255,255,255)` 1 pixel; `(124,253,253)` 1 pixel.

Interpretation: the reference mod appears to redraw borders using vanilla province colors rather than adding a new province-ID schema. However, the absent vanilla IDs and stray undefined pixels must be resolved or explicitly validated before import.

### `map/positions.txt`

- Reference `positions.txt` line count: `57,468`.
- Vanilla 1.37.5 `positions.txt` line count: `59,292`.
- Reference position IDs: 1 through 4789.
- Vanilla position IDs: 1 through 4941.
- No reference position IDs exist outside the vanilla range.
- The reference file is missing vanilla position IDs 4790 through 4941.
- 392 shared position blocks differ from vanilla, indicating intentional object-placement changes for redrawn provinces.

Interpretation: the reference position file is not safe to use as a drop-in Project Crown override without a merge. Project Crown should preserve the 392 intentional Personalized Borders position edits while filling missing 1.37.5 position blocks from vanilla unless a later validator proves those provinces are genuinely unused and safe.

## Compatibility Assessment

The descriptor claims `supported_version="v1.37.5.0"` and `version="1.37.*"`.

Project Crown should not assume the reference files are compatible as-is. The two main compatibility concerns are:

1. `provinces.bmp` has 19 undefined-color pixels and omits 14 vanilla province colors that appear in vanilla 1.37.5.
2. `positions.txt` omits vanilla 1.37.5 province position blocks 4790-4941 even though the reference bitmap still uses many 4790+ province colors.

The safest conclusion is: compatible intent is present in the descriptor, but Project Crown needs a validation/merge pass before adopting the files.

## What Would Need To Be Imported Later

Do not import anything in Phase 1A. If the owner approves the port after this research, the likely import set is:

- `map/provinces.bmp`, after cleaning undefined pixels and resolving absent vanilla province IDs.
- `map/positions.txt`, after merging Personalized Borders edits with vanilla 1.37.5 positions for missing IDs.

The reference mod does not provide these files, so they should not be copied from the reference as part of a Personalized Borders import:

- `map/definition.csv`
- `map/default.map`
- `map/adjacencies.csv`
- `map/terrain.txt`
- `map/continent.txt`
- `map/area.txt`
- `map/region.txt`
- `map/superregion.txt`
- province history
- country history
- tags, countries, localisation, missions, decisions, events, or interface

Project Crown will still later own some of those files for its own systems, but they are not part of this reference mod's provided foundation.

## Likely Compatibility Updates

- Clean or remap the 19 undefined-color pixels in `map/provinces.bmp`.
- Decide whether the 14 absent vanilla province IDs are intentional merges/removals or accidental omissions. If intentional, Project Crown must evaluate whether EU4 accepts those IDs having no pixels while still present in `definition.csv` and `default.map`.
- Merge `positions.txt` with vanilla 1.37.5 so IDs 4790-4941 are present unless proven unnecessary.
- Re-run any future no-straits `adjacencies.csv` generation against the locked Personalized Borders province bitmap, not against the old vanilla assumption.
- Rebuild future development rebalance, colonial regions, home claims, and province lists against the locked foundation.
- Audit terrain, continent, area, region, and superregion membership after the visual border changes, even though the reference mod does not override those files.

## Risks

- Province ID mismatch between the bitmap, vanilla `definition.csv`, vanilla `default.map`, and Project Crown tooling.
- Outdated or partial map files that claim 1.37.5 support but miss newer province-position entries.
- Broken or visually wrong adjacencies if Project Crown later removes straits using assumptions from the old vanilla bitmap.
- Broken positions for cities, units, ports, trade posts, or province names if the reference `positions.txt` is imported without merging.
- Terrain/continent/area/region drift: vanilla data may still work mechanically, but redrawn borders can make later province lists less intuitive.
- Launcher compatibility risk if the Workshop descriptor works in Steam but Project Crown's local descriptor/path setup differs.
- History file drift: Project Crown's future province-history overrides must match the final province IDs and shapes.
- Future development rebalance conflicts if generated history edits assume vanilla province availability or old province lists.
- Future colonial region conflicts if region definitions are drawn before the foundation is locked.
- Permission and credit tracking must remain explicit before publication or redistribution.

## Recommended Import/Port Plan

1. Keep Phase 1A as documentation-only and commit the research.
2. In the next approved phase, create a controlled Project Crown import branch or staging area. Do not edit the Workshop copy.
3. Copy only the required reference files into Project Crown after approval: `map/provinces.bmp` and a staged `positions.txt` merge input.
4. Build or run validators for bitmap dimensions, undefined colors, province color coverage, position ID coverage, and vanilla definition/default-map consistency.
5. Repair or explicitly account for the 19 undefined-color pixels.
6. Resolve the 14 absent vanilla bitmap IDs.
7. Merge positions: keep Personalized Borders changed blocks where intentional, fill missing vanilla 1.37.5 blocks for IDs 4790-4941.
8. Launch EU4 with only the map foundation enabled and inspect logs before adding no-straits, development rebalance, colonial regions, or gameplay systems.
9. Only after the foundation loads cleanly should Project Crown proceed to no-straits, development rebalance, colonial regions, subjects, or any other gameplay layer.

## Recommended Test Plan

- Validate `provinces.bmp` against vanilla `definition.csv`: no unknown colors, expected province ID coverage, correct dimensions, no accidental anti-alias pixels.
- Validate `positions.txt`: all needed province IDs present, changed IDs intentional, missing IDs explained.
- Launch EU4 v1.37.5.0 Inca with the foundation only.
- Review EU4 logs for map errors, unknown colors, missing positions, broken province origins, and adjacency complaints.
- Start a 1444 game and visually inspect high-change regions.
- Click provinces around known changed borders and the 14 absent-ID areas.
- Inspect city/unit/name/port positions in changed regions and in IDs 4790-4941.
- Run a short hands-off observer to confirm no load-time or daily-tick map crash.
- Only then layer Project Crown systems back in one at a time.

## Phase 1A Non-Implementation Statement

No reference files were copied into Project Crown in this phase. No gameplay mechanics were implemented. No base EU4 files, Steam Workshop files, Reference Mods files, deployed user mod files, or Project Pace files were edited.
