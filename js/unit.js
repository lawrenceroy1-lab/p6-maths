// Unit page: loads content/unitXX.json and runs the 6 activities for each section.

const params = new URLSearchParams(location.search);
const UNIT_ID = params.get("u") || "07";
let DATA = null;
let secIdx = 0;
let act = "learn";
let cleanup = null;          // stops timers when leaving an activity

const ACTS = [
  { id: "learn",   e: "📘", name: "Learn" },
  { id: "guided",  e: "🧭", name: "Guided Answers" },
  { id: "flash",   e: "🃏", name: "Flashcards" },
  { id: "match",   e: "🧩", name: "Match Game" },
  { id: "quiz",    e: "⚡", name: "Speed Quiz" },
  { id: "battle",  e: "🏆", name: "Class Battle" }
];

const fig = (spec, cls) => spec ? Diagram.render(spec).replace('class="diagram"', `class="diagram ${cls || ""}"`) : "";
const view = () => document.getElementById("view");

// ---------- Load ----------
fetch(`content/unit${UNIT_ID}.json`, { cache: "no-cache" })
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(d => {
    DATA = d;
    document.title = `Unit ${Number(d.unit)}: ${d.title} | T. Roy`;
    document.getElementById("unitTitle").textContent = `Unit ${Number(d.unit)}: ${d.title}`;
    readHash();
    renderTabs();
    go();
  })
  .catch(() => {
    document.getElementById("unitTitle").textContent = "This unit is coming soon 🙂";
  });
askName(false);

let mode = "";               // "" = a section, "practice" or "test" = whole-unit modes

function readHash() {
  const h = new URLSearchParams(location.hash.slice(1));
  const s = parseInt(h.get("s"), 10);
  if (!isNaN(s) && DATA.sections[s]) secIdx = s;
  if (ACTS.some(a => a.id === h.get("a"))) act = h.get("a");
  if (["practice", "test"].includes(h.get("m"))) mode = h.get("m");
}
function writeHash() { history.replaceState(null, "", mode ? `#m=${mode}` : `#s=${secIdx}&a=${act}`); }

function renderTabs() {
  document.getElementById("unitBar").innerHTML = `
    <button class="ubtn practice ${mode === "practice" ? "on" : ""}" data-m="practice">✏️ Practice</button>
    <button class="ubtn test ${mode === "test" ? "on" : ""}" data-m="test">📝 Unit Test</button>
    <a class="ubtn board" href="leaderboard.html?u=${UNIT_ID}">🏅 Leaderboard</a>`;
  const leaveOk = () => !window.TEST_RUNNING || confirm("Leave the Unit Test? Your answers will be lost.");
  document.querySelectorAll(".ubtn[data-m]").forEach(b => b.onclick = () => { if (!leaveOk()) return; mode = b.dataset.m; renderTabs(); go(); });
  document.getElementById("tabs").innerHTML = DATA.sections.map((s, i) =>
    `<button class="tab ${!mode && i === secIdx ? "on" : ""}" data-i="${i}">${esc(s.short || s.title)}</button>`).join("");
  document.querySelectorAll(".tab").forEach(b => b.onclick = () => { if (!leaveOk()) return; mode = ""; secIdx = +b.dataset.i; renderTabs(); go(); });
  const acts = document.getElementById("acts");
  acts.style.display = mode ? "none" : "";
  acts.innerHTML = ACTS.map(a =>
    `<button class="act ${a.id === act ? "on" : ""}" data-a="${a.id}"><span class="e">${a.e}</span>${a.name}</button>`).join("");
  document.querySelectorAll(".act").forEach(b => b.onclick = () => { act = b.dataset.a; renderTabs(); go(); });
}

