"""Bio-Babel logo family generator.

The mark is the uploaded artwork — a stepped Tower of Babel of four battered
storeys, cornices and arched galleries, in a single flat colour. Its geometry is
transcribed verbatim below; nothing here re-draws it.

Two changes are made to how it is *expressed*:

  1. The original uses a <mask> to punch the arches out. Browsers handle that
     correctly, but non-browser rasterisers (cairosvg, several doc pipelines)
     silently drop the mask and paint a solid 512x512 square. Every file here
     instead uses one path with reversed hole sub-paths and nonzero winding,
     which renders identically in Chromium (verified: the only differing pixels
     are edge anti-aliasing) and works everywhere else too.

  2. The arches stay true cut-outs, so whatever is behind shows through. That is
     why the mark must never sit on a field close to its own colour — on the
     tile the tower is cream and the arches show the violet field.

Outputs -> ../assets/img/
  logo-mark.svg           flat #8477C8, transparent ground  (the canonical mark)
  logo-mark-mono.svg      fill="currentColor" — inline it and tint from CSS
  logo-mark-ghost.svg     white — for low-opacity watermarks
  logo-mark-gradient.svg  site violet -> gold, for use against the dark field
  logo-tile.svg           squircle app tile: cream tower on a violet field
  favicon.svg             simplified tile that still reads at 16 px
  logo-wordmark.svg       horizontal lockup: mark + "Bio-Babel" + tagline
  logo-banner.svg         1080x240 dark banner for the org README

  python3 tools/gen_logo.py        (cairosvg optional; only used for previews)
"""
import pathlib

try:
    import cairosvg              # optional: PNG previews only
except ImportError:
    cairosvg = None

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'assets' / 'img'
PREVIEW = HERE / '_preview'
OUT.mkdir(parents=True, exist_ok=True)

CREAM = '#FFFCF2'
STONE = '#8477C8'          # the uploaded mark's colour
VIOLET = '#8B5CF6'
GOLD = '#F2C879'

# ═════════════════════════════════════════════ geometry (from the artwork) ════
# Four battered storeys, widening as they descend.
STOREYS = ['M220 48h72l13 58h-98z',
           'M185 126h142l17 72H168z',
           'M146 220h220l21 90H125z',
           'M103 334h306l25 100H78z']
# Cornices and the two-course plinth: x, y, w, h, r
CORNICES = [(194, 104, 124, 18, 4), (154, 196, 204, 20, 4), (108, 308, 296, 22, 4),
            (60, 432, 392, 22, 4), (42, 452, 428, 22, 4)]
# Arched galleries (cut out): x_left, y_base, height, radius.
# Each gallery is centred on x=256; spacing tuned so the outermost piers stay
# at least ~10px thick against the battered walls.
ARCHES = [(241, 96, 18, 15),
          (189, 178, 24, 15), (241, 178, 24, 15), (293, 178, 24, 15),
          (147, 290, 30, 17), (193, 290, 30, 17), (239, 290, 30, 17),
          (285, 290, 30, 17), (331, 290, 30, 17),
          (104.5, 414, 40, 19), (157.5, 414, 40, 19), (210.5, 414, 40, 19),
          (263.5, 414, 40, 19), (316.5, 414, 40, 19), (369.5, 414, 40, 19)]

# Small-size variant: same silhouette, fewer and wider openings, so the arcade
# still reads as an arcade instead of turning to mush below ~24 px.
ARCHES_SMALL = [(233, 100, 20, 23),
                (205, 186, 28, 26), (255, 186, 28, 26),
                (166, 298, 36, 29), (230, 298, 36, 29), (294, 298, 36, 29),
                (126, 424, 46, 33), (192, 424, 46, 33), (258, 424, 46, 33),
                (324, 424, 46, 33)]

# glyph bounding box, used to centre the mark inside other artboards
BBOX = (42, 48, 470, 474)      # x0, y0, x1, y1


def _rrect(x, y, w, h, r):
    """Rounded rectangle traced clockwise — same winding as the storey paths."""
    return (f'M{x + r} {y}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h - r}'
            f'a{r} {r} 0 0 1 {-r} {r}H{x + r}a{r} {r} 0 0 1 {-r} {-r}V{y + r}'
            f'a{r} {r} 0 0 1 {r} {-r}z')


