#!/usr/bin/env python3
"""Generates index.html (python3 build.py index.html) for the macOS / iOS style personal site (run once; the output is plain HTML)."""
import html, sys

OUT = sys.argv[1]
E = html.escape

# id, label, icon, x%, y%, title, subtitle, paragraphs, meta rows, previews, link
PROJECTS = [
  dict(id="tiketvisa", label="TiketVisa", x=30, y=12,
       sub="Startup · Founder",
       text=["Onward flight reservations and hotel bookings with a real PNR, for travellers who have to show a ticket out at the embassy or the airport.",
             "I moved the site off WordPress to a static Next.js build in 18 languages, with Cloudflare Workers routing between the new pages and the blog, handling forms and serving images."],
       meta=[("Role", "Founder, product and engineering"), ("Built with", "Next.js, Cloudflare Workers, WordPress"), ("Languages", "18")],
       previews=["img/m/tiketvisa.webp"], link="https://tiketvisa.com"),
  dict(id="unlisim", label="UnliSIM", x=44, y=7,
       sub="Startup · Founder",
       text=["Travel eSIMs for 200+ destinations. Pick a country and the number of days, pay with Apple Pay, Google Pay or card, and the phone is online in about two minutes. No roaming bill, no SIM swap."],
       meta=[("Role", "Founder and engineering"), ("Built with", "Next.js on Cloudflare (OpenNext)"), ("Coverage", "200+ destinations")],
       previews=["img/m/unlisim.webp"], link="https://unlisim.com"),
  dict(id="valuto", label="Valuto", x=58, y=10,
       sub="Startup · Founder",
       text=["A travel wallet that pays merchants abroad by scanning their own local QR codes. One balance in dollars, and the exchange rate is on the screen before you tap.",
             "A React web app, native iOS and Android apps from one Expo codebase, and a small Hono worker that sends every download link to the right store."],
       meta=[("Role", "Founder, web and mobile"), ("Built with", "React, Expo, Supabase, Solana, Cloudflare"), ("Platforms", "Web, iOS, Android")],
       previews=["img/m/valuto.webp", "img/p/valuto-app-mainpage.webp", "img/p/valuto-app-paymentpage.webp"], link="https://getvaluto.com"),
  dict(id="anonympass", label="AnonymPass", x=71, y=20,
       sub="Startup · Founder",
       text=["A crypto payment gateway for merchants that card processors turn away. Funds land straight in the merchant's wallet on Tron or Solana and settle in under 30 seconds, for a flat 0.25% fee."],
       meta=[("Role", "Founder and engineering"), ("Chains", "Tron, Solana"), ("Fee", "0.25% flat")],
       previews=["img/m/anonympass.webp"], link="https://anonympass.com"),
  dict(id="digitalrocket", label="Digital Rocket", x=20, y=30,
       sub="Client · Website",
       text=["Website for an AI-native growth marketing agency in Dubai, blending SEO, AI search and performance media."],
       meta=[("Client", "Digital Rocket, Dubai"), ("Work", "Website design and build")],
       previews=["img/m/digitalrocket.webp"], link="https://digital-rocket.io"),
  dict(id="undrgoods", label="Undrgoods", x=78, y=44,
       sub="Client · Online store",
       text=["Online store for an underwear and loungewear brand."],
       meta=[("Client", "Undrgoods"), ("Work", "E-commerce store")],
       previews=["img/m/undrgoods.webp"], link="https://undrgoods.com"),
  dict(id="missingstone", label="The Missing Stone", x=22, y=52,
       sub="Client · Online store",
       text=["Online store for a jewellery brand: collections, bangles, bracelets, earrings, necklaces and custom-made pieces."],
       meta=[("Client", "The Missing Stone"), ("Work", "E-commerce store")],
       previews=["img/m/missingstone.webp"], link="https://themissingstone.com"),
  dict(id="asiainsight", label="Asia Insight", x=72, y=64,
       sub="Client · Website",
       text=["Website for a destination management company running tours to South-East Asia, in Azerbaijani."],
       meta=[("Client", "Asia Insight, Baku"), ("Work", "Website design and build")],
       previews=["img/m/asiainsight.webp"], link="https://asiainsight.az"),
  dict(id="harborfalcon", label="Harbor Falcon", x=33, y=70,
       sub="Client · Website",
       text=["Website for a US home-buying company: get a competitive cash offer for your house, with no agents and no open houses."],
       meta=[("Client", "Harbor Falcon, United States"), ("Work", "Website design and build")],
       previews=["img/m/harborfalcon.webp"], link="https://harborfalcon.com"),
  dict(id="travelsolotiket", label="TravelSoloTiket", x=86, y=30,
       sub="Client · Website",
       text=["Verified flight and hotel reservations in under 60 seconds: onward or return flight reservations and hotel bookings for visa applications, airline check-in and border control."],
       meta=[("Client", "TravelSoloTiket"), ("Work", "Website design and build")],
       previews=["img/m/travelsolotiket.webp"], link="https://travelsolotiket.com"),
  dict(id="course", label="Elementor course", glyph="course", x=55, y=74,
       sub="Teaching · Udemy",
       text=["Elementor A'dan Z'ye: a web design course on Udemy, taught in Turkish. More than 2,600 students have taken it, and it is rated 4.5 out of 5."],
       meta=[("Students", "2,600+"), ("Rating", "4.5 / 5"), ("Language", "Turkish")],
       previews=[], link="https://www.udemy.com/course/elementor-a-dan-z-ye-ogren-elementorla-web-sitesi-tasarla/", linklabel="Open on Udemy"),
  dict(id="gevelopers", label="Gevelopers LLC", x=10, y=72,
       sub="Company · Since 2022",
       text=["My company. A remote team spread across the globe, building custom web and mobile apps and games for clients: from a startup MVP from scratch to scaling a product that already exists.",
             "Before Gevelopers I designed and built 200+ WordPress sites at ValisoyMedia, worked on the Kontakt Home WooCommerce store, and started out doing SEO at ELSEO in Baku."],
       meta=[("Registered", "Sheridan, Wyoming"), ("Team", "Remote, worldwide"), ("Builds", "Web, mobile, games")],
       previews=["img/m/gevelopers.webp"], link="https://gevelopers.com"),
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
  "terminal": ('Terminal', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-term)"/><rect x="0.75" y="0.75" width="62.5" height="62.5" rx="13.6" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="1.5"/><path d="M15 22.5 26 31l-11 8.5" fill="none" stroke="#fff" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="30" y="38" width="17" height="4.6" rx="2.3" fill="#fff"/></svg>'),
  "warning": ('Problems', '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M27.7 8.6a5 5 0 0 1 8.6 0l24.4 42.3a5 5 0 0 1-4.3 7.5H7.6a5 5 0 0 1-4.3-7.5z" fill="url(#g-warn)"/><path d="M27.7 8.6a5 5 0 0 1 8.6 0l24.4 42.3a5 5 0 0 1-4.3 7.5H7.6a5 5 0 0 1-4.3-7.5z" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.2"/><rect x="29" y="21" width="6" height="21" rx="3" fill="#1d1d1f"/><circle cx="32" cy="49" r="3.6" fill="#1d1d1f"/></svg>'),
  "notes": ('Notes', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-paper)"/><path d="M0 14.3A14.3 14.3 0 0 1 14.3 0h35.4A14.3 14.3 0 0 1 64 14.3V19H0z" fill="url(#g-notes)"/><g stroke="#d9d9de" stroke-width="1.6"><path d="M9 31h46M9 40h46M9 49h46"/></g><g fill="#c2c2c7"><circle cx="9.5" cy="10" r="0"/></g><path d="M0 19h64" stroke="#000" stroke-opacity=".06"/></svg>'),
  "photos": ('Photos', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-paper)"/><g transform="translate(32 32)" style="mix-blend-mode:multiply"><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#fbb034" opacity=".92"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#f57c22" opacity=".9" transform="rotate(45)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#ec3d55" opacity=".9" transform="rotate(90)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#c93ea0" opacity=".9" transform="rotate(135)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#7d4fd8" opacity=".9" transform="rotate(180)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#3d8af0" opacity=".9" transform="rotate(225)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#2ec4b6" opacity=".9" transform="rotate(270)"/><ellipse rx="7.2" ry="12.5" cy="-11.5" fill="#8bd346" opacity=".9" transform="rotate(315)"/></g></svg>'),
  "instagram": ('Instagram', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-ig)"/><rect x="14" y="14" width="36" height="36" rx="11" fill="none" stroke="#fff" stroke-width="4"/><circle cx="32" cy="32" r="8.5" fill="none" stroke="#fff" stroke-width="4"/><circle cx="42.5" cy="21.5" r="2.6" fill="#fff"/></svg>'),
  "github": ('GitHub', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-dark)"/><path transform="translate(12 12) scale(1.667)" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.4 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8 0 3.2.9.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.5.4.9 1 .9 2.2v3.3c0 .3.1.7.8.6A12 12 0 0 0 12 .3" fill="#fff"/></svg>'),
  "telegram": ('Telegram', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-tg)"/><path d="M13 31.5 47 18.4c1.6-.6 3 .4 2.5 2.8l-5.8 27.3c-.4 1.9-1.6 2.4-3.2 1.5l-8.8-6.5-4.2 4.1c-.5.5-.9.9-1.8.9l.6-9 16.4-14.8c.7-.6-.2-1-1.1-.4L22 37.1l-8.7-2.7c-1.9-.6-1.9-1.9.4-2.9z" fill="#fff"/></svg>'),
  "mail": ('Mail', '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14.3" fill="url(#g-mail)"/><rect x="10" y="17" width="44" height="31" rx="5" fill="url(#g-env)"/><path d="M11.5 19.5 32 34.5l20.5-15" fill="none" stroke="#2f8cf0" stroke-opacity=".55" stroke-width="2.4" stroke-linejoin="round"/></svg>'),
  "trash": ('Trash', '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M13.5 17h37l-3.2 40.5a4.5 4.5 0 0 1-4.5 4.1H21.2a4.5 4.5 0 0 1-4.5-4.1z" fill="url(#g-trash)" stroke="#fff" stroke-opacity=".8" stroke-width="1.2"/><g stroke="#8e8e93" stroke-opacity=".55" stroke-width="1.4"><path d="M22 22l1.6 34M28 22l.6 34M36 22l-.6 34M42 22l-1.6 34"/></g><ellipse cx="32" cy="16.5" rx="20" ry="4" fill="#e5e5ea" stroke="#fff" stroke-width="1.2"/></svg>'),
}

# favicon file, tile colour, inner padding (as a share of the tile)
FAV = {
  "tiketvisa": ("img/fav/tiketvisa.svg", "#ffffff", 0.16),
  "unlisim": ("img/fav/unlisim.svg", "#ffffff", 0.16),
  "valuto": ("img/fav/valuto.webp", "#f15a29", 0),
  "anonympass": ("img/fav/anonympass.svg", "#ffffff", 0.2),
  "digitalrocket": ("img/fav/digitalrocket.webp", "#000000", 0),
  "undrgoods": ("img/fav/undrgoods.webp", "#1b2a4e", 0),
  "missingstone": ("img/fav/missingstone.svg", "#f6efe6", 0.24),
  "asiainsight": ("img/fav/asiainsight.svg", "#ffffff", 0.14),
  "harborfalcon": ("img/fav/harborfalcon.svg", "#ffffff", 0.16),
  "travelsolotiket": ("img/fav/travelsolotiket.svg", "#ffffff", 0.16),
  "gevelopers": ("img/fav/gevelopers.svg", "#ffffff", 0),
}

def icon_html(p):
    if p["id"] in FAV:
        src, bg, pad = FAV[p["id"]]
        return f'<span class="tile" style="--tile:{bg};--pad:{pad * 100:.0f}%"><img src="{src}" width="128" height="128" alt="" draggable="false"></span>'
    return f'<span class="tile tile--glyph">{GLYPHS[p["glyph"]]}</span>' 

def project_window(p):
    paras = "".join(f"<p>{E(t)}</p>" for t in p["text"])
    meta = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in p["meta"])
    prev = ""
    if p["previews"]:
        imgs = []
        for i, src in enumerate(p["previews"]):
            app = "app-" in src
            w, h = (540, 1200) if app else (540, 1169)
            alt = f'{p["label"]} app screen' if app else f'{p["label"]} on a phone'
            imgs.append(f'<img class="shot" src="{src}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">')
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
<script>document.documentElement.classList.add('js');if(navigator.userAgentData&&navigator.userAgentData.brands.some(function(b){{return /Chromium/.test(b.brand)}}))document.documentElement.classList.add('refract')</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"Vali Valiyev","alternateName":"vvalisoy","url":"https://vvalisoy.github.io/","jobTitle":"Software engineer","worksFor":{{"@type":"Organization","name":"Gevelopers LLC","url":"https://gevelopers.com"}},"sameAs":["https://github.com/vvalisoy","https://substack.com/@vvalisoy","https://instagram.com/vvalisoy","https://t.me/vvalisoy","https://www.facebook.com/vvalisoy","https://linktr.ee/vvalisoy"]}}
</script>
</head>
<body>

