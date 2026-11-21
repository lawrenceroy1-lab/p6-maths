// T. Roy's P.6 Maths website: score receiver and leaderboard.
// Paste this whole file into Extensions > Apps Script in your Google Sheet.

const SHEET_NAME = "Scores";
const HEADERS = ["Date and time", "Name", "Class", "Unit", "Section", "Activity", "Score", "Total", "Time taken (s)"];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    const sheet = getSheet_();
    sheet.appendRow([
      clean_(d.datetime, 30), clean_(d.name, 20), clean_(d.cls, 5),
      clean_(d.unit, 10), clean_(d.section, 60), clean_(d.activity, 30),
      Number(d.score) || 0, Number(d.total) || 0, Number(d.time) || 0
    ]);
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
  return ContentService.createTextOutput("T. Roy score receiver is working ✅");
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

// Keeps text short and saves it exactly as text. The leading ' works like typing '6/1 in a cell:
// Sheets will not turn it into a date, a number (07 → 7) or a formula. The ' itself is not shown.
function clean_(v, max) {
  const s = String(v == null ? "" : v).slice(0, max);
  return s === "" ? "" : "'" + s;
}
