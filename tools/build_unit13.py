"""Builds content/unit13.json for Unit 13: Patterns (book pages 215 to 230).

Every term, sum and count is worked out here and compared with the answer key using check().
The pattern pictures are drawn by code, and the number of toothpicks / tiles / circles in each
picture is counted and checked too, so the pictures always match the numbers.
Run:  python3 tools/build_unit13.py
"""
import contextlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from geo import check as _check, PROBLEMS  # noqa: E402


def check(value, expected, where):
    """Like geo.check, but also compares lists number by number."""
    if isinstance(expected, list):
        if len(value) != len(expected):
            PROBLEMS.append(f"{where}: calculated {value}, answer key says {expected}")
        for i, (a, b) in enumerate(zip(value, expected)):
            _check(a, b, f"{where} [{i + 1}]")
        return value
    return _check(value, expected, where)

with contextlib.redirect_stdout(io.StringIO()):
    from build_unit09 import poly, seg, txt, num, Q, L  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
TILE, TILE2, STICK = "#FFCC80", "#A5D6A7", "#43A047"


def F(items, w=340, h=200):
    return {"w": w, "h": h, "pts": {}, "items": items}


def label(x, y, s, size=13):
    return txt(x, y, s, size, "#37474f")


def stick(a, b):
    return {"t": "seg", "p": [a, b], "color": STICK, "width": 5}


def sticks(edges):
    return [stick(list(a), list(b)) for a, b in edges]


def r1(p):
    return (round(p[0], 1), round(p[1], 1))


# ---------- pattern pictures: each returns (items, width, count) ----------
def square_sticks(k, x0, yb, s=30):
    """Peter's pattern: 1 upright stick, then k squares in a row."""
    e = {(r1((x0 + i * s, yb)), r1((x0 + i * s, yb - s))) for i in range(k + 1)}
    for i in range(k):
        e.add((r1((x0 + i * s, yb)), r1((x0 + (i + 1) * s, yb))))
        e.add((r1((x0 + i * s, yb - s)), r1((x0 + (i + 1) * s, yb - s))))
    return sticks(sorted(e)), k * s, len(e)


def tri_row(n, x0, yb, s=30):
    """Henry's pattern: n triangles in a row, pointing up, down, up, ..."""
    h = s * 0.866
    e = set()
    for j in range(n):
        m = j // 2
        if j % 2 == 0:
            A, B, C = r1((x0 + m * s, yb)), r1((x0 + (m + 1) * s, yb)), r1((x0 + (m + 0.5) * s, yb - h))
        else:
            A, B, C = r1((x0 + (m + 0.5) * s, yb - h)), r1((x0 + (m + 1.5) * s, yb - h)), r1((x0 + (m + 1) * s, yb))
        for a, b in ((A, B), (B, C), (C, A)):
            e.add(tuple(sorted((a, b))))
    return sticks(sorted(e)), (n + 1) // 2 * s + (s / 2 if n % 2 == 0 else 0), len(e)


def tri_stack(n, x0, yb, s=28):
    """Ravi's pattern: rows of upward triangles (1, 2, 3, ... from the top). No sticks are shared."""
    h = s * 0.866
    e = set()
    for r in range(n):                      # r = 0 is the top row
        y = yb - (n - 1 - r) * h
        for i in range(r + 1):
            x = x0 + (n - 1 - r) * s / 2 + i * s
            A, B, C = r1((x, y)), r1((x + s, y)), r1((x + s / 2, y - h))
            for a, b in ((A, B), (B, C), (C, A)):
                e.add(tuple(sorted((a, b))))
    return sticks(sorted(e)), n * s, len(e)


def circle_rows(n, cx, yb, r=8):
    """Opening picture: rows of 1, 3, 5, ... circles."""
    items, c = [], 0
    for row in range(n):
        k = 2 * row + 1
        y = yb - (n - 1 - row) * 2 * r
        for i in range(k):
            items.append({"t": "circle", "c": [round(cx + (i - (k - 1) / 2) * 2 * r, 1), y], "r": r - 1, "fill": TILE})
            c += 1
    return items, (2 * n - 1) * 2 * r, c


def tile_row(n, x0, yb, s=22):
    """Hands-On: 1, 3, 5, ... tiles in 2 colours."""
    k = 2 * n - 1
    return [poly([[x0 + i * s, yb], [x0 + (i + 1) * s, yb], [x0 + (i + 1) * s, yb - s], [x0 + i * s, yb - s]], TILE if i % 2 == 0 else TILE2) for i in range(k)], k * s, k


