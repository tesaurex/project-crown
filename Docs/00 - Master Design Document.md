# Project Crown: Europa Ascendant — Master Design Document

**Version:** 0.4 - Personalized Borders foundation priority applied; owner decisions of 2026-07-04 and 2026-07-06 recorded; map compatibility gate open
**Date:** 2026-07-06
**Status:** Approved rule set with Phase 1A map-foundation research added; local skeleton and temporary smoke-test decision exist; no real gameplay mechanics implemented
**Base game:** Europa Universalis IV v1.37.5.0 Inca, 1444 start date; intended province/border foundation is Personalized Borders if it can be made compatible

---

## 1. Vision

Project Crown: Europa Ascendant is a full overhaul of EU4 built on a locked province/border foundation. The intended foundation is now the province and border work from **Personalized Borders: Fixes & Historical Borders** (Steam Workshop ID `3418818231`), provided it can be made compatible with EU4 v1.37.5.0 Inca. The overhaul reshapes the game around one central historical dynamic: **Europe projects power outward.** European nations hold a structural advantage in technology, institutions, colonization, and naval power — but no single European major is scripted to win. Instead of blobbing across Europe, the great powers compete for the world: colonies, trade dominance, and overseas empires are the victory currency. The rest of the world is not helpless, but it plays a different game — defense, frontier settlement, and survival against imperial pressure.

## 2. Design Pillars

1. **Europe outward, not inward.** European majors should find overseas expansion cheaper, safer, and more rewarding than conquering each other. Intra-European conquest is discouraged except for historical formation paths (Great Britain, Spain, France consolidation, etc.).
2. **Balanced Europe, dominant Europe.** Europe as a bloc has the upper hand globally, but internally no European major has a guaranteed day-one victory path.
3. **Empire is a structure, not a paint bucket.** Distant conquest and colonization produce *subjects* — Colonial Administrations, Overseas Dependencies, Dominions — not directly stated provinces. Empires look and behave like empires.
4. **Colonization is settlement, not replacement — mostly.** Colonized provinces keep native culture and religion by default. Assimilation is rare, slow, hidden, and driven by economic investment.
5. **Province/border foundation first.** Project Crown must lock the Personalized Borders province/border foundation before no-straits, development rebalance, colonial regions, subjects, or other gameplay systems. Alternate-history border support (1914 / 2026 styles) comes later through formables and decisions, within the limits of the locked foundation.

## 3. Scope & Ground Rules

- **Map:** Intended foundation is Personalized Borders: Fixes & Historical Borders (Workshop ID `3418818231`) if the EU4 v1.37.5.0 compatibility risks can be resolved. Do not continue gameplay-system implementation until this foundation is locked. See [06 - Personalized Borders Foundation Research](06%20-%20Personalized%20Borders%20Foundation%20Research.md).
- **Map import status:** Not imported yet. Phase 1A was research/documentation only.
- **Start date:** 1444 only. No alternate bookmarks in v1.
- **Environment and DLC profile:** Design targets Europa Universalis IV v1.37.5.0 Inca with the confirmed DLC/content profile recorded in [05 - Environment and DLC Profile](05%20-%20Environment%20and%20DLC%20Profile.md). Future mechanics must not assume unconfirmed DLC, and any DLC-dependent mechanic must document its dependency before implementation.
- **Compatibility:** Standalone overhaul. No compatibility patches for other overhauls in v1.
- **No real gameplay mechanics yet.** The mod currently contains only the local skeleton and temporary smoke-test decision. This document and its companions are the contract for implementation. Implementation begins with the Phase Plan (see [01 - Phase Plan](01%20-%20Phase%20Plan.md)).

## 4. Key Definitions

These definitions are used by every system below and must be implemented as **scripted triggers** so every system agrees on them.

