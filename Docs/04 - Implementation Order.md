# Project Crown: Europa Ascendant — Implementation Order

**Revised 2026-07-06 for the Culture-State World pivot.** The ordering principle is unchanged: **province/border foundation before everything, data before systems, risky before safe, engine-verified before built.** The foundation is now locked (Docs 07–09), so the front of the queue is the culture-state political layer — proven in one region before it scales.

## Already done

| System | Status |
|---|---|
| Personalized Borders foundation research (Phase 1A) | ✅ Doc 06 |
| Controlled foundation import + validation | ✅ Doc 07 |
| Vanilla European impassables restoration | ✅ Doc 08 |
| Remaining province-ID resolution | ✅ Doc 09 |

## Build first

| # | System | Why first |
|---|---|---|
| 1 | **Phase 0 research spikes, including the four new pivot spikes** (tag pipeline, formable tag-switch behavior, culture extraction, forced war-joining) | Cheap experiments that de-risk the entire rollout pattern. The tag-pipeline spike (one dummy tag loads with history/loc/flag) is the recipe every culture-state repeats; the formable spike covers the FRA/ENG "target tag exists at start" case (R-34); the forced war-joining spike (10) gates both hostile intervention and colonial parent auto-join (R-47). |
| 2 | **Culture extraction tooling + world tier map + border-cleanliness validator** | The data layer everything in Doc 10 keys off: culture→province tables from the locked foundation, Tier A/B/C assignment per province, and the O7 validator (connectivity, exclave, and snake detection against foundation adjacency data). Pure tooling, zero game files. |
| 3 | **Phase 1B data packages: eligibility pass, staple-country list, multi-country partition tables, tag reuse map, formation sets, flag map, border-cleanliness report** | Generated and owner-reviewed *before* any country file exists, honoring the §4A granularity rules (HRE at vanilla density, staples per major culture) and the O7 border rule (compact connected countries; exceptions justified). The Iberia package is the approval gate for the whole pivot. |
| 4 | **Straits removal** | One file, enormous gameplay impact, unblocked by the foundation lock. Every observer run afterward includes it, so it must land before pace-tuning observations begin. |
| 5 | **Iberia Proof of Concept (Wave 1)** | The pivot's go/no-go: ~8 culture-states (8 vanilla reuse tags after the Phase 1B audit, including `CAT` for Catalonia), Spain formable excluding Portugal, the full cores/claims ladder, AI weights, Iberian vanilla-content audit — plus a **controlled diplomacy slice only**: Iberian local rivalries/friendships and contested-frontier claims where useful (Doc 10 §12). No intervention, dynastic-event, or colonial-war systems here. Smallest region that exercises everything. Aragon (`ARA`) needs primary-culture history review because vanilla history currently marks it Catalan. |
| 6 | **Colonial-zone dev rebalance + Tier B "mostly uncolonized" pass (D-4)** | The colonial world's economic baseline, generated from the locked foundation. Sequenced here so the Sub-Saharan decision (D-4) is made once, not patched later. |
| 7 | **Global colonial regions** | The routing switch for the subject framework. Drawn after world data is stable, before colonization systems test against it. |
| 8 | **European rollout Waves 2–5 (France → Britain → Italy/Germany → rest of Europe)** | Scales the proven Iberia pattern. Wave 4 keeps the HRE at vanilla-style density per Doc 10 §4A (members tweaked, count preserved); D-8 (France staple vs. formable-only) resolves in Wave 2; each wave ships its own audit, flags, and pace test. |
| 9 | **Colonization core (exploration gate, colonizer triggers, head start, formation upgrade, Frontier Settlement, CN hooks)** | Built once the European colonizer cast exists, so the unification-first gates (K-rules) are testable end to end. |
| 10 | **Subject types v1 (CA tuning, Overseas Dependency, skeleton Dominion)** | Long-lead, spike-dependent, and the mod's empire identity. Starts only after the map/world/political data stops moving. |

## Build mid (after the above stabilizes)