def cross(n, cx, cy, s=12):
    """Mike's pattern: a centre tile and 4 arms of (n - 1) tiles."""
    cells = {(0, 0)}
    for d in range(1, n):
        cells |= {(d, 0), (-d, 0), (0, d), (0, -d)}
    items = [poly([[cx + x * s - s / 2, cy + y * s - s / 2], [cx + x * s + s / 2, cy + y * s - s / 2], [cx + x * s + s / 2, cy + y * s + s / 2], [cx + x * s - s / 2, cy + y * s + s / 2]], TILE)
             for x, y in sorted(cells)]
    return items, (2 * n - 1) * s, len(cells)


def tables(n, x0, yb, s=26, r=6):
    """Square tables joined in a row, with a seat on each free side."""
    items, seats = [], 0
    for i in range(n):
        items.append(poly([[x0 + i * s, yb], [x0 + (i + 1) * s, yb], [x0 + (i + 1) * s, yb - s], [x0 + i * s, yb - s]], "#ffffff"))
    for i in range(n):
        for y in (yb - s - 12, yb + 12):
            items.append({"t": "circle", "c": [x0 + i * s + s / 2, y], "r": r, "fill": GREEN}); seats += 1
    for x in (x0 - 12, x0 + n * s + 12):
        items.append({"t": "circle", "c": [x, yb - s / 2], "r": r, "fill": GREEN}); seats += 1
    return items, n * s, seats


def square_grid(n, x0, yb, s=12):
    items = [poly([[x0 + i * s, yb - j * s], [x0 + (i + 1) * s, yb - j * s], [x0 + (i + 1) * s, yb - (j + 1) * s], [x0 + i * s, yb - (j + 1) * s]], TILE)
             for i in range(n) for j in range(n)]
    return items, n * s, len(items)


def tri_grid(n, x0, yb, s=18):
    """Janice's pattern: a big triangle cut into n × n small triangles."""
    h = s * 0.866
    items = []
    for r in range(n):                      # r = 0 top row
        y = yb - (n - 1 - r) * h
        for i in range(r + 1):
            x = x0 + (n - 1 - r) * s / 2 + i * s
            items.append(poly([[x, y], [x + s, y], [x + s / 2, y - h]], TILE2))
        for i in range(r):
            x = x0 + (n - 1 - r) * s / 2 + i * s + s / 2
            items.append(poly([[x, y - h], [x + s, y - h], [x + s / 2, y]], "#E8F5E9"))
    return items, n * s, len(items)


def strip(maker, ns, names=None, gap=26, yb=120, x0=14, lab_dy=24, **kw):
    """Draws Figures side by side with their names underneath. Each Figure gets a slot at least 64 px wide
    so names never overlap, and a single Figure is centred on a 320 px wide picture. Returns (fig, counts)."""
    parts, counts, x = [], [], x0
    for k, n in enumerate(ns):
        _, w, _ = maker(n, 0, yb, **kw)
        slot = max(w, 64)
        its, _, c = maker(n, x + (slot - w) / 2, yb, **kw)
        counts.append(c)
        parts.append((its, x + slot / 2, (names or [f"Figure {m}" for m in ns])[k]))
        x += slot + gap
    width = x - gap + x0
    shift = max(0, (320 - width) / 2)
    items = []
    for its, cx, nm in parts:
        items += [shifted(it, shift) for it in its]
        items.append(label(cx + shift, yb + lab_dy, nm))
    return F(items, round(max(width, 320)), yb + lab_dy + 10), counts


def shifted(it, dx):
    """Moves one drawing item dx pixels to the right."""
    it = dict(it)
    if "p" in it and isinstance(it["p"], list):
        it["p"] = [[q[0] + dx, q[1]] if isinstance(q, (list, tuple)) else q for q in it["p"]]
    if "c" in it:
        it["c"] = [it["c"][0] + dx, it["c"][1]]
    if "at" in it:
        it["at"] = [it["at"][0] + dx, it["at"][1]]
    return it


