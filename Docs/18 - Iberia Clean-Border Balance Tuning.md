# Project Crown: Iberia Clean-Border Balance Tuning

**Date:** 2026-07-09
**Branch:** `iberia-poc-polish`
**Scope:** Phase 2E Iberia balance and clean-border tuning after observer feedback, plus limited Atlantic-island start cleanup.

## Observer Feedback Summary

Observer testing after the Phase 2D Andalusia requirement patch remained stable, but the balance read was still rough:

- Castile dominated much of Iberia.
- Portugal took some southern Spanish land.
- Castile took some Portuguese land.
- Some early-war borders looked ugly.
- Castile and Portugal started with Atlantic islands such as Tenerife, Canarias, Madeira, and the Azores through inherited vanilla province history.
- Castile began colonizing in Africa.
- Portugal colonized Brazil and conquered Morocco.

The user clarified that aggressive Iberian gameplay is good. The target is not static peace; it is a fairer, more legible contest where Castile, Portugal, Granada, Al-Gharb, and the other Iberian states can win through alliances, claims, wars, and planning.

## Ugly-Border Diagnosis

Project Crown itself is not currently giving broad early conquest claims across Iberia.

- Castile starts with no Project Crown claims on Portugal or Granada.
- Granada starts with no Project Crown claims.
- Portugal starts with local claims only on Al-Gharb: Beja (`229`), Algarve (`230`), and Evora (`4150`).
- Al-Gharb starts with only one local claim on Lisboa (`227`).
- Spain formation still excludes `alentejo_area` and `beieras_area`, so Spain does not receive Project Crown permanent claims on Portugal or Al-Gharb.

The ugly borders are therefore most likely from normal AI opportunism, war participation, fabrication after first conquests, and still-live vanilla missions rather than a Project Crown starting-claim layer.

## Castile And Portugal

Castile taking Portuguese land is not encouraged by Project Crown claims. Castile and Portugal already have mutual historical friendship in country history, and Spain formation does not claim Portugal.

No Castile-Portugal starting alliance was added. That would reduce Castile attacking Portugal directly, but it would also pull Portugal into Castile's offensive wars and could make the observed Portugal-in-southern-Spain problem worse.

No Castile or Portugal claims were added or removed in this pass.

## Portugal In Southern Spain

Portugal has intended claims on Al-Gharb because the Portuguese/Al-Gharb split is part of the POC. If Portugal conquers Al-Gharb, it borders Granada and may fabricate or join wars into southern Spain. That is a normal AI path, but it should be watched for repeated border gore.

Vanilla Portuguese missions also include later Iberian intervention, Morocco, Brazil, Africa, and India paths. Project Crown has no mission overrides yet, so those incentives remain live.

No mission rewrite was made in this phase.

## Muslim-Nation Viability

Al-Gharb was the clearest survivability issue: it is small, Muslim, and directly exposed to Portugal. Granada is strong, but without a relationship seed the two Muslim Iberian states can be isolated and eaten separately.

Changes applied:

- Added `historical_friend = AGH` to Granada.
- Added `historical_friend = GRA` to Al-Gharb.
- Added a starting Granada-Al-Gharb alliance in `history/diplomacy/project_crown_iberia.txt`.

This does not block wars. Portugal and Al-Gharb remain historical rivals, and Castile and Granada remain historical rivals. The aim is a real Muslim-Iberian survival chance, not artificial peace.

## Andalusia Formation Review

Phase 2D made Andalusia require both the western flank pair, Beja/Algarve, and the eastern flank pair, Alicante/Xativa. That prevented the fastest one-small-war formation path, but the new feedback clarified that early Andalusia is acceptable when it reflects Muslim-Iberian dominance.

Phase 2E keeps the broad east-west path but adds a dominance path:

- The former must still own and core the core Andalusian block and have Cordoba (`225`) as a state.
- A broad consolidation path still allows formation with Beja (`229`), Algarve (`230`), Alicante (`1750`), and Xativa (`4549`).
- Granada can also form Andalusia if Al-Gharb no longer exists and Granada owns and cores Beja, Algarve, and Evora (`4150`).
- Al-Gharb is now eligible to form Andalusia if it conquers and cores the required Granadan Andalusian block, Granada no longer exists, and it holds its home block.

This keeps Andalusia possible earlier than Phase 2D while still requiring more than an isolated border snip.

## Atlantic Island Cleanup

The user explicitly asked for Atlantic islands not to start owned by Castile or Portugal. This phase adds a limited island exception and does not open the full colonial-region phase.

Changed to unowned/uncolonized at 1444:

- The Canarias (`366`), previously inherited as Castile-owned.
- Tenerife (`4565`), previously inherited as Castile-owned.
- The Azores (`367`), previously inherited as Portugal-owned.
- Madeira (`368`), previously inherited as Portugal-owned.

Cape Verde (`1096`) was audited and left unchanged because vanilla already has it unowned at the 1444 start.

The overrides preserve native/uncolonized setup at 1444 and keep future dated ownership blocks for later bookmarks where appropriate. No map files were edited.

## Overseas Expansion Watch

Castile colonizing Africa and Portugal colonizing Brazil are most likely vanilla Exploration, mission, range, and AI behavior. The inherited Atlantic island ownership probably helped range before this pass, so removing the starting islands is a small, safe first step.

Portugal conquering Morocco is also vanilla-supported: Portuguese mission content includes Tangiers and Moroccan follow-up claims. That direction is not automatically wrong for Portugal, so it was documented rather than disabled.

No global colonization system, idea-group rewrite, mission-tree rewrite, mainland Africa clearing, or Americas clearing was implemented.

## Changes Applied

Gameplay files changed: **yes**.

- Added four Atlantic island province-history overrides.
- Added one Project Crown Iberian diplomacy file.
- Added mutual Granada/Al-Gharb historical friendship.
- Tuned Andalusia formation logic for Muslim-Iberian dominance.

No Iberian mainland province ownership, development, fort placement, localisation, map files, flags, or mission files were changed.

## Deferred

- Full colonization gating.
- Full Portuguese, Castilian, Spanish, and Granadan mission-tree redesign.
- Any mainland Africa or Americas clearing.
- Any Asia, Australia, or Philippines clearing.
- Major Iberian province redistribution.
- Major development rebalance.
- Hostile intervention, rare dynastic events, colonial proxy wars, or automatic development.

## Recommended Next Observer Test

Run at least two observer games from 1444.11.11 with checkpoints at 1475, 1500, and 1550.

At each checkpoint, record:

- Whether Castile, Portugal, Granada, Al-Gharb, and Andalusia exist.
- Whether the Granada-Al-Gharb alliance survived, broke naturally, or shaped early wars.
- Whether Portugal takes Granadan southern Spain or mostly focuses on Al-Gharb/Morocco.
- Whether Castile takes Portuguese land despite no Project Crown claims.
- Whether Atlantic islands remain unowned until colonized normally.
- Whether Castile/Portugal still reach Africa or Brazil too early after losing the starting islands.
- Whether borders are cleaner after early wars.

Stop and review before larger changes if Castile still dominates most runs before 1500, if Portugal repeatedly creates southern-Spain border gore, or if the Muslim Iberian alliance makes Granada unstoppable.
