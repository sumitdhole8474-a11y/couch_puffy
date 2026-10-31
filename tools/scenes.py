import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter

S = 2  # supersampling

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def vgrad(size, c1, c2):
    w, h = size
    t = np.linspace(0, 1, max(h, 1))[:, None, None]
    a = np.array(hexc(c1) if isinstance(c1, str) else c1)[None, None, :]
    b = np.array(hexc(c2) if isinstance(c2, str) else c2)[None, None, :]
    arr = (a + (b - a) * t).astype('uint8')
    return Image.fromarray(np.repeat(arr, w, axis=1), 'RGB')

class Scene:
    def __init__(s, w=1200, h=900, horizon=.68, wall=('#FFF6D8', '#FBE9A8'), floor=('#D8B684', '#B58F5A')):
        s.w, s.h = w, h; s.W, s.H = w * S, h * S; s.hz = int(h * horizon)
        base = Image.new('RGB', (s.W, s.H))
        base.paste(vgrad((s.W, s.hz * S), *wall), (0, 0))
        base.paste(vgrad((s.W, s.H - s.hz * S), *floor), (0, s.hz * S))
        s.im = base.convert('RGBA')
        d = ImageDraw.Draw(s.im)
        d.rectangle([0, (s.hz - 8) * S, s.W, s.hz * S], fill=(255, 255, 255, 255))
        for i in range(1, 9):  # floor boards
            y = s.hz * S + int((s.H - s.hz * S) * (i / 9) ** 1.4)
            d.line([0, y, s.W, y], fill=(0, 0, 0, 22), width=S)
        s.floor_y = s.hz

    def b(s, box): return [int(v * S) for v in box]

    def comp(s, layer, blur=0):
        if blur: layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
        s.im = Image.alpha_composite(s.im, layer)

    def layer(s): return Image.new('RGBA', (s.W, s.H), (0, 0, 0, 0))

    def shadow(s, box, alpha=90, blur=14):
        l = s.layer(); ImageDraw.Draw(l).ellipse(s.b(box), fill=(30, 20, 5, alpha)); s.comp(l, blur)

    def rrect(s, box, r, fill, outline=None, width=1):
        l = s.layer(); ImageDraw.Draw(l).rounded_rectangle(s.b(box), radius=int(r * S), fill=fill, outline=outline, width=width * S); s.comp(l)

    def grect(s, box, r, c1, c2, alpha=255, horizontal=False):
        x0, y0, x1, y1 = s.b(box); w, h = x1 - x0, y1 - y0
        if w <= 0 or h <= 0: return
        g = vgrad((h, w) if horizontal else (w, h), c1, c2)
        if horizontal: g = g.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT) if False else vgrad((w, h), c1, c1)
        if horizontal:
            t = np.linspace(0, 1, w)[None, :, None]; a = np.array(hexc(c1))[None, None, :]; bb = np.array(hexc(c2))[None, None, :]
            g = Image.fromarray(np.repeat((a + (bb - a) * t).astype('uint8'), h, axis=0), 'RGB')
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(r * S), fill=alpha)
        l = s.layer(); l.paste(g.convert('RGBA'), (x0, y0), m); s.comp(l)

    def poly(s, pts, fill):
        l = s.layer(); ImageDraw.Draw(l).polygon([(x * S, y * S) for x, y in pts], fill=fill); s.comp(l)

    def ellipse(s, box, fill):
        l = s.layer(); ImageDraw.Draw(l).ellipse(s.b(box), fill=fill); s.comp(l)

    def glow(s, cx, cy, rad, color=(255, 214, 90), alpha=150):
        yy, xx = np.ogrid[:s.H, :s.W]
        d = np.sqrt((xx - cx * S) ** 2 + (yy - cy * S) ** 2) / (rad * S)
        a = np.clip(1 - d, 0, 1) ** 2 * alpha
        arr = np.zeros((s.H, s.W, 4), 'uint8'); arr[..., 0], arr[..., 1], arr[..., 2] = color; arr[..., 3] = a.astype('uint8')
        s.comp(Image.fromarray(arr, 'RGBA'))

    def rot_rrect(s, cx, cy, w, h, ang, r, c1, c2):
        pad = 20; lw, lh = int((w + pad) * S), int((h + pad) * S)
        g = vgrad((int(w * S), int(h * S)), c1, c2).convert('RGBA')
        m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], radius=int(r * S), fill=255)
        t = Image.new('RGBA', (lw, lh), (0, 0, 0, 0)); t.paste(g, (int(pad * S / 2), int(pad * S / 2)), m)
        t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
        l = s.layer(); l.paste(t, (int(cx * S - t.size[0] / 2), int(cy * S - t.size[1] / 2)), t); s.comp(l)

    def finish(s, size=None):
        im = s.im.convert('RGB').resize((s.w, s.h), Image.LANCZOS)
        return im.resize(size, Image.LANCZOS) if size else im

