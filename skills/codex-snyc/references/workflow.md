# Codex-snyc Sync Workflow

## Roles

- `codex-snyc`: transport, preview, merge, manifests, history, and safe copying for split iCloud hubs: Codex writes `Codex-snyc`, Minis writes `Minis-snyc`.
- `neat-freak`: content cleanup, memory consolidation, docs/index repair, stale fact removal.
- GitHub skill repo: public distribution of reusable skills only; this is separate from trusted local private sync.

## Split Hub Policy

- Codex/Mac write hub: `/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc/`
- Minis/iPhone write hub: `/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Minis-snyc/`
- Codex may read `Minis-snyc` for reference, but must not write there by default.
- Minis may read `Codex-snyc` for reference, but must not write there by default.
- Cross-hub merge, mirror, delete, or conflict resolution is high-risk and requires explicit user confirmation.

## Recommended Codex-snyc Tree

```text
Codex-snyc/
├── memory/
├── skills/
├── projects/
├── bundles/
├── sync/
│   ├── manifests/
│   └── history.jsonl
└── backups/
```

## Recommended Minis-snyc Tree

```text
Minis-snyc/
├── memory/
├── skills/
├── shared/
├── sync/
│   ├── manifests/
│   └── history.jsonl
└── backups/
```

## Operation Modes

- `preview`: compare source and target; no writes.
- `merge`: copy added and changed files from source to target; keep target-only files.
- `bundle`: pack a domain with a manifest for offline transfer or rollback.
- `mirror`: make target match source, including deletes. Avoid unless explicitly requested.

## Conflict Policy

- Same relative path and same checksum: unchanged.
- Source exists, target missing: added.
- Source and target both exist, checksum differs: modified; copy only in merge mode after preview.
- Target exists, source missing: target-only; do not delete by default.
- Local private sync includes all files by default, including filenames that look sensitive. Do not skip them automatically.
- Same relative path changed independently in both hubs: do not auto-resolve. Treat each hub as its own author's copy and summarize both for the user.

## Public Skill Repo Policy

When publishing skills to GitHub:

- Include local reusable skills from `/Users/zhuyuhua/.codex/skills` and `/Users/zhuyuhua/.cc-switch/skills`.
- Exclude system/bundled skills unless the user explicitly asks to vendor them.
- Run a public-audit before pushing. Public publishing is the one place to review credentials, private keys, subscription URLs, generated caches, logs, and local state.
- Include a top-level README explaining that the repo stores skills, not private memory.
- Keep private sync paths in instructions only when they are operational handles and not secrets.

## neuDrive Ideas Worth Borrowing

- Treat sync as a tree with manifests rather than ad-hoc copying.
- Make preview/diff the default step before writes.
- Prefer merge over mirror.
- Keep history and checksums for repeatability.
- Separate transport from content cleanup.
