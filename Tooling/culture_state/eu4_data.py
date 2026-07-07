#!/usr/bin/env python3
"""Shared EU4 data readers for Project Crown culture-state audits."""

from __future__ import annotations

import csv
import json
import re
import struct
from collections import defaultdict
from pathlib import Path
from typing import Any, Union


DEFAULT_VANILLA_ROOT = Path(
    "/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV"
)
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[2]
START_DATE = (1444, 11, 11)


Item = Union[str, tuple[str, Any]]
Block = list[Item]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def strip_comments(text: str) -> str:
    out: list[str] = []
    in_quote = False
    escaped = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '"' and not escaped:
            in_quote = not in_quote
        if ch == "#" and not in_quote:
            while i < len(text) and text[i] not in "\n\r":
                i += 1
            if i < len(text):
                out.append(text[i])
                i += 1
            continue
        out.append(ch)
        escaped = ch == "\\" and not escaped
        if ch != "\\":
            escaped = False
        i += 1
    return "".join(out)


def tokenize_eu4(text: str) -> list[str]:
    text = strip_comments(text)
    tokens: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "{}=":
            tokens.append(ch)
            i += 1
            continue
        if ch == '"':
            i += 1
            buf: list[str] = []
            while i < len(text):
                if text[i] == '"':
                    i += 1
                    break
                buf.append(text[i])
                i += 1
            tokens.append("".join(buf))
            continue
        start = i
        while i < len(text) and not text[i].isspace() and text[i] not in "{}=\"":
            i += 1
        tokens.append(text[start:i])
    return tokens


def parse_eu4(text: str) -> Block:
    tokens = tokenize_eu4(text)
    index = 0

    def parse_block() -> Block:
        nonlocal index
        block: Block = []
        while index < len(tokens):
            tok = tokens[index]
            if tok == "}":
                index += 1
                break
            if index + 1 < len(tokens) and tokens[index + 1] == "=":
                key = tok
                index += 2
                if index < len(tokens) and tokens[index] == "{":
                    index += 1
                    value = parse_block()
                elif index < len(tokens):
                    value = tokens[index]
                    index += 1
                else:
                    value = ""
                block.append((key, value))
            elif tok == "{":
                index += 1
                block.append(parse_block())
            else:
                block.append(tok)
                index += 1
        return block

    return parse_block()


def pairs(block: Block) -> list[tuple[str, Any]]:
    return [item for item in block if isinstance(item, tuple)]


def block_values(block: Any) -> list[str]:
    if not isinstance(block, list):
        return []
    return [item for item in block if isinstance(item, str)]


def first_scalar(block: Block, key: str) -> str | None:
    for k, value in pairs(block):
        if k == key and isinstance(value, str):
            return value
    return None


def scalar_values(block: Block, key: str) -> list[str]:
    return [value for k, value in pairs(block) if k == key and isinstance(value, str)]


def parse_date(value: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"(\d{1,4})\.(\d{1,2})\.(\d{1,2})", value)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def history_state(
    items: Block,
    scalar_keys: set[str],
    multi_keys: set[str] | None = None,
    track_cores: bool = False,
    start_date: tuple[int, int, int] = START_DATE,
) -> dict[str, Any]:
    multi_keys = multi_keys or set()
    scalars: dict[str, str] = {}
    multis: dict[str, list[str]] = {key: [] for key in multi_keys}
    cores: set[str] = set()

    def apply_block(block: Block) -> None:
        for item in block:
            if not isinstance(item, tuple):
                continue
            key, value = item
            if isinstance(value, list):
                continue
            if key in scalar_keys:
                scalars[key] = value
            elif key in multi_keys:
                multis.setdefault(key, []).append(value)
            elif track_cores and key == "add_core":
                cores.add(value)
            elif track_cores and key == "remove_core":
                cores.discard(value)

    apply_block(items)
    dated_blocks: list[tuple[tuple[int, int, int], Block]] = []
    for key, value in pairs(items):
        date = parse_date(key)
        if date and date <= start_date and isinstance(value, list):
            dated_blocks.append((date, value))
    for _, block in sorted(dated_blocks, key=lambda item: item[0]):
        apply_block(block)

    out: dict[str, Any] = dict(scalars)
    for key, values in multis.items():
        out[key] = values
    if track_cores:
        out["cores"] = sorted(cores)
    return out


def load_definition(vanilla_root: Path) -> tuple[dict[int, dict[str, Any]], dict[tuple[int, int, int], int]]:
    definitions: dict[int, dict[str, Any]] = {}
    color_to_id: dict[tuple[int, int, int], int] = {}
    with (vanilla_root / "map" / "definition.csv").open("r", encoding="cp1252", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)
        for row in reader:
            if len(row) < 5 or not row[0].isdigit():
                continue
            province_id = int(row[0])
            color = (int(row[1]), int(row[2]), int(row[3]))
            definitions[province_id] = {
                "province_id": province_id,
                "name": row[4],
                "color": color,
            }
            color_to_id[color] = province_id
    return definitions, color_to_id


