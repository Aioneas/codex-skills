#!/usr/bin/env python3
"""
browser_search.py - 固定搜索优先级与自动降级策略配置脚本
说明：该脚本当前负责输出搜索计划与降级链路，不直接调用 browser_use。
后续可由 Agent 按本脚本生成的计划执行浏览器自动化。
"""

import argparse
import json
import urllib.parse
from typing import Dict, List

SOURCES: Dict[str, Dict] = {
    "google": {
        "name": "Google",
        "url": "https://www.google.com/search?q={query}",
        "priority": "P1",
        "needs_login": False,
        "quality": "wide",
    },
    "perplexity": {
        "name": "Perplexity",
        "url": "https://www.perplexity.ai/search?q={query}",
        "priority": "P2",
        "needs_login": True,
        "quality": "high",
    },
    "bing": {
        "name": "Bing",
        "url": "https://www.bing.com/search?q={query}",
        "priority": "P3",
        "needs_login": False,
        "quality": "good",
    },
}

FALLBACK_CHAIN: List[str] = ["google", "perplexity", "bing"]

BLOCK_SIGNS = [
    "captcha", "验证", "异常流量", "robot", "blocked", "请稍候", "访问受限"
]


def build_url(source: str, query: str) -> str:
    encoded = urllib.parse.quote(query)
    return SOURCES[source]["url"].format(query=encoded)


def choose_chain() -> List[str]:
    return FALLBACK_CHAIN


def make_plan(query: str) -> Dict:
    chain = choose_chain()
    steps = []
    for idx, source in enumerate(chain, start=1):
        steps.append({
            "order": idx,
            "source": source,
            "name": SOURCES[source]["name"],
            "url": build_url(source, query),
            "needs_login": SOURCES[source]["needs_login"],
            "priority": SOURCES[source]["priority"],
        })
    return {
        "query": query,
        "fallback_chain": chain,
        "block_signs": BLOCK_SIGNS,
        "steps": steps,
        "success_rule": [
            "结果页非首页",
            "文本非空且包含结果内容",
            "存在结构化答案/链接列表/引用来源中的任意一种",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="固定搜索优先级计划生成器")
    parser.add_argument("query", nargs="?", help="搜索查询")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有搜索源")
    parser.add_argument("-j", "--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if args.list:
        print("可用搜索源：")
        for key, val in SOURCES.items():
            print(f"- {key}: {val['name']} ({val['priority']})")
        return

    if not args.query:
        parser.print_help()
        return

    plan = make_plan(args.query)
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"查询: {plan['query']}")
        print("固定降级链路:")
        for step in plan["steps"]:
            login = "需登录" if step["needs_login"] else "免登录"
            print(f"  {step['order']}. {step['name']} [{step['priority']}] - {login}")
            print(f"     {step['url']}")
        print("\n遇到以下情况自动切换下一级:")
        for sign in plan["block_signs"]:
            print(f"- {sign}")

if __name__ == "__main__":
    main()
