// Thai under the English. The Thai text comes from content/thXX.json (made by tools/build_thai.py).
// The maths is never changed: only extra Thai lines are added under the English.

let TH_DICT = {};
const thaiOn = () => store.get("thai", true);

async function loadThai(uid) {
  try {
    const r = await fetch(`content/th${uid}.json`, { cache: "no-cache" });
    TH_DICT = r.ok ? await r.json() : {};
  } catch (e) { TH_DICT = {}; }
}

// Words used in question labels and book sources ("Exercise 2 (a)", "Review Q27, p.261")
const TH_WORDS = [
  ["Do and Learn", "ลงมือทำและเรียนรู้"], ["Exercise", "แบบฝึกหัด"], ["Let's Recall", "ทบทวน"], ["Let's Think Along", "คิดไปด้วยกัน"],
  ["Problem Solving", "การแก้โจทย์ปัญหา"], ["Math Journal", "บันทึกคณิตศาสตร์"], ["See and Learn", "ดูและเรียนรู้"], ["Hands-On", "ลงมือปฏิบัติ"],
  ["Challenge", "ท้าทาย"], ["Review", "ทบทวน"], ["New", "ใหม่"],
];
function thLabel(s) {
  let t = s, hit = false;
  for (const [en, th] of TH_WORDS) if (t.includes(en)) { t = t.split(en).join(th); hit = true; }
  return hit ? t.replace(/\bQ(\d)/g, "ข้อ $1").replace(/\bp\.(\d)/g, "หน้า $1") : "";
}

function thOf(s) { return thaiOn() && s ? (TH_DICT[s] || "") : ""; }
function tb(s) { const t = thOf(s); return t ? `${s}<span class="th">${t}</span>` : s; }        // text + Thai line
function tlab(s) { const t = thaiOn() ? thLabel(s) : ""; return t ? `${s}<span class="th">${t}</span>` : s; }
function U(en, th) { return thaiOn() ? `${en}<span class="th">${th}</span>` : en; }               // buttons and headings

// Adds the Thai to a whole unit (a copy, so the English data stays as it was).
function thaiUnit(d) {
  const x = JSON.parse(JSON.stringify(d));
  if (!thaiOn()) return x;
  x.sections.forEach(s => {
    s.thTitle = thOf(s.title);
    s.learn.forEach(l => { l.title = tb(l.title); l.html = tb(l.html); });
    s.questions.forEach(q => {
      q.label = tlab(q.label); q.q = tb(q.q); q.hint = tb(q.hint);
      q.steps = q.steps.map(tb); q.answer = tb(q.answer); q.why = tb(q.why);
    });
    s.flash.forEach(f => { f.front = tb(f.front); f.back = tb(f.back); });
    s.match = s.match.map(m => m.map(tb));
    s.quiz.forEach(q => { q.q = tb(q.q); q.options = q.options.map(tb); });
    if (s.battle) s.battle.forEach(q => { q.q = tb(q.q); q.a = tb(q.a); });
  });
  return x;
}
function thaiBank(qs) {
  if (!thaiOn()) return qs;
  return qs.map(q => ({ ...q, q: tb(q.q), options: q.options.map(tb), why: tb(q.why), src: q.src + (thLabel(q.src) ? " · " + thLabel(q.src) : "") }));
}

function thaiSwitch() {
  return `<button class="ubtn thsw ${thaiOn() ? "on" : ""}" id="thSw" title="Thai on or off">🇹🇭 ไทย ${thaiOn() ? "✓" : "✗"}</button>`;
}
