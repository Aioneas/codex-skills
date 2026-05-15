---
name: news-reader
description: >
  Read and summarize authorized news articles, including paywalled sources when the user has already provided a logged-in browser session, article text, or installed reader/redirect access. Trigger for news article reading, paywalled news, 财新, FT中文, Financial Times, WSJ, Bloomberg, Economist, NYT, 端传媒, DeepView, Entities, 三联生活周刊, 混沌, 三联中读, 樊登读书, article extraction, and article summaries. Use only for lawful user-authorized access; do not bypass paywalls or reproduce full articles.
---

# news-reader

Use this skill to read, extract, and summarize news articles through access the user is already authorized to use. This includes logged-in browser sessions, user-provided article text, and user-installed redirect or reader routes.

## Boundaries

- Do not defeat a paywall, scrape around access controls, harvest credentials, or claim anonymous access is authorized.
- If a paywalled page is blocked, ask the user to open it in a logged-in browser, provide the article text, or confirm the already-installed reader route they want used.
- Do not reproduce full copyrighted articles. Summarize, extract facts, build timelines, compare claims, or quote only short excerpts needed for grounding.
- Prefer the original publisher URL for attribution. Treat mirror or reader URLs as access paths, not as public citations.

## Default Workflow

1. Identify the source URL, publisher, and the user's requested output: summary, bullet brief, timeline, entity list, comparison, translation excerpt, or Q&A.
2. Use the authenticated route first when login matters:
   - In Codex on desktop, prefer the user's logged-in Chrome/profile when the task depends on cookies.
   - In Minis or other mobile/browser contexts, ask the user to open the page after login or provide the visible text if the session is not available to the agent.
3. If the user already has Surge/Tampermonkey/reader access configured, open the original URL and observe whether it redirects. Only generate direct reader candidates when the user intended that access path.
4. Extract the article robustly:
   - Wait for client-side rendering and scroll through the page once for lazy-loaded text.
   - Prefer `article`, `main`, JSON-LD, `meta[property="article:*"]`, headline, byline, date, and body paragraphs.
   - Remove nav, ads, comments, related links, cookie banners, and duplicated teaser text.
5. Verify the extraction before answering: headline, source, publish/update date, and enough body text should be present. If only a teaser is visible, say so and request authorized access.
6. Answer in the requested language. For Chinese users, default to concise Chinese unless the article or request clearly calls for English.

## Redirect Helper

Use `scripts/news_redirect.py` when you need deterministic candidate reader URLs instead of hand-writing routing logic:

```bash
python3 scripts/news_redirect.py "https://www.ft.com/content/00000000-0000-0000-0000-000000000000" --base both --json
```

The helper only maps URLs; it does not fetch pages, authenticate, bypass paywalls, or verify that a reader endpoint works.

Read `references/redirect-map.md` when updating route rules, comparing the Tampermonkey userscripts, or checking whether the local Surge modules need changes.

## Output Rules

- Start with the answer, not the extraction method, unless the user asked for diagnostics.
- Include source, date, and access note when relevant, for example: "已通过登录页面读取" or "只看到 teaser".
- For long articles, provide: one-sentence thesis, 5-8 key points, important names/numbers, and unresolved questions.
- For translations, translate selected excerpts or a summarized version unless the user owns/provides the text and asks for a transformation within the current task.
- Keep direct quotes short and necessary.

## Known Route Families

- `best.viatl.de`: 财新, FT中文, FT, WSJ, Bloomberg, Economist, NYT, 端传媒.
- `best.998888.best` family: 财新 and the same global news families, plus DeepView, Entities, 三联生活周刊, 混沌, 三联中读/樊登读书.
- `reader2.*`: reader-page layout adjustment only; it is not an article routing rule.
