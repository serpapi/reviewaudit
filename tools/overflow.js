// Paste into the console on the docket page: loads every case in hidden iframes at five widths and lists any
// element that leaks past its card (or the page). Prints "clean" when nothing does.
(async () => {
  const links = [...document.querySelectorAll('td.t a')].map(a => a.getAttribute('href'));
  const out = {};
  for (const w of [1395, 1000, 700, 400, 360]) {
    for (const href of links) {
      const f = document.createElement('iframe');
      f.style.cssText = `width:${w}px;height:900px;position:absolute;left:-9999px;top:0`;
      f.src = href + '?overflow=' + Date.now();
      document.body.appendChild(f);
      await new Promise(r => { f.onload = r; });
      await new Promise(r => setTimeout(r, 250));
      const d = f.contentDocument;
      d.querySelectorAll('details').forEach(x => x.open = true);
      for (const box of d.querySelectorAll('.card, .hero, main')) {
        const c = box.getBoundingClientRect(), hits = new Set();
        for (const el of box.querySelectorAll('*')) {
          if (el.closest('.tip, .map, .scroll')) continue;
          const r = el.getBoundingClientRect();
          if (r.width && r.right > c.right + 1) hits.add(`${el.tagName.toLowerCase()}+${Math.round(r.right - c.right)}`);
        }
        if (hits.size) (out[`${w} #${box.id || box.tagName} ${[...hits].slice(0, 5).join(' ')}`] ??= []).push(href);
      }
      if (d.documentElement.scrollWidth > w + 1) (out[`${w} page scrolls sideways`] ??= []).push(href);
      f.remove();
    }
  }
  console.log(Object.entries(out).map(([k, v]) => `${k}  <- ${v.length}, e.g. ${v[0]}`).join('\n') || 'clean');
})();
