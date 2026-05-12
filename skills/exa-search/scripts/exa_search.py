#!/usr/bin/env python3
import argparse
import json
import os
import sys
import textwrap
from typing import Any, Dict

import requests

EXA_ENDPOINT = "https://api.exa.ai/search"


def eprint(*a):
    print(*a, file=sys.stderr)


def request_exa(payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    r = requests.post(EXA_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=60)
    if r.status_code >= 400:
        # Avoid dumping headers; they may include auth metadata.
        raise RuntimeError(f"Exa API error {r.status_code}: {r.text[:800]}")
    return r.json()


def main():
    ap = argparse.ArgumentParser(description="Search the web via Exa API")
    ap.add_argument("--query", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--type", default="auto", choices=["auto", "neural", "keyword"])
    ap.add_argument("--recent", type=int, default=0, help="Recency in days (0=off).")
    ap.add_argument("--language", default="", help="Optional language hint (e.g. en, zh).")
    ap.add_argument("--json", action="store_true", help="Print raw JSON.")
    args = ap.parse_args()

    api_key = os.environ.get("EXA_API_KEY", "")
    if not api_key:
        eprint("Missing EXA_API_KEY env var.")
        eprint("Set it in Minis: Settings -> Environment Variables.")
        sys.exit(2)

    payload: Dict[str, Any] = {
        "query": args.query,
        "numResults": max(1, min(args.k, 25)),
        "type": args.type,
    }
    if args.recent and args.recent > 0:
        # Exa expects ISO 8601 date string.
        from datetime import datetime, timedelta, timezone
        dt = datetime.now(timezone.utc) - timedelta(days=args.recent)
        payload["startPublishedDate"] = dt.isoformat().replace("+00:00", "Z")
    if args.language:
        payload["language"] = args.language

    data = request_exa(payload, api_key)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    results = data.get("results", []) or []
    for i, it in enumerate(results, 1):
        title = (it.get("title") or "").strip() or "(no title)"
        url = (it.get("url") or "").strip()
        score = it.get("score", None)
        published = it.get("publishedDate", "") or ""
        snippet = (it.get("text") or it.get("snippet") or "").strip()
        snippet = " ".join(snippet.split())

        meta = []
        if published:
            meta.append(published)
        if score is not None:
            try:
                meta.append(f"score={float(score):.3f}")
            except Exception:
                meta.append(f"score={score}")

        meta_s = (" (" + ", ".join(meta) + ")") if meta else ""
        print(f"{i}. {title}{meta_s}\n   {url}")
        if snippet:
            print(textwrap.fill(snippet, width=100, subsequent_indent="   ", initial_indent="   "))
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as ex:
        eprint(str(ex))
        sys.exit(1)
