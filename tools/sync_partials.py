"""Stamp the shared page chrome into every page.

The nav, the footer and the icon sprite are identical on every page, so each lives once in
tools/partials/ and is copied into the pages between a pair of marker comments:

    <!-- partial:nav · ... -->
    ...generated, do not edit...
    <!-- /partial:nav -->

The pages stay plain static HTML: Pages serves them exactly as committed, and nothing runs at
deploy time. Edit the partial, never the copy in a page, then

    python3 tools/sync_partials.py            rewrite the pages
    python3 tools/sync_partials.py --check    exit 1 if a page is out of date

Partials are string.Template text with two kinds of placeholder:

    ${root}         the path from the page back to the site root ("" or "../")
    ${here_<id>}    ' class="is-active" aria-current="page"' on page <id>, empty elsewhere
"""
import pathlib
import re
import string
import sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
PARTIALS = HERE / 'partials'

# page -> the id its own nav link is marked with (None: the page has no link of its own)
PAGES = {
    'index.html': None,
    'paper/index.html': 'paper',
    'community/index.html': 'community',
}
CURRENT = ' class="is-active" aria-current="page"'

BLOCK = re.compile(r'(<!-- partial:(\w+)\b[^>]*-->\n)(.*?)(<!-- /partial:\2 -->)', re.S)


def render(name, page, here):
    fields = {'root': '../' * page.count('/')}
    fields.update({f'here_{h}': CURRENT if h == here else ''
                   for h in PAGES.values() if h})
    return string.Template((PARTIALS / f'{name}.html').read_text()).substitute(fields)


def main():
    check = '--check' in sys.argv[1:]
    stale = []
    for page, here in PAGES.items():
        path = SITE / page
        old = path.read_text()
        new, n = BLOCK.subn(lambda m: m[1] + render(m[2], page, here) + m[4], old)
        if not n:
            sys.exit(f'{page}: no <!-- partial:... --> markers')
        if new != old:
            stale.append(page)
            if not check:
                path.write_text(new)

    if check and stale:
        sys.exit('out of date: ' + ', '.join(stale) + ' — run python3 tools/sync_partials.py')
    print(('rewrote: ' + ', '.join(stale)) if stale else 'all pages up to date')


if __name__ == '__main__':
    main()
