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
function getStudent() { return store.get("student", null); }

function renderStudentBar() {
  const bar = document.getElementById("studentBar");
  if (!bar) return;
  const s = getStudent();
  bar.innerHTML = s
    ? `👋 Hi <b>${esc(s.name)}</b> (${esc(s.cls)}) <button class="linkbtn" id="changeName">Not you? Change name</button>`
    : "";
  const btn = document.getElementById("changeName");
  if (btn) btn.onclick = () => askName(true);
}

function askName(force) {
  if (!force && getStudent()) { renderStudentBar(); return; }
  const old = getStudent() || { name: "", cls: "" };
  const wrap = document.createElement("div");
  wrap.className = "modal";
  wrap.innerHTML = `
    <div class="modal-box">
      <h2>Welcome! 👋</h2>
      <p>Type your <b>first name</b> and pick your class.</p>
      <input id="nmInput" maxlength="20" placeholder="First name" value="${esc(old.name)}" autocomplete="off">
      <div class="cls-row">${CLASSES.map(c => `<button class="clsbtn ${c === old.cls ? "on" : ""}" data-c="${c}">${c}</button>`).join("")}</div>
      <p class="small">First name only. No surname.</p>
      <button class="bigbtn green" id="nmGo">Let's go! 🚀</button>
      <p class="err" id="nmErr"></p>
    </div>`;
  document.body.appendChild(wrap);
  let cls = old.cls;
  wrap.querySelectorAll(".clsbtn").forEach(b => b.onclick = () => {
    cls = b.dataset.c;
    wrap.querySelectorAll(".clsbtn").forEach(x => x.classList.toggle("on", x === b));
  });
  const input = wrap.querySelector("#nmInput");
  input.focus();
  wrap.querySelector("#nmGo").onclick = () => {
    const name = input.value.trim().split(/\s+/)[0] || "";
    if (!name) { wrap.querySelector("#nmErr").textContent = "Please type your first name."; return; }
    if (!cls) { wrap.querySelector("#nmErr").textContent = "Please pick your class."; return; }
    store.set("student", { name: name.charAt(0).toUpperCase() + name.slice(1), cls });
    wrap.remove();
    renderStudentBar();
  };
}

// ---------- Scores ----------
// Every result is saved in the browser first, then sent to the Google Sheet.
// If sending fails, it stays in the queue and is tried again next time.
function saveScore(r) {
  const s = getStudent() || { name: "Guest", cls: "-" };
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
