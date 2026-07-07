# Project Crown: Europa Ascendant — Phase Plan

**Revised 2026-07-06 for the Culture-State World pivot.** Phases are ordered by dependency and risk: engine-risk research first, world data second, the culture-state political layer third (Iberia proof of concept before any global rollout), systems fourth, balance and flavor last. Each phase has an exit criterion — do not start the next phase's systems until the current one's criterion is met (parallel *research* is always fine).

Status legend: ✅ complete · 🔶 in progress / partially complete · ⬜ not started.

---

## Phase 0 — Foundations, Tooling & Research Spikes 🔶
**Goal:** A loading, mechanics-empty mod plus verified answers to every "does the engine even allow this?" question.

- Mod skeleton: descriptor, folder layout, load-order sanity check on the target EU4 patch (v1.37.5.0 Inca).
- Tooling bootstrap (Python, in `Tooling/` outside the mod): vanilla file parser, province classifier, history-file emitter, colonial-region validator (ocean access + clean borders).
- **Research spikes — each produces a one-page verdict in Test Notes:**
  1. Which target-patch on_actions exist for colony finished, siege won, province owner change, and colonial nation established?
  2. Do `join_all_offensive_wars` / `join_all_defensive_wars`-style effects exist and can they target a *specific* war? (Back War Effort feasibility)
  3. Exact attribute list of `common/subject_types` — what can actually be tuned per type (diplo slot, forcelimit/manpower share, income share, release gating)?
  4. Can a triggered modifier grant `colonists = 1`?
  5. Idea group `trigger` gating — confirmed behavior and grandfathering.
  6. Does conquest inside a new custom colonial region auto-route to a CN as expected, and how does it collide with trade company regions?
  7. **NEW — Tag pipeline:** one dummy custom tag (country file, country history, localization, placeholder flag) loads cleanly and appears in-game. This validates the per-tag file recipe the whole culture-state rollout scales on.
  8. **NEW — Formable behavior:** a test formation decision tag-switches into an *already-existing* tag (the `FRA`-exists-at-start case) — verify subjects, truces, HRE membership, and missions survive the switch sanely.
  9. **NEW — Culture extraction:** tooling reads 1444 primary culture per province from the locked foundation's history and emits a culture→province table matching in-game observation for a sample region (Iberia).

**Exit criterion:** Mechanics-empty mod loads; all nine spike verdicts written; Risk Register updated with findings.

## Phase 1A — Personalized Borders Foundation Research & Lock ✅
**Complete (2026-07-06).** Research documented in [06](06%20-%20Personalized%20Borders%20Foundation%20Research.md); controlled import, vanilla European impassables restoration, and remaining province-ID resolution logged in [07](07%20-%20Personalized%20Borders%20Import%20Log.md)/[08](08%20-%20Vanilla%20European%20Impassables%20Merge%20Log.md)/[09](09%20-%20Remaining%20Province%20ID%20Resolution%20Log.md). The province/border foundation is imported, validated, and **locked**.

## Phase 1 — Map & World Data 🔶
**Goal:** The locked province/border foundation and world data match the design before any system logic exists.

- ✅ Controlled import/port of the Personalized Borders foundation; map validation (`provinces.bmp` colors, ID coverage, `positions.txt`, logs, launch behavior).
- ⬜ Straits removal (`map/adjacencies.csv` full override) — unblocked now that the foundation is locked.
- ⬜ **World tier map (NEW):** Tier A / B / C assignment for every land province (`Tooling/culture_states/world_tiers`), per Doc 10 §3. This is the routing input for both the culture-state layer and the D-4 Sub-Saharan decision.
- ⬜ Development rebalance of the **Americas, Africa, and Australia/Oceania only** via tooling → generated `history/provinces/` overrides (1/1/1, 1/2/1, 1/2/2 classes). Asia and Europe untouched (Anatolia included).
- ⬜ Tier B "mostly uncolonized" pass design: execute owner decision **D-4** for Sub-Saharan Africa's organized states before generating.
- ⬜ Global colonial regions v1, including the combined **Colonial Philippines & Spice Islands** region (validator-checked: ocean access, clean borders, zero trade-company overlap).
- ⬜ Trade company region audit against the new colonial regions.

**Exit criterion:** Game loads with the locked foundation and new map data; world tier map reviewed and committed; observer run to 1500 with no crashes; dev totals per continent reviewed.

## Phase 1B — Culture-State World Data (NEW) ⬜
**Goal:** All the *data* the culture-state layer needs, before a single country file is written.

