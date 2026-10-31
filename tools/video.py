import subprocess, sys, os, math
sys.path.insert(0, '/home/claude/gen')
from PIL import Image, ImageDraw, ImageFont
import logo

FD = '/usr/share/fonts/truetype/google-fonts/'
PUB = '/home/claude/furniture-website/client/public/'
os.makedirs(PUB + 'videos', exist_ok=True); os.makedirs(PUB + 'images/video', exist_ok=True)
FPS = 24
WIDE = {n: Image.open(f'/home/claude/gen/wide_{n}.png').convert('RGB') for n in ('living', 'dining', 'bedroom')}
YEL, INK = (255, 199, 44), (28, 25, 23)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def kb(scene, t, dur, out, zoom=(1.0, 1.14), pan=(0.0, 0.0)):
    im = WIDE[scene]; W, H = im.size; p = t / dur
    z = zoom[0] + (zoom[1] - zoom[0]) * p
    cw, ch = W / z, H / z
    cx = W / 2 + pan[0] * (p - .5) * (W - cw); cy = H / 2 + pan[1] * (p - .5) * (H - ch)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize(out, Image.BILINEAR, box=box)

class Overlay:
    def __init__(s, out):
        s.out = out; s.k = out[0] / 1280
        s.fb = ImageFont.truetype(FD + 'Poppins-Bold.ttf', int(62 * s.k))
        s.fm = ImageFont.truetype(FD + 'Poppins-Medium.ttf', int(24 * s.k))
        s.fs = ImageFont.truetype(FD + 'Poppins-Bold.ttf', int(22 * s.k))
        s.mark = logo.draw_wordmark(int(46 * s.k), 'light', False)

    def block(s, base, x, y, text, font, bg, fg, a, dx):
        if a <= 0: return
        k = s.k; d = ImageDraw.Draw(base); l, t, r, b = d.textbbox((0, 0), text, font=font)
        pw, ph = int(26 * k), int(14 * k); w, h = r - l + pw * 2, int(font.size * 1.55)
        lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(16 * k), fill=bg + (255,))
        ld.text((pw - l, h / 2), text, font=font, fill=fg, anchor='lm' if False else 'ls') if False else ld.text((w / 2, h / 2), text, font=font, fill=fg, anchor='mm')
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        base.alpha_composite(lay, (int(x + dx * (1 - a)), int(y)))

    def draw(s, frame, t, lines, sub, cta=True, t0=.3, t_out=None, fade_out=0.4):
        base = frame.convert('RGBA'); k = s.k
        gl = 1.0
        if t_out is not None: gl = 1 - ease((t - t_out) / fade_out)
        # logo plate
        pl = Image.new('RGBA', (s.mark.size[0] + int(28 * k), s.mark.size[1] + int(20 * k)), (0, 0, 0, 0))
        ImageDraw.Draw(pl).rounded_rectangle([0, 0, pl.size[0] - 1, pl.size[1] - 1], radius=int(18 * k), fill=(255, 255, 255, 235))
        pl.alpha_composite(s.mark, (int(14 * k), int(10 * k))); base.alpha_composite(pl, (int(40 * k), int(34 * k)))
        y = 120 * k; yy = y
        a1 = ease((t - t0) / .55) * gl; a2 = ease((t - t0 - .3) / .55) * gl; a3 = ease((t - t0 - .75) / .5) * gl; a4 = ease((t - t0 - 1.3) / .5) * gl
        s.block(base, 40 * k, yy, lines[0], s.fb, YEL, INK, a1, -80 * k)
        s.block(base, 40 * k, yy + 96 * k, lines[1], s.fb, INK, YEL, a2, -80 * k)
        s.block(base, 40 * k, yy + 200 * k, sub, s.fm, (255, 255, 255), INK, a3, -60 * k)
        if cta: s.block(base, 40 * k, yy + 266 * k, 'Shop now', s.fs, YEL, INK, a4, -40 * k)
        return base.convert('RGB')

    def end_card(s, w, h, a):
        card = Image.new('RGB', (w, h), YEL)
        lg = logo.draw_wordmark(int(h * .28), 'light', True)
        lg_bg = Image.new('RGBA', (lg.size[0] + int(60 * s.k), lg.size[1] + int(50 * s.k)), (255, 255, 255, 255))
        m = Image.new('L', lg_bg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, lg_bg.size[0] - 1, lg_bg.size[1] - 1], radius=int(30 * s.k), fill=255)
        lg_bg.alpha_composite(lg, (int(30 * s.k), int(25 * s.k)))
        card.paste(lg_bg.convert('RGB'), ((w - lg_bg.size[0]) // 2, int(h * .26)), m)
        d = ImageDraw.Draw(card)
        d.text((w / 2, h * .76), 'Free delivery over $500  ·  30-day returns', font=s.fm, fill=INK, anchor='mm')
        d.text((w / 2, h * .86), 'couchpuffy.example', font=s.fs, fill=INK, anchor='mm')
        return card

def encode(path, size):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-preset', 'slow', '-crf', '28', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', path], stdin=subprocess.PIPE)