def centred(maker, ns, names=None, gap=26, yb=120, **kw):
    """For pictures drawn from their centre (circles, crosses). All names sit on one line under the biggest Figure."""
    sizes = [maker(n, 0, 0, **kw)[1] for n in ns]
    big = max(sizes)
    parts, counts, x = [], [], 14
    for k, n in enumerate(ns):
        slot = max(sizes[k], 64)
        its, _, c = maker(n, x + slot / 2, yb, **kw)
        counts.append(c)
        parts.append((its, x + slot / 2, (names or [f"Figure {m}" for m in ns])[k]))
        x += slot + gap
    width = x - gap + 14
    shift = max(0, (320 - width) / 2)
    lab_y = yb + 30 if maker is circle_rows else yb + big / 2 + 22
    items = []
    for its, cx, nm in parts:
        items += [shifted(it, shift) for it in its]
        items.append(label(cx + shift, lab_y, nm))
    return F(items, round(max(width, 320)), lab_y + 10), counts


def term(first, jump, n):
    return first + (n - 1) * jump


def term_steps(seq, n):
    """Steps for 'what is term n' in the book's style."""
    first, jump = seq[0], seq[1] - seq[0]
    rows = []
    for i, v in enumerate(seq, start=1):
        rows.append(f"Term {i} is {num(v)} = {num(first)}" + (f" + ({i - 1} × {jump})" if i > 1 else ""))
    return first, jump, [
        f"Find the jump: {num(seq[1])} - {num(seq[0])} = <b>{jump}</b>. The pattern adds {jump} each time.",
        "Look at the terms:<br>" + "<br>".join(rows),
        f"The number of jumps is always 1 less than the term number. Term {n} has {n} - 1 = <b>{n - 1} jumps</b>.",
        f"Term {n} = {num(first)} + ({n - 1} × {jump}) = {num(first)} + {num((n - 1) * jump)} = <b>{num(term(first, jump, n))}</b>",
    ]


# ==================================================================
# PICTURES (counted and checked against the book)
# ==================================================================
fig_open, c = centred(circle_rows, [1, 2, 3], yb=70)
check(c, [1, 4, 9], "p.215 circles")
fig_peter, c = strip(square_sticks, [0, 1, 2, 3], ["Figure 1", "Figure 2", "Figure 3", "Figure 4"], yb=70)
check(c, [1, 4, 7, 10], "p.218 toothpicks")
fig_peter5, c = strip(square_sticks, [4], ["Figure 5"], yb=70)
check(c, [13], "p.219 Figure 5")
fig_tiles, c = strip(tile_row, [1, 2, 3], yb=60)
check(c, [1, 3, 5], "p.220 Hands-On")
fig_henry, c = strip(tri_row, [1, 2, 3, 4], yb=60, gap=22)
check(c, [3, 5, 7, 9], "p.220 Henry")
fig_tables, c = strip(tables, [1, 2, 3], ["1 table", "2 tables", "3 tables"], yb=70, gap=40, x0=26, lab_dy=42)
check(c, [4, 6, 8], "p.222 seats")
fig_ravi, c = strip(tri_stack, [1, 2, 3], yb=100, gap=30)
check(c, [3, 9, 18], "p.223 Ravi")
fig_boxes, c = strip(lambda n, x, yb: tile_row(n, x, yb, 20), [1, 2, 3], ["Day 1", "Day 2", "Day 3"], yb=50)
check(c, [1, 3, 5], "p.224 boxes each day")
fig_mike, c = centred(cross, [1, 2, 3, 4], yb=70)
check(c, [1, 5, 9, 13], "p.225 Mike")
fig_mike5, c = centred(cross, [5], ["Figure 5"], yb=70)
check(c, [17], "p.225 Figure 5")
fig_peterJ, c = strip(square_grid, [1, 2, 3, 4], ["Peter 1", "Peter 2", "Peter 3", "Peter 4"], yb=60, gap=20)
check(c, [1, 4, 9, 16], "p.229 Peter")
fig_janice, c = strip(tri_grid, [1, 2, 3, 4], ["Janice 1", "Janice 2", "Janice 3", "Janice 4"], yb=70, gap=18)
check(c, [1, 4, 9, 16], "p.229 Janice")

# ==================================================================
# 13.1 PROBLEM SOLVING INVOLVING PATTERNS (p.215 to 224)
# ==================================================================
check(65 * 65, 4225, "p.215")
check(term(4, 6, 38), 226, "p.216")
evens = list(range(2, 100, 2))
check(len(evens), 49, "p.217 count"); check(48 + 50, 98, "p.217 pair"); check(24 * 98, 2352, "p.217 pairs"); check(2352 + 98, 2450, "p.217"); check(sum(evens), 2450, "p.217 sum")
check(term(1, 3, 5), 13, "p.219 (a)"); check(term(1, 3, 10), 28, "p.219 (b)")
check(term(1, 2, 10), 19, "Hands-On Figure 10")

