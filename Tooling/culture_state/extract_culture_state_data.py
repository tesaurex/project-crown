#!/usr/bin/env python3
"""Extract Project Crown culture-state audit tables from vanilla EU4 data."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from eu4_data import (  # noqa: E402
    DEFAULT_PROJECT_ROOT,
    DEFAULT_VANILLA_ROOT,
    build_province_table,
    load_data_context,
    parse_eu4,
    pairs,
    read_text,
    summarize_cultures,
    write_json,
)


IBERIA_CULTURE_TARGETS = {
    "castillian": {"expected_tag": "CAS", "display": "Castile"},
    "aragonese": {"expected_tag": "ARA", "display": "Aragon"},
    "catalan": {"expected_tag": "CAT", "display": "Catalonia"},
    "leonese": {"expected_tag": "LON", "display": "Leon"},
    "galician": {"expected_tag": "GAL", "display": "Galicia"},
    "basque": {"expected_tag": "NAV", "display": "Navarre/Basque"},
    "andalucian": {"expected_tag": "GRA", "display": "Granada/Andalusia"},
    "portugese": {"expected_tag": "POR", "display": "Portugal"},
}

IBERIA_FORMABLE_FILES = {
    "SpanishNation.txt": ["spanish_nation", "spanish_nation_diplomatically"],
    "AndalusianNation.txt": ["andalusian_nation"],
}

IBERIA_RISK_FILES = [
    ("events/FlavorSPA.txt", ["flavor_spa.3716", "Iberian Wedding", "catalan", "portugese"]),
    ("missions/GC_Spanish_Missions.txt", ["primary_culture = catalan", "catalonia_area", "flavor_spa"]),
    ("missions/Spanish_Missions.txt", ["catalonia_area", "iberia_region"]),
    ("missions/GC_Aragonese_Missions.txt", ["primary_culture = catalan", "gc_ara_portugal"]),
    ("missions/Portuguese_Missions.txt", ["portugal_discovers", "colonial", "india"]),
    ("missions/GC_Granadan_Missions.txt", ["andalusia", "catalonia_area", "adu_conquer_portugal"]),
    ("decisions/SpanishNation.txt", ["spanish_nation", "spanish_nation_diplomatically", "NOT = { tag = POR }"]),
    ("decisions/AndalusianNation.txt", ["andalusian_nation", "add_permanent_claim"]),
]


def filter_rows(rows: list[dict[str, Any]], region: str | None) -> list[dict[str, Any]]:
    if not region:
        return rows
    return [row for row in rows if row.get("region") == region]


def culture_groups_for_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_culture: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.get("province_type") != "land":
            continue
        culture = row.get("culture") or "unknown"
        entry = by_culture.setdefault(
            culture,
            {
                "culture": culture,
                "culture_group": row.get("culture_group"),
                "province_ids": [],
                "province_names": [],
                "vanilla_owners": Counter(),
                "areas": Counter(),
            },
        )
        entry["province_ids"].append(row["province_id"])
        entry["province_names"].append(row["province_name"])
        entry["vanilla_owners"][row.get("vanilla_owner") or "none"] += 1
        entry["areas"][row.get("area") or "unknown"] += 1
    out: list[dict[str, Any]] = []
    for entry in by_culture.values():
        out.append(
            {
                "culture": entry["culture"],
                "culture_group": entry["culture_group"],
                "land_province_count": len(entry["province_ids"]),
                "province_ids": sorted(entry["province_ids"]),
                "province_names": entry["province_names"],
                "vanilla_owner_counts": dict(sorted(entry["vanilla_owners"].items())),
                "area_counts": dict(sorted(entry["areas"].items())),
            }
        )
    return sorted(out, key=lambda item: item["culture"])


def build_iberia_province_audit(rows: list[dict[str, Any]], context: dict[str, Any]) -> dict[str, Any]:
    iberia_rows = [row for row in rows if row.get("region") == "iberia_region"]
    land_rows = [row for row in iberia_rows if row.get("province_type") == "land"]
    missing = [row["province_id"] for row in iberia_rows if row.get("present_in_project_map") is False]
    return {
        "audit": "iberia_province_culture_audit",
        "scope": "vanilla iberia_region, annotated against Project Crown provinces.bmp",
        "sources": {
            "vanilla_root": context["vanilla_root"],
            "project_bmp": context["project_bmp"],
            "region_source": "vanilla map/region.txt -> iberia_region",
            "history_source": "vanilla history/provinces/*.txt at 1444.11.11",
        },
        "summary": {
            "province_count": len(iberia_rows),
            "land_province_count": len(land_rows),
            "project_map_missing_province_ids": missing,
            "all_region_provinces_present_in_project_map": not missing,
            "cultures_present": sorted({row["culture"] for row in land_rows if row.get("culture")}),
        },
        "culture_groups": culture_groups_for_rows(iberia_rows),
        "provinces": sorted(iberia_rows, key=lambda row: row["province_id"]),
    }


def build_tag_audit(context: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    country_tags = context["country_tags"]
    country_histories = context["country_histories"]
    culture_primary_tag = context["culture_primary_tag"]
    province_by_culture = defaultdict(list)
    for row in rows:
        if row.get("region") == "iberia_region" and row.get("province_type") == "land":
            province_by_culture[row.get("culture")].append(row["province_id"])
    entries: list[dict[str, Any]] = []
    for culture, target in IBERIA_CULTURE_TARGETS.items():
        expected_tag = target["expected_tag"]
        vanilla_primary = culture_primary_tag.get(culture)
        history = country_histories.get(expected_tag, {})
        country_file = country_tags.get(expected_tag)
        country_file_exists = (
            (Path(context["vanilla_root"]) / "common" / country_file).exists() if country_file else False
        )
        exists = expected_tag in country_tags and expected_tag in country_histories
        history_matches = history.get("primary_culture") == culture
        if not exists:
            reuse_status = "new_tag_or_repair_needed"
        elif history_matches:
            reuse_status = "usable_vanilla_tag_found"
        else:
            reuse_status = "usable_vanilla_tag_found_history_primary_culture_review"
        entries.append(
            {
                "culture": culture,
                "culture_display": target["display"],
                "expected_reuse_tag": expected_tag,
                "vanilla_culture_primary_tag": vanilla_primary,
                "tag_exists_in_common_country_tags": expected_tag in country_tags,
                "tag_country_file": country_file,
                "tag_country_file_exists": country_file_exists,
                "tag_history_file": history.get("history_file"),
                "tag_primary_culture": history.get("primary_culture"),
                "history_primary_culture_matches_target": history_matches,
                "tag_reuse_status": reuse_status,
                "iberia_region_land_province_ids": sorted(province_by_culture.get(culture, [])),
            }
        )
    return {
        "audit": "iberia_tag_audit",
        "summary": {
            "all_target_cultures_have_reuse_tags": all(
                entry["tag_reuse_status"] != "new_tag_or_repair_needed" for entry in entries
            ),
            "catalonia_tag_status": "CAT exists in vanilla as countries/Catalunya.txt with CAT - Catalunya.txt history",
            "new_tag_need_from_vanilla_audit": [],
            "tags_requiring_history_primary_culture_review": [
                entry["expected_reuse_tag"]
                for entry in entries
                if entry["tag_reuse_status"] == "usable_vanilla_tag_found_history_primary_culture_review"
            ],
            "note": "This is an audit finding only. It does not create, rename, or implement tags.",
        },
        "entries": entries,
        "related_existing_formable_or_regional_tags": [
            {
                "tag": tag,
                "tag_country_file": country_tags.get(tag),
                "tag_country_file_exists": (
                    (Path(context["vanilla_root"]) / "common" / country_tags[tag]).exists()
                    if tag in country_tags
                    else False
                ),
                "tag_history_file": country_histories.get(tag, {}).get("history_file"),
                "primary_culture": country_histories.get(tag, {}).get("primary_culture"),
            }
            for tag in ["SPA", "ADU", "VAL"]
            if tag in country_tags or tag in country_histories
        ],
    }


def decision_names_from_file(path: Path) -> list[str]:
    if not path.exists():
        return []
    parsed = parse_eu4(read_text(path))
    names: list[str] = []
    for key, value in pairs(parsed):
        if key == "country_decisions" and isinstance(value, list):
            names.extend(name for name, block in pairs(value) if isinstance(block, list))
    return names


def province_ids_mentioned(path: Path) -> list[int]:
    if not path.exists():
        return []
    text = read_text(path)
    ids: set[int] = set()
    for match in re.finditer(r"\b(?:province_id|owns_core_province|add_permanent_claim)\s*=\s*(\d+)\b", text):
        ids.add(int(match.group(1)))
    return sorted(ids)


def build_formable_audit(vanilla_root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for file_name, expected in IBERIA_FORMABLE_FILES.items():
        path = vanilla_root / "decisions" / file_name
        decision_names = decision_names_from_file(path)
        entries.append(
            {
                "file": f"decisions/{file_name}",
                "exists": path.exists(),
                "expected_decisions": expected,
                "decision_names_found": decision_names,
                "expected_decisions_found": [name for name in expected if name in decision_names],
                "province_ids_mentioned": province_ids_mentioned(path),
                "risk_note": "Must be disabled, replaced, or re-scoped during Iberia POC because vanilla formation assumes vanilla 1444 politics.",
            }
        )
    return {
        "audit": "iberia_formable_audit",
        "summary": {
            "vanilla_spain_decisions_found": True,
            "vanilla_andalusia_decision_found": True,
            "implementation_status": "audit_only_no_decisions_changed",
        },
        "entries": entries,
    }


def build_border_stub(rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_groups = culture_groups_for_rows([row for row in rows if row.get("region") == "iberia_region"])
    review: list[dict[str, Any]] = []
    for group in candidate_groups:
        culture = group["culture"]
        note = "clean culture cluster candidate"
        if culture == "catalan":
            note = "Catalan land is compact; Balearic adjacency needs island exception if assigned to Catalonia or Aragon."
        elif culture == "aragonese":
            note = "Aragonese and Valencian edge provinces need human review against Catalan/Andalusian contested-frontier plans."
        elif culture == "andalucian":
            note = "Andalucian area is split between vanilla Granada and Castile; clean owner plus claims should be reviewed."
        elif culture == "portugese":
            note = "Portuguese mainland cluster is clean; overseas Atlantic islands are outside iberia_region and excluded from this POC stub."
        elif culture == "basque":
            note = "Basque cluster is small and compact; Navarra/Navarre naming and cross-Pyrenees claims need later review."
        review.append(
            {
                "culture": culture,
                "candidate_owner_tag": IBERIA_CULTURE_TARGETS.get(culture, {}).get("expected_tag"),
                "province_ids": group["province_ids"],
                "review_note": note,
            }
        )
    return {
        "audit": "iberia_border_cleanliness_stub",
        "status": "prototype_stub",
        "note": "Run validate_border_cleanliness.py --mock-iberia-from-cultures for bitmap adjacency validation. This file records design-review targets only.",
        "candidate_groups": review,
        "global_exclusions_for_poc": [
            "No province ownership changes in Phase 1B.",
            "No Canaries/Ceuta/Melilla modern-border implementation in this technical foundation phase.",
            "No claims, cores, natural rivals, events, missions, or formables implemented.",
        ],
    }


def build_contested_candidates(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_area = defaultdict(list)
    for row in rows:
        if row.get("region") == "iberia_region" and row.get("province_type") == "land":
            by_area[row.get("area")].append(row)
    candidates = [
        {
            "contested_region_id": "iberia_granada_frontier_candidate",
            "display_name": "Granada frontier",
            "province_ids": sorted(
                row["province_id"]
                for area in ["lower_andalucia_area", "upper_andalucia_area"]
                for row in by_area.get(area, [])
            ),
            "clean_starting_owner": "TBD in Iberia POC; audit-only candidate",
            "opposing_claimants": ["GRA", "CAS", "SPA", "ADU"],
            "claim_type_recommendation": "mission_claim_or_permanent_claim",
            "reason": "Reconquista and Andalusian restoration tension should be claims/mission content, not messy starting borders.",
            "escalation_rule": "review during Phase 2; no escalation implemented in Phase 1B",
            "border_cleanliness_note": "Keep one clean owner per province and express dispute via claims/cores later.",
            "implementation_phase": "Phase 2 Iberia POC or later",
        },
        {
            "contested_region_id": "iberia_valencia_murcia_candidate",
            "display_name": "Valencia-Murcia frontier",
            "province_ids": sorted(
                row["province_id"]
                for area in ["valencia_area", "toledo_area"]
                for row in by_area.get(area, [])
                if row.get("culture") in {"aragonese", "andalucian", "castillian"}
            ),
            "clean_starting_owner": "TBD in Iberia POC; audit-only candidate",
            "opposing_claimants": ["ARA", "CAS", "GRA", "SPA", "ADU"],
            "claim_type_recommendation": "permanent_claim",
            "reason": "Potential Crown of Aragon / Castile / Granada border tension.",
            "escalation_rule": "review after ownership proposal exists",
            "border_cleanliness_note": "Do not split awkward pockets for dispute representation.",
            "implementation_phase": "Phase 2 Iberia POC or later",
        },
        {
            "contested_region_id": "iberia_portugal_border_candidate",
            "display_name": "Portuguese-Castilian border",
            "province_ids": sorted(
                row["province_id"]
                for area in ["alentejo_area", "beieras_area", "extremadura_area", "leon_area"]
                for row in by_area.get(area, [])
            ),
            "clean_starting_owner": "TBD in Iberia POC; audit-only candidate",
            "opposing_claimants": ["POR", "CAS", "LON"],
            "claim_type_recommendation": "event_claim_or_mission_claim",
            "reason": "Portugal is excluded from Spain by owner rule; any pressure should be restrained and reviewed.",
            "escalation_rule": "no Spain-on-Portugal sanctioned annexation in initial POC",
            "border_cleanliness_note": "Portugal should remain a clean separate culture-state/formable-adjacent power.",
            "implementation_phase": "Phase 2 Iberia POC or later",
        },
    ]
    return {
        "audit": "iberia_contested_region_candidates",
        "status": "candidate_registry_only",
        "entries": candidates,
    }


def build_diplomacy_candidates() -> dict[str, Any]:
    entries = [
        {
            "source": "CAS",
            "target": "GRA",
            "relationship_type": "rival",
            "reason": "Reconquista frontier and Granada/Andalusia formable clash.",
            "supporting_basis": ["contested province", "religion", "history", "formable clash"],
            "strength_priority": "high",
            "rollout_wave": "Iberia POC review",
            "notes": "Audit candidate only; do not seed until Phase 2 controlled diplomacy slice.",
        },
        {
            "source": "CAS",
            "target": "ARA",
            "relationship_type": "opinion_modifier",
            "reason": "Spain formation race can be rivalry or rare-dynastic/friendly path later.",
            "supporting_basis": ["formable clash", "history", "balance"],
            "strength_priority": "medium",
            "rollout_wave": "Iberia POC review",
            "notes": "Do not implement rare dynastic event in Phase 1B or Phase 2 initial foundation.",
        },
        {
            "source": "POR",
            "target": "CAS",
            "relationship_type": "friend",
            "reason": "Vanilla friendship exists, but Portugal exclusion from Spain means it needs independence-safe tuning.",
            "supporting_basis": ["history", "geography", "balance"],
            "strength_priority": "medium",
            "rollout_wave": "Iberia POC review",
            "notes": "Avoid making Portugal an automatic Castilian annexation target.",
        },
        {
            "source": "NAV",
            "target": "CAS",
            "relationship_type": "threat_hint",
            "reason": "Small Basque/Navarre culture-state bordered by larger Iberian unifiers.",
            "supporting_basis": ["geography", "balance"],
            "strength_priority": "low",
            "rollout_wave": "Iberia POC review",
            "notes": "Potential alliance/friendship with Aragon or France-side states is later wave-sensitive.",
        },
    ]
    return {
        "audit": "iberia_diplomacy_seed_candidates",
        "status": "candidate_seed_table_only",
        "entries": entries,
    }


def keyword_lines(path: Path, keywords: list[str]) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    lines = read_text(path).splitlines()
    hits: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        for keyword in keywords:
            if keyword in line:
                hits.append({"line": index, "keyword": keyword, "text": line.strip()[:180]})
                break
        if len(hits) >= 20:
            break
    return hits


def build_risk_audit(vanilla_root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for relative, keywords in IBERIA_RISK_FILES:
        path = vanilla_root / relative
        hits = keyword_lines(path, keywords)
        entries.append(
            {
                "file": relative,
                "exists": path.exists(),
                "keywords_checked": keywords,
                "sample_hits": hits,
                "risk": "review_required_before_Iberia_POC" if hits else "present_but_no_keyword_hit_or_missing",
            }
        )
    return {
        "audit": "iberia_vanilla_content_risk_audit",
        "summary": {
            "implementation_status": "audit_only_no_vanilla_content_changed",
            "headline_risks": [
                "Iberian Wedding in events/FlavorSPA.txt assumes vanilla Castile-Aragon setup.",
                "Spanish and Aragonese missions branch on Catalan primary culture and vanilla Spain/Aragon assumptions.",
                "SpanishNation.txt and AndalusianNation.txt provide useful formable references but need Project Crown re-scope.",
                "Portugal colonial mission content should be preserved later without allowing Spain to absorb Portugal by default.",
            ],
        },
        "entries": entries,
    }


def write_iberia_audit_package(audit_dir: Path, rows: list[dict[str, Any]], context: dict[str, Any], vanilla_root: Path) -> None:
    write_json(audit_dir / "iberia_province_culture_audit.json", build_iberia_province_audit(rows, context))
    write_json(audit_dir / "iberia_tag_audit.json", build_tag_audit(context, rows))
    write_json(audit_dir / "iberia_formable_audit.json", build_formable_audit(vanilla_root))
    write_json(audit_dir / "iberia_border_cleanliness_stub.json", build_border_stub(rows))
    write_json(audit_dir / "iberia_contested_region_candidates.json", build_contested_candidates(rows))
    write_json(audit_dir / "iberia_diplomacy_seed_candidates.json", build_diplomacy_candidates())
    write_json(audit_dir / "iberia_vanilla_content_risk_audit.json", build_risk_audit(vanilla_root))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vanilla-root", type=Path, default=DEFAULT_VANILLA_ROOT)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--project-provinces-bmp", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=SCRIPT_DIR / "audits" / "province_culture_table.json")
    parser.add_argument("--summary-output", type=Path, default=SCRIPT_DIR / "audits" / "province_culture_summary.json")
    parser.add_argument("--region", default=None, help="Optional vanilla region filter, e.g. iberia_region.")
    parser.add_argument("--write-iberia-audits", action="store_true")
    args = parser.parse_args()

    context = load_data_context(args.vanilla_root, args.project_root, args.project_provinces_bmp, scan_project_map=True)
    rows = filter_rows(build_province_table(context), args.region)
    write_json(args.output, rows)
    write_json(args.summary_output, summarize_cultures(rows))
    if args.write_iberia_audits:
        write_iberia_audit_package(SCRIPT_DIR / "audits", build_province_table(context), context, args.vanilla_root)
    print(f"Wrote {len(rows)} province rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
