from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image, ImageDraw, ImageFont
import os

FD = '/usr/share/fonts/truetype/google-fonts/'
BOLD = TTFont(FD + 'Poppins-Bold.ttf')
MED = TTFont(FD + 'Poppins-Medium.ttf')
YEL, INK, WHITE = '#FFC72C', '#1C1917', '#FFFFFF'

def text_path(font, text, size, x, baseline, tracking=0.0):
    """Return (svg path d, advance width) with glyph outlines, so the logo needs no web font."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    s = size / upm; cx = x; d = []
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, cx, baseline))
        gs[g].draw(tp)
        d.append(pen.getCommands())
        cx += font['hmtx'][g][0] * s + tracking
    return ' '.join(d), cx - x - tracking

def width_of(font, text, size, tracking=0.0):
    return text_path(font, text, size, 0, 0, tracking)[1]

def xheight(font, size):
    return font['OS/2'].sxHeight * size / font['head'].unitsPerEm

SZ, H, PADX, GAP, R = 46, 72, 18, 6, 18
w1 = width_of(BOLD, 'couch', SZ, -0.5) + PADX * 2
w2 = width_of(BOLD, 'puffy', SZ, -0.5) + PADX * 2
TOTAL = w1 + GAP + w2
BASE = H / 2 + xheight(BOLD, SZ) / 2

def wordmark(theme='light', tagline=True):
    b1, b2 = YEL, INK
    t1, t2 = INK, YEL
    tag = INK
    if theme == 'dark':
        b1, b2, t1, t2, tag = YEL, WHITE, INK, INK, '#FDE68A'
    p1, _ = text_path(BOLD, 'couch', SZ, PADX, BASE, -0.5)
    p2, _ = text_path(BOLD, 'puffy', SZ, w1 + GAP + PADX, BASE, -0.5)
    vh = H + (34 if tagline else 0)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TOTAL:.1f} {vh}" role="img" aria-labelledby="t">',
           '<title id="t">Couchpuffy – level up your furniture!</title>',
           f'<rect width="{w1:.1f}" height="{H}" rx="{R}" fill="{b1}"/>',
           f'<rect x="{w1+GAP:.1f}" width="{w2:.1f}" height="{H}" rx="{R}" fill="{b2}"/>',
           f'<path d="{p1}" fill="{t1}"/>', f'<path d="{p2}" fill="{t2}"/>']
    if tagline:
        # scale the tagline so it spans the exact width of the wordmark
        raw = width_of(MED, 'level up your furniture!', 100, 0)
        size = 100 * TOTAL / (raw + 0.0) * 0.999
        size = min(size, 22)
        tw = width_of(MED, 'level up your furniture!', size, 0.6)
        pt, _ = text_path(MED, 'level up your furniture!', size, (TOTAL - tw) / 2, H + 25, 0.6)
        out.append(f'<path d="{pt}" fill="{tag}"/>')
    out.append('</svg>')
    return '\n'.join(out)

def mark_svg():
    n = 64; half = 32; sz = 46
    pc, wc = text_path(BOLD, 'c', sz, 0, 0)
    pp, wp = text_path(BOLD, 'p', sz, 0, 0)
    base = n / 2 + xheight(BOLD, sz) / 2
    pc, wc = text_path(BOLD, 'c', sz, half / 2 - wc / 2, base)
    pp, wp = text_path(BOLD, 'p', sz, half + half / 2 - wp / 2, base)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><title>Couchpuffy</title>'
            f'<clipPath id="c"><rect width="64" height="64" rx="15"/></clipPath>'
            f'<g clip-path="url(#c)"><rect width="32" height="64" fill="{YEL}"/><rect x="32" width="32" height="64" fill="{INK}"/></g>'
            f'<path d="{pc}" fill="{INK}"/><path d="{pp}" fill="{YEL}"/></svg>')

# ---------- PNG helpers (PIL) ----------
def pil_font(name, size): return ImageFont.truetype(FD + name, int(size))

def draw_mark(px):
    S = 4; n = px * S
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    mask = Image.new('L', (n, n), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 15 / 64), fill=255)
    body = Image.new('RGBA', (n, n)); d = ImageDraw.Draw(body)
    d.rectangle([0, 0, n // 2, n], fill=YEL); d.rectangle([n // 2, 0, n, n], fill=INK)
    im.paste(body, (0, 0), mask)
    d = ImageDraw.Draw(im); f = pil_font('Poppins-Bold.ttf', n * 46 / 64)
    cy = n / 2
    d.text((n / 4, cy), 'c', font=f, fill=INK, anchor='mm')
    d.text((n * 3 / 4, cy), 'p', font=f, fill=YEL, anchor='mm')
    return im.resize((px, px), Image.LANCZOS)

def draw_wordmark(height, theme='light', tagline=True):
    """Pixel version of the wordmark (used for video end cards and OG image)."""
    k = height / (H + (34 if tagline else 0)); S = 3
    scale = k * S
    vh = H + (34 if tagline else 0)
    w, h = int(TOTAL * scale), int(vh * scale)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b1, b2, t1, t2, tag = (YEL, INK, INK, YEL, INK) if theme == 'light' else (YEL, WHITE, INK, INK, '#FDE68A')
    d.rounded_rectangle([0, 0, w1 * scale, H * scale], radius=R * scale, fill=b1)
    d.rounded_rectangle([(w1 + GAP) * scale, 0, TOTAL * scale, H * scale], radius=R * scale, fill=b2)
    f = pil_font('Poppins-Bold.ttf', SZ * scale)
    d.text((w1 * scale / 2, H * scale / 2), 'couch', font=f, fill=t1, anchor='mm')
    d.text(((w1 + GAP + w2 / 2) * scale, H * scale / 2), 'puffy', font=f, fill=t2, anchor='mm')
    if tagline:
        ft = pil_font('Poppins-Medium.ttf', 20 * scale)
        d.text((TOTAL * scale / 2, (H + 18) * scale), 'level up your furniture!', font=ft, fill=tag, anchor='mm')
    return im.resize((int(w / S), int(h / S)), Image.LANCZOS)

if __name__ == '__main__':
    pub = '/home/claude/furniture-website/client/public/'
    open(pub + 'logo.svg', 'w').write(wordmark('light', True))
    open(pub + 'logo-wordmark.svg', 'w').write(wordmark('light', False))
    open(pub + 'logo-dark.svg', 'w').write(wordmark('dark', True))
    open(pub + 'favicon.svg', 'w').write(mark_svg())
    m = draw_mark(512)
    m.save(pub + 'icon-512.png'); m.resize((192, 192), Image.LANCZOS).save(pub + 'icon-192.png')
    bg = Image.new('RGBA', (180, 180), (255, 255, 255, 255)); mk = draw_mark(180); bg.alpha_composite(mk); bg.convert('RGB').save(pub + 'apple-touch-icon.png')
    draw_mark(64).save(pub + 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('logo files written', round(TOTAL), H)
