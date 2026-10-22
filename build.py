#!/usr/bin/env python3
"""Generates index.html (python3 build.py index.html) for the macOS / iOS style personal site (run once; the output is plain HTML)."""
import html, sys

OUT = sys.argv[1]
E = html.escape

# id, label, icon, x%, y%, title, subtitle, paragraphs, meta rows, previews, link
PROJECTS = [
  dict(id="tiketvisa", label="TiketVisa", icon="img/p/tiketvisa-icon.webp", x=31, y=15,
       sub="Startup · Founder",
       text=["Onward flight reservations and hotel bookings with a real PNR, for travellers who have to show a ticket out at the embassy or the airport.",
             "I moved the site off WordPress to a static Next.js build in 18 languages, with Cloudflare Workers routing between the new pages and the blog, handling forms and serving images."],
       meta=[("Role", "Founder, product and engineering"), ("Built with", "Next.js, Cloudflare Workers, WordPress"), ("Languages", "18")],
       previews=["img/p/tiketvisa.webp"], link="https://tiketvisa.com"),
  dict(id="unlisim", label="UnliSIM", icon="img/p/unlisim-icon.webp", x=46, y=9,
       sub="Startup · Founder",
       text=["Travel eSIMs for 200+ destinations. Pick a country and the number of days, pay with Apple Pay, Google Pay or card, and the phone is online in about two minutes. No roaming bill, no SIM swap."],
       meta=[("Role", "Founder and engineering"), ("Built with", "Next.js on Cloudflare (OpenNext)"), ("Coverage", "200+ destinations")],
       previews=["img/p/unlisim.webp"], link="https://unlisim.com"),
  dict(id="valuto", label="Valuto", icon="img/p/valuto-icon.webp", x=61, y=14,
       sub="Startup · Founder",
       text=["A travel wallet that pays merchants abroad by scanning their own local QR codes. One balance in dollars, and the exchange rate is on the screen before you tap.",
             "A React web app, native iOS and Android apps from one Expo codebase, and a small Hono worker that sends every download link to the right store."],
       meta=[("Role", "Founder, web and mobile"), ("Built with", "React, Expo, Supabase, Solana, Cloudflare"), ("Platforms", "Web, iOS, Android")],
       previews=["img/p/valuto.webp", "img/p/valuto-app-mainpage.webp", "img/p/valuto-app-paymentpage.webp", "img/p/valuto-app-transferspage.webp"], link="https://getvaluto.com"),
  dict(id="anonympass", label="AnonymPass", icon="img/p/anonympass-icon.webp", x=73, y=27,
       sub="Startup · Founder",
       text=["A crypto payment gateway for merchants that card processors turn away. Funds land straight in the merchant's wallet on Tron or Solana and settle in under 30 seconds, for a flat 0.25% fee."],
       meta=[("Role", "Founder and engineering"), ("Chains", "Tron, Solana"), ("Fee", "0.25% flat")],
       previews=["img/p/anonympass.webp"], link="https://anonympass.com"),
  dict(id="digitalrocket", label="Digital Rocket", icon="img/p/digitalrocket-icon.webp", x=19, y=31,
       sub="Client · Website",
       text=["Website for an AI-native growth marketing agency in Dubai, blending SEO, AI search and performance media."],
       meta=[("Client", "Digital Rocket, Dubai"), ("Work", "Website design and build")],
       previews=["img/p/digitalrocket.webp"], link="https://digital-rocket.io"),
  dict(id="undrgoods", label="Undrgoods", icon="img/p/undrgoods-icon.webp", x=78, y=47,
       sub="Client · Online store",
       text=["Online store for an underwear and loungewear brand."],
       meta=[("Client", "Undrgoods"), ("Work", "E-commerce store")],
       previews=["img/p/undrgoods.webp"], link="https://undrgoods.com"),
  dict(id="missingstone", label="The Missing Stone", icon="img/p/missingstone-icon.webp", x=23, y=53,
       sub="Client · Online store",
       text=["Online store for a jewellery brand: collections, bangles, bracelets, earrings, necklaces and custom-made pieces."],
       meta=[("Client", "The Missing Stone"), ("Work", "E-commerce store")],
       previews=["img/p/missingstone.webp"], link="https://themissingstone.com"),
  dict(id="asiainsight", label="Asia Insight", icon="img/p/asiainsight-icon.webp", x=71, y=66,
       sub="Client · Website",
       text=["Website for a destination management company running tours to South-East Asia, in Azerbaijani."],
       meta=[("Client", "Asia Insight, Baku"), ("Work", "Website design and build")],
       previews=["img/p/asiainsight.webp"], link="https://asiainsight.az"),
  dict(id="harborfalcon", label="Harbor Falcon", icon="img/p/harborfalcon-icon.webp", x=33, y=71,
       sub="Client · Website",
       text=["Website for a US home-buying company: get a competitive cash offer for your house, with no agents and no open houses."],
       meta=[("Client", "Harbor Falcon, United States"), ("Work", "Website design and build")],
       previews=["img/p/harborfalcon.webp"], link="https://harborfalcon.com"),
  dict(id="course", label="Elementor course", icon=None, glyph="course", x=54, y=75,
       sub="Teaching · Udemy",
       text=["Elementor A'dan Z'ye: a web design course on Udemy, taught in Turkish. More than 2,600 students have taken it, and it is rated 4.5 out of 5."],
       meta=[("Students", "2,600+"), ("Rating", "4.5 / 5"), ("Language", "Turkish")],
       previews=[], link="https://www.udemy.com/course/elementor-a-dan-z-ye-ogren-elementorla-web-sitesi-tasarla/", linklabel="Open on Udemy"),
  dict(id="gevelopers", label="Gevelopers LLC", icon=None, glyph="folder", x=10, y=72,
       sub="Company · Since 2022",
       text=["My company. A remote team spread across the globe, building custom web and mobile apps and games for clients: from a startup MVP from scratch to scaling a product that already exists.",
             "Before Gevelopers I designed and built 200+ WordPress sites at ValisoyMedia, worked on the Kontakt Home WooCommerce store, and started out doing SEO at ELSEO in Baku."],
       meta=[("Registered", "Sheridan, Wyoming"), ("Team", "Remote, worldwide"), ("Builds", "Web, mobile, games")],
       previews=[], link="https://gevelopers.com"),
]

