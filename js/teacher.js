// Teacher page: all results from the Google Sheet. The sheet only sends them after the PIN is checked.

let T_ROWS = [], T_LISTS = {};
let tClass = "6/1", tUnit = "all", tAct = "all";
const tv = () => document.getElementById("tView");

function needLogin(msg) {
  tv().innerHTML = `<div class="panel"><p>${msg || "Please log in as the teacher to see results."}</p>
    <div class="btnrow"><button class="bigbtn dark" id="tLogin">👩‍🏫 Teacher login</button></div></div>`;
  document.getElementById("tLogin").onclick = () => askName(true);
}

// called by common.js after a correct PIN
function onTeacherLogin(r) { T_ROWS = r.rows || []; T_LISTS = r.students || {}; draw(); }

async function start() {
  renderStudentBar();
  if (!isTeacher() || !teacherPin()) { needLogin(); return; }
  tv().innerHTML = `<div class="panel"><p>Loading results…</p></div>`;
  const r = await teacherLogin(teacherPin());
  if (!r.ok) { needLogin(r.error); return; }
  onTeacherLogin(r);
}

function fmtT(sec) { const m = Math.floor(sec / 60), s = sec % 60; return `${m}:${String(s).padStart(2, "0")}`; }
const units = () => UNITS.filter(u => u.ready && u.id !== "review").map(u => String(Number(u.id)));

function bestTests(rows) {
  const best = {};
  rows.filter(r => r.activity === "Unit Test").forEach(r => {
    const k = `${r.name}|${r.cls}|${Number(r.unit)}`;
    const b = best[k];
    if (!b || r.score > b.score || (r.score === b.score && r.time < b.time)) best[k] = r;
  });
  return best;
}

function draw() {
  const rows = T_ROWS.filter(r => r.cls === tClass);
  const best = bestTests(rows);
  const names = (T_LISTS[tClass] || []).map(itemName);
  rows.forEach(r => { if (!names.includes(r.name)) names.push(r.name); });   // anyone not on the list still shows
  const us = units();
  const active = new Set(rows.map(r => r.name)).size;
  const tests = rows.filter(r => r.activity === "Unit Test");
  const avg = tests.length ? Math.round(tests.reduce((s, r) => s + r.score / r.total, 0) / tests.length * 100) : null;

  const grid = `<table class="lb"><tr><th>Student</th>${us.map(u => `<th>Unit ${u}</th>`).join("")}<th>Tries</th></tr>
    ${names.map(n => {
      const tries = rows.filter(r => r.name === n && r.activity === "Unit Test").length;
      return `<tr><td>${esc(n)}</td>${us.map(u => {
        const b = best[`${n}|${tClass}|${u}`];
        if (!b) return `<td class="small">–</td>`;
        const pct = b.score / b.total;
        return `<td style="background:${pct >= 0.8 ? "#E8F5E9" : pct >= 0.5 ? "#FFF8D6" : "#FFEBEE"}">${b.score}/${b.total}<br><span class="small">${fmtT(b.time)}</span></td>`;
      }).join("")}<td>${tries}</td></tr>`;
    }).join("")}</table>`;

  const filtered = rows.filter(r => (tUnit === "all" || String(Number(r.unit)) === tUnit) && (tAct === "all" || r.activity === tAct)).slice().reverse();
  const recent = `<table class="lb"><tr><th>When</th><th>Name</th><th>Unit</th><th>Activity</th><th>Section</th><th>Score</th><th>Time</th></tr>
    ${filtered.slice(0, 200).map(r => `<tr><td class="small">${esc(r.datetime)}</td><td>${esc(r.name)}</td><td>${esc(r.unit)}</td><td>${esc(r.activity)}</td><td class="small">${esc(r.section)}</td><td>${r.score}/${r.total}</td><td>${fmtT(r.time)}</td></tr>`).join("")}</table>`;

  tv().innerHTML = `
    <div class="lb-tabs">${CLASSES.map(c => `<button data-c="${c}" class="${c === tClass ? "on" : ""}">Class ${c}</button>`).join("")}</div>
    <div class="panel">
      <div class="statrow">
        <div class="stat"><b>${names.length}</b><span>students</span></div>
        <div class="stat"><b>${active}</b><span>have used the site</span></div>
        <div class="stat"><b>${tests.length}</b><span>Unit Tests taken</span></div>
        <div class="stat"><b>${avg === null ? "–" : avg + "%"}</b><span>average test score</span></div>
      </div>
      <h2>Best Unit Test for each student</h2>
      <p class="small">Green 80% or more · Yellow 50% to 79% · Pink below 50% · – not taken yet</p>
      <div style="overflow-x:auto">${grid}</div>
    </div>
    <div class="panel" style="margin-top:14px">
      <div class="panel-title"><h2>All results</h2><button class="bigbtn dark" id="tCsv">⬇ Download CSV</button></div>
      <div class="lb-tabs">
        <select id="tU"><option value="all">All units</option>${units().map(u => `<option value="${u}" ${u === tUnit ? "selected" : ""}>Unit ${u}</option>`).join("")}</select>
        <select id="tA"><option value="all">All activities</option>${["Unit Test", "Speed Quiz", "Match Game"].map(a => `<option ${a === tAct ? "selected" : ""}>${a}</option>`).join("")}</select>
      </div>
      <div style="overflow-x:auto">${filtered.length ? recent : "<p>No results yet.</p>"}</div>
    </div>
    <div class="panel" style="margin-top:14px">
      <h2>Teacher tools</h2>
      <p>🔺 <b><a href="lesson7.html">Unit 7 lesson and class games</a></b>: very simple step-by-step slides and 5 easy team games for the projector.</p>
      <p>🧊 <b><a href="lesson8.html">Unit 8 lesson and class games</a></b>: the same for 3D shapes and nets.</p>
      <p>📚 <b>Units 9 to 14 lessons and class games</b>: ${[9, 10, 11, 12, 13, 14].map(u => `<a href="lesson.html?u=${String(u).padStart(2, "0")}">Unit ${u}</a>`).join(" · ")}</p>
      <p>🏆 <b>Class Battle</b> (for the projector) is now in every unit section for you only. Students don't see it.</p>
      <p>🖨️ <b>Guided Answers</b> can be printed from any section.</p>
      <p>📋 To fix or add a nickname, edit the <b>Students</b> tab in your Google Sheet.</p>
    </div>`;
  tv().querySelectorAll(".lb-tabs button").forEach(b => b.onclick = () => { tClass = b.dataset.c; draw(); });
  document.getElementById("tU").onchange = e => { tUnit = e.target.value; draw(); };
  document.getElementById("tA").onchange = e => { tAct = e.target.value; draw(); };
  document.getElementById("tCsv").onclick = () => {
    const head = ["Date and time", "Name", "Class", "Unit", "Section", "Activity", "Score", "Total", "Time (s)"];
    const lines = [head].concat(filtered.map(r => [r.datetime, r.name, r.cls, r.unit, r.section, r.activity, r.score, r.total, r.time]))
      .map(a => a.map(v => `"${String(v).replace(/"/g, '""')}"`).join(","));
    const url = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/csv" }));
    const a = document.createElement("a");
    a.href = url; a.download = `results-${tClass.replace("/", "-")}.csv`; a.click();
    URL.revokeObjectURL(url);
  };
}

start();
