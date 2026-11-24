// Lesson slides and class games for any unit: lesson.html?u=09
// Slides come from content/lessonXX.json, pictures from content/unitXX.json, Thai from content/thXX.json,
// team-quiz questions from content/bankXX.json. Quick-maths questions are made and worked out by code.

const UID = new URLSearchParams(location.search).get("u") || "09";
const view = () => document.getElementById("view");
const pic = spec => (spec ? `<div class="pic">${Diagram.render(spec)}</div>` : "");
const TH = (en, th) => (th ? `${en}<span class="th">${th}</span>` : en);
const pick = arr => arr[Math.floor(Math.random() * arr.length)];
const rnd = (a, b, step = 1) => a + step * Math.floor(Math.random() * (Math.floor((b - a) / step) + 1));
const fmt = n => (Math.round(n * 100) / 100).toLocaleString("en-US");
let UNIT = null, LES = null, BANKQ = [], THD = {};

function fg(ref) {   // "L1.3" = section 1, Learn card 3; "Q0.2" = section 0, question 2
  if (!UNIT || !ref) return null;
  const m = ref.match(/^([LQ])(\d+)\.(\d+)$/);
  const s = UNIT.sections[+m[2]];
  return s ? (m[1] === "L" ? s.learn : s.questions)[+m[3]].fig : null;
}
function opts(right, wrongs) {
  const o = [right];
  for (const w of shuffle(wrongs)) if (w !== right && !o.includes(w) && o.length < 4) o.push(w);
  return shuffle(o);
}

// ---------- slides ----------
let cur = 0;
function lesson() {
  const S = LES.slides, sl = S[cur];
  view().innerHTML = `
    <div class="jump">${LES.secs.map((t, i) => `<button data-s="${i}" class="${sl.s === i ? "on" : ""}">${TH(t[0], t[1])}</button>`).join("")}</div>
    <div class="slide">
      <span class="sec">${LES.secs[sl.s][0]} · ${LES.secs[sl.s][1]}</span> <span class="badge">📖 p.${sl.p}</span>
      <h2>${sl.e} ${TH(sl.t, sl.tt)}</h2>
      <div class="two"><div class="big">${sl.h}<p class="th">${sl.th}</p></div>${sl.f ? pic(fg(sl.f)) : "<div></div>"}</div>
      ${sl.a ? `<div class="turn">🙋 Your turn: ${TH(sl.a, "ถึงตาเธอ: " + sl.at)}<div class="reveal"><button class="bigbtn" id="reveal">${TH("👀 Show answer", "ดูคำตอบ")}</button></div></div>` : ""}
    </div>
    <div class="slide-nav">
      <button class="bigbtn" id="prev" ${cur === 0 ? "disabled" : ""}>${TH("⬅ Back", "ย้อนกลับ")}</button>
      <span class="count">${cur + 1} / ${S.length}</span>
      <button class="bigbtn dark" id="next" ${cur === S.length - 1 ? "disabled" : ""}>${TH("Next ➡", "ถัดไป")}</button>
    </div>
    ${cur === S.length - 1 ? `<div class="btnrow"><button class="bigbtn green" id="goGames">${TH("🎮 Play the class games", "เล่นเกมในห้อง")}</button></div>` : ""}`;
  view().querySelectorAll(".jump button").forEach(b => b.onclick = () => { cur = S.findIndex(x => x.s === Number(b.dataset.s)); lesson(); });
  document.getElementById("prev").onclick = () => { if (cur > 0) { cur--; lesson(); } };
  document.getElementById("next").onclick = () => { if (cur < S.length - 1) { cur++; lesson(); } };
  const rv = document.getElementById("reveal");
  if (rv) rv.onclick = () => { rv.parentElement.outerHTML = `<div class="ans">✅ ${TH(sl.n, sl.nt)}</div>`; };
  const gg = document.getElementById("goGames");
  if (gg) gg.onclick = () => setMode("games");
}

