"""Checks a unit data file: page order, gaps, duplicates, notation and game data.
Run:  python3 tools/check_unit.py 07
"""
import json
import re
import sys

uid = sys.argv[1] if len(sys.argv) > 1 else "07"
d = json.load(open(f"content/unit{uid}.json", encoding="utf-8"))
errors = []
raw = json.dumps(d, ensure_ascii=False)

if "—" in raw or "–" in raw:
    errors.append("Found an em dash or en dash.")
for bad in ["cm^2", "cm^3", "m^2", "m^3", "cm2", "cm3", "^"]:
    if re.search(re.escape(bad) + r"(?![0-9])", raw):
        errors.append(f"Bad notation found: {bad}")
if "T. Roy" not in open("index.html", encoding="utf-8").read():
    errors.append("Teacher name T. Roy missing from home page.")

last_page = 0
for s in d["sections"]:
    pages = [q["page"] for q in s["questions"]]
    labels = [q["label"] for q in s["questions"]]
    if pages != sorted(pages):
        errors.append(f"{s['id']}: questions not in book page order: {pages}")
    if pages and pages[0] < last_page:
        errors.append(f"{s['id']}: section starts before the previous section ends")
    last_page = max(pages) if pages else last_page
    if len(set(labels)) != len(labels):
        errors.append(f"{s['id']}: duplicate question labels")
    exp = d.get("expectedPages", {}).get(s["id"])
    if exp is not None and sorted(set(pages)) != exp:
        errors.append(f"{s['id']}: pages {sorted(set(pages))} but expected {exp} (gap or extra page)")
    for q in s["questions"]:
        for k in ("q", "hint", "steps", "answer", "why"):
            if not q.get(k):
                errors.append(f"{s['id']} {q['label']}: missing {k}")
    if len(s["quiz"]) < 10:
        errors.append(f"{s['id']}: only {len(s['quiz'])} quiz questions (need 10)")
    for q in s["quiz"]:
        if len(q["options"]) != 4 or len(set(q["options"])) != 4:
            errors.append(f"{s['id']}: quiz needs 4 different options: {q['q']}")
    if len(s["match"]) < 6:
        errors.append(f"{s['id']}: need at least 6 match pairs")
    left = [m[0] for m in s["match"]]; right = [m[1] for m in s["match"]]
    if len(set(left + right)) != len(left + right):
        errors.append(f"{s['id']}: match tiles must all be different")
    if len(s["flash"]) < 6:
        errors.append(f"{s['id']}: need at least 6 flashcards")
    print(f"{s['id']:5} {s['title']:24} questions={len(s['questions']):3} pages={sorted(set(pages))}")

import os
bp = f"content/bank{uid}.json"
if os.path.exists(bp):
    bank = json.load(open(bp, encoding="utf-8"))["questions"]
    braw = json.dumps(bank, ensure_ascii=False)
    if "\u2014" in braw or "\u2013" in braw:
        errors.append("bank: found an em dash or en dash")
    if len(bank) % 10 != 0 or len(bank) < 20:
        errors.append(f"bank: {len(bank)} questions (need a round number, at least 20)")
    texts = [q["q"] + json.dumps(q.get("fig")) for q in bank]
    if len(set(texts)) != len(texts):
        errors.append("bank: duplicate question")
    for q in bank:
        if len(q["options"]) != 4 or len(set(q["options"])) != 4:
            errors.append(f"bank: needs 4 different options: {q['q']}")
        if not q.get("why") or not q.get("src"):
            errors.append(f"bank: missing why or source: {q['q']}")
    print(f"bank  {len(bank)} practice/test questions")
else:
    print("bank  (none yet)")

print("PROBLEMS:" if errors else "All checks passed ✅")
for e in errors:
    print("  -", e)
sys.exit(1 if errors else 0)