# ---------- palettes ----------
def shade(hexcol, f):
    r, g, b = hexc(hexcol); return '#%02x%02x%02x' % tuple(max(0, min(255, int(v * f))) for v in (r, g, b))

# ---------- decor ----------
def window(sc, x, y, w, h):
    sc.rrect([x - 8, y - 8, x + w + 8, y + h + 8], 6, (255, 255, 255, 255))
    sc.grect([x, y, x + w, y + h], 3, '#DFF1FF', '#FFFFFF')
    sc.rrect([x + w / 2 - 3, y, x + w / 2 + 3, y + h], 0, (255, 255, 255, 255))
    sc.rrect([x, y + h / 2 - 3, x + w, y + h / 2 + 3], 0, (255, 255, 255, 255))
    l = sc.layer(); ImageDraw.Draw(l).polygon([(x * S, (y + h) * S), ((x + w) * S, (y + h) * S), ((x + w + 260) * S, (sc.hz + 90) * S), ((x + 60) * S, (sc.hz + 90) * S)], fill=(255, 255, 235, 60)); sc.comp(l, 12)

def art(sc, x, y, w, h, seed=1, frame='#1C1917'):
    rnd = random.Random(seed)
    sc.rrect([x, y, x + w, y + h], 3, frame)
    sc.rrect([x + 8, y + 8, x + w - 8, y + h - 8], 1, '#FFFBEB')
    cols = ['#FACC15', '#EAB308', '#1C1917', '#FDE68A', '#A8A29E']
    sc.ellipse([x + w * .2, y + h * .22, x + w * .62, y + h * .62], cols[rnd.randrange(2)])
    sc.rrect([x + w * .3, y + h * .55, x + w * .85, y + h * .78], 8, cols[2])
    sc.ellipse([x + w * .55, y + h * .15, x + w * .8, y + h * .4], cols[3])

def plant(sc, cx, base, s=1.0, pot='#F3F0E8'):
    sc.shadow([cx - 38 * s, base - 8 * s, cx + 38 * s, base + 10 * s], 70, 6)
    sc.grect([cx - 28 * s, base - 70 * s, cx + 28 * s, base], 8, pot, shade(pot, .85))
    rnd = random.Random(int(cx))
    for i in range(11):
        ang = -80 + i * 16 + rnd.uniform(-5, 5); L = rnd.uniform(90, 150) * s
        a = math.radians(ang - 90 + 90)
        ex, ey = cx + math.sin(math.radians(ang)) * L * .8, base - 70 * s - math.cos(math.radians(ang)) * L
        g = '#4D7C0F' if i % 2 else '#65A30D'
        sc.poly([(cx - 6 * s, base - 66 * s), (cx + 6 * s, base - 66 * s), (ex + 16 * s, ey + 8), (ex, ey), (ex - 16 * s, ey + 8)], g)

