#!/usr/bin/env python3
"""Rebuild Kavana's public inspection assets from the shipped v2 atlas."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "dist" / "kavana" / "spritesheet.webp"
BASE_PATH = ROOT / "source" / "row-strips" / "base.png"
CELL_W, CELL_H = 192, 208
ROWS = [
    ("idle", 0, 6, [280, 110, 110, 140, 140, 320]),
    ("running-right", 1, 8, [120, 120, 120, 120, 120, 120, 120, 220]),
    ("running-left", 2, 8, [120, 120, 120, 120, 120, 120, 120, 220]),
    ("waving", 3, 4, [140, 140, 140, 280]),
    ("jumping", 4, 5, [140, 140, 140, 140, 280]),
    ("failed", 5, 8, [140, 140, 140, 140, 140, 140, 140, 240]),
    ("waiting", 6, 6, [150, 150, 150, 150, 150, 260]),
    ("running", 7, 6, [120, 120, 120, 120, 120, 220]),
    ("review", 8, 6, [150, 150, 150, 150, 150, 280]),
    ("look-a", 9, 8, [150] * 8),
    ("look-b", 10, 8, [150] * 8),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_preview(name: str, frames: list[Image.Image], durations: list[int]) -> None:
    target = ROOT / "assets" / "previews" / f"{name}.mp4"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(f"warning: ffmpeg unavailable; skipped {target.relative_to(ROOT)}")
        return
    with tempfile.TemporaryDirectory(prefix="kavana-preview-") as temp_dir:
        temp = Path(temp_dir)
        concat_lines: list[str] = []
        expanded: list[Image.Image] = []
        if len(frames) != len(durations):
            raise ValueError(f"frame/duration mismatch for {name}")
        for frame, duration in zip(frames, durations):
            expanded.extend([frame] * max(1, round(duration / 40)))
        expanded.extend(expanded[: min(4, len(expanded))])
        for index, frame in enumerate(expanded):
            path = temp / f"{index:03d}.png"
            frame.save(path)
            concat_lines.append(f"file '{path.as_posix()}'")
            concat_lines.append("duration 0.04")
        list_path = temp / "frames.txt"
        list_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
        subprocess.run(
            [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
             "-i", str(list_path), "-vf", "scale=384:416:flags=neighbor,format=yuv420p",
             "-movflags", "+faststart", str(target)],
            check=True,
        )


def main() -> None:
    atlas = Image.open(ATLAS_PATH).convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"unexpected atlas size: {atlas.size}")

    frames_root = ROOT / "source" / "frames"
    strips_root = ROOT / "source" / "row-strips"
    previews_root = ROOT / "assets" / "previews"
    for directory in (frames_root, strips_root, previews_root):
        directory.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "schemaVersion": 1,
        "cellSize": {"width": CELL_W, "height": CELL_H},
        "rows": [],
        "neutralLookFrame": {"row": 0, "column": 6, "path": "source/frames/neutral/00.png"},
    }

    for name, row, count, durations in ROWS:
        row_frames: list[Image.Image] = []
        frame_dir = frames_root / name
        frame_dir.mkdir(parents=True, exist_ok=True)
        for stale in frame_dir.glob("*.png"):
            stale.unlink()
        for column in range(count):
            frame = atlas.crop((column * CELL_W, row * CELL_H, (column + 1) * CELL_W, (row + 1) * CELL_H))
            frame.save(frame_dir / f"{column:02d}.png")
            row_frames.append(frame)
        strip = Image.new("RGBA", (CELL_W * count, CELL_H), (0, 0, 0, 0))
        for column, frame in enumerate(row_frames):
            strip.alpha_composite(frame, (column * CELL_W, 0))
        strip.save(strips_root / f"{name}.png")
        preview_name = "look-around" if name == "look-a" else name
        if name == "look-b":
            look_a = [Image.open(frames_root / "look-a" / f"{column:02d}.png").convert("RGBA") for column in range(8)]
            save_preview("look-around", look_a + row_frames, [150] * 16)
        elif name != "look-a":
            save_preview(preview_name, row_frames, durations)
        manifest["rows"].append({
            "state": name,
            "row": row,
            "frames": count,
            "durationsMs": durations,
            "strip": f"source/row-strips/{name}.png",
        })

    neutral_dir = frames_root / "neutral"
    neutral_dir.mkdir(parents=True, exist_ok=True)
    neutral = atlas.crop((6 * CELL_W, 0, 7 * CELL_W, CELL_H))
    neutral.save(neutral_dir / "00.png")
    neutral.save(strips_root / "neutral.png")
    (frames_root / "frames-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    labels = [name for name, *_ in ROWS]
    label_w = 150
    sheet = Image.new("RGBA", (label_w + atlas.width, atlas.height), (255, 248, 232, 255))
    sheet.alpha_composite(atlas, (label_w, 0))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, label in enumerate(labels):
        draw.text((12, row * CELL_H + 94), label, fill=(37, 31, 27, 255), font=font)
        draw.line((label_w, row * CELL_H, sheet.width, row * CELL_H), fill=(56, 39, 29, 90), width=1)
    sheet.save(ROOT / "assets" / "contact-sheet.png")

    metadata = {
        "schemaVersion": 1,
        "pet": {
            "id": "kavana",
            "displayName": "Kavana",
            "version": "1.0.0",
            "description": "A black-and-tan Shiba Inu Codex pet contributed by the Project Caro community.",
            "spriteVersionNumber": 2,
        },
        "atlas": {
            "format": "WebP",
            "mode": "RGBA",
            "width": atlas.width,
            "height": atlas.height,
            "columns": 8,
            "rows": 11,
            "cellWidth": CELL_W,
            "cellHeight": CELL_H,
            "lookDirectionCount": 16,
            "neutralLookFrame": {"row": 0, "column": 6},
            "sha256": sha256(ATLAS_PATH),
        },
        "source": {
            "project": "Project Caro",
            "projectUrl": "https://github.com/wildcard/caro",
            "contributionPullRequest": "https://github.com/wildcard/caro/pull/1324",
            "canonicalBase": {
                "path": "source/row-strips/base.png",
                "sha256": sha256(BASE_PATH),
            },
        },
    }
    (ROOT / "metadata").mkdir(exist_ok=True)
    (ROOT / "metadata" / "atlas.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    checksum_paths = [
        ROOT / "dist" / "kavana" / "spritesheet.webp",
        ROOT / "dist" / "kavana" / "pet.json",
        ROOT / "assets" / "contact-sheet.png",
        BASE_PATH,
    ]
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in checksum_paths]
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    docs_assets = ROOT / "docs" / "assets"
    docs_previews = docs_assets / "previews"
    docs_posters = docs_assets / "posters"
    docs_previews.mkdir(parents=True, exist_ok=True)
    docs_posters.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ATLAS_PATH, docs_assets / "spritesheet.webp")
    shutil.copy2(BASE_PATH, docs_assets / "canonical-base.png")
    shutil.copy2(ROOT / "assets" / "contact-sheet.png", docs_assets / "contact-sheet.png")
    for preview in previews_root.glob("*.mp4"):
        shutil.copy2(preview, docs_previews / preview.name)
    poster_sources = {
        "idle": frames_root / "idle" / "00.png",
        "running-right": frames_root / "running-right" / "00.png",
        "running-left": frames_root / "running-left" / "00.png",
        "waving": frames_root / "waving" / "00.png",
        "jumping": frames_root / "jumping" / "00.png",
        "failed": frames_root / "failed" / "00.png",
        "waiting": frames_root / "waiting" / "00.png",
        "running": frames_root / "running" / "00.png",
        "review": frames_root / "review" / "00.png",
        "look-around": frames_root / "look-a" / "00.png",
    }
    for name, source in poster_sources.items():
        shutil.copy2(source, docs_posters / f"{name}.png")

    print("Rebuilt Kavana source assets, public website media, metadata, and checksums.")


if __name__ == "__main__":
    main()
