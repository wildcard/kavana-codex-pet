#!/usr/bin/env python3
"""Verify the standalone Kavana Codex pet repository."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PREVIEWS = {
    "idle", "running-right", "running-left", "waving", "jumping",
    "failed", "waiting", "running", "review", "look-around",
}
PRIVATE_MARKERS = [
    "/" + "Users/",
    ":\\" + "Users\\",
    "kobik" + "-private",
    ".codex/" + "worktrees",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    manifest_path = ROOT / "dist" / "kavana" / "pet.json"
    atlas_path = ROOT / "dist" / "kavana" / "spritesheet.webp"
    metadata_path = ROOT / "metadata" / "atlas.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    if manifest.get("id") != "kavana" or manifest.get("displayName") != "Kavana":
        fail("pet manifest identity mismatch")
    if manifest.get("spriteVersionNumber") != 2:
        fail("spriteVersionNumber must be 2")
    if manifest.get("spritesheetPath") != "spritesheet.webp":
        fail("spritesheetPath must be relative to the pet manifest")

    with Image.open(atlas_path) as atlas:
        if atlas.size != (1536, 2288) or atlas.mode != "RGBA":
            fail(f"atlas must be RGBA 1536x2288, got {atlas.mode} {atlas.size}")
    atlas_hash = sha256(atlas_path)
    if metadata["atlas"]["sha256"] != atlas_hash:
        fail("metadata atlas checksum mismatch")

    sums: dict[str, str] = {}
    for line in (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        sums[relative] = digest
    for relative, expected in sums.items():
        path = ROOT / relative
        if not path.is_file() or sha256(path) != expected:
            fail(f"checksum mismatch: {relative}")

    previews = {path.stem for path in (ROOT / "assets" / "previews").glob("*.mp4")}
    missing_previews = EXPECTED_PREVIEWS - previews
    if missing_previews:
        fail(f"missing previews: {', '.join(sorted(missing_previews))}")
    for state in EXPECTED_PREVIEWS - {"look-around"}:
        if not (ROOT / "source" / "row-strips" / f"{state}.png").is_file():
            fail(f"missing row strip: {state}")

    text_extensions = {".md", ".txt", ".json", ".cff", ".yml", ".yaml", ".py", ".ps1", ".sh", ".html", ".css", ".js"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if any(marker in text for marker in PRIVATE_MARKERS):
            fail(f"private or machine-specific path found in {path.relative_to(ROOT)}")

    print("PASS: Kavana package, v2 atlas, checksums, source assets, previews, and privacy scan are valid.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        fail(str(error))
