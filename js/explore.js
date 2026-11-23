// Interactive explorers for the "Explore" tab. Plain SVG, no libraries.
// Explore.triangle(el, mode) · Explore.circle(el) · Explore.compass(el) · Explore.solid(el) · Explore.net(el)
const Explore = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const R2D = 180 / Math.PI;
  const f1 = n => (Math.round(n * 10) / 10).toFixed(1).replace(/\.0$/, "");
  const COL = { A: "#E53935", B: "#1E88E5", C: "#2E7D32" };
  const T = (en, th) => (typeof thaiOn === "function" && !thaiOn() ? en : `${en}<span class="th">${th}</span>`);

  function svgPoint(svg, e) {
    const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }
  // Makes an element draggable. onMove(x, y) gets SVG coordinates.
  function draggable(svg, el, onMove) {
    el.addEventListener("pointerdown", e => {
      e.preventDefault(); el.setPointerCapture(e.pointerId);
      const move = ev => { const p = svgPoint(svg, ev); onMove(p.x, p.y); };
      const up = () => { el.removeEventListener("pointermove", move); el.removeEventListener("pointerup", up); el.removeEventListener("pointercancel", up); };
      el.addEventListener("pointermove", move); el.addEventListener("pointerup", up); el.addEventListener("pointercancel", up);
    });
  }
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const arcPath = (cx, cy, r, a0, a1) => { // angles in degrees, SVG y down, counter-clockwise visually
    const p = a => [cx + r * Math.cos(a / R2D), cy - r * Math.sin(a / R2D)];
    const [x0, y0] = p(a0), [x1, y1] = p(a1);
    return `M${cx},${cy} L${x0},${y0} A${r},${r} 0 ${a1 - a0 > 180 ? 1 : 0} 0 ${x1},${y1} Z`;
  };
  // rounds 3 angles so they still add up to exactly 180
  function round180(a) {
    const r = a.map(Math.round); let d = 180 - r.reduce((s, v) => s + v, 0);
    const order = a.map((v, i) => [v - Math.round(v), i]).sort((x, y) => d > 0 ? y[0] - x[0] : x[0] - y[0]);
    for (let k = 0; d !== 0 && k < 3; k++) { r[order[k][1]] += Math.sign(d); d -= Math.sign(d); }
    return r;
  }

  // ================= TRIANGLE =================
  function triangle(el, mode) {
    const PX = 40; // 40 px = 1 cm
    const PRE = {
      "Equilateral|ด้านเท่า": { A: [200, 66.795], B: [100, 240], C: [300, 240] },
      "Isosceles|หน้าจั่ว": { A: [200, 60], B: [120, 240], C: [280, 240] },
      "Scalene|ด้านไม่เท่า": { A: [140, 70], B: [60, 240], C: [320, 240] },
      "Right|มุมฉาก": { A: [100, 60], B: [100, 240], C: [320, 240] },
      "Obtuse|มุมป้าน": { A: [330, 120], B: [60, 240], C: [240, 240] },
      "Acute|มุมแหลม": { A: [180, 50], B: [80, 240], C: [320, 240] },
    };
    let P = JSON.parse(JSON.stringify(PRE["Scalene|ด้านไม่เท่า"]));
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("👆 Drag the red, blue and green dots. Or tap a button:", "ลากจุดสีแดง น้ำเงิน และเขียว หรือแตะปุ่ม:")}</p>
      <div class="ex-btns">${Object.keys(PRE).map(k => `<button class="chip" data-k="${k}">${T(...k.split("|"))}</button>`).join("")}</div>
      <svg class="ex-svg" viewBox="0 0 400 290"></svg>
      ${mode === "sum" ? `<svg class="ex-svg ex-line" viewBox="0 0 400 150"></svg>` : ""}
      <div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), line = el.querySelector(".ex-line"), info = el.querySelector(".ex-info");
    el.querySelectorAll(".chip").forEach(b => b.onclick = () => { P = JSON.parse(JSON.stringify(PRE[b.dataset.k])); draw(); });
    const len = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);
    const ang = (v, p, q) => { const a = [p[0] - v[0], p[1] - v[1]], b = [q[0] - v[0], q[1] - v[1]]; return Math.acos(clamp((a[0] * b[0] + a[1] * b[1]) / (Math.hypot(...a) * Math.hypot(...b)), -1, 1)) * R2D; };
    function draw() {
      const { A, B, C } = P;
      const s = { a: f1(len(B, C) / PX), b: f1(len(A, C) / PX), c: f1(len(A, B) / PX) }; // a opposite A
      const [ra, rb, rc] = round180([ang(A, B, C), ang(B, A, C), ang(C, A, B)]);
      const eq = [s.c === s.a, s.a === s.b, s.b === s.c]; // AB=BC, BC=CA, CA=AB
      const nEq = s.a === s.b && s.b === s.c ? 3 : eq.some(x => x) ? 2 : 0;
      const bySide = nEq === 3 ? ["Equilateral", "ด้านเท่า", "3 equal sides", "ด้านเท่ากัน 3 ด้าน"] : nEq === 2 ? ["Isosceles", "หน้าจั่ว", "2 equal sides", "ด้านเท่ากัน 2 ด้าน"] : ["Scalene", "ด้านไม่เท่า", "no equal sides", "ไม่มีด้านเท่ากัน"];
      const mx = Math.max(ra, rb, rc);
      const byAng = mx === 90 ? ["Right", "มุมฉาก", "one angle is 90°", "มีมุม 90° หนึ่งมุม"] : mx > 90 ? ["Obtuse", "มุมป้าน", "one angle is more than 90°", "มีมุมหนึ่งใหญ่กว่า 90°"] : ["Acute", "มุมแหลม", "all angles are less than 90°", "ทุกมุมเล็กกว่า 90°"];
      const tick = (p, q, n) => { const mxp = (p[0] + q[0]) / 2, myp = (p[1] + q[1]) / 2, L = len(p, q), ux = (q[0] - p[0]) / L, uy = (q[1] - p[1]) / L; let o = ""; for (let i = 0; i < n; i++) { const d = (i - (n - 1) / 2) * 6; o += `<line x1="${mxp + ux * d - uy * 8}" y1="${myp + uy * d + ux * 8}" x2="${mxp + ux * d + uy * 8}" y2="${myp + uy * d - ux * 8}" stroke="#1f2a44" stroke-width="2.5"/>`; } return o; };
      let ticks = "";
      if (nEq === 3) ticks = tick(A, B, 1) + tick(B, C, 1) + tick(C, A, 1);
      else if (nEq === 2) { if (eq[0]) ticks = tick(A, B, 1) + tick(B, C, 1); else if (eq[1]) ticks = tick(B, C, 1) + tick(C, A, 1); else ticks = tick(C, A, 1) + tick(A, B, 1); }
      const arc = (v, p, q, deg, col) => {
        const a1 = Math.atan2(-(p[1] - v[1]), p[0] - v[0]) * R2D, a2 = Math.atan2(-(q[1] - v[1]), q[0] - v[0]) * R2D;
        let s0 = a1, d = ((a2 - a1) % 360 + 360) % 360; if (d > 180) { s0 = a2; d = 360 - d; }
        const mid = (s0 + d / 2) / R2D, rr = 30;
        if (deg === 90) {
          const u = [(p[0] - v[0]) / len(v, p), (p[1] - v[1]) / len(v, p)], w = [(q[0] - v[0]) / len(v, q), (q[1] - v[1]) / len(v, q)], k = 16;
          return `<polyline points="${v[0] + u[0] * k},${v[1] + u[1] * k} ${v[0] + (u[0] + w[0]) * k},${v[1] + (u[1] + w[1]) * k} ${v[0] + w[0] * k},${v[1] + w[1] * k}" fill="none" stroke="${col}" stroke-width="2.5"/>
            <text x="${v[0] + Math.cos(mid) * 48}" y="${v[1] - Math.sin(mid) * 48 + 6}" class="ex-lab" fill="${col}">${deg}°</text>`;
        }
        return `<path d="${arcPath(v[0], v[1], rr, s0, s0 + d)}" fill="${col}" fill-opacity=".18" stroke="${col}" stroke-width="2"/>
          <text x="${v[0] + Math.cos(mid) * 50}" y="${v[1] - Math.sin(mid) * 50 + 6}" class="ex-lab" fill="${col}">${deg}°</text>`;
      };
      const side = (p, q, t, o) => { const mxp = (p[0] + q[0]) / 2, myp = (p[1] + q[1]) / 2, cx = (A[0] + B[0] + C[0]) / 3, cy = (A[1] + B[1] + C[1]) / 3, dx = mxp - cx, dy = myp - cy, L = Math.hypot(dx, dy) || 1; return `<text x="${mxp + dx / L * 22}" y="${myp + dy / L * 22 + 5}" class="ex-len">${t} cm</text>`; };
      svg.innerHTML = `<polygon points="${A} ${B} ${C}" fill="#FFF59D" stroke="#1f2a44" stroke-width="3" stroke-linejoin="round"/>
        ${arc(A, B, C, ra, COL.A)}${arc(B, A, C, rb, COL.B)}${arc(C, A, B, rc, COL.C)}${ticks}
        ${side(B, C, s.a)}${side(A, C, s.b)}${side(A, B, s.c)}
        ${["A", "B", "C"].map(k => `<circle class="ex-h" data-k="${k}" cx="${P[k][0]}" cy="${P[k][1]}" r="13" fill="${COL[k]}" stroke="#fff" stroke-width="3"/>`).join("")}`;
      svg.querySelectorAll(".ex-h").forEach(h => draggable(svg, h, (x, y) => { P[h.dataset.k] = [clamp(Math.round(x / 5) * 5, 20, 380), clamp(Math.round(y / 5) * 5, 20, 270)]; draw(); }));
      info.innerHTML = `<div class="ex-row"><b>${T("Sides", "ด้าน")}:</b> ${s.c} cm, ${s.a} cm, ${s.b} cm ➡ <b class="ex-name">${T(bySide[0], bySide[1])}</b> <span class="small">(${bySide[2]} · ${bySide[3]})</span></div>
        <div class="ex-row"><b>${T("Angles", "มุม")}:</b> <span style="color:${COL.A}">${ra}°</span> + <span style="color:${COL.B}">${rb}°</span> + <span style="color:${COL.C}">${rc}°</span> = <b>180°</b> ➡ <b class="ex-name">${T(byAng[0], byAng[1])}</b> <span class="small">(${byAng[2]} · ${byAng[3]})</span></div>`;
      if (line) {
        let a0 = 0;
        line.innerHTML = `<line x1="40" y1="120" x2="360" y2="120" stroke="#1f2a44" stroke-width="3"/>` +
          [[ra, COL.A], [rb, COL.B], [rc, COL.C]].map(([d, c]) => { const m = (a0 + d / 2) / R2D; const o = `<path d="${arcPath(200, 120, 95, a0, a0 + d)}" fill="${c}" fill-opacity=".35" stroke="${c}" stroke-width="2"/><text x="${200 + Math.cos(m) * 62}" y="${120 - Math.sin(m) * 62 + 6}" class="ex-lab" fill="${c}">${d}°</text>`; a0 += d; return o; }).join("") +
          `<text x="200" y="146" class="ex-cap">3 corners together = a straight line = 180°</text>`;
        info.innerHTML += `<div class="ex-row small">${T("Tear off the 3 corners and put them side by side: they always make a straight line (180°).", "ฉีกมุมทั้ง 3 มาวางเรียงกัน จะได้เส้นตรงเสมอ (180°)")}</div>`;
      }
    }
    draw();
  }

  // ================= CIRCLE =================
  function circle(el) {
    const PX = 30, O = [200, 150];
    let r = 3, aP = 40, aD = 160, c1 = 215, c2 = 320;
    const show = { radius: true, diameter: true, chord: true, circ: false };
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("👆 Drag the dots on the edge. Change the radius with the slider.", "ลากจุดบนขอบวงกลม เปลี่ยนรัศมีด้วยแถบเลื่อน")}</p>
      <div class="ex-btns">${[["radius", "Radius", "รัศมี"], ["diameter", "Diameter", "เส้นผ่านศูนย์กลาง"], ["chord", "Chord", "คอร์ด"], ["circ", "Circumference", "เส้นรอบวง"]].map(([k, e, t]) => `<button class="chip ${show[k] ? "on" : ""}" data-k="${k}">${T(e, t)}</button>`).join("")}</div>
      <label class="ex-slider">${T("Radius", "รัศมี")}: <input type="range" min="1" max="4" step="0.5" value="${r}"> <b class="rv"></b></label>
      <svg class="ex-svg" viewBox="0 0 400 300"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelector("input").oninput = e => { r = +e.target.value; draw(); };
    el.querySelectorAll(".chip").forEach(b => b.onclick = () => { show[b.dataset.k] = !show[b.dataset.k]; b.classList.toggle("on"); draw(); });
    const at = a => [O[0] + r * PX * Math.cos(a / R2D), O[1] - r * PX * Math.sin(a / R2D)];
    function draw() {
      const R = r * PX, P = at(aP), D1 = at(aD), D2 = at(aD + 180), Q1 = at(c1), Q2 = at(c2);
      let dd = Math.abs(((c2 - c1) % 360 + 360) % 360); if (dd > 180) dd = 360 - dd;
      const chord = 2 * r * Math.sin(dd / 2 / R2D);
      const h = (k, p, col) => `<circle class="ex-h" data-k="${k}" cx="${p[0]}" cy="${p[1]}" r="11" fill="${col}" stroke="#fff" stroke-width="3"/>`;
      svg.innerHTML = `<circle cx="${O[0]}" cy="${O[1]}" r="${R}" fill="#E3F2FD" stroke="${show.circ ? "#FB8C00" : "#1f2a44"}" stroke-width="${show.circ ? 7 : 3}"/>
        ${show.diameter ? `<line x1="${D1[0]}" y1="${D1[1]}" x2="${D2[0]}" y2="${D2[1]}" stroke="#1E88E5" stroke-width="5"/>` : ""}
        ${show.radius ? `<line x1="${O[0]}" y1="${O[1]}" x2="${P[0]}" y2="${P[1]}" stroke="#E53935" stroke-width="5"/>` : ""}
        ${show.chord ? `<line x1="${Q1[0]}" y1="${Q1[1]}" x2="${Q2[0]}" y2="${Q2[1]}" stroke="#2E7D32" stroke-width="5"/>` : ""}
        <circle cx="${O[0]}" cy="${O[1]}" r="6" fill="#1f2a44"/><text x="${O[0] - 16}" y="${O[1] + 22}" class="ex-lab">O</text>
        ${show.radius ? h("P", P, "#E53935") : ""}${show.diameter ? h("D", D1, "#1E88E5") : ""}${show.chord ? h("Q1", Q1, "#2E7D32") + h("Q2", Q2, "#2E7D32") : ""}`;
      svg.querySelectorAll(".ex-h").forEach(hd => draggable(svg, hd, (x, y) => {
        const a = Math.round(Math.atan2(-(y - O[1]), x - O[0]) * R2D / 5) * 5;
        ({ P: () => aP = a, D: () => aD = a, Q1: () => c1 = a, Q2: () => c2 = a })[hd.dataset.k](); draw();
      }));
      el.querySelector(".rv").textContent = `${f1(r)} cm`;
      const rows = [];
      if (show.radius) rows.push(`<span style="color:#E53935">■</span> <b>${T("Radius", "รัศมี")}</b> = ${f1(r)} cm · ${T("center to edge", "จากจุดศูนย์กลางถึงขอบ")}`);
      if (show.diameter) rows.push(`<span style="color:#1E88E5">■</span> <b>${T("Diameter", "เส้นผ่านศูนย์กลาง")}</b> = 2 × ${f1(r)} = <b>${f1(2 * r)} cm</b> · ${T("through the center", "ผ่านจุดศูนย์กลาง")}`);
      if (show.chord) rows.push(`<span style="color:#2E7D32">■</span> <b>${T("Chord", "คอร์ด")}</b> = ${f1(chord)} cm · ${dd === 180 ? T("this chord goes through O, so it is a diameter!", "คอร์ดนี้ผ่าน O จึงเป็นเส้นผ่านศูนย์กลาง!") : T("shorter than the diameter", "สั้นกว่าเส้นผ่านศูนย์กลาง")}`);
      if (show.circ) rows.push(`<span style="color:#FB8C00">■</span> <b>${T("Circumference", "เส้นรอบวง")}</b>: ${T("the distance all the way round", "ระยะทางรอบวงกลมทั้งวง")}`);
      info.innerHTML = rows.map(x => `<div class="ex-row">${x}</div>`).join("");
    }
    draw();
  }

  // ================= COMPASS =================
  function compass(el) {
    const PX = 30, O = [200, 165];
    let r = 2, swept = 0, last = null, start = null, done = false, task = null;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("1. Set the compass gap (the radius). 2. Drag the pencil ✏️ all the way round.", "1. กางวงเวียน (รัศมี) 2. ลากดินสอ ✏️ ให้ครบรอบ")}</p>
      <div class="ex-btns"><button class="chip" data-t="1">${T("🎯 Give me a task", "ขอโจทย์")}</button><button class="chip" data-t="0">${T("🔁 Clear", "ลบ")}</button></div>
      <div class="ex-task"></div>
      <label class="ex-slider">${T("Compass gap (radius)", "ระยะกางวงเวียน (รัศมี)")}: <input type="range" min="1" max="4" step="0.5" value="${r}"> <b class="rv"></b></label>
      <svg class="ex-svg" viewBox="0 0 400 310"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info"), tk = el.querySelector(".ex-task");
    const reset = () => { swept = 0; last = null; start = null; done = false; };
    el.querySelector("input").oninput = e => { r = +e.target.value; reset(); draw(); };
    el.querySelectorAll(".chip").forEach(b => b.onclick = () => {
      reset();
      if (b.dataset.t === "1") {
        const useD = Math.random() < 0.5, rad = [1.5, 2, 2.5, 3, 3.5, 4][Math.floor(Math.random() * 6)];
        task = { rad, text: useD ? T(`Draw a circle with diameter ${f1(rad * 2)} cm.`, `วาดวงกลมที่มีเส้นผ่านศูนย์กลาง ${f1(rad * 2)} cm`) : T(`Draw a circle with radius ${f1(rad)} cm.`, `วาดวงกลมที่มีรัศมี ${f1(rad)} cm`) };
      } else task = null;
      draw();
    });
    let ang = 0;
    function draw() {
      const R = r * PX, P = [O[0] + R * Math.cos(ang / R2D), O[1] - R * Math.sin(ang / R2D)];
      const H = [(O[0] + P[0]) / 2, Math.min(O[1], P[1]) - 120];
      let trace = "";
      if (done) trace = `<circle cx="${O[0]}" cy="${O[1]}" r="${R}" fill="none" stroke="#7E57C2" stroke-width="4"/>`;
      else if (start !== null && Math.abs(swept) > 1) {
        const a0 = swept > 0 ? start : start + swept, a1 = a0 + Math.abs(swept);
        const p = a => [O[0] + R * Math.cos(a / R2D), O[1] - R * Math.sin(a / R2D)];
        const [x0, y0] = p(a0), [x1, y1] = p(a1);
        trace = `<path d="M${x0},${y0} A${R},${R} 0 ${a1 - a0 > 180 ? 1 : 0} 0 ${x1},${y1}" fill="none" stroke="#7E57C2" stroke-width="4"/>`;
      }
      svg.innerHTML = `<circle cx="${O[0]}" cy="${O[1]}" r="${R}" fill="none" stroke="#cfd8dc" stroke-dasharray="4 6" stroke-width="1.5"/>${trace}
        <line x1="${H[0]}" y1="${H[1]}" x2="${O[0]}" y2="${O[1]}" stroke="#78909C" stroke-width="7" stroke-linecap="round"/>
        <line x1="${H[0]}" y1="${H[1]}" x2="${P[0]}" y2="${P[1]}" stroke="#FFB300" stroke-width="7" stroke-linecap="round"/>
        <circle cx="${H[0]}" cy="${H[1]}" r="9" fill="#455A64"/>
        <circle cx="${O[0]}" cy="${O[1]}" r="5" fill="#1f2a44"/><text x="${O[0] - 18}" y="${O[1] + 22}" class="ex-lab">O</text>
        <line x1="${O[0]}" y1="${O[1] + 32}" x2="${O[0] + R}" y2="${O[1] + 32}" stroke="#E53935" stroke-width="2"/><text x="${O[0] + R / 2}" y="${O[1] + 50}" class="ex-len" fill="#E53935">${f1(r)} cm</text>
        <circle class="ex-h" cx="${P[0]}" cy="${P[1]}" r="15" fill="#FFB300" stroke="#fff" stroke-width="3"/><text x="${P[0]}" y="${P[1] + 6}" class="ex-lab" style="pointer-events:none">✏️</text>`;
      const h = svg.querySelector(".ex-h");
      draggable(svg, h, (x, y) => {
        const a = Math.atan2(-(y - O[1]), x - O[0]) * R2D;
        if (last === null) { last = a; start = a; }
        let d = a - last; if (d > 180) d -= 360; if (d < -180) d += 360;
        swept += d; last = a; ang = a;
        if (Math.abs(swept) >= 360) done = true;
        draw();
      });
      el.querySelector(".rv").textContent = `${f1(r)} cm`;
      tk.innerHTML = task ? `<div class="ex-row">🎯 ${task.text}</div>` : "";
      let msg = done ? T(`⭕ Circle complete! Radius ${f1(r)} cm, diameter ${f1(2 * r)} cm.`, `วาดวงกลมเสร็จแล้ว! รัศมี ${f1(r)} cm เส้นผ่านศูนย์กลาง ${f1(2 * r)} cm`)
        : T(`Keep going: ${Math.round(Math.min(Math.abs(swept), 360) / 3.6)}% of the way round.`, `หมุนต่อไป: ไปได้ ${Math.round(Math.min(Math.abs(swept), 360) / 3.6)}% ของรอบ`);
      if (done && task) msg += task.rad === r ? `<div class="result ok">✅ ${T("Correct! The compass gap was the radius.", "ถูกต้อง! ระยะกางวงเวียนคือรัศมี")}</div>` : `<div class="result no">❌ ${T("Not this size. Remember: open the compass to the radius (half the diameter).", "ยังไม่ใช่ขนาดนี้ จำไว้: กางวงเวียนเท่ากับรัศมี (ครึ่งหนึ่งของเส้นผ่านศูนย์กลาง)")}</div>`;
      info.innerHTML = `<div class="ex-row">${msg}</div>`;
    }
    draw();
  }

  // ================= 3D helpers =================
  const rot = (p, yaw, pitch) => {
    const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    const x = p[0] * cy + p[2] * sy, z = -p[0] * sy + p[2] * cy;
    return [x, p[1] * cp - z * sp, p[1] * sp + z * cp];
  };
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const norm = a => { const l = Math.hypot(...a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  function viewDrag(svg, state, redraw) {
    let p0 = null;
    svg.addEventListener("pointerdown", e => { if (e.target.closest(".ex-h")) return; p0 = [e.clientX, e.clientY, state.yaw, state.pitch]; state.auto = false; svg.setPointerCapture(e.pointerId); });
    svg.addEventListener("pointermove", e => { if (!p0) return; state.yaw = p0[2] + (e.clientX - p0[0]) / 90; state.pitch = clamp(p0[3] + (e.clientY - p0[1]) / 90, -1.4, 1.4); redraw(); });
    const up = () => { p0 = null; };
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
  }

  // ================= SOLIDS =================
  const poly = (n, r, y, off = 0) => Array.from({ length: n }, (_, i) => [r * Math.cos(2 * Math.PI * i / n + off), y, r * Math.sin(2 * Math.PI * i / n + off)]);
  function prismOf(base, h) { const n = base.length, v = base.map(p => [p[0], -h, p[2]]).concat(base.map(p => [p[0], h, p[2]])); const f = [[...Array(n).keys()], [...Array(n).keys()].map(i => i + n)]; for (let i = 0; i < n; i++) f.push([i, (i + 1) % n, (i + 1) % n + n, i + n]); return { v, f }; }
  function pyramidOf(base, top) { const n = base.length, v = base.concat([top]); const f = [[...Array(n).keys()]]; for (let i = 0; i < n; i++) f.push([i, (i + 1) % n, n]); return { v, f }; }
  const SOLIDS = {
    cube: ["Cube", "ลูกบาศก์", () => prismOf(poly(4, 1.41, 0, Math.PI / 4), 1)],
    cuboid: ["Cuboid", "ทรงสี่เหลี่ยมมุมฉาก", () => { const s = prismOf([[-1.6, 0, -0.8], [1.6, 0, -0.8], [1.6, 0, 0.8], [-1.6, 0, 0.8]], 0.9); return s; }],
    tprism: ["Triangular prism", "ปริซึมสามเหลี่ยม", () => { const s = prismOf(poly(3, 1.1, 0, Math.PI / 2), 1.3); s.v = s.v.map(p => [p[0], p[2], p[1]]); return s; }],
    pprism: ["Pentagonal prism", "ปริซึมห้าเหลี่ยม", () => prismOf(poly(5, 1.2, 0, Math.PI / 2), 0.9)],
    spyr: ["Square pyramid", "พีระมิดฐานสี่เหลี่ยมจัตุรัส", () => pyramidOf(poly(4, 1.41, -0.8, Math.PI / 4), [0, 1.2, 0])],
    tpyr: ["Triangular pyramid", "พีระมิดฐานสามเหลี่ยม", () => pyramidOf(poly(3, 1.3, -0.7, Math.PI / 2), [0, 1.2, 0])],
    hpyr: ["Hexagonal pyramid", "พีระมิดฐานหกเหลี่ยม", () => pyramidOf(poly(6, 1.3, -0.8), [0, 1.2, 0])],
    cyl: ["Cylinder", "ทรงกระบอก", () => Object.assign(prismOf(poly(28, 1.1, 0), 1.1), { curved: true })],
    cone: ["Cone", "กรวย", () => Object.assign(pyramidOf(poly(28, 1.2, -0.9), [0, 1.3, 0]), { curved: true })],
    sphere: ["Sphere", "ทรงกลม", null],
  };
  const FACTS = {
    cyl: ["2 flat faces (circles) + 1 curved face. No vertices.", "หน้าแบน 2 หน้า (วงกลม) + หน้าโค้ง 1 หน้า ไม่มีจุดยอด"],
    cone: ["1 flat face (circle) + 1 curved face + 1 vertex.", "หน้าแบน 1 หน้า (วงกลม) + หน้าโค้ง 1 หน้า + จุดยอด 1 จุด"],
    sphere: ["No flat face. 1 curved surface. No edges, no vertices.", "ไม่มีหน้าแบน มีผิวโค้ง 1 ผิว ไม่มีขอบ ไม่มีจุดยอด"],
  };
  const SHADE = ["#90CAF9", "#A5D6A7", "#FFCC80", "#F48FB1", "#CE93D8", "#FFF59D", "#80CBC4", "#BCAAA4"];
  function solid(el) {
    const st = { yaw: 0.6, pitch: 0.45, auto: true, key: "cube", dots: false };
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("👆 Drag the solid to turn it. Dotted lines are edges at the back.", "ลากเพื่อหมุนรูปทรง เส้นประคือขอบด้านหลัง")}</p>
      <div class="ex-btns">${Object.entries(SOLIDS).map(([k, s]) => `<button class="chip ${k === st.key ? "on" : ""}" data-k="${k}">${T(s[0], s[1])}</button>`).join("")}</div>
      <div class="ex-btns"><button class="chip" data-d="1">${T("🔴 Show vertices", "แสดงจุดยอด")}</button></div>
      <svg class="ex-svg ex-3d" viewBox="0 0 400 300"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("[data-k]").forEach(b => b.onclick = () => { st.key = b.dataset.k; el.querySelectorAll("[data-k]").forEach(x => x.classList.toggle("on", x === b)); draw(); });
    el.querySelector("[data-d]").onclick = e => { st.dots = !st.dots; e.currentTarget.classList.toggle("on", st.dots); draw(); };
    viewDrag(svg, st, () => draw());
    let S = null, cache = null;
    function draw() {
      const def = SOLIDS[st.key];
      if (!def[2]) { // sphere
        const tilt = Math.sin(st.pitch);
        svg.innerHTML = `<defs><radialGradient id="exg" cx="35%" cy="35%"><stop offset="0" stop-color="#FFFDE7"/><stop offset="1" stop-color="#FDD835"/></radialGradient></defs>
          <circle cx="200" cy="150" r="105" fill="url(#exg)" stroke="#1f2a44" stroke-width="3"/>
          <path d="M95,150 A105,${Math.abs(105 * tilt) + 1} 0 0 ${tilt > 0 ? 0 : 1} 305,150" fill="none" stroke="#1f2a44" stroke-width="2" stroke-dasharray="7 6"/>
          <path d="M95,150 A105,${Math.abs(105 * tilt) + 1} 0 0 ${tilt > 0 ? 1 : 0} 305,150" fill="none" stroke="#1f2a44" stroke-width="2"/>
          <circle cx="200" cy="150" r="5" fill="#1f2a44"/><line x1="200" y1="150" x2="305" y2="150" stroke="#E53935" stroke-width="3"/><text x="252" y="140" class="ex-len" fill="#E53935">${T("radius", "รัศมี").replace(/<[^>]+>/g, " ")}</text>`;
        info.innerHTML = `<div class="ex-row"><b class="ex-name">${T(def[0], def[1])}</b>: ${T(...FACTS.sphere)}</div>`;
        return;
      }
      if (!cache || cache.key !== st.key) { S = def[2](); cache = { key: st.key }; const c = S.v.reduce((a, p) => [a[0] + p[0], a[1] + p[1], a[2] + p[2]], [0, 0, 0]).map(x => x / S.v.length); S.f = S.f.map(f => { const n = cross(sub(S.v[f[1]], S.v[f[0]]), sub(S.v[f[2]], S.v[f[0]])); const fc = f.reduce((a, i) => [a[0] + S.v[i][0], a[1] + S.v[i][1], a[2] + S.v[i][2]], [0, 0, 0]).map(x => x / f.length); return dot(n, sub(fc, c)) < 0 ? f.slice().reverse() : f; }); const E = {}; S.f.forEach((f, fi) => f.forEach((a, i) => { const b = f[(i + 1) % f.length], k = a < b ? a + "_" + b : b + "_" + a; (E[k] = E[k] || []).push(fi); })); S.E = E; }
      const V = S.v.map(p => rot(p, st.yaw, st.pitch));
      const P = V.map(p => [200 + p[0] * 82, 150 - p[1] * 82]);
      const isCurvedSide = fi => S.curved && S.f[fi].length <= 4;
      const front = S.f.map(f => cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]]))[2] > 0);
      const light = norm([-0.4, 0.6, 1]);
      let out = "";
      S.f.map((f, fi) => [f, fi, f.reduce((a, i) => a + V[i][2], 0) / f.length]).filter(x => front[x[1]]).sort((a, b) => a[2] - b[2]).forEach(([f, fi]) => {
        const n = norm(cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]])));
        const base = S.curved ? (isCurvedSide(fi) ? "#FFCC80" : "#FFE0B2") : SHADE[fi % SHADE.length];
        const k = 0.65 + 0.35 * Math.max(0, dot(n, light));
        out += `<polygon points="${f.map(i => P[i]).join(" ")}" fill="${base}" style="filter:brightness(${k.toFixed(2)})" stroke="${S.curved && isCurvedSide(fi) ? "none" : "none"}"/>`;
      });
      const hidden = [], shown = [];
      Object.entries(S.E).forEach(([k, fs]) => {
        const [a, b] = k.split("_").map(Number);
        const curvedBoth = fs.every(isCurvedSide);
        const vis = fs.some(fi => front[fi]);
        if (curvedBoth) { if (fs.length === 2 && front[fs[0]] !== front[fs[1]] && S.f[fs[0]].length === 4) shown.push([a, b]); else if (fs.length === 2 && front[fs[0]] !== front[fs[1]]) shown.push([a, b]); return; }
        (vis ? shown : hidden).push([a, b]);
      });
      const ln = ([a, b], dash) => `<line x1="${P[a][0]}" y1="${P[a][1]}" x2="${P[b][0]}" y2="${P[b][1]}" stroke="#1f2a44" stroke-width="${dash ? 2 : 3}" ${dash ? 'stroke-dasharray="6 5" opacity=".7"' : ""} stroke-linecap="round"/>`;
      out = out + hidden.map(e => ln(e, true)).join("") + shown.map(e => ln(e, false)).join("");
      if (st.dots && !S.curved) out += S.v.map((_, i) => { const vis = S.f.some((f, fi) => front[fi] && f.includes(i)); return `<circle cx="${P[i][0]}" cy="${P[i][1]}" r="7" fill="${vis ? "#E53935" : "#fff"}" stroke="#E53935" stroke-width="2.5"/>`; }).join("");
      if (st.dots && st.key === "cone") out += `<circle cx="${P[S.v.length - 1][0]}" cy="${P[S.v.length - 1][1]}" r="7" fill="#E53935"/>`;
      svg.innerHTML = out;
      if (S.curved) info.innerHTML = `<div class="ex-row"><b class="ex-name">${T(def[0], def[1])}</b>: ${T(...FACTS[st.key])}</div>`;
      else {
        const F = S.f.length, E = Object.keys(S.E).length, Vn = S.v.length;
        info.innerHTML = `<div class="ex-row"><b class="ex-name">${T(def[0], def[1])}</b></div>
          <div class="ex-row ex-count"><span>${T("Faces", "หน้า")}: <b>${F}</b></span><span>${T("Edges", "ขอบ")}: <b>${E}</b></span><span>${T("Vertices", "จุดยอด")}: <b>${Vn}</b></span></div>
          <div class="ex-row small">${T(`Faces + Vertices - Edges = ${F} + ${Vn} - ${E} = ${F + Vn - E}`, `หน้า + จุดยอด - ขอบ = ${F + Vn - E}`)}</div>`;
      }
    }
    draw();
    const tick = () => { if (!el.isConnected) return; if (st.auto) { st.yaw += 0.01; draw(); } requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
  }

  // ================= NETS (fold and unfold) =================
  const sq = (x, y, w = 1, h = 1) => [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
  const NETS = {
    cube1: { n: ["Cube net (cross)", "รูปคลี่ลูกบาศก์ (กากบาท)"], ok: true, faces: [[sq(1, 1), -1, 0], [sq(1, 0), 0, 90], [sq(0, 1), 0, 90], [sq(2, 1), 0, 90], [sq(1, 2), 0, 90], [sq(1, 3), 4, 90]] },
    cube2: { n: ["Cube net (1-4-1)", "รูปคลี่ลูกบาศก์ (1-4-1)"], ok: true, faces: [[sq(1, 1), -1, 0], [sq(0, 1), 0, 90], [sq(2, 1), 0, 90], [sq(1, 0), 0, 90], [sq(3, 1), 2, 90], [sq(2, 2), 2, 90]] },
    cubeX: { n: ["Not a cube net?", "ไม่ใช่รูปคลี่ลูกบาศก์?"], ok: false, faces: [[sq(1, 1), -1, 0], [sq(0, 1), 0, 90], [sq(2, 1), 0, 90], [sq(1, 0), 0, 90], [sq(3, 1), 2, 90], [sq(2, 0), 2, 90]] },
    cuboid: { n: ["Cuboid", "ทรงสี่เหลี่ยมมุมฉาก"], ok: true, faces: [[sq(0, 0, 2, 1), -1, 0], [sq(0, 1, 2, 0.7), 0, 90], [sq(0, 1.7, 2, 1), 1, 90], [sq(0, -0.7, 2, 0.7), 0, 90], [sq(-0.7, 0, 0.7, 1), 0, 90], [sq(2, 0, 0.7, 1), 0, 90]] },
    tprism: { n: ["Triangular prism", "ปริซึมสามเหลี่ยม"], ok: true, faces: [[sq(0, 0, 2, 1), -1, 0], [sq(0, 1, 2, 1), 0, 120], [sq(0, -1, 2, 1), 0, 120], [[[0, 0], [0, 1], [-0.866, 0.5]], 0, 90], [[[2, 0], [2, 1], [2.866, 0.5]], 0, 90]] },
    spyr: { n: ["Square pyramid", "พีระมิดฐานสี่เหลี่ยมจัตุรัส"], ok: true, faces: [[sq(0, 0, 2, 2), -1, 0], [[[0, 0], [2, 0], [1, -2]], 0, 120], [[[2, 0], [2, 2], [4, 1]], 0, 120], [[[2, 2], [0, 2], [1, 4]], 0, 120], [[[0, 2], [0, 0], [-2, 1]], 0, 120]] },
  };
  // Rotation of point p about the axis through a in direction u (unit), by angle t (radians)
  function rotAxis(p, a, u, t) {
    const v = sub(p, a), c = Math.cos(t), s = Math.sin(t), d = dot(u, v), cr = cross(u, v);
    return [a[0] + v[0] * c + cr[0] * s + u[0] * d * (1 - c), a[1] + v[1] * c + cr[1] * s + u[1] * d * (1 - c), a[2] + v[2] * c + cr[2] * s + u[2] * d * (1 - c)];
  }
  function net(el) {
    const st = { yaw: 0.5, pitch: 0.9, auto: false, key: "cube1", t: 0, playing: false };
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Pick a net. Press ▶ Fold, or move the slider. Drag the picture to turn it.", "เลือกรูปคลี่ กด ▶ พับ หรือเลื่อนแถบ ลากรูปเพื่อหมุน")}</p>
      <div class="ex-btns">${Object.entries(NETS).map(([k, s]) => `<button class="chip ${k === st.key ? "on" : ""}" data-k="${k}">${T(s.n[0], s.n[1])}</button>`).join("")}</div>
      <div class="ex-btns"><button class="bigbtn green" id="exPlay">${T("▶ Fold", "พับ")}</button>
        <label class="ex-slider">${T("Flat", "แบน")} <input type="range" min="0" max="100" value="0"> ${T("Folded", "พับแล้ว")}</label></div>
      <svg class="ex-svg ex-3d" viewBox="0 0 400 300"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info"), sl = el.querySelector("input"), play = el.querySelector("#exPlay");
    el.querySelectorAll("[data-k]").forEach(b => b.onclick = () => { st.key = b.dataset.k; st.t = 0; sl.value = 0; el.querySelectorAll("[data-k]").forEach(x => x.classList.toggle("on", x === b)); draw(); });
    sl.oninput = () => { st.t = sl.value / 100; draw(); };
    play.onclick = () => {
      const target = st.t < 0.99 ? 1 : 0, from = st.t, t0 = performance.now();
      const step = now => { const k = Math.min(1, (now - t0) / 1600); st.t = from + (target - from) * (1 - Math.cos(Math.PI * k)) / 2; sl.value = Math.round(st.t * 100); draw(); if (k < 1 && el.isConnected) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    };
    viewDrag(svg, st, () => draw());
    function draw() {
      const N = NETS[st.key], F = N.faces;
      // centre the net
      const all = F.flatMap(f => f[0]); const cx = (Math.min(...all.map(p => p[0])) + Math.max(...all.map(p => p[0]))) / 2, cy = (Math.min(...all.map(p => p[1])) + Math.max(...all.map(p => p[1]))) / 2;
      const base3 = F.map(f => f[0].map(p => [p[0] - cx, 0, p[1] - cy]));
      // fold each face, then apply all its ancestors' folds (parent first rules)
      const chain = i => { const c = []; while (i >= 0) { c.push(i); i = F[i][1]; } return c; };
      const hinge = i => { const p = F[i][1], A = F[i][0], B = F[p][0]; const sh = A.filter(a => B.some(b => Math.abs(a[0] - b[0]) < 1e-6 && Math.abs(a[1] - b[1]) < 1e-6)); return sh.map(q => [q[0] - cx, 0, q[1] - cy]); };
      const face3 = F.map((f, i) => {
        let pts = base3[i];
        for (const j of chain(i)) { // j = this face, then parents
          if (F[j][1] < 0) continue;
          const [h1, h2] = hinge(j), u = norm(sub(h2, h1));
          const c = base3[j].reduce((a, p) => [a[0] + p[0], a[1] + p[1], a[2] + p[2]], [0, 0, 0]).map(x => x / base3[j].length);
          const sign = rotAxis(c, h1, u, 0.1)[1] > 0 ? 1 : -1; // fold upwards
          const t = sign * F[j][2] / R2D * st.t;
          pts = pts.map(p => rotAxis(p, h1, u, t));
          // later parents use their own original hinges: valid because a parent's fold is applied after its children's
        }
        return pts;
      });
      const V = face3.map(f => f.map(p => rot([p[0], p[1] - 0.3, p[2]], st.yaw, st.pitch)));
      const sc = 74;
      const order = V.map((f, i) => [i, f.reduce((a, p) => a + p[2], 0) / f.length]).sort((a, b) => a[1] - b[1]);
      svg.innerHTML = order.map(([i]) => `<polygon points="${V[i].map(p => [200 + p[0] * sc, 160 - p[1] * sc]).join(" ")}" fill="${SHADE[i % SHADE.length]}" fill-opacity=".85" stroke="#1f2a44" stroke-width="2.5" stroke-linejoin="round"/>`).join("");
      const msg = st.t < 0.98 ? T("Keep folding…", "พับต่อไป…") : N.ok ? `<span class="result ok">✅ ${T(`It closes up into a ${N.n[0].replace(/ net.*$/, "").toLowerCase()}!`, "พับแล้วปิดได้พอดี!")}</span>` : `<span class="result no">❌ ${T("Two squares land on the same face and one side is left open. This is NOT a cube net.", "มีสี่เหลี่ยม 2 รูปทับหน้าเดียวกัน และมีด้านหนึ่งเปิดอยู่ จึงไม่ใช่รูปคลี่ของลูกบาศก์")}</span>`;
      info.innerHTML = `<div class="ex-row">${T(`${F.length} faces in this net.`, `รูปคลี่นี้มี ${F.length} หน้า`)}</div><div class="ex-row">${msg}</div>`;
    }
    draw();
  }

  return { triangle, circle, compass, solid, net };
})();
