// Whole-unit Practice and Unit Test. Questions come from content/bankXX.json.

const TEST_N = 20;          // questions in a Unit Test
const TEST_MIN = 30;        // minutes for a Unit Test
const PRACTICE_N = 10;      // questions in one practice round
const LETTERS = ["A", "B", "C", "D"];
let BANK = null;

async function loadBank() {
  if (BANK) return BANK;
  const r = await fetch(`content/bank${UNIT_ID}.json`, { cache: "no-cache" });
  if (!r.ok) throw new Error("no bank");
  BANK = thaiBank((await r.json()).questions).map((q, i) => ({ ...q, id: i }));
  return BANK;
}

function prep(q) {
  // shuffle the options but remember which one is right
  return { ...q, opts: shuffle(q.options.map((o, k) => ({ o, ok: k === 0 }))) };
}

function unitHead(title, sub) {
  return `<div class="panel-title"><h2>${title}</h2></div><p class="small" style="margin-top:-6px">Unit ${Number(DATA.unit)}: ${esc(DATA.title)}${sub ? " · " + sub : ""}</p>`;
}

function noBank() {
  view().innerHTML = `<div class="panel"><p>Practice and the Unit Test for this unit are coming soon 🙂</p></div>`;
}

// =============== PRACTICE ===============
async function Practice() {
  let bank;
  try { bank = await loadBank(); } catch (e) { return noBank(); }
  const seenKey = `practiceSeen_${UNIT_ID}`;
  let round = [], i = 0, right = 0, wrong = [], picks = [];

  function intro() {
    const seen = store.get(seenKey, []);
    view().innerHTML = `<div class="panel">${unitHead("✏️ Practice", `${bank.length} questions`)}
      <p>No timer and no pressure. 🙂 Tap an answer and you will see straight away if it is right, with an explanation.</p>
      <p class="pill">You have practised <b>${seen.length}</b> of <b>${bank.length}</b> questions.</p>
      <div class="btnrow"><button class="bigbtn green" id="pStart">Start ${PRACTICE_N} questions ▶</button></div></div>`;
    document.getElementById("pStart").onclick = () => start(pickRound());
  }
  function pickRound() {
    const seen = new Set(store.get(seenKey, []));
    const fresh = shuffle(bank.filter(q => !seen.has(q.id)));
    const old = shuffle(bank.filter(q => seen.has(q.id)));
    return fresh.concat(old).slice(0, PRACTICE_N);
  }
  function start(qs) { round = qs.map(prep); i = 0; right = 0; wrong = []; picks = []; ask(); }

  function ask() {
    const q = round[i];
    const marks = round.map((_, j) => picks[j] === undefined ? "" : round[j].opts[picks[j]].ok ? "✅" : "❌");
    view().innerHTML = `<div class="panel">${unitHead("✏️ Practice", `Question ${i + 1} of ${round.length}`)}
      <div class="progress"><div style="width:${(picks.filter(x => x !== undefined).length / round.length) * 100}%"></div></div>${withSide(`
      <div class="q-card"><div class="q-head"><span>Question ${i + 1}</span><span class="badge">📖 ${esc(q.src)}</span></div>
      <div class="q-body"><div class="q-text">${q.q}</div>${fig(q.fig)}
        <div class="popts">${q.opts.map((o, k) => `<button class="popt" data-k="${k}"><b class="let">${LETTERS[k]}</b><span>${o.o}</span></button>`).join("")}</div>
        <div id="pfb"></div></div></div>
      <div class="btnrow"><button class="bigbtn grey" id="pBack" ${i === 0 ? "disabled" : ""}>${U("⬅ Back", "ย้อนกลับ")}</button></div>`,
      sideList("✏️ This round", round.map((x, j) => short(x.q, 38)), i, marks))}</div>`;
    view().querySelectorAll(".popt").forEach(b => b.onclick = () => choose(+b.dataset.k));
    document.getElementById("pBack").onclick = () => { i--; ask(); };
    onJump(j => { i = j; ask(); });
    if (picks[i] !== undefined) choose(picks[i], true);   // already answered: show it again, it can't be changed
  }

  function choose(k, review) {
    const q = round[i];
    const ok = q.opts[k].ok;
    view().querySelectorAll(".popt").forEach((b, j) => {
      b.disabled = true;
      if (q.opts[j].ok) b.classList.add("right");
      else if (j === k) b.classList.add("wrong");
      else b.classList.add("dim");
    });
    if (!review) { picks[i] = k; if (ok) right++; else wrong.push(round[i]); }
    const seen = new Set(store.get(seenKey, []));
    seen.add(q.id);
    store.set(seenKey, [...seen]);
    const ans = q.opts.find(o => o.ok).o;
    document.getElementById("pfb").innerHTML = ok
      ? `<div class="fb-box good">✅ <b>Correct!</b> ${q.why}</div>`
      : `<div class="fb-box bad">❌ <b>Not quite.</b> The right answer is <b><u>${ans}</u></b>.<div class="why">💡 ${q.why}</div></div>`;
    document.getElementById("pfb").innerHTML += `<div class="btnrow"><button class="bigbtn" id="pNext">${round.some((_, j) => picks[j] === undefined) ? U("Next question ➡", "ข้อถัดไป") : U("See how I did 🏁", "ดูผล")}</button></div>`;
    document.getElementById("pNext").onclick = () => {
      const next = round.findIndex((_, j) => j > i && picks[j] === undefined);
      const any = round.findIndex((_, j) => picks[j] === undefined);
      i = next >= 0 ? next : any;
      i >= 0 ? ask() : end();
    };
    if (!review) document.getElementById("pfb").scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function end() {
    const msg = right === round.length ? "Perfect! 🌟" : right >= round.length * 0.7 ? "Great work! 🎉" : "Good practice! Keep going 💪";
    view().innerHTML = `<div class="panel">${unitHead("✏️ Practice")}
      <div class="bigscore">${right} / ${round.length}</div><p style="text-align:center;font-weight:800">${msg}</p>
      <div class="btnrow">
        ${wrong.length ? `<button class="bigbtn orange" id="pWrong">🔁 Try my wrong ones again (${wrong.length})</button>` : ""}
        <button class="bigbtn green" id="pMore">Next ${PRACTICE_N} questions ▶</button>
        <button class="bigbtn dark" id="pTest">📝 I'm ready for the Unit Test</button>
      </div></div>`;
    const w = document.getElementById("pWrong");
    if (w) w.onclick = () => start(shuffle(wrong.map(x => bank[x.id])));
    document.getElementById("pMore").onclick = () => start(pickRound());
    document.getElementById("pTest").onclick = () => { mode = "test"; renderTabs(); go(); };
  }
  intro();
}

// =============== UNIT TEST ===============
async function UnitTest() {
  let bank;
  try { bank = await loadBank(); } catch (e) { return noBank(); }
  const n = Math.min(TEST_N, bank.length);
  const bestKey = `testBest_${UNIT_ID}`;
  let qs = [], answers = [], i = 0, t0 = 0, timer = null, finished = false;
  const guard = e => { e.preventDefault(); e.returnValue = ""; };
  cleanup = () => { clearInterval(timer); window.removeEventListener("beforeunload", guard); window.TEST_RUNNING = false; };

  function intro() {
    const best = store.get(bestKey, null);
    const s = getStudent();
    view().innerHTML = `<div class="panel">${unitHead("📝 Unit Test")}
      <ul class="rules">
        <li><b>${n} questions</b> from the whole unit</li>
        <li><b>${TEST_MIN} minutes</b> ⏱️ (the test ends by itself when time is up)</li>
        <li>You can go back and change answers before you press <b>Submit</b></li>
        <li>Each right answer = <b>10 points</b>. Your score goes on the 🏅 Leaderboard</li>
      </ul>
      ${s ? `<p>Taking the test as <b>${esc(s.name)}</b> (${esc(s.cls)})</p>` : ""}
      ${best ? `<p class="pill">🏅 Your best: <b>${best.score} / ${best.total}</b> in ${fmtTime(best.time)}</p>` : ""}
      <div class="btnrow"><button class="bigbtn green" id="tStart">Start the test ▶</button></div></div>`;
    document.getElementById("tStart").onclick = () => {
      if (!getStudent()) { askName(true); return; }
      qs = shuffle(bank).slice(0, n).map(prep);
      answers = new Array(n).fill(-1);
      i = 0; t0 = Date.now(); finished = false;
      window.addEventListener("beforeunload", guard);
      window.TEST_RUNNING = true;
      timer = setInterval(tick, 500);
      draw();
    };
  }

  function left() { return Math.max(0, TEST_MIN * 60 - Math.floor((Date.now() - t0) / 1000)); }
  function tick() {
    const el = document.getElementById("tClock");
    const l = left();
    if (el) { el.textContent = "⏱️ " + fmtTime(l); el.classList.toggle("low", l <= 120); }
    if (l <= 0 && !finished) submit(true);
  }

  function draw() {
    const q = qs[i];
    const done = answers.filter(a => a >= 0).length;
    view().innerHTML = `<div class="panel">
      <div class="testbar"><span>📝 Question ${i + 1} / ${n}</span><span id="tClock" class="clock">⏱️ ${fmtTime(left())}</span><span>✔ ${done} answered</span></div>
      <div class="navgrid">${qs.map((_, k) => `<button class="${k === i ? "cur" : ""} ${answers[k] >= 0 ? "done" : ""}" data-k="${k}">${k + 1}</button>`).join("")}</div>
      <div class="q-card"><div class="q-head"><span>Question ${i + 1}</span></div>
      <div class="q-body"><div class="q-text">${q.q}</div>${fig(q.fig)}
        <div class="popts">${q.opts.map((o, k) => `<button class="popt ${answers[i] === k ? "picked" : ""}" data-k="${k}"><b class="let">${LETTERS[k]}</b><span>${o.o}</span></button>`).join("")}</div>
      </div></div>
      <div class="btnrow">
        <button class="bigbtn grey" id="tPrev" ${i === 0 ? "disabled" : ""}>⬅ Back</button>
        ${i < n - 1 ? `<button class="bigbtn" id="tNext">Next ➡</button>` : ""}
        <button class="bigbtn orange" id="tSubmit">Submit test ✅</button>
      </div></div>`;
    view().querySelectorAll(".popt").forEach(b => b.onclick = () => { answers[i] = +b.dataset.k; draw(); });
    view().querySelectorAll(".navgrid button").forEach(b => b.onclick = () => { i = +b.dataset.k; draw(); });
    const on = (id, f) => { const e = document.getElementById(id); if (e) e.onclick = f; };
    on("tPrev", () => { i--; draw(); });
    on("tNext", () => { i++; draw(); });
    on("tSubmit", () => submit(false));
  }

  function submit(timeUp) {
    const blank = answers.filter(a => a < 0).length;
    if (!timeUp && blank && !confirm(`You have ${blank} question${blank > 1 ? "s" : ""} with no answer. Submit anyway?`)) return;
    finished = true;
    cleanup();
    const time = Math.min(TEST_MIN * 60, Math.round((Date.now() - t0) / 1000));
    const score = qs.reduce((s, q, k) => s + (answers[k] >= 0 && q.opts[answers[k]].ok ? 1 : 0), 0);
    saveScore({ unit: (isNaN(Number(DATA.unit)) ? "Review" : Number(DATA.unit)), section: "Whole unit", activity: "Unit Test", score, total: n, time });
    const best = store.get(bestKey, null);
    const isBest = !best || score > best.score || (score === best.score && time < best.time);
    if (isBest) store.set(bestKey, { score, total: n, time });
    const pct = score / n;
    const msg = pct === 1 ? "Perfect score! 🌟🌟🌟" : pct >= 0.8 ? "Excellent! 🎉" : pct >= 0.5 ? "Good effort! 👍" : "Keep practising, you can do it! 💪";
    view().innerHTML = `<div class="panel">${unitHead("📝 Unit Test results")}
      ${timeUp ? `<p class="pill">⏰ Time was up, so your test was sent in.</p>` : ""}
      <div class="bigscore">${score} / ${n}</div>
      <p style="text-align:center;font-weight:900;font-size:1.2em">⭐ ${score * 10} points · ⏱️ ${fmtTime(time)}</p>
      <p style="text-align:center;font-weight:800">${msg}${isBest ? "<br>🏅 Your best score so far!" : ""}</p>
      <div class="btnrow"><a class="bigbtn dark" href="leaderboard.html?u=${UNIT_ID}">🏅 See the leaderboard</a>
        <button class="bigbtn green" id="tAgain">Take a new test</button></div>
      <h3 style="margin-top:20px">Check your answers</h3>
      ${qs.map((q, k) => {
        const mine = answers[k] >= 0 ? q.opts[answers[k]] : null;
        const ok = mine && mine.ok;
        const right = q.opts.find(o => o.ok).o;
        return `<div class="review ${ok ? "good" : "bad"}">
          <div class="rq"><b>${k + 1}.</b> ${q.q} <span class="badge">📖 ${esc(q.src)}</span></div>${fig(q.fig, "small")}
          <div>Your answer: <b>${mine ? mine.o : "(no answer)"}</b> ${ok ? "✅" : "❌"}</div>
          ${ok ? "" : `<div>Right answer: <b><u>${right}</u></b></div>`}
          <div class="why">💡 ${q.why}</div></div>`;
      }).join("")}</div>`;
    document.getElementById("tAgain").onclick = () => { go(); };
    window.scrollTo({ top: document.getElementById("unitBar").offsetTop - 10, behavior: "smooth" });
  }
  intro();
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60), s = sec % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}
