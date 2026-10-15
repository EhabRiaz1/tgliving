/* TG Living — site behaviour. Content is complete without this file; it only adds motion and tools. */
(() => {
  const root = document.documentElement;
  root.classList.remove("no-js");
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const PHONE = "923317770444";
  const BASE = document.body.dataset.base || "";
  const hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
  const wa = text => `https://wa.me/${PHONE}?text=${encodeURIComponent(text)}`;

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (hasGSAP) gsap.registerPlugin(ScrollTrigger);
  if (!reduce && typeof window.Lenis !== "undefined") {
    lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    if (hasGSAP) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
    $$('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
      const id = a.getAttribute("href"); if (id.length < 2) return;
      const t = document.querySelector(id); if (!t) return;
      e.preventDefault(); lenis.scrollTo(t, { offset: -20 });
    }));
  }

  /* ---------- header ---------- */
  const hdr = $(".hdr");
  if (hdr) {
    const darkTop = document.body.dataset.hero === "dark";
    let last = 0;
    const onScroll = () => {
      const y = window.scrollY;
      const past = y > 40;
      hdr.classList.toggle("scrolled", past);
      hdr.classList.toggle("on-dark", darkTop && !past);
      const hide = y > 300 && y > last;
      hdr.classList.toggle("hide", hide);
      document.body.classList.toggle("hdr-visible", !hide && y > 300);
      last = y;
    };
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });
  }
  const drawer = $(".drawer");
  if (drawer) {
    $(".menu-btn")?.addEventListener("click", () => { drawer.classList.add("open"); lenis?.stop(); });
    $(".drawer .close")?.addEventListener("click", () => { drawer.classList.remove("open"); lenis?.start(); });
    $$(".drawer a").forEach(a => a.addEventListener("click", () => { drawer.classList.remove("open"); lenis?.start(); }));
  }

  /* ---------- curtain: first visit shows the monogram, later pages just lift ---------- */
  const curtain = $(".curtain");
  const intro = (() => { try { const s = sessionStorage.getItem("tg-seen"); sessionStorage.setItem("tg-seen", "1"); return !s; } catch { return false; } })();
  const start = () => { document.body.classList.add("ready"); heroIn(); };
  if (curtain && hasGSAP && !reduce) {
    const tl = gsap.timeline({ onComplete: () => { curtain.classList.add("gone"); } });
    if (intro) {
      gsap.set(curtain.querySelectorAll(".lt"), { opacity: 0, y: 18 });
      gsap.set(curtain.querySelector(".ln"), { scaleY: 0 });
      tl.to(curtain.querySelector(".ln"), { scaleY: 1, duration: .9, ease: "power3.inOut" })
        .to(curtain.querySelectorAll(".lt"), { opacity: 1, y: 0, duration: .8, stagger: .08, ease: "power3.out" }, "-=.35")
        .to(curtain, { clipPath: "inset(0 0 100% 0)", duration: 1.1, ease: "power4.inOut", delay: .25 })
        .add(start, "-=.55");
    } else {
      gsap.set(curtain.querySelector("svg"), { opacity: 0 });
      tl.to(curtain, { clipPath: "inset(0 0 100% 0)", duration: .9, ease: "power4.inOut" }).add(start, "-=.5");
    }
  } else { curtain?.classList.add("gone"); start(); }

  /* page-leave curtain for internal links */
  if (curtain && hasGSAP && !reduce) {
    $$("a[href]").forEach(a => {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#") || a.target === "_blank" || /^(https?:|mailto:|tel:)/.test(href)) return;
      a.addEventListener("click", e => {
        if (e.metaKey || e.ctrlKey || e.shiftKey) return;
        e.preventDefault();
        curtain.classList.remove("gone");
        gsap.set(curtain.querySelector("svg"), { opacity: 0 });
        gsap.fromTo(curtain, { clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)", duration: .7, ease: "power4.inOut", onComplete: () => { location.href = href; } });
      });
    });
    addEventListener("pageshow", e => { if (e.persisted) curtain.classList.add("gone"); });
  }

  /* ---------- split headings into masked lines (by words, regrouped per rendered line) ---------- */
  function splitLines(el) {
    if (el.dataset.split) return [];
    el.dataset.split = "1";
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(w => `<span class="w" style="display:inline-block">${w}</span>`).join(" ");
    const lines = []; let top = null;
    $$(".w", el).forEach(w => { const t = w.offsetTop; if (t !== top) { lines.push([]); top = t; } lines[lines.length - 1].push(w.textContent); });
    el.innerHTML = lines.map(l => `<span class="line"><span>${l.join(" ")}</span></span>`).join("");
    return $$(".line>span", el);
  }

  function heroIn() {
    if (!hasGSAP || reduce) return;
    const h = $(".hero h1");
    if (h) { const ls = splitLines(h); gsap.from(ls, { yPercent: 110, duration: 1.4, stagger: .1, ease: "power4.out" }); }
    const side = $$(".hero .side > *");
    if (side.length) gsap.from(side, { opacity: 0, y: 20, duration: 1, stagger: .1, delay: .5, ease: "power3.out" });
  }

  /* ---------- scroll reveals ---------- */
  if (hasGSAP && !reduce) {
    $$("[data-split]").forEach(el => {
      const ls = splitLines(el);
      gsap.from(ls, { yPercent: 110, duration: 1.3, stagger: .09, ease: "power4.out", scrollTrigger: { trigger: el, start: "top 88%" } });
    });
    $$("[data-fade]").forEach(el => gsap.from(el, { opacity: 0, y: 28, duration: 1.2, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 90%" } }));
    $$("[data-stagger]").forEach(el => gsap.from(el.children, { opacity: 0, y: 36, duration: 1.1, stagger: .08, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 85%" } }));
    $$("[data-reveal]").forEach(el => {
      const img = el.querySelector("img");
      gsap.fromTo(el, { clipPath: "inset(18% 12% 18% 12%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.6, ease: "power4.out", scrollTrigger: { trigger: el, start: "top 85%" } });
      if (img) gsap.fromTo(img, { scale: 1.25 }, { scale: 1, duration: 1.8, ease: "power4.out", scrollTrigger: { trigger: el, start: "top 85%" } });
    });
    $$("[data-parallax]").forEach(el => {
      const amt = parseFloat(el.dataset.parallax) || 12;
      gsap.fromTo(el, { yPercent: -amt / 2 }, { yPercent: amt / 2, ease: "none", scrollTrigger: { trigger: el.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
    });
  }

  /* ---------- hero slides ---------- */
  const slides = $$(".hero .slide");
  if (slides.length > 1) {
    const bars = $$(".hero .bars i"); const cap = $(".hero .cap a");
    let k = 0, timer = null;
    const go = n => {
      slides[k].classList.remove("on"); bars[k]?.classList.remove("on"); bars[k]?.classList.add("done");
      k = n % slides.length;
      if (k === 0) bars.forEach(b => b.classList.remove("done"));
      slides[k].classList.add("on"); bars[k]?.classList.add("on");
      if (cap) { cap.textContent = slides[k].dataset.cap; cap.href = slides[k].dataset.href; }
    };
    bars[0]?.classList.add("on");
    if (!reduce) timer = setInterval(() => { if (!document.hidden) go(k + 1); }, 6000);
  }

  /* ---------- horizontal object gallery ---------- */
  const track = $(".objects .track");
  if (track && hasGSAP && !reduce && matchMedia("(min-width: 901px)").matches) {
    const sec = $(".objects");
    const dist = () => Math.max(0, track.scrollWidth - innerWidth);
    gsap.to(track, { x: () => -dist(), ease: "none", scrollTrigger: { trigger: sec, start: "top top", end: () => "+=" + dist(), pin: true, scrub: .6, invalidateOnRefresh: true } });
  }

  /* phone: the carousel scrolls natively; the bar under the heading follows it */
  if (track && !matchMedia("(min-width: 901px)").matches) {
    const bar = $(".swipe b");
    const upd = () => { const max = track.scrollWidth - track.clientWidth; bar?.style.setProperty("--p", max > 0 ? Math.max(.08, track.scrollLeft / max) : 1); };
    track.addEventListener("scroll", upd, { passive: true }); upd();
  }

  /* ---------- volume peek ---------- */
  const peek = $(".vpeek");
  if (peek && fine) {
    const imgs = $$("img", peek);
    let x = innerWidth / 2, y = innerHeight / 2, px = x, py = y;
    $$(".vrow").forEach((row, i) => {
      row.addEventListener("mouseenter", () => { peek.classList.add("on"); imgs.forEach((im, j) => im.classList.toggle("on", j === i)); });
      row.addEventListener("mouseleave", () => peek.classList.remove("on"));
    });
    addEventListener("mousemove", e => { x = e.clientX; y = e.clientY; });
    const loop = () => { px += (x - px) * .14; py += (y - py) * .14; peek.style.left = px + "px"; peek.style.top = py + "px"; requestAnimationFrame(loop); };
    loop();
  }

  /* ---------- cursor ---------- */
  if (fine && !reduce) {
    const c = document.createElement("div"); c.className = "cursor"; c.innerHTML = "<span>View</span>"; document.body.append(c);
    let x = 0, y = 0, cx = 0, cy = 0;
    addEventListener("mousemove", e => { x = e.clientX; y = e.clientY; c.classList.add("show"); });
    document.addEventListener("mouseleave", () => c.classList.remove("show"));
    const loop = () => { cx += (x - cx) * .2; cy += (y - cy) * .2; c.style.transform = `translate(${cx}px,${cy}px)`; requestAnimationFrame(loop); };
    loop();
    document.addEventListener("mouseover", e => { const t = e.target.closest("[data-cursor]"); c.classList.toggle("big", !!t); if (t) c.querySelector("span").textContent = t.dataset.cursor; });
  }

  /* ---------- copy number ---------- */
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-copy]"); if (!b) return;
    navigator.clipboard?.writeText(b.dataset.copy).then(() => toast("Number copied"), () => toast("+92 331 7770444"));
  });
  function toast(m) { const t = document.createElement("div"); t.className = "toast"; t.textContent = m; document.body.append(t); setTimeout(() => t.remove(), 2200); }

  /* ---------- pin to piece maker ---------- */
  const maker = $("#maker");
  if (maker) {
    const out = $("#makerPreview"), send = $("#makerSend");
    const build = () => {
      const f = Object.fromEntries(new FormData(maker));
      const lines = ["Hello TG Living, I'd like a piece made from a pin."];
      if (f.pin) lines.push(`Pin: ${f.pin}`);
      if (f.kind) lines.push(`Piece: ${f.kind}`);
      if (f.size) lines.push(`Size or room: ${f.size}`);
      if (f.finish) lines.push(`Finish: ${f.finish}`);
      if (f.city) lines.push(`Delivery city: ${f.city}`);
      const text = lines.join("\n");
      out.textContent = text; send.href = wa(text);
    };
    maker.addEventListener("input", build); maker.addEventListener("change", build);
    maker.addEventListener("submit", e => { e.preventDefault(); build(); window.open(send.href, "_blank", "noopener"); });
    build();
  }

  /* ---------- piece page: finish + enquiry ---------- */
  const enq = $("#enquire");
  if (enq) {
    const name = enq.dataset.name, vol = enq.dataset.vol;
    let finish = "As shown";
    const notes = $("#notes");
    const sync = () => {
      $$(".sw").forEach(b => b.setAttribute("aria-pressed", b.dataset.f === finish));
      $("#finishName").textContent = finish;
      const n = notes.value.trim();
      enq.href = wa(`Hello TG Living, I'm interested in the ${name} (${vol}). Finish: ${finish}.${n ? " Notes: " + n + "." : ""} Could you share details and pricing?`);
    };
    $$(".sw").forEach(b => b.addEventListener("click", () => { finish = b.dataset.f; sync(); }));
    notes.addEventListener("input", sync);
    sync();
  }

  /* ---------- collection filters ---------- */
  const grid = $("#pgrid");
  if (grid && window.TG) {
    const { PIECES, CATS, VOLS } = window.TG;
    const st = { cat: "all", vol: "all" };
    const fromHash = () => { const h = location.hash.slice(1); if (VOLS[h]) { st.vol = h; st.cat = "all"; } else if (CATS[h]) { st.cat = h; st.vol = "all"; } };
    fromHash();
    const fl = $("#fl"), vs = $("#vsel"), intro = $("#volIntro"), count = $("#count");
    fl.innerHTML = [["all", "All pieces", PIECES.length], ...Object.entries(CATS).map(([k, v]) => [k, v, PIECES.filter(p => p.cat === k).length])]
      .map(([k, v, n]) => `<button type="button" data-cat="${k}" aria-pressed="false">${v}<sup>${n}</sup></button>`).join("");
    vs.innerHTML = `<option value="all">All volumes</option>` + Object.entries(VOLS).map(([k, v]) => `<option value="${k}">${v.n} · ${v.name}</option>`).join("");
    fl.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; st.cat = b.dataset.cat; render(true); });
    vs.addEventListener("change", () => { st.vol = vs.value; render(true); });
    addEventListener("hashchange", () => { fromHash(); render(true); });
    function card(p) {
      const v = VOLS[p.vol];
      const ph = p.cut
        ? `<div class="ph cut has-alt"><img src="cutouts/c${p.id}.webp" alt="${p.name}" loading="lazy"><img class="alt" src="images/p${p.id}.jpg" alt="" loading="lazy"></div>`
        : `<div class="ph"><img src="images/p${p.id}.jpg" alt="${p.name}" loading="lazy"></div>`;
      return `<a class="card" href="pieces/${p.slug}.html" data-cursor="View">${ph}<div class="tx"><h3>${p.name}</h3><span class="meta">${v.n} · ${v.name}</span></div><p class="ds">${p.desc}</p></a>`;
    }
    function render(scroll) {
      $$("button", fl).forEach(b => b.setAttribute("aria-pressed", b.dataset.cat === st.cat));
      vs.value = st.vol;
      const list = PIECES.filter(p => (st.cat === "all" || p.cat === st.cat) && (st.vol === "all" || p.vol === st.vol));
      if (st.vol !== "all") {
        const v = VOLS[st.vol];
        intro.hidden = false;
        intro.innerHTML = `<span class="n">${v.n}</span><h2>${v.name}<span lang="ur">${v.ur}</span></h2><p>${v.story}</p>`;
      } else intro.hidden = true;
      count.textContent = `${list.length} ${list.length === 1 ? "piece" : "pieces"}`;
      grid.innerHTML = list.length ? list.map(card).join("") : `<p class="empty">Nothing in this combination yet. Choose another room or volume, or send us your own pin.</p>`;
      if (hasGSAP && !reduce) gsap.from(grid.children, { opacity: 0, y: 30, duration: .9, stagger: .05, ease: "power3.out" });
      if (scroll) { const top = $(".filters").getBoundingClientRect().top + scrollY - 10; lenis ? lenis.scrollTo(top) : scrollTo({ top, behavior: "smooth" }); }
      if (hasGSAP) ScrollTrigger.refresh();
    }
    render(false);
  }
})();
