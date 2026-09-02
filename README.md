# Bio-Babel.github.io

Source of <https://biobabel.stanford.edu> (the `CNAME`; <https://bio-babel.github.io> redirects
there). Pages serves `main` from the repo root.

## Hard-coded facts

The catalog is a snapshot, so some numbers are hand-maintained. Find all of them:

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
| the UMI-tools-cpp card (`tracks 1.1.7.dev53`, the seven subcommands) | the first paragraph of that repository's README |
| the argument in the hero and the Why section | `manuscript/Draft_main_text_human.txt` — the copy is drawn from it, so keep the two consistent |
