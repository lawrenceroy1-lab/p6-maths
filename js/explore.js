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
      if (mode === "perim") { const P3 = [s.a, s.b, s.c].map(Number); info.innerHTML += `<div class="ex-row"><b>${T("Perimeter", "ความยาวรอบรูป")}</b> = ${s.c} + ${s.a} + ${s.b} = <b>${f1(P3[0] + P3[1] + P3[2])} cm</b></div>`; }
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
    const tick = () => { if (!el.isConnected) return; if (st.auto) { st.yaw += 0.02; draw(); } setTimeout(tick, 50); };
    setTimeout(tick, 50);
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
      const step = () => { const k = Math.min(1, (performance.now() - t0) / 1600); st.t = from + (target - from) * (1 - Math.cos(Math.PI * k)) / 2; sl.value = Math.round(st.t * 100); draw(); if (k < 1 && el.isConnected) setTimeout(step, 30); };
      step();
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

  // ================= TRIANGLE AREA (base and height) =================
  function tarea(el) {
    const PX = 34, Y0 = 250, X0 = 40; // 34 px = 1 cm, base on y = 250
    let b = 6, h = 4, ax = 3; // apex x (cm from the left end of the base)
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("👆 Drag the top corner left and right. Change the base and height with the sliders.", "ลากมุมบนไปทางซ้ายขวา เปลี่ยนฐานและความสูงด้วยแถบเลื่อน")}</p>
      <div class="ex-btns">
        <label class="ex-slider">${T("Base", "ฐาน")} <input type="range" data-k="b" min="2" max="8" step="1" value="${b}"> <b class="vb"></b></label>
        <label class="ex-slider">${T("Height", "ความสูง")} <input type="range" data-k="h" min="1" max="6" step="1" value="${h}"> <b class="vh"></b></label>
        <button class="chip" data-r="1">${T("Show related rectangle", "แสดงสี่เหลี่ยมผืนผ้าที่เกี่ยวข้อง")}</button></div>
      <svg class="ex-svg" viewBox="0 0 400 280"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    let rect = false;
    el.querySelectorAll("input").forEach(i => i.oninput = () => { if (i.dataset.k === "b") b = +i.value; else h = +i.value; ax = Math.min(ax, b + 2); draw(); });
    el.querySelector("[data-r]").onclick = e => { rect = !rect; e.currentTarget.classList.toggle("on", rect); draw(); };
    function draw() {
      const L = [X0, Y0], R = [X0 + b * PX, Y0], A = [X0 + ax * PX, Y0 - h * PX], F = [A[0], Y0];
      let g = "";
      for (let x = 0; x <= 10; x++) g += `<line x1="${X0 + x * PX}" y1="${Y0 - 7 * PX}" x2="${X0 + x * PX}" y2="${Y0}" stroke="#e3e8f0"/>`;
      for (let y = 0; y <= 7; y++) g += `<line x1="${X0}" y1="${Y0 - y * PX}" x2="${X0 + 10 * PX}" y2="${Y0 - y * PX}" stroke="#e3e8f0"/>`;
      const outside = ax < 0 || ax > b;
      svg.innerHTML = g +
        (rect ? `<rect x="${X0}" y="${Y0 - h * PX}" width="${b * PX}" height="${h * PX}" fill="#BBDEFB" fill-opacity=".5" stroke="#1E88E5" stroke-width="2" stroke-dasharray="6 5"/>` : "") +
        (outside ? `<line x1="${Math.min(L[0], F[0])}" y1="${Y0}" x2="${Math.max(R[0], F[0])}" y2="${Y0}" stroke="#1f2a44" stroke-width="2" stroke-dasharray="5 5"/>` : "") +
        `<polygon points="${L} ${R} ${A}" fill="#FFF59D" stroke="#1f2a44" stroke-width="3" stroke-linejoin="round"/>
        <line x1="${A[0]}" y1="${A[1]}" x2="${F[0]}" y2="${F[1]}" stroke="#E53935" stroke-width="3" stroke-dasharray="7 5"/>
        <polyline points="${F[0]},${Y0 - 12} ${F[0] + (ax > b / 2 ? -12 : 12)},${Y0 - 12} ${F[0] + (ax > b / 2 ? -12 : 12)},${Y0}" fill="none" stroke="#E53935" stroke-width="2"/>
        <text x="${(L[0] + R[0]) / 2}" y="${Y0 + 22}" class="ex-len">${T("base", "ฐาน").replace(/<[^>]+>/g, " ")} ${b} cm</text>
        <text x="${A[0] + 10}" y="${Y0 - h * PX / 2}" class="ex-len" fill="#E53935" style="text-anchor:start">${h} cm</text>
        <circle class="ex-h" cx="${A[0]}" cy="${A[1]}" r="13" fill="#E53935" stroke="#fff" stroke-width="3"/>`;
      draggable(svg, svg.querySelector(".ex-h"), x => { ax = clamp(Math.round((x - X0) / PX * 2) / 2, -1, 10 - 0.5); draw(); });
      el.querySelector(".vb").textContent = `${b} cm`; el.querySelector(".vh").textContent = `${h} cm`;
      const area = b * h / 2;
      info.innerHTML = `<div class="ex-row"><b>${T("Area of the triangle", "พื้นที่รูปสามเหลี่ยม")}</b> = ½ × ${b} × ${h} = ½ × ${b * h} = <b>${f1(area)} cm²</b></div>
        ${rect ? `<div class="ex-row">${T(`Related rectangle = ${b} × ${h} = ${b * h} cm². The triangle is exactly half of it.`, `สี่เหลี่ยมผืนผ้าที่เกี่ยวข้อง = ${b} × ${h} = ${b * h} cm² รูปสามเหลี่ยมเป็นครึ่งหนึ่งพอดี`)}</div>` : ""}
        <div class="ex-row small">${outside ? T("The height is outside the triangle, but it still meets the base line at 90°.", "ความสูงอยู่นอกรูปสามเหลี่ยม แต่ยังตั้งฉากกับแนวฐาน") : T("Move the top corner: the area does not change, because the base and height stay the same!", "เลื่อนมุมบน: พื้นที่ไม่เปลี่ยน เพราะฐานและความสูงเท่าเดิม!")}</div>`;
    }
    draw();
  }

  // ================= POLYGONS: interior angles / perimeter =================
  function polygon(el, mode) {
    let n = 5, s = 4;
    const NAMES = { 3: ["triangle", "สามเหลี่ยม"], 4: ["quadrilateral", "สี่เหลี่ยม"], 5: ["pentagon", "ห้าเหลี่ยม"], 6: ["hexagon", "หกเหลี่ยม"], 7: ["heptagon", "เจ็ดเหลี่ยม"], 8: ["octagon", "แปดเหลี่ยม"], 9: ["nonagon", "เก้าเหลี่ยม"], 10: ["decagon", "สิบเหลี่ยม"] };
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${mode === "perim" ? T("Change the number of sides and the side length.", "เปลี่ยนจำนวนด้านและความยาวด้าน") : T("Change the number of sides. Watch the polygon split into triangles from one corner.", "เปลี่ยนจำนวนด้าน ดูรูปหลายเหลี่ยมแบ่งเป็นรูปสามเหลี่ยมจากมุมเดียว")}</p>
      <div class="ex-btns"><label class="ex-slider">${T("Sides", "จำนวนด้าน")} <input type="range" data-k="n" min="3" max="10" value="${n}"> <b class="vn"></b></label>
      ${mode === "perim" ? `<label class="ex-slider">${T("Each side", "ความยาวแต่ละด้าน")} <input type="range" data-k="s" min="1" max="12" step="0.5" value="${s}"> <b class="vs"></b></label>` : ""}</div>
      <svg class="ex-svg" viewBox="0 0 400 300"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("input").forEach(i => i.oninput = () => { if (i.dataset.k === "n") n = +i.value; else s = +i.value; draw(); });
    function draw() {
      const R = 115, C = [200, 155], off = -Math.PI / 2 - Math.PI / n;
      const P = Array.from({ length: n }, (_, i) => [C[0] + R * Math.cos(off + 2 * Math.PI * i / n), C[1] + R * Math.sin(off + 2 * Math.PI * i / n) + (n % 2 ? 12 : 0)]);
      let o = "";
      if (mode !== "perim") for (let i = 1; i < n - 1; i++) o += `<polygon points="${P[0]} ${P[i]} ${P[i + 1]}" fill="${SHADE[i % SHADE.length]}" fill-opacity=".75" stroke="#1f2a44" stroke-width="1.5"/>`;
      o += `<polygon points="${P.join(" ")}" fill="${mode === "perim" ? "#FFF59D" : "none"}" stroke="#1f2a44" stroke-width="3" stroke-linejoin="round"/>`;
      if (mode === "perim") P.forEach((p, i) => { const q = P[(i + 1) % n], mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2, dx = mx - C[0], dy = my - C[1], L = Math.hypot(dx, dy); o += `<text x="${mx + dx / L * 20}" y="${my + dy / L * 20 + 5}" class="ex-len">${f1(s)}</text>`; });
      else for (let i = 1; i < n - 1; i++) { const cx = (P[0][0] + P[i][0] + P[i + 1][0]) / 3, cy = (P[0][1] + P[i][1] + P[i + 1][1]) / 3; o += `<text x="${cx}" y="${cy + 5}" class="ex-lab">180°</text>`; }
      svg.innerHTML = o;
      el.querySelector(".vn").textContent = n;
      const nm = T(NAMES[n][0], NAMES[n][1]);
      if (mode === "perim") {
        el.querySelector(".vs").textContent = `${f1(s)} cm`;
        info.innerHTML = `<div class="ex-row"><b class="ex-name">${T("Regular", "ปกติ")} ${nm}</b>: ${n} ${T("equal sides", "ด้านยาวเท่ากัน")}</div>
          <div class="ex-row"><b>${T("Perimeter", "ความยาวรอบรูป")}</b> = ${f1(s)} × ${n} = <b>${f1(s * n)} cm</b></div>
          <div class="ex-row small">${T("Equal sides? Multiply instead of adding them one by one.", "ด้านยาวเท่ากัน? ใช้การคูณแทนการบวกทีละด้าน")}</div>`;
      } else {
        const sum = (n - 2) * 180, each = sum / n;
        info.innerHTML = `<div class="ex-row"><b class="ex-name">${nm}</b>: ${n} ${T("sides", "ด้าน")} ➡ ${n - 2} ${T("triangles", "รูปสามเหลี่ยม")}</div>
          <div class="ex-row"><b>${T("Sum of interior angles", "ผลรวมของมุมภายใน")}</b> = ${n - 2} × 180° = <b>${sum.toLocaleString("en-US")}°</b></div>
          <div class="ex-row">${T("Regular polygon: each angle", "รูปหลายเหลี่ยมด้านเท่ามุมเท่า: แต่ละมุม")} = ${sum.toLocaleString("en-US")}° ÷ ${n} = <b>${Number.isInteger(each) ? each : "≈ " + f1(each)}°</b></div>`;
      }
    }
    draw();
  }

  // ================= AREA BY SPLITTING =================
  function split(el) {
    const U = 30, O = [55, 250];
    const SH = {
      "L-shape|รูปตัว L": { outline: [[0, 0], [6, 0], [6, 2], [2, 2], [2, 5], [0, 5]], parts: [["rect", [[0, 0], [6, 0], [6, 2], [0, 2]], "6 × 2", 12], ["rect", [[0, 2], [2, 2], [2, 5], [0, 5]], "2 × 3", 6]] },
      "House|รูปบ้าน": { outline: [[0, 0], [4, 0], [4, 4], [2, 7], [0, 4]], parts: [["rect", [[0, 0], [4, 0], [4, 4], [0, 4]], "4 × 4", 16], ["tri", [[0, 4], [4, 4], [2, 7]], "½ × 4 × 3", 6]] },
      "Trapezium|สี่เหลี่ยมคางหมู": { outline: [[0, 0], [6, 0], [4, 3], [0, 3]], parts: [["rect", [[0, 0], [4, 0], [4, 3], [0, 3]], "4 × 3", 12], ["tri", [[4, 0], [6, 0], [4, 3]], "½ × 2 × 3", 3]] },
      "Take away|ลบออก": { outline: [[0, 0], [8, 0], [8, 5], [0, 5]], cut: [[4, 5], [8, 5], [8, 2]], parts: [["rect", [[0, 0], [8, 0], [8, 5], [0, 5]], "8 × 5", 40], ["tri", [[4, 5], [8, 5], [8, 2]], "½ × 4 × 3", -6]] },
    };
    let key = "L-shape|รูปตัว L", show = false;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Pick a shape, then tap ✂️ Split it. Each square on the grid is 1 cm².", "เลือกรูป แล้วแตะ ✂️ แบ่งรูป แต่ละช่องตารางคือ 1 cm²")}</p>
      <div class="ex-btns">${Object.keys(SH).map(k => `<button class="chip ${k === key ? "on" : ""}" data-k="${k}">${T(...k.split("|"))}</button>`).join("")}<button class="bigbtn green" id="exSplit">${T("✂️ Split it", "แบ่งรูป")}</button></div>
      <svg class="ex-svg" viewBox="0 0 400 275"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("[data-k]").forEach(b => b.onclick = () => { key = b.dataset.k; show = false; el.querySelectorAll("[data-k]").forEach(x => x.classList.toggle("on", x === b)); draw(); });
    el.querySelector("#exSplit").onclick = () => { show = !show; draw(); };
    const pt = p => [O[0] + p[0] * U, O[1] - p[1] * U];
    function draw() {
      const S = SH[key];
      let g = "";
      for (let x = 0; x <= 10; x++) g += `<line x1="${O[0] + x * U}" y1="${O[1] - 7 * U}" x2="${O[0] + x * U}" y2="${O[1]}" stroke="#e3e8f0"/>`;
      for (let y = 0; y <= 7; y++) g += `<line x1="${O[0]}" y1="${O[1] - y * U}" x2="${O[0] + 10 * U}" y2="${O[1] - y * U}" stroke="#e3e8f0"/>`;
      let o = g;
      if (!show) {
        o += `<polygon points="${S.outline.map(pt).join(" ")}" fill="#FFE0B2" stroke="#1f2a44" stroke-width="3"/>`;
        if (S.cut) o += `<polygon points="${S.cut.map(pt).join(" ")}" fill="#fff" stroke="#1f2a44" stroke-width="3"/>`;
      } else S.parts.forEach((p, i) => {
        const pts = p[1].map(pt), cx = pts.reduce((a, q) => a + q[0], 0) / pts.length, cy = pts.reduce((a, q) => a + q[1], 0) / pts.length;
        o += `<polygon points="${pts.join(" ")}" fill="${p[3] < 0 ? "#fff" : SHADE[i]}" stroke="#1f2a44" stroke-width="2.5" ${p[3] < 0 ? 'stroke-dasharray="6 4"' : ""}/>
          <text x="${cx}" y="${cy + 5}" class="ex-lab">${String.fromCharCode(65 + i)}</text>`;
      });
      svg.innerHTML = o;
      const total = S.parts.reduce((a, p) => a + p[3], 0);
      info.innerHTML = show
        ? S.parts.map((p, i) => `<div class="ex-row">${String.fromCharCode(65 + i)}: ${p[2]} = ${Math.abs(p[3])} cm² ${p[3] < 0 ? T("(take away)", "(ลบออก)") : ""}</div>`).join("") +
          `<div class="ex-row"><b>${T("Total area", "พื้นที่ทั้งหมด")}</b> = ${S.parts.map(p => Math.abs(p[3])).join(S.parts.some(p => p[3] < 0) ? " - " : " + ")} = <b>${total} cm²</b></div>`
        : `<div class="ex-row">${T("How would you split this shape into rectangles and triangles?", "จะแบ่งรูปนี้เป็นสี่เหลี่ยมผืนผ้าและสามเหลี่ยมอย่างไร")}</div>`;
    }
    draw();
  }

  // ================= CIRCUMFERENCE (roll the circle) =================
  function circum(el) {
    const PX = 50; let d = 2, t = 0, timer = null;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Press ▶ Roll: the wheel turns once. The line it leaves is the circumference.", "กด ▶ กลิ้ง: ล้อหมุน 1 รอบ เส้นที่ได้คือเส้นรอบวง")}</p>
      <div class="ex-btns"><label class="ex-slider">${T("Diameter", "เส้นผ่านศูนย์กลาง")} <input type="range" min="1" max="3" step="0.5" value="${d}"> <b class="vd"></b></label>
      <button class="bigbtn green" id="exRoll">${T("▶ Roll", "กลิ้ง")}</button></div>
      <svg class="ex-svg" viewBox="0 0 560 240"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelector("input").oninput = e => { d = +e.target.value; t = 0; draw(); };
    el.querySelector("#exRoll").onclick = () => { clearTimeout(timer); t = 0; const t0 = performance.now(); const step = () => { t = Math.min(1, (performance.now() - t0) / 2400); draw(); if (t < 1 && el.isConnected) timer = setTimeout(step, 30); }; step(); };
    function draw() {
      const r = d * PX / 2, X0 = 82, Y = 200, C = Math.PI * d * PX, cx = X0 + C * t, ang = 2 * Math.PI * t;
      const dot = [cx - r * Math.sin(ang), Y - r + r * Math.cos(ang)];
      let o = `<line x1="10" y1="${Y}" x2="550" y2="${Y}" stroke="#90A4AE" stroke-width="2"/>`;
      for (let k = 1; k <= 3; k++) o += `<line x1="${X0 + k * d * PX}" y1="${Y + 6}" x2="${X0 + k * d * PX}" y2="${Y + 18}" stroke="#1E88E5" stroke-width="2"/><text x="${X0 + (k - 0.5) * d * PX}" y="${Y + 32}" class="ex-len">d</text>`;
      o += `<line x1="${X0}" y1="${Y}" x2="${cx}" y2="${Y}" stroke="#E53935" stroke-width="6" stroke-linecap="round"/>
        <circle cx="${cx}" cy="${Y - r}" r="${r}" fill="#E3F2FD" stroke="#1f2a44" stroke-width="3"/>
        <line x1="${cx - r * Math.cos(ang)}" y1="${Y - r - r * Math.sin(ang)}" x2="${cx + r * Math.cos(ang)}" y2="${Y - r + r * Math.sin(ang)}" stroke="#1E88E5" stroke-width="2"/>
        <circle cx="${dot[0]}" cy="${dot[1]}" r="7" fill="#E53935"/>`;
      svg.innerHTML = o;
      el.querySelector(".vd").textContent = `${f1(d)} cm`;
      info.innerHTML = `<div class="ex-row">${T("The red line is a bit more than 3 diameters long: that number is π (about 3.14).", "เส้นสีแดงยาวกว่า 3 เท่าของเส้นผ่านศูนย์กลางเล็กน้อย: ตัวเลขนั้นคือ π (ประมาณ 3.14)")}</div>
        <div class="ex-row"><b>${T("Circumference", "เส้นรอบวง")}</b> = π × d ≈ 3.14 × ${f1(d)} = <b>${(Math.round(314 * d) / 100).toFixed(2).replace(/0$/, "").replace(/\.0$/, "")} cm</b></div>`;
    }
    draw();
  }

  // ================= AREA OF A CIRCLE (slices) =================
  function carea(el) {
    let n = 12, r = 2;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Cut the circle into more slices. The slices make a shape that looks more and more like a rectangle.", "ตัดวงกลมเป็นชิ้นมากขึ้น ชิ้นที่เรียงกันจะดูเหมือนสี่เหลี่ยมผืนผ้ามากขึ้น")}</p>
      <div class="ex-btns"><label class="ex-slider">${T("Slices", "จำนวนชิ้น")} <input type="range" data-k="n" min="4" max="32" step="2" value="${n}"> <b class="vn"></b></label>
      <label class="ex-slider">${T("Radius", "รัศมี")} <input type="range" data-k="r" min="1" max="3" step="0.5" value="${r}"> <b class="vr"></b></label></div>
      <svg class="ex-svg" viewBox="0 0 520 250"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("input").forEach(i => i.oninput = () => { if (i.dataset.k === "n") n = +i.value; else r = +i.value; draw(); });
    function draw() {
      const R = 75, C = [95, 125], a = 2 * Math.PI / n;
      let o = "";
      for (let i = 0; i < n; i++) {
        const a0 = i * a, a1 = (i + 1) * a;
        o += `<path d="M${C[0]},${C[1]} L${C[0] + R * Math.cos(a0)},${C[1] + R * Math.sin(a0)} A${R},${R} 0 0 1 ${C[0] + R * Math.cos(a1)},${C[1] + R * Math.sin(a1)} Z" fill="${i % 2 ? "#FFCC80" : "#90CAF9"}" stroke="#fff" stroke-width="1"/>`;
      }
      // rearranged: slices alternately pointing up and down
      const w = R * a, X0 = 215, Yb = 170;
      for (let i = 0; i < n; i++) {
        const up = i % 2 === 0, x = X0 + i * w / 2;
        const tip = up ? [x + w / 2, Yb - R] : [x + w / 2, Yb];
        const p1 = up ? [x, Yb] : [x, Yb - R], p2 = up ? [x + w, Yb] : [x + w, Yb - R];
        o += `<path d="M${tip} L${p1} Q${(p1[0] + p2[0]) / 2},${up ? Yb + w * 0.25 : Yb - R - w * 0.25} ${p2} Z" fill="${up ? "#90CAF9" : "#FFCC80"}" stroke="#fff" stroke-width="1"/>`;
      }
      const W = (n + 1) * w / 2;
      o += `<line x1="${X0}" y1="${Yb + 22}" x2="${X0 + W}" y2="${Yb + 22}" stroke="#1E88E5" stroke-width="2"/><text x="${X0 + W / 2}" y="${Yb + 40}" class="ex-len">½ × circumference = π × r</text>
        <line x1="${X0 + W + 14}" y1="${Yb - R}" x2="${X0 + W + 14}" y2="${Yb}" stroke="#E53935" stroke-width="2"/><text x="${X0 + W + 22}" y="${Yb - R / 2}" class="ex-len" fill="#E53935" style="text-anchor:start">r</text>`;
      svg.innerHTML = o;
      el.querySelector(".vn").textContent = n; el.querySelector(".vr").textContent = `${f1(r)} cm`;
      const area = Math.round(314 * r * r) / 100;
      info.innerHTML = `<div class="ex-row">${T("Rectangle area = length × height = (π × r) × r", "พื้นที่สี่เหลี่ยมผืนผ้า = ยาว × สูง = (π × r) × r")}</div>
        <div class="ex-row"><b>${T("Area of a circle", "พื้นที่วงกลม")}</b> = π × r × r ≈ 3.14 × ${f1(r)} × ${f1(r)} = <b>${area} cm²</b></div>`;
    }
    draw();
  }

  // ================= VOLUME (unit cubes) =================
  function volume(el) {
    let l = 4, w = 3, h = 2, layers = false;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Build a cuboid from 1 cm cubes. Each cube is 1 cm³.", "สร้างทรงสี่เหลี่ยมมุมฉากจากลูกบาศก์ขนาด 1 cm แต่ละลูกคือ 1 cm³")}</p>
      <div class="ex-btns">${[["l", "Length", "ความยาว"], ["w", "Width", "ความกว้าง"], ["h", "Height", "ความสูง"]].map(([k, e, t]) => `<label class="ex-slider">${T(e, t)} <input type="range" data-k="${k}" min="1" max="5" value="${{ l, w, h }[k]}"> <b class="v${k}"></b></label>`).join("")}
      <button class="chip" data-y="1">${T("Colour the layers", "ระบายสีแต่ละชั้น")}</button></div>
      <svg class="ex-svg" viewBox="0 0 400 300"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("input").forEach(i => i.oninput = () => { ({ l: () => l = +i.value, w: () => w = +i.value, h: () => h = +i.value })[i.dataset.k](); draw(); });
    el.querySelector("[data-y]").onclick = e => { layers = !layers; e.currentTarget.classList.toggle("on", layers); draw(); };
    function draw() {
      const s = 34, dx = s * 0.55, dy = -s * 0.45, ox = 200 - (l * s + w * dx) / 2, oy = 250 - (w * dy) / 2 + 0;
      const LAY = ["#90CAF9", "#A5D6A7", "#FFCC80", "#F48FB1", "#CE93D8"];
      let o = "";
      const cells = [];
      for (let z = 0; z < h; z++) for (let y = 0; y < w; y++) for (let x = 0; x < l; x++) cells.push([x, y, z]);
      cells.sort((a, b) => (b[1] - a[1]) || (a[2] - b[2]) || (a[0] - b[0]));
      for (const [x, y, z] of cells) {
        const X = ox + x * s + y * dx, Y = oy - z * s + y * dy, f = layers ? LAY[z % 5] : "#FFE082";
        o += `<polygon points="${X},${Y} ${X + s},${Y} ${X + s},${Y - s} ${X},${Y - s}" fill="${f}" stroke="#1f2a44" stroke-width="1.2"/>
          <polygon points="${X},${Y - s} ${X + s},${Y - s} ${X + s + dx},${Y - s + dy} ${X + dx},${Y - s + dy}" fill="${f}" style="filter:brightness(1.12)" stroke="#1f2a44" stroke-width="1.2"/>
          <polygon points="${X + s},${Y} ${X + s + dx},${Y + dy} ${X + s + dx},${Y - s + dy} ${X + s},${Y - s}" fill="${f}" style="filter:brightness(.85)" stroke="#1f2a44" stroke-width="1.2"/>`;
      }
      svg.innerHTML = o;
      ["l", "w", "h"].forEach(k => el.querySelector(".v" + k).textContent = `${{ l, w, h }[k]} cm`);
      info.innerHTML = `<div class="ex-row">${T("Base area", "พื้นที่ฐาน")} = ${l} × ${w} = ${l * w} cm² · ${T("layers", "จำนวนชั้น")}: ${h}</div>
        <div class="ex-row"><b>${T("Volume", "ปริมาตร")}</b> = ${l} × ${w} × ${h} = <b>${l * w * h} cm³</b> (${l * w * h} ${T("cubes", "ลูกบาศก์")})</div>`;
    }
    draw();
  }

  // ================= WATER TANK (capacity) =================
  function tank(el) {
    let L = 40, W = 25, H = 30, water = 12;
    el.innerHTML = `<div class="ex">
      <p class="ex-tip">${T("Change the tank and the water height. Pour in 1 litre at a time.", "เปลี่ยนขนาดถังและความสูงของน้ำ เทน้ำเพิ่มครั้งละ 1 ลิตร")}</p>
      <div class="ex-btns">${[["L", "Length", "ความยาว", 10, 50], ["W", "Width", "ความกว้าง", 10, 40], ["H", "Height", "ความสูง", 10, 40]].map(([k, e, t, a, b]) => `<label class="ex-slider">${T(e, t)} <input type="range" data-k="${k}" min="${a}" max="${b}" step="5" value="${{ L, W, H }[k]}"> <b class="v${k}"></b></label>`).join("")}
      <button class="bigbtn" id="exPour">${T("🚰 Pour in 1 ℓ", "เทน้ำ 1 ℓ")}</button><button class="chip" id="exEmpty">${T("Empty", "เทออกหมด")}</button></div>
      <svg class="ex-svg" viewBox="0 0 400 290"></svg><div class="ex-info"></div></div>`;
    const svg = el.querySelector(".ex-svg"), info = el.querySelector(".ex-info");
    el.querySelectorAll("input").forEach(i => i.oninput = () => { ({ L: () => L = +i.value, W: () => W = +i.value, H: () => H = +i.value })[i.dataset.k](); water = Math.min(water, H); draw(); });
    el.querySelector("#exPour").onclick = () => { water = Math.min(H, water + 1000 / (L * W)); draw(); };
    el.querySelector("#exEmpty").onclick = () => { water = 0; draw(); };
    const r2 = x => Math.round(x * 100) / 100;
    function draw() {
      const k = 5, w = L * k, h = H * k, d = W * k * 0.45, ox = 200 - (w + d) / 2, oy = 250;
      const wh = water * k;
      const box = (y0, hh, fill, op) => `<polygon points="${ox},${y0} ${ox + w},${y0} ${ox + w},${y0 - hh} ${ox},${y0 - hh}" fill="${fill}" fill-opacity="${op}"/>
        <polygon points="${ox},${y0 - hh} ${ox + w},${y0 - hh} ${ox + w + d},${y0 - hh - d * 0.6} ${ox + d},${y0 - hh - d * 0.6}" fill="${fill}" fill-opacity="${op * 0.9}"/>
        <polygon points="${ox + w},${y0} ${ox + w + d},${y0 - d * 0.6} ${ox + w + d},${y0 - hh - d * 0.6} ${ox + w},${y0 - hh}" fill="${fill}" fill-opacity="${op * 0.8}"/>`;
      svg.innerHTML = (wh > 0 ? box(oy, wh, "#4FC3F7", 0.75) : "") +
        `<polyline points="${ox},${oy - h} ${ox},${oy} ${ox + w},${oy} ${ox + w + d},${oy - d * 0.6} ${ox + w + d},${oy - h - d * 0.6} ${ox + d},${oy - h - d * 0.6} ${ox},${oy - h} ${ox + w},${oy - h} ${ox + w + d},${oy - h - d * 0.6}" fill="none" stroke="#1f2a44" stroke-width="2.5"/>
        <line x1="${ox + w}" y1="${oy}" x2="${ox + w}" y2="${oy - h}" stroke="#1f2a44" stroke-width="2.5"/>
        <polyline points="${ox},${oy} ${ox + d},${oy - d * 0.6} ${ox + w + d},${oy - d * 0.6}" fill="none" stroke="#1f2a44" stroke-width="1.5" stroke-dasharray="5 4"/>
        <line x1="${ox + d}" y1="${oy - d * 0.6}" x2="${ox + d}" y2="${oy - h - d * 0.6}" stroke="#1f2a44" stroke-width="1.5" stroke-dasharray="5 4"/>
        <text x="${ox + w / 2}" y="${oy + 20}" class="ex-len">${L} cm</text><text x="${ox + w + d / 2 + 16}" y="${oy - d * 0.3 + 10}" class="ex-len">${W} cm</text><text x="${ox - 8}" y="${oy - h / 2}" class="ex-len" style="text-anchor:end">${H} cm</text>`;
      ["L", "W", "H"].forEach(q => el.querySelector(".v" + q).textContent = `${{ L, W, H }[q]} cm`);
      const cap = L * W * H, vol = r2(L * W * water);
      info.innerHTML = `<div class="ex-row">${T("Base area", "พื้นที่ฐาน")} = ${L} × ${W} = ${(L * W).toLocaleString("en-US")} cm² · ${T("water height", "ความสูงของน้ำ")} = ${r2(water)} cm</div>
        <div class="ex-row"><b>${T("Water", "ปริมาตรน้ำ")}</b> = ${(L * W).toLocaleString("en-US")} × ${r2(water)} = <b>${vol.toLocaleString("en-US")} cm³</b> = ${r2(vol / 1000)} ℓ</div>
        <div class="ex-row">${T("Capacity (full)", "ความจุ (เต็มถัง)")} = ${L} × ${W} × ${H} = ${cap.toLocaleString("en-US")} cm³ = ${r2(cap / 1000)} ℓ ${water >= H ? "· " + T("FULL!", "เต็มแล้ว!") : ""}</div>
        <div class="ex-row small">1 ℓ = 1,000 cm³</div>`;
    }
    draw();
  }

  return { triangle, circle, compass, solid, net, tarea, polygon, split, circum, carea, volume, tank };
})();