learn131 = [
    L("Idea", "What is a pattern?", "<p>A <b>pattern</b> follows the same rule again and again.</p>"
      "<p>In a <b>number pattern</b>, each number is called a <b>term</b>. Term 1 is the first number, term 2 is the second, and so on.</p>"
      "<p>Many patterns <b>add the same number</b> each time. We call it the jump.</p>", None, 216),
    L("Example", "How many circles?", "<p>Ravi's class saw this pattern on the board. How many circles are there in Figure 65?</p>"
      "<p>Figure 1: 1 = 1 × 1<br>Figure 2: 4 = 2 × 2<br>Figure 3: 9 = 3 × 3</p>"
      "<p>These are <b>square numbers</b>. Figure 65 has 65 × 65 = <b>4,225 circles</b>.</p>", fig_open, 215),
    L("Idea", "Finding any term", "<p>Count the jumps! To get to term 5, you make 4 jumps.</p>"
      "<p>The number of jumps is always <b>1 less</b> than the term number.</p>"
      "<p>Term = first number + (number of jumps × the jump)</p>", None, 216),
    L("Example", "4, 10, 16, 22, 28, … term 38", "<p>The jump is 6.</p>"
      "<p>Term 1 = 4<br>Term 2 = 4 + (1 × 6) = 10<br>Term 3 = 4 + (2 × 6) = 16<br>Term 5 = 4 + (4 × 6) = 28</p>"
      "<p>Term 38 = 4 + (37 × 6) = 4 + 222 = <b>226</b></p>", None, 216),
    L("Idea", "Adding in pairs", "<p>To add a long list of numbers, pair the <b>first and last</b>, then the next two, and so on.</p>"
      "<p>Easy start: 1 + 2 + 3 + 4 = (1 + 4) + (2 + 3) = 5 + 5 = 10</p>", None, 217),
    L("Example", "All even numbers smaller than 100", "<p>2 + 4 + 6 + … + 96 + 98. 100 is not included.</p>"
      "<p>From 1 to 100, 100 ÷ 2 = 50 numbers are even. Take away 100: 50 - 1 = <b>49 even numbers</b>.</p>"
      "<p>2 + 96 = 98, 4 + 94 = 98, … 46 + 52 = 98, 48 + 50 = 98. That uses 48 numbers, so 48 ÷ 2 = <b>24 pairs</b> of 98.</p>"
      "<p>24 × 98 = 2,352. The number 98 is left over: 2,352 + 98 = <b>2,450</b></p>", None, 217),
    L("Idea", "Shape patterns", "<p>Look at what is <b>added each time</b>. Make a table: Figure, how many are added, total.</p>"
      "<p>Then use the same rule as for numbers.</p>", None, 218),
    L("Example", "Peter's toothpick squares", "<p>Peter started with 1 toothpick and added more to make squares.</p>"
      "<p>Figure 1: 1<br>Figure 2: 1 + 3 = 4<br>Figure 3: 1 + 3 + 3 = 7<br>Figure 4: 1 + 3 + 3 + 3 = 10</p>"
      "<p>Each new square needs <b>3 more</b> toothpicks.</p>", fig_peter, 218),
    L("Example", "Peter: Figures 5 and 10", "<p>Figure 5 = 1 + (4 × 3) = 1 + 12 = <b>13 toothpicks</b></p>"
      "<p>The groups of 3 are 1 less than the Figure number.</p>"
      "<p>Figure 10 = 1 + (9 × 3) = 1 + 27 = <b>28 toothpicks</b></p>", fig_peter5, 219),
    L("Idea", "Hands-On: tiles in 2 colours", "<p>Work in pairs. Figure 1 has 1 tile, Figure 2 has 3, Figure 3 has 5.</p>"
      "<p>Make Figures 4 and 5 with your tiles. Each time, <b>2 tiles</b> are added.</p>"
      "<p>So Figure 10 = 1 + (9 × 2) = 1 + 18 = <b>19 tiles</b>.</p>", fig_tiles, 220),
]

