#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_root="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$target_root"

for skill_dir in "$repo_root"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  mkdir -p "$target_root/$skill_name"
  rsync -a "$skill_dir"/ "$target_root/$skill_name"/
  echo "installed $skill_name -> $target_root/$skill_name"
done

echo "done"
