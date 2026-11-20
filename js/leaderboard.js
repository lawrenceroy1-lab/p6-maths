// Leaderboard: reads Unit Test results from T. Roy's Google Sheet (or this device if the sheet is not connected).

const lbParams = new URLSearchParams(location.search);
let lbTab = lbParams.get("u") || "all";      // "all" or a unit id like "07"
let lbClass = "all";
let ROWS = [];
let LIVE = false;

const keyOf = r => `${String(r.name).trim().toLowerCase()}|${r.cls}`;
const unitKey = u => String(u).padStart(2, "0");

async function loadRows() {
  if (SHEET_URL) {
    try {
      const r = await fetch(`${SHEET_URL}?action=leaderboard`, { cache: "no-cache" });
      const data = await r.json();
      LIVE = true;
      return data.rows || [];
    } catch (e) { /* fall back to this device */ }
  }
  LIVE = false;
  return store.get("scoreHistory", []).filter(r => r.activity === "Unit Test");
}

// best test per student per unit: highest score, then fastest time
function bestPerUnit(rows) {
  const best = {};
  for (const r of rows) {
    const k = keyOf(r) + "|" + unitKey(r.unit);
    const b = best[k];
    const sc = Number(r.score), tm = Number(r.time);
    if (!b || sc > b.score || (sc === b.score && tm < b.time)) {
      best[k] = { name: r.name, cls: r.cls, unit: unitKey(r.unit), score: sc, total: Number(r.total), time: tm };
    }
  }
  return Object.values(best);
}

function overall(rows) {
  const people = {};
  for (const b of bestPerUnit(rows)) {
    const k = keyOf(b);
    const p = people[k] || (people[k] = { name: b.name, cls: b.cls, points: 0, units: 0, tests: 0, time: 0 });
    p.points += b.score * 10;
    p.units += 1;
    p.time += b.time;
  }
  for (const r of rows) { const p = people[keyOf(r)]; if (p) p.tests += 1; }
  return Object.values(people).sort((a, b) => b.points - a.points || a.time - b.time || b.tests - a.tests);
}

function forUnit(rows, u) {
  return bestPerUnit(rows).filter(b => b.unit === u).sort((a, b) => b.score - a.score || a.time - b.time);
}

function medal(i) { return ["🥇", "🥈", "🥉"][i] || i + 1; }
function isMe(r) { const s = getStudent(); return s && keyOf(r) === keyOf({ name: s.name, cls: s.cls }); }

function podium(list, label) {
  const top = list.slice(0, 3);
  if (!top.length) return "";
  const order = [top[1], top[0], top[2]];
  const cls = ["p2", "p1", "p3"];
  const med = ["🥈", "🥇", "🥉"];
  return `<div class="podium">${order.map((p, k) => p ? `<div class="${cls[k]}"><div class="medal">${med[k]}</div><div class="nm">${esc(p.name)}</div><div class="sc">${esc(p.cls)}<br>${label(p)}</div></div>` : "<div></div>").join("")}</div>`;
}

function render() {
  const units = UNITS.filter(u => u.ready && u.id !== "review");
  document.getElementById("lbUnits").innerHTML =
    `<button data-u="all" class="${lbTab === "all" ? "on" : ""}">🌟 Overall</button>` +
    units.map(u => `<button data-u="${u.id}" class="${lbTab === u.id ? "on" : ""}">Unit ${Number(u.id)}</button>`).join("");
  document.getElementById("lbClass").innerHTML = ["all", ...CLASSES].map(c =>
    `<button data-c="${c}" class="${lbClass === c ? "on" : ""}">${c === "all" ? "All classes" : c}</button>`).join("");
  document.querySelectorAll("#lbUnits button").forEach(b => b.onclick = () => { lbTab = b.dataset.u; render(); });
  document.querySelectorAll("#lbClass button").forEach(b => b.onclick = () => { lbClass = b.dataset.c; render(); });

  const rows = ROWS.filter(r => lbClass === "all" || r.cls === lbClass);
  const note = LIVE ? "" : `<p class="pill">📱 Showing results from <b>this device only</b>. The whole-class leaderboard switches on when T. Roy connects the Google Sheet.</p>`;
  let html = note;
  if (lbTab === "all") {
    const list = overall(rows);
    html += `<h2>🌟 Overall</h2>` + (list.length ? podium(list, p => `${p.points} pts`) +
      `<table class="lb"><tr><th>#</th><th>Name</th><th>Class</th><th>Points</th><th>Tests</th></tr>
      ${list.map((p, i) => `<tr class="${isMe(p) ? "me" : ""}"><td class="medal">${medal(i)}</td><td>${esc(p.name)}</td><td>${esc(p.cls)}</td><td>${p.points}</td><td>${p.tests}</td></tr>`).join("")}</table>`
      : `<p>No Unit Tests yet. Be the first! 🚀</p>`);
  } else {
    const u = UNITS.find(x => x.id === lbTab);
    const list = forUnit(rows, lbTab);
    html += `<h2>Unit ${Number(lbTab)}: ${esc(u ? u.title : "")}</h2>` + (list.length ? podium(list, p => `${p.score}/${p.total} · ${fmtT(p.time)}`) +
      `<table class="lb"><tr><th>#</th><th>Name</th><th>Class</th><th>Best score</th><th>Time</th></tr>
      ${list.map((p, i) => `<tr class="${isMe(p) ? "me" : ""}"><td class="medal">${medal(i)}</td><td>${esc(p.name)}</td><td>${esc(p.cls)}</td><td>${p.score} / ${p.total}</td><td>${fmtT(p.time)}</td></tr>`).join("")}</table>`
      : `<p>No one has taken this Unit Test yet. <a href="unit.html?u=${lbTab}#m=test">Be the first! 🚀</a></p>`);
  }
  document.getElementById("lbView").innerHTML = html;
}

function fmtT(sec) { const m = Math.floor(sec / 60), s = sec % 60; return `${m}:${String(s).padStart(2, "0")}`; }

askName(false);
loadRows().then(r => { ROWS = r; render(); });
