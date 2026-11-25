// Shared helpers: student name, safe storage, score sending.

const store = {
  get(key, fallback) {
    try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); }
    catch (e) { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* storage blocked */ }
  }
};

function esc(s) {
  return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ---------- Student name ----------
// Students pick their nickname from their class list (kept in T. Roy's Google Sheet, "Students" tab).
// Typing "teacher" or "Lawrence" opens the teacher login, which needs the PIN (checked by Google).
const TEACHER_WORDS = ["teacher", "lawrence", "t. roy", "t.roy", "troy"];

function getStudent() {
  const s = store.get("student", null);
  return s && s.v === 2 ? s : null;      // names typed before the class lists existed must be picked again
}
function isTeacher() { const s = getStudent(); return !!(s && s.teacher); }
function teacherPin() { try { return sessionStorage.getItem("tpin") || ""; } catch (e) { return ""; } }
function teacherWho() { try { return sessionStorage.getItem("twho") || ""; } catch (e) { return ""; } }
// Staff (Jaa, Aor, Kong, Lookpat, Yo) use the Teacher login button: their name + the staff password.
// The password is checked by Google (Code.gs v7), never stored in this file.

async function loadClassLists() {
  const cached = store.get("classLists", null);
  if (!SHEET_URL) return cached;
  try {
    const r = await fetch(`${SHEET_URL}?action=students`, { cache: "no-cache" });
    const d = await r.json();
    if (d && d.students) { store.set("classLists", d.students); return d.students; }
  } catch (e) { /* offline: use the saved copy */ }
  return cached;
}

async function teacherLogin(pin, who) {
  if (who === undefined) who = teacherWho();
  try {
    const r = await fetch(SHEET_URL, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify({ action: "teacher", pin, who }) });
    return await r.json();
  } catch (e) { return { ok: false, error: "No internet. Try again." }; }
}

function renderStudentBar() {
  const bar = document.getElementById("studentBar");
  if (!bar) return;
  const s = getStudent();
  if (s && s.teacher) {
    bar.innerHTML = `👩‍🏫 <b>${esc(s.name || "T. Roy")}</b> (Teacher) <a class="linkbtn" href="teacher.html">Teacher page</a> <button class="linkbtn" id="changeName">Log out</button>`;
  } else {
    bar.innerHTML = s ? `👋 Hi <b>${esc(s.name)}</b> (${esc(s.cls)}) <button class="linkbtn" id="changeName">Not you? Change name</button>` : "";
  }
  const btn = document.getElementById("changeName");
  if (btn) btn.onclick = () => {
    if (s && s.teacher) { try { sessionStorage.removeItem("tpin"); sessionStorage.removeItem("twho"); } catch (e) { } store.set("student", null); location.href = "index.html"; return; }
    askName(true);
  };
}

// How alike two names are (0 = same). Used for "Did you mean…?"
function nameDistance(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++)
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length];
}
const normName = s => String(s).toLowerCase().replace(/\(no\.\s*\d+\)/, "").replace(/[^a-z0-9]/g, "");
// the "sound" of a name: no vowels, no double letters (Artym, Artem, Atom → rtm, rtm, tm)
const skelName = s => normName(s).replace(/[aeiouy]/g, "").replace(/(.)\1+/g, "$1");
const collName = s => normName(s).replace(/(.)\1+/g, "$1");      // I/IOON, Ioon → ion
// How a Thai nickname sounds when written in English letters. Children often mix up these spellings:
// ph/p/f, th/t, kh/k/g, ch/j/sh, r/l, v/w, ee/i, oo/u, ai/ay, ae/e, and silent h.
function soundName(s) {
  let x = normName(s);
  [[/ph/g, "p"], [/f/g, "p"], [/th/g, "t"], [/kh/g, "k"], [/g/g, "k"], [/q/g, "k"], [/c(?!h)/g, "k"],
   [/sh/g, "c"], [/ch/g, "c"], [/j/g, "c"], [/r/g, "l"], [/v/g, "w"], [/z/g, "s"], [/x/g, "s"],
   [/ee|ea|ie|ey|y/g, "i"], [/oo|ou|uu/g, "u"], [/ay|ai|ei/g, "ai"], [/ae/g, "e"], [/aw|ao/g, "ao"],
   [/h/g, ""], [/(.)\1+/g, "$1"]].forEach(([a, b]) => { x = x.replace(a, b); });
  return x;
}

// A class list item is "Atom" or {name: "Atom", aka: ["Artem", "Artom"]}
const itemName = it => typeof it === "string" ? it : it.name;
const itemSpellings = it => [itemName(it)].concat(typeof it === "string" ? [] : (it.aka || []));