| Term | Definition | Implementation note |
|---|---|---|
| **European nation** | A nation whose capital is on the Europe continent at game start (1444). Locked in with a hidden country flag on startup so capital-moving cannot change status. | Scripted trigger `crown_is_european` (geographic/balance tier). Remaining edge cases (Muscovy/Russia, Byzantium) resolve European under this rule. |
| **European colonizer** | European nations minus explicit carve-outs (currently: the Ottomans). Only this tier can take Exploration Ideas and use true overseas colonization. | Scripted trigger `crown_is_european_colonizer`. |
| **European-adjacent great power (Ottomans)** | The Ottomans are **partial European**: balanced as a European-tier great power, but never a colonial European. **Permanently barred** from normal Exploration Ideas (only an explicit later design decision can change this), never counted as a Western European colonizer. They may use Frontier Settlement where valid (§8.3); disconnected overseas conquests become Overseas Dependencies (§10); Anatolia keeps vanilla development (§6). | Owner decision 2026-07-04. Tag-specific carve-out flag. |
| **Russian overland expansion (special case)** | Russia is a special European-adjacent expansion case: contiguous overland expansion into Siberia is **connected land** and may be stated directly — it is overland settlement, not overseas colonization, and Siberia is never a colonial region (§8.4). Russia is **not** a Western European overseas colonizer at game start (no head-start package). Disconnected overseas land (Alaska, far Pacific islands) goes through the colonial/overseas subject system like everyone else's (§10). | Owner decision 2026-07-04. |
| **Western European colonial power** | Subset of European colonizers designated for the colonial head start: Portugal, Castile, Aragon, England, France, plus a curated secondary list (Netherlands-formers, Denmark, Norway, Scotland, Brittany, Genoa). The Ottomans are never in this set. | Curated tag/culture list in a scripted trigger, not a geometric rule. |
| **Home region** | The region(s) inside which a nation's "home claims" (missions, permanent claims, cheap cores) live. Defined per major nation (§7.3). | Province lists maintained in tooling, emitted to history/mission files. |
| **Connected land** | A province that can reach the owner's capital through a chain of provinces owned by the same country, using land adjacency only (no strait or sea hops — there are no straits). | Approximated in script; exact algorithm defined during implementation of §10. |
| **Overseas disconnected land** | Owned land outside the capital's continent that does not border connected owned land. | Drives the forced-subject rule (§10). |
| **Colonial region** | A map zone (moddable file) where cored overseas provinces automatically aggregate into a colonial nation. | Rebuilt globally per §8.4. |

## 5. Map & Movement

### 5.0 Province/Border Foundation Gate
Project Crown's first map priority is no longer "vanilla map first." The project should use the Personalized Borders province/border foundation if it can be made compatible with EU4 v1.37.5.0 Inca.

This gate comes before every dependent world or gameplay layer:

- No straits removal until the final province bitmap and positions are locked.
- No development rebalance until province IDs and province availability are confirmed.
- No colonial regions until the final province/border foundation is loaded cleanly.
- No subject framework, mission, claim, event, idea, fort, assimilation, or Back War Effort work until the foundation is stable enough for those systems to target.

Phase 1A found that the reference mod supplies only `map/provinces.bmp` and `map/positions.txt`. It appears to redraw borders using vanilla province colors rather than adding a new province-ID schema, but it needs a compatibility pass for undefined bitmap pixels, absent vanilla bitmap IDs, and missing 1.37.5 position entries. No import happened during Phase 1A.

### 5.1 No Straits (Rule 1)
After the province/border foundation is locked, all strait crossings are removed. Armies cross water only by naval transport.

- **Implementation:** Full override of `map/adjacencies.csv`, deleting every sea-crossing adjacency. Canal and impassable entries are preserved.
- **Consequences accepted by design:**
  - England, Denmark, the Ottomans (Bosphorus), Japan, and Indonesia become genuinely naval powers or genuinely isolated. This reinforces the naval-power pillar.
  - Strait-blockade mechanics disappear entirely.
- **Known risk:** EU4 AI is historically weak at naval invasions. Removing the Channel and the Øresund may make AI England/Denmark passive. This is the single biggest AI-behavior risk in the mod — see Risk Register R-15. Mitigation is AI-side (transport fleet weighting, mission nudges), evaluated in playtests.

### 5.2 Fort Capture (Rule 21)
When a fort falls, the surrounding provinces should fall with it.

- Vanilla Zone of Control already flips control of most surrounding unfortified provinces when a fort is sieged down. Project Crown makes this **explicit and complete**: on fort siege won, all non-fort provinces in the fort's area/ZoC flip to the besieger's control, including edge cases vanilla misses.
- **Implementation:** `on_siege_won` on_action hook if available (verify in Phase 0), otherwise a monthly control-sweep event. This affects **military control during war only**, not ownership at peace — ownership transfer at peace deals is hardcoded per-province and out of scope (Risk R-12).

## 6. World Development Rebalance (Rule 2, amended)

Development flattening is blocked until the Personalized Borders foundation is locked. Once the foundation is stable, flattening applies **only to three designated colonial macro-regions**: the **Americas**, **Australia/Oceania**, and **all of Africa**.

