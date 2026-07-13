# Contributing

Small, focused contributions are welcome: install documentation, platform compatibility, preview quality, metadata and checksum fixes, validation improvements, and accessibility improvements to the landing page.

## Asset Rules

- Never commit private photos, raw references, prompt dumps, job logs, local Codex state, credentials, or machine-specific paths.
- Keep `dist/kavana/pet.json` and `dist/kavana/spritesheet.webp` installable together.
- Kavana is a black-and-tan Shiba Inu; preserve her tan eyebrow spots, cream muzzle and chest, upright ears, compact build, and curled tail.
- Preserve the 8×11 v2 atlas geometry and clockwise look-direction order.
- Update `SHA256SUMS.txt`, `metadata/atlas.json`, `CHANGELOG.md`, and preview/source assets when released art changes.

## Before a Pull Request

```bash
python3 scripts/verify.py
```

Also inspect the diff for private material and explain any asset provenance or compatibility claim.
