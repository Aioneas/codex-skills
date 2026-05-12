---
name: web-search
description: >
  通用网页搜索技能，通过浏览器自动化使用固定搜索引擎链路。
  仅保留：Google、Perplexity、Bing。
  当用户提到"网页搜索"、"搜索一下"、"帮我搜"、"网上查一下"、"搜索引擎"，或需要从互联网获取实时信息时触发。
---

# web-search

Compatibility: browser_use tool required; optional login for Perplexity; no API key required.

Use browser automation to search the web through a fixed engine chain, then fall back automatically when one engine is blocked, logged out, or returns poor results.

## When to use

Activate this skill when the user wants:
- real-time web search
- search engine results instead of model memory
- official site lookup
- original page lookup
- fallback behavior across the fixed search engines

## Search engines

| Engine | URL pattern | Strength | Notes |
|---|---|---|---|
| Google | `https://www.google.com/search?q={query}` | Default first choice | Best general web coverage |
| Perplexity | `https://www.perplexity.ai/search?q={query}` | High answer quality | Needs login once |
| Bing | `https://www.bing.com/search?q={query}` | Stable fallback | Good general coverage |

## Default priority chain

`Google -> Perplexity -> Bing`

## Fallback rules

Immediately switch to the next engine when any of these happens:
- login expired
- captcha / verification / blocked / robot / abnormal traffic
- empty result page
- redirected back to the home page
- page structure is broken and no useful text can be extracted
- only input box is visible with no actual results

## Success criteria

Treat a search as successful when at least two of these are true:
- the page title or URL clearly indicates a result page
- extracted text is non-empty and contains meaningful results
- there are structured answers, result lists, citations, or related questions
- the content is clearly not just the search homepage

## Execution flow

1. Use Google first.
2. If unavailable or poor, switch to Perplexity.
3. If unavailable or poor, switch to Bing.
4. Return the first good result, and optionally add a second source for comparison.

## Scripts

- `scripts/browser_search.py` — generate the fixed priority plan
- `evals/evals.json` — prompt coverage for the routing scenario

## Notes

- Google is the default first engine.
- Perplexity is the second choice when Google is blocked or poor.
- Bing is the final fallback.
- Do not use any other search engine.