def rug(sc, cx, y, w, h, color='#FDE68A'):
    l = sc.layer(); d = ImageDraw.Draw(l)
    d.ellipse(sc.b([cx - w / 2, y - h / 2, cx + w / 2, y + h / 2]), fill=hexc(color) + (255,))
    d.ellipse(sc.b([cx - w / 2 + 22, y - h / 2 + 8, cx + w / 2 - 22, y + h / 2 - 8]), outline=(255, 255, 255, 190), width=3 * S)
    sc.comp(l)

def vase(sc, cx, base, s=1.0, color='#FFFFFF'):
    sc.grect([cx - 14 * s, base - 46 * s, cx + 14 * s, base], 10, color, shade(color, .82))
    for dx, h in ((-8, 70), (0, 90), (9, 64)):
        sc.rrect([cx + dx * s - 1.5, base - 46 * s - h * s, cx + dx * s + 1.5, base - 40 * s], 1, '#6B8E23')
        sc.ellipse([cx + dx * s - 8 * s, base - 46 * s - h * s - 8 * s, cx + dx * s + 8 * s, base - 46 * s - h * s + 8 * s], '#FACC15')

def books(sc, x, base, n=5, seed=3, maxh=46):
    rnd = random.Random(seed); cols = ['#FACC15', '#1C1917', '#E7E5E4', '#EAB308', '#78716C', '#FDE68A']
    for i in range(n):
        h = rnd.randint(int(maxh * .6), maxh); w = rnd.randint(9, 15); c = cols[rnd.randrange(len(cols))]
        sc.rrect([x, base - h, x + w, base], 1, c); x += w + 1
    return x

# ---------- furniture ----------
LEG = '#2B211A'

def sofa(sc, cx, base, w=520, color='#FACC15', pillows=True):
    d = shade(color, .82); l = shade(color, 1.08)
    sc.shadow([cx - w / 2 - 10, base - 14, cx + w / 2 + 10, base + 22], 110, 14)
    for lx in (cx - w / 2 + 28, cx + w / 2 - 40):
        sc.rrect([lx, base - 6, lx + 12, base + 18], 3, LEG)
    sc.grect([cx - w / 2 + 40, base - 210, cx + w / 2 - 40, base - 70], 44, l, color)          # back
    sc.grect([cx - w / 2, base - 130, cx - w / 2 + 62, base - 6], 30, color, d)                # left arm
    sc.grect([cx + w / 2 - 62, base - 130, cx + w / 2, base - 6], 30, color, d)                # right arm
    inner = w - 124; cw = inner / 2
    for i in range(2):
        x0 = cx - w / 2 + 62 + i * cw
        sc.grect([x0 + 2, base - 120, x0 + cw - 2, base - 52], 22, l, color)
        sc.rrect([x0 + 2, base - 60, x0 + cw - 2, base - 28], 14, shade(color, .9))
    sc.rrect([cx - 1, base - 118, cx + 1, base - 56], 0, (0, 0, 0, 30))
    for i in range(2):  # back cushions
        x0 = cx - w / 2 + 70 + i * (cw - 4)
        sc.grect([x0, base - 205, x0 + cw - 12, base - 108], 32, shade(color, 1.12), shade(color, .96))
    if pillows:
        sc.rot_rrect(cx - w / 2 + 112, base - 112, 74, 70, -14, 18, '#1C1917', '#44403C')
        sc.rot_rrect(cx + w / 2 - 112, base - 110, 74, 70, 12, 18, '#FFFFFF', '#E7E5E4')

