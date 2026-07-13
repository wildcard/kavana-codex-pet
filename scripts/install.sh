#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET="$CODEX_DIR/pets/kavana"

mkdir -p "$TARGET"
cp "$ROOT/dist/kavana/pet.json" "$TARGET/pet.json"
cp "$ROOT/dist/kavana/spritesheet.webp" "$TARGET/spritesheet.webp"

echo "Installed Kavana to $TARGET"
echo "Select Kavana in Codex Desktop: Settings > Appearance > Pets."
