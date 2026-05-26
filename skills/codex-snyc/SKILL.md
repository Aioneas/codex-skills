---
name: codex-snyc
description: Safely plan, preview, merge, and audit Codex/Minis skill and memory movement through split iCloud hubs: Codex writes Codex-snyc, Minis writes Minis-snyc, each reads the other only as reference. Use when the user mentions Codex-snyc, Minis-snyc, iCloud sync, F50, SOVINS, Minis同步盘, 内网同步, memory sync, skill sync, syncing skills or memories between Mac/Codex/Minis/F50, ADB/SMB paths for F50, or asks to borrow neuDrive-style workflows without GitHub/cloud memory sync.
---

# Codex-snyc Sync

## Purpose

Use this skill for transport safety: split iCloud hubs move skills and memories; `neat-freak` cleans and deduplicates content. Keep those roles separate.

The user's preferred architecture is private-first:

- `Codex-snyc` is the Codex/Mac write hub. Codex writes here by default.
- `Minis-snyc` is the Minis/iPhone write hub. Minis writes there; Codex treats it as read-only reference.
- The two agents can read each other's memories for context, but each writes only to its own hub to avoid stomping conflicts.
- F50/SOVINS remains an optional fallback, archive, or Android-side transfer target.
- Local private sync is trusted by default. Do not skip tokens, private keys, certificates, subscriptions, or other sensitive-looking filenames during local private `scan`, `preview`, or `merge-copy`.
- GitHub/GitLab may be used for public skills, but publishing to a public repo is a separate workflow from local private sync.
- Default to `preview` and `merge`; do not mirror or delete unless the user explicitly requests it after seeing a diff.

## Known Paths

- Codex skills: `/Users/zhuyuhua/.codex/skills/`
- CC Switch skills: `/Users/zhuyuhua/.cc-switch/skills/`
- Codex memories: `/Users/zhuyuhua/.codex/memories/`
- Local Minis mirror: `/Users/zhuyuhua/Library/Group Containers/group.com.openminis.app/MinisFileProvider/`
- iCloud Drive: `/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/`
- Codex-snyc root: `/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc/`
- Minis-snyc root: `/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Minis-snyc/`
- F50 SMB hint: `smb://192.168.0.1/F50/Minis/`
- F50 ADB endpoint: `192.168.0.1:5555`
- F50 ADB sync root: `/data/SAMBA_SHARE/机内存储/Minis同步盘/`
- Stale F50 ADB path to avoid: `/data/SAMBA_SHARE/机内存储/Minis/`

## Workflow

1. Identify the task domain: `skills`, `memory`, `projects`, or a narrow subfolder. Narrow domains are safer than whole-disk operations.
2. Check availability with `scripts/codex_snyc.py status`. Prefer the local iCloud Drive path first, mounted volumes second, and ADB only when needed for F50 fallback.
3. Build a source and target manifest. Use `scripts/codex_snyc.py scan --root <path>` for inventory, or `preview --source <src> --target <dst>` for comparisons.
4. Show the user a concise diff before writes: added, modified, unchanged, and target-only.
5. For writes, use merge semantics. Only copy new/changed files from source to target. Do not delete target-only files by default.
6. Codex writes to `Codex-snyc` only. Do not write, merge, mirror, or delete inside `Minis-snyc` unless the user explicitly asks to repair the Minis hub.
7. Write history after successful sync when possible: `sync/history.jsonl` under the writer's hub root with absolute date, source, target, file counts, and summary.
8. If memory content changed, run `neat-freak` after transport to reconcile indexes and remove stale facts.

## Safety Rules

- Never print or copy private key contents. It is okay to record public key fingerprints and file paths.
- Local private sync should include all files by default; the user accepts and controls the local risk.
- Public GitHub skill repos may include reusable skill source only. Use public-audit/review for public publishing, but do not apply those exclusions to local Codex-snyc/F50 sync.
- Treat `Minis-snyc` as read-only from Codex by default. It exists so Codex can reference Minis memory, not so Codex overwrites it.
- Treat `Codex-snyc` as read-only from Minis by default. It exists so Minis can reference Codex memory, not so Minis overwrites it.
- Prefer `merge` over `mirror`. Treat deletion, overwrite-all, and bidirectional conflict resolution as high-risk operations.
- Use absolute dates such as `2026-05-12`; avoid "today" or "recently" in durable notes.

## Helper Script

Use `scripts/codex_snyc.py` for deterministic checks:

```bash
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py status
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py init-hub --hub both --apply
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py scan --root /Users/zhuyuhua/.codex/skills
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py preview --source <source-dir> --target <target-dir>
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py merge-copy --source <source-dir> --target <target-dir> --history-root "/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc" --apply
python3 /Users/zhuyuhua/.codex/skills/codex-snyc/scripts/codex_snyc.py public-audit --root <public-repo-dir>
```

Without `--apply`, `merge-copy` is a dry run.

Read `references/workflow.md` when planning a multi-machine sync, publishing skills to GitHub, or handling conflicts.