function go() {
  if (cleanup) { cleanup(); cleanup = null; }
  writeHash();
  if (mode === "practice") Practice();
  else if (mode === "test") UnitTest();
  else {
    const sec = DATA.sections[secIdx];
    ({ learn: Learn, guided: Guided, flash: Flash, match: Match, quiz: Quiz, battle: Battle })[act](sec);
  }
  window.scrollTo({ top: document.getElementById("unitBar").offsetTop - 10, behavior: "smooth" });
}

function header(sec, title, extra) {
  return `<div class="panel-title"><h2>${title}</h2>${extra || ""}</div>
          <p class="small" style="margin-top:-6px">${esc(sec.title)} · 📖 ${esc(sec.pages)}</p>`;
}

// =============== 1. LEARN ===============
function Learn(sec) {
  let i = 0;
  const cards = sec.learn;
  function draw() {
    const c = cards[i];
    view().innerHTML = `<div class="panel">${header(sec, "📘 Learn")}
      <div class="learn-card">
        <span class="tag ${c.tag === "Example" ? "ex" : ""}">${c.tag === "Example" ? "✏️ Example" : "💡 " + esc(c.tag || "Idea")}</span>
        ${c.page ? `<span class="badge" style="float:right;color:var(--teach)">📖 p.${c.page}</span>` : ""}
        <h3>${c.title}</h3>
        ${fig(c.fig)}
        <div>${c.html}</div>
      </div>
      <div class="btnrow">
        <button class="bigbtn grey" id="lp" ${i === 0 ? "disabled" : ""}>⬅ Back</button>
        <button class="bigbtn" id="ln">${i === cards.length - 1 ? "Done ✅" : "Next ➡"}</button>
      </div>
      <div class="dots">Card ${i + 1} of ${cards.length}</div></div>`;
    document.getElementById("lp").onclick = () => { i--; draw(); };
    document.getElementById("ln").onclick = () => {
      if (i < cards.length - 1) { i++; draw(); }
      else { act = "guided"; renderTabs(); go(); }
    };
  }
  draw();
}

// =============== 2. GUIDED ANSWERS ===============
function Guided(sec) {
  const qs = sec.questions;
  let i = 0, shown = 0, hint = false;
  function draw() {
    const q = qs[i];
    const steps = q.steps.slice(0, shown).map((s, k) => `<div class="step${k === shown - 1 ? " new" : ""}"><b class="n">Step ${k + 1}:</b> ${s}</div>`).join("");
    const done = shown >= q.steps.length;
    let btns = "";
    if (!hint) btns += `<button class="bigbtn yellow" id="gh">💡 Hint</button>`;
    if (!done) btns += `<button class="bigbtn" id="gs">${shown === 0 ? "Show Step 1" : "Show next step"}</button>`;
    view().innerHTML = `<div class="panel">${header(sec, "🧭 Guided Answers",
        `<button class="bigbtn dark no-print" id="gprint">🖨️ Print / Save as PDF</button>`)}
      <div class="q-pick">${qs.map((x, k) => `<button class="${k === i ? "on" : ""}" data-k="${k}" title="${esc(x.label)}">${k + 1}</button>`).join("")}</div>
      <div class="q-card">
        <div class="q-head"><span>${esc(q.label)}</span><span class="badge">📖 p.${q.page}</span></div>
        <div class="q-body">
          <div class="q-text">${q.q}</div>
          ${fig(q.fig)}
          ${hint ? `<div class="hint-box">💡 ${q.hint}</div>` : ""}
          ${steps}
          ${done ? `<div class="answer-box"><div>Answer: <span class="final">${q.answer}</span></div><div class="why">✅ WHY: ${q.why}</div></div>` : ""}
          <div class="btnrow">${btns}</div>
        </div>
      </div>
      <div class="btnrow">
        <button class="bigbtn grey" id="gp" ${i === 0 ? "disabled" : ""}>⬅ Previous question</button>
        <button class="bigbtn orange" id="gn" ${i === qs.length - 1 ? "disabled" : ""}>Next question ➡</button>
      </div>
      <div class="dots">Question ${i + 1} of ${qs.length}</div></div>`;
    const on = (id, f) => { const el = document.getElementById(id); if (el) el.onclick = f; };
    on("gh", () => { hint = true; draw(); });
    on("gs", () => { shown++; draw(); });
    on("gp", () => { i--; reset(); });
    on("gn", () => { i++; reset(); });
    on("gprint", () => printGuided(sec));
    view().querySelectorAll(".q-pick button").forEach(b => b.onclick = () => { i = +b.dataset.k; reset(); });
  }
  function reset() { shown = 0; hint = false; draw(); }
  draw();
}