<svg class="sr" width="0" height="0" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="g-term" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a4e"/><stop offset=".55" stop-color="#1c1c1e"/><stop offset="1" stop-color="#000"/></linearGradient>
    <linearGradient id="g-paper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ececf0"/></linearGradient>
    <linearGradient id="g-notes" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe26a"/><stop offset="1" stop-color="#ffc800"/></linearGradient>
    <linearGradient id="g-mail" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6ad1ff"/><stop offset="1" stop-color="#0a6cf5"/></linearGradient>
    <linearGradient id="g-env" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e3eefc"/></linearGradient>
    <linearGradient id="g-tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fc3fb"/><stop offset="1" stop-color="#1287d6"/></linearGradient>
    <linearGradient id="g-dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a3c"/><stop offset="1" stop-color="#0d0d0f"/></linearGradient>
    <linearGradient id="g-warn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe066"/><stop offset="1" stop-color="#ffb800"/></linearGradient>
    <linearGradient id="g-trash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f7f9" stop-opacity=".95"/><stop offset="1" stop-color="#c7c7cc" stop-opacity=".85"/></linearGradient>
    <radialGradient id="g-ig" cx="30%" cy="107%" r="150%"><stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/><stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285aeb"/></radialGradient>
  </defs>
  <filter id="lg-refract" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.011 0.011" numOctaves="1" seed="7" result="noise"/>
    <feGaussianBlur in="noise" stdDeviation="2.5" result="map"/>
    <feDisplacementMap in="SourceGraphic" in2="map" scale="26" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>