def armchair(sc, cx, base, s=1.0, color='#FACC15', legs='#B07A45'):
    d = shade(color, .8); l = shade(color, 1.1)
    sc.shadow([cx - 150 * s, base - 12 * s, cx + 150 * s, base + 24 * s], 110, 12)
    for dx, tilt in ((-92, -9), (92, 9)):
        sc.poly([(cx + dx * s - 8 * s, base - 70 * s), (cx + dx * s + 8 * s, base - 70 * s), (cx + (dx + tilt) * s + 5 * s, base + 14 * s), (cx + (dx + tilt) * s - 5 * s, base + 14 * s)], legs)
    sc.grect([cx - 135 * s, base - 330 * s, cx + 135 * s, base - 120 * s], 110 * s, l, color)       # back barrel
    sc.grect([cx - 150 * s, base - 200 * s, cx - 100 * s, base - 62 * s], 26 * s, color, d)
    sc.grect([cx + 100 * s, base - 200 * s, cx + 150 * s, base - 62 * s], 26 * s, color, d)
    sc.grect([cx - 112 * s, base - 150 * s, cx + 112 * s, base - 62 * s], 26 * s, l, color)          # seat
    sc.rrect([cx - 112 * s, base - 78 * s, cx + 112 * s, base - 62 * s], 8 * s, shade(color, .86))

def side_chair(sc, cx, base, s=1.0, seat='#FACC15', wood='#C79A63', flip=False):
    sc.shadow([cx - 70 * s, base - 8 * s, cx + 70 * s, base + 14 * s], 100, 8)
    for dx in (-52, 46):
        sc.rrect([cx + dx * s, base - 140 * s, cx + (dx + 9) * s, base + 4 * s], 3, wood)
    sc.rrect([cx - 54 * s, base - 300 * s, cx - 45 * s, base - 140 * s], 3, wood)
    sc.rrect([cx + 46 * s, base - 300 * s, cx + 55 * s, base - 140 * s], 3, wood)
    sc.grect([cx - 56 * s, base - 300 * s, cx + 57 * s, base - 224 * s], 14 * s, shade(wood, 1.12), wood)
    sc.grect([cx - 62 * s, base - 160 * s, cx + 62 * s, base - 130 * s], 12 * s, shade(seat, 1.1), seat)

def dining_table(sc, cx, base, w=640, top='#C9955B'):
    sc.shadow([cx - w / 2, base - 12, cx + w / 2, base + 24], 100, 14)
    for dx in (-w / 2 + 40, w / 2 - 56):
        sc.grect([cx + dx, base - 250, cx + dx + 16, base + 4], 3, shade(top, .8), shade(top, .62))
    sc.rrect([cx - w / 2 + 52, base - 252, cx + w / 2 - 52, base - 232], 3, shade(top, .72))
    sc.grect([cx - w / 2, base - 282, cx + w / 2, base - 248], 10, shade(top, 1.14), top)
    sc.rrect([cx - w / 2 + 10, base - 280, cx + w / 2 - 10, base - 274], 3, (255, 255, 255, 70))

def coffee_table(sc, cx, base, w=380, top='#D2A56B'):
    sc.shadow([cx - w / 2, base - 8, cx + w / 2, base + 22], 100, 12)
    for dx in (-w / 2 + 40, w / 2 - 48):
        sc.poly([(cx + dx, base - 100), (cx + dx + 8, base - 100), (cx + dx + 2, base + 6), (cx + dx - 6, base + 6)], '#1C1917')
    sc.ellipse([cx - w / 2, base - 134, cx + w / 2, base - 70], shade(top, .8))
    sc.grect([cx - w / 2, base - 130, cx + w / 2, base - 100], 14, shade(top, .9), shade(top, .72))
    sc.ellipse([cx - w / 2, base - 144, cx + w / 2, base - 84], top)
    sc.ellipse([cx - w / 2 + 14, base - 138, cx + w / 2 - 14, base - 94], shade(top, 1.1))

def floor_lamp(sc, cx, base, h=520, shade_c='#FFF1B8', glow_on=True):
    top = base - h
    if glow_on: sc.glow(cx, top + 60, 280, (255, 214, 90), 120)
    sc.shadow([cx - 60, base - 8, cx + 60, base + 12], 100, 6)
    sc.ellipse([cx - 52, base - 14, cx + 52, base + 8], '#B8860B')
    sc.rrect([cx - 4, top + 90, cx + 4, base - 6], 2, '#B8860B')
    sc.poly([(cx - 70, top + 130), (cx + 70, top + 130), (cx + 100, top + 10), (cx - 100, top + 10)], shade_c)
    sc.poly([(cx - 100, top + 10), (cx + 100, top + 10), (cx + 90, top - 6), (cx - 90, top - 6)], '#FFF9DC')
    sc.poly([(cx - 70, top + 130), (cx + 70, top + 130), (cx + 76, top + 112), (cx - 76, top + 112)], (255, 255, 255, 120))