- Culture extraction tooling (spike 9 productionized): culture→province tables for all Tier A regions from the locked foundation's 1444 history, with the manual override table for bad vanilla culture data (R-35).
- Eligibility pass (Doc 10 E-rules): eligible culture list, micro-culture merge table, vanilla-tag reuse map, new-tag needs list — reviewed per region.
- **Staple-country designation** (`Tooling/culture_states/staple_countries`, Doc 10 E8) and **multi-country partition tables** for large cultures (E9), honoring the §4A granularity rules (HRE at vanilla-style density, Japan mostly vanilla, Ottomans as Turkish staple, India strong-regional).
- **Border-cleanliness validator (Doc 10 O7):** tooling checks every proposed culture-state for connectivity, exclaves, and province snakes against the locked foundation's adjacency data; violations are fixed by reassignment (O2) or same-culture splits (E9), or justified in the exception list (`Tooling/culture_states/border_exceptions` — islands, historic enclaves, trade ports, chokepoints only).
- Formation-set definitions (`Tooling/culture_states/formation_sets`) for Waves 1–4 at minimum.
- Flag mapping table (`Tooling/culture_states/flag_map`): design-time flag assignment per tag (modern national for formables, modern regional for culture-states). **No flag files imported.**
- Tag/content budget estimate per wave (how many new tags, history files, localization entries).

**Exit criterion:** Iberia's complete data package (culture table, tag map, formation set, flag map, ownership diff vs. vanilla, **border-cleanliness validator report**) reviewed and approved by the owner; global eligible-culture census committed.

## Phase 2 — Iberia Proof of Concept (Wave 1) ⬜
**Goal:** The full unification ladder working in one region — the pivot's go/no-go gate.