def _arch(x, yb, h, r):
    """An opening, traced anticlockwise so nonzero winding subtracts it."""
    d = 2 * r
    return f'M{x + d} {yb}v{-h}a{r} {r} 0 0 0 {-d} 0v{h}z'


def mark_path(small=False):
    arches = ARCHES_SMALL if small else ARCHES
    return ' '.join(STOREYS + [_rrect(*c) for c in CORNICES] +
                    [_arch(*a) for a in arches])


def mark(fill, small=False, transform=None):
    g = f'<path fill="{fill}" d="{mark_path(small)}"/>'
    if transform:
        return f'  <g transform="{transform}">\n    {g}\n  </g>'
    return f'  {g}'


def fit(box_cx, box_cy, scale):
    """Centre the glyph's bounding box on (box_cx, box_cy) at the given scale."""
    gx = (BBOX[0] + BBOX[2]) / 2
    gy = (BBOX[1] + BBOX[3]) / 2
    return f'translate({box_cx} {box_cy}) scale({scale:g}) translate({-gx:g} {-gy:g})'


TITLE = ('  <title>Bio-Babel</title>\n'
         '  <desc>A stepped Tower of Babel of four battered storeys, cornices and '
         'arched galleries.</desc>\n')


def svg(w, h, body, label='Bio-Babel', titled=True):
    if label:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{label}">\n')
    else:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" fill="none" aria-hidden="true">\n')
    return head + (TITLE if titled else '') + body + '\n</svg>\n'


# ── 1. the mark, in its four dresses ────────────────────────────────────────
(OUT / 'logo-mark.svg').write_text(svg(512, 512, mark(STONE)))
(OUT / 'logo-mark-mono.svg').write_text(svg(512, 512, mark('currentColor')))
(OUT / 'logo-mark-ghost.svg').write_text(
    svg(512, 512, mark('#FFFFFF'), label='', titled=False))

GRAD = ('  <defs>\n'
        '    <linearGradient id="bbAscend" gradientUnits="userSpaceOnUse" '
        'x1="256" y1="474" x2="256" y2="48">\n'
        '      <stop offset="0"    stop-color="#6A48F2"/>\n'
        '      <stop offset="0.55" stop-color="#8B5CF6"/>\n'
        '      <stop offset="0.82" stop-color="#B49BFF"/>\n'
        '      <stop offset="1"    stop-color="#F2C879"/>\n'
        '    </linearGradient>\n'
        '  </defs>\n')
(OUT / 'logo-mark-gradient.svg').write_text(
    svg(512, 512, GRAD + mark('url(#bbAscend)')))

# ── 2. app tile ─────────────────────────────────────────────────────────────
TILE_BG = ('  <defs>\n'
           '    <linearGradient id="bbTile" gradientUnits="userSpaceOnUse" '
           'x1="0" y1="0" x2="512" y2="512">\n'
           '      <stop offset="0" stop-color="#7C5CF6"/>\n'
           '      <stop offset="1" stop-color="#4B2FB8"/>\n'
           '    </linearGradient>\n'
           '  </defs>\n'
           '  <rect width="512" height="512" rx="116" fill="url(#bbTile)"/>\n')
(OUT / 'logo-tile.svg').write_text(
    svg(512, 512, TILE_BG + mark(CREAM, transform=fit(256, 252, 0.80))))

# ── 3. favicon — simplified arcade, tighter crop ────────────────────────────
(OUT / 'favicon.svg').write_text(
    svg(512, 512, TILE_BG + mark(CREAM, small=True, transform=fit(256, 254, 0.90))))

# ── 4. wordmark lockup ──────────────────────────────────────────────────────
SANS = ('Inter,&quot;SF Pro Display&quot;,-apple-system,BlinkMacSystemFont,'
        '&quot;Segoe UI&quot;,Helvetica,Arial,sans-serif')
MONO = ('ui-monospace,SFMono-Regular,&quot;SF Mono&quot;,Menlo,Consolas,'
        '&quot;Liberation Mono&quot;,monospace')