<div class="wallpaper" aria-hidden="true"><img src="img/vali.webp" width="1000" height="1000" alt=""></div>

<header class="menubar">
  <div class="menubar__left">
    <a class="menubar__logo" href="#w-about" data-open="w-about" aria-label="About Vali">V</a>
    <a class="menubar__app" href="#w-about" data-open="w-about">Vali Valiyev</a>
    <a href="#w-terminal" data-open="w-terminal">Terminal</a>
    <a href="#w-photos" data-open="w-photos">Gallery</a>
    <a href="#w-mail" data-open="w-mail">Contact</a>
    <a href="#desktop" class="menubar__cleanup" data-cleanup>Clean Up</a>
  </div>
  <div class="menubar__right">
    <span class="status-icons" aria-hidden="true">
      <svg viewBox="0 0 18 12" width="18" height="12"><g fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></g></svg>
      <svg viewBox="0 0 17 12" width="17" height="12"><g fill="currentColor"><path d="M8.5 11.6 6.1 9.2a3.4 3.4 0 0 1 4.8 0z"/><path d="M3.9 7l1.4 1.4a4.5 4.5 0 0 1 6.4 0L13.1 7a6.5 6.5 0 0 0-9.2 0z"/><path d="M1.1 4.2l1.4 1.4a8.5 8.5 0 0 1 12 0l1.4-1.4a10.5 10.5 0 0 0-14.8 0z"/></g></svg>
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
        <p>Travel, mostly, and usually with a laptop. 32 countries so far:</p>
        <p class="flags" aria-label="Azerbaijan, Georgia, Iran, Turkey, Ukraine, Moldova, Serbia, Montenegro, Albania, North Macedonia, United States, Qatar, Malaysia, Indonesia, Philippines, United Arab Emirates, Laos, Cambodia, Vietnam, Singapore, Tajikistan, Uzbekistan, Kyrgyzstan, Kazakhstan, Japan, Taiwan, Hong Kong, China, India, Nepal, Maldives, Sri Lanka">🇦🇿 🇬🇪 🇮🇷 🇹🇷 🇺🇦 🇲🇩 🇷🇸 🇲🇪 🇦🇱 🇲🇰 🇺🇸 🇶🇦 🇲🇾 🇮🇩 🇵🇭 🇦🇪 🇱🇦 🇰🇭 🇻🇳 🇸🇬 🇹🇯 🇺🇿 🇰🇬 🇰🇿 🇯🇵 🇹🇼 🇭🇰 🇨🇳 🇮🇳 🇳🇵 🇲🇻 🇱🇰</p>
        <p>And still going, slow and chill. The Photos app has some of it; Instagram has the rest.</p>
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
    <pre class="term__out" aria-live="polite"></pre>
    <form class="term__line"><label for="term-in"><span class="term__ps">vali@macbook ~ %</span></label><input id="term-in" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="send"></form>
  </div>
