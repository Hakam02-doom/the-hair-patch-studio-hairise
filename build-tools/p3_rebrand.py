"""Project 3: apply The Hair Patch Studio branding, copy and site fixes to the pristine Hairise mirror.
usage: venv/bin/python -I p3_rebrand.py PRISTINE_DIR SITE_DIR ORIG_ASSETS_DIR"""
import os, re, sys, html, shutil
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
from p3_content import TEXT, SEQ, DEFAULT, PAGE_TEXT, NAME_SEQ, PHONE, TEL, EMAIL, ADDRESS, MAPS, IG, WA

PR, SITE, OA = sys.argv[1:4]
ASSETS = os.path.join(SITE, 'assets')

COLOR_SUBS = [
    (r'(?i)#2458B3', '#FD9800'), (r'36,\s*88,\s*179', '253, 152, 0'),
    (r'(?i)#ECF4FB', '#FEF9E1'), (r'236,\s*244,\s*251', '254, 249, 225'),
    (r'(?i)#222222\b', '#0F172A'), (r'(?i)#666666\b', '#454F5E'),
    (r'(?i)"?Chivo"?(,\s*sans-serif)?', "'Rubik', sans-serif"),
    (r'(?i)"?DM Sans"?(,\s*sans-serif)?', "'Karla', sans-serif"),
]
TOK = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)', re.S | re.I)

def norm(s): return ' '.join(html.unescape(s).replace('​', '').replace('\xa0', ' ').split())

def map_text(h, page):
    seq = {k: list(v) for k, v in SEQ.get(page, {}).items()}
    names = {k: list(v) for k, v in NAME_SEQ.get(page, {}).items()}
    pt = PAGE_TEXT.get(page, {})
    out = []
    in_header = False
    for t in TOK.split(h):
        if not t: continue
        if t.startswith('<'):
            if not t.startswith(('<script', '<style', '<!--')):
                def attr(m):
                    v = norm(m.group(3))
                    r = pt.get(v, TEXT.get(v))
                    return f'{m.group(1)}={m.group(2)}{html.escape(r)}{m.group(2)}' if r is not None else m.group(0)
                t = re.sub(r'\b(data-text|data-title|title|alt|placeholder|aria-label|value)=(["\'])(.*?)\2', attr, t)
            out.append(t); continue
        n = norm(t)
        new = None
        if not n:
            out.append(t); continue
        if n in seq and seq[n]:
            new = seq[n].pop(0)
        elif n in seq or n in DEFAULT:
            new = DEFAULT.get(n)
        elif n in names and names[n]:
            new = names[n].pop(0)
        elif n in pt:
            new = pt[n]
        elif n in TEXT:
            new = TEXT[n]
        if new is not None:
            lead = t[:len(t) - len(t.lstrip())]; trail = t[len(t.rstrip()):]
            out.append(lead + html.escape(new, quote=False) + trail)
        else:
            out.append(t)
    return ''.join(out)