INSTAGRAM = [
  ("Da-sv5FjU8Q", 480, 640, "Vali sitting on the wall of a stone arch railway bridge in the jungle"),
  ("Dao3FkxjIPz", 480, 640, "Vali sitting on a rock at sunset, a tall flat-topped rock fortress behind him"),
  ("DbBUdZrDRDZ", 480, 640, "Vali smiling in an orange T-shirt with elephants grazing behind him"),
  ("DanaccyEt0s", 480, 640, "Vali walking in front of a huge white Buddhist stupa under blue sky"),
  ("DaskucZgLbs", 480, 640, "Three small fishing boats on green sea, seen from above"),
  ("Da2Lip5AD5I", 640, 480, "Vali looking out over green hills and valleys"),
  ("DbM28fDMc61", 360, 640, "Vali drinking from a fresh coconut"),
  ("DbIlprukiwd", 640, 360, "Close-up selfie of Vali on a beach"),
  ("Dd9kQJaxnXc", 360, 640, "A Formula 1 car racing through the streets of Baku, the Flame Towers behind"),
]

GLYPHS = {
  "folder": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M4 14a4 4 0 0 1 4-4h16l6 6h26a4 4 0 0 1 4 4v32a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z" fill="#5ac8fa"/><path d="M4 22h56v30a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z" fill="#7ad7ff"/><text x="32" y="46" text-anchor="middle" font-size="16" font-weight="800" fill="#0a6aa1" font-family="system-ui">G</text></svg>',
  "course": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#111"/><path d="M14 22 32 13l18 9-18 9z" fill="#fff"/><path d="M21 27v10c0 4 5 7 11 7s11-3 11-7V27l-11 5.5z" fill="#fff" opacity=".75"/><text x="32" y="56" text-anchor="middle" font-size="9" font-weight="800" fill="#fff" font-family="system-ui">2,600+</text></svg>',
  "readme": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 4h26l12 12v44H14z" fill="#fff"/><path d="M40 4v12h12" fill="#e5e5e5"/><g fill="#9a9a9a"><rect x="20" y="24" width="24" height="3"/><rect x="20" y="31" width="20" height="3"/><rect x="20" y="38" width="24" height="3"/><rect x="20" y="45" width="14" height="3"/></g><text x="32" y="17" text-anchor="middle" font-size="8" font-weight="800" fill="#111" font-family="system-ui">MD</text></svg>',
}

