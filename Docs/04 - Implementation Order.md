# Project Crown: Europa Ascendant — Implementation Order

The ordering principle: **province/border foundation before everything, data before systems, risky before safe, engine-verified before built.** Anything sitting on an unverified engine assumption gets a Phase 0 spike before a single real file is written for it.

## Build first

| # | System | Why first |
|---|---|---|
| 1 | **Personalized Borders foundation research and lock** | The user has made the province/border map the top priority. Project Crown should target Personalized Borders (Workshop ID `3418818231`) if compatible, and every province-list system depends on that decision. |
| 2 | **Controlled foundation import/port** | Only after research approval: validate/repair `map/provinces.bmp`, merge `map/positions.txt` against vanilla 1.37.5, launch-test the foundation alone, and do not edit the Workshop copy. |
| 3 | **Mod skeleton + tooling pipeline** | Everything else flows through it; the province-history generator and validators must target the locked foundation. |
| 4 | **Phase 0 research spikes** (on_actions inventory, war-join effects, subject_type attributes, triggered-modifier colonists, idea gating, colonial-region routing) | Six cheap experiments that de-risk five major systems. Highest information-per-hour in the whole project, but gameplay systems still wait on the map foundation. |
| 5 | **Straits removal** | One file, enormous gameplay impact, and every AI/balance observation afterward must include it. It now waits until the final province bitmap/positions are locked. |
| 6 | **Colonial-zone dev rebalance (Americas, Africa, Oceania — Asia and Europe untouched)** | The colonial world's economic baseline. It must be generated from the locked foundation so province coverage is not stale. |
| 7 | **Global colonial regions** | The routing switch for the entire subject framework (what becomes a Colonial Administration vs. an Overseas Dependency). Must be drawn after the foundation is stable. |
| 8 | **Exploration gate + European/colonizer triggers (incl. the Ottoman carve-out) + colonial head start** | Cheap to build, defines who plays which game; needed for any meaningful observer run after world data is stable. |
| 9 | **Subject types v1 (CA tuning, Overseas Dependency, skeleton Dominion)** | Long-lead, spike-dependent, and the mod's identity. Start only after the map/world-data layer stops moving. |

## Build mid (after the above stabilizes)

- Frontier Settlement (needs colonial regions + exploration gate in place to test against).
- CN formation hooks (+1 colonist, capital conversion).
- Disconnected-conquest enforcement v1 (needs subject types).
- Permanent modern-border claims + mission redirects for UK/France/Spain, plus Germany's formation-attached claim set and the Alsace-Lorraine contested-zone system.
- PU event rework (Burgundian/Iberian) + lucky nations replacement.

## Delay until later

| System | Why delayed |
|---|---|
| **Back War Effort** | Highest engine risk (hardcoded diplomacy, coarse war-join effects), zero other systems depend on it, and its AI restrictions only mean anything once the war/AI landscape is stable. Build in Phase 5 against the spike verdict. |
| **Assimilation suite** | Pure long-horizon flavor; needs the native-retention system, colonial nations, and liberty-desire behavior all working first. Its blockers reference half the mod. Phase 6. |
| **Dominion AI behavior & tuning** | The type skeleton comes early, but "AI converts at LD > 50, late game only" is meaningless before liberty desire dynamics are observable in long runs. Phase 5–7. |
| **Fort capture completion** | Vanilla ZoC already covers ~90% of the intent; this is polish on top. Phase 5. |
| **Balance-of-power deterrent tuning** | The event layer comes mid, but its numbers can only be tuned against Phase 7 observer campaigns. |
| **Trade company final disposition (disable / replace / Trade Post Charter)** | Vanilla trade companies are deliberate interim scaffolding (owner decision, R-19). The disposition decision needs stable subject-framework and economy data from Phase 7 observer runs; deciding earlier means deciding blind. |
| **1914 / 2026 formables** | Explicitly the long-term layer (Rule 28). Rides on the finished subject/independence framework; touching it earlier means reworking it later. Phase 8. |
| **Localization polish, icons, UI art** | Ship-quality concerns. English placeholder text is fine until Phase 9. |

## The three hard sequencing rules

1. **Foundation first.** Personalized Borders research/lock and the controlled map import/port come before no-straits, development rebalance, colonial regions, subjects, missions, claims, events, ideas, fort work, Back War Effort, assimilation, and all other gameplay systems.
2. **No spike, no system.** Back War Effort, the CN colonist modifier, disconnected-conquest enforcement, and every on_action-dependent hook wait for their Phase 0 verdict — fallbacks are already named in the Risk Register, so a negative verdict changes the plan, not the schedule.
3. **World data freezes before balance opens.** Dev rebalance and colonial regions must stop moving before anyone tunes economy, AI, or subject contribution numbers — every balance observation on shifting world data is wasted.
