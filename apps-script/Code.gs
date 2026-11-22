// T. Roy's P.6 Maths website: score receiver, leaderboard, class lists and teacher area (code v5).
// Paste this whole file into Extensions > Apps Script in your Google Sheet.

const SHEET_NAME = "Scores";
const HEADERS = ["Date and time", "Name", "Class", "Unit", "Section", "Activity", "Score", "Total", "Time taken (s)"];

// Teacher PIN: typed by T. Roy in the "Settings" tab of this sheet (cell B2), or set as the
// Script property TEACHER_PIN. It is never written in this file, so it never appears on GitHub.
const MAX_TRIES = 5;          // wrong PINs allowed before a 10 minute pause

function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return ContentService.createTextOutput("error"); }
  if (d && d.action === "teacher") return teacher_(d);
  if (!d || !String(d.name || "").trim() || !String(d.cls || "").trim()) return ContentService.createTextOutput("ignored");
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sheet = getSheet_();
    // Set columns A to F of the new row to plain text FIRST, then write the values.
    // (appendRow ignores the column format and turns "6/1" into a date.)
    const row = sheet.getLastRow() + 1;
    sheet.getRange(row, 1, 1, 6).setNumberFormat("@");
    sheet.getRange(row, 1, 1, 9).setValues([[
      clean_(d.datetime, 30), clean_(d.name, 20), clean_(d.cls, 5),
      clean_(d.unit, 10), clean_(d.section, 60), clean_(d.activity, 30),
      Number(d.score) || 0, Number(d.total) || 0, Number(d.time) || 0
    ]]);
    return ContentService.createTextOutput("ok");
  } catch (err) {
    return ContentService.createTextOutput("error");
  } finally {
    lock.releaseLock();
  }
}

// GET: ?action=leaderboard sends the Unit Test results (first name, class, unit, score, total, time).
// Opening the web app link with nothing after it just says the receiver is working.
function doGet(e) {
  if (e && e.parameter && e.parameter.action === "leaderboard") {
    const values = getSheet_().getDataRange().getValues().slice(1);
    const rows = values
      .filter(r => r[5] === "Unit Test")
      .map(r => ({ name: String(r[1]), cls: String(r[2]), unit: String(r[3]), score: Number(r[6]), total: Number(r[7]), time: Number(r[8]) }));
    return ContentService.createTextOutput(JSON.stringify({ rows: rows }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  if (e && e.parameter && e.parameter.action === "students") return json_({ students: students_() });
  return ContentService.createTextOutput("T. Roy score receiver is working ✅ (code v5)");
}

// The class lists from the "Students" tab: column A class, column D the name shown on the website,
// column E other spellings students might type (comma separated), for "Did you mean…?".
function students_() {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Students");
  const out = { "6/1": [], "6/2": [], "6/3": [] };
  if (!sh) return out;
  sh.getDataRange().getDisplayValues().slice(1).forEach(r => {
    const cls = String(r[0]).trim(), name = String(r[3]).trim();
    if (!cls || !name) return;
    const aka = String(r[4] || "").split(",").map(x => x.trim()).filter(Boolean);
    (out[cls] = out[cls] || []).push(aka.length ? { name: name, aka: aka } : name);
  });
  return out;
}

// Teacher area: only answers when the PIN matches. Too many wrong PINs pause it for 10 minutes.
function teacher_(d) {
  const cache = CacheService.getScriptCache();
  const tries = Number(cache.get("pinTries") || 0);
  if (tries >= MAX_TRIES) return json_({ ok: false, error: "Too many wrong PINs. Wait 10 minutes." });
  const pin = teacherPin_();
  if (!pin) return json_({ ok: false, error: "No teacher PIN is set up yet." });
  if (String(d.pin || "").trim() !== pin) {
    cache.put("pinTries", String(tries + 1), 600);
    return json_({ ok: false, error: "Wrong PIN." });
  }
  cache.remove("pinTries");
  const rows = getSheet_().getDataRange().getDisplayValues().slice(1).map(r => ({
    datetime: r[0], name: r[1], cls: r[2], unit: r[3], section: r[4], activity: r[5],
    score: Number(r[6]), total: Number(r[7]), time: Number(r[8])
  }));
  return json_({ ok: true, rows: rows, students: students_() });
}

function teacherPin_() {
  const prop = PropertiesService.getScriptProperties().getProperty("TEACHER_PIN");
  if (prop) return String(prop).trim();
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Settings");
  return sh ? String(sh.getRange("B2").getDisplayValue()).trim() : "";
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold");
    sheet.setFrozenRows(1);
  }
  // Keep columns A to F as plain text, so a class like "6/1" is not turned into a date (1 June).
  const textCols = sheet.getRange("A:F");
  if (textCols.getNumberFormat() !== "@") textCols.setNumberFormat("@");
  return sheet;
}

// Keeps text short and stops spreadsheet formulas being injected.
// The cells are plain text, so "6/1" and "07" stay exactly as sent.
function clean_(v, max) {
  let s = String(v == null ? "" : v).slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}