# dock / app icons (macOS-like squircles drawn in SVG)
APPS = {
  "terminal": ('Terminal', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1d1d1f"/><rect x="2" y="2" width="60" height="60" rx="12" fill="#2b2b2d"/><path d="M15 22l11 9-11 9" fill="none" stroke="#e6e6e6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="30" y="38" width="17" height="4.5" rx="2" fill="#e6e6e6"/></svg>'),
  "code": ('Code', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#0f6fc6"/><path d="M24 20 12 32l12 12M40 20l12 12-12 12" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M35 16 29 48" stroke="#9fd0ff" stroke-width="4" stroke-linecap="round"/></svg>'),
  "warning": ('Problems', '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6 61 56H3z" fill="#ffcc00" stroke="#e0a800" stroke-width="2" stroke-linejoin="round"/><rect x="29" y="22" width="6" height="20" rx="3" fill="#1d1d1f"/><circle cx="32" cy="48" r="3.6" fill="#1d1d1f"/></svg>'),
  "notes": ('Notes', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#fff"/><path d="M0 14A14 14 0 0 1 14 0h36a14 14 0 0 1 14 14v6H0z" fill="#ffd52e"/><g stroke="#d6d6d6" stroke-width="2"><path d="M8 32h48M8 42h48M8 52h48"/></g><g fill="#c9c9c9"><circle cx="20" cy="20" r="0"/></g></svg>'),
  "photos": ('Photos', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#fff"/><g transform="translate(32 32)"><g opacity=".9"><ellipse rx="7" ry="12" cy="-11" fill="#f9b233"/><ellipse rx="7" ry="12" cy="-11" fill="#f39c12" transform="rotate(45)"/><ellipse rx="7" ry="12" cy="-11" fill="#e74c3c" transform="rotate(90)"/><ellipse rx="7" ry="12" cy="-11" fill="#c0398b" transform="rotate(135)"/><ellipse rx="7" ry="12" cy="-11" fill="#8e44ad" transform="rotate(180)"/><ellipse rx="7" ry="12" cy="-11" fill="#3498db" transform="rotate(225)"/><ellipse rx="7" ry="12" cy="-11" fill="#1abc9c" transform="rotate(270)"/><ellipse rx="7" ry="12" cy="-11" fill="#7ac943" transform="rotate(315)"/></g></g></svg>'),
  "instagram": ('Instagram', '<svg viewBox="0 0 64 64" aria-hidden="true"><defs><radialGradient id="ig" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/><stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs><rect width="64" height="64" rx="14" fill="url(#ig)"/><rect x="14" y="14" width="36" height="36" rx="11" fill="none" stroke="#fff" stroke-width="4"/><circle cx="32" cy="32" r="8.5" fill="none" stroke="#fff" stroke-width="4"/><circle cx="42.5" cy="21.5" r="2.6" fill="#fff"/></svg>'),
  "github": ('GitHub', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#fff"/><path transform="translate(12 12) scale(1.667)" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.4 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8 0 3.2.9.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.5.4.9 1 .9 2.2v3.3c0 .3.1.7.8.6A12 12 0 0 0 12 .3" fill="#111"/></svg>'),
  "telegram": ('Telegram', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#2aabee"/><path d="M13 31.5 47 18.4c1.6-.6 3 .4 2.5 2.8l-5.8 27.3c-.4 1.9-1.6 2.4-3.2 1.5l-8.8-6.5-4.2 4.1c-.5.5-.9.9-1.8.9l.6-9 16.4-14.8c.7-.6-.2-1-1.1-.4L22 37.1l-8.7-2.7c-1.9-.6-1.9-1.9.4-2.9z" fill="#fff"/></svg>'),
  "mail": ('Mail', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1e88f5"/><rect x="10" y="18" width="44" height="30" rx="4" fill="#fff"/><path d="M11 20l21 15 21-15" fill="none" stroke="#1e88f5" stroke-width="3" stroke-linejoin="round"/></svg>'),
  "trash": ('Trash', '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 18h36l-3 40a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4z" fill="#e9e9ec" stroke="#bdbdc2" stroke-width="2"/><rect x="11" y="12" width="42" height="7" rx="3.5" fill="#d4d4d8"/><g stroke="#bdbdc2" stroke-width="2"><path d="M24 24l1 32M32 24v32M40 24l-1 32"/></g></svg>'),
}

def icon_html(p, cls="icon"):
    if p.get("icon"):
        img = f'<img src="{p["icon"]}" width="320" height="320" alt="" draggable="false">'
    else:
        img = GLYPHS[p["glyph"]]
    return img

def project_window(p):
    paras = "".join(f"<p>{E(t)}</p>" for t in p["text"])
    meta = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in p["meta"])
    prev = ""
    if p["previews"]:
        imgs = []
        for i, src in enumerate(p["previews"]):
            phone = "app-" in src
            w, h = (540, 1200) if phone else (1200, 750)
            alt = f'{p["label"]} app screen' if phone else f'Homepage of {p["label"]}'
            imgs.append(f'<img class="{"shot shot--phone" if phone else "shot"}" src="{src}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">')
        prev = f'<details class="preview" open><summary>Preview:</summary><div class="preview__body">{"".join(imgs)}</div></details>'
    head_icon = icon_html(p)
    return f'''
<section class="win win--info" id="w-{p["id"]}" role="dialog" aria-labelledby="w-{p["id"]}-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-{p["id"]}-t"><span class="win__pre">Information about: </span>{E(p["label"])}</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body">
    <div class="info__head"><span class="info__icon">{head_icon}</span><div><h3>{E(p["label"])}</h3><p>{E(p["sub"])}</p></div></div>
    <div class="info__text">{paras}</div>
    <dl class="info__meta">{meta}</dl>
    {prev}
    <a class="mac-button" href="{p["link"]}" target="_blank" rel="noopener">{E(p.get("linklabel", "Open " + p["link"].split("//")[1].split("/")[0]))} ↗</a>
  </div>
</section>'''

def desktop_icon(p):
    return f'<a class="icon" href="#w-{p["id"]}" data-open="w-{p["id"]}" style="--x:{p["x"]}%;--y:{p["y"]}%"><span class="icon__img">{icon_html(p)}</span><span class="icon__label">{E(p["label"])}</span></a>'

def app_icon(key, target, href=None, extra=""):
    label, svg = APPS[key]
    if href:
        return f'<a class="app" href="{href}" target="_blank" rel="noopener" aria-label="{label}"{extra}><span class="app__img">{svg}</span><span class="app__label">{label}</span></a>'
    return f'<a class="app" href="#{target}" data-open="{target}" aria-label="{label}"{extra}><span class="app__img">{svg}</span><span class="app__label">{label}</span></a>'

gallery = "".join(
    f'<a class="photo" href="https://www.instagram.com/p/{pid}/" data-photo="{i}" target="_blank" rel="noopener"><img src="img/ig/{pid}.webp" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy"></a>'
    for i, (pid, w, h, alt) in enumerate(INSTAGRAM))

readme_icon = dict(id="about", label="README.md", glyph="readme", x=84, y=12)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Vali Valiyev — Software engineer</title>
<meta name="description" content="Vali Valiyev (vvalisoy) is a software engineer and digital nomad from Azerbaijan, founder of Gevelopers LLC and builder of TiketVisa, UnliSIM, Valuto and AnonymPass.">
<meta name="theme-color" content="#d9d9d9">
<link rel="canonical" href="https://vvalisoy.github.io/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://vvalisoy.github.io/">
<meta property="og:title" content="Vali Valiyev — Software engineer">
<meta property="og:description" content="Travel products and websites, built from wherever the Wi-Fi holds.">
<meta property="og:image" content="https://vvalisoy.github.io/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"Vali Valiyev","alternateName":"vvalisoy","url":"https://vvalisoy.github.io/","jobTitle":"Software engineer","worksFor":{{"@type":"Organization","name":"Gevelopers LLC","url":"https://gevelopers.com"}},"sameAs":["https://github.com/vvalisoy","https://substack.com/@vvalisoy","https://instagram.com/vvalisoy","https://t.me/vvalisoy","https://www.facebook.com/vvalisoy","https://linktr.ee/vvalisoy"]}}
</script>
</head>
<body>

<div class="wallpaper" aria-hidden="true"><img src="img/vali.webp" width="1000" height="1000" alt=""></div>

<header class="menubar">
  <div class="menubar__left">
    <a class="menubar__logo" href="#w-about" data-open="w-about" aria-label="About Vali">V</a>
    <a class="menubar__app" href="#w-about" data-open="w-about">Vali Valiyev</a>
    <a href="#w-terminal" data-open="w-terminal">Terminal</a>
    <a href="#w-photos" data-open="w-photos">Gallery</a>
    <a href="#w-mail" data-open="w-mail">Contact</a>
  </div>
  <div class="menubar__right">
    <span class="status-icons" aria-hidden="true">
      <svg viewBox="0 0 18 12" width="18" height="12"><g fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></g></svg>
      <svg viewBox="0 0 16 12" width="16" height="12"><path d="M8 11.5 5.6 9a3.4 3.4 0 0 1 4.8 0zM3.5 6.9a6.4 6.4 0 0 1 9 0l1.5-1.5a8.5 8.5 0 0 0-12 0zM.6 4a10.6 10.6 0 0 1 14.8 0L16.9 2.5a12.7 12.7 0 0 0-17.8 0z" fill="currentColor"/></svg>
      <svg viewBox="0 0 27 12" width="27" height="12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="currentColor" opacity=".45"/><rect x="2" y="2" width="16" height="8" rx="1.6" fill="currentColor"/><rect x="24" y="4" width="2" height="4" rx="1" fill="currentColor" opacity=".45"/></svg>
    </span>
    <span class="clock" data-clock data-tz="Asia/Baku"><span class="clock__city">Baku</span> <span data-clock-time>GMT+4</span></span>
  </div>
</header>

<main class="desktop" id="desktop">
  <h1 class="sr">Vali Valiyev, software engineer</h1>
  <section class="widget" aria-label="Vali Valiyev">
    <p class="widget__name">Vali Valiyev</p>
    <p class="widget__role">Software engineer · Founder of Gevelopers</p>
    <p class="widget__time"><span data-clock-big>--:--</span> in Baku</p>
  </section>
  <div class="icons">
    {''.join(desktop_icon(p) for p in PROJECTS)}
    {desktop_icon(readme_icon)}
  </div>
  <div class="phone-apps">
    {app_icon("terminal", "w-terminal")}
    {app_icon("code", "w-code")}
    {app_icon("warning", "w-error")}
    {app_icon("github", None, "https://github.com/vvalisoy")}
    {app_icon("telegram", None, "https://t.me/vvalisoy")}
    {app_icon("trash", "w-trash")}
  </div>
  <p class="hint">Click an icon to open it.</p>
</main>

<nav class="dock" aria-label="Dock">
  <div class="dock__group dock__group--mac">
    {app_icon("terminal", "w-terminal")}
    {app_icon("code", "w-code")}
    {app_icon("warning", "w-error")}
  </div>
  <span class="dock__sep dock__sep--mac" aria-hidden="true"></span>
  <div class="dock__group">
    {app_icon("notes", "w-about")}
    {app_icon("photos", "w-photos")}
    {app_icon("instagram", None, "https://instagram.com/vvalisoy")}
    {app_icon("mail", "w-mail")}
  </div>
  <span class="dock__sep dock__sep--mac" aria-hidden="true"></span>
  <div class="dock__group dock__group--mac">
    {app_icon("github", None, "https://github.com/vvalisoy")}
    {app_icon("telegram", None, "https://t.me/vvalisoy")}
    {app_icon("trash", "w-trash")}
  </div>
</nav>

<div class="windows">
{''.join(project_window(p) for p in PROJECTS)}

<section class="win win--notes" id="w-about" role="dialog" aria-labelledby="w-about-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-about-t"><span class="win__pre">Information about: </span>Vali Valiyev, vali@gevelopers.com</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body notes">
    <nav class="notes__side" aria-label="Notes">
      <a href="#note-about" data-note="note-about" aria-current="true"><span>About me</span><span>11</span></a>
      <a href="#note-cv" data-note="note-cv"><span>Experience</span><span>4</span></a>
      <a href="#note-skills" data-note="note-skills"><span>Skills</span><span>12</span></a>
      <a href="#note-school" data-note="note-school"><span>Education</span><span>2</span></a>
      <a href="#note-life" data-note="note-life"><span>Interests</span><span>∞</span></a>
    </nav>
    <div class="notes__main">
      <article class="note" id="note-about">
        <p class="note__date">Baku · Sumgait · wherever the Wi-Fi holds</p>
        <p>Software engineer, digital nomad and founder of Gevelopers LLC. I trained as a pharmacist in Baku and became a developer instead.</p>
        <p>That was 2015, doing SEO at ELSEO. Then the Kontakt Home WooCommerce store, then four years and 200+ WordPress sites at ValisoyMedia. Since 2022 I run Gevelopers, a remote team building web and mobile apps, and my own travel products from whichever city I am in that month.</p>
        <p>I can build…</p>
        <ul class="checks">
          <li>Travel products people use at a border</li>
          <li>Web apps (React, Next.js, Vite)</li>
          <li>Mobile apps for iOS and Android (Expo)</li>
          <li>Payments: cards, QR, crypto on Solana and Tron</li>
          <li>Backends on Cloudflare Workers and Supabase</li>
          <li>WordPress and WooCommerce, any theme, any builder</li>
          <li>Online stores (WooCommerce, Shopify, OpenCart)</li>
          <li>Sites in 18 languages</li>
          <li>SEO that ranks</li>
          <li>Automations (n8n)</li>
          <li>An Elementor course with 2,600+ students</li>
        </ul>
      </article>
      <article class="note" id="note-cv">
        <p class="note__date">Experience</p>
        <ul class="rows">
          <li><span><b>Gevelopers LLC</b> Software developer, founder · Sheridan, WY (remote)</span><span>2022–now</span></li>
          <li><span><b>ValisoyMedia</b> WordPress developer · Houston, TX (remote). 200+ sites, 100+ themes, custom plugins, Figma and Adobe XD to WordPress, Shopify and OpenCart stores</span><span>2018–22</span></li>
          <li><span><b>Kontakt Home</b> WordPress developer · Baku. Bug fixes and product sections for kontakt.az, in an 85-person team</span><span>2016–18</span></li>
          <li><span><b>ELSEO</b> WordPress developer · Baku. On-page and technical SEO</span><span>2015–16</span></li>
        </ul>
      </article>
      <article class="note" id="note-skills">
        <p class="note__date">Skills</p>
        <ul class="tags">
          <li>JavaScript</li><li>TypeScript</li><li>React</li><li>Next.js</li><li>React Native / Expo</li><li>PHP</li><li>MySQL</li><li>WordPress</li><li>WooCommerce</li><li>Cloudflare Workers</li><li>Supabase</li><li>Solana</li><li>Stripe</li><li>Shopify</li><li>REST APIs</li><li>Git</li><li>SEO</li><li>Elementor</li><li>n8n</li>
        </ul>
      </article>
      <article class="note" id="note-school">
        <p class="note__date">Education</p>
        <ul class="rows">
          <li><span><b>University of Wisconsin–Milwaukee</b> Computer Science, master's</span><span>2021–22</span></li>
          <li><span><b>Azerbaijan Medical University</b> Bachelor of Pharmacy</span><span>2013–17</span></li>
        </ul>
        <p>Languages: Azerbaijani (native), Turkish (C2), English (B2).</p>
      </article>
      <article class="note" id="note-life">
        <p class="note__date">Interests</p>
        <p>Travel, mostly, and usually with a laptop. The Photos app has some of it; Instagram has the rest.</p>
        <p>Writing on Substack, teaching web design in Turkish, and building the tools I wished existed at the last border I crossed.</p>
        <p><a href="https://substack.com/@vvalisoy" target="_blank" rel="noopener">Substack ↗</a> · <a href="https://instagram.com/vvalisoy" target="_blank" rel="noopener">Instagram ↗</a> · <a href="https://www.facebook.com/vvalisoy" target="_blank" rel="noopener">Facebook ↗</a></p>
      </article>
    </div>
  </div>
</section>

<section class="win win--photos" id="w-photos" role="dialog" aria-labelledby="w-photos-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-photos-t"><span class="win__pre">Information about: </span>Gallery</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body">
    <div class="info__head"><span class="info__icon">{APPS["photos"][1]}</span><div><h3>Gallery</h3><p>Lately, from @vvalisoy</p></div></div>
    <div class="gallery">{gallery}</div>
    <div class="viewer" hidden><img alt=""><div class="viewer__bar"><button type="button" data-step="-1" aria-label="Previous photo">‹</button><a target="_blank" rel="noopener">View on Instagram ↗</a><button type="button" data-step="1" aria-label="Next photo">›</button></div></div>
    <a class="mac-button" href="https://instagram.com/vvalisoy" target="_blank" rel="noopener">More on Instagram ↗</a>
  </div>
</section>

<section class="win win--terminal" id="w-terminal" role="dialog" aria-labelledby="w-terminal-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-terminal-t">vali — zsh — 80×24</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body term" data-term>
    <pre class="term__out" aria-live="polite">Last login: <span data-login></span> on ttys001
Type <b>help</b> to see what this terminal can do.
</pre>
    <form class="term__line"><label for="term-in"><span class="term__ps">vali@macbook ~ %</span></label><input id="term-in" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="send"></form>
  </div>
</section>

<section class="win win--code" id="w-code" role="dialog" aria-labelledby="w-code-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-code-t">vali.ts — vvalisoy</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body code"><pre><code><span class="c">// Hi. This is me, typed.</span>
<span class="k">export const</span> <span class="v">vali</span> = {{
  name: <span class="s">"Vali Valiyev"</span>,
  handle: <span class="s">"@vvalisoy"</span>,
  from: <span class="s">"Sumgait, Azerbaijan"</span>,
  basedIn: <span class="s">"Baku, mostly"</span>,
  role: <span class="s">"Software engineer"</span>,
  company: <span class="s">"Gevelopers LLC"</span>,
  shipping: [<span class="s">"TiketVisa"</span>, <span class="s">"UnliSIM"</span>, <span class="s">"Valuto"</span>, <span class="s">"AnonymPass"</span>],
  stack: [<span class="s">"TypeScript"</span>, <span class="s">"React"</span>, <span class="s">"Next.js"</span>, <span class="s">"Expo"</span>,
          <span class="s">"Cloudflare Workers"</span>, <span class="s">"Supabase"</span>, <span class="s">"PHP"</span>, <span class="s">"WordPress"</span>],
  wordpressSitesBuilt: <span class="n">200</span>,
  udemyStudents: <span class="n">2600</span>,
  speaks: [<span class="s">"az"</span>, <span class="s">"tr"</span>, <span class="s">"en"</span>],
  availableForWork: <span class="k">true</span>,
}};

<span class="k">export function</span> <span class="f">hire</span>(project: <span class="t">string</span>) {{
  <span class="k">return</span> <span class="f">fetch</span>(<span class="s">"mailto:vali@gevelopers.com"</span>, {{ body: project }});
}}</code></pre></div>
</section>

<section class="win win--mail" id="w-mail" role="dialog" aria-labelledby="w-mail-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-mail-t">New Message</h2><a class="win__done" href="#">Done</a></header>
  <form class="win__body mail" data-mail action="mailto:vali@gevelopers.com" method="get" enctype="text/plain">
    <div class="mail__row"><span>To:</span><span class="mail__to">Vali Valiyev &lt;vali@gevelopers.com&gt;</span></div>
    <label class="mail__row"><span>Subject:</span><input name="subject" value="Hello Vali" autocomplete="off"></label>
    <textarea name="body" rows="8" aria-label="Message" placeholder="What are we building?"></textarea>
    <div class="mail__foot">
      <span class="mail__alt">Or <a href="https://t.me/vvalisoy" target="_blank" rel="noopener">Telegram @vvalisoy</a></span>
      <button class="mac-button mac-button--blue" type="submit">Send</button>
    </div>
  </form>
</section>

<section class="win win--trash" id="w-trash" role="dialog" aria-labelledby="w-trash-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-trash-t">Trash</h2><a class="win__done" href="#">Done</a></header>
  <div class="win__body">
    <table class="finder">
      <thead><tr><th>Name</th><th>Size</th><th>Date</th></tr></thead>
      <tbody>
        <tr><td>wordpress-site-FINAL-final-v7.zip</td><td>212 MB</td><td>2019</td></tr>
        <tr><td>node_modules</td><td>2.4 GB</td><td>Yesterday</td></tr>
        <tr><td>jquery-1.4.2.min.js</td><td>71 KB</td><td>2016</td></tr>
        <tr><td>pharmacology-notes.pdf</td><td>18 MB</td><td>2017</td></tr>
        <tr><td>startup-idea-#47.txt</td><td>2 KB</td><td>Today</td></tr>
        <tr><td>roaming-bill-before-unlisim.pdf</td><td>340 KB</td><td>2023</td></tr>
      </tbody>
    </table>
    <p class="finder__foot">6 items. Emptying the trash is turned off on this Mac.</p>
  </div>
</section>

<section class="win win--alert" id="w-error" role="alertdialog" aria-labelledby="w-error-t" aria-describedby="w-error-d">
  <header class="win__bar"><h2 class="win__title" id="w-error-t">Build error</h2></header>
  <div class="win__body alert">
    {APPS["warning"][1]}
    <p id="w-error-d">Vali started another startup before the last one finished deploying. Shame there is no undo for ideas.</p>
    <a class="mac-button mac-button--blue" href="#">Ship it anyway</a>
  </div>
</section>
</div>

<script src="main.js" defer></script>
</body>
</html>
'''
open(OUT, "w").write(page)
print("ok", len(page))
