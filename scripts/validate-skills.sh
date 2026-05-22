#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"

if [ ! -d "$skills_root" ]; then
  echo "missing skills directory: $skills_root" >&2
  exit 1
fi

status=0
count=0

for skill_dir in "$skills_root"/*; do
  [ -d "$skill_dir" ] || continue
  count=$((count + 1))
  skill_name="$(basename "$skill_dir")"
  skill_file="$skill_dir/SKILL.md"

  if [ ! -f "$skill_file" ]; then
    echo "missing SKILL.md: $skill_name" >&2
    status=1
    continue
  fi

  if ! grep -q '^---$' "$skill_file"; then
    echo "missing frontmatter fence: $skill_name" >&2
    status=1
  fi

  if ! grep -q '^name:[[:space:]]*' "$skill_file"; then
    echo "missing frontmatter name: $skill_name" >&2
    status=1
  fi

  if ! grep -q '^description:[[:space:]]*' "$skill_file"; then
    echo "missing frontmatter description: $skill_name" >&2
    status=1
  fi

  declared_name="$(awk -F': *' '/^name:[[:space:]]*/ {print $2; exit}' "$skill_file" | tr -d '"' | tr -d "'")"
  if [ -n "$declared_name" ] && [ "$declared_name" != "$skill_name" ]; then
    echo "skill directory/name mismatch: dir=$skill_name frontmatter=$declared_name" >&2
    status=1
  fi

done

if [ "$count" -eq 0 ]; then
  echo "no skills found" >&2
  exit 1
fi

if grep -RInE \
  --exclude-dir=.git \
  --exclude='validate-skills.sh' \
  'BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY|aws_secret_access_key|client_secret|refresh_token|access_token|Authorization: Bearer|PRIVATE KEY' \
  "$repo_root" \
  >/tmp/codex_skills_secret_matches.$$; then
  echo "potential secret material found; review these matches:" >&2
  cat /tmp/codex_skills_secret_matches.$$ >&2
  rm -f /tmp/codex_skills_secret_matches.$$
  exit 1
fi
rm -f /tmp/codex_skills_secret_matches.$$

if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo "OK: validated $count skills"
