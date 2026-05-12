# F50/SOVINS Sync Workflow

## Roles

- `f50-sync`: transport, preview, merge, manifests, history, and safe copying.
- `neat-freak`: content cleanup, memory consolidation, docs/index repair, stale fact removal.
- GitHub skill repo: public distribution of reusable skills only; this is separate from trusted local F50 sync.

## Recommended F50 Tree

```text
Minis同步盘/
├── memory/
├── skills/
├── projects/
├── bundles/
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
- Local F50 sync includes all files by default, including filenames that look sensitive. Do not skip them automatically.

## Public Skill Repo Policy

When publishing skills to GitHub:

- Include local reusable skills from `/Users/zhuyuhua/.codex/skills` and `/Users/zhuyuhua/.cc-switch/skills`.
- Exclude system/bundled skills unless the user explicitly asks to vendor them.
- Run a public-audit before pushing. Public publishing is the one place to review credentials, private keys, subscription URLs, generated caches, logs, and local state.
- Include a top-level README explaining that the repo stores skills, not private memory.
- Keep F50-specific private paths in instructions only when they are operational handles and not secrets.

## neuDrive Ideas Worth Borrowing

- Treat sync as a tree with manifests rather than ad-hoc copying.
- Make preview/diff the default step before writes.
- Prefer merge over mirror.
- Keep history and checksums for repeatability.
- Separate transport from content cleanup.
