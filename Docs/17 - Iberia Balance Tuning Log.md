# Project Crown: Iberia Balance Tuning Log

**Date:** 2026-07-08
**Branch:** `iberia-poc-polish`
**Scope:** Phase 2D Iberia balance tuning after the first observer run.

## First Observer Result

The first post-crash Iberia observer run reached **1489** without reproducing the earlier 1446 crash. By 1489, Castile had expanded quickly, Granada had expanded quickly, and Andalusia had formed.

This is one observer result, not a full balance sample. It is enough to justify a narrow Andalusia formable pacing fix, but not enough to justify province redistribution, development rebalance, broad diplomacy changes, minor fort buffs, or non-Iberian work.

## Diagnosis

The fastest confirmed acceleration path is the inherited vanilla Andalusia decision, not a Project Crown claim layer.

Project Crown Granada starts with all ten mandatory vanilla Andalusia core provinces:

- Murcia (`221`)
- Almeria (`222`)
- Granada (`223`)
- Andalucia (`224`)
- Cordoba (`225`)
- Gibraltar (`226`)
- Jaen (`1748`)
- Cadiz (`1749`)
- Albacete (`4547`)
- Huelva (`4548`)

Vanilla Andalusia then required either the western flank pair, Beja (`229`) and Algarve (`230`), or the eastern flank pair, Alicante (`1750`) and Xativa (`4549`). In the Project Crown setup, that meant Granada could form Andalusia after conquering only Beja and Algarve from small Al-Gharb, or only Alicante and Xativa from Catalonia.

Granada is strong at 109 development, but it does not start with broad outgoing claims. Castile is similarly strong at 110 development and keeps Portugal as a historical friend. Portugal and Al-Gharb have restrained local claims only. Spain formation is not the source of the acceleration because Granada and Andalusia are excluded from the Project Crown Spain decision.

## Changes Applied

Gameplay files changed: **yes**.

Added `Mod Build/project_crown/decisions/AndalusianNation.txt` as a Project Crown override of the vanilla Andalusia decision.

The override keeps the vanilla decision's potential, effects, rewards, AI willingness, tag switch, mission swap, claims, and government handling. The only balance change is the final formation geography gate:

- Before: required Beja/Algarve **or** Alicante/Xativa.
- After: requires Beja/Algarve **and** Alicante/Xativa.

This keeps Granada's Andalusia path available, but makes it require meaningful western and eastern consolidation rather than one small early war.

No Spain formation changes were made. No starting claims, rivalries, friendships, forts, country histories, province ownership, development, map files, localisation, flags, or non-Iberian regions were changed.

## Risks

The new gate may delay Andalusia too much if Granada cannot reliably expand east against Catalonia. If later observer runs show Granada collapsing too often, the next response should be cautious and evidence-led.

Castile and Catalonia may still be repeat snowball winners. If so, the safer next levers are restrained diplomacy or minor survival tuning after repeat observer data, not immediate province redistribution.

Portugal and Al-Gharb still need observer confirmation. Their local claims and forts were left untouched because the first run does not prove either side is structurally broken.

## Validation

Validation passed after the gameplay change:

- EU4 text brace validation: 78 Project Crown `.txt` files checked, 0 brace-balance errors.
- JSON parse validation: 34 Tooling JSON files parsed successfully.
- Owner/controller consistency: 62 province overrides checked, 0 mismatches.
- Border-cleanliness validator: passed with the existing Catalonia/Balearics island exception.
- Map validator quick check: passed with 0 undefined province pixels and no missing vanilla-defined province IDs.
- Andalusia flank-gate check: `230`, `229`, `1750`, and `4549` are all required as owned core provinces in the Project Crown override.

Localisation was not touched.

## Recommended Next Observer Test

Run at least two Iberia-focused observer games from 1444.11.11 with checkpoints at 1500 and 1550. A 1650 checkpoint is useful if the run remains stable.

At 1500, record:

- Whether Andalusia exists.
- Whether Granada exists.
- Which Iberian countries are the top three by province count.
- Whether Portugal and Al-Gharb still exist.
- Whether Granada owns and cores both Beja/Algarve and Alicante/Xativa.

At 1550, record:

- Number of independent Iberian powers.
- Whether Iberia has consolidated toward roughly 2-4 meaningful states.
- Whether Castile, Granada, or Catalonia is a repeat runaway.
- Whether Portugal remains outside Spain or Andalusia.
- Border cleanliness after early wars.

At 1650, record whether Spain formed, whether its timing is plausible, and whether Portugal usually remains independent from Spain.

## Wait For More Data

Do not tune Iberian province ownership, development values, minor forts, broad diplomacy, or mission trees from this single observer result alone.

Do not touch Africa, Asia, Australia, the Americas, or the Philippines in this phase. Those remain future open-region work.

No map files were edited, no non-Iberian region was overhauled, and no Africa/Asia/Australia/Philippines files were changed.