def table_lamp(sc, cx, base, s=1.0):
    sc.glow(cx, base - 190 * s, 220 * s, (255, 214, 90), 130)
    sc.grect([cx - 34 * s, base - 130 * s, cx + 34 * s, base], 28 * s, '#FFFFFF', '#E7E5E4')
    sc.rrect([cx - 6 * s, base - 160 * s, cx + 6 * s, base - 126 * s], 2, '#B8860B')
    sc.poly([(cx - 52 * s, base - 160 * s), (cx + 52 * s, base - 160 * s), (cx + 72 * s, base - 255 * s), (cx - 72 * s, base - 255 * s)], '#FFF1B8')
    sc.poly([(cx - 72 * s, base - 255 * s), (cx + 72 * s, base - 255 * s), (cx + 66 * s, base - 265 * s), (cx - 66 * s, base - 265 * s)], '#FFFBE6')

def bed(sc, cx, base, w=660, color='#F5F0E6', accent='#FACC15', head='#E8B923', low=False):
    hh = 150 if low else 330
    sc.shadow([cx - w / 2 - 20, base - 16, cx + w / 2 + 20, base + 26], 110, 14)
    sc.grect([cx - w / 2 + 14, base - hh - 40, cx + w / 2 - 14, base - 90], 26, shade(head, 1.1), shade(head, .86))
    if not low:
        for r in range(3):
            for c in range(7):
                sc.ellipse([cx - w / 2 + 70 + c * 86, base - 290 + r * 60, cx - w / 2 + 80 + c * 86, base - 280 + r * 60], shade(head, .7))
    sc.grect([cx - w / 2, base - 110, cx + w / 2, base - 8], 18, shade('#8B6A45', 1.0), '#6E5336')       # frame
    sc.grect([cx - w / 2 + 6, base - 190, cx + w / 2 - 6, base - 70], 22, '#FFFFFF', color)                # mattress+duvet
    for i in range(2):
        sc.rot_rrect(cx - w / 4 + i * (w / 2), base - 214, 220, 82, -3 + i * 6, 30, '#FFFFFF', '#ECE7DC')
    sc.grect([cx - w / 2 + 6, base - 140, cx + w / 2 - 6, base - 76], 20, shade(accent, 1.1), accent)     # blanket
    sc.rrect([cx - w / 2 + 6, base - 100, cx + w / 2 - 6, base - 94], 0, (255, 255, 255, 80))
    sc.rot_rrect(cx + w / 4, base - 160, 150, 52, 0, 16, '#1C1917', '#44403C')
    for lx in (cx - w / 2 + 30, cx + w / 2 - 44):
        sc.rrect([lx, base - 12, lx + 14, base + 16], 3, LEG)

def nightstand(sc, cx, base, lamp=True):
    sc.shadow([cx - 60, base - 8, cx + 60, base + 14], 90, 6)
    sc.grect([cx - 52, base - 150, cx + 52, base - 12], 6, '#D2A56B', '#B98850')
    sc.rrect([cx - 40, base - 138, cx + 40, base - 84], 3, (0, 0, 0, 30)); sc.rrect([cx - 8, base - 112, cx + 8, base - 106], 3, '#1C1917')
    sc.rrect([cx - 40, base - 78, cx + 40, base - 24], 3, (0, 0, 0, 30)); sc.rrect([cx - 8, base - 52, cx + 8, base - 46], 3, '#1C1917')
    if lamp: table_lamp(sc, cx, base - 150, .7)

