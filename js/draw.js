// Draw on the page (for the smart board): pen, colours, eraser, clear. Works with mouse, finger and pen.
(() => {
  const css = `
  .dp-btn { position: fixed; right: 14px; bottom: 14px; z-index: 80; background: #0D2B6B; color: #fff; border: 0; border-radius: 999px; padding: 12px 18px; font: inherit; font-weight: 900; font-size: 18px; box-shadow: 0 4px 12px rgba(0,0,0,.25); cursor: pointer; }
  .dp-canvas { position: fixed; inset: 0; z-index: 70; touch-action: none; cursor: crosshair; display: none; }
  .dp-bar { position: fixed; left: 50%; transform: translateX(-50%); bottom: 12px; z-index: 81; display: none; gap: 6px; background: #fff; border: 3px solid #0D2B6B; border-radius: 16px; padding: 6px 8px; box-shadow: 0 4px 14px rgba(0,0,0,.25); flex-wrap: wrap; justify-content: center; max-width: calc(100vw - 24px); }
  .dp-bar button { border: 2px solid #dfe5ef; background: #fff; border-radius: 10px; min-width: 40px; height: 40px; font: inherit; font-weight: 900; font-size: 16px; cursor: pointer; }
  .dp-bar button.on { outline: 3px solid #FFB300; }
  .dp-dot { display: inline-block; width: 20px; height: 20px; border-radius: 50%; vertical-align: middle; }
  body.dp-on .dp-canvas, body.dp-on .dp-bar { display: flex; }
  body.dp-on .dp-canvas { display: block; }
  body.dp-on .dp-btn { display: none; }
  body.dp-pass .dp-canvas { pointer-events: none; }
  @media print { .dp-btn, .dp-bar, .dp-canvas { display: none !important; } }`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  const btn = document.createElement("button");
  btn.className = "dp-btn no-print"; btn.textContent = "✏️ Draw"; btn.title = "Write on the page";
  const cv = document.createElement("canvas"); cv.className = "dp-canvas";
  const bar = document.createElement("div"); bar.className = "dp-bar";
  const COLORS = ["#E53935", "#1E88E5", "#1f2a44", "#2E7D32", "#FB8C00"];
  bar.innerHTML = COLORS.map((c, i) => `<button data-c="${c}" class="${i === 0 ? "on" : ""}" title="Pen"><span class="dp-dot" style="background:${c}"></span></button>`).join("")
    + `<button data-w="4" title="Thin">✒️</button><button data-w="9" class="on" title="Thick">🖍️</button>`
    + `<button data-e="1" title="Eraser">🧽</button><button data-pass="1" title="Click buttons on the page, keep the writing">👆 Click page</button><button data-clear="1" title="Clear all">🧹 Clear</button><button data-close="1" title="Stop drawing">✖ Close</button>`;
  document.body.append(cv, bar, btn);

  const ctx = cv.getContext("2d");
  let color = COLORS[0], width = 9, erase = false, down = false, last = null;
  function size() {
    const r = window.devicePixelRatio || 1, img = cv.width ? ctx.getImageData(0, 0, cv.width, cv.height) : null;
    cv.width = innerWidth * r; cv.height = innerHeight * r;
    cv.style.width = innerWidth + "px"; cv.style.height = innerHeight + "px";
    ctx.setTransform(r, 0, 0, r, 0, 0);
    if (img) ctx.putImageData(img, 0, 0);
  }
  size(); addEventListener("resize", size);

  const pos = e => [e.clientX, e.clientY];
  cv.addEventListener("pointerdown", e => { down = true; last = pos(e); cv.setPointerCapture(e.pointerId); dot(last); });
  cv.addEventListener("pointermove", e => { if (!down) return; const p = pos(e); line(last, p); last = p; });
  ["pointerup", "pointercancel", "pointerleave"].forEach(t => cv.addEventListener(t, () => { down = false; }));
  function style() {
    ctx.globalCompositeOperation = erase ? "destination-out" : "source-over";
    ctx.strokeStyle = ctx.fillStyle = color; ctx.lineWidth = erase ? 34 : width; ctx.lineCap = ctx.lineJoin = "round";
  }
  function line(a, b) { style(); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); }
  function dot(p) { style(); ctx.beginPath(); ctx.arc(p[0], p[1], (erase ? 34 : width) / 2, 0, Math.PI * 2); ctx.fill(); }
  function clear() { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height); ctx.restore(); }

  btn.onclick = () => document.body.classList.add("dp-on");
  bar.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.dataset.c || b.dataset.w || b.dataset.e) { document.body.classList.remove("dp-pass"); const pb = bar.querySelector("[data-pass]"); pb.classList.remove("on"); pb.textContent = "👆 Click page"; }
    if (b.dataset.c) { color = b.dataset.c; erase = false; bar.querySelectorAll("[data-c],[data-e]").forEach(x => x.classList.toggle("on", x === b)); }
    if (b.dataset.w) { width = +b.dataset.w; erase = false; bar.querySelectorAll("[data-w]").forEach(x => x.classList.toggle("on", x === b)); }
    if (b.dataset.e) { erase = true; bar.querySelectorAll("[data-c],[data-e]").forEach(x => x.classList.toggle("on", x === b)); }
    if (b.dataset.pass) { const p = document.body.classList.toggle("dp-pass"); b.classList.toggle("on", p); b.textContent = p ? "✏️ Write again" : "👆 Click page"; }
    if (b.dataset.clear) clear();
    if (b.dataset.close) { document.body.classList.remove("dp-on", "dp-pass"); const pb = bar.querySelector("[data-pass]"); pb.classList.remove("on"); pb.textContent = "👆 Click page"; clear(); }
  });
  window.DrawPad = { clear };
})();
