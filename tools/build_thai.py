"""Builds content/thXX.json: the Thai text shown under the English on the website.

The Thai is written in tools/thai/XX.tsv, one line per English text:
    number <TAB> check code <TAB> Thai text
Run:  python3 tools/build_thai.py 07 list     (shows the English texts with their number and check code)
      python3 tools/build_thai.py 07          (checks the Thai and writes content/th07.json)
Every Thai line must keep exactly the same numbers and the same HTML tags as the English,
so a translation can never change the maths.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
LABEL = re.compile(r"^(Do and Learn|Exercise|Let's Recall|Let's Think Along|Problem Solving|Math Journal|See and Learn|Hands-On|Challenge|Review)\b")


def texts(u):
    d = json.load(open(os.path.join(ROOT, "content", f"unit{u}.json"), encoding="utf-8"))
    b = json.load(open(os.path.join(ROOT, "content", f"bank{u}.json"), encoding="utf-8"))
    out = []

    def add(x):
        if x and x not in out and re.search(r"[A-Za-z]{3,}", re.sub(r"<[^>]+>", "", x)) and not LABEL.match(x):
            out.append(x)
    for s in d["sections"]:
        add(s["title"])
        for l in s["learn"]:
            add(l["title"]); add(l["html"])
        for q in s["questions"]:
            add(q["q"]); add(q["hint"])
            for st in q["steps"]:
                add(st)
            add(q["answer"]); add(q["why"])
        for f in s["flash"]:
            add(f["front"]); add(f["back"])
        for m in s["match"]:
            add(m[0]); add(m[1])
        for q in s["quiz"]:
            add(q["q"])
            for o in q["options"]:
                add(o)
    for q in b["questions"]:
        add(q["q"])
        for o in q["options"]:
            add(o)
        add(q["why"])
    return out


def code(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:6]


def nums(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return sorted(re.findall(r"\d+(?:[.,]\d+)*", s))


def tags(s):
    return re.findall(r"</?[a-z]+", s)


def main():
    u = sys.argv[1]
    T = texts(u)
    if len(sys.argv) > 2 and sys.argv[2] == "list":
        a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        z = int(sys.argv[4]) if len(sys.argv) > 4 else len(T)
        for i in range(a, min(z, len(T))):
            print(f"{i}\t{code(T[i])}\t{T[i]}")
        return
    path = os.path.join(ROOT, "tools", "thai", f"{u}.tsv")
    th, problems = {}, []
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        n, c, t = line.split("\t", 2)
        n = int(n)
        if n >= len(T) or code(T[n]) != c:
            problems.append(f"line {ln}: number {n} does not match the English any more")
            continue
        en = T[n]
        if nums(en) != nums(t):
            problems.append(f"line {ln} ({n}): numbers differ. English {nums(en)} Thai {nums(t)}")
        if tags(en) != tags(t):
            problems.append(f"line {ln} ({n}): HTML tags differ")
        if "—" in t:
            problems.append(f"line {ln} ({n}): em dash")
        th[en] = t
    if problems:
        print("THAI CHECK FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    json.dump(th, open(os.path.join(ROOT, "content", f"th{u}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"OK: content/th{u}.json has Thai for {len(th)} of {len(T)} texts. Numbers and tags all match.")


main()
