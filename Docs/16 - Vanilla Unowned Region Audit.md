# Project Crown: Vanilla Unowned Region Audit

**Date:** 2026-07-08
**Branch:** `iberia-poc-polish`
**Scope:** Phase 2C.3 audit of vanilla 1444 land ownership against Project Crown province-history overrides.

## What Was Audited

The audit script reads vanilla EU4 province history from:

`/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV/history/provinces`

It also checks Project Crown province-history overrides under:

`Mod Build/project_crown/history/provinces`

For each land province, the audit records province ID, province name, owner/controller at 1444 if present, culture, religion, area, region, superregion, continent, whether vanilla starts it unowned/uncolonized, and whether Project Crown currently overrides the province.

Audit outputs:

- `Tooling/culture_state/audits/global_vanilla_unowned_audit.json`
- `Tooling/culture_state/audits/excluded_region_unowned_audit.json`
- `Tooling/culture_state/audits/africa_unowned_audit.json`
- `Tooling/culture_state/audits/asia_unowned_audit.json`
- `Tooling/culture_state/audits/australia_oceania_unowned_audit.json`
- `Tooling/culture_state/audits/philippines_unowned_audit.json`

## Project Crown Override Status

Project Crown currently has **62** province-history overrides, all in the Iberian POC scope. It has **0** non-Iberian province-history overrides and **0** non-Iberian owner/controller changes.

That means the current Project Crown ownership layer matches vanilla outside Iberia. The map foundation is imported, but non-Iberian starting ownership has not been overhauled.

## Summary By Design Region

| Design region | Land provinces | Vanilla owned | Vanilla unowned/uncolonized | Project Crown owner/controller changes |
|---|---:|---:|---:|---:|
| Americas | 783 | 221 | 562 | 0 |
| Sub-Saharan Africa | 350 | 261 | 89 | 0 |
| North Africa | 88 | 87 | 1 | 0 |
| Australia/Oceania | 87 | 27 | 60 | 0 |
| Philippines | 23 | 13 | 10 | 0 |
| Asia excluding Philippines | 1109 | 1035 | 74 | 0 |

Global land audit: **3272** land provinces, **2472** vanilla-owned, **800** vanilla-unowned/uncolonized.

Excluded colonial-open regions combined - Americas, Sub-Saharan Africa, Australia/Oceania, and the Philippines - contain **1243** land provinces: **522** vanilla-owned and **721** vanilla-unowned/uncolonized.

## Region Readout

The Americas are mostly unowned in vanilla, but not empty. The audit finds 221 vanilla-owned land provinces and 562 unowned/uncolonized land provinces. Many unowned provinces also carry `tribal_owner`, which should be treated as native presence data, not normal 1444 ownership.

Sub-Saharan Africa is heavily populated in vanilla: 261 owned land provinces and 89 unowned/uncolonized. A future open-region phase cannot simply clear everything by continent; it needs owner-approved exceptions and probably a separate decision for organized states.

North Africa is almost entirely populated in vanilla: 87 owned land provinces and 1 unowned/uncolonized. It remains a populated Tier A region and is not part of any Sub-Saharan clearing pass.

Australia/Oceania is mixed: 27 owned land provinces and 60 unowned/uncolonized. It needs a future open-region clearing pass if Project Crown wants it mostly uncolonized.

The Philippines are mixed: 13 owned land provinces and 10 unowned/uncolonized. They are a special future mostly-uncolonized region, not part of the general Asia-populated rule.

Asia excluding the Philippines is overwhelmingly populated: 1035 owned land provinces and 74 unowned/uncolonized. Asia should remain generally populated unless a specific later decision approves an exception.

## Regions Needing Future Clearing Or Opening

- Americas: preserve vanilla-unowned land and review remaining vanilla-owned/native exceptions deliberately.
- Sub-Saharan Africa: future clearing/opening phase required, with organized-state exceptions decided before implementation.
- Australia/Oceania: future clearing/opening phase required.
- Philippines: future mostly-uncolonized phase required, with explicit exceptions approved first.

## Regions That Should Remain Populated

- North Africa.
- Asia excluding the Philippines.
- Europe and other Tier A rollout regions unless their specific wave design says otherwise.

## Risks

- Clearing from visual inspection can erase intentional vanilla-owned states.
- `tribal_owner` is not the same as normal province `owner`; scripts must preserve the distinction.
- Sub-Saharan Africa and the Philippines have many vanilla-owned provinces, so making them mostly uncolonized requires explicit design exceptions rather than a blanket assumption.
- These audits use vanilla area/region/continent data for classification. Future custom colonial-region work should re-run or extend the audit after region files change.

## Recommended Next Phase

Run a dedicated open-region design phase before any ownership edits. That phase should use these JSON audits as the source of truth, decide approved exceptions for each excluded region, then generate a reviewable clearing plan before touching province history.

No province ownership changes were made in this audit phase.

## Phase 2E Addendum

Phase 2E added a limited Atlantic-island start cleanup at the user's request. Project Crown now overrides the Canarias (`366`), Tenerife (`4565`), the Azores (`367`), and Madeira (`368`) so they are unowned at the 1444 start. Cape Verde (`1096`) was audited and left unchanged because it already starts unowned in vanilla 1444.

This is a narrow Atlantic-island exception, not the full open-region phase. No mainland Africa, Americas, Asia, Australia, or Philippines province history was cleared or overhauled.
