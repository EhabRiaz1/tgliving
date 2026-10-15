#!/usr/bin/env python3
"""Builds the TG Living site: index, collection, from-pin-to-piece and one page per piece.
Edit the data below, then run:  python3 build.py
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = ""   # the live address once published, e.g. "https://tgliving.pk" (needed for WhatsApp previews)
PHONE = "923317770444"
PHONE_TXT = "+92 331 7770444"
IG = "https://www.instagram.com/tgliving_/"

CATS = {"dining-table": "Dining tables", "dining-chair": "Dining chairs", "console": "Consoles & credenzas",
        "sofa-lounge": "Lounge sofas", "sofa-drawing": "Drawing room", "chair": "Accent chairs", "coffee-table": "Coffee tables"}

VOLS = {
  "darbar": dict(n="I", name="Darbar", ur="دربار", mood="The court", img="p35",
    story="Gilded, carved and grand. Darbar is built on our crane motif: carved frames in gold leaf, crane jacquard and deep black velvet."),
  "shajar": dict(n="II", name="Shajar", ur="شجر", mood="The tree", img="p42",
    story="Sculpted walnut and open grain. Shajar follows the tree, from turned console posts to a table that keeps its natural edge."),
  "sang": dict(n="III", name="Sang", ur="سنگ", mood="Stone", img="p09",
    story="Quiet, minimal and led by stone. Marble and travertine on sculpted pedestals, with almost nothing else."),
  "zarr": dict(n="IV", name="Zarr", ur="زر", mood="Gold", img="p13",
    story="Polished brass and cast metal that catch the light: looped bases, brass frames and bouclé seats."),
  "khayal": dict(n="V", name="Khayal", ur="خیال", mood="Imagination", img="p15",
    story="Art furniture. Every Khayal piece is made by commission only and priced on request."),
}

CUT = {11,12,13,14,15,16,17,18,20,21,22,23,24,39,41,43,46,47,49,52,53}

# id, name, category, volume, one line, materials
PIECES = [
  (0,"Zumurrud Dining Table","dining-table","sang","A long table that reads as one slab of green stone.","Emerald marble top, twin stone plinths, brass-lined base"),
  (1,"Qaus Dining Table","dining-table","sang","Two stone cones linked by a single brass arch.","Ebonised top, stone pedestals, polished brass"),
  (2,"Pul Dining Table","dining-table","shajar","Stepped timber with stone set into the legs, like a bridge.","Ebonised ribbed timber, burl stone panels"),
  (3,"Lehr Dining Table","dining-table","sang","A poured black wave carrying a marble top.","Black high-gloss lacquer base, marble top"),
  (4,"Sutoon Dining Table","dining-table","sang","The sculpted-pedestal oval table of Volume III.","Oval stone top, bronze cylinder pedestals"),
  (5,"Bagh Dining Suite","dining-table","darbar","A full dining room in emerald and brass.","Brass-framed table, sculpted chairs in green velvet"),
  (6,"Noor Dining Suite","dining-table","darbar","Ivory sculpted chairs around a gold base.","Gold-finish table base, ivory upholstered chairs"),
  (7,"Shahi Dining Suite","dining-table","darbar","High-back chairs with gilded crests for formal dining.","Gilded carved frames, powder-blue velvet"),
  (8,"Saaya Dining Table","dining-table","sang","Marble on a thin black frame, with ribbed chairs.","Black-and-white marble, black steel, ribbed bouclé"),
  (9,"Chattan Dining Table","dining-table","sang","Rock-form tables with cast gold seating.","Hand-plastered bases, cast gold-finish chairs"),
  (10,"Halqa Dining Table","dining-table","zarr","A looped metal base under an oval glass top.","Bronze loop base, oval glass top"),
  (11,"Chand Dining Chair","dining-chair","shajar","A round back held in a thin brass ring.","Walnut legs, brass ring, woven upholstery"),
  (12,"Titli Dining Chair","dining-chair","zarr","A split velvet back, like folded wings.","Polished brass frame, velvet back, ivory seat"),
  (13,"Shakh Chair","dining-chair","zarr","A brass frame cast to grow like a branch.","Cast brass, upholstered seat"),
  (14,"Zari Dining Chair","dining-chair","darbar","Black lacquer and burl with an embroidered back.","Black lacquer, burl wood, gold-embroidered velvet"),
  (15,"Parwaz Chair","dining-chair","khayal","The winged chair. Made by commission only.","Verdigris-finish back, bent walnut legs, velvet seat"),
  (16,"Takia Lounge Chair","dining-chair","zarr","A deep seat with a single bolster for a back.","Bronze tube frame, bouclé seat, velvet bolster"),
  (17,"Gol Swivel Chair","dining-chair","zarr","A swivel seat framed in brass with a velvet roll.","Brass frame and base, bouclé, green velvet"),
  (18,"Bagla Console","console","darbar","Herons holding up a stone shelf.","Cast bronze birds, natural stone top"),
  (19,"Darwaza Sideboard","console","khayal","A row of arches in red lacquer.","High-gloss red lacquer, brass inlay"),
  (20,"Chehra Credenza","console","khayal","Carved faces across four doors. Made by commission only.","Carved and painted wood, black legs"),
  (21,"Chehra Console","console","khayal","A narrow console with one carved face.","Carved wood in terracotta, ivory and black"),
  (22,"Raqs Bar Cabinet","console","khayal","A painted lacquer cabinet on brass rods.","Hand-painted lacquer, brass legs"),
  (23,"Pankha Console","console","shajar","A carved fan holds up a thin black top.","Ebonised carved timber"),
  (24,"Sabz Sofa","sofa-lounge","zarr","A low curved sofa resting on brass shoes.","Emerald velvet, cast brass feet"),
  (26,"Darya Sofa","sofa-lounge","sang","Double-sided and serpentine, for the middle of a room.","Grey velvet, sculpted base"),
  (27,"Sarson Sofa","sofa-lounge","khayal","A sofa and ottoman that curl around each other.","Mustard mohair velvet"),
  (28,"Anaar Sofa","sofa-lounge","khayal","Five soft pebbles in pomegranate red.","Oxblood velvet"),
  (29,"Raat Sectional","sofa-lounge","zarr","Deep black seating on a bronze plinth.","Black upholstery, bronze base"),
  (30,"Lakeer Sofa","sofa-lounge","khayal","A full curve dressed in ink-line upholstery.","Striped printed fabric"),
  (31,"Badal Sofa","sofa-lounge","sang","Cloud-like bouclé forms on a stone floor.","Ivory bouclé"),
  (32,"Hilal Sofas","sofa-lounge","zarr","A facing pair of crescents.","Oxblood and black velvet, brass legs"),
  (33,"Darbar Drawing Room","sofa-drawing","darbar","A classical drawing room with carved gilt frames.","Gilded carved wood, ivory and navy upholstery"),
  (34,"Mahal Suite","sofa-drawing","darbar","White and gold, with a tufted centre ottoman.","Carved wood in white and gold leaf, tufted upholstery"),
  (35,"Jhalar Sofa","sofa-drawing","darbar","A caramel curve finished with a long fringe.","Caramel velvet, silk fringe"),
  (36,"Sukoon Sofa","sofa-drawing","sang","A low modular sofa with sculpted stools.","Linen upholstery, stone and wood tables"),
  (37,"Gulnar Sofa","sofa-drawing","shajar","A red curved sofa between two round chairs.","Red velvet, ivory bouclé"),
  (38,"Bahar Sectional","sofa-drawing","shajar","A corner sectional with printed ottomans.","Natural upholstery, printed ottomans"),
  (39,"Begum Chair","chair","darbar","A slipper chair with a full fringed skirt.","Teal velvet, contrast piping, fringe"),
  (40,"Naqsh Chair","chair","khayal","Stacked pebble forms covered in hand-drawn pattern.","Printed upholstery"),
  (41,"Mor Chair","chair","darbar","A swivel tub chair embroidered with fronds.","Teal velvet, embroidery"),
  (42,"Zaitoon Chair","chair","shajar","Olive velvet on a turned walnut plinth.","Olive velvet, walnut base"),
  (43,"Khol Chair","chair","zarr","A lacquered shell around a woven leather seat.","Oxblood lacquer, woven leather"),
  (44,"Safar Armchair","chair","shajar","A tweed armchair with sculpted wooden arms.","Wool tweed, walnut arms"),
  (45,"Baradari Lounge Chair","chair","zarr","A lounge chair belted in leather and brass.","Houndstooth fabric, leather strap, brass frame"),
  (46,"Sheesham Armchair","chair","shajar","A slim ebonised frame with brass tips.","Ebonised wood, brass sabots, printed upholstery"),
  (47,"Shagufa Chair","chair","darbar","Black lacquer and cherry blossom on gold legs.","Black lacquer, printed upholstery, gold-finish legs"),
  (48,"Moj Coffee Table","coffee-table","zarr","A gold ribbon under a sheet of glass.","Gilded ribbon base, glass top"),
  (49,"Chand Raat Coffee Table","coffee-table","sang","A terrazzo disc on three brass crescents.","Terrazzo top, brass legs"),
  (50,"Jora Nesting Tables","coffee-table","shajar","Two round tables that nest together.","Dark oak, brass sleeves"),
  (51,"Pighal Coffee Table","coffee-table","zarr","Bronze that looks poured and left to set.","Cast bronze"),
  (52,"Teh Coffee Table","coffee-table","zarr","Layered tops in bronze and dark wood.","Patinated bronze, dark wood, steel base"),
  (53,"Jheel Coffee Tables","coffee-table","khayal","A pair of tables like frozen lakes.","Resin, liquid-metal finish, bronze legs"),
]

FINISHES = [("As shown","linear-gradient(135deg,#d9d2c5,#8a9e9d)"),("Gold leaf","#c4a15e"),("Brass","#a8874f"),
            ("Walnut","#5b3a29"),("Black lacquer","#1c1b19"),("Natural stone","#d4cdc1")]

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def e(s): return html.escape(s, quote=True)
def wa(text): from urllib.parse import quote; return f"https://wa.me/{PHONE}?text={quote(text)}"

P = [dict(id=f"{i:02d}", name=n, cat=c, vol=v, desc=d, mat=m, slug=slug(n), cut=i in CUT) for i,n,c,v,d,m in PIECES]

# ---------------------------------------------------------------- shared parts
def logo(cls=""):
    return f'''<svg class="{cls}" viewBox="0 0 150 64" role="img" aria-label="TG Living"><g fill="currentColor">
<text class="lt" x="44" y="50" font-size="50" text-anchor="middle" font-family="Bodoni Moda, Didot, serif">T</text>
<g class="ln"><rect x="74.5" y="4" width="1" height="22"/><rect x="74.5" y="38" width="1" height="22"/></g>
<text class="lt" x="75" y="34.5" font-size="7.2" text-anchor="middle" letter-spacing="2.2" font-family="Bodoni Moda, Didot, serif">LIVING</text>
<text class="lt" x="107" y="50" font-size="50" text-anchor="middle" font-family="Bodoni Moda, Didot, serif">G</text></g></svg>'''

def head(title, desc, base, path="", image="brand/og.jpg"):
    # WhatsApp, iMessage and Facebook only show the preview image from a full https:// address,
    # so set SITE_URL to the live domain before publishing.
    site = SITE_URL.rstrip("/")
    abs_ = (lambda p: f"{site}/{p}") if site else (lambda p: base + p)
    canon = f'<link rel="canonical" href="{site}/{path}">\n<meta property="og:url" content="{site}/{path}">\n' if site else ""
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#fbf7f1">
{canon}<meta property="og:type" content="website">
<meta property="og:site_name" content="TG Living">
<meta property="og:locale" content="en_PK">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{abs_(image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="TG Living, designed for the art of living">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}brand/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{base}brand/icon-32.png">
<link rel="apple-touch-icon" href="{base}brand/icon-180.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@300;400;500&family=Noto+Nastaliq+Urdu&display=swap">
<link rel="stylesheet" href="{base}css/site.css">
</head>'''

def header(base, dark=False):
    return f'''<div class="curtain" aria-hidden="true">{logo()}</div>
<header class="hdr{' on-dark' if dark else ''}">
  <div class="wrap">
    <nav aria-label="Main">
      <a class="ulink" href="{base}collection.html">Collection</a>
      <a class="ulink" href="{base}index.html#volumes">Volumes</a>
      <a class="ulink" href="{base}from-pin-to-piece.html">From pin to piece</a>
    </nav>
    <button class="menu-btn" type="button">Menu</button>
    <a class="logo" href="{base}index.html" aria-label="TG Living, home">{logo()}</a>
    <div class="right">
      <span class="meta loc">Lahore</span>
      <a class="btn light" href="https://wa.me/{PHONE}" target="_blank" rel="noopener">Enquire</a>
    </div>
  </div>
</header>
<div class="drawer" aria-label="Menu">
  <button class="close" type="button">Close</button>
  <ul>
    <li><a href="{base}index.html">Home</a></li>
    <li><a href="{base}collection.html">Collection</a></li>
    <li><a href="{base}index.html#volumes">Volumes</a></li>
    <li><a href="{base}from-pin-to-piece.html">From pin to piece</a></li>
    <li><a href="https://wa.me/{PHONE}" target="_blank" rel="noopener">WhatsApp</a></li>
  </ul>
  <p class="meta">Lahore · Delivery nationwide</p>
</div>'''

def footer(base, credits=""):
    vols = "".join(f'<li><a href="{base}collection.html#{k}">{v["n"]} · {v["name"]}</a></li>' for k,v in VOLS.items())
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="cta">
      <h2 data-split>Have a pin in mind? We will make it.</h2>
      <div class="acts">
        <a class="btn light" href="{wa("Hello TG Living, I have a pin I'd like made.")}" target="_blank" rel="noopener">Message on WhatsApp <span class="arr">→</span></a>
        <a class="btn light" href="{IG}" target="_blank" rel="noopener">Follow @tgliving_</a>
      </div>
    </div>
    <div class="cols">
      <div><p class="meta">Atelier</p><ul><li>Lahore, Pakistan</li><li>Delivery nationwide</li><li>Every piece made to order</li></ul></div>
      <div><p class="meta">Contact</p><ul><li><a href="https://wa.me/{PHONE}" target="_blank" rel="noopener">WhatsApp {PHONE_TXT}</a></li><li><a href="tel:+{PHONE}">Call {PHONE_TXT}</a></li><li><a href="{IG}" target="_blank" rel="noopener">Instagram @tgliving_</a></li></ul></div>
      <div><p class="meta">Explore</p><ul><li><a href="{base}collection.html">The collection</a></li><li><a href="{base}from-pin-to-piece.html">From pin to piece</a></li><li><a href="{base}index.html#volumes">The five volumes</a></li></ul></div>
      <div><p class="meta">Volumes</p><ul>{vols}</ul></div>
    </div>
  </div>
  <p class="mega" aria-hidden="true">TG Living</p>
  <div class="legal wrap"><span>© 2026 TG Living. Designed for the art of living.</span>{credits}</div>
</footer>'''

def scripts(base, data=False):
    d = f'<script src="{base}js/data.js"></script>\n' if data else ""
    return f'''{d}<script src="{base}js/vendor/gsap.min.js"></script>
<script src="{base}js/vendor/ScrollTrigger.min.js"></script>
<script src="{base}js/vendor/lenis.min.js"></script>
<script src="{base}js/site.js"></script>
</body>
</html>
'''

def card(p, base=""):
    v = VOLS[p["vol"]]
    if p["cut"]:
        ph = f'<div class="ph cut has-alt"><img src="{base}cutouts/c{p["id"]}.webp" alt="{e(p["name"])}" loading="lazy"><img class="alt" src="{base}images/p{p["id"]}.jpg" alt="" loading="lazy"></div>'
    else:
        ph = f'<div class="ph"><img src="{base}images/p{p["id"]}.jpg" alt="{e(p["name"])}" loading="lazy"></div>'
    return f'<a class="card" href="{base}pieces/{p["slug"]}.html" data-cursor="View">{ph}<div class="tx"><h3>{e(p["name"])}</h3><span class="meta">{v["n"]} · {v["name"]}</span></div><p class="ds">{e(p["desc"])}</p></a>'

def pin_section(base):
    kinds = "".join(f"<option>{v[:-1] if v.endswith('s') and not v.endswith('ss') else v}</option>" for v in ["Dining table","Dining chairs","Console","Sofa","Armchair","Coffee table","Bed","Something else"])
    fins = "".join(f"<option>{f}</option>" for f,_ in FINISHES[1:]) + "<option>Not sure yet</option>"
    return f'''<section class="pin" id="pin" aria-labelledby="pinTitle">
  <div class="wrap grid">
    <div class="intro">
      <p class="meta">From pin to piece</p>
      <h2 id="pinTitle" data-split style="margin-top:22px">Your Pinterest board, made real.</h2>
      <p data-fade>Send us the piece you have saved. Our workshop in Lahore makes it in your size, your fabric and your finish, and delivers it anywhere in Pakistan.</p>
      <span class="rule"></span>
    </div>
    <ol class="steps" data-stagger>
      <li><div><h3>Send the pin</h3><p>Share the Pinterest link or a screenshot on WhatsApp or Instagram, with a photo of the room if you have one.</p></div></li>
      <li><div><h3>Drawing and samples</h3><p>We return a measured drawing and show you real samples of wood, stone, metal and fabric.</p></div></li>
      <li><div><h3>Made by hand</h3><p>Carving, gilding, lacquer and upholstery are done by our craftsmen. You see progress photos as it takes shape.</p></div></li>
      <li><div><h3>Delivered</h3><p>Wrapped, delivered and placed in your home, in Lahore or anywhere in the country.</p></div></li>
    </ol>
    <div class="maker" data-fade>
      <div class="side">
        <h3>Start with your pin</h3>
        <p>Fill in what you know. We turn it into a WhatsApp message for you to send, so nothing gets lost.</p>
        <button class="btn" type="button" data-copy="+{PHONE}">Copy our number</button>
      </div>
      <form id="maker" autocomplete="off">
        <div class="field"><label class="meta" for="pin-link">Pinterest link</label><input id="pin-link" name="pin" type="url" inputmode="url" placeholder="https://pin.it/…"></div>
        <div class="row2">
          <div class="field"><label class="meta" for="pin-kind">Piece</label><select id="pin-kind" name="kind">{kinds}</select></div>
          <div class="field"><label class="meta" for="pin-finish">Finish</label><select id="pin-finish" name="finish">{fins}</select></div>
        </div>
        <div class="row2">
          <div class="field"><label class="meta" for="pin-size">Size or room</label><input id="pin-size" name="size" type="text" placeholder="Seats 8, room 5 × 4 m"></div>
          <div class="field"><label class="meta" for="pin-city">Delivery city</label><input id="pin-city" name="city" type="text" placeholder="Lahore"></div>
        </div>
        <p class="preview" id="makerPreview" aria-live="polite"></p>
        <a class="btn solid" id="makerSend" href="https://wa.me/{PHONE}" target="_blank" rel="noopener">Send on WhatsApp <span class="arr">→</span></a>
      </form>
    </div>
  </div>
</section>'''

def write(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

write("site.webmanifest", json.dumps(dict(name="TG Living", short_name="TG Living", start_url="./index.html", display="standalone",
    background_color="#fbf7f1", theme_color="#8a9e9d", icons=[dict(src="brand/icon-192.png", sizes="192x192", type="image/png"),
    dict(src="brand/icon-512.png", sizes="512x512", type="image/png")]), indent=1))
if not SITE_URL: print("Note: SITE_URL is empty, so link previews will not show an image until it is set to the live address.")

# ---------------------------------------------------------------- data for the collection page
write("js/data.js", "window.TG=" + json.dumps(dict(PIECES=P, CATS=CATS, VOLS=VOLS), ensure_ascii=False) + ";\n")

# ---------------------------------------------------------------- home
byid = {p["id"]: p for p in P}
slides = [("14","50% 62%"),("23","50% 58%"),("26","50% 55%")]
slide_html = "".join(f'<div class="slide{" on" if i==0 else ""}" data-cap="{e(byid[s]["name"])}" data-href="pieces/{byid[s]["slug"]}.html"><img src="images/p{s}.jpg" alt="{e(byid[s]["name"])}" style="object-position:{pos}" {"" if i==0 else "loading=\"lazy\""}></div>' for i,(s,pos) in enumerate(slides))
feat_ids = ["15","13","22","20","23","43","46","47","18","52","53","12"]
objs = "".join(f'<a class="obj" href="pieces/{byid[i]["slug"]}.html" data-cursor="View"><div class="stage"><img src="cutouts/c{i}.webp" alt="{e(byid[i]["name"])}" decoding="async"></div><div class="nm"><h3>{e(byid[i]["name"])}</h3><span class="meta">{VOLS[byid[i]["vol"]]["n"]} · {VOLS[byid[i]["vol"]]["name"]}</span></div></a>' for i in feat_ids)
vrows = "".join(f'<a class="vrow" href="collection.html#{k}" data-cursor="Enter"><span class="n">{v["n"]}</span><span class="nm"><b>{v["name"]}</b><span lang="ur">{v["ur"]}</span></span><span class="mood">{v["mood"]}. {v["story"].split(".")[0]}.</span><span class="cnt meta">{sum(1 for p in P if p["vol"]==k)} pieces</span></a>' for k,v in VOLS.items())
peek = "".join(f'<img src="images/{v["img"]}.jpg" alt="">' for v in VOLS.values())
igs = "".join(f'<a href="{IG}" target="_blank" rel="noopener" data-cursor="Open"><img src="ig/ig{n}.jpg" alt="A TG Living post on Instagram" loading="lazy"></a>' for n in ["04","05","06","07","09","12"])

index = head("TG Living — Designed for the art of living", "From pin to piece: luxury furniture made to order in Lahore and delivered across Pakistan.", "", "") + f'''
<body data-hero="dark">
{header("", dark=True)}
<main>
  <section class="hero" aria-label="Introduction">
    <div class="slides">{slide_html}</div>
    <div class="copy wrap">
      <h1>Designed for the art of living.</h1>
      <div class="side">
        <p>From pin to piece. Furniture made to order in Lahore and delivered across Pakistan.</p>
        <div class="cap"><span class="bars"><i><b></b></i><i><b></b></i><i><b></b></i></span><a class="meta ulink" href="pieces/{byid["14"]["slug"]}.html">{byid["14"]["name"]}</a></div>
      </div>
    </div>
  </section>

  <section class="manifesto wrap" aria-labelledby="manTitle">
    <div class="grid">
      <p class="meta k">Lahore · Made to order</p>
      <h2 id="manTitle" data-split>Every piece begins as an image someone loved.</h2>
      <div class="body" data-fade>
        <p>Most furniture worth wanting cannot be bought here. So we make it. Send us the chair, the console or the dining table you have saved, and our craftsmen build it for your room.</p>
        <p>Carved frames, gold leaf, walnut, marble, brass and velvet. Your size, your fabric, your finish.</p>
        <a class="btn" href="from-pin-to-piece.html">How it works <span class="arr">→</span></a>
      </div>
      <div class="pics">
        <figure><div class="clip" data-reveal><img src="images/p23.jpg" alt="A carved black fan console in a pale room" loading="lazy"></div><figcaption><span class="meta">Pankha Console</span><span class="meta">II · Shajar</span></figcaption></figure>
        <figure><div class="clip" data-reveal><img src="ig/ig05.jpg" alt="A bolster bench on a wooden base, from TG Living's Instagram" loading="lazy"></div><figcaption><span class="meta">From our studio</span></figcaption></figure>
        <figure><div class="clip" data-reveal><img src="ig/ig04.jpg" alt="A gilded winged armchair in plum velvet, from TG Living's Instagram" loading="lazy"></div><figcaption><span class="meta">From our studio</span></figcaption></figure>
      </div>
    </div>
  </section>

  <section class="objects" aria-labelledby="objTitle">
    <div class="head wrap">
      <h2 id="objTitle" data-split>The collection, one object at a time.</h2>
      <p data-fade>Fifty-three pieces across five volumes. Every one is made to order and can be changed to suit your room. <a class="ulink" href="collection.html">See all pieces</a></p>
      <p class="swipe meta" aria-hidden="true">Swipe <i><b></b></i></p>
    </div>
    <div class="track">{objs}</div>
  </section>

  <section class="volumes wrap" id="volumes" aria-labelledby="volTitle">
    <div class="top">
      <p class="meta">Five volumes</p>
      <h2 id="volTitle" data-split>A volume is a mood, not a room.</h2>
      <p data-fade>Each volume has a name, a story and a material it returns to. They are released in this order, beginning with the gilded court of Darbar.</p>
    </div>
    <div class="vlist">{vrows}</div>
    <div class="vpeek" aria-hidden="true">{peek}</div>
  </section>

  <section class="feature" aria-labelledby="featTitle">
    <img src="images/p22.jpg" alt="A hand-painted lacquer bar cabinet on brass legs" data-parallax="16" loading="lazy">
    <div class="copy wrap">
      <h2 id="featTitle" data-split>Made by hand, in Lahore.</h2>
      <a class="btn light" href="pieces/{byid["22"]["slug"]}.html">Raqs Bar Cabinet <span class="arr">→</span></a>
    </div>
  </section>

  {pin_section("")}

  <section class="ig wrap" aria-labelledby="igTitle">
    <div class="head"><h2 id="igTitle" data-split>@tgliving_</h2><a class="btn" href="{IG}" target="_blank" rel="noopener">Follow on Instagram</a></div>
    <div class="grid" data-stagger>{igs}</div>
  </section>
</main>
{footer("")}
{scripts("")}'''
write("index.html", index)

# ---------------------------------------------------------------- collection
coll = head("The Collection — TG Living", "Fifty-three pieces of luxury furniture made to order in Lahore, in five volumes.", "", "collection.html") + f'''
<body>
{header("")}
<main>
  <section class="page-head wrap">
    <div class="grid">
      <p class="meta">The collection · {len(P)} pieces</p>
      <h1 data-split>Every piece, made for one room.</h1>
      <p data-fade>Browse by room or by volume. Open a piece to choose a finish and send us an enquiry. Nothing here is kept in stock.</p>
    </div>
  </section>
  <div class="filters"><div class="wrap"><div class="fl" id="fl" role="group" aria-label="Filter by room"></div><label class="sr" for="vsel">Volume</label><select class="vsel" id="vsel"></select></div></div>
  <div class="wrap">
    <div class="vol-intro" id="volIntro" hidden></div>
    <p class="meta" id="count" style="margin-top:40px;color:var(--muted)" aria-live="polite"></p>
    <div class="pgrid" id="pgrid">{"".join(card(p) for p in P)}</div>
  </div>
</main>
{footer("")}
{scripts("", data=True)}'''
write("collection.html", coll)

# ---------------------------------------------------------------- pin to piece page
credits = '<span>Archive pictures: <a href="https://commons.wikimedia.org/w/index.php?curid=60849079">Sheraton, The Cabinet-Maker and Upholsterer\'s Drawing-Book</a>, CC0; <a href="https://www.artic.edu/artworks/157108">Carved Panel with Mythical Birds</a>, India, late 16th century, CC0, Art Institute of Chicago.</span>'
bespoke = head("From pin to piece — TG Living", "Send us a Pinterest pin and we make the piece, in your size and finish, in Lahore.", "", "from-pin-to-piece.html") + f'''
<body>
{header("")}
<main>
  <section class="page-head wrap">
    <div class="grid">
      <p class="meta">From pin to piece</p>
      <h1 data-split>You saved it. We make it.</h1>
      <p data-fade>TG Living turns the furniture on your Pinterest board into real pieces for your home, built by hand in Lahore.</p>
    </div>
  </section>
  <section class="split wrap">
    <figure><div class="clip" data-reveal><img src="assets/the-cabinet-maker-and-upholsterer-s-drawing.jpg" alt="An engraved sheet of chair-back designs from a 1790s cabinet-maker's drawing book" loading="lazy"></div></figure>
    <div class="tx"><p class="meta">I · Drawing</p><h2 data-split>Every pin becomes a drawing.</h2><p data-fade>A photograph rarely shows how a piece is built. We study it, ask about your room, and draw it to size with every joint and finish named. Nothing is made until you approve the drawing.</p></div>
  </section>
  <section class="split rev wrap">
    <figure><div class="clip" data-reveal><img src="assets/carved-panel-with-mythical-birds.jpg" alt="A sixteenth-century Indian carved wooden panel with two birds among vines" loading="lazy"></div></figure>
    <div class="tx"><p class="meta">II · Carving</p><h2 data-split>Carved the way it always was.</h2><p data-fade>Our frames are carved by hand, in a tradition you can see in panels like this one from sixteenth-century India. Then they are gilded, lacquered or oiled.</p></div>
  </section>
  <section class="split wrap">
    <figure><div class="clip" data-reveal><img src="images/p13.jpg" alt="A cast brass chair with branch-like legs" loading="lazy"></div></figure>
    <div class="tx"><p class="meta">III · Finishing</p><h2 data-split>Brass, velvet and gold leaf.</h2><p data-fade>Metalwork, upholstery and gilding happen under one roof, so the finish you chose from a sample is the finish you receive. We send progress photos along the way.</p></div>
  </section>
  {pin_section("")}
  <section class="faq wrap" aria-labelledby="faqTitle">
    <h2 id="faqTitle" data-split>Questions</h2>
    <dl>
      <details><summary>Can you make anything I find on Pinterest?</summary><p>Most furniture, yes. Send it over and we will tell you honestly what we can make, what we would change, and why.</p></details>
      <details><summary>Can I change the size, fabric or finish?</summary><p>Always. Every piece is drawn for your room, and you choose the wood, stone, metal and fabric from real samples.</p></details>
      <details><summary>How long does it take?</summary><p>It depends on the piece. We give you a timeline together with the drawing and the quote, before anything is made.</p></details>
      <details><summary>Do you deliver outside Lahore?</summary><p>Yes. We deliver nationwide and place the piece in your home.</p></details>
      <details><summary>How do I start?</summary><p>Message us on WhatsApp at {PHONE_TXT} or on Instagram at @tgliving_ with your pin and, if you can, a photo of the room.</p></details>
    </dl>
  </section>
</main>
{footer("", credits)}
{scripts("")}'''
write("from-pin-to-piece.html", bespoke)

# ---------------------------------------------------------------- piece pages
for idx, p in enumerate(P):
    v = VOLS[p["vol"]]; b = "../"
    gal = f'<figure data-fade><img src="{b}images/p{p["id"]}.jpg" alt="{e(p["name"])}"></figure>'
    if p["cut"]:
        gal += f'<figure class="cut" data-fade><img src="{b}cutouts/c{p["id"]}.webp" alt="{e(p["name"])}, the piece on its own" loading="lazy"></figure>'
    sw = "".join(f'<button class="sw" type="button" data-f="{f}" aria-pressed="false"><i style="background:{c}"></i>{f}</button>' for f,c in FINISHES)
    rel = [q for q in P if q["vol"] == p["vol"] and q["id"] != p["id"]][:4]
    prev, nxt = P[idx-1], P[(idx+1) % len(P)]
    msg = f"Hello TG Living, I'm interested in the {p['name']} (Volume {v['n']}, {v['name']}). Could you share details and pricing?"
    page = head(f"{p['name']} — TG Living", f"{p['name']}: {p['desc']} Made to order in Lahore.", b, f"pieces/{p['slug']}.html", f"brand/og/{p['slug']}.jpg") + f'''
<body data-base="{b}">
{header(b)}
<main class="piece wrap">
  <div class="grid">
    <div class="gallery">{gal}</div>
    <div class="info">
      <p class="crumbs meta"><a href="{b}collection.html">Collection</a><span>/</span><a href="{b}collection.html#{p["cat"]}">{CATS[p["cat"]]}</a><span>/</span><a href="{b}collection.html#{p["vol"]}">{v["n"]} · {v["name"]}</a></p>
      <h1 data-split>{e(p["name"])}</h1>
      <p class="lead" data-fade>{e(p["desc"])}</p>
      <dl class="specs" data-fade>
        <div><dt class="meta">Volume</dt><dd>{v["n"]} · {v["name"]}, {v["mood"].lower()}</dd></div>
        <div><dt class="meta">Materials</dt><dd>{e(p["mat"])}</dd></div>
        <div><dt class="meta">Dimensions</dt><dd>Made to your room</dd></div>
        <div><dt class="meta">Delivery</dt><dd>From Lahore, nationwide</dd></div>
        <div><dt class="meta">Price</dt><dd>On request</dd></div>
      </dl>
      <div data-fade><p class="meta" style="margin-bottom:14px">Finish · <span id="finishName">As shown</span></p><div class="swatches">{sw}</div></div>
      <div class="field" data-fade><label class="meta" for="notes">Size or room notes</label><input id="notes" type="text" placeholder="Seats 8, room 5 × 4 m"></div>
      <div class="acts" data-fade>
        <a class="btn solid" id="enquire" data-name="{e(p["name"])}" data-vol="Volume {v["n"]}, {v["name"]}" href="{wa(msg)}" target="_blank" rel="noopener">Enquire on WhatsApp <span class="arr">→</span></a>
        <a class="btn" href="{IG}" target="_blank" rel="noopener">Message on Instagram</a>
      </div>
      <p class="note">Finishes shown are a starting point. Every piece is drawn for you and confirmed against real samples before it is made.</p>
    </div>
  </div>
  <nav class="pnav" aria-label="More pieces">
    <a href="{prev["slug"]}.html"><span class="meta">Previous</span><b>{e(prev["name"])}</b></a>
    <a href="{nxt["slug"]}.html"><span class="meta">Next</span><b>{e(nxt["name"])}</b></a>
  </nav>
</main>
<section class="related wrap" aria-labelledby="relTitle">
  <h2 id="relTitle" data-split>More from {v["name"]}</h2>
  <div class="pgrid">{"".join(card(q, b) for q in rel)}</div>
</section>
{footer(b)}
{scripts(b)}'''
    write(f"pieces/{p['slug']}.html", page)

print(f"Built index, collection, from-pin-to-piece and {len(P)} piece pages.")