q131 = []
check(term(3, 2, 10), 21, "p.220 Do and Learn 1")
q131.append(Q("Do and Learn 1", 220, "Henry uses some toothpicks to make the following pattern: How many toothpicks are there in Figure 10?",
              "Count the toothpicks in each Figure. How many are added each time?",
              ["Figure 1 = <b>3</b> toothpicks, Figure 2 = <b>5</b>, Figure 3 = <b>7</b>, Figure 4 = <b>9</b>.",
               "Each new triangle adds <b>2 toothpicks</b>.",
               "Figure 10 has 10 - 1 = <b>9 groups</b> of 2 added.",
               "Figure 10 = 3 + (9 × 2) = 3 + 18 = <b>21</b>"],
              "21 toothpicks", "Start with 3, then add 2 nine times: 3 + 18 = 21.", fig_henry))
for lab, seq, n, ans in (("Do and Learn 2 (a)", [5, 11, 17, 23, 29], 50, 299), ("Do and Learn 2 (b)", [18, 23, 28, 33, 38], 99, 508)):
    first, jump, steps = term_steps(seq, n)
    check(term(first, jump, n), ans, f"p.220 {lab}")
    check([term(first, jump, i) for i in range(1, 6)], seq, f"p.220 {lab} seq")
    q131.append(Q(lab, 220, f"Fill in the missing number. {', '.join(map(str, seq))}, ... From the above pattern, what number is term {n}?",
                  f"Find the jump. Term {n} has {n - 1} jumps.", steps, num(ans), f"{first} + ({n - 1} × {jump}) = {num(ans)}."))
for lab, seq, n, ans, page in (("Exercise 1", [8, 15, 22, 29, 36], 20, 141, 221), ("Exercise 2", [13, 21, 29, 37, 45], 25, 205, 221)):
    first, jump, steps = term_steps(seq, n)
    check(term(first, jump, n), ans, f"p.{page} {lab}")
    check([term(first, jump, i) for i in range(1, 6)], seq, f"p.{page} {lab} seq")
    steps = steps[:1] + [f"The rule is to <b>add {jump} each time</b>."] + steps[1:]
    q131.append(Q(lab, page, f"Look at the following number pattern: {', '.join(map(str, seq))}, ..., ({n}th term) Write the rule for the pattern and find the missing number.",
                  f"What is added each time? The {n}th term has {n - 1} jumps.", steps,
                  f"The rule is to add {jump} each time. The missing number is {num(ans)}.", f"{first} + ({n - 1} × {jump}) = {num(ans)}."))
