# Project Crown: Europa Ascendant — Culture-State World Design

**Version:** 1.2 — owner border cleanliness rule added (O7); ownership and split rules amended accordingly
**Date:** 2026-07-06
**Status:** Approved design pivot (owner directive 2026-07-06). Design only — no countries created, no gameplay files edited, no flags imported, no map files changed.
**Authority:** This document defines the Culture-State World layer. Where it conflicts with pre-pivot text in [00 - Master Design Document](00%20-%20Master%20Design%20Document.md), this document and Appendix B Round 4 of the MDD win.

---

## 1. Concept

Project Crown's 1444 world is **fractured along culture lines**. Instead of the vanilla political map, every eligible culture and subculture starts as its own country where possible. "Its own country" does not always mean *exactly one*: every major culture is anchored by a **staple country** that always exists (England for English, Castile for Castilian, the Ottomans for the Turkish group…), and a culture too large for one balanced state may be split into several same-culture countries (E8–E9). Starting borders must read as **intentional, clean, and playable** — compact, connected countries, no border gore (O7). Anchor examples:

- Castilian, Aragonese, Leonese, Catalan, Galician, Basque, Portuguese, and Andalusian states in Iberia.
- French subcultures (Francien, Norman, Gascon, Occitan, Burgundian, etc.) that can form **France**.
- German subcultures (Bavarian, Swabian, Saxon, Westphalian, Pomeranian, etc.) that can form **Germany**.
- Italian subcultures (Lombard, Tuscan, Neapolitan, Sicilian, etc.) that can form **Italy**.
- British Isles cultures (English, Scottish, Welsh, Irish, Highlander) that can form **Great Britain / the UK**.

This applies **globally where appropriate**, not only in Europe. North Africa is explicitly included and breaks into culture-based countries. Asia is included unless a later design decision excludes a specific area.

The game loop for a culture-state is a ladder:

1. **Unify your culture area** (cheap, sanctioned, claimed).
2. **Unify your culture group** into the larger formable nation (France, Germany, Spain, Italy, Great Britain, …).
3. **Project power outward** — colonization and global competition, per the existing Project Crown premise.

Everything else in Project Crown survives: the Personalized Borders map foundation, vanilla European impassables, the Europe-outward colonial premise, the subject taxonomy, development flattening in the colonial zones, and the mostly-uncolonized frontier regions.

## 2. Pivot, Not Restart

**Decision: design pivot.** A restart was considered and rejected:

| Layer | Fate under the pivot | Why |
|---|---|---|
| Personalized Borders map foundation (imported, validated, impassables restored) | **Kept unchanged** | Political setup is a `history/` layer; it never touches `map/` files |
| Vanilla European impassables | **Kept** | Owner decision, already merged |
| No-straits rule, fort capture | **Kept** | Orthogonal to the political layer |
| Development flattening (Americas, Africa, Oceania) | **Kept** | Reinforces the mostly-uncolonized frontier requirement |
| Colonial regions, Exploration lock, Frontier Settlement, colonial head start | **Kept, re-expressed** | Membership lists now name culture-states and formables instead of vanilla 1444 tags (§9) |
| Subject taxonomy (CA / Overseas Dependency / Dominion), disconnected-conquest rule | **Kept** | Unaffected by who the countries are |
| Modern-border permanent claims (UK/France/Spain/Germany) | **Kept, promoted** | They become the reward layer of the formable tier (§6) |
| Vanilla 1444 political setup, PU mega-event reworks, HYW framing | **Superseded** | The culture-state map replaces the vanilla start; content referencing it is audited per rollout wave (Risk R-31) |

The only pre-pivot work invalidated is design text about the *vanilla 1444 political situation* — no committed files are thrown away.

## 3. World Tiers

Every land province belongs to exactly one tier. The tier map is tooling-maintained data (`Tooling/culture_states/world_tiers`), generated after review, and is the routing switch for the whole layer.

| Tier | Name | Treatment | Coverage |
|---|---|---|---|
| **A** | Fragmented Old World | Culture-state rules (§4–§8) apply: eligible cultures become countries | Europe, North Africa, Middle East, Asia (unless a later decision excludes a specific area) |
| **B** | Uncolonized frontier | **No culture-states.** Starts mostly uncolonized; colonial regions and dev flattening apply | Americas, Sub-Saharan Africa, Australia/Oceania, the Philippines |
| **C** | Special cases | Explicit owner-decision handling, one rule per case | Russia/Siberia (existing owner decision), Japan, steppe hordes, and any case the E-rules cannot express (§14) |