- North Africa / Middle East / Asia rollout (Waves 6–7; Ottomans ship as the staple Turkish power per Doc 10 §4A; Japan stays mostly vanilla; China regional-states-first per D-3/R-39; India strong-regional with the Bharat/Hindustan path per R-40).
- Disconnected-conquest enforcement v1 (needs subject types).
- Modern-border permanent claim rewards + Alsace-Lorraine contested-zone system (attach to the formables built in Waves 2–4; Alsace-Lorraine is the model contested region, Doc 10 CP4).
- Contested-region registry + diplomacy seed tables shipping with each wave's data package (Doc 10 CP5/N4), each with its per-wave audit that disputed claims and seeded relationships support clean culture-state gameplay.
- Balance of Power outside-group deterrent full version + mission-ladder passes.
- Lucky nations replacement (curated culture-state/formable list).

## Delay until later

| System | Why delayed |
|---|---|
| **Back War Effort + hostile intervention (MDD §11.1)** | Highest engine risk (hardcoded diplomacy, coarse war-join effects — spikes 2 and 10), zero other systems depend on it. The full package — friendly backing, enemy-of-my-enemy path, rival rule, Great Power freedoms via the `crown_is_great_power` scripted trigger — builds in Phase 8 against the spike verdicts. Documented now, implemented later. |
| **Rare dynastic & diplomatic unification package (Doc 10 U-rules)** | The classic blob accelerant (R-45/R-46) — only safe to build once the country setup is stable and unification pace is observable. Phase 7. Documented now, implemented later. |
| **Colonial nation war rights + parent escalation/auto-join (MDD §9.4)** | Needs colonial nations (Phase 4) and the subject framework (Phase 6) stable, plus spike 10's forced-participation verdict (R-47). Phase 8, with its dedicated proxy-war balance pass in Phase 10 (R-48). Documented now, implemented later. Never blocks the Iberia POC. |
| **Assimilation suite** | Pure long-horizon flavor; needs native retention, colonial nations, and liberty-desire behavior working first. Phase 9. |
| **Dominion AI behavior & tuning** | "AI converts at LD > 50, late game only" is meaningless before liberty-desire dynamics are observable in long runs. Phases 8–10. |
| **Fort capture completion** | Vanilla ZoC covers ~90% of the intent; polish. Phase 8. |
| **Unification pace & deterrent tuning** | The levers ship with each wave, but the numbers can only be tuned against Phase 10 full-campaign observer data (R-32). |
| **Trade company final disposition (disable / replace / Trade Post Charter)** | Deliberate interim scaffolding (R-19); decided against Phase 10 observer data. |
| **Flag completeness pass & ET Modern Flags source decision** | Design-time flag *mapping* is maintained from Phase 1B, and each wave ships its own flags — but the global completeness pass and the ET source/permission decision (R-36) are Phase 11. **No flag files are imported before their wave.** |
| **Residual alt-history formables (Belgium, Romania, …; 2026 layer)** | The unification ladder absorbed the 1914 core; what's left is flavor on top of a finished framework. Phase 11 / post-v1. |
| **Localization polish, icons, UI art** | Ship-quality concerns. English placeholder text is fine until Phase 11. |

## The four hard sequencing rules

1. **Foundation first — satisfied.** The Personalized Borders foundation is imported, validated, and locked; it stays frozen. The culture-state layer is history-file work only and never touches `map/` files (Doc 10, O5).
2. **No spike, no system.** Back War Effort, the CN colonist modifier, on_action-dependent hooks, the tag pipeline, and formable tag-switching all wait for their Phase 0 verdicts — fallbacks are named in the Risk Register, so a negative verdict changes the plan, not the schedule.
3. **Data before countries, Iberia before the world.** No country file is written before its Phase 1B data package is reviewed — including a clean (or justified-exception) border-cleanliness report per Doc 10 O7 — and no wave beyond Iberia starts before the Iberia POC exit criteria are met and the owner approves scaling the pattern.
4. **World data freezes before balance opens.** Dev rebalance, colonial regions, and the Tier A political map must stop moving before anyone tunes economy, AI, unification pace, or subject contribution numbers — every balance observation on shifting world data is wasted.
