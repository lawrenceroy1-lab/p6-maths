// Draws maths diagrams as SVG from a small description in the unit data file.
// spec = { w, h, pts: { A: [x, y], ... }, items: [ { t: "poly", p: ["A","B","C"] }, ... ] }
// Item types:
//   poly   p:[points] fill        filled shape with outline
//   seg    p:[a,b] dash color      straight line
//   circle c:point r fill dash     circle
//   dot    p:point                 small dot
//   pl     p:point d:[dx,dy] s     point name label (s = text, default the point name)
//   txt    at:[x,y] s size color anchor bold
//   ang    v a b s r               angle arc at vertex v between rays to a and b, label s
//   ra     v a b                   right angle mark
//   tick   p:[a,b] n               equal-side tick marks
//   len    p:[a,b] s off           length label beside a side
//   grid   x y cols rows size      square grid

const Diagram = (() => {
  const COLORS = { line: "#1f2a44", label: "#0D2B6B", angle: "#c2185b", len: "#1565c0" };

  function P(spec, p) { return Array.isArray(p) ? p : spec.pts[p]; }
  function f(n) { return Math.round(n * 10) / 10; }

  function render(spec) {
    if (!spec) return "";
    const out = [];
    const w = spec.w || 300, h = spec.h || 220;
    for (const it of spec.items || []) {
      const pt = q => P(spec, q);
      switch (it.t) {
        case "grid": {
          const s = it.size || 20;
          for (let i = 0; i <= it.cols; i++) out.push(`<line x1="${it.x + i * s}" y1="${it.y}" x2="${it.x + i * s}" y2="${it.y + it.rows * s}" stroke="#b0bec5" stroke-width="1"/>`);
          for (let j = 0; j <= it.rows; j++) out.push(`<line x1="${it.x}" y1="${it.y + j * s}" x2="${it.x + it.cols * s}" y2="${it.y + j * s}" stroke="#b0bec5" stroke-width="1"/>`);
          break;
        }
        case "poly": {
          const pts = it.p.map(pt).map(a => `${f(a[0])},${f(a[1])}`).join(" ");
          out.push(`<polygon points="${pts}" fill="${it.fill || "#fff3e0"}" stroke="${it.color || COLORS.line}" stroke-width="2.5" stroke-linejoin="round"/>`);
          break;
        }
        case "seg": {
          const [a, b] = it.p.map(pt);
          out.push(`<line x1="${f(a[0])}" y1="${f(a[1])}" x2="${f(b[0])}" y2="${f(b[1])}" stroke="${it.color || COLORS.line}" stroke-width="${it.width || 2.5}" ${it.dash ? 'stroke-dasharray="6 5"' : ""} stroke-linecap="round"/>`);
          break;
        }
        case "circle": {
          const c = pt(it.c);
          out.push(`<circle cx="${f(c[0])}" cy="${f(c[1])}" r="${it.r}" fill="${it.fill || "none"}" stroke="${it.color || COLORS.line}" stroke-width="2.5" ${it.dash ? 'stroke-dasharray="6 5"' : ""}/>`);
          break;
        }
        case "ell": {
          // ellipse; half: "front" (lower half only) or "back" (upper half only)
          const c = pt(it.c), rx = it.rx, ry = it.ry;
          const st = `fill="${it.fill || "none"}" stroke="${it.color || COLORS.line}" stroke-width="2.5" ${it.dash ? 'stroke-dasharray="6 5"' : ""}`;
          if (it.half === "front") out.push(`<path d="M${f(c[0] - rx)},${f(c[1])} A${rx},${ry} 0 0 0 ${f(c[0] + rx)},${f(c[1])}" ${st}/>`);
          else if (it.half === "back") out.push(`<path d="M${f(c[0] - rx)},${f(c[1])} A${rx},${ry} 0 0 1 ${f(c[0] + rx)},${f(c[1])}" ${st}/>`);
          else out.push(`<ellipse cx="${f(c[0])}" cy="${f(c[1])}" rx="${rx}" ry="${ry}" ${st}/>`);
          break;
        }
        case "sector": {
          // pie slice (or just the curve with open: true). a0, a1 in degrees, clockwise from 3 o'clock
          const c = pt(it.c), r = it.r;
          const rad = d => d * Math.PI / 180;
          const s = [c[0] + r * Math.cos(rad(it.a0)), c[1] + r * Math.sin(rad(it.a0))];
          const e = [c[0] + r * Math.cos(rad(it.a1)), c[1] + r * Math.sin(rad(it.a1))];
          const large = ((it.a1 - it.a0) % 360 + 360) % 360 > 180 ? 1 : 0;
          const arc = `A${r},${r} 0 ${large} 1 ${f(e[0])},${f(e[1])}`;
          const d = it.open ? `M${f(s[0])},${f(s[1])} ${arc}` : `M${f(c[0])},${f(c[1])} L${f(s[0])},${f(s[1])} ${arc} Z`;
          out.push(`<path d="${d}" fill="${it.open ? "none" : (it.fill || "none")}" stroke="${it.color || COLORS.line}" stroke-width="2.5" ${it.dash ? 'stroke-dasharray="6 5"' : ""}/>`);
          break;
        }
        case "dot": {
          const c = pt(it.p);
          out.push(`<circle cx="${f(c[0])}" cy="${f(c[1])}" r="${it.r || 4}" fill="${it.color || COLORS.line}"/>`);
          break;
        }
        case "pl": {
          const c = pt(it.p), d = it.d || [0, -10];
          out.push(text(c[0] + d[0], c[1] + d[1], it.s || it.p, { size: it.size || 20, color: COLORS.label, bold: true, anchor: "middle" }));
          break;
        }
        case "txt":
          out.push(text(it.at[0], it.at[1], it.s, { size: it.size || 18, color: it.color || COLORS.line, bold: it.bold, anchor: it.anchor || "middle" }));
          break;
        case "len": {
          const [a, b] = it.p.map(pt);
          const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
          let nx = -(b[1] - a[1]), ny = b[0] - a[0];
          const L = Math.hypot(nx, ny) || 1;
          let off = it.off;
          if (off === undefined) {
            // put the label on the outside: away from the middle of the shape
            const c = centre(spec);
            const side = (c[0] - mx) * nx + (c[1] - my) * ny;
            off = side > 0 ? -16 : 16;
          }
          out.push(text(mx + nx / L * off, my + ny / L * off + 6, it.s, { size: it.size || 17, color: COLORS.len, bold: true, anchor: "middle" }));
          break;
        }
        case "tick": {
          const [a, b] = it.p.map(pt);
          const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
          const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
          const ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
          const n = it.n || 1;
          for (let i = 0; i < n; i++) {
            const o = (i - (n - 1) / 2) * 6;
            const cx = mx + ux * o, cy = my + uy * o;
            out.push(`<line x1="${f(cx - nx * 7)}" y1="${f(cy - ny * 7)}" x2="${f(cx + nx * 7)}" y2="${f(cy + ny * 7)}" stroke="${COLORS.line}" stroke-width="2"/>`);
          }
          break;
        }
        case "ra": {
          const v = pt(it.v), a = pt(it.a), b = pt(it.b), s = it.size || 13;
          const u1 = unit(v, a), u2 = unit(v, b);
          const p1 = [v[0] + u1[0] * s, v[1] + u1[1] * s];
          const p3 = [v[0] + u2[0] * s, v[1] + u2[1] * s];
          const p2 = [p1[0] + u2[0] * s, p1[1] + u2[1] * s];
          out.push(`<polyline points="${f(p1[0])},${f(p1[1])} ${f(p2[0])},${f(p2[1])} ${f(p3[0])},${f(p3[1])}" fill="none" stroke="${COLORS.line}" stroke-width="2"/>`);
          break;
        }
        case "ang": {
          const v = pt(it.v), a = pt(it.a), b = pt(it.b), r = it.r || 26;
          let a1 = Math.atan2(a[1] - v[1], a[0] - v[0]);
          let a2 = Math.atan2(b[1] - v[1], b[0] - v[0]);
          let d = a2 - a1;
          while (d <= -Math.PI) d += 2 * Math.PI;
          while (d > Math.PI) d -= 2 * Math.PI;
          const sweep = d > 0 ? 1 : 0;
          const s1 = [v[0] + r * Math.cos(a1), v[1] + r * Math.sin(a1)];
          const s2 = [v[0] + r * Math.cos(a1 + d), v[1] + r * Math.sin(a1 + d)];
          const col = it.color || COLORS.angle;
          out.push(`<path d="M${f(s1[0])},${f(s1[1])} A${r},${r} 0 0 ${sweep} ${f(s2[0])},${f(s2[1])}" fill="none" stroke="${col}" stroke-width="2"/>`);
          if (it.s) {
            const mid = a1 + d / 2, lr = r + (it.lr || 18);
            out.push(text(v[0] + lr * Math.cos(mid), v[1] + lr * Math.sin(mid) + 6, it.s, { size: it.size || 17, color: col, bold: true, anchor: "middle" }));
          }
          break;
        }
      }
    }
    // grow the view so nothing is cut off at the edges
    let x0 = 0, y0 = 0, x1 = w, y1 = h;
    const grow = (x, y, pad) => { x0 = Math.min(x0, x - pad); y0 = Math.min(y0, y - pad); x1 = Math.max(x1, x + pad); y1 = Math.max(y1, y + pad); };
    Object.values(spec.pts || {}).forEach(p => grow(p[0], p[1], 30));
    for (const it of spec.items || []) {
      if (it.t === "circle") { const c = P(spec, it.c); grow(c[0] - it.r, c[1] - it.r, 8); grow(c[0] + it.r, c[1] + it.r, 8); }
      if (it.t === "sector") { const c = P(spec, it.c); grow(c[0] - it.r, c[1] - it.r, 8); grow(c[0] + it.r, c[1] + it.r, 8); }
      if (it.t === "ell") { const c = P(spec, it.c); grow(c[0] - it.rx, c[1] - it.ry, 8); grow(c[0] + it.rx, c[1] + it.ry, 8); }
      if (it.t === "poly" || it.t === "seg") it.p.forEach(q => { const c = P(spec, q); if (c) grow(c[0], c[1], 8); });
      if (it.t === "txt") grow(it.at[0], it.at[1], 20);
    }
    return `<svg class="diagram" viewBox="${f(x0)} ${f(y0)} ${f(x1 - x0)} ${f(y1 - y0)}" role="img" aria-label="diagram" xmlns="http://www.w3.org/2000/svg">${out.join("")}</svg>`;
  }

  function centre(spec) {
    const ps = Object.values(spec.pts || {});
    if (!ps.length) return [(spec.w || 300) / 2, (spec.h || 220) / 2];
    return [ps.reduce((s, p) => s + p[0], 0) / ps.length, ps.reduce((s, p) => s + p[1], 0) / ps.length];
  }

  function unit(v, a) {
    const dx = a[0] - v[0], dy = a[1] - v[1], L = Math.hypot(dx, dy) || 1;
    return [dx / L, dy / L];
  }

  function text(x, y, s, o) {
    return `<text x="${f(x)}" y="${f(y)}" font-size="${o.size}" fill="${o.color}" text-anchor="${o.anchor}" font-weight="${o.bold ? 800 : 600}" font-family="inherit" paint-order="stroke" stroke="#fff" stroke-width="4" stroke-linejoin="round">${esc(s)}</text>`;
  }

  return { render };
})();