function printGuided(sec) {
  view().innerHTML = `<div class="panel">
    <div class="no-print btnrow"><button class="bigbtn" onclick="window.print()">🖨️ Print / Save as PDF</button>
      <button class="bigbtn grey" id="backG">⬅ Back</button></div>
    <h1>Unit ${Number(DATA.unit)}: ${esc(DATA.title)}</h1>
    <h2>${esc(sec.title)} · Guided Answers</h2>
    <p class="small">T. Roy · 📖 ${esc(sec.pages)}</p>
    ${sec.questions.map(q => `
      <div class="q-card" style="margin-bottom:14px">
        <div class="q-head"><span>${esc(q.label)}</span><span class="badge">📖 p.${q.page}</span></div>
        <div class="q-body">
          <div class="q-text">${q.q}</div>${fig(q.fig, "small")}
          <div class="hint-box">💡 ${q.hint}</div>
          ${q.steps.map((s, k) => `<div class="step"><b class="n">Step ${k + 1}:</b> ${s}</div>`).join("")}
          <div class="answer-box"><div>Answer: <span class="final">${q.answer}</span></div><div class="why">✅ WHY: ${q.why}</div></div>
        </div></div>`).join("")}
  </div>`;
  document.getElementById("backG").onclick = () => go();
  setTimeout(() => window.print(), 300);
}

// =============== 3. FLASHCARDS ===============
function Flash(sec) {
  let deck = sec.flash.slice(), know = [], learning = [], flipped = false;
  function draw() {
    if (!deck.length) {
      view().innerHTML = `<div class="panel">${header(sec, "🃏 Flashcards")}
        <div class="bigscore">🎉</div>
        <p style="text-align:center"><b class="pile-know">I know it: ${know.length}</b> · <b class="pile-learn">Still learning: ${learning.length}</b></p>
        <div class="btnrow">
          ${learning.length ? `<button class="bigbtn orange" id="fl">Practise "Still learning" again</button>` : ""}
          <button class="bigbtn" id="fa">Start again with all cards</button></div></div>`;
      const fl = document.getElementById("fl");
      if (fl) fl.onclick = () => { deck = shuffle(learning); learning = []; draw(); };
      document.getElementById("fa").onclick = () => { deck = sec.flash.slice(); know = []; learning = []; draw(); };
      return;
    }
    const c = deck[0];
    view().innerHTML = `<div class="panel">${header(sec, "🃏 Flashcards", `<button class="bigbtn dark" id="fs">🔀 Shuffle</button>`)}
      <div class="piles"><span>Cards left: ${deck.length}</span><span class="pile-know">✅ I know it: ${know.length}</span><span class="pile-learn">🔁 Still learning: ${learning.length}</span></div>
      <div class="flash-area"><div class="flash ${flipped ? "flipped" : ""}" id="card">
        <div class="face front">${fig(c.fig)}<div>${c.front}</div></div>
        <div class="face back"><div>${c.back}</div></div>
      </div></div>
      <p class="tapnote">Tap the card to flip it</p>
      <div class="btnrow">
        <button class="bigbtn orange" id="fn">🔁 Still learning</button>
        <button class="bigbtn green" id="fk">✅ I know it</button>
      </div></div>`;
    document.getElementById("card").onclick = () => { flipped = !flipped; document.getElementById("card").classList.toggle("flipped", flipped); };
    document.getElementById("fs").onclick = () => { deck = shuffle(deck); flipped = false; draw(); };
    document.getElementById("fk").onclick = () => { know.push(deck.shift()); flipped = false; draw(); };
    document.getElementById("fn").onclick = () => { learning.push(deck.shift()); flipped = false; draw(); };
  }
  draw();
}