// ---------- quick maths (worked out by code) ----------
const QUICK = {
  tri() {
    if (Math.random() < 0.5) {
      const b = rnd(2, 14, 2), h = rnd(2, 12), a = b * h / 2;
      return { q: `Base ${b} cm, height ${h} cm. Area of the triangle? · ฐาน ${b} cm ความสูง ${h} cm พื้นที่รูปสามเหลี่ยมเท่าไร`,
        options: opts(`${a} cm²`, [`${b * h} cm²`, `${b + h} cm²`, `${a + h} cm²`, `${2 * (b + h)} cm²`]), right: `${a} cm²`, why: `½ × ${b} × ${h} = ½ × ${b * h} = ${a} cm². Don't forget the ½!` };
    }
    const x = rnd(5, 25), y = rnd(5, 25), z = rnd(5, 25), p = x + y + z;
    return { q: `Sides ${x} cm, ${y} cm and ${z} cm. Perimeter? · ด้าน ${x} cm, ${y} cm และ ${z} cm ความยาวรอบรูปเท่าไร`,
      options: opts(`${p} cm`, [`${p - 10} cm`, `${x * y} cm`, `${p + 10} cm`, `${x + y} cm`]), right: `${p} cm`, why: `${x} + ${y} + ${z} = ${p} cm.` };
  },
  poly() {
    const NM = { 3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon", 10: "decagon", 12: "dodecagon" };
    const n = pick([4, 5, 6, 8, 10, 12]), sum = (n - 2) * 180;
    if (Math.random() < 0.5) return { q: `Sum of the interior angles of a ${NM[n]} (${n} sides)? · ผลรวมของมุมภายในรูป ${n} เหลี่ยม`,
      options: opts(`${sum.toLocaleString("en-US")}°`, [`${(n * 180).toLocaleString("en-US")}°`, `${((n - 1) * 180).toLocaleString("en-US")}°`, `${(sum - 180).toLocaleString("en-US")}°`, "360°"]), right: `${sum.toLocaleString("en-US")}°`,
      why: `${n} sides → ${n - 2} triangles: ${n - 2} × 180° = ${sum.toLocaleString("en-US")}°.` };
    const e = sum / n;
    return { q: `Each angle of a regular ${NM[n]} (${n} sides)? · แต่ละมุมของรูป ${n} เหลี่ยมด้านเท่ามุมเท่า`,
      options: opts(`${e}°`, [`${180 - e}°`, `${sum}°`, `${e + 10}°`, `${e - 15}°`]), right: `${e}°`, why: `(${n} - 2) × 180° = ${sum.toLocaleString("en-US")}°, and ${sum.toLocaleString("en-US")}° ÷ ${n} = ${e}°.` };
  },
  circle() {
    const r = pick([7, 14, 21, 28]), k = Math.random();
    if (k < 0.34) { const c = 2 * 22 * r / 7; return { q: `Radius ${r} cm. Circumference? (π ≈ 22/7) · รัศมี ${r} cm เส้นรอบวงเท่าไร`,
      options: opts(`${c} cm`, [`${c / 2} cm`, `${22 * r * r / 7} cm`, `${c * 2} cm`, `${c + 7} cm`]), right: `${c} cm`, why: `2 × 22/7 × ${r} = ${c} cm.` }; }
    if (k < 0.67) { const a = 22 * r * r / 7; return { q: `Radius ${r} cm. Area? (π ≈ 22/7) · รัศมี ${r} cm พื้นที่เท่าไร`,
      options: opts(`${a.toLocaleString("en-US")} cm²`, [`${(2 * 22 * r / 7)} cm²`, `${(22 * 4 * r * r / 7).toLocaleString("en-US")} cm²`, `${(a / 2).toLocaleString("en-US")} cm²`, `${(a + 22).toLocaleString("en-US")} cm²`]),
      right: `${a.toLocaleString("en-US")} cm²`, why: `22/7 × ${r} × ${r} = ${a.toLocaleString("en-US")} cm². Use the radius, not the diameter.` }; }
    const d = rnd(2, 20), c = Math.round(314 * d) / 100;
    return { q: `Diameter ${d} cm. Circumference? (π ≈ 3.14) · เส้นผ่านศูนย์กลาง ${d} cm เส้นรอบวงเท่าไร`,
      options: opts(`${fmt(c)} cm`, [`${fmt(c * 2)} cm`, `${fmt(c / 2)} cm`, `${fmt(3.14 * d * d / 4)} cm`, `${fmt(c + 3.14)} cm`]), right: `${fmt(c)} cm`, why: `3.14 × ${d} = ${fmt(c)} cm.` };
  },
  volume() {
    if (Math.random() < 0.6) {
      const l = rnd(2, 12), w = rnd(2, 9), h = rnd(2, 9), v = l * w * h;
      return { q: `A cuboid is ${l} cm × ${w} cm × ${h} cm. Volume? · ทรงสี่เหลี่ยมมุมฉาก ${l} × ${w} × ${h} cm ปริมาตรเท่าไร`,
        options: opts(`${v} cm³`, [`${l + w + h} cm³`, `${l * w} cm³`, `${v * 2} cm³`, `${2 * (l * w + w * h + l * h)} cm³`]), right: `${v} cm³`, why: `${l} × ${w} × ${h} = ${v} cm³.` };
    }
    const L = pick([2, 3, 4, 5, 6, 7, 8, 9, 12, 15]), c = L * 1000;
    return { q: `${L} ℓ = ? cm³ · ${L} ℓ = ? cm³`, options: opts(`${c.toLocaleString("en-US")} cm³`, [`${(L * 100).toLocaleString("en-US")} cm³`, `${(L * 10).toLocaleString("en-US")} cm³`, `${(L * 1000000).toLocaleString("en-US")} cm³`]),
      right: `${c.toLocaleString("en-US")} cm³`, why: `1 ℓ = 1,000 cm³, so ${L} × 1,000 = ${c.toLocaleString("en-US")} cm³.` };
  },
  pattern() {
    const a = rnd(1, 20), d = rnd(2, 9), n = pick([10, 12, 15, 20, 25, 30, 50]), t = a + (n - 1) * d;
    return { q: `${a}, ${a + d}, ${a + 2 * d}, ${a + 3 * d}, … What is term ${n}? · พจน์ที่ ${n} คืออะไร`,
      options: opts(String(t), [String(a + n * d), String(t + d), String(n * d), String(t - 1)]), right: String(t),
      why: `The jump is ${d}. Term ${n} has ${n - 1} jumps: ${a} + (${n - 1} × ${d}) = ${t}.` };
  },
  chart() {
    const k = Math.random();
    if (k < 0.25) { const x = pick([15, 20, 25, 30, 45, 60, 75, 120]), t = x * 4;
      return { q: `A quarter of a pie chart is ${x}. What is the total? · หนึ่งในสี่ของแผนภูมิรูปวงกลมคือ ${x} ทั้งหมดเท่าไร`,
        options: opts(String(t), [String(x * 2), String(x + 4), String(x * 3), String(t + x)]), right: String(t), why: `4 quarters make the whole circle: ${x} × 4 = ${t}.` }; }
    if (k < 0.5) { const a = pick([10, 15, 20, 25, 30, 35, 40]), b = pick([10, 15, 20, 25, 30]), c = 100 - a - b;
      return { q: `Two slices are ${a}% and ${b}%. What percent is the last slice? · สองชิ้นคือ ${a}% และ ${b}% ชิ้นสุดท้ายคิดเป็นร้อยละเท่าไร`,
        options: opts(`${c}%`, [`${a + b}%`, `${c + 10}%`, `${100 - a}%`, `${Math.abs(a - b)}%`, `${c - 5}%`, `${c + 5}%`]), right: `${c}%`, why: `The whole circle is 100%: 100% - ${a}% - ${b}% = ${c}%.` }; }
    if (k < 0.75) { const p = pick([10, 20, 25, 40, 50, 75]), t = pick([40, 80, 120, 200, 240, 320, 400]), v = p * t / 100;
      return { q: `${p}% of ${t} children like football. How many children? · เด็ก ${t} คน ${p}% ชอบฟุตบอล มีกี่คน`,
        options: opts(String(v), [String(p), String(t - v), String(v * 2), String(v + 10), String(v + 5), String(v + 1)].filter(x => +x > 0)), right: String(v), why: `${p}/100 × ${t} = ${v}.` }; }
    const F = pick([["1/4", 25], ["1/2", 50], ["3/4", 75], ["1/5", 20], ["2/5", 40], ["3/5", 60], ["1/8", 12.5], ["3/8", 37.5], ["1/10", 10], ["7/10", 70]]);
    return { q: `A slice is ${F[0]} of the pie chart. What percentage is that? · ชิ้นหนึ่งเป็น ${F[0]} ของแผนภูมิ คิดเป็นร้อยละเท่าไร`,
      options: opts(`${F[1]}%`, [`${F[0].split("/")[1]}%`, `${F[1] / 2}%`, `${100 - F[1]}%`, `${F[1] + 5}%`, `${F[1] * 2}%`]), right: `${F[1]}%`, why: `${F[0]} × 100% = ${F[1]}%.` };
  },
};

const GAMES = {
  bank: { e: "🧠", name: "Team quiz", th: "ทายคำถามเป็นทีม", desc: "Questions from the whole unit, with pictures.", make() {
    const b = pick(BANKQ);
    return { q: b.q + (THD[b.q] ? " · " + THD[b.q].replace(/<[^>]+>/g, "") : ""), fig: b.fig, options: shuffle(b.options.slice()), right: b.options[0], why: b.why };
  } },
  quick: { e: "⚡", name: "Quick maths", th: "คิดเลขเร็ว", desc: "New numbers every time!", make() { return QUICK[LES.quick](); } },
  tf: { e: "👍", name: "True or false?", th: "จริงหรือเท็จ", desc: "Thumbs up or thumbs down!", make() {
    const [s, t, why] = pick(LES.tf);
    return { q: s, options: ["👍 True", "👎 False"], right: t ? "👍 True" : "👎 False", why };
  } },
};
const OPT_TH = o => (o === "👍 True" ? "จริง" : o === "👎 False" ? "เท็จ" : (THD[o] || ""));

let G = null;
let gPick = "bank", nTeams = 2;
function gamesMenu() {
  view().innerHTML = `
    <div class="panel"><h2>🎮 Pick a game · เลือกเกม</h2>
      <div class="games">${Object.entries(GAMES).map(([id, g]) => `<button class="gcard ${id === gPick ? "on" : ""}" data-g="${id}"><div class="gt">${g.e} ${g.name} · ${g.th}</div>${g.desc}</button>`).join("")}</div>
      <h2 style="margin-top:16px">👥 How many teams? · กี่ทีม</h2>
      <div class="btnrow">${[2, 3, 4].map(n => `<button class="bigbtn ${n === nTeams ? "dark" : ""}" data-n="${n}">${n} teams</button>`).join("")}</div>
      <div class="team-setup">${Array.from({ length: nTeams }, (_, i) => `<input id="tn${i}" value="Team ${i + 1}" aria-label="Team ${i + 1} name">`).join("")}</div>
      <p class="small">Each team gets 3 questions, one at a time. Tap the team's answer. Right = 1 point.</p>
      <div class="btnrow"><button class="bigbtn dark" id="startG">▶ Start</button></div>
    </div>`;
  view().querySelectorAll(".gcard").forEach(b => b.onclick = () => { gPick = b.dataset.g; gamesMenu(); });
  view().querySelectorAll("[data-n]").forEach(b => b.onclick = () => { nTeams = Number(b.dataset.n); gamesMenu(); });
  document.getElementById("startG").onclick = () => {
    const teams = Array.from({ length: nTeams }, (_, i) => ({ name: (document.getElementById("tn" + i).value || `Team ${i + 1}`).slice(0, 20), pts: 0 }));
    G = { game: gPick, teams, turn: 0, n: 0, total: nTeams * 3, last: "" };
    nextQ();
  };
}
function board() {
  const top = Math.max(...G.teams.map(t => t.pts));
  return `<div class="scoreboard">${G.teams.map((t, i) => `<div class="team t${i} ${top > 0 && t.pts === top ? "lead" : ""}">${esc(t.name)}<div class="pts">${t.pts}</div></div>`).join("")}</div>`;
}
function nextQ() {
  if (G.n >= G.total) return winner();
  let q, tries = 0;
  do { q = GAMES[G.game].make(); tries++; } while (q.q + q.right === G.last && tries < 10);
  G.last = q.q + q.right; G.q = q; G.done = false;
  drawQ();
}
function drawQ() {
  const q = G.q, team = G.teams[G.turn], shapes = ["▲", "◆", "●", "■"];
  view().innerHTML = `${board()}
    <div class="turnbar team t${G.turn}">🎯 ${esc(team.name)}'s turn · Question ${G.n + 1} of ${G.total}</div>
    <div class="battle-q">${esc(q.q)}${q.fig ? pic(q.fig) : ""}</div>
    <div class="opts" style="margin-top:12px">${q.options.map((o, i) => `<button class="opt c${i}" data-i="${i}"><span class="shape">${shapes[i]}</span> <span>${esc(o)}${OPT_TH(o) ? `<span class="th">${esc(OPT_TH(o).replace(/<[^>]+>/g, ""))}</span>` : ""}</span></button>`).join("")}</div>
    <div id="res"></div>
    <div class="btnrow"><button class="linkbtn" id="quitG">⬅ Back to the game list</button></div>`;
  view().querySelectorAll(".opt").forEach(b => b.onclick = () => answer(q.options[+b.dataset.i]));
  document.getElementById("quitG").onclick = gamesMenu;
}
function answer(o) {
  if (G.done) return;
  G.done = true;
  const ok = o === G.q.right;
  if (ok) G.teams[G.turn].pts++;
  view().querySelectorAll(".opt").forEach(b => { b.disabled = true; b.classList.add(G.q.options[+b.dataset.i] === G.q.right ? "right" : "dim"); });
  view().querySelector(".scoreboard").outerHTML = board();
  document.getElementById("res").innerHTML = `<div class="result ${ok ? "ok" : "no"}">${ok ? "✅ Right! +1 point · ถูกต้อง! ได้ 1 คะแนน" : `❌ Not this time. The answer is ${esc(G.q.right)}.`}<div class="small">${esc(G.q.why)}</div></div>
    <div class="btnrow"><button class="bigbtn dark" id="nextG">${G.n + 1 >= G.total ? "🏆 See the winner · ดูผู้ชนะ" : "Next team ➡ · ทีมต่อไป"}</button></div>`;
  document.getElementById("nextG").onclick = () => { G.n++; G.turn = (G.turn + 1) % G.teams.length; nextQ(); };
}
function winner() {
  const top = Math.max(...G.teams.map(t => t.pts));
  const w = G.teams.filter(t => t.pts === top).map(t => esc(t.name));
  view().innerHTML = `${board()}<div class="panel"><div class="winner">🏆 ${w.length > 1 ? "It's a tie! " + w.join(" and ") : w[0] + " wins!"} 🎉</div>
    <div class="btnrow"><button class="bigbtn dark" id="again">🔁 Play again</button><button class="bigbtn" id="menuG">🎮 Another game</button></div></div>`;
  document.getElementById("again").onclick = () => { G.teams.forEach(t => t.pts = 0); G.n = 0; G.turn = 0; nextQ(); };
  document.getElementById("menuG").onclick = gamesMenu;
}

// ---------- page ----------
let mode = "lesson";
function setMode(m) {
  mode = m;
  document.querySelectorAll("#modeTabs button").forEach(b => b.classList.toggle("on", b.dataset.m === m));
  if (m === "lesson") lesson(); else gamesMenu();
  window.scrollTo(0, 0);
}
document.querySelectorAll("#modeTabs button").forEach(b => b.onclick = () => setMode(b.dataset.m));
document.addEventListener("keydown", e => {
  if (mode !== "lesson" || e.target.tagName === "INPUT") return;
  if (e.key === "ArrowRight" && cur < LES.slides.length - 1) { cur++; lesson(); }
  if (e.key === "ArrowLeft" && cur > 0) { cur--; lesson(); }
});
renderStudentBar();
const get = f => fetch(`content/${f}`, { cache: "no-cache" }).then(r => (r.ok ? r.json() : null)).catch(() => null);
Promise.all([get(`lesson${UID}.json`), get(`unit${UID}.json`), get(`bank${UID}.json`), get(`th${UID}.json`)]).then(([les, unit, bank, th]) => {
  if (!les || !unit) { view().innerHTML = `<div class="panel"><p>This lesson is coming soon 🙂</p></div>`; return; }
  LES = les; UNIT = unit; BANKQ = bank ? bank.questions : []; THD = th || {};
  document.title = `Unit ${Number(UID)} Lesson and Games | P.6 Maths with T. Roy`;
  document.getElementById("lTitle").innerHTML = `${les.icon} Unit ${Number(UID)}: ${esc(unit.title)}, Lesson and Games<span class="th">บทที่ ${Number(UID)}: ${les.th_title} บทเรียนและเกม</span>`;
  setMode(location.hash === "#games" ? "games" : "lesson");
});
