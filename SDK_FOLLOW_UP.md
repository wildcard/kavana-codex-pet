# Codex Pet Web SDK — Next-Agent Handoff

## Mission

Extract the proven Kavana companion from [Caro PR #1324](https://github.com/wildcard/caro/pull/1324) into a small, framework-neutral SDK that can place any valid Codex pet on any website. Ship it with a hosted agent skill and a lean prompt so Codex or another development agent can perform the integration without copying Kavana-specific code.

Kavana is the reference implementation and first compatibility fixture. Do not change her artwork or her Codex package format to make the SDK easier.

## Product contract

A site owner should need only:

1. a Codex `pet.json` and `spritesheet.webp`;
2. one SDK installation or generated Web Component bundle;
3. a short behavior configuration;
4. the hosted skill plus the prompt at the end of this document when delegating the work to an agent.

The result must preserve the host site's visual system and expose the pet as an accessible companion—not a pasted Caro widget.

## Architecture

Create a dedicated public repository, provisionally `wildcard/codex-pet-web`, with these workspaces:

```text
packages/
  core/             # atlas parsing, state machine, scheduling, persistence
  web-component/    # <codex-pet-companion>; framework-neutral default
  react/            # thin optional adapter over core
  cli/              # project detection, asset copy, config scaffold, validation
skills/
  codex-pet-web/
    SKILL.md
    scripts/        # deterministic pet/site validation and smoke test helpers
    references/     # framework notes loaded only when needed
examples/
  vanilla/
  react/
fixtures/
  kavana/           # public two-file runtime package or pinned test fixture
```

The core must not import React, Astro, Caro components, or Kavana-specific copy. The Web Component is the default public surface because it works in static HTML and modern frameworks; adapters should only translate lifecycle and properties.

### Runtime configuration

Support a compact configuration object with:

- pet manifest URL and atlas URL;
- atlas cell geometry and Codex sprite version, inferred from `pet.json` where possible;
- state-to-row/frame timing map with safe v1 and v2 defaults;
- enabled behaviors: idle, wave, jump, roam, look, work/review, rest/sleep, drag, tuck/recall;
- dialogue/topics supplied by the host;
- persistence key and default placement;
- theme tokens through CSS custom properties;
- reduced-motion behavior and optional autoplay.

Reject incompatible or malformed assets with a useful validation error. Never silently display a wrong atlas row.

## Hosted skill

Keep `skills/codex-pet-web/SKILL.md` concise and imperative. Its frontmatter description must trigger when a user asks to add, embed, install, or migrate a Codex pet on a website. The core workflow should be:

1. Inspect the host framework, build tool, styling conventions, and existing accessibility rules.
2. Locate or request the pet's two runtime files and validate them with the bundled script.
3. Select Web Component by default; select React only when it materially fits the host.
4. Install the SDK and scaffold a local configuration without rewriting the site's design system.
5. Configure behavior, touch controls, keyboard access, focus handling, persistence, and reduced motion.
6. Run unit, build, and browser smoke tests at desktop and coarse-pointer mobile sizes.
7. Report the integration files, verification evidence, and any deliberately disabled behaviors.

Put framework-specific commands in one-level `references/` files. Put repeatable validation and scaffold operations in scripts rather than expanding `SKILL.md`. Do not add extra README or quick-reference files inside the skill package.

Publish the repository in a form compatible with the skills.sh repository installer and make this command work from a clean project:

```bash
npx skills add wildcard/codex-pet-web --skill codex-pet-web
```

## Lean agent prompt

Host this prompt next to the skill's public install link:

> Use the `codex-pet-web` skill to add this Codex pet to the current website. Preserve the site's design system, use the pet's real manifest and transparent atlas, enable accessible touch/keyboard/reduced-motion behavior, and verify the result on desktop and mobile. Show me the live integration and the checks you ran.

The skill—not the prompt—must carry the implementation procedure.

## Delivery sequence

1. Extract the atlas state engine from Kavana's standalone field guide and the interaction model from Caro without copying product-specific text.
2. Define and validate the public configuration schema against Kavana and at least one additional Codex v1 or v2 pet.
3. Ship the Web Component and vanilla example.
4. Ship the React adapter and migrate Caro's Kavana companion onto it without behavior regressions.
5. Ship the CLI validators/scaffold and the hosted skill.
6. Run the skill from a clean agent task against both examples; revise any instruction the agent must guess.
7. Publish packages, docs, demo, and a migration note linking back to Kavana and Caro.

## Acceptance gates

- No Kavana, Caro, Astro, or React dependency in `packages/core`.
- A valid Codex two-file pet can be embedded without editing SDK source.
- Transparent atlas playback has no opaque video fallback or black background.
- Keyboard, touch/coarse-pointer, drag, tuck/recall focus, and reduced-motion flows pass browser tests.
- The pet remains usable under a strict Content Security Policy and without third-party runtime requests.
- Core plus default renderer has an explicit, measured bundle budget set before release.
- The Caro migration matches the current companion's roam, dialogue, sleep, placement, persistence, and minimize behavior.
- Automated tests cover v1/v2 geometry, invalid manifests, timers, cleanup, persistence, and focus restoration.
- The skill succeeds from the lean prompt in vanilla and React projects without undocumented manual repair.
- Public docs preserve asset provenance, license boundaries, and the distinction between community pets and official Codex/OpenAI assets.

## Non-goals for v1

- Reading private Codex desktop state or relying on undocumented local APIs.
- Generating pet artwork; that remains the `hatch-pet` skill's responsibility.
- A visual no-code editor, marketplace, analytics, or hosted backend.
- Framework-specific replicas of the core engine.

## Completion evidence

The next agent should close the task only with links to the SDK repository, published package(s), hosted skill, live examples, Caro migration PR, and green automated/browser checks. A design-only scaffold is not completion.
