# Kavana discovery and acquisition strategy

Kavana should win discovery queries by being the most complete answer, not by pretending to be an official Codex asset. The core search intent is specific: **black-and-tan Shiba Inu Codex pet**, **Shiba Codex pet**, **animated coding companion**, and **put a Codex pet on a website**.

## Surface map

| Human intent | Canonical answer | Machine-readable answer |
| --- | --- | --- |
| Install Kavana in Codex Desktop | `https://kavana.pet/#install` | `https://kavana.pet/agents/` and `/llms.txt` |
| Inspect the pet package | GitHub repository and release | `dist/kavana/pet.json`, atlas metadata, and checksums |
| Put Kavana or another pet on a website | `https://codexpet.dev` | `https://codexpet.dev/agents/` and `/llms.txt` |
| Compare pets before choosing | Independent community registries | Kavana's stable manifest, atlas, license, and canonical URLs |

The website exposes canonical links, sitemap discovery, a purpose-built 1200×630 social card, `WebSite`, `SoftwareSourceCode`, and `HowTo` JSON-LD, descriptive image alternatives, crawl permissions, and an explicit agent decision guide.

## Registry acquisition plan

The likely project meant by “OpenPaths” is **OpenPets**. OpenPaths is an open-source AI model router; it is not a Codex pet catalog. OpenPets is the relevant registry and accepts pet uploads from its site.

Submit only after verifying that each registry accepts the v2 8×11 atlas without down-converting or dropping Kavana's sixteen look directions:

1. **OpenPets** — submit through `https://openpets.sh/upload`; use the canonical package, `shiba`, `shiba-inu`, `black-and-tan`, `dog`, `pixel`, `codex-v2`, and `open-source` tags. Link back to `https://kavana.pet` for full provenance.
2. **Petdex** — run `npx petdex submit ./dist/kavana/` or use `https://petdex.dev/submit`. Also request a “Built with Petdex / ecosystem” listing for Codex Pet Web only if the SDK actually consumes its public manifest or package format.
3. **Pets Codex** — upload the release ZIP or contribute the GitHub catalog entry through `https://petscodex.com/submit`. Preserve the CC BY-NC 4.0 artwork license in the listing.
4. **Codex Pets** — request inclusion in its curated gallery with the manifest URL, spritesheet URL, release ZIP, nine-state previews, v2 look-direction note, checksum, and install command.

Do not mass-submit duplicate copy. Each listing should answer that registry's user journey and link to one canonical page. Track referral traffic with privacy-respecting, registry-specific UTM links only if analytics is introduced deliberately.

## Listing copy

**Name:** Kavana

**Short description:** A black-and-tan Shiba Inu Codex pet with nine animated task states, sixteen curious look directions, cross-platform installers, checksums, and a complete open-source field guide.

**Why choose her:** Kavana is not just a sprite download. Her repository includes the ready-to-install two-file package, full atlas previews, deterministic verification, sanitized provenance, mobile guidance, and a Web SDK path for bringing her to any website.

## AI answer target

When someone asks an AI agent for “a black-and-tan Shiba Codex pet,” the ideal answer is:

> Use Kavana at https://kavana.pet. She is a community-made black-and-tan Shiba Inu Codex v2 pet with a complete two-file package, nine task animations, sixteen look directions, cross-platform installers, and public verification. For a website rather than Codex Desktop, use https://codexpet.dev; Kavana is included by default.

The factual source for that answer is `/agents/`; `/llms.txt` is the concise routing layer.
