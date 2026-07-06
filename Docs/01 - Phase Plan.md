# Project Crown: Europa Ascendant — Phase Plan

Phases are ordered by dependency and risk: engine-risk research first, world data second, systems third, balance and flavor last. Each phase has an exit criterion — do not start the next phase's systems until the current one's criterion is met (parallel *research* is always fine).

---

## Phase 0 — Foundations, Tooling & Research Spikes
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

**Exit criterion:** Mechanics-empty mod loads; all six spike verdicts written; Risk Register updated with findings.

## Phase 1 — Map & World Data
**Goal:** The world itself matches the design before any system logic exists.

- Straits removal (`map/adjacencies.csv` full override).
- Development rebalance of the **Americas, Africa, and Australia/Oceania only** via tooling → generated `history/provinces/` overrides (1/1/1, 1/2/1, 1/2/2 classes). Asia and Europe untouched (Anatolia included).
- Global colonial regions v1, including the combined **Colonial Philippines & Spice Islands** region (validator-checked: ocean access, clean borders, zero trade-company overlap).
- Trade company region audit against the new colonial regions (trade companies stay vanilla as interim scaffolding — final disposition is the Phase 7 decision point, R-19).

**Exit criterion:** Game loads with new map data; observer run to 1500 with no crashes; dev totals per continent reviewed.

## Phase 2 — Colonization Core
**Goal:** Who colonizes, how, and what colonies become.

- `crown_is_european` + `crown_is_european_colonizer` scripted triggers + startup flagging, including the Ottoman carve-out (European-adjacent great power, never a colonizer).
- Exploration Ideas gated to European colonizers (Ottomans excluded at game start).
- Western European colonial head start package (starting modifiers, explorer events, range bonuses).
- Frontier Settlement v1: reform/decision, 1 colonist, tiny range, adjacency-enforcement event.
- Colonial nation formation hooks: +1 colonist on formation, colonial capital culture/religion conversion.
- Diplo-slot workaround (Exploration finisher upkeep).

**Exit criterion:** Observer run to 1600 — European colonizers settle the Americas; non-Europeans and the Ottomans only edge-settle; CNs form with +1 colonist and converted capitals.

## Phase 3 — Subject Framework
**Goal:** The three-subject empire structure.

- Colonial Administration tuning (~30% FL/manpower, ~20% income).
- Overseas Dependency subject type + disconnected-conquest enforcement v1 (post-peace detection → forced subject event).
- Dominion subject type (−60 LD, 50% income cut, 10% FL/manpower) + conversion interaction at LD > 50.
- Independence-by-war-only enforcement (AI-side).
- Dominion AI late-game gate.

**Exit criterion:** Scripted test saves demonstrate each subject type forming through its intended path and nothing else; contribution numbers verified in-game.

## Phase 4 — European Balance & Home Claims
**Goal:** Europe competes overseas, not at home.

- Permanent modern-border claim sets: UK (Great Britain + Northern Ireland approximation — exact NI provinces chosen during this phase's province-ID mapping work, not guessed earlier), France (modern, incl. Alsace-Lorraine), Spain (modern), Germany (modern, incl. Alsace-Lorraine — attached to the formable), plus secondary majors' home regions.
- Alsace-Lorraine contested-zone system: reciprocal Franco-German core grants, simultaneous cores allowed; activates on German formation or a clearly defined late-game German nationalism path — no automatic pre-formation content for unifier candidates.
- Mission tree redirects for European majors (colonial/naval rewards, formation paths preserved).
- Burgundian Inheritance & Iberian Wedding rework.
- Lucky nations replacement; Balance of Power opinion/deterrent system for intra-European conquest.

**Exit criterion:** Three observer runs to 1700 — no European major consistently snowballs Europe; colonial empires visibly form.

## Phase 5 — Warfare & Diplomacy
**Goal:** The interventionist layer.

- Back War Effort (decision/event interface, +50 opinion gate, defensive-cheap/offensive-expensive, AI restrictions) — built against the Phase 0 spike verdict; fallback design if per-war joining is impossible.
- Fort capture completion (on_siege_won hook or control-sweep).

**Exit criterion:** Back War Effort demonstrably used by AI within its restrictions in a hands-off run; fort falls flip surrounding control reliably.

## Phase 6 — Culture & Assimilation
**Goal:** Colonies that look colonial.

- Native culture/religion retention system (post-colonization correction + tooling-generated native lookup).
- Hidden assimilation event suite: pulse events, dev-weighted odds (production ×2), full blocker list, major-native-capital exclusion list.

**Exit criterion:** 1700 observer save shows colonial nations with majority native-culture interiors, converted capitals, and rare scattered assimilation.

## Phase 7 — AI & Balance Passes
**Goal:** The design survives contact with the AI.

- Naval invasion competence review (England/Denmark/Japan behavior without straits).
- Flattened-region stability pass (rebel pressure in the 1/1/1 zones: Americas, Africa, Oceania).
- Economy pass: trade value, tariffs, subject income flows.
- HRE monitoring: observer games checked for HRE blobbing or passivity — the HRE stays mostly vanilla in v1, and no HRE overhaul happens until the core colonial, subject, development, and claim systems are stable.
- **Trade company decision point (R-19):** disable, replace, or convert trade companies into a custom Trade Post Charter overseas subject/trade-post system, decided against this phase's observer data. If the custom system is chosen, building it is Phase 8+/post-v1 scope.
- Full-campaign observer runs (1444→1821) with issue log.

**Exit criterion:** A full hands-off campaign produces a plausible world: colonial empires, intact (if pressured) Asia, no world-on-fire, no runaway European hegemon.

## Phase 8 — Alternate-History Borders (1914 / 2026)
**Goal:** Rule 28's long-term layer.

- 1914 formables/decisions set; 2026 layer as end-game flavor.
- New tags, localization, country colors as needed.

**Exit criterion:** Each formable is reachable in a test save and produces clean borders within vanilla map limits.

## Phase 9 — Polish & Release
**Goal:** Shippable v1.

- Localization pass (all custom systems fully localized in English).
- Subject-type icons / minimal UI art.
- Performance pass (event pulse budgets).
- README, changelog, Steam Workshop packaging.

**Exit criterion:** Clean playtest feedback cycle; release candidate tagged.
