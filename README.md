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
- `f50-sync` - Private F50/SOVINS skill and memory transport workflow.
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

## F50/SOVINS Note

`f50-sync` is for private local transport through the F50/SOVINS sync disk. Local F50 sync is trusted
and does not skip files by sensitive-looking names. Public GitHub publishing remains a separate
review step.