def bookshelf(sc, cx, base, w=380, h=640, wood='#C9955B'):
    sc.shadow([cx - w / 2 - 8, base - 12, cx + w / 2 + 8, base + 18], 100, 10)
    sc.grect([cx - w / 2, base - h, cx + w / 2, base], 6, shade(wood, .9), shade(wood, .78))
    n = 5; cell = (h - 20) / n
    for i in range(n):
        y0 = base - h + 10 + i * cell; y1 = y0 + cell - 10
        sc.rrect([cx - w / 2 + 12, y0, cx + w / 2 - 12, y1 + 4], 2, '#FFFBEB')
        sc.rrect([cx - w / 2 + 12, y1, cx + w / 2 - 12, y1 + 10], 0, shade(wood, 1.15))
        x = cx - w / 2 + 22
        if i == 0: plant(sc, cx + w / 4, y1 + 4, .42)
        if i in (1, 3): x = books(sc, x, y1, 7 if i == 1 else 6, seed=i + 2, maxh=int(cell - 22))
        if i == 1: sc.rrect([x + 20, y1 - 30, x + 90, y1], 4, '#FACC15')
        if i == 2:
            sc.rrect([cx - w / 2 + 26, y1 - 58, cx - w / 2 + 130, y1], 5, '#FACC15'); sc.rrect([cx - w / 2 + 140, y1 - 40, cx - w / 2 + 220, y1], 5, '#1C1917'); vase(sc, cx + w / 4 + 30, y1, .8)
        if i == 4: books(sc, cx - w / 2 + 40, y1, 9, seed=9, maxh=int(cell - 24)); sc.rrect([cx + 60, y1 - 44, cx + 150, y1], 5, '#FFFFFF')

def media_console(sc, cx, base, w=640, wood='#8A5A33'):
    sc.shadow([cx - w / 2 - 10, base - 10, cx + w / 2 + 10, base + 20], 100, 12)
    for lx in (cx - w / 2 + 40, cx + w / 2 - 54):
        sc.poly([(lx, base - 60), (lx + 14, base - 60), (lx + 8, base + 6), (lx + 4, base + 6)], '#1C1917')
    sc.grect([cx - w / 2, base - 170, cx + w / 2, base - 56], 10, shade(wood, 1.15), wood)
    dw = (w - 40) / 3
    for i in range(3):
        x0 = cx - w / 2 + 14 + i * (dw + 6)
        sc.rrect([x0, base - 158, x0 + dw - 6, base - 68], 6, shade(wood, .88), outline=(255, 255, 255, 40), width=2)
        sc.rrect([x0 + dw / 2 - 18, base - 120, x0 + dw / 2 + 10, base - 112], 3, '#FACC15')
    # TV
    sc.rrect([cx - 232, base - 436, cx + 232, base - 170], 8, '#111111')
    sc.grect([cx - 224, base - 428, cx + 224, base - 178], 4, '#FDE68A', '#F59E0B')
    sc.ellipse([cx - 120, base - 400, cx + 40, base - 250], (255, 255, 255, 70))
    sc.rrect([cx - 40, base - 176, cx + 40, base - 170], 2, '#111111')
    vase(sc, cx - w / 2 + 70, base - 170, .8); sc.rrect([cx + w / 2 - 130, base - 205, cx + w / 2 - 40, base - 170], 4, '#FFFFFF')

def side_table(sc, cx, base, s=1.0, top='#FFFFFF'):
    sc.shadow([cx - 60 * s, base - 8, cx + 60 * s, base + 12], 90, 6)
    sc.rrect([cx - 3 * s, base - 160 * s, cx + 3 * s, base], 2, '#1C1917')
    sc.ellipse([cx - 56 * s, base - 8, cx + 56 * s, base + 8], '#1C1917')
    sc.ellipse([cx - 62 * s, base - 182 * s, cx + 62 * s, base - 150 * s], top)

def sprinkle_cup(sc, x, y):
    sc.grect([x, y - 26, x + 28, y], 6, '#FFFFFF', '#E7E5E4'); sc.rrect([x + 26, y - 20, x + 36, y - 8], 4, '#E7E5E4')