</section>


<section class="win win--mail" id="w-mail" role="dialog" aria-labelledby="w-mail-t">
  <header class="win__bar"><span class="lights"><a class="light light--close" href="#" aria-label="Close"></a><span class="light light--min"></span><span class="light light--max"></span></span><h2 class="win__title" id="w-mail-t">New Message</h2><a class="win__done" href="#">Cancel</a><button class="mail__send" type="submit" form="mail-form" aria-label="Send"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 19.5V5M5.8 11.2 12 5l6.2 6.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button></header>
  <form class="win__body mail" id="mail-form" data-mail action="https://api.web3forms.com/submit" method="post">
    <div class="mail__row"><span class="mail__label">To:</span><span class="mail__to" title="Fixed recipient">Vali Valiyev</span><span class="mail__addr">vali@gevelopers.com</span></div>
    <label class="mail__row"><span class="mail__label">Subject:</span><input name="subject" value="Hello Vali" autocomplete="off" required></label>
    <label class="mail__row"><span class="mail__label">From:</span><input type="email" name="email" placeholder="your@email.com" autocomplete="email" required></label>
    <input type="hidden" name="access_key" value="578732c5-06c1-4c9a-b583-5af530e0ff11">
    <input type="hidden" name="from_name" value="vvalisoy.github.io">
    <input type="checkbox" name="botcheck" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
    <textarea name="message" rows="12" aria-label="Message" required></textarea>
    <p class="mail__status" role="status" aria-live="polite"></p>
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