- Culture-states: Castile, Aragon, Catalonia (new tag), Galicia, León, Navarra (Basque), Granada (Andalusian), Portugal — tooling-generated province/country history, cores per C-rules.
- Cores/claims: own-culture cores day one; Tier 1 "United <Culture>" rank-up; mission-gated group claims.
- Spain formable (`SPA`, excludes Portugal) with formation-set cores + modern-border permanent claims on formation; Andalusia (`ADU`) as competing formable.
- AI weights: formation decision `ai_importance`, mission sequencing, outside-group deterrent v0 scoped to Iberia.
- Vanilla-content audit for Iberia: Iberian Wedding, Reconquista content, Granada war setup — disable/replace as needed (R-31 pattern).
- Placeholder or wave-1 flags per the flag map (modern regional; St George's Cross/tricolor are later waves).

**Exit criterion:** Loads clean; **starting borders pass the O7 cleanliness review** (validator clean or exceptions justified, plus an in-game visual check); observer runs show Iberia consolidating to 2–4 states by ~1550 and Spain forming in most runs by ~1650; no vanilla Iberian event misfires in the log; owner reviews and approves scaling the pattern.

## Phase 3 — European Rollout (Waves 2–5) ⬜
**Goal:** The fractured Europe, wave by wave, each on the proven Iberia pattern.

- **Wave 2 — France** (Francien staple plus Norman, Gascon, Occitan, Burgundian, Breton, etc. → France formable; tricolor on formation; **D-8 resolves here**: staple named France at start vs. `FRA` reserved as formable).
- **Wave 3 — Britain & Ireland** (staple England with St George's Cross, Scotland, Wales, unified Ireland, Highlands → Great Britain/UK formable; Union Jack; modern-UK claims per §7.3).
- **Wave 4 — Italy & Germany** (Italian subculture states → Italy formable; **HRE at vanilla-style density per Doc 10 §4A** — nation count close to vanilla, members tweaked for culture coherence, subculture staples like Bavaria/Saxony/Brandenburg designated, Germany formable above the sandbox; Alsace-Lorraine contested zone activates with Germany per §7.4).
- **Wave 5 — Rest of Europe** (Scandinavia, Balkans, Eastern Europe; East Slavic mapping decides which state inherits the Russia special case; horde decision D-6).
- Each wave ships: tags, ownership, cores/claims, formation set, AI weights, vanilla-content audit, wave flags, border-cleanliness validation + visual review (O7), observer pace test.

**Exit criterion:** Full-Europe observer run to 1650: unification proceeds at target pace in every wave region, no runaway pan-European blob, no crash, audited vanilla content quiet in logs.

## Phase 4 — Colonization Core ⬜
**Goal:** Who colonizes, how, and what colonies become — now that the European cast exists.

- `crown_is_european` + `crown_is_european_colonizer` scripted triggers + startup flagging; Ottoman carve-out unchanged (the Ottomans exist as the staple Turkish power, never a Western colonial country — Doc 10 §4A).
- Exploration Ideas gated per Doc 10 K-rules: colonizer trigger + coastal capital/naval gates + Tier-1-unification-or-head-start-list requirement.
- Western European colonial head start package for the curated coastal culture-state list; **formation upgrade package** (extra colonist, range, naval FL) on Tier 2 formation.
- Frontier Settlement v1: reform/decision, 1 colonist, tiny range, adjacency-enforcement event.
- Colonial nation formation hooks: +1 colonist on formation, colonial capital culture/religion conversion.
- Diplo-slot workaround (Exploration finisher upkeep).

**Exit criterion:** Observer run to 1600 — coastal Western European states (unified or head-start) settle the Americas; tiny inland minors and non-Europeans do not; formed nations visibly out-colonize culture-states; CNs form with +1 colonist and converted capitals.

## Phase 5 — North Africa, Middle East & Asia Rollout (Waves 6–7) ⬜
**Goal:** Complete the Tier A fractured world.

- **Wave 6 — North Africa & Middle East** (Maghrebi/Egyptian/Levantine culture-states; **the Ottomans exist as the staple Turkish power** holding all or most Turkish culture land per Doc 10 §4A, non-Turkish land fragmenting normally).
- **Wave 7 — Asia** (Persia, Southeast Asia; **Japan mostly vanilla** per §4A; **China regional-states-first** per §4A/D-3 with its own Mandate of Heaven/Ming content audit, R-39; **India as strong regional/culture states plus some smaller states** with the India/Bharat/Hindustan unification path, R-40).
- Same per-wave package as Phase 3.

**Exit criterion:** Global observer run to 1650 with all Tier A waves live: regional unification pace on target, Tier B untouched and mostly uncolonized, log clean.

## Phase 6 — Subject Framework ⬜
**Goal:** The three-subject empire structure. (Unchanged from the pre-pivot plan.)

- Colonial Administration tuning (~30% FL/manpower, ~20% income).
- Overseas Dependency subject type + disconnected-conquest enforcement v1 (post-peace detection → forced subject event).
- Dominion subject type (−60 LD, 50% income cut, 10% FL/manpower) + conversion interaction at LD > 50.
- Independence-by-war-only enforcement (AI-side); Dominion AI late-game gate.

**Exit criterion:** Scripted test saves demonstrate each subject type forming through its intended path and nothing else; contribution numbers verified in-game.

## Phase 7 — Unification & Global Balance ⬜
**Goal:** The ladder and the deterrent, tuned; Europe competes overseas, not at home.

- Balance of Power outside-group deterrent full version (re-scoped per §7.2); AE/coalition/opinion tuning.
- Modern-border permanent claim sets finalized for UK/France/Spain/Germany formation rewards; Alsace-Lorraine contested-zone system verified live.
- Mission tree passes: ladder sequencing (culture → group → outward) for all major formation sets; colonial/naval redirects for formables.
- Lucky nations replacement (curated culture-state/formable list).
- Unification pace tuning against observer targets per wave region (R-32).

**Exit criterion:** Three observer runs to 1700 — formables form at plausible dates across Europe, no state consistently snowballs across culture-group lines, colonial empires visibly form.

## Phase 8 — Warfare & Diplomacy ⬜
**Goal:** The interventionist layer. (Unchanged.)

- Back War Effort (decision/event interface, +50 opinion gate, defensive-cheap/offensive-expensive, AI restrictions) — built against the Phase 0 spike verdict; fallback design if per-war joining is impossible.
- Fort capture completion (on_siege_won hook or control-sweep).

**Exit criterion:** Back War Effort demonstrably used by AI within its restrictions in a hands-off run; fort falls flip surrounding control reliably.

## Phase 9 — Culture & Assimilation ⬜
**Goal:** Colonies that look colonial. (Unchanged.)

- Native culture/religion retention system (post-colonization correction + tooling-generated native lookup).
- Hidden assimilation event suite: pulse events, dev-weighted odds (production ×2), full blocker list, major-native-capital exclusion list.

**Exit criterion:** 1700 observer save shows colonial nations with majority native-culture interiors, converted capitals, and rare scattered assimilation.

## Phase 10 — AI & Balance Passes ⬜
**Goal:** The design survives contact with the AI.

- Naval invasion competence review (England/Denmark/Japan behavior without straits).
- Unification stall/snowball review across all Tier A regions (R-32): pace levers re-tuned against full campaigns.
- Flattened-region stability pass (rebel pressure in the 1/1/1 zones).
- Economy pass: trade value, tariffs, subject income flows.
- HRE monitoring per the vanilla-density rule (Doc 10 §4A): blobbing/passivity at near-vanilla member counts, R-33.
- **Trade company decision point (R-19):** disable, replace, or convert into a custom Trade Post Charter system, decided against this phase's observer data.
- Full-campaign observer runs (1444→1821) with issue log.

**Exit criterion:** A full hands-off campaign produces a plausible world: unified nation-states out of the culture-state start, colonial empires, intact (if pressured) Asia, no world-on-fire, no runaway hegemon.

## Phase 11 — Flags, Alt-History Residual & Polish ⬜
**Goal:** Shippable v1.

- Flag completeness pass: every tag on the modern/regional flag standard; ET Modern Flags source decision (permission/credit per R-36) or original flag set.
- Residual alt-history layer: formables the ladder doesn't produce (Belgium, Romania, etc.); the 2026 layer stays post-v1.
- Localization pass (all custom systems and new tags fully localized in English).
- Subject-type icons / minimal UI art; performance pass (event pulse budgets).
- README, changelog, credits/permissions audit (R-29/R-36), Steam Workshop packaging.

**Exit criterion:** Clean playtest feedback cycle; release candidate tagged.
