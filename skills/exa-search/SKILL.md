---
name: exa-search
description: Use Exa (exa.ai) web search to find and summarize sources with citations. Trigger when the user asks to search the web, look up sources, find articles, get links, verify information with sources, or needs up-to-date information. Requires `EXA_API_KEY`.
---

# Exa Search

Use this skill when the user wants source-backed web results through Exa instead of model memory.

## Requirements

- Environment variable `EXA_API_KEY` must be set.
- Script path:
  `/Users/zhuyuhua/.cc-switch/skills/exa-search/scripts/exa_search.py`

If `EXA_API_KEY` is missing, tell the user it needs to be configured in the local environment. Do not invent a settings deep link for another app runtime.

## Workflow

1. Clarify the query only if the request is genuinely ambiguous.
2. Choose sensible defaults:
   - `--type auto`
   - `--k 5` for normal lookup
   - `--k 10` for broader research
   - `--recent <days>` only when recency matters
   - `--language zh` or `--language en` when language targeting matters
3. Run the script.
4. Return:
   - a short synthesis
   - cited sources with title + URL
   - quotes only when the user explicitly wants them

## Commands

Basic:

```bash
python3 /Users/zhuyuhua/.cc-switch/skills/exa-search/scripts/exa_search.py \
  --query "OpenAI Responses API" \
  --k 5 \
  --type auto
```

Recent news:

```bash
python3 /Users/zhuyuhua/.cc-switch/skills/exa-search/scripts/exa_search.py \
  --query "latest browser engine vulnerabilities" \
  --k 5 \
  --type auto \
  --recent 30
```

Structured parsing:

```bash
python3 /Users/zhuyuhua/.cc-switch/skills/exa-search/scripts/exa_search.py \
  --query "China EV export policy 2026" \
  --k 10 \
  --type auto \
  --language en \
  --json
```

## Output rules

- Never reveal `EXA_API_KEY`.
- If Exa fails, summarize the error briefly and tell the user to verify API key and network access.
- Do not claim information is verified unless the returned sources actually support it.
