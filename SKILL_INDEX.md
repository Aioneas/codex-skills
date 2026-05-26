# Skill Index

This repository stores reusable public skills for Codex / CC Switch compatible environments.

Private memories, runtime tokens, API keys, subscription URLs, local databases, and machine-specific state do not belong here.

## Risk tiers

Risk is based on the kind of access a skill normally needs, not on whether the skill is useful.

### Low risk

| Skill | Purpose | Notes |
|---|---|---|
| `pdf` | PDF reading, rendering, extraction, and generation | Review generated artifacts before sharing. |
| `news-reader` | Authorized article extraction and summaries | Use only for content the user is allowed to access. |
| `neat-freak` | Knowledge cleanup and docs reconciliation | Keep private memories out of public commits. |

### Medium risk

| Skill | Purpose | Notes |
|---|---|---|
| `web-search` | Browser-based web search workflow | Network access required. |
| `exa-search` | Exa web search workflow | API/network access required. |
| `doubao-tts` | Doubao / Volcengine TTS workflow | May require service credentials in the local environment. |
| `playwright` | Browser automation | Can interact with logged-in browser sessions; review scope before use. |
| `qiaomu-music-player-spotify` | Spotify playback and music metadata | May touch local playback/session state. |

### High risk / review before use

| Skill | Purpose | Notes |
|---|---|---|
| `surge` | Surge CLI operations and troubleshooting | Can mutate live network routing state. Collect baseline before changes. |
| `rpi-workflow` | Research-plan-implement workflow helper | May run broad file/code operations depending on task. |
| `codex-snyc` | Split Codex-snyc / Minis-snyc iCloud sync workflow | Codex writes Codex-snyc; Minis writes Minis-snyc. Treat the other hub as read-only reference unless explicitly repairing it. |
| `skill-vetter` | Security-first skill review workflow | Used to review other skills; keep its criteria strict. |

## Before installing a skill

1. Read the target `skills/<name>/SKILL.md`.
2. Check for unexpected network calls, credential access, or broad filesystem writes.
3. Run the repository validator:

```bash
./scripts/validate-skills.sh
```

4. Install only the skills you actually need.

## Public publishing rule

A skill may be safe for a private machine and still unsafe for a public repository. Review every commit for secrets, machine-specific paths, private memories, and copied local state before pushing.
