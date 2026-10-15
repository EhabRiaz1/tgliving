# tgliving

Website for **TG Living**: luxury furniture made to order in Lahore, "from pin to piece".

## Run it

It's a static site, so you can open `index.html` directly or serve the folder:

```
python3 -m http.server 8765
```

## Edit it

Pages are generated from the data at the top of `build.py` (pieces, volumes, categories). After editing:

```
python3.12 build.py
```

This rebuilds `index.html`, `collection.html`, `from-pin-to-piece.html`, every page in `pieces/` and `js/data.js`.

Before publishing, set `SITE_URL` in `build.py` to the live address and rebuild, so WhatsApp and social previews show the image.

## Layout

- `css/site.css`, `js/site.js`: styles and behaviour (GSAP, ScrollTrigger and Lenis are in `js/vendor/`)
- `images/`: graded product photos; `cutouts/`: background-removed pieces
- `brand/`: favicon, app icons and link-preview cards (`brand/og/` holds one card per piece)
- `ig/`: images from @tgliving_; `assets/`: CC0 archive images (credited on the From pin to piece page)