def scan_bmp_province_ids(bmp_path: Path, color_to_id: dict[tuple[int, int, int], int]) -> set[int]:
    province_ids: set[int] = set()
    with bmp_path.open("rb") as f:
        header = f.read(54)
        if header[:2] != b"BM":
            raise ValueError(f"Not a BMP file: {bmp_path}")
        pixel_offset = struct.unpack_from("<I", header, 10)[0]
        width = struct.unpack_from("<i", header, 18)[0]
        height = struct.unpack_from("<i", header, 22)[0]
        bpp = struct.unpack_from("<H", header, 28)[0]
        compression = struct.unpack_from("<I", header, 30)[0]
        if bpp != 24 or compression != 0:
            raise ValueError(f"Expected uncompressed 24-bit BMP: {bmp_path}")
        width = abs(width)
        height = abs(height)
        row_stride = ((width * 3 + 3) // 4) * 4
        f.seek(pixel_offset)
        for _ in range(height):
            row = f.read(row_stride)
            for offset in range(0, width * 3, 3):
                b, g, r = row[offset : offset + 3]
                province_id = color_to_id.get((r, g, b))
                if province_id is not None:
                    province_ids.add(province_id)
    return province_ids


def scan_bmp_adjacency(bmp_path: Path, color_to_id: dict[tuple[int, int, int], int]) -> dict[int, set[int]]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    with bmp_path.open("rb") as f:
        header = f.read(54)
        if header[:2] != b"BM":
            raise ValueError(f"Not a BMP file: {bmp_path}")
        pixel_offset = struct.unpack_from("<I", header, 10)[0]
        width = abs(struct.unpack_from("<i", header, 18)[0])
        height = abs(struct.unpack_from("<i", header, 22)[0])
        bpp = struct.unpack_from("<H", header, 28)[0]
        compression = struct.unpack_from("<I", header, 30)[0]
        if bpp != 24 or compression != 0:
            raise ValueError(f"Expected uncompressed 24-bit BMP: {bmp_path}")
        row_stride = ((width * 3 + 3) // 4) * 4
        previous_row: list[int | None] | None = None
        f.seek(pixel_offset)
        for _ in range(height):
            raw = f.read(row_stride)
            row: list[int | None] = []
            last: int | None = None
            for offset in range(0, width * 3, 3):
                b, g, r = raw[offset : offset + 3]
                province_id = color_to_id.get((r, g, b))
                row.append(province_id)
                if province_id is not None and last is not None and province_id != last:
                    adjacency[province_id].add(last)
                    adjacency[last].add(province_id)
                last = province_id
            if previous_row is not None:
                for province_id, above in zip(row, previous_row):
                    if province_id is not None and above is not None and province_id != above:
                        adjacency[province_id].add(above)
                        adjacency[above].add(province_id)
            previous_row = row
    return adjacency


def load_id_block_file(path: Path) -> dict[str, list[int]]:
    parsed = parse_eu4(read_text(path))
    out: dict[str, list[int]] = {}
    for key, value in pairs(parsed):
        if isinstance(value, list):
            out[key] = [int(item) for item in block_values(value) if item.isdigit()]
    return out


def load_area_data(vanilla_root: Path) -> tuple[dict[str, list[int]], dict[int, str]]:
    areas = load_id_block_file(vanilla_root / "map" / "area.txt")
    by_province: dict[int, str] = {}
    for area, province_ids in areas.items():
        for province_id in province_ids:
            by_province[province_id] = area
    return areas, by_province


def load_region_data(vanilla_root: Path, area_to_provinces: dict[str, list[int]]) -> tuple[dict[str, list[str]], dict[int, str]]:
    parsed = parse_eu4(read_text(vanilla_root / "map" / "region.txt"))
    regions: dict[str, list[str]] = {}
    by_province: dict[int, str] = {}
    for region, value in pairs(parsed):
        if not isinstance(value, list):
            continue
        area_names: list[str] = []
        for key, area_block in pairs(value):
            if key == "areas" and isinstance(area_block, list):
                area_names.extend(block_values(area_block))
        regions[region] = area_names
        for area in area_names:
            for province_id in area_to_provinces.get(area, []):
                by_province[province_id] = region
    return regions, by_province


def load_superregion_data(vanilla_root: Path, province_to_region: dict[int, str]) -> tuple[dict[str, list[str]], dict[int, str]]:
    parsed = parse_eu4(read_text(vanilla_root / "map" / "superregion.txt"))
    superregions: dict[str, list[str]] = {}
    region_to_superregion: dict[str, str] = {}
    for superregion, value in pairs(parsed):
        if isinstance(value, list):
            names = block_values(value)
            if not names:
                for key, inner in pairs(value):
                    if key == "regions" and isinstance(inner, list):
                        names.extend(block_values(inner))
            superregions[superregion] = names
            for region in names:
                region_to_superregion[region] = superregion
    by_province = {
        province_id: region_to_superregion[region]
        for province_id, region in province_to_region.items()
        if region in region_to_superregion
    }
    return superregions, by_province


def load_continent_data(vanilla_root: Path) -> tuple[dict[str, list[int]], dict[int, str]]:
    continents = load_id_block_file(vanilla_root / "map" / "continent.txt")
    by_province: dict[int, str] = {}
    for continent, province_ids in continents.items():
        for province_id in province_ids:
            by_province[province_id] = continent
    return continents, by_province


def load_default_map_sets(vanilla_root: Path) -> dict[str, set[int]]:
    parsed = parse_eu4(read_text(vanilla_root / "map" / "default.map"))
    wanted = {"sea_starts", "lakes", "only_used_for_random"}
    out: dict[str, set[int]] = {key: set() for key in wanted}
    for key, value in pairs(parsed):
        if key in wanted and isinstance(value, list):
            out[key] = {int(item) for item in block_values(value) if item.isdigit()}
    return out


def load_climate_sets(vanilla_root: Path) -> dict[str, set[int]]:
    parsed = parse_eu4(read_text(vanilla_root / "map" / "climate.txt"))
    out: dict[str, set[int]] = {}
    for key, value in pairs(parsed):
        if isinstance(value, list):
            out[key] = {int(item) for item in block_values(value) if item.isdigit()}
    return out


def load_terrain_overrides(vanilla_root: Path) -> dict[int, str]:
    parsed = parse_eu4(read_text(vanilla_root / "map" / "terrain.txt"))
    overrides: dict[int, str] = {}
    for key, value in pairs(parsed):
        if key != "categories" or not isinstance(value, list):
            continue
        for category, category_block in pairs(value):
            if not isinstance(category_block, list):
                continue
            for inner_key, inner_value in pairs(category_block):
                if inner_key == "terrain_override" and isinstance(inner_value, list):
                    for item in block_values(inner_value):
                        if item.isdigit():
                            overrides[int(item)] = category
    return overrides


def load_culture_data(vanilla_root: Path) -> tuple[dict[str, str], dict[str, str]]:
    culture_to_group: dict[str, str] = {}
    culture_primary_tag: dict[str, str] = {}
    meta_blocks = {
        "graphical_culture",
        "second_graphical_culture",
        "male_names",
        "female_names",
        "dynasty_names",
        "country",
        "province",
    }
    for path in sorted((vanilla_root / "common" / "cultures").glob("*.txt")):
        parsed = parse_eu4(read_text(path))
        for group, group_block in pairs(parsed):
            if not isinstance(group_block, list):
                continue
            for culture, culture_block in pairs(group_block):
                if culture in meta_blocks or not isinstance(culture_block, list):
                    continue
                culture_to_group[culture] = group
                primary = first_scalar(culture_block, "primary")
                if primary:
                    culture_primary_tag[culture] = primary
    return culture_to_group, culture_primary_tag


def load_country_tags(vanilla_root: Path) -> dict[str, str]:
    tags: dict[str, str] = {}
    for path in sorted((vanilla_root / "common" / "country_tags").glob("*.txt")):
        text = strip_comments(read_text(path))
        for match in re.finditer(r"\b([A-Z0-9]{3})\s*=\s*\"([^\"]+)\"", text):
            tags[match.group(1)] = match.group(2)
    return tags


def load_country_histories(vanilla_root: Path) -> dict[str, dict[str, Any]]:
    histories: dict[str, dict[str, Any]] = {}
    scalar_keys = {"primary_culture", "religion", "capital", "government", "technology_group"}
    multi_keys = {"historical_rival", "historical_friend", "add_accepted_culture"}
    for path in sorted((vanilla_root / "history" / "countries").glob("*.txt")):
        match = re.match(r"([A-Z0-9]{3})\s*-", path.name)
        if not match:
            continue
        tag = match.group(1)
        parsed = parse_eu4(read_text(path))
        state = history_state(parsed, scalar_keys, multi_keys=multi_keys)
        state["history_file"] = path.name
        histories[tag] = state
    return histories


def load_province_histories(vanilla_root: Path) -> dict[int, dict[str, Any]]:
    histories: dict[int, dict[str, Any]] = {}
    scalar_keys = {
        "owner",
        "controller",
        "culture",
        "religion",
        "base_tax",
        "base_production",
        "base_manpower",
        "trade_goods",
        "capital",
        "is_city",
        "hre",
    }
    for path in sorted((vanilla_root / "history" / "provinces").glob("*.txt")):
        match = re.match(r"(\d+)", path.name)
        if not match:
            continue
        province_id = int(match.group(1))
        parsed = parse_eu4(read_text(path))
        state = history_state(parsed, scalar_keys, track_cores=True)
        state["history_file"] = path.name
        histories[province_id] = state
    return histories


def province_type(province_id: int, default_sets: dict[str, set[int]], climate_sets: dict[str, set[int]]) -> str:
    if province_id in default_sets.get("lakes", set()):
        return "lake"
    if province_id in default_sets.get("sea_starts", set()):
        return "sea"
    if province_id in climate_sets.get("impassable", set()):
        return "wasteland"
    if province_id in default_sets.get("only_used_for_random", set()):
        return "random_only"
    return "land"


def load_data_context(
    vanilla_root: Path = DEFAULT_VANILLA_ROOT,
    project_root: Path = DEFAULT_PROJECT_ROOT,
    project_bmp: Path | None = None,
    scan_project_map: bool = True,
) -> dict[str, Any]:
    definitions, color_to_id = load_definition(vanilla_root)
    areas, province_to_area = load_area_data(vanilla_root)
    regions, province_to_region = load_region_data(vanilla_root, areas)
    superregions, province_to_superregion = load_superregion_data(vanilla_root, province_to_region)
    continents, province_to_continent = load_continent_data(vanilla_root)
    default_sets = load_default_map_sets(vanilla_root)
    climate_sets = load_climate_sets(vanilla_root)
    terrain_overrides = load_terrain_overrides(vanilla_root)
    culture_to_group, culture_primary_tag = load_culture_data(vanilla_root)
    country_tags = load_country_tags(vanilla_root)
    country_histories = load_country_histories(vanilla_root)
    province_histories = load_province_histories(vanilla_root)
    project_bmp = project_bmp or project_root / "Mod Build" / "project_crown" / "map" / "provinces.bmp"
    project_present_ids: set[int] | None = None
    if scan_project_map and project_bmp.exists():
        project_present_ids = scan_bmp_province_ids(project_bmp, color_to_id)
    return {
        "vanilla_root": str(vanilla_root),
        "project_root": str(project_root),
        "project_bmp": str(project_bmp),
        "definitions": definitions,
        "color_to_id": color_to_id,
        "areas": areas,
        "province_to_area": province_to_area,
        "regions": regions,
        "province_to_region": province_to_region,
        "superregions": superregions,
        "province_to_superregion": province_to_superregion,
        "continents": continents,
        "province_to_continent": province_to_continent,
        "default_sets": default_sets,
        "climate_sets": climate_sets,
        "terrain_overrides": terrain_overrides,
        "culture_to_group": culture_to_group,
        "culture_primary_tag": culture_primary_tag,
        "country_tags": country_tags,
        "country_histories": country_histories,
        "province_histories": province_histories,
        "project_present_ids": project_present_ids,
    }


def build_province_table(context: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    project_present_ids: set[int] | None = context["project_present_ids"]
    for province_id in sorted(context["definitions"]):
        definition = context["definitions"][province_id]
        history = context["province_histories"].get(province_id, {})
        culture = history.get("culture")
        terrain = context["terrain_overrides"].get(province_id)
        row = {
            "province_id": province_id,
            "province_name": definition["name"],
            "map_color_rgb": list(definition["color"]),
            "present_in_project_map": None if project_present_ids is None else province_id in project_present_ids,
            "culture": culture,
            "culture_group": context["culture_to_group"].get(culture) if culture else None,
            "religion": history.get("religion"),
            "vanilla_owner": history.get("owner"),
            "vanilla_controller": history.get("controller"),
            "vanilla_cores": history.get("cores", []),
            "area": context["province_to_area"].get(province_id),
            "region": context["province_to_region"].get(province_id),
            "superregion": context["province_to_superregion"].get(province_id),
            "continent": context["province_to_continent"].get(province_id),
            "terrain": terrain,
            "terrain_source": "terrain.txt override" if terrain else None,
            "province_type": province_type(province_id, context["default_sets"], context["climate_sets"]),
            "history_file": history.get("history_file"),
        }
        rows.append(row)
    return rows


def summarize_cultures(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_culture: dict[str, dict[str, Any]] = {}
    for row in rows:
        culture = row.get("culture") or "unknown"
        entry = by_culture.setdefault(
            culture,
            {
                "culture": culture,
                "culture_group": row.get("culture_group"),
                "province_count": 0,
                "land_province_count": 0,
                "province_ids": [],
            },
        )
        entry["province_count"] += 1
        entry["province_ids"].append(row["province_id"])
        if row.get("province_type") == "land":
            entry["land_province_count"] += 1
    return {
        "culture_count": len(by_culture),
        "cultures": sorted(by_culture.values(), key=lambda item: (-item["land_province_count"], item["culture"])),
    }