odds = list(range(1, 100, 2))
check(len(odds), 50, "p.222 count"); check(49 + 51, 100, "p.222 pair"); check(50 // 2, 25, "p.222 pairs"); check(25 * 100, 2500, "p.222"); check(sum(odds), 2500, "p.222 sum")
q131.append(Q("Exercise 3", 222, "Find the sum of all odd numbers that are smaller than 100.",
              "Pair the first and the last: 1 + 99. Then 3 + 97 ...",
              ["From 1 to 100 there are 100 whole numbers. Half are odd: 100 ÷ 2 = <b>50 odd numbers</b>.",
               "Pair them up: 1 + 99 = 100, 3 + 97 = 100, 47 + 53 = 100, 49 + 51 = 100.",
               "All 50 odd numbers are used, so there are 50 ÷ 2 = <b>25 pairs</b>. Each pair makes 100.",
               "25 × 100 = <b>2,500</b>"],
              "2,500", "25 pairs, and each pair adds up to 100."))
check(2 + 30 * 2, 62, "p.222 Exercise 4")
q131.append(Q("Exercise 4", 222, "A square table has 4 seats at first. Each time a table is joined together, some more seats are added. How many seats are there if there are 30 tables?",
              "Count the seats for 1, 2 and 3 tables. What is the same each time?",
              ["1 table: <b>4</b> seats. 2 tables: <b>6</b> seats. 3 tables: <b>8</b> seats.",
               "Each table has 1 seat on top and 1 below: 2 seats for each table. There is also 1 seat at each end: 2 more.",
               "The rule is 2 + (number of tables) × 2. Check: 2 + (3 × 2) = 8 ✓",
               "30 tables: 2 + (30 × 2) = 2 + 60 = <b>62</b>"],
              "62 seats", "2 seats for each of the 30 tables, plus 2 at the ends.", fig_tables))
rv = [3]
for k in range(2, 11):
    rv.append(rv[-1] + k * 3)
check(rv[:4], [3, 9, 18, 30], "p.223 table"); check(rv, [3, 9, 18, 30, 45, 63, 84, 108, 135, 165], "p.223 all"); check(3 * (10 * 11 // 2), 165, "p.223 Figure 10")
q131.append(Q("Exercise 5", 223, "Ravi made the following pattern using toothpicks. He wrote the number of toothpicks needed in the table below. How many toothpicks are needed to make the 10th figure?<br>Figure 1: 3, Figure 2: 9, Figure 3: 18, Figure 4: 30",
              "Find how much is added each time: 3 → 9 → 18 → 30. Is the jump the same?",
              ["The jumps are 9 - 3 = <b>6</b>, 18 - 9 = <b>9</b>, 30 - 18 = <b>12</b>. The jump grows by 3 each time: 2 × 3, 3 × 3, 4 × 3.",
               "Figure 5 = 30 + (5 × 3) = <b>45</b><br>Figure 6 = 45 + (6 × 3) = <b>63</b><br>Figure 7 = 63 + (7 × 3) = <b>84</b>",
               "Figure 8 = 84 + (8 × 3) = <b>108</b><br>Figure 9 = 108 + (9 × 3) = <b>135</b><br>Figure 10 = 135 + (10 × 3) = <b>165</b>"],
              "165 toothpicks", "Each Figure adds a bigger multiple of 3: + 6, + 9, + 12, … + 30.", fig_ravi))
check(1280 // 20, 64, "p.224 boxes"); check(8 * 8, 64, "p.224 day"); check([n * n for n in (1, 2, 3, 4)], [1, 4, 9, 16], "p.224 table")
q131.append(Q("Exercise 6", 224, "Siti has a box of paper clips. There are 20 paper clips in a box. Each day, she buys 2 more boxes of paper clips than the previous day. On which day would she have 1,280 paper clips?",
              "Make a table: boxes each day and total boxes. Do the totals look familiar?",
              ["Boxes each day: 1, 3, 5, 7, … (2 more each day).",
               "Total boxes: Day 1 = <b>1</b>, Day 2 = 1 + 3 = <b>4</b>, Day 3 = 4 + 5 = <b>9</b>, Day 4 = 9 + 7 = <b>16</b>. These are square numbers: 1 × 1, 2 × 2, 3 × 3, 4 × 4.",
               "1,280 paper clips ÷ 20 in a box = <b>64 boxes</b>.",
               "8 × 8 = 64, so it is <b>Day 8</b>."],
              "Day 8", "On Day 8 she has 8 × 8 = 64 boxes, and 64 × 20 = 1,280 paper clips.", fig_boxes))

flash131 = [
    {"front": "Term", "back": "One number in a number pattern (term 1, term 2, …)"},
    {"front": "Rule", "back": "What the pattern does each time, like 'add 6 each time'"},
    {"front": "Jumps to reach term 38", "back": "37 (always 1 less than the term number)"},
    {"front": "Term = ?", "back": "First number + (number of jumps × the jump)"},
    {"front": "Square numbers", "back": "1, 4, 9, 16, 25, … (1 × 1, 2 × 2, 3 × 3, …)"},
    {"front": "Sum of odd numbers smaller than 100", "back": "2,500 (25 pairs of 100)"},
    {"front": "Sum of even numbers smaller than 100", "back": "2,450 (24 pairs of 98, plus 98)"},
    {"front": "Peter's toothpick squares", "back": "1, 4, 7, 10, … add 3 each time"},
    {"front": "Henry's toothpick triangles", "back": "3, 5, 7, 9, … add 2 each time"},
    {"front": "Seats around joined tables", "back": "2 + (number of tables) × 2"},
]
for a, b_ in ((term(4, 6, 38), 226), (term(5, 6, 50), 299), (term(18, 5, 99), 508), (term(8, 7, 20), 141), (term(13, 8, 25), 205), (2 + 30 * 2, 62), (term(1, 3, 10), 28), (65 * 65, 4225)):
    check(a, b_, "match")
match131 = [["4, 10, 16, … term 38", "226"], ["5, 11, 17, … term 50", "299"], ["18, 23, 28, … term 99", "508"], ["8, 15, 22, … term 20", "141"],
            ["13, 21, 29, … term 25", "205"], ["Seats for 30 tables", "62"], ["Peter's Figure 10", "28 toothpicks"], ["Circles in Figure 65", "4,225"]]
for a, b_ in ((term(3, 4, 10), 39), (term(2, 5, 20), 97), (term(7, 3, 30), 94), (term(1, 3, 20), 58), (15 * 15, 225), (2 + 10 * 2, 22), (term(10, 10, 15), 150), (term(3, 2, 25), 51)):
    check(a, b_, "quiz")
quiz131 = [
    {"q": "3, 7, 11, 15, … What is term 10?", "options": ["39", "43", "40", "35"]},
    {"q": "2, 7, 12, 17, … What is term 20?", "options": ["97", "102", "100", "95"]},
    {"q": "What is the rule for 9, 16, 23, 30, …?", "options": ["Add 7 each time", "Add 9 each time", "Multiply by 2", "Add 6 each time"]},
    {"q": "How many jumps from term 1 to term 30?", "options": ["29", "30", "31", "15"]},
    {"q": "7, 10, 13, 16, … What is term 30?", "options": ["94", "97", "90", "100"]},
    {"q": "Peter's toothpicks: 1, 4, 7, 10, … Figure 20?", "options": ["58", "61", "60", "57"]},
    {"q": "Which are square numbers?", "options": ["1, 4, 9, 16", "1, 3, 5, 7", "2, 4, 6, 8", "1, 2, 4, 8"]},
    {"q": "Figure 15 of the circle pattern (1, 4, 9, …) has how many circles?", "options": ["225", "30", "45", "29"]},
    {"q": "Seats around 10 joined tables (rule 2 + tables × 2)?", "options": ["22", "20", "40", "24"]},
    {"q": "3, 5, 7, 9, … What is term 25?", "options": ["51", "53", "50", "75"]},
]
sections = [{"id": "13-1", "title": "Problem Solving Involving Patterns", "short": "1. Patterns", "pages": "p.215 to 224",
             "learn": learn131, "questions": q131, "flash": flash131, "match": match131, "quiz": quiz131}]

# ==================================================================
# UNIT 13 CHALLENGE (p.225 to 230)
# ==================================================================
check(term(1, 4, 5), 17, "p.225 (a)"); check(term(1, 4, 10), 37, "p.225 (b)")
check(420 - 100, 320, "p.228"); check(320 // 40, 8, "p.228"); check(100 + 8 * 40, 420, "p.227")
check(100 * 100, 10000, "p.229")
check(term(50, 30, 10), 320, "p.230 Real Life")
qch = [
    Q("Let's Think Along (a)", 225, "Mike makes the following pattern using square tiles. Draw Figure 5. How many tiles are there in Figure 5?",
      "Count the tiles in each Figure. How many are added each time?",
      ["Figure 1 = <b>1</b> tile, Figure 2 = <b>5</b>, Figure 3 = <b>9</b>, Figure 4 = <b>13</b>.",
       "Each time, 1 tile is added to each of the 4 arms: <b>4 tiles</b> are added.",
       "Figure 5 = 13 + 4 = <b>17</b>. Each arm now has 4 tiles."],
      "17 tiles", "Figure 5 is a cross with a centre tile and 4 arms of 4 tiles: 1 + 16 = 17.", fig_mike),
    Q("Let's Think Along (b)", 225, "Mike makes the following pattern using square tiles. How many tiles are there in Figure 10?",
      "1 tile to start, then groups of 4. How many groups in Figure 10?",
      ["Figure 1 = 1 + (0 × 4) = 1<br>Figure 2 = 1 + (1 × 4) = 5<br>Figure 3 = 1 + (2 × 4) = 9<br>Figure 5 = 1 + (4 × 4) = 17",
       "The groups of 4 are 1 less than the Figure number. Figure 10 has <b>9 groups</b> of 4.",
       "Figure 10 = 1 + (9 × 4) = 1 + 36 = <b>37</b>"],
      "37 tiles", "1 centre tile plus 9 groups of 4.", fig_mike5),
    Q("Problem Solving", 227, "John had 100 baht at first. He saved 40 baht more each day for the next few days. On the last day, he saved 420 baht altogether. How many days did he save 40 baht more each time?",
      "Write the pattern: 100, 140, 180, … How many 40s make the jump from 100 to 420?",
      ["The pattern: 100, then 100 + 40 = <b>140</b>, then 100 + 40 + 40 = <b>180</b>, then <b>220</b>, …",
       "So 100 + (? × 40) = 420.",
       "Take away the 100 he had at first: 420 - 100 = <b>320 baht</b> saved.",
       "320 ÷ 40 = <b>8</b>",
       "<b>Check:</b> 100 + (8 × 40) = 100 + 320 = 420 ✓"],
      "8 days", "8 groups of 40 baht is 320 baht, and 100 + 320 = 420."),
    Q("Math Journal (a)", 229, "Peter and Janice drew some shapes to make a pattern. What is similar between Peter's and Janice's patterns?",
      "Count the squares in Peter's Figures and the small triangles in Janice's Figures.",
      ["Peter: 1, 4, 9, 16 squares.", "Janice: 1, 4, 9, 16 small triangles.", "Both are 1 × 1, 2 × 2, 3 × 3, 4 × 4."],
      "Both are patterns of square numbers: 1, 4, 9, 16, 25 and so on.", "Each Figure has (Figure number) × (Figure number) pieces.", fig_peterJ),
    Q("Math Journal (b)", 229, "Peter and Janice drew some shapes to make a pattern. What is the number of tiles or triangles in Figure 100?",
      "Square numbers: Figure 4 has 4 × 4.",
      ["Figure 4 has 4 × 4 = 16, so Figure 100 has 100 × 100.", "100 × 100 = <b>10,000</b>"],
      "10,000", "Square numbers: 100 × 100 = 10,000.", fig_janice),
]
learn_ch = [
    L("Idea", "Unit 13 big ideas", "<p>Find the <b>jump</b>. Count the jumps: always <b>1 less</b> than the term or Figure number.</p>"
      "<p>Term = first number + (jumps × the jump).</p><p>Square numbers: 1, 4, 9, 16, 25, …</p>", None, 225),
    L("Idea", "Performance Task", "<p>Work in pairs. Make your own pattern with square tiles that adds the <b>same number of tiles</b> each time.</p>"
      "<p>Draw Figures 1 to 4, fill in a table (Figure, tiles added, total), then use your rule to find Figure 10.</p>", None, 226),
    L("Example", "Draw a model to check", "<p>John: 100 baht, then groups of 40 baht, up to 420 baht.</p>"
      "<p>420 - 100 = 320<br>320 ÷ 40 = <b>8 groups</b> of 40 baht</p>", None, 228),
    L("Example", "Math in Real Life", "<p>Dean has 50 baht at first. He then saves 30 baht from the next day onward. How much will he have after 10 days?</p>"
      "<p>Day 1: 50<br>Day 2: 50 + 30<br>Day 3: 50 + 30 + 30<br>Day 4: 50 + 30 + 30 + 30</p>"
      "<p>Day 10 = 50 + (9 × 30) = 50 + 270 = <b>320 baht</b></p>", None, 230),
]
for a, b_ in ((term(1, 4, 20), 77), (100 + 5 * 40, 300), (12 * 12, 144), (term(50, 30, 5), 170)):
    check(a, b_, "challenge quiz")
sections.append({"id": "13-ch", "title": "Unit 13 Challenge", "short": "⭐ Challenge", "pages": "p.225 to 230",
                 "learn": learn_ch, "questions": qch,
                 "flash": flash131[:6] + [{"front": "Mike's crosses", "back": "1, 5, 9, 13, … add 4 each time"}, {"front": "Figure 100 of the square pattern", "back": "10,000"}],
                 "match": match131[:6] + [["Mike's Figure 10", "37 tiles"], ["Square pattern Figure 100", "10,000"]],
                 "quiz": quiz131[:6] + [
                     {"q": "Mike's crosses: 1, 5, 9, 13, … Figure 20?", "options": ["77", "81", "80", "76"]},
                     {"q": "100 baht, then 40 baht more each day for 5 days. Total?", "options": ["300 baht", "240 baht", "200 baht", "500 baht"]},
                     {"q": "Figure 12 of the square pattern?", "options": ["144", "24", "48", "121"]},
                     {"q": "Dean: 50 baht, then 30 baht a day. Day 5?", "options": ["170 baht", "200 baht", "150 baht", "180 baht"]}]})

unit = {"unit": "13", "title": "Patterns", "pages": "p.215 to 230", "sections": sections,
        "expectedPages": {"13-1": [220, 221, 222, 223, 224], "13-ch": [225, 227, 229]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit13.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit13.json ({n} guided questions, {len(sections)} sections).")