- **Asia is untouched.** India, China, Japan, mainland Southeast Asia, and the rest of Asia keep vanilla development unless a later, specific balance change targets them. This explicitly includes **Anatolia** — the Ottoman heartland is never flattened.
- **Europe is untouched** in this pass. Europe's internal balance is handled separately (§7).

Within the flattened regions, provinces are set in history files (not startup events — history edits are cleaner, lag-free, and moddable downstream):

| Province class | Tax / Production / Manpower | Classification rule (precedence top-down) |
|---|---|---|
| **Capital** (of any 1444 nation in a flattened region) | 1 / 2 / 2 | Is a country capital in 1444 history |
| **Trade post / port / trade hub** | 1 / 2 / 1 | Has a Center of Trade, estuary modifier, is a trade-node capital, or is coastal (has port) |
| **Normal province** | 1 / 1 / 1 | Everything else in a flattened region |

- **Implementation:** A tooling script (Python) reads vanilla `history/provinces/`, classifies every province in the three macro-regions, and emits overridden history files. Manual override list for special cases.
- **Accepted consequences (must be monitored in balance passes):**
  - Trade value collapses in the flattened zones → colonial and trade-company income there needs a dedicated rebalance pass. Asian trade wealth stays vanilla and remains a prize worth competing for.
  - States in the flattened regions become militarily weak → this is the colonial-frontier lever; the pace of European steamrolling there is throttled by distance, attrition, and the subject-income cuts in §9, not by native strength.
  - Because Asia keeps vanilla development, Europe's upper hand over Asia comes from technology, institutions, naval power, and the subject framework — not from a dev gap. Asian majors remain real obstacles, which is intended.
  - Very low manpower in flattened regions may leave local AI unable to suppress rebels → watch for regional instability; a stability pass is budgeted in the balance phase.
  - Institution spawn/growth conditions that key off development must be audited so institutions stay Europe-born (§7.1).

## 7. The European Power Framework

### 7.1 Europe's Global Upper Hand (Premise)
Europe's advantage comes from four stacked levers, none of which is "Europe gets +20% discipline":

1. **Development gap in the colonial zones** (§6) — the Americas, Africa, and Oceania are flattened, so Europe out-develops every colonial frontier. Asia keeps vanilla development; Europe's edge over Asia rides on levers 2–4 plus the subject framework, not raw development.
2. **Institutions** — institution spawn conditions are edited so all institutions through Global Trade originate in Europe or European colonial holdings. Spread to other continents is slowed.
3. **Technology** — vanilla tech groups already encode this; audited, not rebuilt, in v1.
4. **Naval & colonial monopoly** — Exploration Ideas are Europe-only (§8.2); everyone else gets Frontier Settlement (§8.3).

### 7.2 Internal European Balance (Premise)
No European major gets a guaranteed win. Concretely:

