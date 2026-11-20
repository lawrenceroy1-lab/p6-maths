"""Builds content/unit09.json for Unit 9: Perimeter and Area of Triangles (book pages 71 to 104).

Every perimeter and area is calculated here and compared with the answer key using check().
Run:  python3 tools/build_unit09.py
"""
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, PROBLEMS  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
SQ = "²"


def num(x):
    """Book style numbers: 3,500 and 1,462.5 and 12.5."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    s = f"{x:,.2f}".rstrip("0").rstrip(".")
    return s


def Q(label, page, q, hint, steps, answer, why, fig=None):
    return {"label": label, "page": page, "q": q, "fig": fig, "hint": hint, "steps": steps, "answer": answer, "why": why}


def L(tag, title, html, fig=None, page=None):
    return {"tag": tag, "title": title, "html": html, "fig": fig, "page": page}


def FIG(pts, items, w=320, h=230, names=True, name_off=None):
    """pts: dict name -> [x, y]. Point names starting with '_' are not labelled."""
    its = list(items)
    if names:
        cx = sum(p[0] for p in pts.values()) / len(pts)
        cy = sum(p[1] for p in pts.values()) / len(pts)
        for n, p in pts.items():
            if n.startswith("_"):
                continue
            if name_off and n in name_off:
                d = name_off[n]
            else:
                dx, dy = p[0] - cx, p[1] - cy
                L_ = (dx * dx + dy * dy) ** 0.5 or 1
                d = [round(dx / L_ * 16, 1), round(dy / L_ * 16 + 7, 1)]
            its.append({"t": "pl", "p": n, "d": d})
    return {"w": w, "h": h, "pts": pts, "items": its}


def poly(p, fill):
    return {"t": "poly", "p": p, "fill": fill}


def seg(a, b, dash=False):
    d = {"t": "seg", "p": [a, b]}
    if dash:
        d["dash"] = True
    return d


def lab(a, b, s, off=None):
    d = {"t": "len", "p": [a, b], "s": s}
    if off is not None:
        d["off"] = off
    return d


def ra(v, a, b):
    return {"t": "ra", "v": v, "a": a, "b": b}


def tick(a, b, n=1):
    return {"t": "tick", "p": [a, b], "n": n}


def txt(x, y, s, size=16, color="#1565c0"):
    return {"t": "txt", "at": [x, y], "s": s, "size": size, "bold": True, "color": color}


def grid_fig(cols, rows, pts, shaded, extra=(), size=26, fill=BLUE, w=None, h=None, name_off=None):
    """Points given in grid squares; converted to pixels."""
    P = {n: [20 + x * size, 20 + y * size] for n, (x, y) in pts.items()}
    items = [{"t": "grid", "x": 20, "y": 20, "cols": cols, "rows": rows, "size": size}, poly(shaded, fill)] + list(extra)
    return FIG(P, items, w or cols * size + 40, h or rows * size + 40, name_off=name_off)


# ------------------------------------------------------------------
# Step builders
# ------------------------------------------------------------------
def add_steps(nums, unit):
    steps = []
    total = nums[0]
    for n in nums[1:]:
        steps.append(f"{num(total)} + {num(n)} = {num(total + n)}")
        total += n
    return steps, total


def perim_q(label, page, fig, sides, key, unit="cm", intro=None, q=None, hint=None, extra_first=None):
    check(sum(sides), key, f"p.{page} {label}")
    expr = " + ".join(num(s) for s in sides)
    steps = []
    if extra_first:
        steps += extra_first
    steps += [intro or "The perimeter is the distance all the way around: add the 3 sides.",
              f"Perimeter = {expr}"]
    more, total = add_steps(sides, unit)
    more[-1] = more[-1].rsplit("=", 1)[0] + f"= <b>{num(total)} {unit}</b>"
    steps += more
    return Q(label, page, q or "Find the perimeter of the triangle.",
             hint or "Add the lengths of all 3 sides.", steps, f"Perimeter = {num(key)} {unit}",
             f"{expr} = {num(key)} {unit}", fig)


def area_steps(base, height, unit, base_name="base", height_name="height", note_base=None, note_height=None):
    check(Fraction(1, 2) * Fraction(str(base)) * Fraction(str(height)), Fraction(str(base)) * Fraction(str(height)) / 2, "area")
    prod = base * height
    steps = []
    steps.append(f"The {base_name} is <b>{num(base)} {unit}</b>." + (f" {note_base}" if note_base else ""))
    steps.append(f"The {height_name} is <b>{num(height)} {unit}</b>. It meets the base at a right angle." + (f" {note_height}" if note_height else ""))
    steps.append(f"Area of triangle = ½ × base × height = ½ × {num(base)} × {num(height)}")
    steps.append(f"{num(base)} × {num(height)} = {num(prod)}")
    steps.append(f"Half of {num(prod)}: {num(prod)} ÷ 2 = <b>{num(prod / 2)} {unit}{SQ}</b>")
    return steps, prod / 2


def area_q(label, page, fig, base, height, key, unit="cm", q=None, hint=None, note_base=None, note_height=None, pre=None):
    steps, val = area_steps(base, height, unit, note_base=note_base, note_height=note_height)
    check(val, key, f"p.{page} {label}")
    return Q(label, page, q or "Find the area of the shaded triangle.",
             hint or "Find a base and the height that meets it at a right angle. Area = ½ × base × height.",
             (pre or []) + steps, f"Area = {num(key)} {unit}{SQ}",
             f"The triangle is half of a {num(base)} by {num(height)} rectangle.", fig)


sections = []

# ==================================================================
# 9.1 FINDING PERIMETER OF A TRIANGLE (p.72 to 77)
# ==================================================================
def tri(pts, fill, sides=(), rights=(), ticks=(), w=320, h=230, name_off=None, extra=()):
    names = list(pts.keys())
    items = [poly(names[:3], fill)]
    for a, b, s in sides:
        items.append(lab(a, b, s))
    for v, a, b in rights:
        items.append(ra(v, a, b))
    for a, b, n in ticks:
        items.append(tick(a, b, n))
    return FIG(pts, items + list(extra), w, h, name_off=name_off)


f72 = tri({"A": [160, 30], "B": [260, 200], "C": [60, 200]}, BLUE, [("A", "B", "15 cm"), ("B", "C", "15 cm"), ("C", "A", "15 cm")],
          ticks=[("A", "B", 1), ("B", "C", 1), ("C", "A", 1)])
f73 = tri({"S": [90, 40], "T": [290, 190], "U": [40, 190]}, PINK, [("S", "T", "26 cm"), ("T", "U", "19 cm"), ("U", "S", "12 cm")])
f73c = tri({"E": [150, 30], "F": [270, 190], "G": [40, 190]}, GREEN, [("E", "F", "25 cm"), ("G", "E", "21 cm"), ("F", "G", "?")])
check(15 + 15 + 15, 45, "p.72"); check(12 + 26 + 19, 57, "p.73 Q2"); check(17 + 17 + 11, 45, "p.73 Q3"); check(69 - 21 - 25, 23, "p.73 Q4")
learn91 = [
    L("Idea", "What is perimeter?", "<p>The <b>perimeter</b> is the distance all the way around a shape.</p>"
      "<p>Imagine an ant 🐜 walking along every side of the triangle and back to the start. The distance it walks is the perimeter.</p>"
      "<p><b>Perimeter of a triangle = side + side + side</b></p>", None, 72),
    L("Example", "Equilateral triangle ABC", "<p>Each side is 15 cm.</p><p>Perimeter = 15 + 15 + 15 = <b>45 cm</b></p>", f72, 72),
    L("Example", "Triangle STU", "<p>Perimeter = 12 + 26 + 19</p><p>12 + 26 = 38, 38 + 19 = <b>57 cm</b></p>", f73, 73),
    L("Idea", "Finding a missing side", "<p>If you know the perimeter and 2 sides:</p><p><b>Missing side = perimeter - the 2 sides you know</b></p>", None, 73),
    L("Example", "Find side GE. Perimeter = 69 cm", "<p>The 2 known sides: 21 + 25 = 46 cm.</p><p>GE = 69 - 46 = <b>23 cm</b></p>"
      "<p>Check: 21 + 25 + 23 = 69 ✓</p>", f73c, 73),
]

q91 = []
q91.append(perim_q("Do and Learn (a)", 74, tri({"A": [80, 20], "B": [270, 190], "C": [80, 190]}, YELLOW,
                                                 [("A", "B", "23 cm"), ("B", "C", "20 cm"), ("C", "A", "19 cm")], rights=[("C", "A", "B")]),
                   [23, 20, 19], 62))
q91.append(perim_q("Do and Learn (b)", 74, tri({"E": [160, 20], "F": [215, 200], "G": [105, 200]}, PINK,
                                                 [("E", "F", "19 cm"), ("F", "G", "7 cm")], ticks=[("E", "F", 1), ("G", "E", 1)]),
                   [19, 7, 19], 45, extra_first=["EG and EF have the same tick mark, so EG = EF = <b>19 cm</b>."],
                   hint="The tick marks show 2 equal sides."))
q91.append(perim_q("Do and Learn (c)", 74, tri({"M": [140, 40], "N": [290, 190], "O": [30, 190]}, ORANGE,
                                                 [("M", "N", "24 cm"), ("N", "O", "27 cm"), ("O", "M", "22 cm")], rights=[("M", "O", "N")]),
                   [24, 27, 22], 73))
q91.append(perim_q("Do and Learn (d)", 74, tri({"S": [120, 30], "T": [220, 110], "U": [90, 190]}, BLUE,
                                                 [("S", "T", "12 cm")], ticks=[("S", "T", 1), ("T", "U", 1), ("U", "S", 1)]),
                   [12, 12, 12], 36, extra_first=["All 3 sides have the same tick mark, so every side is <b>12 cm</b>."],
                   hint="The tick marks show that all 3 sides are equal."))

ex1 = [("(a)", {"A": [40, 140], "B": [280, 50], "C": [220, 150]}, ORANGE, [("A", "B", "28 cm"), ("B", "C", "11 cm"), ("C", "A", "22 cm")], [28, 11, 22], 61, (), ()),
       ("(b)", {"Q": [110, 60], "U": [290, 150], "V": [40, 100]}, YELLOW, [("V", "Q", "10 cm"), ("Q", "U", "21 cm"), ("U", "V", "27 cm")], [10, 21, 27], 58, (), ()),
       ("(c)", {"M": [40, 50], "N": [270, 50], "O": [270, 170]}, GREEN, [("M", "N", "25 cm"), ("N", "O", "12 cm"), ("O", "M", "28 cm")], [25, 12, 28], 65, [("N", "M", "O")], ()),
       ("(d)", {"I": [100, 50], "L": [220, 50], "J": [160, 160]}, PINK, [("I", "L", "13 cm")], [13, 13, 13], 39, (), [("I", "L", 1), ("L", "J", 1), ("J", "I", 1)]),
       ("(e)", {"X": [150, 30], "W": [280, 170], "Z": [30, 170]}, BLUE, [("X", "W", "23 cm"), ("W", "Z", "31 cm")], [23, 31, 23], 77, (), [("X", "W", 1), ("Z", "X", 1)]),
       ("(f)", {"S": [50, 30], "T": [230, 90], "U": [240, 200]}, PURPLE, [("S", "T", "24 cm"), ("T", "U", "18 cm"), ("U", "S", "32 cm")], [24, 18, 32], 74, (), ())]
for part, pts, fill, sides, nums_, key, rights, ticks in ex1:
    order = {"(a)": [28, 11, 22], "(b)": [10, 21, 27], "(c)": [25, 12, 28], "(d)": [13, 13, 13], "(e)": [23, 31, 23], "(f)": [24, 18, 32]}[part]
    first = None
    hint = None
    if part == "(d)":
        first = ["All 3 sides have the same tick mark, so all 3 sides are <b>13 cm</b>."]
        hint = "Equal tick marks mean equal sides."
    if part == "(e)":
        first = ["ZX and XW have the same tick mark, so ZX = XW = <b>23 cm</b>."]
        hint = "Equal tick marks mean equal sides."
    q91.append(perim_q(f"Exercise 1 {part}", 75, tri(pts, fill, sides, rights=rights, ticks=ticks), order, key, extra_first=first, hint=hint))

ex2 = [("(a)", {"A": [40, 40], "B": [280, 30], "C": [160, 170]}, ORANGE, [5, 4.5, 3], 12.5, "AB = 5 cm, BC = 4.5 cm, CA = 3 cm"),
       ("(b)", {"E": [80, 40], "F": [230, 40], "G": [80, 200]}, YELLOW, [3, 5, 4], 12, "EF = 3 cm, FG = 5 cm, GE = 4 cm"),
       ("(c)", {"H": [30, 120], "I": [140, 60], "J": [290, 150]}, GREEN, [2.5, 4.1, 6], 12.6, "HI = 2.5 cm, IJ = 4.1 cm, JH = 6 cm"),
       ("(d)", {"K": [50, 40], "L": [240, 40], "M": [240, 200]}, PINK, [4.5, 3.5, 5.7], 13.7, "KL = 4.5 cm, LM = 3.5 cm, MK = 5.7 cm"),
       ("(e)", {"N": [40, 40], "O": [280, 40], "P": [160, 190]}, BLUE, [5.8, 4.3, 4.3], 14.4, "NO = 5.8 cm, OP = 4.3 cm, PN = 4.3 cm"),
       ("(f)", {"Q": [160, 30], "R": [210, 200], "S": [110, 200]}, PURPLE, [4.3, 4.3, 2.2], 10.8, "QR = 4.3 cm, QS = 4.3 cm, SR = 2.2 cm")]
for part, pts, fill, sides, key, meas in ex2:
    q91.append(perim_q(f"Exercise 2 {part}", 76, tri(pts, fill), sides, key,
                       q="Measure all sides of the triangle and find its perimeter. (Measure the triangle in your book with a ruler.)",
                       hint="Measure each side in cm with your ruler. Then add the 3 lengths.",
                       extra_first=[f"Measure each side in your book: {meas}."]))

ex3 = [("(a)", 47, [15, 13], "AC", tri({"A": [40, 50], "B": [230, 60], "C": [210, 190]}, ORANGE, [("A", "B", "15 cm"), ("B", "C", "13 cm"), ("C", "A", "?")]), 19),
       ("(b)", 32, [8, 11], "ON", tri({"M": [160, 40], "N": [290, 180], "O": [40, 180]}, YELLOW, [("O", "M", "8 cm"), ("M", "N", "11 cm"), ("N", "O", "?")]), 13),
       ("(c)", 52, [19, 17], "PS", tri({"P": [80, 30], "Q": [270, 190], "S": [80, 190]}, GREEN, [("P", "Q", "19 cm"), ("Q", "S", "17 cm"), ("S", "P", "?")], rights=[("S", "P", "Q")]), 16)]
for part, per, known, side, fg, key in ex3:
    s2 = known[0] + known[1]
    check(per - s2, key, f"p.77 Q3{part}")
    q91.append(Q(f"Exercise 3 {part}", 77, f"Find the unknown side of the triangle.<br>Perimeter = {per} cm",
                 "Add the 2 sides you know. Take that away from the perimeter.",
                 [f"The perimeter is all 3 sides added: {num(known[0])} + {num(known[1])} + {side} = {per}",
                  f"Add the 2 known sides: {known[0]} + {known[1]} = {s2} cm",
                  f"So {s2} + {side} = {per}",
                  f"{side} = {per} - {s2} = <b>{per - s2} cm</b>",
                  f"Check: {known[0]} + {known[1]} + {per - s2} = {per} ✓"],
                 f"{side} = {key} cm", f"The 3 sides must add up to the perimeter, {per} cm.", fg))
check(36 / 3, 12, "p.77 Q3(d)")
q91.append(Q("Exercise 3 (d)", 77, "Find the unknown side of the triangle.<br>Perimeter = 36 cm",
             "The tick marks show that all 3 sides are equal.",
             ["All 3 sides have the same tick mark. So IJ = JK = KI. It is an equilateral triangle.",
              "The 3 equal sides add up to 36 cm: IJ + IJ + IJ = 36",
              "So 3 groups of IJ make 36. IJ = 36 ÷ 3",
              "IJ = <b>12 cm</b>",
              "Check: 12 + 12 + 12 = 36 ✓"],
             "IJ = 12 cm", "3 equal sides share the perimeter equally: 36 ÷ 3 = 12.",
             tri({"I": [160, 30], "J": [270, 190], "K": [50, 190]}, PURPLE, [("I", "J", "?"), ("J", "K", "?"), ("K", "I", "?")],
                 ticks=[("I", "J", 1), ("J", "K", 1), ("K", "I", 1)])))

flash91 = [
    {"front": "Perimeter", "back": "The distance all the way around a shape"},
    {"front": "Perimeter of a triangle", "back": "side + side + side"},
    {"front": "Missing side", "back": "Perimeter - the 2 known sides"},
    {"front": "Equilateral triangle, side 9 cm. Perimeter?", "back": "9 + 9 + 9 = 27 cm"},
    {"front": "Equilateral triangle, perimeter 30 cm. Each side?", "back": "30 ÷ 3 = 10 cm"},
    {"front": "Sides 5 cm, 7 cm, 9 cm. Perimeter?", "back": "21 cm"},
    {"front": "Perimeter 40 cm, sides 12 cm and 15 cm. Third side?", "back": "40 - 27 = 13 cm"},
    {"front": "Isosceles triangle 10 cm, 10 cm, 6 cm. Perimeter?", "back": "26 cm"},
]
check(27, 9 * 3, "f"); check(30 / 3, 10, "f"); check(5 + 7 + 9, 21, "f"); check(40 - 12 - 15, 13, "f"); check(10 + 10 + 6, 26, "f")
match91 = [["6 + 8 + 10", "24 cm"], ["7 + 7 + 7", "21 cm"], ["15 + 15 + 4", "34 cm"], ["12 + 9 + 11", "32 cm"],
           ["Perimeter 30, sides 10 and 12", "8 cm"], ["Equilateral, perimeter 45", "15 cm"], ["20 + 20 + 9", "49 cm"], ["5.5 + 4.5 + 3", "13 cm"]]
check(6 + 8 + 10, 24, "m"); check(21, 21, "m"); check(15 + 15 + 4, 34, "m"); check(12 + 9 + 11, 32, "m"); check(30 - 22, 8, "m"); check(45 / 3, 15, "m"); check(49, 49, "m"); check(5.5 + 4.5 + 3, 13, "m")
quiz91 = [
    {"q": "Sides 8 cm, 10 cm and 12 cm. Perimeter?", "options": ["30 cm", "28 cm", "960 cm", "40 cm"]},
    {"q": "An equilateral triangle has sides of 11 cm. Perimeter?", "options": ["33 cm", "22 cm", "121 cm", "11 cm"]},
    {"q": "An isosceles triangle has sides 14 cm, 14 cm and 9 cm. Perimeter?", "options": ["37 cm", "23 cm", "28 cm", "42 cm"]},
    {"q": "Perimeter 50 cm. Two sides are 18 cm and 20 cm. Third side?", "options": ["12 cm", "38 cm", "88 cm", "22 cm"]},
    {"q": "Equilateral triangle, perimeter 48 cm. Each side?", "options": ["16 cm", "24 cm", "144 cm", "12 cm"]},
    {"q": "Sides 4.5 cm, 3.5 cm and 5 cm. Perimeter?", "options": ["13 cm", "12 cm", "12.5 cm", "14 cm"]},
    {"q": "Perimeter 36 cm. Two sides are 10 cm and 14 cm. Third side?", "options": ["12 cm", "24 cm", "60 cm", "14 cm"]},
    {"q": "Sides 2.5 cm, 4.1 cm and 6 cm. Perimeter?", "options": ["12.6 cm", "12.5 cm", "11.6 cm", "10.6 cm"]},
    {"q": "Perimeter means…", "options": ["The distance around a shape", "The space inside a shape", "The longest side", "Base × height"]},
    {"q": "Isosceles triangle: 2 equal sides of 7 cm, perimeter 20 cm. Base?", "options": ["6 cm", "13 cm", "14 cm", "3 cm"]},
]
check(8 + 10 + 12, 30, "q"); check(33, 11 * 3, "q"); check(14 + 14 + 9, 37, "q"); check(50 - 38, 12, "q"); check(48 / 3, 16, "q")
check(4.5 + 3.5 + 5, 13, "q"); check(36 - 24, 12, "q"); check(2.5 + 4.1 + 6, 12.6, "q"); check(20 - 14, 6, "q")
sections.append({"id": "9-1", "title": "Finding Perimeter of a Triangle", "short": "1. Perimeter", "pages": "p.72 to 77",
                 "learn": learn91, "questions": q91, "flash": flash91, "match": match91, "quiz": quiz91})

# ==================================================================
# 9.2 FINDING AREA OF A TRIANGLE (p.78 to 88)
# ==================================================================
rel = grid_fig(6, 4, {"A": (0, 0), "B": (6, 0), "C": (6, 4), "D": (0, 4)}, ["A", "C", "D"],
               [poly(["A", "B", "C", "D"], "none"), seg("A", "C")], fill=ORANGE)
check(6 * 4, 24, "p.78 rect"); check(24 / 2, 12, "p.78 tri")
f80 = FIG({"A": [60, 40], "B": [60, 190], "C": [260, 190]}, [poly(["A", "B", "C"], GREEN), ra("B", "A", "C"), lab("A", "B", "3 cm"), lab("B", "C", "4 cm")])
check(Fraction(1, 2) * 4 * 3, 6, "p.80 ABC"); check(Fraction(1, 2) * 10 * 6, 30, "p.80 DEF")
fjkl = FIG({"J": [250, 30], "K": [40, 190], "L": [150, 190], "_F": [250, 190]},
           [poly(["J", "K", "L"], PINK), seg("L", "_F", True), seg("J", "_F", True), ra("_F", "J", "L"),
            lab("K", "L", "7 cm", 16), lab("_F", "J", "16 cm", 16)])
check(Fraction(1, 2) * 7 * 16, 56, "p.81 JKL")
f81 = FIG({"A": [40, 30], "B": [280, 30], "C": [280, 190], "D": [40, 190], "E": [100, 30]},
          [poly(["A", "B", "C", "D"], ORANGE), poly(["D", "E", "C"], "#ffffff"), lab("A", "B", "12 cm", -16), lab("B", "C", "8 cm", -16)])
check(12 * 8, 96, "p.81 rect"); check(Fraction(1, 2) * 12 * 8, 48, "p.81 tri"); check(96 - 48, 48, "p.81 shaded")
learn92 = [
    L("Idea", "Related rectangle", "<p>Draw a rectangle around a triangle so they share the same <b>base</b> and <b>height</b>. This is the triangle's <b>related rectangle</b>.</p>"
      "<p>The triangle is always <b>half</b> of its related rectangle.</p>", rel, 78),
    L("Example", "Rectangle 6 cm by 4 cm", "<p>Area of rectangle = 6 × 4 = 24 cm²</p><p>Triangle ACD is half of it: ½ × 24 = <b>12 cm²</b></p>"
      "<p>Count the squares to check: whole squares and half squares make 12 ✓</p>", rel, 78),
    L("Idea", "The area formula", "<p><b>Area of triangle = ½ × base × height</b></p>"
      "<p>The <b>height</b> must meet the base at a right angle. It can be a side, a dashed line inside, or even a dashed line outside the triangle.</p>", None, 80),
    L("Example", "Triangle ABC", "<p>Base = 4 cm, height = 3 cm.</p><p>Area = ½ × 4 × 3 = ½ × 12 = <b>6 cm²</b></p>", f80, 80),
    L("Example", "Height outside the triangle", "<p>Base KL = 7 cm. The height is the dashed line, 16 cm. It is outside the triangle, but it still meets the base line at a right angle.</p>"
      "<p>Area = ½ × 7 × 16 = ½ × 112 = <b>56 cm²</b></p>", fjkl, 81),
    L("Idea", "Shaded parts", "<p>Sometimes the shaded part is <b>not</b> a triangle.</p><p><b>Shaded area = whole shape - the part that is not shaded</b></p>", None, 81),
    L("Example", "ABCD is a rectangle", "<p>Area of rectangle = 12 × 8 = 96 cm²</p><p>White triangle DEC = ½ × 12 × 8 = 48 cm²</p><p>Shaded part = 96 - 48 = <b>48 cm²</b></p>", f81, 81),
]

q92 = []
q92.append(area_q("Do and Learn 1", 82, grid_fig(8, 6, {"A": (2, 0), "B": (8, 6), "C": (0, 6)}, ["A", "B", "C"]), 8, 6, 24,
                  hint="Count squares. Each square is 1 cm. Count the base along the bottom and the height straight up.",
                  note_base="Count the squares from C to B: 8.", note_height="Count the squares from the base straight up to A: 6."))
q92.append(area_q("Do and Learn 2 (a)", 82, FIG({"A": [80, 30], "B": [80, 190], "C": [200, 190]}, [poly(["A", "B", "C"], PURPLE), ra("B", "A", "C"), lab("A", "B", "8 cm"), lab("B", "C", "6 cm")], names=False),
                  6, 8, 24, q="Find the area of the triangle."))
q92.append(area_q("Do and Learn 2 (b)", 82, FIG({"A": [80, 90], "B": [190, 40], "C": [290, 150]}, [poly(["A", "B", "C"], PINK), ra("B", "A", "C"), lab("B", "A", "5 cm"), lab("B", "C", "12 cm"), lab("A", "C", "13 cm")], names=False),
                  5, 12, 30, q="Find the area of the triangle.",
                  hint="Use the 2 sides that make the right angle. The 13 cm side is not the height.",
                  note_base="It is one of the 2 sides at the right angle.", note_height="The 13 cm side is not used: it does not meet a side at a right angle."))
q92.append(area_q("Exercise 1 (a)", 83, grid_fig(11, 7, {"P": (0, 7), "Q": (11, 1), "R": (7, 7)}, ["P", "Q", "R"]), 7, 6, 21,
                  note_base="Count from P to R along the bottom: 7 squares.", note_height="Count from the base line straight up to Q: 6 squares. (The height is outside the triangle.)"))
q92.append(area_q("Exercise 1 (b)", 83, grid_fig(10, 6, {"R": (0, 1), "S": (8, 1), "T": (10, 6)}, ["R", "S", "T"]), 8, 5, 20,
                  note_base="Count from R to S along the top: 8 squares.", note_height="Count from the line RS straight down to T: 5 squares."))

# Exercise 2 (a): rectangle ACDE 5 x 4, B at (2,0), F at (0,2)
check(5 * 4, 20, "p.84 rect"); check(Fraction(1, 2) * 2 * 2, 2, "p.84 ABF"); check(Fraction(1, 2) * 3 * 4, 6, "p.84 BCD"); check(Fraction(1, 2) * 5 * 2, 5, "p.84 DEF")
check(20 - 2 - 6 - 5, 7, "p.84 shaded")
f84 = grid_fig(5, 4, {"A": (0, 0), "B": (2, 0), "C": (5, 0), "D": (5, 4), "E": (0, 4), "F": (0, 2)}, ["F", "B", "D"])
q92.append(Q("Exercise 2 (a)", 84, "Find the area of the shaded triangle.",
             "The shaded triangle has no easy base and height. Find the big rectangle, then take away the 3 white triangles.",
             ["Area of rectangle ACDE = 5 × 4 = <b>20 cm²</b>",
              "White triangle ABF = ½ × 2 × 2 = <b>2 cm²</b>",
              "White triangle BCD = ½ × 3 × 4: 3 × 4 = 12, 12 ÷ 2 = <b>6 cm²</b>",
              "White triangle DEF = ½ × 5 × 2: 5 × 2 = 10, 10 ÷ 2 = <b>5 cm²</b>",
              "Shaded triangle = 20 - 2 - 6 - 5",
              "20 - 2 = 18, 18 - 6 = 12, 12 - 5 = <b>7 cm²</b>"],
             "Area = 7 cm²", "The rectangle (20 cm²) minus the 3 white triangles (2 + 6 + 5 = 13 cm²) leaves 7 cm².", f84))
check(4 * 3, 12, "p.85 rect"); check(Fraction(1, 2) * 3 * 1, 1.5, "p.85 UVZ"); check(Fraction(1, 2) * 1 * 3, 1.5, "p.85 VWX"); check(Fraction(1, 2) * 4 * 2, 4, "p.85 XYZ")
check(12 - 1.5 - 1.5 - 4, 5, "p.85 shaded")
f85 = grid_fig(4, 3, {"U": (0, 0), "V": (3, 0), "W": (4, 0), "X": (4, 3), "Y": (0, 3), "Z": (0, 1)}, ["Z", "V", "X"])
q92.append(Q("Exercise 2 (b)", 85, "Find the area of the shaded triangle.",
             "Find the big rectangle UWXY, then take away the 3 white triangles.",
             ["Area of rectangle UWXY = 4 × 3 = <b>12 cm²</b>",
              "White triangle UVZ = ½ × 3 × 1: 3 × 1 = 3, 3 ÷ 2 = <b>1.5 cm²</b>",
              "White triangle VWX = ½ × 1 × 3: 1 × 3 = 3, 3 ÷ 2 = <b>1.5 cm²</b>",
              "White triangle XYZ = ½ × 4 × 2: 4 × 2 = 8, 8 ÷ 2 = <b>4 cm²</b>",
              "Shaded triangle = 12 - 1.5 - 1.5 - 4",
              "12 - 1.5 = 10.5, 10.5 - 1.5 = 9, 9 - 4 = <b>5 cm²</b>"],
             "Area = 5 cm²", "12 cm² minus the white triangles (1.5 + 1.5 + 4 = 7 cm²) leaves 5 cm².", f85))

# Exercise 3 (a) to (h)
fa = FIG({"_A": [140, 30], "_B": [60, 170], "_C": [290, 170], "_H": [100, 100]},
         [poly(["_A", "_B", "_C"], YELLOW), seg("_C", "_H", True), ra("_H", "_A", "_C"), lab("_B", "_A", "20 cm", 16), lab("_A", "_C", "28 cm"), lab("_H", "_C", "26 cm", -14)])
fb = FIG({"_A": [70, 30], "_B": [210, 30], "_C": [110, 200], "_H": [110, 30]},
         [poly(["_A", "_B", "_C"], BLUE), seg("_C", "_H", True), ra("_H", "_C", "_B"), lab("_A", "_B", "18 cm", -14), lab("_H", "_C", "24 cm", 18), lab("_B", "_C", "26 cm")])
fc = FIG({"_A": [70, 70], "_B": [100, 40], "_C": [290, 190]},
         [poly(["_A", "_B", "_C"], PINK), ra("_B", "_A", "_C"), lab("_A", "_B", "7 cm", 14), lab("_B", "_C", "24 cm", -14), lab("_C", "_A", "25 cm", -14)])
fd = FIG({"_P": [50, 50], "_A": [150, 50], "_B": [290, 50], "_C": [50, 170]},
         [poly(["_A", "_B", "_C"], GREEN), seg("_P", "_A", True), seg("_P", "_C", True), ra("_P", "_A", "_C"),
          lab("_P", "_A", "30 cm", -14), lab("_A", "_B", "40 cm", -14), lab("_C", "_P", "24 cm", -16)])
fe = FIG({"_A": [210, 20], "_B": [150, 200], "_C": [210, 200]},
         [poly(["_A", "_B", "_C"], PURPLE), ra("_C", "_A", "_B"), lab("_B", "_C", "8 m", 16), lab("_C", "_A", "35 m", 18), lab("_A", "_B", "37 m", 18)])
ff = FIG({"_A": [60, 170], "_B": [130, 120], "_C": [290, 170], "_H": [200, 70]},
         [poly(["_A", "_B", "_C"], ORANGE), seg("_B", "_H", True), seg("_C", "_H", True), ra("_H", "_B", "_C"),
          lab("_A", "_B", "10 m", -14), lab("_H", "_C", "20 m", -14)])
fg_ = FIG({"_A": [70, 40], "_B": [110, 170], "_C": [230, 170], "_P": [70, 170]},
          [poly(["_A", "_B", "_C"], BLUE), seg("_A", "_P", True), seg("_P", "_B", True), ra("_P", "_A", "_B"),
           lab("_P", "_A", "12 m", 18), lab("_B", "_C", "12 m", 16), lab("_A", "_C", "20 m", -14)])
fh = FIG({"_A": [30, 180], "_B": [230, 180], "_C": [270, 110], "_P": [270, 180]},
         [poly(["_A", "_B", "_C"], GREEN), seg("_B", "_P", True), seg("_P", "_C", True), ra("_P", "_C", "_B"),
          lab("_A", "_B", "30 m", 16), lab("_B", "_P", "6 m", 16), lab("_P", "_C", "15 m", 18)])
ex3 = [("(a)", fa, 20, 26, 260, "cm", "The base is the 20 cm side.", "The dashed 26 cm line meets the 20 cm side at a right angle. (The 28 cm side is not needed.)"),
       ("(b)", fb, 18, 24, 216, "cm", "The base is the top side, 18 cm.", "The dashed 24 cm line goes from the bottom corner up to the base. (The 26 cm side is not needed.)"),
       ("(c)", fc, 7, 24, 84, "cm", "The 7 cm and 24 cm sides make the right angle, so one is the base.", "The 25 cm side is not needed."),
       ("(d)", fd, 40, 24, 480, "cm", "The base is the shaded part of the top line: 40 cm (not 30 + 40).", "The dashed line outside is the height. (The 30 cm is outside the triangle and is not part of the base.)"),
       ("(e)", fe, 8, 35, 140, "m", "The base is the bottom, 8 m.", "The 35 m side meets the base at a right angle. (The 37 m side is not needed.)"),
       ("(f)", ff, 10, 20, 100, "m", "The base is the 10 m side.", "The dashed 20 m line meets the 10 m side (made longer) at a right angle."),
       ("(g)", fg_, 12, 12, 72, "m", "The base is the bottom side, 12 m.", "The dashed 12 m line outside the triangle is the height. (The 20 m side is not needed.)"),
       ("(h)", fh, 30, 15, 225, "m", "The base is 30 m. (The 6 m is outside the triangle.)", "The dashed 15 m line outside the triangle is the height.")]
for part, fg, b, h, key, unit, nb, nh in ex3:
    q92.append(area_q(f"Exercise 3 {part}", 86 if part in ("(a)", "(b)", "(c)", "(d)") else 87, fg, b, h, key, unit,
                      note_base=nb, note_height=nh, hint="Find a base and the height that meets it at a right angle. Ignore the extra lengths."))

f88a = FIG({"A": [60, 30], "B": [220, 30], "C": [220, 190], "D": [60, 190], "E": [140, 190]},
           [poly(["A", "B", "C", "D"], "#ffffff"), poly(["A", "E", "C"], ORANGE), tick("D", "E"), tick("E", "C"), lab("A", "B", "12 cm", -14)])
check(12 / 2, 6, "p.88 EC"); check(Fraction(1, 2) * 6 * 12, 36, "p.88 (a)")
q92.append(Q("Exercise 4 (a)", 88, "Find the area of the shaded triangle in the figure.<br>ABCD is a square of side 12 cm and DE = EC.",
             "E is the middle of DC. Use EC as the base.",
             ["DE = EC and DC = 12 cm, so EC = 12 ÷ 2 = <b>6 cm</b>. This is the base.",
              "The height is AD, the side of the square: <b>12 cm</b>. It meets DC at a right angle.",
              "Area = ½ × 6 × 12",
              "6 × 12 = 72, 72 ÷ 2 = <b>36 cm²</b>"],
             "Area = 36 cm²", "The base is half of 12 cm and the height is the full side of the square.", f88a))
f88b = FIG({"A": [40, 180], "C": [120, 180], "F": [280, 180], "B": [280, 30], "D": [160, 105], "E": [205, 105]},
           [poly(["A", "C", "B"], "#ffffff"), poly(["D", "E", "B"], GREEN), seg("C", "F", True), seg("F", "B", True), ra("F", "B", "C"),
            lab("A", "C", "8 cm", 16), lab("F", "B", "14 cm", 18)])
check(Fraction(1, 2) * 8 * 14, 56, "p.88 ABC"); check(56 / 2, 28, "p.88 (b)")
q92.append(Q("Exercise 4 (b)", 88, "Find the area of the shaded triangle in the figure.<br>The area of triangle ABC is twice the area of triangle DBE.",
             "First find the area of the big triangle ABC. The shaded triangle is half of it.",
             ["Triangle ABC: the base is AC = <b>8 cm</b>. The height is BF = <b>14 cm</b> (outside the triangle).",
              "Area of triangle ABC = ½ × 8 × 14: 8 × 14 = 112, 112 ÷ 2 = <b>56 cm²</b>",
              "ABC is twice DBE, so DBE is half of ABC.",
              "Shaded triangle = ½ × 56 = <b>28 cm²</b>"],
             "Area = 28 cm²", "56 is twice 28.", f88b))

flash92 = [
    {"front": "Area of a triangle", "back": "½ × base × height"},
    {"front": "Related rectangle", "back": "The rectangle with the same base and height. The triangle is half of it."},
    {"front": "Height of a triangle", "back": "A line from a vertex that meets the base at 90°"},
    {"front": "Can the height be outside the triangle?", "back": "Yes, it meets the base line made longer"},
    {"front": "Base 10 cm, height 6 cm. Area?", "back": "½ × 10 × 6 = 30 cm²"},
    {"front": "Base 7 cm, height 4 cm. Area?", "back": "½ × 7 × 4 = 14 cm²"},
    {"front": "Unit for area", "back": "Square units: cm², m²"},
    {"front": "Shaded area", "back": "Whole shape - the white part"},
    {"front": "Right triangle 5, 12, 13. Area?", "back": "½ × 5 × 12 = 30 cm² (13 is not used)"},
]
check(Fraction(1, 2) * 10 * 6, 30, "f"); check(Fraction(1, 2) * 7 * 4, 14, "f")
match92 = [["Base 8, height 6", "24 cm²"], ["Base 10, height 5", "25 cm²"], ["Base 12, height 3", "18 cm²"], ["Base 9, height 4", "18.5 cm²"],
           ["Base 7, height 6", "21 cm²"], ["Base 20, height 26", "260 cm²"], ["Base 14, height 10", "70 cm²"], ["Base 5, height 3", "7.5 cm²"]]
# fix the one wrong on purpose? No: every pair must be right.
match92[3] = ["Base 9, height 5", "22.5 cm²"]
for a, b in match92:
    bb, hh = [float(x.split()[-1]) for x in a.split(",")]
    check(bb * hh / 2, float(b.split()[0].replace(",", "")), "match 9.2")
quiz92 = [
    {"q": "Base 12 cm, height 8 cm. Area of the triangle?", "options": ["48 cm²", "96 cm²", "20 cm²", "40 cm²"]},
    {"q": "Base 9 cm, height 6 cm. Area of the triangle?", "options": ["27 cm²", "54 cm²", "15 cm²", "30 cm²"]},
    {"q": "Right triangle with sides 6 cm, 8 cm, 10 cm. Area?", "options": ["24 cm²", "40 cm²", "48 cm²", "30 cm²"]},
    {"q": "Base 15 m, height 4 m. Area?", "options": ["30 m²", "60 m²", "19 m²", "38 m²"]},
    {"q": "A rectangle is 10 cm by 6 cm. Its diagonal cuts it into 2 triangles. Area of one triangle?", "options": ["30 cm²", "60 cm²", "16 cm²", "120 cm²"]},
    {"q": "Rectangle 96 cm², white triangle 48 cm². Shaded part?", "options": ["48 cm²", "144 cm²", "96 cm²", "24 cm²"]},
    {"q": "Base 7 cm, height 5 cm. Area?", "options": ["17.5 cm²", "35 cm²", "12 cm²", "70 cm²"]},
    {"q": "The height of a triangle meets the base at…", "options": ["90°", "60°", "180°", "45°"]},
    {"q": "Base 30 m, height 15 m. Area?", "options": ["225 m²", "450 m²", "45 m²", "90 m²"]},
    {"q": "Which unit is used for area?", "options": ["cm²", "cm", "cm³", "°"]},
    {"q": "Base 40 cm, height 24 cm. Area?", "options": ["480 cm²", "960 cm²", "64 cm²", "240 cm²"]},
]
for b, h, a in [(12, 8, 48), (9, 6, 27), (6, 8, 24), (15, 4, 30), (10, 6, 30), (7, 5, 17.5), (30, 15, 225), (40, 24, 480)]:
    check(b * h / 2, a, "quiz 9.2")
sections.append({"id": "9-2", "title": "Finding Area of a Triangle", "short": "2. Area", "pages": "p.78 to 88",
                 "learn": learn92, "questions": q92, "flash": flash92, "match": match92, "quiz": quiz92})

# ==================================================================
# 9.3 WORD PROBLEMS (p.89 to 98)
# ==================================================================
check(Fraction(1, 2) * 32 * 26, 416, "p.89 Q1"); check(48 - 16 - 12, 20, "p.89 Q2"); check(28 + 20 + 26, 74, "p.90 Q3")
check(17 + 23.5 + 16, 56.5, "p.90 Q4 P"); check(Fraction(1, 2) * 16 * 17, 136, "p.90 Q4 A"); check((1.2 + 0.8 + 0.8) * 100, 280, "p.91 Q5")
check(70 * 50, 3500, "p.91 rect"); check(Fraction(1, 2) * 54 * 25, 675, "p.91 tri"); check(3500 - 675, 2825, "p.91 Q6")
check(6 * 6 + Fraction(1, 2) * 4 * 6, 48, "p.92 Q7 m1"); check(10 * 6 - Fraction(1, 2) * 4 * 6, 48, "p.92 Q7 m2"); check(4 * Fraction(1, 2) * 2 * 3, 12, "p.92 Q8")
f92 = FIG({"P": [40, 40], "T": [160, 40], "Q": [240, 40], "R": [240, 160], "S": [40, 160]},
          [poly(["P", "T", "R", "S"], GREEN), poly(["T", "Q", "R"], "#ffffff"), seg("T", [160, 160], True), lab("S", "R", "10 m", 16), lab("S", "P", "6 m", 16), lab("P", "T", "6 m", -14)])
learn93 = [
    L("Idea", "Solving word problems", "<p>1. <b>Read</b> and draw a picture.</p><p>2. Is it asking for <b>perimeter</b> (distance around) or <b>area</b> (space inside)?</p>"
      "<p>3. Write the numbers on the picture.</p><p>4. Calculate and write the <b>unit</b>: cm or m for perimeter, cm² or m² for area.</p>", None, 89),
    L("Example", "Lily's triangular wood", "<p>Lily paints a triangular piece of wood with base 32 cm and height 26 cm. What area does she paint?</p>"
      "<p>Area = ½ × 32 × 26 = ½ × 832 = <b>416 cm²</b></p>", None, 89),
    L("Example", "A missing side", "<p>A tile has perimeter 48 cm. Two sides are 16 cm and 12 cm.</p>"
      "<p>16 + 12 = 28. The third side = 48 - 28 = <b>20 cm</b>.</p>", None, 89),
    L("Idea", "Change units first", "<p>1 m = 100 cm. To change m to cm, <b>× 100</b>.</p><p>2.8 m = 2.8 × 100 = <b>280 cm</b></p>", None, 91),
    L("Example", "Tom's triangular scarf", "<p>Tom's scarf has sides 1.2 m, 0.8 m and 0.8 m. Perimeter in cm?</p>"
      "<p>1.2 + 0.8 + 0.8 = 2.8 m = 2.8 × 100 = <b>280 cm</b></p>", None, 91),
    L("Idea", "Two ways to find a shaded area", "<p><b>Add</b> the pieces together, or</p><p>find the <b>whole</b> shape and <b>take away</b> the white part.</p>", f92, 92),
    L("Example", "Area of the field PTRS", "<p><b>Way 1:</b> square 6 × 6 = 36 m², triangle ½ × 4 × 6 = 12 m², 36 + 12 = <b>48 m²</b></p>"
      "<p><b>Way 2:</b> rectangle 10 × 6 = 60 m², white triangle 12 m², 60 - 12 = <b>48 m²</b></p>", f92, 92),
]

q93 = []
check(46.5 - 14.5 - 14.5, 17.5, "p.93 Q1")
q93.append(Q("Do and Learn 1", 93, "Alex cut a piece of paper into an isosceles triangle. Its perimeter is 46.5 cm. If the adjacent sides to the vertex are 14.5 cm each, what is its base?",
             "The 2 sides next to the vertex are equal (14.5 cm each). The base is what is left of the perimeter.",
             ["The 2 equal sides: 14.5 + 14.5 = <b>29 cm</b>", "Base = perimeter - the 2 equal sides = 46.5 - 29",
              "46.5 - 29 = <b>17.5 cm</b>", "Check: 14.5 + 14.5 + 17.5 = 46.5 ✓"],
             "17.5 cm", "The 3 sides must add up to 46.5 cm.",
             FIG({"V": [160, 30], "_B": [250, 190], "_C": [70, 190]}, [poly(["V", "_B", "_C"], PINK), lab("_C", "V", "14.5 cm"), lab("V", "_B", "14.5 cm"), lab("_B", "_C", "?")], names=False)))
check(10 - 6, 4, "p.93 Q2 base"); check(Fraction(1, 2) * 4 * 15, 30, "p.93 Q2")
f93 = FIG({"A": [40, 40], "B": [250, 40], "C": [250, 180], "D": [40, 180], "_G": [250, 96]},
          [poly(["A", "B", "C", "D"], "#ffffff"), poly(["D", "B", "_G"], ORANGE), lab("A", "B", "15 cm", -14), lab("D", "A", "10 cm", 16), lab("C", "_G", "6 cm", -16)])
q93.append(Q("Do and Learn 2", 93, "Marvin cut out the orange triangle from the rectangular piece of paper shown. What is the area of the orange triangle?",
             "Use the short side on BC as the base. The height is the length of the rectangle.",
             ["BC is 10 cm long (the same as AD). The bottom part of BC is 6 cm.",
              "So the base of the orange triangle (on BC) = 10 - 6 = <b>4 cm</b>.",
              "The height goes from D straight across to BC: <b>15 cm</b>.",
              "Area = ½ × 4 × 15: 4 × 15 = 60, 60 ÷ 2 = <b>30 cm²</b>"],
             "30 cm²", "The orange triangle has base 4 cm on BC and height 15 cm.", f93))
check(36.5 + 22.5 + 22.5, 81.5, "p.94 Q1")
q93.append(Q("Exercise 1", 94, "An aluminum sheet in the shape of an isosceles triangle has a base of 36.5 cm. If each adjacent side to the vertex of this triangle is 22.5 cm, what is its perimeter?",
             "An isosceles triangle has 2 equal sides. Add all 3 sides.",
             ["The 3 sides are 36.5 cm, 22.5 cm and 22.5 cm.", "Perimeter = 36.5 + 22.5 + 22.5",
              "36.5 + 22.5 = 59, 59 + 22.5 = <b>81.5 cm</b>"],
             "81.5 cm", "36.5 + 22.5 + 22.5 = 81.5"))
check(Fraction(1, 2) * 7 * 9, 31.5, "p.94 Q2")
q93.append(Q("Exercise 2", 94, "The floor pattern of a room is as shown below. What is the area of the green part?",
             "Use EG as the base (count the squares down). The height goes across to F.",
             ["Each square is 1 cm. The base EG goes down the left side: count <b>7 squares</b>, so 7 cm.",
              "The height goes from the line EG straight across to F: count <b>9 squares</b>, so 9 cm.",
              "Area = ½ × 7 × 9: 7 × 9 = 63, 63 ÷ 2 = <b>31.5 cm²</b>"],
             "31.5 cm²", "The green triangle EFG has base 7 cm and height 9 cm.",
             grid_fig(9, 7, {"E": (0, 0), "F": (9, 1), "G": (0, 7)}, ["E", "F", "G"], fill=GREEN)))
check(15.5 * 3, 46.5, "p.95 Q3")
q93.append(Q("Exercise 3", 95, "The length of a playground in the shape of an equilateral triangle is 15.5 m. What is its perimeter?",
             "An equilateral triangle has 3 equal sides.",
             ["All 3 sides are 15.5 m.", "Perimeter = 15.5 + 15.5 + 15.5", "15.5 + 15.5 = 31, 31 + 15.5 = <b>46.5 m</b>"],
             "46.5 m", "3 sides of 15.5 m: 3 × 15.5 = 46.5"))
check((96 - 34) / 2, 31, "p.95 Q4")
q93.append(Q("Exercise 4", 95, "Jaden owns a land in the shape of an isosceles triangle. Its perimeter is 96 m. If one of the non-identical sides of the land is 34 m, what are the lengths of the other two sides?",
             "The other 2 sides are the same length. Take away 34 m, then share what is left equally.",
             ["An isosceles triangle has 2 sides the same length. The 34 m side is the different one.",
              "The 2 equal sides together = 96 - 34 = <b>62 m</b>",
              "Each equal side = 62 ÷ 2 = <b>31 m</b>",
              "Check: 34 + 31 + 31 = 96 ✓"],
             "31 m each", "The 2 equal sides share the 62 m: 31 + 31 = 62."))
check(28 + 9, 37, "p.96 Q5 base"); check(Fraction(1, 2) * 37 * 24, 444, "p.96 Q5")
f96a = FIG({"_A": [40, 40], "_T": [210, 40], "_B": [270, 40], "_C": [270, 180], "_D": [40, 180]},
           [poly(["_A", "_B", "_C", "_D"], "#ffffff"), poly(["_D", "_T", "_C"], ORANGE), lab("_A", "_T", "28 m", -14), lab("_T", "_B", "9 m", -14), lab("_D", "_A", "24 m", 18),
            txt(110, 90, "A", 18, "#1f2a44"), txt(170, 140, "B", 18, "#1f2a44")], names=False)
q93.append(Q("Exercise 5", 96, "A land in the shape of a rectangle was divided into 3 parts as shown below. What is the area of Part B?",
             "Part B's base is the whole bottom of the rectangle. Its height is the width of the rectangle.",
             ["The bottom of the rectangle = 28 + 9 = <b>37 m</b>. This is the base of Part B.",
              "The height of Part B = the width of the rectangle = <b>24 m</b>.",
              "Area = ½ × 37 × 24", "37 × 24 = 888, 888 ÷ 2 = <b>444 m²</b>"],
             "444 m²", "Part B has base 37 m and height 24 m.", f96a))
check(Fraction(1, 2) * 60 * 25, 750, "p.96 ABD"); check(Fraction(1, 2) * 65 * 45, 1462.5, "p.96 BCD"); check(750 + 1462.5, 2212.5, "p.96 ABCD"); check(25 + 65 + 60, 150, "p.96 perim")
f96b = FIG({"A": [50, 190], "B": [50, 120], "C": [220, 20], "D": [280, 190], "E": [175, 150]},
           [poly(["A", "B", "C", "D"], GREEN), seg("B", "D"), seg("C", "E", True), ra("A", "B", "D"), ra("E", "C", "D"),
            lab("A", "B", "25 cm", -18), lab("A", "D", "60 cm", 16), lab("B", "E", "65 cm", 14), lab("C", "E", "45 cm", 16)])
q93.append(Q("Exercise 6", 96, "The figure ABCD is made up of two different triangles. ABD is a right triangle. AB = 25 cm, AD = 60 cm, BD = 65 cm and CE = 45 cm. Find the area of figure ABCD. Find the perimeter of triangle ABD.",
             "Find each triangle's area and add them. For BCD, BD is the base and CE is the height.",
             ["Triangle ABD: base AD = 60 cm, height AB = 25 cm.", "Area of ABD = ½ × 60 × 25: 60 × 25 = 1,500, 1,500 ÷ 2 = <b>750 cm²</b>",
              "Triangle BCD: base BD = 65 cm, height CE = 45 cm.", "Area of BCD = ½ × 65 × 45: 65 × 45 = 2,925, 2,925 ÷ 2 = <b>1,462.5 cm²</b>",
              "Area of ABCD = 750 + 1,462.5 = <b>2,212.5 cm²</b>",
              "Perimeter of triangle ABD = 25 + 65 + 60 = <b>150 cm</b>"],
             "Area of ABCD = 2,212.5 cm², perimeter of ABD = 150 cm", "The figure is 2 triangles added together.", f96b))
check(80 / 10, 8, "p.97 width"); check(8 / 2, 4, "p.97 BC"); check(10 - 4, 6, "p.97 AB")
check(Fraction(1, 2) * 6 * 8, 24, "p.97 ABF"); check(Fraction(1, 2) * 4 * 4, 8, "p.97 BCD"); check(Fraction(1, 2) * 10 * 4, 20, "p.97 DEF"); check(80 - 24 - 8 - 20, 28, "p.97 BDF")
f97 = FIG({"A": [40, 40], "B": [184, 40], "C": [280, 40], "D": [280, 136], "E": [280, 232], "F": [40, 232]},
          [poly(["A", "C", "E", "F"], "#ffffff"), poly(["B", "D", "F"], YELLOW), tick("B", "C"), tick("C", "D"), tick("D", "E"), lab("F", "E", "10 cm", 16)])
q93.append(Q("Exercise 7", 97, "In the figure, ACEF is a rectangle and BC = CD = DE. The area of rectangle ACEF is 80 cm². Find the area of the triangle BDF.",
             "First find the width CE. Then find the 3 white triangles and take them away from 80 cm².",
             ["The length FE is 10 cm. Width CE = 80 ÷ 10 = <b>8 cm</b>.",
              "CD = DE and CD + DE = 8, so CD = DE = 4 cm. BC = CD, so <b>BC = 4 cm</b>.",
              "AB = 10 - 4 = <b>6 cm</b>.",
              "White triangle ABF = ½ × 6 × 8 = <b>24 cm²</b>",
              "White triangle BCD = ½ × 4 × 4 = <b>8 cm²</b>",
              "White triangle DEF = ½ × 10 × 4 = <b>20 cm²</b>",
              "Triangle BDF = 80 - 24 - 8 - 20 = <b>28 cm²</b>"],
             "28 cm²", "80 cm² minus the white triangles (24 + 8 + 20 = 52 cm²) leaves 28 cm².", f97))
check(40 * 40, 1600, "p.98 PQUV"); check(25 * 25, 625, "p.98 QRST"); check(Fraction(1, 2) * 40 * 40, 800, "p.98 PUV")
check(Fraction(1, 2) * 65 * 25, 812.5, "p.98 PRS"); check(1600 + 625 - 800 - 812.5, 612.5, "p.98 Q8")
f98 = FIG({"P": [40, 40], "Q": [200, 40], "R": [300, 40], "S": [300, 140], "T": [200, 140], "U": [200, 200], "V": [40, 200]},
          [poly(["P", "Q", "U", "V"], "#ffffff"), poly(["Q", "R", "S", "T"], "#ffffff"),
           poly(["P", [200, 101.5], "U"], ORANGE), poly([[200, 101.5], "S", "T"], ORANGE),
           seg("P", "S"), seg("P", "U"), lab("P", "Q", "40 cm", -14), lab("Q", "R", "25 cm", -14)])
q93.append(Q("Exercise 8", 98, "Janice place 2 tiles next to each other to create a pattern. What is the area of the orange part?",
             "Add the 2 squares. Then take away the 2 white triangles.",
             ["Big square PQUV = 40 × 40 = <b>1,600 cm²</b>", "Small square QRST = 25 × 25 = <b>625 cm²</b>",
              "Both squares: 1,600 + 625 = <b>2,225 cm²</b>",
              "White triangle PUV = ½ × 40 × 40 = <b>800 cm²</b>",
              "White triangle PRS: base PR = 40 + 25 = 65 cm, height RS = 25 cm. Area = ½ × 65 × 25 = <b>812.5 cm²</b>",
              "White parts: 800 + 812.5 = <b>1,612.5 cm²</b>",
              "Orange part = 2,225 - 1,612.5 = <b>612.5 cm²</b>"],
             "612.5 cm²", "The 2 squares (2,225 cm²) minus the 2 white triangles (1,612.5 cm²).", f98))

flash93 = [
    {"front": "Perimeter unit", "back": "cm or m (a length)"},
    {"front": "Area unit", "back": "cm² or m² (square units)"},
    {"front": "1 m = ? cm", "back": "100 cm"},
    {"front": "2.5 m in cm", "back": "250 cm"},
    {"front": "Isosceles: perimeter 30 cm, base 10 cm. Each equal side?", "back": "(30 - 10) ÷ 2 = 10 cm"},
    {"front": "Shaded area method", "back": "Whole shape - white parts"},
    {"front": "Equilateral triangle side 15.5 m. Perimeter?", "back": "46.5 m"},
    {"front": "Square 6 m + triangle 12 m². Total?", "back": "36 + 12 = 48 m²"},
]
check(2.5 * 100, 250, "f"); check((30 - 10) / 2, 10, "f"); check(15.5 * 3, 46.5, "f")
match93 = [["1 m", "100 cm"], ["2.8 m", "280 cm"], ["0.5 m", "50 cm"], ["Area", "cm²"], ["Perimeter", "cm"],
           ["Isosceles, perimeter 96, odd side 34", "31 m each"], ["½ × 32 × 26", "416 cm²"], ["70 × 50", "3,500 cm²"]]
check(2.8 * 100, 280, "m"); check(0.5 * 100, 50, "m"); check(32 * 26 / 2, 416, "m"); check(70 * 50, 3500, "m")
quiz93 = [
    {"q": "Emma's triangular flag has base 30 cm and height 20 cm. Area?", "options": ["300 cm²", "600 cm²", "50 cm²", "100 cm²"]},
    {"q": "Sophie's triangle has sides 1.5 m, 1 m and 1 m. Perimeter in cm?", "options": ["350 cm", "3.5 cm", "35 cm", "150 cm"]},
    {"q": "An isosceles triangle has perimeter 40 cm and base 12 cm. Each equal side?", "options": ["14 cm", "28 cm", "26 cm", "12 cm"]},
    {"q": "Tom's equilateral garden has sides of 8.5 m. Perimeter?", "options": ["25.5 m", "17 m", "24.5 m", "72.25 m"]},
    {"q": "A rectangle 20 cm by 10 cm has a white triangle of 100 cm². Shaded area?", "options": ["100 cm²", "200 cm²", "300 cm²", "50 cm²"]},
    {"q": "James's triangle has perimeter 60 cm. Two sides are 25 cm and 20 cm. Third side?", "options": ["15 cm", "45 cm", "105 cm", "20 cm"]},
    {"q": "3.2 m = ? cm", "options": ["320 cm", "32 cm", "3,200 cm", "3.2 cm"]},
    {"q": "Lily's sign is a right triangle with sides 9 cm and 12 cm at the right angle. Area?", "options": ["54 cm²", "108 cm²", "21 cm²", "42 cm²"]},
    {"q": "Which answer needs cm²?", "options": ["Area of a tile", "Perimeter of a tile", "Length of a side", "An angle"]},
    {"q": "Two triangles of 750 cm² and 1,462.5 cm². Total area?", "options": ["2,212.5 cm²", "2,112.5 cm²", "712.5 cm²", "2,250 cm²"]},
]
check(30 * 20 / 2, 300, "q"); check((1.5 + 1 + 1) * 100, 350, "q"); check((40 - 12) / 2, 14, "q"); check(8.5 * 3, 25.5, "q")
check(200 - 100, 100, "q"); check(60 - 45, 15, "q"); check(3.2 * 100, 320, "q"); check(9 * 12 / 2, 54, "q"); check(750 + 1462.5, 2212.5, "q")
sections.append({"id": "9-3", "title": "Word Problems", "short": "3. Word Problems", "pages": "p.89 to 98",
                 "learn": learn93, "questions": q93, "flash": flash93, "match": match93, "quiz": quiz93})

# ==================================================================
# UNIT 9 CHALLENGE (p.99 to 104)
# ==================================================================
check(8 * 8, 64, "p.99 B"); check(Fraction(1, 4) * 64, 16, "p.99 D"); check(64 + 16, 80, "p.99 C")
check(8 - 6, 2, "p.101 small"); check(2 * 2, 4, "p.101 small area"); check(4 * Fraction(1, 2) * 6 * 8, 96, "p.101 triangles"); check(4 + 96, 100, "p.101 big")
check(10 * 10, 100, "p.101 side")
f99 = FIG({"_a": [40, 40], "_b": [120, 40], "_c": [40, 120], "_t": [160, 40], "_r": [240, 120], "_btm": [160, 200], "_l": [80, 120]},
          [poly(["_a", "_b", "_l", "_c"], PURPLE), poly(["_t", "_r", "_btm", "_l"], YELLOW), lab("_t", "_r", "8 cm", -14), lab("_r", "_btm", "8 cm", -14),
           txt(70, 75, "D", 18, "#1f2a44")], names=False)
f101 = FIG({"_A": [40, 40], "_B": [200, 40], "_C": [200, 200], "_D": [40, 200]},
           [poly(["_A", "_B", "_C", "_D"], ORANGE), seg("_A", [136, 136]), seg("_B", [104, 136]), seg("_C", [104, 104]), seg("_D", [136, 104]),
            poly([[104, 104], [136, 104], [136, 136], [104, 136]], "#ffffff")], names=False)
f103 = FIG({"A": [40, 40], "E": [210, 40], "B": [250, 40], "C": [250, 180], "D": [40, 180]},
           [poly(["A", "B", "C", "D"], "#ffffff"), poly(["E", "B", "D"], BLUE)])
qch = [
    Q("Let's Think Along", 99, "Ravi is given 2 squares, A and B. He covers ½ of the small square with the big square as shown to make Figure C. Find the area of Figure C.",
      "Draw the 2 diagonals of the big square. It splits into 4 identical triangles. The uncovered part D is one of them.",
      ["Area of square B = 8 × 8 = <b>64 cm²</b>",
       "The 2 diagonals of square B cut it into 4 identical triangles. The uncovered part D is the same size as one of them.",
       "Area of triangle D = ¼ of 64 = 64 ÷ 4 = <b>16 cm²</b>",
       "Area of Figure C = 64 + 16 = <b>80 cm²</b>"],
      "80 cm²", "Figure C is the big square plus the uncovered triangle D.", f99),
    Q("Problem Solving", 101, "Figure A is a right triangle with base 6 cm and height 8 cm. 4 of these right triangles are arranged and pasted on a piece of paper to form Figure B as shown below. What is the length of each side of the big square in Figure B?",
      "Find the small square in the middle first. Then add up all the pieces to get the big square's area.",
      ["The small square in the middle has side 8 - 6 = <b>2 cm</b>. Its area = 2 × 2 = <b>4 cm²</b>",
       "Each right triangle = ½ × 6 × 8 = 24 cm². 4 triangles = 4 × 24 = <b>96 cm²</b>",
       "Area of big square = 4 + 96 = <b>100 cm²</b>",
       "Which number times itself makes 100? 10 × 10 = 100. So each side is <b>10 cm</b>.",
       "<b>Check:</b> 10 × 10 = 100 and 100 - 96 = 4 = 2 × 2 ✓"],
      "10 cm", "The big square is 4 triangles (96 cm²) and the small square (4 cm²): 100 cm² = 10 cm × 10 cm.", f101),
    Q("Math Journal", 103, "In the figure, ABCD is a rectangle and EBD is a triangle. Describe two methods to find the area of the shaded triangle.",
      "One method uses taking away. The other uses the triangle formula.",
      ["<b>Method 1:</b> Find the area of rectangle ABCD. Then subtract the areas of triangles AED and BCD.",
       "<b>Method 2:</b> Use area of triangle = ½ × base × height.",
       "The base is <b>BE</b>. The height is <b>AD</b> (it meets the line AB at a right angle).",
       "Area of triangle EBD = ½ × BE × AD"],
      "Method 1: rectangle ABCD - triangle AED - triangle BCD. Method 2: ½ × BE × AD",
      "Both methods give the same area.", f103),
]
sections.append({"id": "9-ch", "title": "Unit 9 Challenge", "short": "⭐ Challenge", "pages": "p.99 to 104",
                 "learn": [
                     L("Idea", "Unit 9 big ideas", "<p><b>Perimeter</b> = add all 3 sides (cm, m).</p><p><b>Area</b> = ½ × base × height (cm², m²).</p>"
                       "<p>The height meets the base at a right angle. It can be outside the triangle.</p>", None, 104),
                     L("Idea", "Square numbers help", "<p>If a square has area 100 cm², its side is the number that times itself makes 100: 10 × 10 = 100, so 10 cm.</p>", None, 101),
                     L("Example", "Math in Real Life (p.104)", "<p>A right triangle has sides 3 cm and 4 cm at the right angle. The long side is 5 cm, because 3 × 3 + 4 × 4 = 9 + 16 = 25 = 5 × 5.</p>"
                       "<p>Perimeter = 3 + 4 + 5 = <b>12 cm</b>. Area = ½ × 3 × 4 = <b>6 cm²</b>.</p>", None, 104),
                 ],
                 "questions": qch, "flash": flash91[:4] + flash92[:5] + flash93[:3],
                 "match": [["Perimeter", "Add the 3 sides"], ["Area", "½ × base × height"], ["Area unit", "cm²"], ["Length unit", "cm"],
                           ["Square 8 cm", "64 cm²"], ["¼ of 64", "16"], ["10 × 10", "100"], ["Base 6, height 8", "24 cm²"]],
                 "quiz": quiz91[:4] + quiz92[:4] + quiz93[:2] + [
                     {"q": "A square has an area of 100 cm². Each side is…", "options": ["10 cm", "25 cm", "50 cm", "100 cm"]},
                     {"q": "Square 8 cm by 8 cm. ¼ of its area?", "options": ["16 cm²", "64 cm²", "32 cm²", "2 cm²"]}]})
check(3 + 4 + 5, 12, "p.104"); check(3 * 4 / 2, 6, "p.104"); check(9 + 16, 25, "p.104")

unit = {"unit": "09", "title": "Perimeter and Area of Triangles", "pages": "p.71 to 104", "sections": sections,
        "expectedPages": {"9-1": [74, 75, 76, 77], "9-2": [82, 83, 84, 85, 86, 87, 88], "9-3": [93, 94, 95, 96, 97, 98], "9-ch": [99, 101, 103]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written. Add these to content/CHECK-ME.md:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit09.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit09.json ({n} guided questions, {len(sections)} sections).")
