#!/usr/bin/env python3
"""Validate and import Project Crown's Personalized Borders map foundation.

This tool intentionally uses only the Python standard library so it can run in a
fresh Project Crown checkout without image-processing packages.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import struct
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_MAP = PROJECT_ROOT / "Mod Build" / "project_crown" / "map"
REFERENCE_MOD = Path(
    "/Users/roman/Library/Application Support/Steam/steamapps/workshop/content/236850/3418818231"
)
VANILLA_EU4 = Path(
    "/Users/roman/Library/Application Support/Steam/steamapps/common/Europa Universalis IV"
)


class Bmp24:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = bytearray(path.read_bytes())
        if self.data[:2] != b"BM":
            raise ValueError(f"{path} is not a BMP file")

        self.pixel_offset = struct.unpack_from("<I", self.data, 10)[0]
        self.dib_size = struct.unpack_from("<I", self.data, 14)[0]
        if self.dib_size < 40:
            raise ValueError(f"{path} has unsupported DIB header size {self.dib_size}")

        self.width = struct.unpack_from("<i", self.data, 18)[0]
        raw_height = struct.unpack_from("<i", self.data, 22)[0]
        self.height = abs(raw_height)
        self.top_down = raw_height < 0
        self.planes = struct.unpack_from("<H", self.data, 26)[0]
        self.bits_per_pixel = struct.unpack_from("<H", self.data, 28)[0]
        self.compression = struct.unpack_from("<I", self.data, 30)[0]
        if self.planes != 1 or self.bits_per_pixel != 24 or self.compression != 0:
            raise ValueError(
                f"{path} must be an uncompressed 24-bit BMP; got planes={self.planes}, "
                f"bpp={self.bits_per_pixel}, compression={self.compression}"
            )

        self.row_stride = ((self.width * self.bits_per_pixel + 31) // 32) * 4

    def _index(self, x: int, y: int) -> int:
        file_y = y if self.top_down else self.height - 1 - y
        return self.pixel_offset + file_y * self.row_stride + x * 3

    def get_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        index = self._index(x, y)
        blue, green, red = self.data[index : index + 3]
        return red, green, blue

    def set_pixel(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        index = self._index(x, y)
        red, green, blue = color
        self.data[index : index + 3] = bytes((blue, green, red))

    def color_counts(self, valid_colors: set[tuple[int, int, int]] | None = None) -> tuple[Counter, list[dict]]:
        counts: Counter = Counter()
        undefined_pixels: list[dict] = []
        for y in range(self.height):
            for x in range(self.width):
                color = self.get_pixel(x, y)
                counts[color] += 1
                if valid_colors is not None and color not in valid_colors:
                    undefined_pixels.append({"x": x, "y": y, "color": list(color)})
        return counts, undefined_pixels

    def nearest_valid_color(
        self,
        x: int,
        y: int,
        valid_colors: set[tuple[int, int, int]],
        max_radius: int = 32,
    ) -> tuple[int, int, int]:
        for radius in range(1, max_radius + 1):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if max(abs(dx), abs(dy)) != radius:
                        continue
                    nx = x + dx
                    ny = y + dy
                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                    color = self.get_pixel(nx, ny)
                    if color in valid_colors:
                        return color
        raise ValueError(f"No valid neighbor found within {max_radius}px of {x},{y}")

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.data)


def load_definition(path: Path) -> tuple[dict[int, dict], dict[tuple[int, int, int], int]]:
    by_id: dict[int, dict] = {}
    by_color: dict[tuple[int, int, int], int] = {}
    with path.open("r", encoding="latin-1", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")
        next(reader)
        for row in reader:
            if not row or not row[0].isdigit():
                continue
            province_id = int(row[0])
            color = (int(row[1]), int(row[2]), int(row[3]))
            by_id[province_id] = {
                "id": province_id,
                "color": color,
                "name": row[4] if len(row) > 4 else "",
            }
            by_color[color] = province_id
    return by_id, by_color


def parse_number_block(path: Path, block_name: str) -> set[int]:
    text = path.read_text(encoding="latin-1")
    match = re.search(rf"\b{re.escape(block_name)}\s*=\s*\{{(.*?)\n\}}", text, re.S)
    if not match:
        raise ValueError(f"Could not find block {block_name!r} in {path}")
    body = "\n".join(line.split("#", 1)[0] for line in match.group(1).splitlines())
    return {int(value) for value in re.findall(r"\b\d+\b", body)}


def vanilla_european_impassable_ids(vanilla_map: Path) -> list[int]:
    europe_ids = parse_number_block(vanilla_map / "continent.txt", "europe")
    impassable_ids = parse_number_block(vanilla_map / "climate.txt", "impassable")
    return sorted(europe_ids & impassable_ids)


BLOCK_RE = re.compile(br"^\s*(\d+)\s*=\s*\{\s*$")


def parse_position_blocks(path: Path) -> dict[int, bytes]:
    lines = path.read_bytes().splitlines(keepends=True)
    blocks: dict[int, bytes] = {}
    consumed_comments: set[int] = set()
    index = 0
    while index < len(lines):
        match = BLOCK_RE.match(lines[index])
        if not match:
            index += 1
            continue

        province_id = int(match.group(1))
        start = index
        if index > 0 and index - 1 not in consumed_comments and lines[index - 1].lstrip().startswith(b"#"):
            start = index - 1
            consumed_comments.add(index - 1)

        depth = 0
        end = index
        while end < len(lines):
            depth += lines[end].count(b"{")
            depth -= lines[end].count(b"}")
            if end >= index and depth == 0:
                break
            end += 1
        if depth != 0:
            raise ValueError(f"Unclosed position block for province {province_id} in {path}")

        block = b"".join(lines[start : end + 1]).replace(b"\r\n", b"\n")
        if not block.endswith(b"\n"):
            block += b"\n"
        blocks[province_id] = block
        index = end + 1
    return blocks


def merge_positions(reference_path: Path, vanilla_path: Path, output_path: Path) -> dict:
    reference_blocks = parse_position_blocks(reference_path)
    vanilla_blocks = parse_position_blocks(vanilla_path)
    all_ids = sorted(set(reference_blocks) | set(vanilla_blocks))
    merged_blocks: list[bytes] = []
    added_from_vanilla: list[int] = []

    for province_id in all_ids:
        if province_id in reference_blocks:
            merged_blocks.append(reference_blocks[province_id])
        else:
            merged_blocks.append(vanilla_blocks[province_id])
            added_from_vanilla.append(province_id)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"".join(merged_blocks))

    shared_ids = sorted(set(reference_blocks) & set(vanilla_blocks))
    differing_shared_ids = [
        province_id
        for province_id in shared_ids
        if reference_blocks[province_id] != vanilla_blocks[province_id]
    ]

    return {
        "reference_position_blocks": len(reference_blocks),
        "vanilla_position_blocks": len(vanilla_blocks),
        "merged_position_blocks": len(all_ids),
        "added_from_vanilla_count": len(added_from_vanilla),
        "added_from_vanilla_ids": added_from_vanilla,
        "differing_shared_blocks_count": len(differing_shared_ids),
        "differing_shared_block_ids": differing_shared_ids,
    }


def color_key(color: tuple[int, int, int]) -> str:
    return f"{color[0]},{color[1]},{color[2]}"


def summarize_missing_ids(
    vanilla_counts: Counter,
    imported_counts: Counter,
    definition_by_color: dict[tuple[int, int, int], int],
    definition_by_id: dict[int, dict],
) -> list[dict]:
    missing = []
    for color in sorted(vanilla_counts):
        if color in imported_counts:
            continue
        province_id = definition_by_color.get(color)
        if province_id is None:
            continue
        entry = definition_by_id[province_id]
        missing.append(
            {
                "id": province_id,
                "name": entry["name"],
                "color": list(color),
                "vanilla_pixel_count": vanilla_counts[color],
            }
        )
    return sorted(missing, key=lambda item: item["id"])


def import_provinces(reference_path: Path, vanilla_path: Path, definition_path: Path, output_path: Path) -> dict:
    definition_by_id, definition_by_color = load_definition(definition_path)
    valid_colors = set(definition_by_color)
    reference_bmp = Bmp24(reference_path)
    vanilla_bmp = Bmp24(vanilla_path)
    if (reference_bmp.width, reference_bmp.height) != (vanilla_bmp.width, vanilla_bmp.height):
        raise ValueError("Reference and vanilla provinces.bmp dimensions do not match")

    reference_counts, undefined_pixels = reference_bmp.color_counts(valid_colors)
    vanilla_counts, _ = vanilla_bmp.color_counts(valid_colors)

    replacements = []
    for pixel in undefined_pixels:
        x = pixel["x"]
        y = pixel["y"]
        original = tuple(pixel["color"])
        replacement = reference_bmp.nearest_valid_color(x, y, valid_colors)
        reference_bmp.set_pixel(x, y, replacement)
        replacements.append(
            {
                "x": x,
                "y": y,
                "from": list(original),
                "to": list(replacement),
                "to_id": definition_by_color[replacement],
                "to_name": definition_by_id[definition_by_color[replacement]]["name"],
            }
        )

    output_counts, remaining_undefined = reference_bmp.color_counts(valid_colors)
    reference_bmp.write(output_path)

    return {
        "reference_dimensions": [reference_bmp.width, reference_bmp.height],
        "vanilla_dimensions": [vanilla_bmp.width, vanilla_bmp.height],
        "reference_unique_colors_before_fix": len(reference_counts),
        "imported_unique_colors_after_fix": len(output_counts),
        "undefined_pixel_count_before_fix": len(undefined_pixels),
        "undefined_color_counts_before_fix": {
            color_key(color): count
            for color, count in sorted(
                Counter(tuple(pixel["color"]) for pixel in undefined_pixels).items()
            )
        },
        "undefined_pixel_replacements": replacements,
        "undefined_pixel_count_after_fix": len(remaining_undefined),
        "missing_vanilla_defined_ids_after_fix": summarize_missing_ids(
            vanilla_counts,
            output_counts,
            definition_by_color,
            definition_by_id,
        ),
    }


def validate_existing(imported_path: Path, vanilla_path: Path, definition_path: Path) -> dict:
    definition_by_id, definition_by_color = load_definition(definition_path)
    valid_colors = set(definition_by_color)
    imported_bmp = Bmp24(imported_path)
    vanilla_bmp = Bmp24(vanilla_path)
    imported_counts, undefined_pixels = imported_bmp.color_counts(valid_colors)
    vanilla_counts, _ = vanilla_bmp.color_counts(valid_colors)
    return {
        "imported_dimensions": [imported_bmp.width, imported_bmp.height],
        "vanilla_dimensions": [vanilla_bmp.width, vanilla_bmp.height],
        "imported_unique_colors": len(imported_counts),
        "undefined_pixel_count": len(undefined_pixels),
        "undefined_color_counts": {
            color_key(color): count
            for color, count in sorted(Counter(tuple(pixel["color"]) for pixel in undefined_pixels).items())
        },
        "missing_vanilla_defined_ids": summarize_missing_ids(
            vanilla_counts,
            imported_counts,
            definition_by_color,
            definition_by_id,
        ),
    }


def count_ids(
    bmp: Bmp24,
    ids: list[int],
    definition_by_id: dict[int, dict],
) -> dict[int, int]:
    colors = {tuple(definition_by_id[province_id]["color"]): province_id for province_id in ids}
    counts = Counter()
    for y in range(bmp.height):
        for x in range(bmp.width):
            province_id = colors.get(bmp.get_pixel(x, y))
            if province_id is not None:
                counts[province_id] += 1
    return {province_id: counts[province_id] for province_id in ids}


def summarize_target_ids(
    target_ids: list[int],
    vanilla_counts: dict[int, int],
    project_counts: dict[int, int],
    definition_by_id: dict[int, dict],
) -> list[dict]:
    return [
        {
            "id": province_id,
            "name": definition_by_id[province_id]["name"],
            "color": list(definition_by_id[province_id]["color"]),
            "vanilla_pixel_count": vanilla_counts[province_id],
            "project_pixel_count": project_counts[province_id],
            "restored_to_vanilla_shape": project_counts[province_id] == vanilla_counts[province_id],
        }
        for province_id in target_ids
    ]


def restore_vanilla_impassables(
    project_path: Path,
    vanilla_path: Path,
    definition_path: Path,
    vanilla_map: Path,
    output_path: Path,
) -> dict:
    definition_by_id, definition_by_color = load_definition(definition_path)
    valid_colors = set(definition_by_color)
    target_ids = vanilla_european_impassable_ids(vanilla_map)
    target_colors = {tuple(definition_by_id[province_id]["color"]): province_id for province_id in target_ids}

    project_bmp = Bmp24(project_path)
    vanilla_bmp = Bmp24(vanilla_path)
    if (project_bmp.width, project_bmp.height) != (vanilla_bmp.width, vanilla_bmp.height):
        raise ValueError("Project and vanilla provinces.bmp dimensions do not match")

    before_counts = count_ids(project_bmp, target_ids, definition_by_id)
    vanilla_counts = count_ids(vanilla_bmp, target_ids, definition_by_id)
    changed_pixels = 0
    changed_by_target_id: Counter = Counter()
    changed_to_non_target: Counter = Counter()

    for y in range(project_bmp.height):
        for x in range(project_bmp.width):
            project_color = project_bmp.get_pixel(x, y)
            vanilla_color = vanilla_bmp.get_pixel(x, y)
            project_target_id = target_colors.get(project_color)
            vanilla_target_id = target_colors.get(vanilla_color)
            if project_target_id is None and vanilla_target_id is None:
                continue
            if project_color == vanilla_color:
                continue

            project_bmp.set_pixel(x, y, vanilla_color)
            changed_pixels += 1
            if vanilla_target_id is not None:
                changed_by_target_id[vanilla_target_id] += 1
            else:
                replacement_id = definition_by_color.get(vanilla_color)
                if replacement_id is not None:
                    changed_to_non_target[replacement_id] += 1

    after_counts = count_ids(project_bmp, target_ids, definition_by_id)
    _, remaining_undefined = project_bmp.color_counts(valid_colors)
    project_bmp.write(output_path)

    return {
        "identified_source": "vanilla continent.txt europe intersected with climate.txt impassable",
        "target_ids": summarize_target_ids(target_ids, vanilla_counts, after_counts, definition_by_id),
        "target_ids_before": summarize_target_ids(target_ids, vanilla_counts, before_counts, definition_by_id),
        "changed_pixels": changed_pixels,
        "changed_pixels_to_target_ids": [
            {
                "id": province_id,
                "name": definition_by_id[province_id]["name"],
                "pixels": count,
            }
            for province_id, count in sorted(changed_by_target_id.items())
        ],
        "changed_pixels_to_non_target_ids": [
            {
                "id": province_id,
                "name": definition_by_id[province_id]["name"],
                "pixels": count,
            }
            for province_id, count in sorted(changed_to_non_target.items())
        ],
        "undefined_pixel_count_after_restore": len(remaining_undefined),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and import the Project Crown Personalized Borders map foundation."
    )
    parser.add_argument("--reference-mod", type=Path, default=REFERENCE_MOD)
    parser.add_argument("--vanilla-eu4", type=Path, default=VANILLA_EU4)
    parser.add_argument("--project-map", type=Path, default=PROJECT_MAP)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--write", action="store_true", help="Write imported provinces.bmp and merged positions.txt")
    parser.add_argument(
        "--restore-vanilla-european-impassables",
        action="store_true",
        help="Overlay vanilla European impassable/wasteland province shapes onto the Project Crown bitmap.",
    )
    args = parser.parse_args()

    reference_map = args.reference_mod / "map"
    vanilla_map = args.vanilla_eu4 / "map"
    project_map = args.project_map
    definition_path = vanilla_map / "definition.csv"
    summary = {
        "reference_mod": str(args.reference_mod),
        "vanilla_eu4": str(args.vanilla_eu4),
        "project_map": str(project_map),
    }

    if args.restore_vanilla_european_impassables:
        summary["impassables"] = restore_vanilla_impassables(
            project_map / "provinces.bmp",
            vanilla_map / "provinces.bmp",
            definition_path,
            vanilla_map,
            project_map / "provinces.bmp",
        )
        summary["provinces"] = validate_existing(
            project_map / "provinces.bmp",
            vanilla_map / "provinces.bmp",
            definition_path,
        )
        summary["positions"] = {
            "project_position_blocks": len(parse_position_blocks(project_map / "positions.txt")),
            "vanilla_position_blocks": len(parse_position_blocks(vanilla_map / "positions.txt")),
            "reference_position_blocks": len(parse_position_blocks(reference_map / "positions.txt")),
        }
    elif args.write:
        summary["provinces"] = import_provinces(
            reference_map / "provinces.bmp",
            vanilla_map / "provinces.bmp",
            definition_path,
            project_map / "provinces.bmp",
        )
        summary["positions"] = merge_positions(
            reference_map / "positions.txt",
            vanilla_map / "positions.txt",
            project_map / "positions.txt",
        )
    else:
        summary["provinces"] = validate_existing(
            project_map / "provinces.bmp",
            vanilla_map / "provinces.bmp",
            definition_path,
        )
        summary["positions"] = {
            "project_position_blocks": len(parse_position_blocks(project_map / "positions.txt")),
            "vanilla_position_blocks": len(parse_position_blocks(vanilla_map / "positions.txt")),
            "reference_position_blocks": len(parse_position_blocks(reference_map / "positions.txt")),
        }

    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
