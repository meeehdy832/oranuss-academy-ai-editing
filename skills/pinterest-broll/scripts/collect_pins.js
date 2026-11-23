// Run on a Pinterest search page (https://www.pinterest.com/search/pins/?q=...) with the
// browser's JavaScript tool. Scrolls the grid, collects every image pin it sees, and returns
// JSON: [{id, url, alt, thumb, original, fallback, w, h, video}]. Pinterest keeps only the
// on-screen pins in the page, so pins are gathered while scrolling.
// Set window.__PIN_LIMIT before running to change how many pins to collect (default 40).
(async () => {
  const limit = window.__PIN_LIMIT || 40, found = new Map();
  const grab = () => {
    for (const a of document.querySelectorAll('a[href*="/pin/"]')) {
      const img = a.querySelector('img[src*="pinimg.com"]');
      if (!img) continue;
      const m = new URL(a.getAttribute("href"), location.origin).pathname.match(/\/pin\/([^/]+)/);
      if (!m || found.has(m[1])) continue;
      const card = a.closest('[data-grid-item="true"], [role="listitem"]') || a.parentElement;
      const src = img.currentSrc || img.src;
      const title = ((card && card.innerText) || "").split("\n").map(s => s.trim()).filter(Boolean).join(" · ").slice(0, 140);
      const stock = /pngtree|freepik|vecteezy|shutterstock|dreamstime|istock|gettyimages|depositphotos|123rf|alamy|adobe ?stock|canstock|pngwing|cleanpng|pngegg|png transparent image and clipart|for free download|royalty[- ]free|stock (photo|illustration|vector)/i
        .test(title + " " + (img.alt || "") + " " + a.getAttribute("href"));
      found.set(m[1], {
        title, stock,
        id: m[1],
        url: "https://www.pinterest.com/pin/" + m[1] + "/",
        alt: (img.alt || "").replace(/^This may contain:\s*/i, "").slice(0, 160),
        thumb: src,
        original: src.replace(/\/\d+x(\d+)?\//, "/originals/"),
        fallback: src.replace(/\/\d+x(\d+)?\//, "/736x/"),
        w: img.naturalWidth, h: img.naturalHeight,
        video: !!(card && card.querySelector("video")),
      });
    }
  };
  grab();
  for (let i = 0; i < 14 && found.size < limit; i++) {
    window.scrollBy(0, Math.round(innerHeight * 0.9));
    await new Promise(r => setTimeout(r, 900));
    grab();
  }
  window.scrollTo(0, 0);
  const pins = [...found.values()].filter(p => !p.video).slice(0, limit);
  pins.forEach((p, i) => (p.n = i));
  window.__pins = pins;
  // Number badges on the grid, so a screenshot shows which number is which image.
  await new Promise(r => setTimeout(r, 700));
  document.querySelectorAll(".__pinbadge").forEach(b => b.remove());
  const byId = new Map(pins.map(p => [p.id, p.n]));
  for (const a of document.querySelectorAll('a[href*="/pin/"]')) {
    const m = new URL(a.getAttribute("href"), location.origin).pathname.match(/\/pin\/([^/]+)/);
    if (!m || !byId.has(m[1]) || a.querySelector(".__pinbadge")) continue;
    const b = document.createElement("div");
    b.className = "__pinbadge"; b.textContent = byId.get(m[1]);
    b.style.cssText = "position:absolute;left:8px;top:8px;z-index:9;min-width:34px;height:34px;padding:0 8px;border-radius:17px;background:#5B2BE0;color:#fff;font:700 18px/34px system-ui;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.4)";
    if (getComputedStyle(a).position === "static") a.style.position = "relative";
    a.appendChild(b);
  }
  // Pick later with: JSON.stringify({main: __pins[N], backup: __pins[M]})
  return JSON.stringify(pins.map(p => ({ n: p.n, id: p.id, w: p.w, h: p.h, stock: p.stock, title: p.title, alt: p.alt })));
})();