def process(name):
    h = open(os.path.join(PR, name), encoding='utf-8').read()
    for a, b in COLOR_SUBS: h = re.sub(a, b, h)
    # header nav labels shouldn't take page-specific overrides: map the header first with no page overrides
    m = re.search(r'<header\b.*?</header>', h, re.S)
    if m:
        h = map_text(h[:m.start()], '_head') + map_text(m.group(0), '_header') + map_text(h[m.end():], name)
    else:
        h = map_text(h, name)
    soup = BeautifulSoup(h, 'html.parser')

    # --- third-party / shop / demo leftovers
    for s in soup.find_all('script'):
        src = s.get('src', ''); body = s.string or ''
        if any(k in src for k in ('add-to-cart', 'woocommerce', 'sourcebuster', 'order-attribution', 'cookiebot', 'googletagmanager', 'blockUI', 'index-a00a55', 'index-6b62f6')) \
                or 'gtag(' in body or 'wc_add_to_cart' in body or 'woocommerce_params' in body:
            s.decompose()
    for l in soup.find_all('link', href=re.compile(r'fonts\.googleapis|woocommerce|gfonts-')):
        l.decompose()
    for e in soup.select('.header-cart-inner, .header-cart, .search-icon, .search-form, .search-inner, form.search-form, '
                         '.post-navigation, .navigation.post-navigation'):
        e.decompose()
    for w in soup.select('.widget'):
        if 'Service Brochure' in w.get_text():
            w.decompose()

    # --- navigation: Home / About / Services (submenu) / Contact
    for menu in soup.select('ul.menu, ul#menu-main-menu, ul.navbar-nav, ul.mobile-menu'):
        for li in menu.find_all('li', recursive=False):
            a = li.find('a')
            if not a: continue
            label = norm(a.get_text())
            if label in ('Portfolio', 'Blog'):
                li.decompose(); continue
            target = {'Home': 'index.html', 'About': 'about.html', 'Services': 'services.html', 'Contact us': 'contact.html'}.get(label)
            if target:
                a['href'] = target
                if label in ('Home', 'About'):
                    for sub in li.select('ul.sub-menu'): sub.decompose()
                    li['class'] = [c for c in li.get('class', []) if 'has-children' not in c and 'dropdown' not in c]

    # --- links
    SERVICES = {'Hair Patch Fixing', 'Glue Bond Hair System', 'Tape Bond Hair System', 'Clip-On Hair System', 'Hair Topper Solutions',
                'Hair System Maintenance', 'Custom Hair System Design', 'Custom Hair Systems', 'Glue & Tape Bonding', 'Maintenance & Refitting',
                'Hair system maintenance', 'Hair patch cleaning & refitting', 'Hair topper solutions', 'Our Services'}
    LINKS = {'About Us': 'about.html', 'Our Specialists': 'about.html', 'Our Mission': 'about.html', 'about us': 'about.html',
             'Contact Us': 'contact.html', 'Contact': 'contact.html', 'contact us': 'contact.html', 'Contact us': 'contact.html',
             'Free Consultation': 'contact.html', 'Home': 'index.html',
             'Call ' + PHONE: TEL, PHONE: TEL, 'WhatsApp': WA, 'Instagram': IG, 'More on Instagram': IG,
             'Email us': 'mailto:' + EMAIL, EMAIL: 'mailto:' + EMAIL, 'Find the studio': MAPS, ADDRESS: MAPS}
    for a in soup.find_all('a'):
        t = norm(a.get_text()); href = a.get('href', '')
        if t in SERVICES: a['href'] = 'services.html'
        elif t in LINKS: a['href'] = LINKS[t]
        elif 'themesht.com' in href or 'themeht.com' in href: a['href'] = 'index.html'
        if a.get('href', '').startswith('http') and 'localhost' not in a['href']:
            a['target'] = '_blank'; a['rel'] = 'noopener'
    # portfolio (transformations) and blog cards -> Instagram / services
    for a in soup.select('a[href="#"]'):
        par = a.find_parent(class_=re.compile('portfolio|project|case'))
        blog = a.find_parent(class_=re.compile('post|blog'))
        if par: a['href'] = IG; a['target'] = '_blank'; a['rel'] = 'noopener'
        elif blog: a['href'] = 'services.html'
    # social: HPS is on Instagram only (+WhatsApp)
    for i in soup.select('i.bi-facebook, i.flaticon-twitter, i.bi-twitter, i.bi-twitter-x, i.bi-linkedin, i.bi-youtube, i.bi-pinterest'):
        a = i.find_parent('a'); li = a.find_parent('li') if a else None
        (li or a or i).decompose()
    for i in soup.select('i.bi-instagram'):
        a = i.find_parent('a')
        if a: a['href'] = IG; a['target'] = '_blank'; a['rel'] = 'noopener'; a['aria-label'] = 'Instagram'
    # footer: Instagram + WhatsApp icons (demo had Facebook / LinkedIn)
    for i in soup.select('i.flaticon-facebook-logo'):
        i['class'] = ['bi', 'bi-instagram']; a = i.find_parent('a')
        if a: a['href'] = IG; a['target'] = '_blank'; a['rel'] = 'noopener'; a['aria-label'] = 'Instagram'
    for i in soup.select('i.flaticon-linkedin'):
        i['class'] = ['bi', 'bi-whatsapp']; a = i.find_parent('a')
        if a: a['href'] = WA; a['target'] = '_blank'; a['rel'] = 'noopener'; a['aria-label'] = 'WhatsApp'
    # footer 'Free Consultation' widget was an empty newsletter slot on the demo -> real booking CTA
    for h in soup.select('footer h5.widget-title'):
        if norm(h.get_text()) == 'Free Consultation':
            tw = h.find_next_sibling(class_='textwidget')
            if tw is not None:
                tw.clear()
                tw.append(BeautifulSoup(f'<p class="hps-footer-cta-text">Book your free one-to-one consultation — call, WhatsApp or visit us in East London. Open every day, 9am–9pm.</p>'
                                        f'<div class="hps-footer-ctas"><a class="themeht-btn primary-btn" href="{TEL}">Call {PHONE}</a>'
                                        f'<a class="themeht-btn hps-btn-outline" href="{WA}" target="_blank" rel="noopener">WhatsApp us</a></div>', 'html.parser'))

    # remaining dead '#' links: drop list items for demo pages
    for a in soup.find_all('a', href='#'):
        if a.find('i') or a.get('class') and 'ht-nav-toggle' in a['class']: continue
        li = a.find_parent('li')
        if li and not li.find('ul') and norm(a.get_text()): li.decompose()

    # contact map: theme default (London Eye) -> the studio
    for f in soup.find_all('iframe', src=re.compile(r'maps\.google')):
        f['src'] = 'https://maps.google.com/maps?q=67%20Plashet%20Road%2C%20London%20E13%200QA&t=m&z=15&output=embed&iwloc=near'
        f['title'] = 'The Hair Patch Studio, 67 Plashet Road, London E13 0QA'

    # --- services page: page title + drop cap
    if name == 'services.html':
        for h1 in soup.select('.page-title h1, h1'):
            h1.string = 'Our Services'
        crumbs = soup.select('.breadcrumb li, .breadcrumb span, .breadcrumb a')
        if crumbs:
            last = [c for c in crumbs if norm(c.get_text())][-1]
            last.string = 'Our Services'
        for sp in soup.select('span.big-text'):
            if norm(sp.get_text()) == 'M': sp.string = 'W'

    # --- meta + brand layer
    for m in soup.find_all('meta', attrs={'name': 'description'}) + soup.find_all('meta', attrs={'property': 'og:description'}):
        m['content'] = 'The Hair Patch Studio — specialist non-surgical hair replacement in London: hair patch fixing, custom hair systems, glue & tape bonding, toppers and maintenance. Call ' + PHONE + '.'
    for m in soup.find_all('meta', attrs={'property': re.compile('og:(site_name|url|title)')}):
        m['content'] = {'og:site_name': 'The Hair Patch Studio', 'og:url': 'https://www.thehairpatchstudio.com/'}.get(m['property'], soup.title.string if soup.title else 'The Hair Patch Studio')
    for l in soup.find_all('link', rel=lambda r: r and ('icon' in r or 'apple-touch-icon' in r)):
        l['href'] = 'assets/' + [f for f in os.listdir(ASSETS) if f.startswith('favicon-1')][0]
    soup.head.append(BeautifulSoup('<link rel="stylesheet" href="assets/hps/fonts/fonts.css"><link rel="stylesheet" href="assets/hps-brand.css">', 'html.parser'))
    soup.body.append(BeautifulSoup('<script src="assets/hps-site.js" defer></script>', 'html.parser'))
    out = str(soup)
    for pre in ('https://themeht.com/hairise', 'https:\\/\\/themeht.com\\/hairise', 'https://themesht.com/hairise'):
        out = out.replace(pre, '.')
    out = out.replace('Hairise', 'The Hair Patch Studio')
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(out)
    print('built', name)

os.makedirs(os.path.join(OA, 'css'), exist_ok=True)
for f in os.listdir(ASSETS):
    if not f.endswith('.css') or f == 'hps-brand.css': continue
    p = os.path.join(ASSETS, f); b = os.path.join(OA, 'css', f)
    if not os.path.exists(b): shutil.copy2(p, b)
    css = open(b, encoding='utf-8', errors='replace').read()
    for a, c in COLOR_SUBS: css = re.sub(a, c, css)
    open(p, 'w', encoding='utf-8').write(css)

for f in sorted(os.listdir(PR)):
    if f.endswith('.html'): process(f)