- **PU/inheritance mega-events are reined in.** The Burgundian Inheritance and Iberian Wedding are reworked to be slower, conditional, or compensated — no day-one snowball chains. (Historical formations still possible: Spain via Castile+Aragon remains a supported path.)
- **Lucky nations** are replaced with a curated, balanced list (or disabled) so the AI field stays competitive.
- **Mission trees of European majors are redirected outward:** claims and rewards point at colonial regions, trade nodes, and naval targets, not at each other's cores — except historical formation steps.
- **Intra-European conquest deterrent:** aggressive expansion, coalition, and opinion consequences for taking European land from Europeans are sharply increased via an event-driven "Balance of Power" opinion system (AE itself is only globally tunable — see Risk R-11). Historical formation paths (GB, Spain, France's home region, Italy, Germany-era formables) are exempted via decision/mission framing.
- **HRE: mostly vanilla in v1.** No HRE overhaul until the core colonial, subject, development, and claim systems are stable. Observer games are monitored for HRE blobbing or passivity (Phase 7); findings feed a post-v1 decision.

### 7.3 Home Claims — Permanent Modern-Border Claims (Rules 3–5, amended)
"Home claims" are the only cheap, sanctioned expansion inside Europe: **permanent claims**, mission claims, and reduced coring/AE treatment, strictly limited to a defined home region per nation. Owner decision (2026-07-04): the four anchor nations below receive permanent claims matching their **modern (present-day) borders**.

| Nation | Permanent claim zone | Notes |
|---|---|---|
| England / Great Britain (UK) | Modern United Kingdom: Great Britain **plus a Northern Ireland approximation** | GB formation is the sanctioned path. The exact Northern Ireland provinces are **not guessed in design** — they are chosen during the province-ID mapping phase as the best vanilla approximation. The rest of Ireland is **not** a default UK claim — an all-Ireland set may exist later only as a separate optional alternate-history path. No mainland-France mission claims — the Hundred Years' War content is reframed toward disengagement/naval pivot. |
| France | Modern French borders, **including Alsace-Lorraine** | Also includes Savoy, Nice, Corsica, Roussillon, Franche-Comté, French Flanders per the modern line. Alsace-Lorraine is a contested Franco-German core zone (§7.4). |
| Spain (Castile/Aragon/Spain) | Modern (present-day) Spanish borders | Includes Balearics, Canaries, Ceuta/Melilla footholds. **Excludes Portugal** — no sanctioned Iberian annexation; Iberian union content reworked per §7.2. |
| Germany (formable) | Modern German borders, **including Alsace-Lorraine** | Claims attach when Germany forms — normal unifier candidates carry **no automatic contested-zone content** beforehand (§7.4). Alsace-Lorraine is shared contested ground with France (§7.4). |

Other European majors receive home regions in the same spirit during implementation (e.g., Portugal = modern Portugal; Austria/HRE handling stays close to vanilla in v1). Home zone province lists live in tooling as the single source of truth.

### 7.4 Contested Core Zone: Alsace-Lorraine
Alsace-Lorraine belongs to **both** the French and German modern-border claim sets and is a permanent Franco-German flashpoint:

- If **France** gets/owns/forms into its modern borders first, **Germany gains (or retains) cores** on Alsace-Lorraine.
- If **Germany** gets/owns/forms into its modern borders first, **France gains (or retains) cores** on Alsace-Lorraine.
- Both nations may hold cores there **at the same time** — the zone is designed to stay contested, not to resolve.
- **Activation:** the full contested-zone system activates **when Germany forms**, or through a clearly defined late-game German nationalism path. Normal German unifier candidates receive no automatic Alsace-Lorraine content before formation. France's modern-border permanent claims (including Alsace-Lorraine) exist from the start regardless, per §7.3.
- **Implementation:** an event system watching ownership/formation state grants and refreshes the reciprocal cores; the province list is maintained in tooling (`Tooling/home_regions/`).

## 8. Colonization Systems

### 8.1 Western European Colonial Head Start (Rules 6–7)
Western European colonial powers open the game already leaning overseas:

- Starting bonuses at 1444 (via country history / startup flags): bonus colonial range, an early explorer or conquistador event chain, and a national "Age of Discovery Impulse" modifier (colonist chance, range, naval force limit — initial values set in implementation, tuned in balance phase).
- Exploration Ideas are cheaper/earlier for this group (tunable), and their mission trees deliver colonial rewards early.
- Europeans use **true overseas colonization**: the full vanilla colonist system, global colonial regions, colonial nations — upgraded by the subject framework in §9.

### 8.2 Exploration Lock (Rule 8, amended)
Non-European nations — **and the Ottomans** — cannot take Exploration Ideas. For the Ottomans this bar is **permanent unless a later design decision explicitly changes it**: they use Frontier Settlement where valid and Overseas Dependencies for disconnected conquest, and must never drift into a normal Western European-style colonial empire by default. Implementation: a `trigger` block on the Exploration idea group requiring `crown_is_european_colonizer` (Europeans minus the Ottoman carve-out). (Idea-group availability triggers are supported; verified as a Phase 0 spike, Risk R-14 covers grandfathering edge cases.)

Expansion Ideas remain available to all, but any colonist from any source is still bound by Frontier Settlement rules below when the owner is non-European.

### 8.3 Frontier Settlement (Non-European colonization) (Rule 8)
Non-Europeans get exactly one path to new land: settling **directly bordering uncolonized provinces.**

- Delivered as a government reform / decision unlock ("Frontier Settlement") granting **1 colonist** and a deliberately tiny colonial range.
- **Adjacency is the law, range is just the fence.** Colonial range is radial and cannot express "adjacent only" (Risk R-9), so an enforcement event cancels any non-colonizer's colony (non-Europeans and the Ottomans alike) that does not border a province owned by the colonizer.
- Intended users in practice: Manchu/Chinese northern expansion, Sub-Saharan interior powers, American natives expanding into wilderness.
- **Russia is its own special case (§4):** Siberia is deliberately **not** a colonial region (§8.4), so Russia's contiguous overland expansion there is connected land, stated directly — overland settlement, not overseas colonization. Russia gets no Western colonial head start at game start, and any disconnected overseas Russian land (Alaska, far Pacific islands) flows through the colonial/overseas subject system (§10) like anyone else's.
- The **Ottomans** fall under Frontier Settlement rules for any colonization, like non-Europeans — they are not a colonial European power (§4).

### 8.4 Global Colonial Regions (Rule 9)
Colonial regions are rebuilt as a **global** set only after the Personalized Borders foundation is locked. They have two hard constraints: every colonial region must have **ocean access**, and borders must be **clean** (follow the locked foundation's area/region boundaries as much as possible, no orphan pockets).

Design criteria for where colonial regions exist:

- **Included:** low-state-density, largely uncolonized zones — the vanilla Americas set (audited for border cleanliness), Australia/New Zealand, plus new regions: Coastal West Africa, Kongo & Southern Africa, Coastal East Africa, Madagascar, and **Colonial Philippines & Spice Islands** — a single combined region covering the Philippines, the Spice Islands/Maluku, and nearby island provinces only where needed for clean borders. Ocean-accessible and border-clean like every other region, and explicitly designed as an overseas rivalry arena for Spain, Portugal, the Netherlands, and other European colonizers. Native sultanates inside it (Ternate, Tidore, Sulu, etc.) are accepted; European conquest there routes into colonial nations per the hardcoded rule (R-4).
- **Excluded:** dense civilizations (India, China, Japan, Middle East, North Africa, Southeast Asian mainland, Java/Sumatra) and Siberia (land frontier, not naval colony). Conquest in excluded zones flows into **Overseas Dependencies** (§9.2), not colonial nations.
- **Critical hardcoded interaction (Risk R-4):** any cored overseas province inside a colonial region is auto-transferred to a colonial nation. Colonial region placement is therefore the *routing switch* between "this becomes a Colonial Administration" and "this becomes an Overseas Dependency." The region map must be designed with that in mind, and colonial regions must not overlap trade-company regions.

### 8.5 Colonial Nation Lifecycle (Rules 10–11, 23)
- **Formation:** vanilla threshold — 5 cored provinces in a colonial region (vanilla define; unchanged, but pinned in our defines override so future patches can't drift it).
- **On formation, immediately:**
  - The new colonial nation receives **+1 colonist** (triggered modifier keyed to being a Crown colonial subject; verified as a Phase 0 spike).
  - The colonial **capital converts** to the parent nation's culture and religion (formation-hook event).
  - All **other provinces keep native culture and religion** (§12).

## 9. The Subject Taxonomy (Rules 12, 14–19)

Three subject types carry the empire structure. All are defined in `common/subject_types` (moddable), based on vanilla types via `copy_from`, with behavior tuned by subject/overlord modifiers.

| | **Colonial Administration** | **Overseas Dependency** | **Dominion** |
|---|---|---|---|
| **Who gets one** | European colonial subjects (evolution of vanilla colonial nation) | Any nation's disconnected overseas conquest (§10) | Conversion offered when a colonial subject's liberty desire exceeds 50 |
| **How it forms** | 5 cored provinces in a colonial region | Forced-subject rule on disconnected conquest | Overlord-side event/interaction, player choice or late-game AI |
| **Force limit / manpower to overlord** | ~30% | Between CA and Dominion (tuned in implementation; suggest ~20%) | 10% |
| **Income to overlord** | ~20% (must not crush the colony's own growth) | Moderate (suggest ~25–30%, it's extraction, not partnership) | 50% reduction vs. what a CA would pay |
| **Liberty desire** | Vanilla-like behavior | Elevated baseline (it was conquered, not settled) | **−60 flat** |
| **AI usage** | Default for AI colonizers | Automatic via §10 | **AI must not create Dominions until late game** (age/year gate, e.g. Age of Revolutions — tuned later) |

Notes:

- Colonial Administration should stay as close to the hardcoded `colonial_nation` type as possible (ideally *is* the vanilla type, re-tuned) to keep tariffs, colonial wars, naming, and map-color behavior — Risk R-5 covers what custom types lose.
- Exact hooks for per-type force-limit/manpower/income percentages are limited (Risk R-7); the table above is the design target, implemented with the closest available combination of subject-type attributes and modifiers.

### 9.1 Diplomatic Slots (Rule 12)
Colonial subjects must not cost diplomatic relation slots **if the overlord has Exploration Ideas.** `takes_diplo_slot` is static per subject type and cannot be conditioned on ideas (Risk R-6). Approved workaround: colonial-type subjects keep their vanilla no-slot behavior where it exists, and the Exploration finisher grants `+diplomatic_upkeep` sized to cover subject overhead for the others.

### 9.2 Independence Requires War (Rule 18)
- **AI overlords can never peacefully release a colonial subject as independent.** Independence happens through independence wars (supported or solo) only.
- The release action itself is hardcoded diplomacy (Risk R-8); enforcement is a layered mitigation: verify subject-type attributes that gate release, and accept that vanilla AI essentially never voluntarily releases subjects anyway. Player-side peaceful release remains legal.

### 9.3 Trade Companies (interim only)
Vanilla trade companies are **not** the final Project Crown system — they are scaffolding so the mod can be built in phases:

- **Early phases:** trade companies remain vanilla, audited for colonial-region overlap (§8.4). This is a deliberate temporary state.
- **Long-term goal:** disconnected overseas land lives in the subject taxonomy — Colonial Administrations, Overseas Dependencies, Dominions — or in a later custom **Trade Post Charter** system.
- **Scheduled decision point (Phase 7; Risk R-19):** trade companies are ultimately **disabled, replaced, or converted** into the custom overseas subject/trade-post system, decided against stable observer-run data. If the Trade Post Charter system is chosen, building it is Phase 8+/post-v1 scope.

## 10. The Disconnected Conquest Rule (Rules 13, 15)

**Overseas disconnected land cannot be held directly.** If a country takes ownership of land outside its capital continent/area that does not border connected owned land, that land is packaged into a subject:

- Inside a colonial region → the hardcoded engine already routes it into the colonial nation → **Colonial Administration**. (This is the one place a hardcoded behavior works *for* us.)
- Outside colonial regions → a scripted enforcement system detects disconnected overseas ownership and forces creation of (or transfer into) an **Overseas Dependency**.
- **Non-colonizers, including the Ottomans:** every disconnected overseas conquest becomes an **Overseas Dependency** — they have no Colonial Administration path. If the engine auto-routes a non-colonizer's cored land inside a colonial region into a colonial nation (R-4), a script converts that subject into an Overseas Dependency.

Implementation reality (Risk R-1): peace treaties cannot be modded to produce subjects directly, so enforcement is **post-hoc**: an on-action/pulse detects violating provinces after a peace, then an event seizes them into a Dependency (with player-facing framing — "the court establishes a colonial charter" — not a silent gotcha). Edge cases (capital moves, land bridges formed later, subject inheritance) get explicit rules during implementation.

## 11. Warfare & Diplomacy

### 11.1 Back War Effort (Rule 20)
A limited "join someone else's war" system:

- **Eligibility:** the backer must have **+50 opinion** of the country it backs; the war must be active; the backer must not already be in the war.
- **Defensive backing (joining the defender's side): easier.** Lower cost (design target: modest prestige + ducat cost, no stability hit).
- **Offensive backing (joining the attacker's side): more expensive.** Higher cost (design target: significant ducats + prestige, possible stability cost) and stricter eligibility.
- **AI usage is allowed but strait-jacketed:** no active loans/low debt, healthy manpower (>50%), war exhaustion below a low threshold, not already at war beyond the target war, and a long per-country cooldown after any backing. All thresholds are tunables.
- **Implementation reality (Risk R-2):** diplomatic actions are hardcoded — this cannot be a real diplo-action button. It ships as a decision/event interface. Scripted war-joining effects are limited and coarse (`join_all_offensive_wars`-style effects join *all* of a target's wars); Phase 0 must prototype whether per-war joining is achievable, with a declared fallback design (backing = subsidies + military access + war-taxes package) if true joining proves impossible.

### 11.2 Fort Capture
See §5.2.

## 12. Culture, Religion & Assimilation (Rules 22–27)

### 12.1 Defaults
- **Colonized provinces keep native culture and religion.** The hardcoded colonization result (colonizer's culture/religion) is reverted by a post-colonization correction system using a tooling-generated province→native-culture/religion lookup (scripted effects), fired from the best available hook (colony-finished on_action if it exists — Phase 0 spike — else pulse). (Risk R-3)
- **Exception:** the colonial capital converts to the parent's culture/religion when the colonial nation forms (§8.5).

### 12.2 Assimilation (the only other conversion path)
- Conversion of other colonial provinces happens **only** through **rare, hidden assimilation events** — no player button, no visible progress bar. Pulse-driven, low base chance.
- **Boosters:** development of the province by the colonial nation or its parent boosts assimilation odds. **Production development counts roughly double** tax or manpower development. (Mechanically: assimilation weight scales with current dev, production dev double-weighted; plus an "Assimilation Momentum" province modifier applied on dev-up if a usable dev hook exists — Phase 0 spike.)
- **Hard blockers — assimilation cannot fire while any of these hold:**
  - separatism / recent-conquest nationalism active
  - unrest above zero
  - any devastation
  - rebellion in the province within the last N years (tracked via flags)
  - the colonial nation's liberty desire above 50
  - the province is a religious center (Center of Reformation, holy site)
  - the province is the original capital of a major native state (curated list: Tenochtitlan, Cusco, Cahokia-tier picks, etc.)

## 13. Long-Term: Alternate-History Border Support (Rule 28)

Post-v1 goal, explicitly **after** the core systems are stable:

- **1914 layer:** formables/decisions producing plausible 1914 borders — Germany, Italy (partly vanilla), Belgium, Romania, Serbia, Greece expansion, unified colonial empires — as close as vanilla provinces allow.
- **2026 layer:** decisions for modern-style nations (post-colonial independence outcomes, national unifications) as an end-game flavor layer.
- Both layers ride on the subject framework: Dominions and independence wars are the narrative machinery for decolonization-era borders.
- Accuracy is bounded by the locked province/border foundation; "accurate-looking," not exact.

## 14. AI Behavior Charter

Every system above carries AI requirements. Summarized in one place:

| System | AI must | AI must not |
|---|---|---|
| European strategy | Prefer colonization/overseas targets; pursue historical formables | Grind neighbors for European land outside home regions |
| Naval invasions | Actually cross water (no straits!) — transport fleet weighting is a first-class balance concern | Go passive when island-locked (England watch item) |
| Frontier Settlement | Use it at a slow, plausible pace | Chain-colonize beyond its borders |
| Dominions | Convert high-LD colonies **late game only** | Create Dominions early |
| Independence | Fight independence wars | Peacefully release colonial subjects |
| Back War Effort | Use it under strict debt/manpower/WE/cooldown limits | Suicide-join wars |

AI control in EU4 is coarse (event `ai_chance`, defines, mission weights); every "AI must" above is a playtest commitment, not just a script commitment.

## 15. Open Design Questions

**None currently open.** Every question raised during design has been resolved by the owner decisions of 2026-07-04 and recorded in Appendix B (rounds 1–2). New questions that surface during implementation are logged here before work on the affected system begins.

One scheduled future decision remains by design (not an open question): the **trade company disposition** — disable, replace, or convert into a Trade Post Charter system — decided at the Phase 7 checkpoint against observer-run data (§9.3, Risk R-19).

## 16. Companion Documents

- [01 - Phase Plan](01%20-%20Phase%20Plan.md) — build order with exit criteria
- [02 - Hardcoded Risk Register](02%20-%20Hardcoded%20Risk%20Register.md) — every place EU4's engine fights this design, with mitigations
- [03 - File & Folder Map](03%20-%20File%20and%20Folder%20Map.md) — mod structure and tooling layout
- [04 - Implementation Order](04%20-%20Implementation%20Order.md) — what to build first, what to defer, and why
- [06 - Personalized Borders Foundation Research](06%20-%20Personalized%20Borders%20Foundation%20Research.md) — Phase 1A research on the intended province/border foundation

## Appendix A — Rule Traceability

Rules 2–5 and 8 are read **as amended** by the owner decisions in Appendix B.

| Rule # | Rule (short) | Section |
|---|---|---|
| 1 | No straits | §5.1 |
| 2 | Dev rebalance (amended scope: Americas, Africa, Oceania) | §6 |
| 3 | England/UK home claims (amended: modern UK) | §7.3 |
| 4 | France home claims (amended: modern France incl. Alsace-Lorraine) | §7.3–7.4 |
| 5 | Spain home claims (modern Spain) | §7.3 |
| 6 | Western colonial head start | §8.1 |
| 7 | True overseas colonization | §8.1 |
| 8 | Exploration lock + Frontier Settlement | §8.2–8.3 |
| 9 | Global colonial regions | §8.4 |
| 10 | CN forms at 5 cores | §8.5 |
| 11 | New CN +1 colonist | §8.5 |
| 12 | No diplo slot cost w/ Exploration | §9.1 |
| 13 | Disconnected land → subject | §10 |
| 14 | Colonial Administrations | §9 |
| 15 | Overseas Dependencies | §9, §10 |
| 16 | Dominions at LD > 50 | §9 |
| 17 | Dominion effects | §9 table |
| 18 | Independence requires war | §9.2 |
| 19 | CA contribution levels | §9 table |
| 20 | Back War Effort | §11.1 |
| 21 | Fort capture | §5.2 |
| 22 | Colonies keep native culture/religion | §12.1 |
| 23 | Colonial capital converts | §8.5, §12.1 |
| 24 | Rare hidden assimilation | §12.2 |
| 25 | Dev boosts assimilation | §12.2 |
| 26 | Production dev boosts most | §12.2 |
| 27 | Assimilation blockers | §12.2 |
| 28 | 1914 / 2026 border support | §13 |

## Appendix B — Owner Decision Log (2026-07-04)

Overrides to the original rule set and resolutions of open questions. Where this log conflicts with an original rule or an earlier assumption, **the log wins** (higher-numbered entries win over lower-numbered ones).

**Round 1 — rule amendments (2026-07-04):**

1. **Ottomans:** partial European — balanced as a European-adjacent great power; never a Western/colonial European; no Exploration Ideas at game start; disconnected overseas conquest becomes Overseas Dependencies; Anatolia keeps vanilla development. (§4, §6, §8.2–8.3, §10)
2. **Development rebalance scope:** only the Americas, Australia/Oceania, and all of Africa are flattened. Asia is untouched — India, China, Japan, mainland Southeast Asia, and most Asian regions keep vanilla development unless later changed for specific balance reasons. The 1/1/1 · 1/2/1 · 1/2/2 class system applies within flattened regions only. (§6)
3. **Alsace-Lorraine:** included in both the French and German modern-border claim sets; permanent contested Franco-German core zone with reciprocal core grants; simultaneous cores allowed. (§7.3–7.4)
4. **Permanent modern-border claims:** UK (Great Britain + Northern Ireland approximation — not all of Ireland by default; all-Ireland only as a possible later optional alt-history path), Spain (modern), France (modern incl. Alsace-Lorraine), Germany (modern incl. Alsace-Lorraine). (§7.3)
5. **Colonial Philippines & Spice Islands:** one combined, ocean-accessible, border-clean colonial region (Philippines + Spice Islands/Maluku + nearby islands only as needed), open to colonial rivalry between Spain, Portugal, the Netherlands, and other European colonizers. (§8.4)

**Round 2 — final open-question resolutions (2026-07-04):**

6. **Russia/Siberia:** Russia is a special European-adjacent expansion case. Contiguous overland Siberian expansion is connected land and may be stated directly; Siberia is never a normal colonial region; Russia is not a Western European overseas colonizer at game start; disconnected overseas land (Alaska, far Pacific islands) uses the colonial/overseas subject system, never direct state ownership. (§4, §8.3–8.4, §10)
7. **Trade companies:** vanilla trade companies are interim scaffolding only, never the final system. Long-term, disconnected overseas land becomes Colonial Administrations, Overseas Dependencies, Dominions, or a later custom Trade Post Charter system. A scheduled Phase 7 decision point (Risk R-19) determines disable / replace / convert. (§9.3)
8. **HRE:** mostly vanilla in v1. No HRE overhaul until the core colonial, subject, development, and claim systems are stable; observer games monitored for HRE blobbing or passivity. (§7.2)
9. **Northern Ireland approximation:** exact vanilla provinces are not guessed in design — they are chosen during the province-ID mapping phase as the best modern-Northern-Ireland approximation. UK permanent claims = Great Britain + that approximation; the rest of Ireland is not a default UK claim (optional alternate-history path only, if ever added). (§7.3)
10. **Ottoman Exploration:** the bar on normal Exploration Ideas is permanent unless a later design decision explicitly changes it. Ottomans use Frontier Settlement where valid and Overseas Dependencies for disconnected conquest; they must not become a normal Western European-style colonial empire by default. (§4, §8.2–8.3)
11. **Pre-Germany Alsace-Lorraine:** normal German unifier candidates get no automatic contested-zone content before Germany forms. The full Franco-German contested-zone system activates when Germany forms, or through a clearly defined late-game German nationalism path. France's modern-border permanent claims (incl. Alsace-Lorraine) apply from the start per the approved France rule. (§7.3–7.4)

**Round 3 — province/border foundation priority (2026-07-06):**

12. **Personalized Borders foundation:** Project Crown should use the province/border foundation from Personalized Borders: Fixes & Historical Borders (Workshop ID `3418818231`) if it can be made compatible with EU4 v1.37.5.0 Inca. This priority supersedes the earlier "vanilla map first" premise. (§5.0)
13. **Foundation sequencing:** Province/border foundation work comes before no-straits, development rebalance, colonial regions, subjects, missions, claims, events, ideas, fort work, Back War Effort, assimilation, and all other gameplay systems. Permission/credit tracking is required before publication or redistribution. (§5.0)
