# Project Crown: Europa Ascendant — Implementation Order

The ordering principle: **data before systems, risky before safe, engine-verified before built.** Anything sitting on an unverified engine assumption gets a Phase 0 spike before a single real file is written for it.

## Build first

| # | System | Why first |
|---|---|---|
| 1 | **Mod skeleton + tooling pipeline** | Everything else flows through it; the province-history generator is the project's backbone. |
| 2 | **Phase 0 research spikes** (on_actions inventory, war-join effects, subject_type attributes, triggered-modifier colonists, idea gating, colonial-region routing) | Six cheap experiments that de-risk five major systems. Highest information-per-hour in the whole project. |
| 3 | **Straits removal** | One file, enormous gameplay impact, and every AI/balance observation afterward must include it — testing anything on a straits map is testing the wrong mod. |
| 4 | **Colonial-zone dev rebalance (Americas, Africa, Oceania — Asia and Europe untouched)** | The colonial world's economic baseline. Colonial income, institution flow, and military balance all read differently on top of it; do it before tuning anything that depends on it. |
| 5 | **Global colonial regions** | The routing switch for the entire subject framework (what becomes a Colonial Administration vs. an Overseas Dependency). Must exist before colonization or subjects can be tested honestly. |
| 6 | **Exploration gate + European/colonizer triggers (incl. the Ottoman carve-out) + colonial head start** | Cheap to build, defines who plays which game; needed for any meaningful observer run. |
| 7 | **Subject types v1 (CA tuning, Overseas Dependency, skeleton Dominion)** | Long-lead, spike-dependent, and the mod's identity. Start early even if numbers stay rough. |

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

## The two hard sequencing rules

1. **No spike, no system.** Back War Effort, the CN colonist modifier, disconnected-conquest enforcement, and every on_action-dependent hook wait for their Phase 0 verdict — fallbacks are already named in the Risk Register, so a negative verdict changes the plan, not the schedule.
2. **World data freezes before balance opens.** Dev rebalance and colonial regions must stop moving before anyone tunes economy, AI, or subject contribution numbers — every balance observation on shifting world data is wasted.