// =============== 4. MATCH GAME ===============
function Match(sec) {
  const key = `best_${DATA.unit}_${sec.id}`;
  let timer = null;
  cleanup = () => clearInterval(timer);
  function start() {
    const pairs = shuffle(sec.match).slice(0, 6);
    const tiles = shuffle(pairs.flatMap((p, k) => [{ k, s: p[0] }, { k, s: p[1] }]));
    let sel = null, left = pairs.length, t0 = Date.now(), penalty = 0;
    view().innerHTML = `<div class="panel">${header(sec, "🧩 Match Game")}
      <div class="timer" id="mt">0.0 s</div>
      <p class="tapnote">Tap two cards that go together. A wrong match adds 1 second.</p>
      <div class="match-grid">${tiles.map((t, i) => `<button class="tile" data-i="${i}">${t.s}</button>`).join("")}</div></div>`;
    const mt = document.getElementById("mt");
    timer = setInterval(() => { mt.textContent = (((Date.now() - t0) / 1000) + penalty).toFixed(1) + " s"; }, 100);
    view().querySelectorAll(".tile").forEach(b => b.onclick = () => {
      const i = +b.dataset.i;
      if (b.classList.contains("gone")) return;
      if (sel === null) { sel = i; b.classList.add("sel"); return; }
      if (sel === i) { b.classList.remove("sel"); sel = null; return; }
      const a = view().querySelector(`.tile[data-i="${sel}"]`);
      if (tiles[sel].k === tiles[i].k) {
        a.classList.add("gone"); b.classList.add("gone"); left--;
        if (!left) finish(((Date.now() - t0) / 1000) + penalty, pairs.length);
      } else {
        penalty += 1;
        a.classList.add("bad"); b.classList.add("bad");
        setTimeout(() => { a.classList.remove("bad", "sel"); b.classList.remove("bad"); }, 400);
      }
      a.classList.remove("sel"); sel = null;
    });
  }
  function finish(sec2, n) {
    clearInterval(timer);
    const time = Math.round(sec2 * 10) / 10;
    const best = store.get(key, null);
    const isBest = best === null || time < best;
    if (isBest) store.set(key, time);
    saveScore({ unit: Number(DATA.unit), section: sec.title, activity: "Match Game", score: n, total: n, time });
    view().innerHTML = `<div class="panel">${header(sec, "🧩 Match Game")}
      <div class="bigscore">⏱️ ${time} s</div>
      <p style="text-align:center;font-weight:800">${isBest ? "🎉 New best time!" : `Your best time: ${best} s`}</p>
      <div class="btnrow"><button class="bigbtn green" id="ma">Play again</button></div></div>`;
    document.getElementById("ma").onclick = start;
  }
  const best = store.get(key, null);
  view().innerHTML = `<div class="panel">${header(sec, "🧩 Match Game")}
    <p style="text-align:center">Match each pair as fast as you can!</p>
    ${best !== null ? `<p style="text-align:center;font-weight:800">🏅 Your best time: ${best} s</p>` : ""}
    <div class="btnrow"><button class="bigbtn green" id="ms">Start ▶</button></div></div>`;
  document.getElementById("ms").onclick = start;
}