function matchScore(typed, spelling) {
  const t = normName(typed), n = normName(spelling);
  if (!t || !n) return 99;
  if (t === n) return 0;
  if (collName(typed) === collName(spelling)) return 0.1;
  if (soundName(typed) === soundName(spelling)) return 0.2;
  if (n.startsWith(t) || t.startsWith(n)) return 0.4 + Math.abs(n.length - t.length) * 0.05;
  const lev = nameDistance(t, n) / Math.max(t.length, n.length);
  const st = skelName(typed), ss = skelName(spelling);
  const sk = st.length >= 2 && ss.length >= 2 ? nameDistance(st, ss) / Math.max(st.length, ss.length) + 0.1 : 9;
  const a = soundName(typed), b = soundName(spelling);
  const snd = nameDistance(a, b) / Math.max(a.length, b.length, 1) + 0.05;
  return 1 + Math.min(lev, sk, snd);
}

// Best guesses for what a student typed: always the closest few names in the class.
function suggestNames(typed, list) {
  if (!normName(typed)) return [];
  return list.map(it => ({ n: itemName(it), s: Math.min(...itemSpellings(it).map(sp => matchScore(typed, sp))) }))
    .sort((a, b) => a.s - b.s).slice(0, 4).map(x => x.n);
}
// Names that match what was typed exactly (ignoring case, spaces, slashes, dashes and double letters).
function exactNames(typed, list) {
  const t = collName(typed);
  return list.filter(it => itemSpellings(it).some(sp => collName(sp) === t)).map(itemName);
}

