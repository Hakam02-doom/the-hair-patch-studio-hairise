"""Project 3: replace Hairise images in place with The Hair Patch Studio imagery (same filename + pixel size).
usage: venv/bin/python -I p2_assets.py SITE_ASSETS BACKUP_DIR FONTS_DIR"""
import os, re, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

A, BK, FD = sys.argv[1:4]
HPS = os.path.join(A, 'hps')
os.makedirs(BK, exist_ok=True)
ORANGE = (253, 152, 0); ORANGE_D = (233, 140, 0); NAVY = (15, 23, 42); SLATE = (69, 79, 94)
CREAM = (254, 249, 225); CREAM2 = (249, 240, 200); WHITE = (255, 255, 255)

STOCK = os.path.join(A, 'stock')   # high-res Unsplash photos (Unsplash License) for large generic slots

def src(name):
    if name.startswith('stock:'):
        im = Image.open(os.path.join(STOCK, name[6:] + '.jpg'))
        return im.convert('RGB')
    f = [x for x in os.listdir(HPS) if x.startswith(name)][0]
    im = Image.open(os.path.join(HPS, f))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (*WHITE, 255)); bg.alpha_composite(im); im = bg
    return im.convert('RGB')

def half(name, side):
    im = src(name); w, h = im.size
    return im.crop((0, 0, w // 2, h)) if side == 'L' else im.crop((w - w // 2, 0, w, h))

def cover(im, size, fx=.5, fy=.5):
    w, h = size
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    if s > 1.15:  # source smaller than the slot: restore edge detail lost in upscaling
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4 * min(s, 3), percent=70, threshold=2))
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

def hero_composite(im, size, place=.62, darken=.45):
    """Wide banner from a portrait photo: blurred fill + sharp photo, no extreme upscaling."""
    w, h = size
    bg = cover(im, size).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new('RGB', size, NAVY), darken)
    s = h / im.height
    fg = im.resize((round(im.width * s), h), Image.LANCZOS)
    x = int(w * place - fg.width / 2)
    mask = Image.new('L', fg.size, 255)
    fade = 80
    d = ImageDraw.Draw(mask)
    for i in range(fade):
        a = int(255 * i / fade)
        d.line([(i, 0), (i, h)], fill=a); d.line([(fg.width - 1 - i, 0), (fg.width - 1 - i, h)], fill=a)
    bg.paste(fg, (x, 0), mask)
    return bg

def initials(size, letter):
    im = Image.new('RGB', size, ORANGE); d = ImageDraw.Draw(im)
    d.text((size[0] / 2, size[1] / 2 + 1), letter, font=font('rubik-500.ttf', int(size[1] * .46)), fill=NAVY, anchor='mm')
    return im

def badge(size, text, sub=None):
    im = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((size[0] / 2, size[1] / 2 - (8 if sub else 0)), text, font=font('rubik-500.ttf', 19), fill=NAVY, anchor='mm')
    if sub:
        d.text((size[0] / 2, size[1] / 2 + 16), sub, font=font('karla-500.ttf', 13), fill=SLATE, anchor='mm')
    return im

