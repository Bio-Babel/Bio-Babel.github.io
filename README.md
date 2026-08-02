# Bio-Babel.github.io

Source of <https://bio-babel.github.io>. Pages serves `main` from the repo root, so a push
is a deploy.

`index.html` is the whole page — static markup, nothing rendered at runtime. `assets/js/main.js`
only adds behaviour: sticky nav, scroll reveals, the stat counters, the stack tier picker, the
library filter. Changing copy means editing `index.html`.

```bash
python3 -m http.server 8000
```

## Constraints

Not preferences — each of these has already caused a bug.

1. **No CDN, no web fonts, no runtime API calls.** Much of the audience is in mainland China,
   where Google Fonts and `api.github.com` are blocked or slow. Hence the system font stack and
   the hand-maintained catalog below. To guarantee Inter, self-host the woff2; do not add a
   `<link>`.
2. **Paths stay relative**, so the site survives a move to a sub-path or a custom domain.
3. **`.nojekyll` stays**, or Pages runs Jekyll over the files.
4. **`og:image` stays a raster at an absolute URL.** Crawlers on X, Facebook, LinkedIn, Slack
   and Discord reject SVG and ignore relative URLs. Break this and every shared link renders
   without an image, silently.
5. **Organization voice.** The libraries and the community lead; the contract layer and its
   benchmark share one section because they are two of the org's repositories, not the point
   of it.
6. **R → Python is the demonstration, not the definition.** Copy may say the problem is
   particular to no pair of languages — that is a claim about the problem. Do not upgrade it
   into a claim that the tooling is already language-agnostic: `manifest_api.py` still carries
   an `r_package` field and the porting skill is still named `r2py-skills`. When that changes,
   the copy can.

## Hard-coded facts

The catalog is a snapshot (constraint 1), so some numbers are hand-maintained. Find all of them:

```bash
grep -niE 'seventeen|17 (r )?(librar|classic)|data-(count|filter)=|read-only tools' index.html
```

That covers the meta and OpenGraph descriptions, the hero pill and paragraph, the stats strip,
the catalog heading and the five filter counts. The cards themselves are one
`<article class="lib">` each. Do not trust line numbers in this file — use the grep, and if you
reword the copy, check the pattern still matches.

| figure | where the truth is |
|---|---|
| library and repo counts | `curl -s 'https://api.github.com/orgs/Bio-Babel/repos?per_page=100'` — everything except `.github`, `Bio-Babel.github.io`, `bio-babel-MCP` and `bio-babel-MCPBench` is a library (`bio-babel-toolkit` and `bio-babel-annotator` are private and do not appear) |
| `1,606` contracted symbols | sum of `symbols/` across each port's `_biobabel/` |
| `12` read-only MCP tools | asserted by `tests/test_mcp_server.py::tool_count` in `bio-babel-MCP` |
| per-card versions | PyPI |
| the argument in the hero and the Why section | `manuscript/Draft_main_text_human.txt` — the copy is drawn from it, so keep the two consistent |

## Logo

```bash
python3 tools/gen_logo.py     # cairosvg is optional, previews only
```

Regenerate rather than hand-editing the SVGs: the geometry is transcribed once in the script and
every file derives from it. Two properties are easy to break —

* **The arches are transparent cut-outs, not white fill.** Whatever sits behind shows through, so
  the mark must never go on a field near its own violet: the arcade disappears and the tower
  flattens into a triangle. On the tile the tower is cream for exactly this reason.
* **The shipped files carry no `<mask>`.** The master artwork (`Bio-Babel/.github`,
  `profile/imgs/bio-babel-logo.svg`) uses one, and non-browser rasterisers silently drop it and
  paint a solid square. Everything here is a single nonzero-winding path instead.

`<text>` in the banner is pinned with `textLength`; the viewer's fallback font is unknown and
without it the tagline overflows the artboard.

| file | use |
|---|---|
| `logo-mark.svg` | the mark, flat `#8477C8`. Nav, hero, footer |
| `logo-mark-mono.svg` | `fill="currentColor"` — inline it to tint from CSS |
| `logo-mark-ghost.svg` | white, for low-opacity watermarks |
| `logo-mark-gradient.svg` | violet→gold; point the `logo-mark.svg` references at this for more lift |
| `logo-tile.svg` | squircle tile — the org avatar and the touch icon |
| `favicon.svg` | tile with a simplified arcade, so it still reads at 16 px |
| `logo-wordmark.svg` | mark + `Bio-Babel` + tagline |
| `logo-banner.svg` | 1080×240 banner, in use in the org profile README |
| `og-card.png` | 1200×630 link preview, rendered from `tools/og-card.html` — command in its header |
