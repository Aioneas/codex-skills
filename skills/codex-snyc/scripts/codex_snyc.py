#!/usr/bin/env python3
"""Small helper for Codex-snyc/iCloud skill and memory sync workflows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULTS = {
    "codex_skills": "/Users/zhuyuhua/.codex/skills",
    "cc_switch_skills": "/Users/zhuyuhua/.cc-switch/skills",
    "codex_memories": "/Users/zhuyuhua/.codex/memories",
    "minis_mirror": "/Users/zhuyuhua/Library/Group Containers/group.com.openminis.app/MinisFileProvider",
    "icloud_drive": "/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs",
    "codex_sync_root": "/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc",
    "codex_sync_skills": "/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc/skills",
    "codex_sync_memory": "/Users/zhuyuhua/Library/Mobile Documents/com~apple~CloudDocs/Codex-snyc/memory",
    "f50_adb_endpoint": "192.168.0.1:5555",
    "f50_adb_root": "/data/SAMBA_SHARE/机内存储/Minis同步盘",
    "f50_smb_hint": "smb://192.168.0.1/F50/Minis/",
}

HUB_DIRS = (
    "memory",
    "skills",
    "projects",
    "bundles",
    "sync/manifests",
    "backups",
)

SKIP_DIRS = {".git", "node_modules", "__pycache__"}
SKIP_FILES = {".DS_Store"}
PUBLIC_RISK_PARTS = (
    "auth.json",
    "subscription-url",
    "id_rsa",
    "id_ed25519",
    ".pem",
    ".p12",
    ".key",
    "token",
    "secret",
    "password",
    "passwd",
)


def write_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def run(cmd: list[str], timeout: int = 8) -> dict[str, object]:
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except FileNotFoundError:
        return {"ok": False, "returncode": 127, "stdout": "", "stderr": f"{cmd[0]} not found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": 124, "stdout": "", "stderr": "timeout"}


def is_public_risk(path: Path) -> bool:
    lowered = str(path).lower()
    return any(part in lowered for part in PUBLIC_RISK_PARTS)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_manifest(root: Path) -> dict[str, dict[str, object]]:
    files: dict[str, dict[str, object]] = {}
    root = root.expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"root does not exist: {root}")
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(current)
        for name in names:
            if name in SKIP_FILES:
                continue
            path = base / name
            rel = path.relative_to(root).as_posix()
            if not path.is_file():
                continue
            stat = path.stat()
            files[rel] = {
                "sha256": file_hash(path),
                "size": stat.st_size,
                "mtime": int(stat.st_mtime),
            }
    return files


def compare(source: Path, target: Path) -> dict[str, object]:
    source_manifest = walk_manifest(source)
    target_manifest = walk_manifest(target) if target.exists() else {}
    added: list[str] = []
    modified: list[str] = []
    unchanged: list[str] = []
    target_only: list[str] = []
    for rel, src_meta in sorted(source_manifest.items()):
        dst_meta = target_manifest.get(rel)
        if dst_meta is None:
            added.append(rel)
        elif dst_meta["sha256"] != src_meta["sha256"]:
            modified.append(rel)
        else:
            unchanged.append(rel)
    for rel in sorted(set(target_manifest) - set(source_manifest)):
        target_only.append(rel)
    return {
        "source": str(source.expanduser().resolve()),
        "target": str(target.expanduser().resolve()),
        "counts": {
            "added": len(added),
            "modified": len(modified),
            "unchanged": len(unchanged),
            "target_only": len(target_only),
        },
        "added": added,
        "modified": modified,
        "target_only": target_only,
    }


def cmd_status(_: argparse.Namespace) -> None:
    adb = run(["adb", "devices", "-l"], timeout=5)
    adb_root = run(
        ["adb", "shell", "test", "-d", DEFAULTS["f50_adb_root"], "&&", "echo", "ok"],
        timeout=5,
    )
    data = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "defaults": DEFAULTS,
        "local_paths": {
            key: Path(path).expanduser().exists()
            for key, path in DEFAULTS.items()
            if key not in {"f50_adb_endpoint", "f50_smb_hint"}
        },
        "primary_hub": DEFAULTS["codex_sync_root"],
        "adb_devices": adb,
        "adb_f50_root_exists": adb_root,
        "mounted_volumes": [p.name for p in Path("/Volumes").iterdir()] if Path("/Volumes").exists() else [],
    }
    write_json(data)


def cmd_init_hub(args: argparse.Namespace) -> None:
    root = Path(args.root or DEFAULTS["codex_sync_root"]).expanduser().resolve()
    created: list[str] = []
    existing: list[str] = []
    for rel in HUB_DIRS:
        path = root / rel
        if path.exists():
            existing.append(rel)
            continue
        if args.apply:
            path.mkdir(parents=True, exist_ok=True)
        created.append(rel)
    write_json(
        {
            "root": str(root),
            "mode": "apply" if args.apply else "dry-run",
            "created": created,
            "existing": existing,
        }
    )


def cmd_scan(args: argparse.Namespace) -> None:
    files = walk_manifest(Path(args.root))
    write_json(
        {
            "root": str(Path(args.root).expanduser().resolve()),
            "counts": {"files": len(files)},
            "files": files,
        }
    )


def cmd_preview(args: argparse.Namespace) -> None:
    write_json(compare(Path(args.source), Path(args.target)))


def cmd_merge_copy(args: argparse.Namespace) -> None:
    source = Path(args.source).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()
    history_root = Path(args.history_root).expanduser().resolve() if args.history_root else target
    plan = compare(source, target)
    copied: list[str] = []
    for rel in plan["added"] + plan["modified"]:
        src = source / rel
        dst = target / rel
        if args.apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        copied.append(rel)
    plan["mode"] = "apply" if args.apply else "dry-run"
    plan["copied" if args.apply else "would_copy"] = copied
    if args.apply:
        history_dir = history_root / "sync"
        history_dir.mkdir(parents=True, exist_ok=True)
        with (history_dir / "history.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(), "plan": plan}, ensure_ascii=False) + "\n")
    write_json(plan)


def cmd_public_audit(args: argparse.Namespace) -> None:
    root = Path(args.root).expanduser().resolve()
    risky: list[str] = []
    if not root.exists():
        raise SystemExit(f"root does not exist: {root}")
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(current)
        for name in names:
            path = base / name
            if path.is_file() and is_public_risk(path):
                risky.append(path.relative_to(root).as_posix())
    write_json({"root": str(root), "counts": {"public_risk_files": len(risky)}, "public_risk_files": sorted(risky)})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex-snyc/iCloud sync helper")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Check local paths, iCloud hub, and F50 fallback availability")
    status.set_defaults(func=cmd_status)

    init_hub = sub.add_parser("init-hub", help="Create the Codex-snyc hub directory tree; dry-run unless --apply is passed")
    init_hub.add_argument("--root")
    init_hub.add_argument("--apply", action="store_true")
    init_hub.set_defaults(func=cmd_init_hub)

    scan = sub.add_parser("scan", help="Create a checksum manifest for a directory")
    scan.add_argument("--root", required=True)
    scan.set_defaults(func=cmd_scan)

    preview = sub.add_parser("preview", help="Compare source and target directories")
    preview.add_argument("--source", required=True)
    preview.add_argument("--target", required=True)
    preview.set_defaults(func=cmd_preview)

    merge = sub.add_parser("merge-copy", help="Merge-copy added/modified files; dry-run unless --apply is passed")
    merge.add_argument("--source", required=True)
    merge.add_argument("--target", required=True)
    merge.add_argument("--history-root", help="Write sync/history.jsonl under this hub root instead of the target directory")
    merge.add_argument("--apply", action="store_true")
    merge.set_defaults(func=cmd_merge_copy)

    audit = sub.add_parser("public-audit", help="List files that deserve manual review before public GitHub publishing")
    audit.add_argument("--root", required=True)
    audit.set_defaults(func=cmd_public_audit)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
