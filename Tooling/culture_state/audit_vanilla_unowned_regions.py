#!/usr/bin/env python3
"""Audit vanilla unowned land against Project Crown province overrides."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from eu4_data import (  # noqa: E402
    DEFAULT_PROJECT_ROOT,
    DEFAULT_VANILLA_ROOT,
    build_province_table,
    history_state,
    load_data_context,
    parse_eu4,
    read_text,
    write_json,
)


AUDIT_DATE = "2026-07-08"
PROJECT_HISTORY_RELATIVE = Path("Mod Build/project_crown/history/provinces")
NORTH_AFRICA_REGIONS = {"egypt_region", "maghreb_region"}
PHILIPPINES_AREAS = {
    "luzon_area",
    "southern_luzon_area",
    "mindanao_area",
    "west_mindanao_area",
    "visayas_area",
    "palawan_area",
}
EXCLUDED_COLONIAL_OPEN_REGIONS = {
    "Americas",
    "Sub-Saharan Africa",
    "Australia/Oceania",
    "Philippines",
}
START_STATE_SCALAR_KEYS = {
    "owner",
    "controller",
    "culture",
    "religion",
    "is_city",
    "tribal_owner",
    "native_size",
    "native_ferocity",
    "native_hostileness",
}


def load_province_start_states(history_dir: Path) -> dict[int, dict[str, Any]]:
    states: dict[int, dict[str, Any]] = {}
    if not history_dir.exists():
        return states
    for path in sorted(history_dir.glob("*.txt")):
        match = re.match(r"(\d+)", path.name)
        if not match:
            continue
        province_id = int(match.group(1))
        parsed = parse_eu4(read_text(path))
        state = history_state(parsed, START_STATE_SCALAR_KEYS, track_cores=True)
        state["history_file"] = path.name
        states[province_id] = state
    return states


def is_philippines(row: dict[str, Any]) -> bool:
    return row.get("area") in PHILIPPINES_AREAS


def design_region(row: dict[str, Any]) -> str:
    continent = row.get("continent")
    region = row.get("region")
    if is_philippines(row):
        return "Philippines"
    if continent in {"north_america", "south_america"}:
        return "Americas"
    if continent == "africa":
        if region in NORTH_AFRICA_REGIONS:
            return "North Africa"
        return "Sub-Saharan Africa"
    if continent == "oceania":
        return "Australia/Oceania"
    if continent == "asia":
        return "Asia excluding Philippines"
    if continent == "europe":
        return "Europe"
    return "Other"


def vanilla_ownership_class(owner: str | None, controller: str | None) -> str:
    if owner:
        return "vanilla_owned"
    if controller:
        return "vanilla_unowned_with_controller"
    return "vanilla_unowned_uncolonized"


def none_if_missing(value: Any) -> Any:
    return None if value == "" else value


def build_record(
    row: dict[str, Any],
    vanilla_state: dict[str, Any],
    project_state: dict[str, Any] | None,
) -> dict[str, Any]:
    vanilla_owner = none_if_missing(vanilla_state.get("owner"))
    vanilla_controller = none_if_missing(vanilla_state.get("controller"))
    project_owner = none_if_missing(project_state.get("owner")) if project_state else None
    project_controller = none_if_missing(project_state.get("controller")) if project_state else None
    project_culture = none_if_missing(project_state.get("culture")) if project_state else None
    project_religion = none_if_missing(project_state.get("religion")) if project_state else None
    ownership_class = vanilla_ownership_class(vanilla_owner, vanilla_controller)
    region_label = design_region(row)
    project_effective_owner = project_owner if project_state else vanilla_owner
    project_effective_controller = project_controller if project_state else vanilla_controller
    project_effective_culture = project_culture if project_state else none_if_missing(vanilla_state.get("culture"))
    project_effective_religion = project_religion if project_state else none_if_missing(vanilla_state.get("religion"))

    return {
        "province_id": row["province_id"],
        "province_name": row["province_name"],
        "province_type": row["province_type"],
        "continent": row.get("continent"),
        "superregion": row.get("superregion"),
        "region": row.get("region"),
        "area": row.get("area"),
        "design_region": region_label,
        "is_excluded_colonial_open_region": region_label in EXCLUDED_COLONIAL_OPEN_REGIONS,
        "vanilla_history_file": vanilla_state.get("history_file"),
        "vanilla_owner_1444": vanilla_owner,
        "vanilla_controller_1444": vanilla_controller,
        "vanilla_culture_1444": none_if_missing(vanilla_state.get("culture")),
        "vanilla_religion_1444": none_if_missing(vanilla_state.get("religion")),
        "vanilla_is_city_1444": none_if_missing(vanilla_state.get("is_city")),
        "vanilla_tribal_owner_1444": none_if_missing(vanilla_state.get("tribal_owner")),
        "vanilla_native_size": none_if_missing(vanilla_state.get("native_size")),
        "vanilla_native_ferocity": none_if_missing(vanilla_state.get("native_ferocity")),
        "vanilla_native_hostileness": none_if_missing(vanilla_state.get("native_hostileness")),
        "vanilla_ownership_class": ownership_class,
        "vanilla_starts_unowned_uncolonized": ownership_class == "vanilla_unowned_uncolonized",
        "project_override_exists": project_state is not None,
        "project_override_file": project_state.get("history_file") if project_state else None,
        "project_owner_1444": project_owner,
        "project_controller_1444": project_controller,
        "project_culture_1444": project_culture,
        "project_religion_1444": project_religion,
        "project_effective_owner_1444": project_effective_owner,
        "project_effective_controller_1444": project_effective_controller,
        "project_effective_culture_1444": project_effective_culture,
        "project_effective_religion_1444": project_effective_religion,
        "project_changes_owner_or_controller": project_state is not None
        and (project_owner != vanilla_owner or project_controller != vanilla_controller),
        "project_changes_culture_or_religion": project_state is not None
        and (
            project_culture != none_if_missing(vanilla_state.get("culture"))
            or project_religion != none_if_missing(vanilla_state.get("religion"))
        ),
        "project_override_status": "Project Crown override exists" if project_state else "No Project Crown override exists",
    }


def top_counts(counter: Counter[str], limit: int = 12) -> list[dict[str, Any]]:
    return [{"value": value, "count": count} for value, count in counter.most_common(limit)]


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    ownership_classes = Counter(record["vanilla_ownership_class"] for record in records)
    owner_counts = Counter(
        record["vanilla_owner_1444"] for record in records if record.get("vanilla_owner_1444")
    )
    tribal_counts = Counter(
        record["vanilla_tribal_owner_1444"] for record in records if record.get("vanilla_tribal_owner_1444")
    )
    project_override_count = sum(1 for record in records if record["project_override_exists"])
    project_owner_change_count = sum(1 for record in records if record["project_changes_owner_or_controller"])
    project_culture_religion_change_count = sum(1 for record in records if record["project_changes_culture_or_religion"])
    vanilla_unowned = ownership_classes["vanilla_unowned_uncolonized"]
    return {
        "province_count": len(records),
        "vanilla_owned_count": ownership_classes["vanilla_owned"],
        "vanilla_unowned_uncolonized_count": vanilla_unowned,
        "vanilla_unowned_with_controller_count": ownership_classes["vanilla_unowned_with_controller"],
        "vanilla_unowned_with_tribal_owner_count": sum(
            1
            for record in records
            if record["vanilla_starts_unowned_uncolonized"] and record.get("vanilla_tribal_owner_1444")
        ),
        "vanilla_unowned_without_tribal_owner_count": sum(
            1
            for record in records
            if record["vanilla_starts_unowned_uncolonized"] and not record.get("vanilla_tribal_owner_1444")
        ),
        "project_override_count": project_override_count,
        "project_owner_or_controller_change_count": project_owner_change_count,
        "project_culture_or_religion_change_count": project_culture_religion_change_count,
        "top_vanilla_owners": top_counts(owner_counts),
        "top_vanilla_tribal_owners": top_counts(tribal_counts),
    }


def summarize_by(records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        group_key = record.get(key) or "unknown"
        grouped.setdefault(group_key, []).append(record)
    return {group_key: summarize(grouped[group_key]) for group_key in sorted(grouped)}


def base_metadata(vanilla_root: Path, project_root: Path) -> dict[str, Any]:
    return {
        "audit": "vanilla_unowned_region_audit",
        "phase": "Phase 2C.3",
        "audit_date": AUDIT_DATE,
        "sources": {
            "vanilla_root": str(vanilla_root),
            "vanilla_history": "history/provinces/*.txt at 1444.11.11",
            "vanilla_geography": [
                "map/continent.txt",
                "map/region.txt",
                "map/area.txt",
                "map/default.map",
                "map/climate.txt",
            ],
            "project_root": str(project_root),
            "project_history": str(PROJECT_HISTORY_RELATIVE),
        },
        "definitions": {
            "vanilla_owned": "A land province with a 1444 owner in vanilla province history.",
            "vanilla_unowned_uncolonized": "A land province with no 1444 owner or controller in vanilla province history.",
            "project_override_exists": "A same-ID province history file exists under Project Crown.",
            "project_effective_owner_1444": "Project Crown override owner when present, otherwise vanilla owner.",
            "north_africa": sorted(NORTH_AFRICA_REGIONS),
            "philippines_areas": sorted(PHILIPPINES_AREAS),
            "excluded_colonial_open_regions": sorted(EXCLUDED_COLONIAL_OPEN_REGIONS),
        },
    }


def audit_document(
    title: str,
    records: list[dict[str, Any]],
    vanilla_root: Path,
    project_root: Path,
    extra_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    summary = summarize(records)
    if extra_summary:
        summary.update(extra_summary)
    return {
        **base_metadata(vanilla_root, project_root),
        "title": title,
        "summary": summary,
        "summary_by_design_region": summarize_by(records, "design_region"),
        "summary_by_continent": summarize_by(records, "continent"),
        "summary_by_region": summarize_by(records, "region"),
        "provinces": sorted(records, key=lambda record: record["province_id"]),
    }


def write_audits(records: list[dict[str, Any]], vanilla_root: Path, project_root: Path, output_dir: Path) -> None:
    global_extra = {
        "project_non_iberian_history_override_count": sum(
            1 for record in records if record["project_override_exists"] and record.get("region") != "iberia_region"
        ),
        "project_non_iberian_owner_or_controller_change_count": sum(
            1
            for record in records
            if record["project_changes_owner_or_controller"] and record.get("region") != "iberia_region"
        ),
        "project_non_iberian_ownership_matches_vanilla": not any(
            record["project_changes_owner_or_controller"] and record.get("region") != "iberia_region"
            for record in records
        ),
    }
    write_json(
        output_dir / "global_vanilla_unowned_audit.json",
        audit_document("Global vanilla land ownership audit", records, vanilla_root, project_root, global_extra),
    )

    excluded_records = [
        record for record in records if record["design_region"] in EXCLUDED_COLONIAL_OPEN_REGIONS
    ]
    write_json(
        output_dir / "excluded_region_unowned_audit.json",
        audit_document(
            "Excluded colonial-open region vanilla ownership audit",
            excluded_records,
            vanilla_root,
            project_root,
        ),
    )

    africa_records = [record for record in records if record.get("continent") == "africa"]
    write_json(
        output_dir / "africa_unowned_audit.json",
        audit_document("Africa vanilla ownership audit", africa_records, vanilla_root, project_root),
    )

    asia_records = [record for record in records if record["design_region"] == "Asia excluding Philippines"]
    write_json(
        output_dir / "asia_unowned_audit.json",
        audit_document("Asia excluding Philippines vanilla ownership audit", asia_records, vanilla_root, project_root),
    )

    australia_oceania_records = [record for record in records if record["design_region"] == "Australia/Oceania"]
    write_json(
        output_dir / "australia_oceania_unowned_audit.json",
        audit_document(
            "Australia/Oceania vanilla ownership audit",
            australia_oceania_records,
            vanilla_root,
            project_root,
        ),
    )

    philippines_records = [record for record in records if record["design_region"] == "Philippines"]
    write_json(
        output_dir / "philippines_unowned_audit.json",
        audit_document("Philippines vanilla ownership audit", philippines_records, vanilla_root, project_root),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vanilla-root", type=Path, default=DEFAULT_VANILLA_ROOT)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT_ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PROJECT_ROOT / "Tooling" / "culture_state" / "audits",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    context = load_data_context(args.vanilla_root, args.project_root, scan_project_map=False)
    vanilla_states = load_province_start_states(args.vanilla_root / "history" / "provinces")
    project_states = load_province_start_states(args.project_root / PROJECT_HISTORY_RELATIVE)
    records: list[dict[str, Any]] = []
    for row in build_province_table(context):
        if row.get("province_type") != "land":
            continue
        province_id = row["province_id"]
        records.append(build_record(row, vanilla_states.get(province_id, {}), project_states.get(province_id)))
    write_audits(records, args.vanilla_root, args.project_root, args.output_dir)
    print(f"Wrote vanilla unowned-region audits to {args.output_dir}")


if __name__ == "__main__":
    main()
