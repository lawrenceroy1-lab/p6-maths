"""Checks content/lessonXX.json (the lesson slides for lesson.html?u=XX).

- Page badges: a slide with a picture ("f": "L1.3") takes the page of that Learn card in unitXX.json;
  other slides take the page of the first Learn card of their section. So badges always match the book data.
- Every Thai line must keep the same numbers as its English line.
- No em dashes. Every picture reference must exist.
Run:  python3 tools/build_lessons.py 09 10 11 12
"""
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def nums(s):
    return sorted(re.findall(r"\d+(?:[.,]\d+)*", re.sub(r"<[^>]+>", " ", s or "")))


def main():
    bad = []
    for u in sys.argv[1:]:
        p = os.path.join(ROOT, "content", f"lesson{u}.json")
        L = json.load(open(p, encoding="utf-8"))
        U = json.load(open(os.path.join(ROOT, "content", f"unit{u}.json"), encoding="utf-8"))
        first = {}
        for k, sl in enumerate(L["slides"]):
            ref = sl.get("f")
            if ref:
                m = re.match(r"^([LQ])(\d+)\.(\d+)$", ref)
                sec = U["sections"][int(m[2])]
                card = (sec["learn"] if m[1] == "L" else sec["questions"])[int(m[3])]
                if not card.get("fig"):
                    bad.append(f"{u} slide {k + 1}: {ref} has no picture")
                sl["p"] = card["page"]
            else:
                sec = U["sections"][min(sl["s"], len(U["sections"]) - 1)]
                sl["p"] = sl.get("p") if sl.get("keep_p") else sec["learn"][0]["page"]
            for en, th in (("t", "tt"), ("h", "th"), ("a", "at"), ("n", "nt")):
                if sl.get(en) and nums(sl[en]) != nums(sl.get(th)):
                    bad.append(f"{u} slide {k + 1} {en}/{th}: numbers {nums(sl[en])} vs {nums(sl.get(th))}")
        for row in L.get("tf", []):
            en, th = row[0].split(" · ", 1)
            if nums(en) != nums(th):
                bad.append(f"{u} true/false '{en}': numbers differ in Thai")
        if "—" in json.dumps(L, ensure_ascii=False):
            bad.append(f"{u}: em dash found")
        json.dump(L, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"lesson{u}.json: {len(L['slides'])} slides, {len(L.get('tf', []))} true/false")
    if bad:
        print("PROBLEMS:")
        for b in bad:
            print("  -", b)
        sys.exit(1)
    print("All lesson checks passed.")


main()