function askName(force) {
  if (!force && getStudent()) { renderStudentBar(); return; }
  if (document.getElementById("nameModal")) return;
  const wrap = document.createElement("div");
  wrap.className = "modal";
  wrap.id = "nameModal";
  document.body.appendChild(wrap);
  let lists = store.get("classLists", null);
  let cls = "", screen = "";
  loadClassLists().then(l => { if (l) { lists = l; if (screen === "pick") drawPick(); } });

  function drawClass() {
    screen = "class";
    wrap.innerHTML = `<div class="modal-box">
      <h2>Welcome! 👋</h2><p><b>Step 1:</b> Pick your class.</p>
      <div class="cls-row">${CLASSES.map(c => `<button class="clsbtn big" data-c="${c}">${c}</button>`).join("")}</div>
      <p class="small" style="margin-top:14px">Are you the teacher? <button class="linkbtn dark" id="tBtn">Teacher login</button></p></div>`;
    wrap.querySelectorAll(".clsbtn").forEach(b => b.onclick = () => { cls = b.dataset.c; drawPick(); });
    wrap.querySelector("#tBtn").onclick = () => drawTeacher();
  }

  function drawPick() {
    const list = (lists && lists[cls]) || [];
    screen = "pick";
    wrap.innerHTML = `<div class="modal-box">
      <h2>Class ${esc(cls)} 👋</h2><p><b>Step 2:</b> Type your <b>nickname</b>.</p>
      <input id="nmInput" maxlength="20" placeholder="Nickname" autocomplete="off">
      <div id="nmSug" class="sug"></div>
      ${list.length ? `<button class="linkbtn dark" id="nmAll">I can't find my name: show the whole class</button>` : `<p class="small">Class list not loaded (no internet?). Type your nickname and press Go.</p>`}
      <div id="nmAllBox"></div>
      ${list.length ? "" : `<button class="bigbtn green" id="nmGo">Let's go! 🚀</button>`}
      <p class="err" id="nmErr"></p>
      <button class="linkbtn" id="nmBack">⬅ Change class</button></div>`;
    const input = wrap.querySelector("#nmInput");
    const sug = wrap.querySelector("#nmSug");
    input.focus();
    const pickBtns = names => names.map(n => `<button class="namebtn" data-n="${esc(n)}">${esc(n)}</button>`).join("");
    const wire = box => box.querySelectorAll(".namebtn").forEach(b => b.onclick = () => drawConfirm(b.dataset.n));
    input.oninput = () => {
      const v = input.value.trim();
      if (TEACHER_WORDS.includes(v.toLowerCase())) { drawTeacher(); return; }
      if (!list.length || !v) { sug.innerHTML = ""; return; }
      const exact = exactNames(v, list);
      const s = exact.length ? exact : suggestNames(v, list);
      sug.innerHTML = `<p class="small">${exact.length ? "Is this you? Tap your name:" : "Did you mean… Tap your name:"}</p>${pickBtns(s)}`;
      wire(sug);
    };
    const all = wrap.querySelector("#nmAll");
    if (all) all.onclick = () => { const box = wrap.querySelector("#nmAllBox"); box.innerHTML = `<div class="sug">${pickBtns(list.map(itemName))}</div>`; wire(box); };
    const go = wrap.querySelector("#nmGo");
    if (go) go.onclick = () => {
      const v = input.value.trim().split(/\s+/)[0] || "";
      if (!v) { wrap.querySelector("#nmErr").textContent = "Please type your nickname."; return; }
      drawConfirm(v.charAt(0).toUpperCase() + v.slice(1));
    };
    wrap.querySelector("#nmBack").onclick = drawClass;
  }

  function drawConfirm(name) {
    screen = "confirm";
    wrap.innerHTML = `<div class="modal-box">
      <h2>Is this you? 🤔</h2>
      <p style="font-size:1.4em;font-weight:900;color:var(--title)">${esc(name)}<br><span class="small">Class ${esc(cls)}</span></p>
      <div class="btnrow"><button class="bigbtn green" id="cYes">✅ Yes, that's me</button><button class="bigbtn grey" id="cNo">❌ No</button></div></div>`;
    wrap.querySelector("#cYes").onclick = () => { store.set("student", { name, cls, v: 2 }); wrap.remove(); renderStudentBar(); };
    wrap.querySelector("#cNo").onclick = drawPick;
  }

  function drawTeacher() {
    screen = "teacher";
    wrap.innerHTML = `<div class="modal-box">
      <h2>👩‍🏫 Teacher login</h2><p>Type your name and password.</p>
      <input id="tWho" maxlength="20" placeholder="Your name (Kong, Lookpat, Yo…)" autocomplete="off" autocapitalize="words">
      <input id="tPin" type="password" maxlength="20" placeholder="Password" autocomplete="off">
      <div class="btnrow"><button class="bigbtn dark" id="tGo">Log in</button></div>
      <p class="err" id="tErr"></p>
      <button class="linkbtn" id="tBack">⬅ I'm a student</button></div>`;
    const pin = wrap.querySelector("#tPin");
    const who = wrap.querySelector("#tWho");
    who.focus();
    who.onkeydown = e => { if (e.key === "Enter") pin.focus(); };
    const go = async () => {
      const err = wrap.querySelector("#tErr");
      if (!SHEET_URL) { err.textContent = "The Google Sheet is not connected."; return; }
      err.textContent = "Checking…";
      const w = who.value.trim();
      const r = await teacherLogin(pin.value.trim(), w);
      if (!r.ok) { err.textContent = r.error || "Wrong password."; return; }
      try { sessionStorage.setItem("tpin", pin.value.trim()); sessionStorage.setItem("twho", w); } catch (e) { }
      store.set("student", { name: r.name || "T. Roy", cls: "Teacher", teacher: true, v: 2 });
      wrap.remove(); renderStudentBar();
      if (typeof onTeacherLogin === "function") onTeacherLogin(r);
    };
    wrap.querySelector("#tGo").onclick = go;
    pin.onkeydown = e => { if (e.key === "Enter") go(); };
    wrap.querySelector("#tBack").onclick = cls ? drawPick : drawClass;
  }

  drawClass();
}

// ---------- Scores ----------
// Every result is saved in the browser first, then sent to the Google Sheet.
// If sending fails, it stays in the queue and is tried again next time.
function saveScore(r) {
  const s = getStudent() || { name: "Guest", cls: "-" };
  if (s.teacher) return;               // the teacher's own practice does not go on the leaderboard
  const row = {
    datetime: new Date().toLocaleString("en-GB"),
    name: s.name, cls: s.cls,
    unit: r.unit, section: r.section, activity: r.activity,
    score: r.score, total: r.total, time: r.time
  };
  const history = store.get("scoreHistory", []);
  history.push(row);
  store.set("scoreHistory", history.slice(-200));
  const queue = store.get("scoreQueue", []);
  queue.push(row);
  store.set("scoreQueue", queue);
  flushScores();
}

let flushing = false;
async function flushScores() {
  if (!SHEET_URL || flushing) return;
  const queue = store.get("scoreQueue", []);
  if (!queue.length) return;
  flushing = true;
  const left = [];
  for (const row of queue) {
    try {
      await fetch(SHEET_URL, {
        method: "POST", mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify(row)
      });
    } catch (e) { left.push(row); }
  }
  store.set("scoreQueue", left);
  flushing = false;
}

window.addEventListener("online", flushScores);
document.addEventListener("DOMContentLoaded", () => { flushScores(); });
