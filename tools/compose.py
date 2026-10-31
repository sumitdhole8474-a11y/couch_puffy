import json, os, sys
sys.path.insert(0, '/home/claude/gen')
from scenes import *

PUB = '/home/claude/furniture-website/client/public/images/'
os.makedirs(PUB + 'products', exist_ok=True); os.makedirs(PUB + 'scenes', exist_ok=True)

def room(w=1200, h=900, wall=('#FFF6D8', '#FBE9A8'), floor=('#D8B684', '#B58F5A'), hz=.68):
    return Scene(w, h, hz, wall, floor)

CREAM = ('#FFFBEB', '#FEF3C7'); WHITE = ('#FFFFFF', '#F5F5F4'); WARM = ('#FFF3C4', '#FCE38A'); STONE = ('#F5F5F4', '#E7E5E4')

def p_aurora():
    sc = room(wall=CREAM); window(sc, 90, 120, 200, 300); art(sc, 860, 150, 190, 250, 2)
    rug(sc, 600, 770, 780, 150, '#FDE68A'); plant(sc, 1090, 650, 1.1); floor_lamp(sc, 120, 640, 470, glow_on=False)
    sofa(sc, 580, 690, 560, '#FACC15'); return sc
def p_solace():
    sc = room(wall=STONE, floor=('#CBB08A', '#A88B62')); art(sc, 420, 120, 240, 160, 5, '#FACC15'); art(sc, 700, 120, 120, 160, 7)
    rug(sc, 600, 780, 820, 150, '#FACC15'); sofa(sc, 600, 690, 700, '#57534E', pillows=False)
    sc.rot_rrect(430, 590, 78, 72, -10, 18, '#FACC15', '#EAB308'); sc.rot_rrect(790, 592, 78, 72, 9, 18, '#FFFFFF', '#E7E5E4')
    side_table(sc, 1010, 700, 1.1); vase(sc, 1010, 524, .9); return sc
def p_halo():
    sc = room(wall=WARM); window(sc, 780, 130, 260, 330); rug(sc, 560, 770, 560, 120, '#FFFFFF')
    plant(sc, 130, 690, 1.2); armchair(sc, 540, 700, 1.2, '#FACC15'); side_table(sc, 860, 700, 1.2); vase(sc, 860, 505, 1.0); return sc
def p_nord():
    sc = room(wall=WHITE, floor=('#E2C79B', '#C4A173')); art(sc, 470, 130, 260, 200, 4, '#C79A63')
    side_chair(sc, 410, 700, 1.45, '#FACC15'); side_chair(sc, 790, 700, 1.45, '#1C1917'); plant(sc, 130, 700, 1.0); return sc
def p_meridian():
    sc = room(wall=CREAM); window(sc, 120, 120, 220, 320)
    sc.rrect([590, 0, 594, 190], 0, '#1C1917'); sc.poly([(520, 190), (664, 190), (690, 250), (494, 250)], '#FACC15'); sc.glow(592, 250, 300, (255, 214, 90), 130)
    side_chair(sc, 420, 640, 1.1, '#FACC15'); side_chair(sc, 780, 640, 1.1, '#FACC15')
    dining_table(sc, 600, 740, 720); vase(sc, 600, 458, 1.3); sc.rrect([380, 478, 470, 490], 6, '#FFFFFF'); sc.rrect([730, 478, 820, 490], 6, '#FFFFFF')
    plant(sc, 1090, 660, 1.1); return sc
def p_sol():
    sc = room(wall=STONE); art(sc, 470, 120, 260, 200, 8)
    sofa(sc, 600, 610, 800, '#78716C', pillows=False); rug(sc, 600, 800, 700, 130, '#FACC15')
    coffee_table(sc, 600, 800, 420); sc.rrect([480, 658, 580, 668], 3, '#1C1917'); sc.rrect([488, 648, 572, 658], 3, '#FACC15'); sprinkle_cup(sc, 650, 664)
    plant(sc, 1100, 650, 1.0); return sc
def p_haven():
    sc = room(wall=('#FFF8E0', '#FDEFB5')); window(sc, 90, 140, 180, 260); art(sc, 900, 150, 160, 220, 11)
    bed(sc, 600, 740, 640, '#F5F0E6', '#FACC15', '#E8B923'); nightstand(sc, 170, 740); nightstand(sc, 1030, 740)
    rug(sc, 600, 835, 760, 110, '#FEF3C7'); return sc
def p_dune():
    sc = room(wall=WHITE, floor=('#D5B88C', '#B0905F')); art(sc, 470, 140, 260, 180, 13, '#1C1917'); art(sc, 740, 150, 100, 140, 14, '#FACC15')
    bed(sc, 600, 730, 700, '#FFFFFF', '#1C1917', '#B98850', low=True); plant(sc, 1090, 690, 1.0); rug(sc, 600, 830, 800, 100, '#FDE68A'); return sc
