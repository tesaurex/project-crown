#!/usr/bin/env python3
"""Prototype border-cleanliness validator for Project Crown culture-state data."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from eu4_data import (  # noqa: E402
    DEFAULT_PROJECT_ROOT,
    DEFAULT_VANILLA_ROOT,
    build_province_table,
    load_data_context,
    scan_bmp_adjacency,
    write_json,
)


IBERIA_CULTURE_TO_TAG = {
    "castillian": "CAS",
    "aragonese": "ARA",
    "catalan": "CAT",
    "leonese": "LON",
    "galician": "GAL",
    "basque": "NAV",
    "andalucian": "GRA",
    "portugese": "POR",
}


def load_ownership(path: Path) -> dict[str, set[int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    ownership: dict[str, set[int]] = defaultdict(set)
    if isinstance(data, dict) and "ownership" in data:
        data = data["ownership"]
    if isinstance(data, dict):
        for tag, province_ids in data.items():
            ownership[str(tag)].update(int(pid) for pid in province_ids)
    elif isinstance(data, list):
        for entry in data:
            tag = entry.get("tag") or entry.get("owner") or entry.get("culture_state_id")
            province_ids = entry.get("province_ids") or entry.get("starting_province_ids") or []
            if tag:
                ownership[str(tag)].update(int(pid) for pid in province_ids)
    return dict(ownership)


def mock_iberia_ownership(rows: list[dict[str, Any]]) -> dict[str, set[int]]:
    ownership: dict[str, set[int]] = defaultdict(set)
    for row in rows:
        if row.get("region") != "iberia_region" or row.get("province_type") != "land":
            continue
        tag = IBERIA_CULTURE_TO_TAG.get(row.get("culture"))
        if tag:
            ownership[tag].add(row["province_id"])
    return dict(ownership)


def connected_components(province_ids: set[int], adjacency: dict[int, set[int]]) -> list[list[int]]:
    remaining = set(province_ids)
    components: list[list[int]] = []
    while remaining:
        start = remaining.pop()
        queue: deque[int] = deque([start])
        component = [start]
        while queue:
            province_id = queue.popleft()
            for neighbor in adjacency.get(province_id, set()):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)
                    component.append(neighbor)
        components.append(sorted(component))
    return sorted(components, key=lambda component: (-len(component), component[0]))


def exception_hint(component: list[int], province_rows: dict[int, dict[str, Any]]) -> str | None:
    areas = {province_rows.get(pid, {}).get("area") for pid in component}
    if "baleares_area" in areas:
        return "island_exception_candidate_baleares"
    if len(component) == 1:
        province = province_rows.get(component[0], {})
        name = province.get("province_name", component[0])
        return f"single_province_component_review:{name}"
    return None


def validate_ownership(
    ownership: dict[str, set[int]],
    adjacency: dict[int, set[int]],
    province_rows: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    disconnected_tags = 0
    snake_warning_tags = 0
    for tag, raw_ids in sorted(ownership.items()):
        land_ids = {pid for pid in raw_ids if province_rows.get(pid, {}).get("province_type") == "land"}
        components = connected_components(land_ids, adjacency)
        same_owner_degree = {
            pid: len(adjacency.get(pid, set()) & land_ids)
            for pid in land_ids
        }
        leaf_like = sorted(pid for pid, degree in same_owner_degree.items() if degree <= 1)
        snake_score = round(len(leaf_like) / len(land_ids), 3) if land_ids else 0.0
        snake_warning = len(land_ids) >= 4 and snake_score >= 0.55
        warnings: list[str] = []
        if len(components) > 1:
            warnings.append("disconnected_ownership")
            disconnected_tags += 1
        if any(len(component) == 1 for component in components):
            warnings.append("isolated_component")
        if snake_warning:
            warnings.append("possible_province_snake")
            snake_warning_tags += 1
        results.append(
            {
                "tag": tag,
                "land_province_count": len(land_ids),
                "components": components,
                "component_count": len(components),
                "largest_component_size": len(components[0]) if components else 0,
                "isolated_province_ids": [component[0] for component in components if len(component) == 1],
                "low_internal_adjacency_province_ids": leaf_like,
                "snake_score": snake_score,
                "warnings": warnings,
                "exception_hints": [
                    hint
                    for hint in (exception_hint(component, province_rows) for component in components)
                    if hint
                ],
            }
        )
    return {
        "summary": {
            "countries_checked": len(results),
            "countries_with_disconnected_ownership": disconnected_tags,
            "countries_with_snake_warning": snake_warning_tags,
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vanilla-root", type=Path, default=DEFAULT_VANILLA_ROOT)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--project-provinces-bmp", type=Path, default=None)
    parser.add_argument("--ownership-json", type=Path, default=None)
    parser.add_argument("--mock-iberia-from-cultures", action="store_true")
    parser.add_argument("--output", type=Path, default=SCRIPT_DIR / "audits" / "iberia_border_cleanliness_validation.json")
    args = parser.parse_args()

    if not args.ownership_json and not args.mock_iberia_from_cultures:
        parser.error("Provide --ownership-json or --mock-iberia-from-cultures.")

    context = load_data_context(args.vanilla_root, args.project_root, args.project_provinces_bmp, scan_project_map=True)
    rows = build_province_table(context)
    province_rows = {row["province_id"]: row for row in rows}
    if args.ownership_json:
        ownership = load_ownership(args.ownership_json)
        ownership_source = str(args.ownership_json)
    else:
        ownership = mock_iberia_ownership(rows)
        ownership_source = "mock Iberia ownership generated from vanilla province culture primary tags"

    adjacency = scan_bmp_adjacency(Path(context["project_bmp"]), context["color_to_id"])
    land_adjacency = {
        pid: {
            neighbor
            for neighbor in neighbors
            if province_rows.get(pid, {}).get("province_type") == "land"
            and province_rows.get(neighbor, {}).get("province_type") == "land"
        }
        for pid, neighbors in adjacency.items()
    }
    validation = validate_ownership(ownership, land_adjacency, province_rows)
    report = {
        "audit": "border_cleanliness_validation",
        "status": "prototype",
        "ownership_source": ownership_source,
        "adjacency_source": context["project_bmp"],
        "rules_checked": [
            "same-owner land connectivity by Project Crown bitmap pixel adjacency",
            "isolated one-province components",
            "rough province-snake warning via low internal adjacency ratio",
        ],
        "limits": [
            "Sea crossings are not treated as land adjacency.",
            "Historical enclave, island, trade-port, and chokepoint exceptions are flagged as hints, not approved.",
            "This validator does not implement gameplay or edit ownership.",
        ],
        **validation,
    }
    write_json(args.output, report)
    print(f"Wrote border cleanliness report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
