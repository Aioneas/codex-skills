#!/usr/bin/env python3
"""Generate authorized reader-route candidates for known news URLs.

This script does not fetch, authenticate, or bypass access controls. It only
maps a source URL to candidate reader URLs reflected by the user's configured
Tampermonkey/Surge rules.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Iterable
from urllib.parse import parse_qs, urlparse


BASES = {
    "viatl": "https://best.viatl.de",
    "998888": "https://best.998888.best",
}


@dataclass(frozen=True)
class Candidate:
    source_url: str
    site: str
    route_family: str
    candidate_url: str
    note: str


def clean_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        parsed = urlparse("https://" + url.strip())
    return parsed.geturl()


def host_matches(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def wanted_bases(choice: str) -> list[str]:
    if choice == "both":
        return ["viatl", "998888"]
    return [choice]


def add_base_candidates(
    out: list[Candidate],
    source_url: str,
    site: str,
    route_path: str,
    base_choice: str,
    note: str,
    allowed: Iterable[str] = ("viatl", "998888"),
) -> None:
    allowed_set = set(allowed)
    for key in wanted_bases(base_choice):
        if key in allowed_set:
            out.append(
                Candidate(
                    source_url=source_url,
                    site=site,
                    route_family=key,
                    candidate_url=BASES[key] + route_path,
                    note=note,
                )
            )


def candidates_for(url: str, base_choice: str) -> list[Candidate]:
    source_url = clean_url(url)
    parsed = urlparse(source_url)
    host = parsed.hostname or ""
    path = parsed.path or "/"
    query = parse_qs(parsed.query, keep_blank_values=True)
    out: list[Candidate] = []

    if host_matches(host, "caixin.com") and host not in {
        "deepview.caixin.com",
        "datanews.caixin.com",
        "entities.caixin.com",
    }:
        match = re.search(r"/(\d{7,})\.html$", path)
        if match:
            article_id = match.group(1)
            allowed = ["998888"]
            if len(article_id) == 9:
                allowed.append("viatl")
            add_base_candidates(
                out,
                source_url,
                "caixin",
                f"/cx/{article_id}",
                base_choice,
                "caixin numeric article id",
                allowed,
            )

    if host_matches(host, "ftchinese.com"):
        match = re.match(r"/(?:story|interactive)/(\d+)", path)
        if not match:
            match = re.search(r"/(\d+)", path)
        if match:
            add_base_candidates(
                out,
                source_url,
                "ftchinese",
                f"/ft/{match.group(1)}",
                base_choice,
                "FT Chinese story or interactive id",
            )

    if host == "www.ft.com":
        match = re.match(r"/content/([^/?#]+)", path)
        if match:
            add_base_candidates(
                out,
                source_url,
                "financial-times",
                f"/fte/{match.group(1)}",
                base_choice,
                "FT content uuid",
            )

    if host in {"www.wsj.com", "cn.wsj.com"}:
        last = path.rstrip("/").split("/")[-1]
        if re.search(r"-[A-Fa-f0-9]{8}$", last):
            add_base_candidates(
                out,
                source_url,
                "wsj",
                f"/wsj/{source_url}",
                base_choice,
                "WSJ slug ending with 8 hex chars",
            )

    if host == "www.bloomberg.com" and re.search(
        r"/(?:[^/?#]+/)?(?:articles|features|newsletters)/[^/?#]+", path
    ):
        add_base_candidates(
            out,
            source_url,
            "bloomberg",
            f"/bb/{source_url}",
            base_choice,
            "Bloomberg article, feature, or newsletter path",
        )

    if host == "www.economist.com" and re.search(r"/\d{4}/\d{2}/\d{2}/", path):
        add_base_candidates(
            out,
            source_url,
            "economist",
            f"/te/{source_url}",
            base_choice,
            "Economist dated article path",
        )

    if host == "www.nytimes.com" and re.match(r"/\d{4}/\d{2}/\d{2}/", path):
        add_base_candidates(
            out,
            source_url,
            "nytimes",
            f"/nyt/{source_url}",
            base_choice,
            "NYT dated article path",
        )

    if host_matches(host, "theinitium.com") and re.match(r"/\d{8}-", path):
        add_base_candidates(
            out,
            source_url,
            "theinitium",
            f"/duan/{source_url}",
            base_choice,
            "Initium dated article path",
        )

    if host == "deepview.caixin.com":
        match = re.match(r"/(topic|event)/(.+?)\.html$", path)
        if match:
            out.append(
                Candidate(
                    source_url=source_url,
                    site=f"caixin-deepview-{match.group(1)}",
                    route_family="998888-adjacent",
                    candidate_url=f"https://cxv.998888.best/{match.group(1)}/{match.group(2)}",
                    note="DeepView topic or event",
                )
            )

    if host == "entities.caixin.com" and path in {
        "/persons/index",
        "/companies/index",
    }:
        entity_id = (query.get("id") or [""])[0]
        if entity_id:
            kind = "person" if "persons" in path else "company"
            out.append(
                Candidate(
                    source_url=source_url,
                    site=f"caixin-entities-{kind}",
                    route_family="998888-adjacent",
                    candidate_url=f"https://cxd.998888.best/{kind}/{entity_id}",
                    note="Caixin entity id query parameter",
                )
            )

    if host == "www.lifeweek.com.cn":
        match = re.match(r"/article/(\d+)", path)
        if match:
            out.append(
                Candidate(
                    source_url=source_url,
                    site="lifeweek",
                    route_family="998888-adjacent",
                    candidate_url=f"https://best.998888.best/lw/{match.group(1)}",
                    note="Lifeweek article id",
                )
            )

    if host == "www.hundun.cn":
        match = re.match(r"/course/intro/([^/?#]+)", path)
        if match:
            out.append(
                Candidate(
                    source_url=source_url,
                    site="hundun",
                    route_family="998888-adjacent",
                    candidate_url=f"https://hd.998888.best/course/{match.group(1)}",
                    note="Hundun course intro id",
                )
            )

    if host == "www.dushu365.com":
        match = re.match(r"/(book|course)/(\d+)", path)
        if match:
            route = "book" if match.group(1) == "book" else "course"
            out.append(
                Candidate(
                    source_url=source_url,
                    site=f"dushu365-{route}",
                    route_family="998888-adjacent",
                    candidate_url=f"https://fs.998888.best/{route}/{match.group(2)}",
                    note="Dushu365 book or course id",
                )
            )

    return out


def print_table(candidates: list[Candidate]) -> None:
    if not candidates:
        print("No known reader-route candidates.")
        return
    for item in candidates:
        print(f"{item.site}\t{item.route_family}\t{item.candidate_url}\t{item.note}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate candidate reader URLs for known authorized news routes."
    )
    parser.add_argument("urls", nargs="+", help="Source article URL(s)")
    parser.add_argument(
        "--base",
        choices=["viatl", "998888", "both"],
        default="both",
        help="General news route family to emit",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    all_candidates: list[Candidate] = []
    for url in args.urls:
        all_candidates.extend(candidates_for(url, args.base))

    if args.json:
        print(json.dumps([asdict(item) for item in all_candidates], ensure_ascii=False, indent=2))
    else:
        print_table(all_candidates)

    return 0 if all_candidates else 2


if __name__ == "__main__":
    raise SystemExit(main())