def p_atlas():
    sc = room(wall=WARM); window(sc, 90, 150, 180, 280)
    bookshelf(sc, 600, 730, 420, 640, '#C9955B'); plant(sc, 970, 720, 1.2); sc.rrect([1040, 640, 1110, 720], 4, '#FACC15'); return sc
def p_loft():
    sc = room(wall=STONE, floor=('#CBB08A', '#A88B62')); art(sc, 160, 180, 200, 260, 15); art(sc, 840, 160, 240, 170, 16, '#FACC15')
    media_console(sc, 600, 700, 700, '#8A5A33'); plant(sc, 1100, 700, 1.0); floor_lamp(sc, 90, 710, 520, glow_on=False); return sc
def p_lumen():
    sc = room(wall=('#FFF3C9', '#FADF8C'), hz=.70); armchair(sc, 760, 710, .9, '#57534E'); floor_lamp(sc, 330, 720, 620)
    plant(sc, 1100, 690, 1.0); art(sc, 520, 120, 200, 260, 17); return sc
def p_glow():
    sc = room(wall=('#FFF3C9', '#FADF8C'), hz=.70)
    sc.grect([380, 560, 820, 600], 6, '#D2A56B', '#B98850')
    for lx in (410, 770): sc.rrect([lx, 598, lx + 16, 720], 3, '#1C1917')
    sc.shadow([360, 700, 840, 740], 90, 10)
    table_lamp(sc, 520, 560, 1.7); books(sc, 650, 560, 4, 21, 70); sprinkle_cup(sc, 740, 560); art(sc, 850, 150, 160, 230, 19); return sc

MAP = {'aurora-three-seater-sofa': p_aurora, 'solace-lounge-sofa': p_solace, 'halo-accent-chair': p_halo, 'nord-dining-chair-set-of-2': p_nord,
       'meridian-dining-table': p_meridian, 'sol-coffee-table': p_sol, 'haven-king-bed-frame': p_haven, 'dune-platform-bed': p_dune,
       'atlas-open-bookshelf': p_atlas, 'loft-media-console': p_loft, 'lumen-floor-lamp': p_lumen, 'glow-table-lamp': p_glow}

# ---------- wide 16:9 scenes (for hero, videos) ----------
def w_living():
    sc = room(1600, 900, wall=CREAM, hz=.7); window(sc, 130, 120, 240, 340); art(sc, 1040, 140, 220, 290, 22); art(sc, 1290, 180, 130, 190, 23, '#FACC15')
    rug(sc, 780, 800, 980, 130, '#FDE68A'); floor_lamp(sc, 1470, 700, 520); plant(sc, 120, 700, 1.3)
    sofa(sc, 760, 690, 700, '#FACC15'); coffee_table(sc, 790, 830, 340); return sc
def w_dining():
    sc = room(1600, 900, wall=WARM, hz=.7); window(sc, 1170, 120, 260, 340)
    sc.rrect([798, 0, 802, 150], 0, '#1C1917'); sc.poly([(720, 150), (880, 150), (910, 215), (690, 215)], '#FACC15'); sc.glow(800, 220, 340, (255, 214, 90), 140)
    side_chair(sc, 560, 650, 1.2, '#FACC15'); side_chair(sc, 1040, 650, 1.2, '#FACC15'); dining_table(sc, 800, 760, 860)
    vase(sc, 800, 456, 1.4); plant(sc, 200, 700, 1.3); art(sc, 160, 140, 220, 280, 24); return sc
def w_bedroom():
    sc = room(1600, 900, wall=('#FFF8E0', '#FDEFB5'), hz=.7); window(sc, 110, 140, 220, 300); art(sc, 1250, 150, 200, 270, 25)
    bed(sc, 800, 760, 720, '#F5F0E6', '#FACC15', '#E8B923'); nightstand(sc, 330, 760); nightstand(sc, 1270, 760); rug(sc, 800, 850, 900, 90, '#FEF3C7'); return sc

if __name__ == '__main__':
    prods = json.load(open('/home/claude/furniture-website/client/src/data/products.json'))
    sheet = Image.new('RGB', (4 * 400, 3 * 300), 'white')
    for i, p in enumerate(prods):
        im = MAP[p['slug']]().finish()
        im.save(PUB + f"products/{p['slug']}.webp", quality=82, method=6)
        im.resize((600, 450), Image.LANCZOS).save(PUB + f"products/{p['slug']}-sm.webp", quality=80, method=6)
        sheet.paste(im.resize((400, 300)), ((i % 4) * 400, (i // 4) * 300))
    sheet.save('/home/claude/gen/sheet.jpg', quality=85)
    for n, f in (('living', w_living), ('dining', w_dining), ('bedroom', w_bedroom)):
        im = f().finish(); im.save(f'/home/claude/gen/wide_{n}.png'); im.save(PUB + f'scenes/{n}.webp', quality=82, method=6)
    print('done')
