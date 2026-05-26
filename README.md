# Codex Skills

Personal public skill repository for Codex / CC Switch compatible skills.

This repository stores reusable skills only. Private memories, runtime tokens, private keys,
subscription URLs, local databases, and machine-specific state do not belong here.

Some copied skills are normalized in this repository so their `SKILL.md` frontmatter passes the
current Codex validator.

## Skills

See [`SKILL_INDEX.md`](./SKILL_INDEX.md) for risk tiers and review notes.

- `doubao-tts` - Doubao / Volcengine text-to-speech workflow.
- `exa-search` - Exa web search workflow.
- `codex-snyc` - Private split iCloud skill and memory transport workflow: Codex writes `Codex-snyc`, Minis writes `Minis-snyc`.
- `neat-freak` - Knowledge cleanup and memory/docs reconciliation workflow.
- `news-reader` - Authorized news article reading, extraction, and summary workflow.
- `pdf` - PDF reading, rendering, extraction, and generation workflow.
- `playwright` - Browser automation via Playwright.
- `qiaomu-music-player-spotify` - Spotify playback plus music genre database.
- `rpi-workflow` - Research-plan-implement workflow helper.
- `skill-vetter` - Security-first skill review workflow.
- `surge` - Surge CLI operations and troubleshooting.
- `web-search` - Browser-based web search workflow.

## Validate

Run the repository validator before publishing changes:

```bash
./scripts/validate-skills.sh
```

It checks each skill for a `SKILL.md`, required frontmatter, directory/name consistency, and obvious secret-looking material.

## Install

Clone the repository, then install skills into the local Codex skills directory:

```bash
git clone https://github.com/Aioneas/codex-skills.git
cd codex-skills
./scripts/install-to-codex.sh
```

The installer uses merge semantics: it copies skills into `${CODEX_HOME:-$HOME/.codex}/skills`
without deleting unrelated local skills.

If you prefer to install a single skill from the repository, use the repo/path form supported by
`skill-installer` and point it at `skills/<skill-name>`.

## Codex-snyc Note

`codex-snyc` is for private local transport through split iCloud hubs. Codex writes `Codex-snyc`;
Minis writes `Minis-snyc`; each treats the other hub as read-only reference by default. Local
private sync is trusted and does not skip files by sensitive-looking names. F50/SOVINS can still be
used as a fallback or archive target. Public GitHub publishing remains a separate review step.