wordmark = (GRAD
            + mark('url(#bbAscend)', transform=fit(62, 64, 0.215)) + '\n'
            + f'  <text x="140" y="74" font-family="{SANS}" font-size="50" '
              f'font-weight="700" letter-spacing="-1.5" fill="{CREAM}">Bio'
              f'<tspan fill="{VIOLET}">-</tspan>Babel</text>\n'
            + f'  <text x="143" y="98" font-family="{SANS}" font-size="13" '
              f'font-weight="500" letter-spacing="3" fill="#8B94A7">'
              'THE CLASSICS, IN MORE THAN ONE TONGUE</text>')
(OUT / 'logo-wordmark.svg').write_text(svg(600, 128, wordmark))

# ── 5. README banner ────────────────────────────────────────────────────────
banner_defs = (
    '  <defs>\n'
    '    <linearGradient id="bbAscend" gradientUnits="userSpaceOnUse" '
    'x1="256" y1="474" x2="256" y2="48">\n'
    '      <stop offset="0"    stop-color="#6A48F2"/>\n'
    '      <stop offset="0.55" stop-color="#8B5CF6"/>\n'
    '      <stop offset="0.82" stop-color="#B49BFF"/>\n'
    '      <stop offset="1"    stop-color="#F2C879"/>\n'
    '    </linearGradient>\n'
    '    <radialGradient id="bbGlow" cx="0.5" cy="0.5" r="0.5">\n'
    '      <stop offset="0" stop-color="#8B5CF6" stop-opacity="0.34"/>\n'
    '      <stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/>\n'
    '    </radialGradient>\n'
    '    <pattern id="bbGrid" width="40" height="40" patternUnits="userSpaceOnUse">\n'
    '      <path d="M40 0 H0 V40" fill="none" stroke="#FFFFFF" '
    'stroke-opacity="0.045" stroke-width="1"/>\n'
    '    </pattern>\n'
    '  </defs>\n'
    '  <rect width="1080" height="240" fill="#0B0E14"/>\n'
    '  <rect width="1080" height="240" fill="url(#bbGrid)"/>\n'
    '  <ellipse cx="180" cy="120" rx="265" ry="165" fill="url(#bbGlow)"/>\n'
    '  <rect y="239" width="1080" height="1" fill="#FFFFFF" fill-opacity="0.08"/>\n')

# The README already carries a one-line subtitle directly beneath this image, so the
# banner holds no prose and no catalog list — wordmark and tagline only, nothing
# repeated and no package name that can go stale.
banner = (banner_defs
          + mark('url(#bbAscend)', transform=fit(180, 120, 0.42)) + '\n'
          + f'  <text x="340" y="126" font-family="{SANS}" font-size="74" '
            f'font-weight="700" letter-spacing="-2.6" fill="{CREAM}">Bio'
            f'<tspan fill="{VIOLET}">-</tspan>Babel</text>\n'
          + f'  <text x="344" y="164" font-family="{MONO}" font-size="16.5" '
            f'fill="{GOLD}" textLength="616" lengthAdjust="spacing">'
            'THE CLASSICS, KEPT ALIVE IN MORE THAN ONE TONGUE</text>')
(OUT / 'logo-banner.svg').write_text(svg(1080, 240, banner))

names = sorted(p.name for p in OUT.glob('*.svg'))
if cairosvg is None:
    print('generated (cairosvg absent — skipped PNG previews):', *names)
    raise SystemExit

PREVIEW.mkdir(exist_ok=True)
for name, sizes in [('logo-mark', (384, 96, 32)), ('logo-tile', (256, 64, 32)),
                    ('favicon', (128, 32, 16))]:
    for sz in sizes:
        cairosvg.svg2png(url=str(OUT / f'{name}.svg'),
                         write_to=str(PREVIEW / f'{name}_{sz}.png'),
                         output_width=sz, output_height=sz, background_color='#0d1117')
cairosvg.svg2png(url=str(OUT / 'logo-banner.svg'),
                 write_to=str(PREVIEW / 'banner.png'), output_width=1200)
print('generated:', *names)