def make_ad(name, scene, lines, sub, pan):
    out = (1280, 720); ov = Overlay(out); dur = 6.0; p = encode(PUB + f'videos/{name}.mp4', out); poster_done = False
    for i in range(int(dur * FPS)):
        t = i / FPS
        fr = ov.draw(kb(scene, t, dur, out, (1.0, 1.12), pan), t, lines, sub)
        if t >= 4.7:
            fr = Image.blend(fr, ov.end_card(*out, 1), ease((t - 4.7) / .5))
        if not poster_done and t >= 2.6:
            fr.save(PUB + f'images/video/{name}.webp', quality=80, method=6); poster_done = True
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

def make_hero():
    out = (960, 540); ov = Overlay(out); seg = 4.0; xf = .6; scenes = ['living', 'dining', 'bedroom']
    texts = [(('Level up', 'your furniture!'), 'New autumn collection'), (('Made for', 'gathering.'), 'Dining sets from $249'), (('Free delivery', 'over $500.'), '30-day returns · 10-year warranty')]
    pans = [(.6, 0), (-.6, 0), (.4, .3)]; total = seg * 3; p = encode(PUB + 'videos/hero-loop.mp4', out); poster_done = False
    def frame(idx, tl):
        f = kb(scenes[idx], tl, seg + xf, out, (1.0, 1.1), pans[idx])
        ln, sub = texts[idx]
        return ov.draw(f, tl, ln, sub, cta=False, t0=.25, t_out=seg - .5, fade_out=.35)
    for i in range(int(total * FPS)):
        t = i / FPS; idx = int(t // seg); tl = t - idx * seg
        fr = frame(idx, tl)
        if tl > seg - xf:
            nxt = (idx + 1) % 3
            fr = Image.blend(fr, frame(nxt, tl - (seg - xf) if False else 0.0 + (tl - (seg - xf)) * 0.0 + 0.0), ease((tl - (seg - xf)) / xf))
        if not poster_done and t >= .9:
            fr.save(PUB + 'images/video/hero-loop.webp', quality=80, method=6); poster_done = True
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    make_ad('ad-living-room', 'living', ('Sink into', 'puffy comfort.'), 'Aurora Sofa · from $1,299', (.5, 0))
    make_ad('ad-dining', 'dining', ('Gather around', 'something golden.'), 'Meridian Table · from $899', (-.5, 0))
    make_ad('ad-bedroom', 'bedroom', ('Sleep in', 'a cloud.'), 'Haven King Bed · from $1,099', (.3, .2))
    make_hero()
    for f in sorted(os.listdir(PUB + 'videos')): print(f, os.path.getsize(PUB + 'videos/' + f) // 1024, 'KB')
