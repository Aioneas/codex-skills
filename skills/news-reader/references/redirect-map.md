# Redirect Map

This reference summarizes the four reviewed Tampermonkey scripts and the two local Surge modules. Use it for rule maintenance and for choosing the right access route after the user has confirmed authorized access.

## Reviewed Sources

- `all_redirect_enhanced2.user.js`: base `https://best.viatl.de`, broad news-site redirect, auto/manual/disabled modes.
- `all_redirect_enhanced.user.js`: base `https://best.998888.best`, same broad news-site redirect, improved NYT date-path filter.
- `reader2.user.js`: layout-only adjustment for `reader2.998888.best`, `reader2.viatl.de`, and `2reader2.998888.best`.
- `caixingetfullarticle.user.js`: manual button routes for 财新, DeepView, Entities, 三联生活周刊, 混沌, 三联中读/樊登读书.
- Local Surge modules:
  - `news.redirect.aioneas.sgmodule`: general news routes to `best.viatl.de`.
  - `news.redirect.caixin.sgmodule`: 财新周边 routes to the `998888.best` family.

## General News Routes

| Source URL pattern | Reader route |
|---|---|
| `*.caixin.com/.../<9-digit>.html` | `https://best.viatl.de/cx/<id>` |
| `*.caixin.com/.../<7+ digit>.html` | `https://best.998888.best/cx/<id>` |
| `ftchinese.com/story/<id>` or `ftchinese.com/interactive/<id>` | `<base>/ft/<id>` |
| `www.ft.com/content/<uuid>` | `<base>/fte/<uuid>` |
| `www.wsj.com/...-<8-hex>` or `cn.wsj.com/...-<8-hex>` | `<base>/wsj/<full-original-url>` |
| `www.bloomberg.com/.../articles/...` | `<base>/bb/<full-original-url>` |
| `www.bloomberg.com/.../features/...` | `<base>/bb/<full-original-url>` |
| `www.bloomberg.com/.../newsletters/...` | `<base>/bb/<full-original-url>` |
| `www.economist.com/.../YYYY/MM/DD/...` | `<base>/te/<full-original-url>` |
| `www.nytimes.com/YYYY/MM/DD/...` | `<base>/nyt/<full-original-url>` |
| `theinitium.com/YYYYMMDD-...` or subdomain equivalent | `<base>/duan/<full-original-url>` |

`<base>` is either `https://best.viatl.de` or `https://best.998888.best` when that route family is enabled.

## Caixin Adjacent Routes

| Source URL pattern | Reader route |
|---|---|
| `deepview.caixin.com/topic/<id>.html` | `https://cxv.998888.best/topic/<id>` |
| `deepview.caixin.com/event/<id>.html` | `https://cxv.998888.best/event/<id>` |
| `entities.caixin.com/persons/index?id=<id>` | `https://cxd.998888.best/person/<id>` |
| `entities.caixin.com/companies/index?id=<id>` | `https://cxd.998888.best/company/<id>` |
| `www.lifeweek.com.cn/article/<id>` | `https://best.998888.best/lw/<id>` |
| `www.hundun.cn/course/intro/<id>` | `https://hd.998888.best/course/<id>` |
| `www.dushu365.com/book/<id>` | `https://fs.998888.best/book/<id>` |
| `www.dushu365.com/course/<id>` | `https://fs.998888.best/course/<id>` |

## Implementation Notes

- The `all_redirect` scripts support `auto`, `manual`, and `disabled` modes where Tampermonkey storage is available. In Via/Safari-compatible mode, they default to automatic redirects.
- The `best.viatl.de` userscript used a broad NYT condition; the local Surge module already uses the safer date-path pattern from the newer script.
- The `reader2` script only moves the reader header controls and removes the small title span. It should not be represented as a content-access route.
- When both local Surge modules are enabled, 财新 main articles can match both modules. The effective target depends on Surge's module/rule ordering, so avoid assuming which mirror wins unless you inspect the active profile.
- Safer Surge regexes should anchor full article URL patterns, preserve optional query handling deliberately, and capture query IDs with `[^&#]+` instead of `.+`.