Tier A vs. B boundary notes:

- **North Africa is Tier A** (owner directive): Maghrebi and Egyptian-area cultures become culture-states.
- **Sub-Saharan Africa is Tier B**: it should start *mostly* uncolonized. How existing organized states (Mali, Songhai, Ethiopia, Kongo, the Swahili coast) are handled is Open Decision D-4.
- The Philippines' Tier B status matches the existing **Colonial Philippines & Spice Islands** region (MDD owner decision 5).
- Siberia stays a Tier C land frontier per the existing Russia rule — never a colonial region, never fragmented into culture-states by default.

## 4. Eligible Culture-Countries (E-rules)

- **E1 — One culture, at least one country.** Each culture that is the primary culture of a coherent homeland in Tier A gets **at least one** starting country. The default is exactly one — but see E8 (every major culture has a staple country) and E9 (large cultures may be split into several same-culture countries).
- **E2 — Minimum footprint.** A culture qualifies if it is the 1444 primary culture (per the locked foundation's province history) of **at least 3 land provinces** forming one contiguous or near-contiguous cluster.
- **E3 — Merge rule for micro-cultures.** Cultures below the E2 threshold, or hopelessly scattered ones, are merged into a designated sibling culture-state. The merge table lives in tooling and is reviewed per rollout wave.
- **E4 — Reuse vanilla tags first.** Where a plausible vanilla tag exists (active or releasable — e.g., `CAS`, `ARA`, `GAL`, `LON`, `NAV`, `GRA`, `POR`), the culture-state uses it. New tags are created only when no vanilla tag fits (e.g., Catalonia). This keeps vanilla localization, colors, and some content working for free.
- **E5 — Consolidation cuts both ways.** Where vanilla splits one culture across many tags (e.g., the Irish minors), the culture-state world *may* consolidate them into fewer countries per culture. Consolidation is bounded by the regional granularity rules in §4A — in particular, the HRE keeps roughly its vanilla nation count.
- **E6 — Special-case guard.** Single-culture civilizations that already have an internal-unification mechanic (Japan's Sengoku/shogunate system) are **not** auto-unified by E1. Japan is resolved by owner rule (§4A): keep the vanilla daimyo setup, never a unified 1444 Japan.
- **E7 — Culture data source of truth.** Culture assignments come from vanilla 1444 province history read against the locked Personalized Borders foundation, with a manual override table in tooling for known-bad vanilla assignments (Risk R-35).
- **E8 — Staple country rule (owner rule, 2026-07-06).** Every major eligible culture/subculture has a designated **staple (anchor) country** that always exists at start: **England** for English, **Castile** for Castilian, **Aragon** for Aragonese, the **Ottomans** for the Turkish culture group. **France** is the Francien staple unless a specific region plan reserves France strictly as the formable (Open Decision D-8). The staple list lives in `Tooling/culture_states/staple_countries` and is reviewed per wave.
- **E9 — Multi-country cultures (owner rule, 2026-07-06).** A culture too large for one balanced country — **or too geographically awkward for one clean, connected country (O7)** — may start as **2, 3, or more same-culture countries** where balance, regional density, or border cleanliness needs it. The staple country (E8) must exist among them and starts as the strongest. Partition tables live in tooling per wave.

## 4A. Regional Granularity Rules (owner rules, 2026-07-06)

The E-rules set the default; these regional rules override the default where the owner has decided granularity explicitly.

- **HRE — keep vanilla-style density.** The HRE nation count stays **relatively close to vanilla EU4**: roughly the same number of HRE nations exists in Project Crown. Individual members may be tweaked (borders nudged toward culture coherence, a few merges/splits where they clearly improve the sandbox), but the HRE is **neither collapsed into a handful of subculture states nor massively expanded**. German subcultures are the flagship multi-country cultures (E9): many same-culture princes, each major subculture anchored by a staple (e.g., Bavaria, Saxony, Brandenburg — finalized in the Wave 4 data package), and **Germany remains the Tier 2 formable** above them. The dense HRE political sandbox is a design feature, not a casualty of the pivot.
- **Japan — mostly vanilla.** Japanese nations stay mostly as in vanilla (Sengoku daimyo under the shogunate). Tweak only what's needed; break Japan up further **only if testing/design shows a need**. Japan never starts unified.
- **Ottomans — staple Turkish power.** The Ottomans **exist at start** as the staple country of the Turkish culture group. They control **all or the majority of Turkish culture land** (exact share is a later balance/design call). They remain a major regional power — and remain **never a Western colonial country**: the existing Exploration/colonial carve-out (MDD §4, owner decisions 1 and 10) applies unchanged. Their non-Turkish land (Balkans, etc.) fragments into culture-states per the normal rules.
- **China — fragmentation allowed later, flagged high-risk.** China *can* still be fragmented, but this is explicitly **high-risk** (Risk R-39): Mandate of Heaven, Ming/Qing content, the tributary system, dense development, and AI snowball potential all fight it. Recommended path: **strong regional Chinese states first** (a handful of plausible regional powers), never extreme one-province fragmentation. Decision D-3 stays open with this refined framing.
- **India — fragmented but not steamrollable.** India is broken up **a lot, but not into hundreds of weak minors**: prefer **strong regional/culture states plus some smaller states**, sized so outside powers cannot easily steamroll the subcontinent (Risk R-40). India gets a future **India / Bharat / Hindustan unification path** — a formation set (or tiered sets) defined in the Wave 7 data package, reusing the vanilla Bharat/Hindustan formable tags where they fit.

## 5. Starting Ownership (O-rules)

- **O1 — Culture defines the border.** Each culture-state starts owning the Tier A provinces whose 1444 primary culture is its culture. For multi-country cultures (E9), the culture area is partitioned among the same-culture states per the tooling partition table, with the staple (E8) taking the strongest share.
- **O2 — Exclave and edge handling.** Tooling flags exclaves and awkward pockets; a manual override list reassigns them for border cleanliness (an exclave may go to the surrounding culture-state). Overrides are logged. O7 is the governing principle.
- **O3 — Empires dissolve.** Existing multi-culture states in Tier A (the 1444 Ottoman, Mamluk, Timurid, Ming, etc. setups) are dissolved into culture-states. Survivor exceptions require an explicit owner decision (D-1, D-3, D-5).
- **O4 — Untouched land.** Uncolonized/native provinces, wastelands, and the restored vanilla European impassables are unchanged. Tier B keeps its mostly-uncolonized state.
- **O5 — History layer only.** Starting ownership is implemented purely in `history/provinces/` and `history/countries/` overrides generated by tooling. **No `map/` file changes.**
- **O6 — Capitals.** Each culture-state's capital is the historically strongest own-culture province (curated per wave; default = highest-development own-culture province).
- **O7 — Border cleanliness rule (owner rule, 2026-07-06).** Starting borders must look **intentional, clean, and playable**:
  - Culture-state ownership prefers **compact, connected, readable countries**. No weird, ugly, or disconnected borders unless there is a clear strategic, historical, geographic, or gameplay reason — and that reason is logged.
  - **Culture purity never outranks readability.** Do not assign every same-culture province to one country if that creates disconnected exclaves or border gore; reassign edge provinces (O2) or split the culture into multiple same-culture countries (E9) instead — one of which must still be the staple tag (E8).
  - **Disconnected land is acceptable only for strategic cases:** islands, historically meaningful enclaves, trade ports, chokepoints, and later overseas/colonial holdings.
  - **No random exclaves and no ugly province snakes** in the 1444 start. Tooling enforces this with a border-cleanliness validator (connectivity check per country + exclave/snake detection); every surviving exception carries a justification in the exception list (`Tooling/culture_states/border_exceptions`).

## 6. Cores and Claims (C-rules)

- **C1 — Core what you own.** Every culture-state cores all its starting provinces.
- **C2 — Core your culture area.** A single-country culture-state also holds cores on *all* provinces of its own culture, including any it does not start with (mixed-zone overrides, Tier C survivors). In a multi-country culture (E9), each state cores its own partition and holds **permanent claims** on the rest of the culture area — any of them can win the intra-culture race to Tier 1, with the staple starting strongest. Either way, unifying your own culture is the cheapest possible war goal.
- **C3 — Claims ladder into the group.** Permanent claims on the culture group's area are **not** given at start. Mission/decision content grants claims on the formation set (§7) progressively, gated on Tier 1 (own-culture) unification progress.
- **C4 — Formation reward.** Forming the group nation grants cores/permanent claims on the full formation-set area, and — for UK, France, Spain, and Germany — the existing **modern-border permanent claims** from MDD §7.3 attach at this moment. The Alsace-Lorraine contested-zone rules are unchanged.
- **C5 — No sanctioned cross-group expansion.** No claims outside your own culture group in Tier A. Conquest outside the group triggers the Balance of Power deterrent (§8, A3).

## 7. The Unification Ladder & Formable Nations (F-rules)

- **F1 — Tier 1: unify the culture.** Owning ~90–100% of the culture area fires a "United <Culture>" event/decision: government rank up, small national buffs, and it unlocks Tier 2 mission content. In multi-country cultures (E9) this is a race between the same-culture states — whoever unifies the culture takes the rank-up. Tunable threshold.
- **F2 — Tier 2: form the nation.** The group formable requires: primary culture in the formation set, not a subject, at war with no one (vanilla convention), and ownership of a defined share of the formation-set area or a curated key-province list. Effects: tag switch, modern national flag, formation-set cores/claims (C4), and the colonization upgrade package (K3).
- **F3 — Formation sets are curated, not vanilla culture groups.** A **formation set** is a curated list of cultures + area per formable, maintained in `Tooling/culture_states/formation_sets`. It can cross vanilla culture-group lines (the UK set includes English, Scottish, Welsh, Irish, Highlander even though vanilla splits them across groups; Breton belongs to the France set, not the UK set).
- **F4 — Reuse vanilla formable tags.** `SPA`, `GBR`, `FRA`, `GER`, `ITA`, `IRE`, `NED`, etc. Where the target tag exists at start as a culture-state (e.g., `FRA` as the Francien state, `ENG` as the English state), forming the nation is a tag switch into it — the vanilla "form Spain" pattern.
- **F5 — One canonical formable per set; historical rivals allowed.** Spain is the Iberian formable and **excludes Portugal** (existing owner decision). Andalusia (`ADU`) may remain as a competing historical formable. Similar rival formables are decided per wave.
- **F6 — Anchor examples.**

| Formation set | Formable | Member culture-states (indicative — tooling finalizes) |
|---|---|---|
| Iberian (minus Portuguese) | **Spain** (`SPA`) | Castile, Aragon, Catalonia, Galicia, León, Navarra (Basque), Granada (Andalusian) |
| French | **France** (`FRA`) | Francien, Norman, Gascon, Occitan, Burgundian, Breton, Walloon-area states |
| British Isles | **Great Britain / UK** (`GBR`) | England, Scotland, Wales, Ireland, Highlands |
| German | **Germany** (`GER`) | German subculture states at vanilla-style HRE density (§4A): many princes per subculture, anchored by staples (Bavaria, Saxony, Brandenburg, …) |
| Italian | **Italy** (`ITA`) | Lombard, Tuscan, Neapolitan, Sicilian, Sardinian, etc. |
| Indian (tiered) | **India / Bharat / Hindustan** (vanilla `BHA`/`HIN` where they fit) | Strong regional/culture states plus some smaller states (§4A) — exact sets defined in the Wave 7 data package |

Equivalent sets are defined per rollout wave for the rest of Tier A (Scandinavia, the Balkans, North Africa, the Middle East, Asia).

## 8. AI Unification Behavior (A-rules)

- **A1 — Claims steer the AI.** EU4's AI strongly prefers cored/claimed targets. C2 cores (own culture) plus C3 mission claims (group, unlocked later) naturally sequence AI expansion: own culture first, group second.
- **A2 — AI takes the formables.** Formation decisions carry high `ai_importance`/`ai_will_do`; the vanilla AI reliably takes such decisions when eligible.
- **A3 — Outside-group deterrent.** The MDD's Balance of Power opinion/coalition deterrent is **re-scoped**: it now punishes taking Tier A land *outside your culture group*, instead of "European land from Europeans." Inside-group conquest is the sanctioned path.
- **A4 — Pace targets, not scripts.** Unification pace is tuned against observer targets per wave (e.g., Iberia consolidates to 2–4 states by ~1550; Spain forms between ~1550–1650 in most runs). Levers: mission gating, claim timing, AE/truce natural pacing, deterrent strength. (Risk R-32.)
- **A5 — Unify before you colonize.** AI weighting and the colonization gates in §9 keep culture-states focused on the ladder before overseas play.

## 9. Colonization Behavior (K-rules)

The existing colonization architecture (MDD §8: Exploration lock, Frontier Settlement, colonial regions, head start; §9–10: subjects) is kept. The pivot changes *who* qualifies and *when*:

- **K1 — Same triggers, new membership.** `crown_is_european` / `crown_is_european_colonizer` survive. The **Western European colonial head start** list is re-expressed as a curated set of coastal Western European culture-states and their formables (Portugal, Castile, Galicia, England, Brittany, Normandy, Netherlands-precursors, plus the existing secondary list) — still a curated list, never a geometric rule.
- **K2 — Unification-first gating.** Exploration Ideas and head-start event chains require, in addition to `crown_is_european_colonizer`: a **coastal capital and minimum port/naval presence**, and either Tier 1 unification achieved or membership in the curated head-start list. Tiny inland minors can never rush colonization.
- **K3 — Formation upgrade.** Forming the group nation grants a stronger colonization package (extra colonist, colonial range, naval force limit). Formed nations out-colonize culture-states by design.
- **K4 — Range tiers.** Culture-states get modest colonial range; formables get full range. Combined with K2, this prevents absurd early colonization by tiny minors while letting coastal Western European states become the strongest early colonizers.
- **K5 — Carve-outs survive.** The Ottoman never-a-colonizer carve-out transfers to the Turkish successor state (pending D-1); the Russia/Siberia special case is unchanged. Frontier Settlement remains the only path for non-Europeans (and the Ottoman successor).

## 10. Modern & Regional Flags (G-rules)

- **G1 — No medieval vanilla flags.** Every Project Crown tag ships a modern or clean flag: **formables use modern national flags; culture-states use modern regional/cultural flags.** Anachronism is the intended aesthetic.
- **G2 — Anchor flags (owner-set):** England = **St George's Cross**; France = **tricolor**; UK = Union Jack; Spain = Rojigualda; Germany = black-red-gold; Italy = il Tricolore. Regional candidates: Catalonia = Senyera, Basque = Ikurriña, Galicia = modern Galician flag, León = purple lion, Andalusia = green-white-green, Brittany = Gwenn-ha-du, Scotland = Saltire, Bavaria = lozenges.
- **G3 — ET Modern Flags is a reference/source candidate only.** It may be used later; **it is not imported now.** Any use requires the same permission/credit handling as the map foundation (Risk R-36, pattern of R-29).
- **G4 — Flags ship with their wave.** The design-time flag mapping table (`Tooling/culture_states/flag_map`) is maintained from now; actual flag *files* (TGA, vanilla flag pipeline) are only added when a rollout wave implements its region. Until a wave's flag pass, placeholder/vanilla flags are acceptable in test builds.

## 11. Excluded Uncolonized Regions

Restating the Tier B rule as hard requirements:

- The **Americas, Sub-Saharan Africa, Australia/Oceania, and the Philippines** start mostly uncolonized. No culture-states are created there.
- Colonial regions (MDD §8.4) and development flattening (MDD §6) apply there unchanged.
- Native/tribal presence: the Americas and Oceania keep their (already mostly-uncolonized) vanilla native setup. Sub-Saharan Africa's organized states are Open Decision D-4.
- **North Africa is not excluded** — it is Tier A and fragments into culture-based countries (Maghrebi and Egyptian-area cultures).

## 12. Rollout Order & Iberia Proof of Concept

Implementation proceeds in **waves**, each shipping: tags + starting ownership + cores/claims + formation set + AI weights + a vanilla-content audit + flags for that region.

1. **Wave 1 — Iberia** (proof of concept; staples Castile and Aragon)
2. **Wave 2 — France** (D-8 resolves here: France as Francien staple at start vs. formable-only)
3. **Wave 3 — Britain & Ireland** (staple England, St George's Cross)
4. **Wave 4 — Italy & Germany** (HRE at vanilla-style density per §4A — members tweaked for culture coherence, count preserved; Germany formable above the sandbox)
5. **Wave 5 — Rest of Europe** (Scandinavia, Balkans, Eastern Europe; horde decision D-6)
6. **Wave 6 — North Africa & Middle East** (Ottomans exist as the staple Turkish power per §4A, carve-outs unchanged)
7. **Wave 7 — Asia** (Japan mostly vanilla per §4A; China regional-states-first per §4A/D-3; India granular-but-strong with the Bharat/Hindustan path per §4A)

**Why Iberia first:** it exercises the entire ladder in the smallest package. ~8 culture-states of which **7 reuse existing vanilla tags** (`CAS`, `ARA`, `GAL`, `LON`, `NAV`, `GRA`, `POR`) and only ~1 new tag is needed (Catalonia); a clean peninsula boundary; a vanilla formable target (`SPA`) with an owner-decided rule already in place (Spain excludes Portugal); a competing formable (`ADU`) to test rival formation; and the flagship colonizers (Castile, Portugal) to later test the unification-then-colonization sequence end to end.

**Wave 1 exit criteria:** mod loads with the Iberian culture-states; **starting borders pass the O7 cleanliness review** (validator clean or exceptions justified, visual in-game check); Iberian vanilla content audited (Iberian Wedding, Reconquista-era events disabled/reworked as needed); observer runs show Iberia consolidating to 2–4 states by ~1550 and Spain forming in most runs by ~1650; no crashes; log clean.

## 13. Interactions with Existing Systems

| Existing system | Effect of the pivot |
|---|---|
| MDD §7.3 modern-border claims | Become the Tier 2 formation reward (C4). Province lists still tooling-maintained. |
| MDD §7.4 Alsace-Lorraine | Unchanged; activates on German formation exactly as decided. |
| MDD §7.2 Burgundian Inheritance / Iberian Wedding rework | Largely superseded — the vanilla setups those events assume no longer exist. Each rollout wave's audit disables or replaces them (R-31). |
| Lucky nations replacement | Still needed; the curated list now names culture-states/formables. |
| HRE "mostly vanilla in v1" | **Resolved (owner rule 2026-07-06, §4A):** HRE nation count stays close to vanilla; members tweaked, sandbox density preserved; vanilla HRE mechanics kept in v1. Residual mechanical risk tracked as R-33. |
| Ottoman carve-out (owner decisions 1, 10) | **Resolved (owner rule 2026-07-06, §4A):** the Ottomans exist as the staple Turkish-group country and keep the carve-out unchanged — major regional power, never a Western colonial country. |
| Russia special case (owner decision 6) | Unchanged in substance; which culture-state(s) inherit it depends on the East Slavic fragmentation mapping (Wave 5). |
| 1914 alt-history layer (Rule 28) | Largely **absorbed** by the formable ladder; the 2026 layer stays post-v1. |
| No-straits, dev flattening, colonial regions, subject taxonomy, assimilation | Unchanged. |

## 14. Decisions — Resolved and Open

Logged here and in MDD §15; open items must be resolved before the wave that needs them.

**Resolved by owner rules of 2026-07-06 (round 2):**

| ID | Decision | Resolution |
|---|---|---|
| **D-1** | Ottoman Empire disposition | **Resolved — Ottomans survive** as the staple Turkish-group country (§4A): all or the majority of Turkish culture land (balance-tunable), major regional power, never a Western colonial country; carve-outs unchanged. Their non-Turkish land fragments normally. |
| **D-2** | HRE handling | **Resolved — keep vanilla-style density** (§4A): HRE nation count stays close to vanilla, members tweakable, no collapse and no massive expansion; vanilla HRE mechanics in v1. |
| **D-5** | Japan | **Resolved — mostly vanilla** (§4A): keep the Sengoku daimyo setup, tweak only as needed, break up further only if testing shows a need, never a unified 1444 Japan. |

**Still open:**

| ID | Decision | Needed before | Recommendation |
|---|---|---|---|
| **D-3** | China: fragment Ming, and if so how far? **High-risk** (Mandate of Heaven, Ming/Qing content, tributaries, dense development, AI snowball — R-39). | Wave 7 | **Regional Chinese states first** — a handful of strong regional powers, never one-province fragmentation; deeper fragmentation only after its own content audit. |
| **D-4** | Sub-Saharan Africa "mostly uncolonized": remove/downgrade organized states inside colonial regions only, or clear the whole subcontinent? | Phase 1 dev/colonial-region pass | **Remove/downgrade inside colonial regions; keep interior empires** (Mali, Ethiopia) in v1. |
| **D-6** | Steppe hordes (Golden Horde, Uzbek, Oirat…): fragment by culture or keep as hordes? | Wave 5–7 | Keep hordes in v1 (Tier C); fragmentation adds little and horde mechanics resist it. |
| **D-7** | Naming for non-staple culture-states: regional names (recommended) vs. dynastic/vanilla names. Staples carry their national name by definition (England, Castile, Aragon, the Ottomans…). | Wave 1 | Regional names for non-staple culture-states; staples and formables own the national names. |
| **D-8** | France at start: Francien staple country named France (default per E8), or `FRA` reserved strictly as the formable with a differently-named Francien staple? | Wave 2 | **Staple France exists at start** (E8 default); reserve-as-formable only if Wave 2 design shows the ladder reads better that way. |