def faces_group(size):
    """'Happy clients' avatar cluster: two client 'after' photos + plus circle (Regrow layout 167x72)."""
    w, h = size; im = Image.new('RGBA', size, (0, 0, 0, 0)); d = 64
    for i, (nm, side, fx, fy) in enumerate([('Men8', 'R', .5, .25), ('Men7', 'R', .55, .3)]):
        face = cover(half(nm, side), (d * 2, d * 2), fx, fy).resize((d, d), Image.LANCZOS)
        m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
        ring = Image.new('RGBA', (d + 6, d + 6), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((0, 0, d + 5, d + 5), fill=(*WHITE, 255))
        im.alpha_composite(ring, (i * 48, (h - d - 6) // 2)); im.paste(face, (i * 48 + 3, (h - d) // 2), m)
    cx = 2 * 48 + 3
    ImageDraw.Draw(im).ellipse((cx, (h - d) // 2, cx + d, (h + d) // 2), fill=(*WHITE, 255))
    ImageDraw.Draw(im).text((cx + d / 2, h / 2), '+', font=font('rubik-500.ttf', 34), fill=NAVY, anchor='mm')
    return im

# Hairise stem -> how to build the replacement (no photo repeats within a page)
PHOTO = {
    'banner-bg01': ('hero', 'g5062', .66),                         # hero slide 1
    'banner01-bg01-1': ('hero', 'Homepage', .66),                  # hero slide 2
    'banner3-bg2-1': ('shade', 'Men4', .5, .3),                     # page-title banner (about/services/contact)
    'form-bg': ('shade', 'stock:brickchair', .5, .5),                           # appointment form band
    'service-bg': ('shade', 'stock:sinks', .5, .5),                       # services list band
    'home01-about-img01': ('cover', 'stock:hairline', .5, .3),
    'home2-about-img': ('cover', 'Custom_Hair_System_Design', .5, .4),
    'portfolio-img1': ('cover', 'Men1', .5, .3), 'portfolio-img2': ('cover', 'Men3', .5, .3),
    'portfolio-img3': ('fit', 'Men2'), 'portfolio-img4': ('cover', 'Men4', .5, .3),
    'portfolio-img6': ('cover', 'Men8', .5, .3),
    'step-img1': ('cover', 'stock:gloves', .5, .35), 'step-img2': ('cover', 'stock:scissors', .5, .4),
    'step-img3': ('cover', 'stock:cutting', .6, .4),
    'team-img02': ('cover', 'stock:beard', .5, .3), 'team-img03': ('cover', 'stock:blowdry', .5, .25),
    'team-img04': ('cover', 'stock:tools', .5, .5), 'team-img06': ('cover', 'stock:mirrors', .5, .5),
}
AVATARS = {'testimonial-member4': 'B', 'testimonial-member5': 'P', 'testimonial-member6': 'D'}
BADGES = {}

# Hair_System_Maintenance has no own photo on the HPS site: use the cleaning photo
ALIASES = {'Hair_System_Maintenance': 'Hair_Patch_Cleaning'}

def stem_of(f):
    return re.sub(r'(-\d+x\d+)?-[0-9a-f]{6}\.\w+$', '', f)

n = 0
for f in sorted(os.listdir(A)):
    p = os.path.join(A, f)
    if not os.path.isfile(p) or not re.search(r'\.(jpe?g|png|webp)$', f): continue
    st = stem_of(f)
    if st not in PHOTO and st not in AVATARS and st not in ('favicon-1',):
        continue
    b = os.path.join(BK, f)
    if not os.path.exists(b): shutil.copy2(p, b)
    size = Image.open(b).size
    if st in PHOTO:
        spec = PHOTO[st]; kind = spec[0]
        name = ALIASES.get(spec[1], spec[1])
        if kind == 'hero': out = hero_composite(src(name), size, spec[2])
        elif kind == 'pair': out = hero_composite(half(name, spec[2]), size, .5, .12)
        elif kind == 'fit': out = hero_composite(src(name), size, .5, .12)
        elif kind == 'half': out = cover(half(name, spec[2]), size, spec[3], spec[4])
        elif kind == 'shade':
            out = cover(src(name), size, spec[2], spec[3]).convert('RGBA'); w_, h_ = size
            g = Image.new('L', (w_, 1))
            for x in range(w_): g.putpixel((x, 0), max(0, int(215 * (1 - x / (w_ * .62)))))
            ov = Image.new('RGBA', size, (*NAVY, 255)); ov.putalpha(g.resize(size)); out.alpha_composite(ov); out = out.convert('RGB')
        else: out = cover(src(name), size, spec[2], spec[3])
    elif st in AVATARS: out = initials(size, AVATARS[st])
    elif st in BADGES: out = badge(size, *BADGES[st])
    elif st.startswith('favicon'):
        logo = Image.open(os.path.join(HPS, 'HairPatchLogo-removebg-preview.png')).convert('RGBA')
        icon = logo.crop((150, 0, 470, 250))
        out = Image.new('RGB', size, CREAM); icon.thumbnail((int(size[0] * .9), int(size[1] * .9)), Image.LANCZOS)
        out.paste(icon, ((size[0] - icon.width) // 2, (size[1] - icon.height) // 2), icon)
    else:  # logos: full HPS logo; secondary (dark footer) gets light text
        logo = Image.open(os.path.join(HPS, 'HairPatchLogo-removebg-preview.png')).convert('RGBA')
        if st.startswith('secondary'):
            px = logo.load(); W, Hh = logo.size
            for y in range(int(Hh * .55), Hh):
                for x in range(W):
                    r, g, bb, a = px[x, y]
                    if a > 40 and r < 120 and g < 120 and bb < 140: px[x, y] = (255, 255, 255, a)
        scale = 2 if 'retina' in st else 1
        h = 64 * scale; w = round(logo.width * h / logo.height)
        out = logo.resize((w, h), Image.LANCZOS)
        out.save(p, 'PNG'); n += 1; continue
    if f.lower().endswith('.png'):
        (out if out.mode == 'RGBA' else out.convert('RGB')).save(p, 'PNG', optimize=True)
    else:
        out.convert('RGB').save(p, 'JPEG', quality=88, optimize=True, progressive=True)
    n += 1
print('replaced', n)

# Hairise logos are SVG files wrapping a PNG: replace with the HPS logo (dark text + white-text variant)
import base64, io
logo = Image.open(os.path.join(HPS, 'HairPatchLogo-removebg-preview.png')).convert('RGBA')
def svg_of(im):
    b = io.BytesIO(); im.save(b, 'PNG')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {im.width} {im.height}" '
            f'width="{im.width}" height="{im.height}"><image width="{im.width}" height="{im.height}" '
            f'href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/></svg>')
white = logo.copy(); px = white.load()
for y in range(int(white.height * .55), white.height):
    for x in range(white.width):
        r, g, bb, a = px[x, y]
        if a > 40 and r < 120 and g < 120 and bb < 140: px[x, y] = (255, 255, 255, a)
for f in os.listdir(A):
    if f.startswith('logo-white') and f.endswith('.svg'): open(os.path.join(A, f), 'w').write(svg_of(white))
    if f.startswith('logo-dark') and f.endswith('.svg'): open(os.path.join(A, f), 'w').write(svg_of(logo))

# SVG accents: Hairise blue -> HPS orange
for f in os.listdir(A):
    if f.endswith('.svg'):
        p = os.path.join(A, f); s = open(p, encoding='utf-8', errors='ignore').read()
        t = re.sub(r'(?i)#2458B3', '#FD9800', s)
        if t != s: open(p, 'w', encoding='utf-8').write(t)