// =============== 5. SPEED QUIZ ===============
function Quiz(sec) {
  const SHAPES = ["▲", "◆", "●", "■"];
  const LIMIT = 20;
  let timer = null;
  cleanup = () => clearInterval(timer);
  let qs, i, points, correct, streak, t0Quiz;

  function start() {
    qs = shuffle(sec.quiz).slice(0, 10).map(q => {
      const opts = shuffle(q.options.map((o, k) => ({ o, ok: k === 0 })));
      return { ...q, opts };
    });
    i = 0; points = 0; correct = 0; streak = 0; t0Quiz = Date.now();
    ask();
  }
  function ask() {
    const q = qs[i];
    const t0 = Date.now();
    let answered = false;
    view().innerHTML = `<div class="panel">
      <div class="quiz-top"><span>Question ${i + 1} / ${qs.length}</span><span>⭐ ${points}</span><span id="qt">${LIMIT}</span></div>
      <div class="timebar"><div id="tb" style="width:100%"></div></div>
      <div class="quiz-q">${q.q}${fig(q.fig)}</div>
      <div class="opts">${q.opts.map((o, k) => `<button class="opt c${k}" data-k="${k}"><span class="shape">${SHAPES[k]}</span><span>${o.o}</span></button>`).join("")}</div>
      <div id="fb"></div></div>`;
    const tb = document.getElementById("tb"), qt = document.getElementById("qt");
    timer = setInterval(() => {
      const el = (Date.now() - t0) / 1000;
      tb.style.width = Math.max(0, 100 - el / LIMIT * 100) + "%";
      qt.textContent = Math.max(0, Math.ceil(LIMIT - el));
      if (el >= LIMIT && !answered) answer(-1);
    }, 100);
    view().querySelectorAll(".opt").forEach(b => b.onclick = () => { if (!answered) answer(+b.dataset.k); });

    function answer(k) {
      answered = true;
      clearInterval(timer);
      const el = (Date.now() - t0) / 1000;
      const ok = k >= 0 && q.opts[k].ok;
      let gained = 0;
      if (ok) {
        streak++; correct++;
        gained = Math.round(500 + 500 * Math.max(0, (LIMIT - el) / LIMIT));
        const bonus = streak >= 2 ? Math.min(500, (streak - 1) * 100) : 0;
        gained += bonus;
        points += gained;
      } else streak = 0;
      view().querySelectorAll(".opt").forEach((b, j) => {
        b.classList.add(q.opts[j].ok ? "right" : "dim");
        b.disabled = true;
      });
      const right = q.opts.find(o => o.ok).o;
      document.getElementById("fb").innerHTML = `
        <div class="feedback ${ok ? "good" : "bad"}">${ok ? `✅ Correct! +${gained}${streak >= 2 ? ` 🔥 Streak ${streak}` : ""}` : (k < 0 ? "⏰ Time's up!" : "❌ Not quite.")}</div>
        ${ok ? "" : `<p style="text-align:center">The answer is <b>${right}</b>.</p>`}
        <div class="btnrow"><button class="bigbtn" id="qn">${i < qs.length - 1 ? "Next ➡" : "See my score 🏁"}</button></div>`;
      document.getElementById("qn").onclick = () => { i++; i < qs.length ? ask() : end(); };
    }
  }
  function end() {
    const time = Math.round((Date.now() - t0Quiz) / 1000);
    saveScore({ unit: Number(DATA.unit), section: sec.title, activity: "Speed Quiz", score: correct, total: qs.length, time });
    const msg = correct === qs.length ? "Perfect! 🌟" : correct >= 7 ? "Great job! 🎉" : correct >= 4 ? "Good try! Keep practising 💪" : "Try Learn and Guided Answers, then play again 💪";
    view().innerHTML = `<div class="panel">${header(sec, "⚡ Speed Quiz")}
      <div class="bigscore">${correct} / ${qs.length}</div>
      <p style="text-align:center;font-weight:900;font-size:1.3em">⭐ ${points} points</p>
      <p style="text-align:center">${msg}</p>
      <div class="btnrow"><button class="bigbtn green" id="qa">Play again</button></div></div>`;
    document.getElementById("qa").onclick = start;
  }
  view().innerHTML = `<div class="panel">${header(sec, "⚡ Speed Quiz")}
    <p style="text-align:center">10 questions · 20 seconds each<br>Answer fast for more points. Get them right in a row for a 🔥 streak bonus!</p>
    <div class="btnrow"><button class="bigbtn green" id="qs">Start ▶</button></div></div>`;
  document.getElementById("qs").onclick = start;
}

