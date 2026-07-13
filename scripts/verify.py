#!/usr/bin/env python3
"""Verify the standalone Kavana Codex pet repository."""

from __future__ import annotations

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

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


class WebsiteReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        for name in ("src", "href", "poster"):
            reference = attributes.get(name)
            if reference:
                self.references.append(reference)


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
    base_path = ROOT / "source" / "row-strips" / "base.png"
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
    with Image.open(base_path) as base:
        if base.size != (1205, 1305) or base.mode not in {"RGB", "RGBA"}:
            fail(f"canonical base must be RGB/RGBA 1205x1305, got {base.mode} {base.size}")
    if metadata["source"]["canonicalBase"] != {
        "path": "source/row-strips/base.png",
        "sha256": sha256(base_path),
    }:
        fail("canonical base metadata mismatch")

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

    docs_root = ROOT / "docs"
    website_html = docs_root / "index.html"
    website_script = docs_root / "script.js"
    website_style = docs_root / "style.css"
    for path in (website_html, website_script, website_style):
        if not path.is_file():
            fail(f"missing website file: {path.relative_to(ROOT)}")

    parser = WebsiteReferenceParser()
    html = website_html.read_text(encoding="utf-8")
    parser.feed(html)
    if parser.duplicate_ids:
        fail(f"duplicate website ids: {', '.join(sorted(parser.duplicate_ids))}")
    for reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith(("#", "data:")):
            continue
        path = docs_root / parsed.path
        if not path.is_file():
            fail(f"missing local website reference: {reference}")

    docs_assets = docs_root / "assets"
    mirrored_assets = {
        docs_assets / "spritesheet.webp": atlas_path,
        docs_assets / "contact-sheet.png": ROOT / "assets" / "contact-sheet.png",
        docs_assets / "canonical-base.png": base_path,
    }
    for website_asset, canonical_asset in mirrored_assets.items():
        if not website_asset.is_file() or sha256(website_asset) != sha256(canonical_asset):
            fail(f"stale website asset: {website_asset.relative_to(ROOT)}")
    for preview in (ROOT / "assets" / "previews").glob("*.mp4"):
        website_preview = docs_assets / "previews" / preview.name
        if not website_preview.is_file() or sha256(website_preview) != sha256(preview):
            fail(f"stale website preview: {website_preview.relative_to(ROOT)}")

    poster_sources = {
        "idle": "idle", "running-right": "running-right", "running-left": "running-left",
        "waving": "waving", "jumping": "jumping", "failed": "failed",
        "waiting": "waiting", "running": "running", "review": "review", "look-around": "look-a",
    }
    for poster_name, frame_state in poster_sources.items():
        website_poster = docs_assets / "posters" / f"{poster_name}.png"
        canonical_frame = ROOT / "source" / "frames" / frame_state / "00.png"
        if not website_poster.is_file() or sha256(website_poster) != sha256(canonical_frame):
            fail(f"stale website poster: {website_poster.relative_to(ROOT)}")

    required_experience = {
        'data-action="zoomies"', 'data-action="roam"', 'data-action="wave"',
        'data-action="jump"', 'data-action="look"', 'data-action="work"',
        'data-action="sleep"', 'data-play-all', 'data-install-tab="windows"',
        'data-wake-mobile', 'assets/contact-sheet.png',
    }
    missing_experience = sorted(token for token in required_experience if token not in html)
    if missing_experience:
        fail(f"website experience is incomplete: {', '.join(missing_experience)}")

    text_extensions = {".md", ".txt", ".json", ".cff", ".yml", ".yaml", ".py", ".ps1", ".sh", ".html", ".css", ".js"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if any(marker in text for marker in PRIVATE_MARKERS):
            fail(f"private or machine-specific path found in {path.relative_to(ROOT)}")

    print("PASS: Kavana package, v2 atlas, website experience, checksums, source assets, previews, and privacy scan are valid.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        fail(str(error))
