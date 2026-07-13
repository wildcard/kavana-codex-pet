# Malou → Kavana Parity Ledger

This ledger records the public-project capabilities reviewed from [`mySebbe/malou-codex-pet`](https://github.com/mySebbe/malou-codex-pet) and where Kavana provides the equivalent or stronger capability.

| Malou capability | Kavana implementation | Evidence |
| --- | --- | --- |
| Ready-to-install manifest and transparent WebP atlas | Ready-to-install v2 package | `dist/kavana/` |
| Desktop installation docs | macOS/Linux shell installer, Windows PowerShell installer, and manual instructions | `scripts/install.sh`, `scripts/install.ps1`, `README.md` |
| Select active pet during Windows install | `-Select` writes `custom:kavana` through the repair helper | `scripts/install.ps1` |
| Desktop-to-mobile selection documentation | Same desktop/mobile model without claiming a separate mobile package | `README.md#mobile-sync` |
| Mobile selection diagnosis and repair | Checks and repairs both Codex selection files | `scripts/check-mobile-sync.ps1` |
| Repair after Codex exits | Waits for the running Codex process before repairing selection | `scripts/repair-after-codex-exit.ps1` |
| Nine standard state animations | All nine v2 standard rows | `source/frames/`, `source/row-strips/` |
| Status-readable poses | Distinct failed, waiting, working, and review body-pose families | `assets/previews/` |
| Source frames | Curated transparent frames regenerated from the release atlas | `source/frames/` |
| Source row strips and canonical base | Approved identity render, nine standard rows, neutral frame, and two look rows | `source/row-strips/` |
| Contact sheet | Labeled full 8×11 atlas inspection sheet | `assets/contact-sheet.png` |
| Per-state MP4 previews | All nine standard states plus look-around | `assets/previews/` |
| Sanitized atlas metadata | Version, geometry, checksums, canonical base, provenance, and Caro contribution | `metadata/atlas.json` |
| Package checksums | SHA-256 for manifest, atlas, contact sheet, and canonical base | `SHA256SUMS.txt` |
| Verification script | Cross-platform package, atlas, checksum, source, preview, and privacy validation | `scripts/verify.py`, `.github/workflows/verify.yml` |
| Asset rebuild script | Deterministic source frames, strips, contact sheet, previews, metadata, and checksums | `scripts/rebuild-assets.py` |
| Release notes and changelog | Standalone v1.0.0 release documentation | `RELEASE_NOTES.md`, `CHANGELOG.md` |
| Attribution and split licensing | MIT for project materials; CC BY-NC 4.0 for art | `ATTRIBUTION.md`, `LICENSE.md` |
| Citation metadata | CFF 1.2 metadata | `CITATION.cff` |
| Contribution and conduct guidance | Privacy-aware asset contribution rules | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` |
| Security policy | Supported-version and sensitive-data reporting guidance | `SECURITY.md` |
| Issue and pull request templates | Structured bug areas, privacy gate, and release checks | `.github/` |
| Public landing page | Responsive interactive field guide with state controls, mobile sync, full preview gallery, install UI, atlas inspection, SEO metadata, reduced-motion handling, and scroll reveals | `docs/` |
| Public release package | Versioned GitHub release with install archive | GitHub Releases |

## Website feature parity

| Malou website experience | Kavana implementation |
| --- | --- |
| Hero story, release actions, and package facts | Kavana identity story, release/source actions, and live v2 package facts |
| Interactive Idle, Run, Wave, Jump, and Review picker | Autonomous sequence plus Zoomies, Roam, Wave, Jump, Look, Work/Review, and Nap controls |
| Single-state sprite loop | Duration-aware playback using Kavana’s real per-frame timings and all sixteen look frames |
| Android/iOS screenshot story | Honest connected-host explainer, interactive mobile wake illustration, current OpenAI availability boundary, and repair links |
| Nine hover, focus, and click previews | All nine standard states plus the v2 look-around loop, with individual and Play All controls |
| One-platform install command panel | Keyboard-accessible macOS/Linux, Windows, and manual tabs with clipboard actions |
| Atlas specifications and contact sheet | v2 geometry, checksum, metadata, CI, full contact sheet, and approved canonical base |
| Scroll reveal choreography | Intersection-observed reveals with a no-JavaScript-safe visible page structure |
| Reduced-motion video and sprite behavior | Automatic motion disabled while every action remains available as a persistent still pose |
| Canonical, Open Graph, Twitter, and CSP metadata | Equivalent public metadata using Kavana’s canonical derived artwork |
| Public-project provenance | Malou inspiration, Project Caro contribution, privacy boundary, attribution, licensing, and contribution paths |

## Kavana’s v2 additions

Kavana preserves Malou’s project-level completeness and adds newer Codex pet capabilities:

- `spriteVersionNumber: 2`
- 8×11 atlas (`1536 × 2288`) rather than 8×9
- sixteen clockwise pointer-aware look directions
- explicit neutral look frame
- tenth preview covering the look-around loop
- deterministic privacy scanning in the verifier
- top-of-page Caro-derived zoomies, roaming, work/review, look, and rest controls
- keyboard-accessible install tabs and a complete ten-preview interaction gallery
- Project Caro contribution provenance and an HN launch draft