// =============== 6. CLASS BATTLE (teacher, projector) ===============
function Battle(sec) {
  const pool = (sec.battle && sec.battle.length ? sec.battle : sec.quiz.map(q => ({ q: q.q, a: q.options[0], fig: q.fig })));
  const DEFAULT = ["Red Team", "Blue Team", "Yellow Team", "Green Team"];
  let n = 2, names = DEFAULT.slice(), scores, qs, i, revealed;

  function setup() {
    view().innerHTML = `<div class="panel team-setup">${header(sec, "🏆 Class Battle")}
      <p>For the projector. Teams answer, then the teacher clicks the team that got it right.</p>
      <p><b>How many teams?</b></p>
      <div class="cls-row">${[2, 3, 4].map(k => `<button class="clsbtn ${k === n ? "on" : ""}" data-n="${k}">${k}</button>`).join("")}</div>
      <div>${names.slice(0, n).map((nm, k) => `<div><input data-k="${k}" value="${esc(nm)}" maxlength="18"></div>`).join("")}</div>
      <div class="btnrow"><button class="bigbtn green" id="bs">Start battle ▶</button></div></div>`;
    view().querySelectorAll(".clsbtn").forEach(b => b.onclick = () => { n = +b.dataset.n; setup(); });
    view().querySelectorAll("input").forEach(inp => inp.oninput = () => { names[+inp.dataset.k] = inp.value || DEFAULT[+inp.dataset.k]; });
    document.getElementById("bs").onclick = () => {
      scores = new Array(n).fill(0);
      qs = shuffle(pool).slice(0, 10);
      i = 0; revealed = false; draw();
    };
  }
  function board(clickable) {
    return `<div class="scoreboard">${scores.map((s, k) => `
      <div class="team t${k}"><div>${esc(names[k])}</div><div class="pts">${s}</div>
      ${clickable ? `<button data-k="${k}">✅ Got it!</button>` : ""}</div>`).join("")}</div>`;
  }
  function draw() {
    const q = qs[i];
    view().innerHTML = `<div class="panel">
      <div class="quiz-top"><span>🏆 Question ${i + 1} / ${qs.length}</span></div>
      <div class="battle-q">${q.q}${fig(q.fig)}</div>
      ${revealed ? `<div class="battle-a">✅ ${q.a}</div>` : ""}
      ${board(revealed)}
      <div class="btnrow">
        ${revealed ? `<button class="bigbtn grey" id="bnone">Nobody got it ➡</button>` : `<button class="bigbtn orange" id="brev">Show answer 👀</button>`}
        <button class="bigbtn dark" id="bend">End battle 🏁</button>
      </div></div>`;
    const next = () => { i++; revealed = false; i < qs.length ? draw() : end(); };
    const on = (id, f) => { const el = document.getElementById(id); if (el) el.onclick = f; };
    on("brev", () => { revealed = true; draw(); });
    on("bnone", next);
    on("bend", end);
    view().querySelectorAll(".team button").forEach(b => b.onclick = () => { scores[+b.dataset.k]++; next(); });
  }
  function end() {
    const top = Math.max(...scores);
    const winners = names.slice(0, n).filter((_, k) => scores[k] === top);
    view().innerHTML = `<div class="panel">
      <div class="winner">🎉🏆🎉<br>${winners.length > 1 ? "It's a tie!<br>" + winners.map(esc).join(" & ") : esc(winners[0]) + " wins!"}</div>
      ${board(false)}
      <div class="btnrow"><button class="bigbtn green" id="bagain">New battle</button></div></div>`;
    document.getElementById("bagain").onclick = setup;
  }
  setup();
}
