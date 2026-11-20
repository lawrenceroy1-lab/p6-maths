"""Builds content/unit07.json for Unit 7: 2D Shapes (book pages 1 to 46).

Every number that ends up in an answer is calculated here and compared with the
answer key value using check(). The build stops if anything disagrees.
Run:  python3 tools/build_unit07.py
"""
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, fmt, apex, polar, lerp, foot, PROBLEMS  # noqa: E402

DEG = "°"
ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"


def Q(label, page, q, hint, steps, answer, why, fig=None):
    return {"label": label, "page": page, "q": q, "fig": fig, "hint": hint,
            "steps": steps, "answer": answer, "why": why}


def L(tag, title, html, fig=None, page=None):
    return {"tag": tag, "title": title, "html": html, "fig": fig, "page": page}


def F(w, h, pts, items):
    return {"w": w, "h": h, "pts": pts, "items": items}


def deg(n):
    return f"{fmt(n)}{DEG}"


# ------------------------------------------------------------------
# Reusable small triangle figure: names at corners, optional angles
# ------------------------------------------------------------------
def triangle(names, P, fill, extra=(), w=320, h=230, label_off=None):
    pts = dict(zip(names, P))
    items = [{"t": "poly", "p": list(names), "fill": fill}]
    items += list(extra)
    cx = sum(p[0] for p in P) / 3
    cy = sum(p[1] for p in P) / 3
    for n, p in zip(names, P):
        if label_off and n in label_off:
            d = label_off[n]
        else:
            dx, dy = p[0] - cx, p[1] - cy
            L_ = (dx * dx + dy * dy) ** 0.5 or 1
            d = [round(dx / L_ * 18, 1), round(dy / L_ * 18 + 7, 1)]
        if n and not n.startswith("_"):
            items.append({"t": "pl", "p": n, "d": d})
    return F(w, h, pts, items)


sections = []

# ==================================================================
# 7.1 TYPES OF TRIANGLES  (p.2 to 12)
# ==================================================================
A1, B1, C1 = [170, 30], [50, 190], [270, 190]
D1 = foot(A1, B1, C1)
fig_parts = F(320, 230, {"A": A1, "B": B1, "C": C1, "D": D1}, [
    {"t": "poly", "p": ["A", "B", "C"], "fill": BLUE},
    {"t": "seg", "p": ["A", "D"], "dash": True},
    {"t": "ra", "v": "D", "a": "A", "b": "C"},
    {"t": "ang", "v": "A", "a": "B", "b": "C", "s": "vertex angle", "r": 24, "lr": 4, "size": 13},
    {"t": "ang", "v": "B", "a": "A", "b": "C", "r": 22},
    {"t": "ang", "v": "C", "a": "A", "b": "B", "r": 22},
    {"t": "txt", "at": [235, 218], "s": "base", "size": 15, "color": "#1565c0"},
    {"t": "txt", "at": [195, 130], "s": "height", "size": 14, "color": "#1565c0"},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [-14, 8]},
    {"t": "pl", "p": "C", "d": [14, 8]}, {"t": "pl", "p": "D", "d": [0, 26]},
])

eq_fig = triangle("ABC", [[160, 25], [60, 198], [260, 198]], BLUE, [
    {"t": "tick", "p": ["A", "B"]}, {"t": "tick", "p": ["B", "C"]}, {"t": "tick", "p": ["A", "C"]},
    {"t": "len", "p": ["B", "A"], "s": "3.5 cm"}, {"t": "len", "p": ["A", "C"], "s": "3.5 cm"},
    {"t": "len", "p": ["C", "B"], "s": "3.5 cm"},
    {"t": "ang", "v": "A", "a": "B", "b": "C", "s": "60°"},
    {"t": "ang", "v": "B", "a": "C", "b": "A", "s": "60°"},
    {"t": "ang", "v": "C", "a": "A", "b": "B", "s": "60°"},
])

iso_fig = triangle("PQR", [[160, 20], [230, 205], [90, 205]], PINK, [
    {"t": "tick", "p": ["P", "Q"], "n": 2}, {"t": "tick", "p": ["P", "R"], "n": 2},
    {"t": "len", "p": ["P", "Q"], "s": "3.5 cm"}, {"t": "len", "p": ["R", "P"], "s": "3.5 cm"},
    {"t": "len", "p": ["Q", "R"], "s": "2.5 cm"},
    {"t": "ang", "v": "Q", "a": "P", "b": "R", "r": 22, "color": "#2e7d32"},
    {"t": "ang", "v": "R", "a": "Q", "b": "P", "r": 22, "color": "#2e7d32"},
])

scal_fig = F(320, 230, {"P": [110, 40], "Q": [50, 190], "R": [280, 190]}, [
    {"t": "poly", "p": ["P", "Q", "R"], "fill": GREEN},
    {"t": "len", "p": ["Q", "P"], "s": "2 cm"},
    {"t": "len", "p": ["P", "R"], "s": "3 cm"},
    {"t": "len", "p": ["R", "Q"], "s": "4 cm"},
])


def right_fig(a_deg):
    Y, Z = [70, 200], [270, 200]
    X = apex(Y, Z, 90, 90 - a_deg)  # angle at X will be a_deg
    return triangle("XYZ", [X, Y, Z], YELLOW, [
        {"t": "ra", "v": "Y", "a": "X", "b": "Z"},
        {"t": "ang", "v": "X", "a": "Y", "b": "Z", "s": deg(a_deg), "r": 26},
        {"t": "ang", "v": "Z", "a": "X", "b": "Y", "s": deg(90 - a_deg), "r": 30, "lr": 22},
    ])


def angles_fig(names, angs, fill, w=320, h=230, base=None, up=True):
    """Triangle drawn from its 3 angles: names[1]-names[2] is the base."""
    B, C = base or ([50, 190], [270, 190])
    A = apex(B, C, angs[1], angs[2], up)
    extra = []
    P = [A, B, C]
    for k in range(3):
        v = names[k]
        a, b = [names[j] for j in range(3) if j != k]
        extra.append({"t": "ang", "v": v, "a": a, "b": b, "s": deg(angs[k]), "r": 24})
    return triangle(names, P, fill, extra, w, h)


acute_ex = angles_fig("ABC", [60, 70, 50], GREEN)
obtuse_ex = angles_fig("DEF", [120, 30, 30], ORANGE)
check(60 + 70 + 50, 180, "Learn 7.1 acute example")
check(120 + 30 + 30, 180, "Learn 7.1 obtuse example")
check(90 + 45 + 45, 180, "Learn 7.1 right isosceles example")

learn71 = [
    L("Idea", "Parts of a triangle",
      "<p>The <b>base</b> is the side at the bottom. The <b>vertex angle</b> is the angle opposite the base. "
      "The 2 angles on the base are the <b>base angles</b>. The <b>height</b> is a line from the vertex that meets the base at a right angle (90°).</p>",
      fig_parts, 2),
    L("Example", "Name the parts of triangle ABC",
      "<p>Base: <b>BC</b><br>Vertex angle: <b>∠BAC</b><br>Base angles: <b>∠ABC</b> and <b>∠BCA</b><br>"
      "Sides next to the vertex angle: <b>BA</b> and <b>CA</b><br>Height: <b>AD</b></p>", fig_parts, 2),
    L("Idea", "Equilateral triangle",
      "<p>An <b>equilateral triangle</b> has <b>3 equal sides</b> and <b>3 equal angles</b>.</p>"
      "<p>Each angle is <b>60°</b>. The little tick marks show which sides are equal.</p>", None, 3),
    L("Example", "Is this triangle equilateral?",
      "<p>All 3 sides are 3.5 cm. So AB = BC = AC.</p><p>Yes! It is an equilateral triangle, and every angle is 60°.</p>", eq_fig, 3),
    L("Idea", "Isosceles triangle",
      "<p>An <b>isosceles triangle</b> has <b>2 equal sides</b> and <b>2 equal angles</b>.</p>"
      "<p>The 2 equal angles are opposite the 2 equal sides.</p>", None, 4),
    L("Example", "Find the equal angles",
      "<p>PQ = PR = 3.5 cm. These are the 2 equal sides.</p><p>So the angles opposite them are equal: <b>∠PQR = ∠PRQ</b> (the green arcs).</p>", iso_fig, 4),
    L("Idea", "Scalene triangle",
      "<p>A <b>scalene triangle</b> has <b>3 different sides</b> and <b>3 different angles</b>.</p>", None, 5),
    L("Example", "Is this triangle scalene?",
      "<p>The sides are 2 cm, 3 cm and 4 cm. No two sides are the same.</p><p>Yes! It is a scalene triangle.</p>", scal_fig, 5),
    L("Idea", "Right triangle",
      "<p>A <b>right triangle</b> has <b>1 right angle</b> (90°). The small square shows the right angle.</p>"
      "<p>The other 2 angles always add up to <b>90°</b>.</p>", None, 5),
    L("Example", "The other 2 angles",
      "<p>∠XYZ = 90°. ∠X = 35° and ∠Z = 55°.</p><p>35° + 55° = <b>90°</b>. They add up to 90°, just like the rule says.</p>", right_fig(35), 5),
    L("Idea", "Acute triangle",
      "<p>An <b>acute angle</b> is less than 90°.</p><p>In an <b>acute triangle</b>, <b>all 3 angles</b> are acute.</p>", None, 6),
    L("Example", "Is this an acute triangle?",
      "<p>The angles are 60°, 70° and 50°. Each one is less than 90°.</p><p>Yes! It is an acute triangle.</p>", acute_ex, 6),
    L("Idea", "Obtuse triangle",
      "<p>An <b>obtuse angle</b> is more than 90° but less than 180°.</p><p>An <b>obtuse triangle</b> has <b>1 obtuse angle</b>. "
      "An obtuse triangle can also be isosceles.</p>", None, 6),
    L("Example", "Is this an obtuse triangle?",
      "<p>The angles are 120°, 30° and 30°. 120° is more than 90°.</p><p>Yes! It is an obtuse triangle. It also has 2 equal angles, so it is isosceles too.</p>", obtuse_ex, 6),
    L("Idea", "One triangle, two names",
      "<p>Look at the <b>sides</b>: equilateral, isosceles or scalene.</p><p>Look at the <b>angles</b>: acute, right or obtuse.</p>"
      "<p>So one triangle can have two names. Every equilateral triangle is also acute (60°, 60°, 60°).</p>", None, 7),
    L("Example", "A right isosceles triangle",
      "<p>Angles: 90°, 45° and 45°. It has a right angle, so it is a <b>right triangle</b>.</p>"
      "<p>It has 2 equal angles, so it is also an <b>isosceles triangle</b>.</p>",
      angles_fig("JKL", [90, 45, 45], PURPLE), 7),
]

# ---- Guided answers 7.1 ----
q71 = []
# Do and Learn p.8 Q1
fa = triangle("PQR", [[60, 40], [260, 40], [160, 213]], ORANGE, [
    {"t": "tick", "p": ["P", "Q"]}, {"t": "tick", "p": ["Q", "R"]}, {"t": "tick", "p": ["P", "R"]},
    {"t": "ang", "v": "P", "a": "Q", "b": "R", "s": "p", "r": 22},
    {"t": "ang", "v": "Q", "a": "P", "b": "R", "s": "q", "r": 22},
    {"t": "ang", "v": "R", "a": "P", "b": "Q", "s": "r", "r": 22},
])
check(180 / 3, 60, "p.8 Q1(a)")
q71.append(Q("Do and Learn 1 (a)", 8,
             "Fill in the blanks.<br>PQ = ___ = ___<br>∠p = ∠q = ∠___ = ___°",
             "Look at the tick marks. How many sides are equal?",
             ["Each side of the triangle has 1 tick mark. Same tick marks mean the sides are equal.",
              "So all 3 sides are equal: <b>PQ = PR = QR</b>. This is an equilateral triangle.",
              "An equilateral triangle has 3 equal angles. All the angles add up to 180°.",
              "180° ÷ 3 = <b>60°</b>. So ∠p = ∠q = ∠r = 60°."],
             "PQ = PR = QR, ∠p = ∠q = ∠r = 60°",
             "All 3 sides have the same tick mark, so the triangle is equilateral, and each angle is 60°.", fa))

fb = triangle("EFG", [[110, 50], [290, 80], [40, 200]], GREEN, [
    {"t": "tick", "p": ["E", "F"], "n": 2}, {"t": "tick", "p": ["E", "G"], "n": 2},
    {"t": "ang", "v": "E", "a": "F", "b": "G", "s": "e", "r": 22},
    {"t": "ang", "v": "F", "a": "E", "b": "G", "s": "f", "r": 34, "lr": 12},
    {"t": "ang", "v": "G", "a": "E", "b": "F", "s": "g", "r": 30, "lr": 12},
])
q71.append(Q("Do and Learn 1 (b)", 8,
             "Fill in the blanks.<br>∠g = ∠___<br>EG = ___",
             "Find the 2 sides with the same tick marks.",
             ["EG and EF both have 2 tick marks. So <b>EG = EF</b>. This is an isosceles triangle.",
              "In an isosceles triangle, the 2 angles opposite the equal sides are equal.",
              "∠g is opposite side EF. ∠f is opposite side EG.",
              "So <b>∠g = ∠f</b>."],
             "∠g = ∠f, EG = EF",
             "The angles opposite the 2 equal sides of an isosceles triangle are equal.", fb))

fc = triangle("UVW", [[240, 25], [240, 200], [60, 200]], YELLOW, [
    {"t": "ra", "v": "V", "a": "U", "b": "W"},
    {"t": "ang", "v": "U", "a": "V", "b": "W", "s": "u", "r": 24},
    {"t": "ang", "v": "W", "a": "U", "b": "V", "s": "w", "r": 34, "lr": 12},
    {"t": "txt", "at": [222, 190], "s": "v", "size": 16, "color": "#c2185b", "bold": True},
])
check(180 - 90, 90, "p.8 Q1(c)")
q71.append(Q("Do and Learn 1 (c)", 8,
             "Fill in the blanks.<br>∠v = ___°<br>∠u + ∠w = ___°",
             "The small square means a right angle.",
             ["∠v has a small square. A small square means a right angle, so <b>∠v = 90°</b>.",
              "All 3 angles of a triangle add up to 180°.",
              "∠u + ∠w = 180° - 90° = <b>90°</b>."],
             "∠v = 90°, ∠u + ∠w = 90°",
             "In a right triangle, the other 2 angles add up to 90°.", fc))

f2a = angles_fig("TSU", [47, 53, 80], PURPLE)
check(47 + 53 + 80, 180, "p.8 Q2(a) angle sum")
q71.append(Q("Do and Learn 2 (a)", 8, "Name the type of triangle.",
             "Is any angle 90° or bigger?",
             ["The angles are 47°, 53° and 80°.",
              "47° is less than 90°. 53° is less than 90°. 80° is less than 90°.",
              "All 3 angles are acute, so it is an <b>acute triangle</b>."],
             "acute triangle", "All 3 angles are less than 90°.", f2a))

f2b = angles_fig("YXZ", [115, 40, 25], ORANGE)
check(115 + 40 + 25, 180, "p.8 Q2(b) angle sum")
q71.append(Q("Do and Learn 2 (b)", 8, "Name the type of triangle.",
             "Is any angle bigger than 90°?",
             ["The angles are 40°, 115° and 25°.",
              "115° is more than 90° and less than 180°. So 115° is an obtuse angle.",
              "A triangle with 1 obtuse angle is an <b>obtuse triangle</b>."],
             "obtuse triangle", "∠XYZ = 115° is an obtuse angle.", f2b))

# Exercise p.9 Q1
A9, C9, B9 = [55, 30], [55, 190], [290, 190]
e9a = triangle("ACB", [A9, C9, B9], ORANGE, [{"t": "ra", "v": "C", "a": "A", "b": "B"},
                                             {"t": "ang", "v": "A", "a": "C", "b": "B", "r": 22},
                                             {"t": "ang", "v": "B", "a": "A", "b": "C", "r": 30}])
q71.append(Q("Exercise 1 (a)", 9,
             "Fill in the blanks.<br>Given that CB is the base of triangle ABC.<br>Vertex angle: ___<br>Base angles: ___ and ___<br>"
             "Sides adjacent to vertex angle: ___ and ___<br>Height: ___",
             "The vertex angle is at the corner that is NOT on the base.",
             ["The base is CB. The corner not on the base is <b>A</b>. So the vertex angle is <b>∠CAB</b>.",
              "The base angles are the 2 angles on the base CB: <b>∠ACB</b> and <b>∠CBA</b>.",
              "The sides that touch the vertex angle at A are <b>CA</b> and <b>BA</b>.",
              "The height goes from A down to the base at a right angle. ∠ACB is already a right angle, so the height is <b>AC</b>."],
             "Vertex angle: ∠CAB; Base angles: ∠ACB and ∠CBA; Sides: CA and BA; Height: AC",
             "AC meets the base CB at a right angle, so AC is the height.", e9a))

S9, U9, T9 = [190, 30], [40, 200], [280, 200]
V9 = [190, 200]
e9b = F(320, 235, {"S": S9, "U": U9, "T": T9, "V": V9}, [
    {"t": "poly", "p": ["S", "U", "T"], "fill": YELLOW},
    {"t": "seg", "p": ["S", "V"], "dash": True}, {"t": "ra", "v": "V", "a": "S", "b": "T"},
    {"t": "ang", "v": "S", "a": "U", "b": "T", "r": 20},
    {"t": "pl", "p": "S", "d": [0, -8]}, {"t": "pl", "p": "U", "d": [-14, 8]},
    {"t": "pl", "p": "T", "d": [14, 8]}, {"t": "pl", "p": "V", "d": [0, 26]}])
q71.append(Q("Exercise 1 (b)", 9,
             "Fill in the blanks.<br>Given that UT is the base of triangle STU.<br>Vertex angle: ___<br>Base angles: ___ and ___<br>"
             "Sides adjacent to vertex angle: ___ and ___<br>Height: ___",
             "Find the corner that is not on UT.",
             ["The base is UT. The corner not on the base is <b>S</b>. So the vertex angle is <b>∠UST</b>.",
              "The base angles are on the base UT: <b>∠SUT</b> and <b>∠UTS</b>.",
              "The sides that touch the vertex angle at S are <b>US</b> and <b>TS</b>.",
              "SV goes from S to the base and makes a right angle. So the height is <b>SV</b>."],
             "Vertex angle: ∠UST; Base angles: ∠SUT and ∠UTS; Sides: US and TS; Height: SV",
             "SV is drawn from the vertex S and is perpendicular to the base UT.", e9b))

I9, L9, K9 = [270, 30], [40, 190], [205, 190]
J9 = [270, 190]
e9c = F(320, 230, {"I": I9, "L": L9, "K": K9, "J": J9}, [
    {"t": "poly", "p": ["I", "L", "K"], "fill": PURPLE},
    {"t": "seg", "p": ["K", "J"], "dash": True}, {"t": "seg", "p": ["I", "J"], "dash": True},
    {"t": "ra", "v": "J", "a": "I", "b": "K"},
    {"t": "ang", "v": "I", "a": "L", "b": "K", "r": 30},
    {"t": "pl", "p": "I", "d": [8, -6]}, {"t": "pl", "p": "L", "d": [-14, 8]},
    {"t": "pl", "p": "K", "d": [0, 26]}, {"t": "pl", "p": "J", "d": [12, 24]}])
q71.append(Q("Exercise 1 (c)", 9,
             "Fill in the blanks.<br>Given that LK is the base of triangle IKL.<br>Vertex angle: ___<br>Base angles: ___ and ___<br>"
             "Sides adjacent to vertex angle: ___ and ___<br>Height: ___",
             "The height can be outside the triangle. Look for the dotted line with a right angle.",
             ["The base is LK. The corner not on the base is <b>I</b>. So the vertex angle is <b>∠LIK</b>.",
              "The base angles are on the base LK: <b>∠ILK</b> and <b>∠LKI</b>.",
              "The sides that touch the vertex angle at I are <b>LI</b> and <b>KI</b>.",
              "The base LK is made longer (dotted line) to J. IJ meets it at a right angle. So the height is <b>IJ</b>."],
             "Vertex angle: ∠LIK; Base angles: ∠ILK and ∠LKI; Sides: LI and KI; Height: IJ",
             "For an obtuse triangle, the height can fall outside. IJ is perpendicular to the base line.", e9c))

# Exercise p.10 Q2 (8 triangles)
g = {}
it = []


def add(name, P, fill, extras, lab):
    keys = [f"{name}{k}" for k in range(3)]
    for k, p in zip(keys, P):
        g[k] = p
    it.append({"t": "poly", "p": keys, "fill": fill})
    for e in extras:
        e2 = dict(e)
        for f_ in ("v", "a", "b"):
            if f_ in e2:
                e2[f_] = f"{name}{e2[f_]}"
        if "p" in e2 and isinstance(e2["p"], list):
            e2["p"] = [f"{name}{x}" for x in e2["p"]]
        it.append(e2)
    it.append({"t": "txt", "at": lab, "s": name, "size": 18, "bold": True})


add("A", [[30, 20], [100, 25], [25, 120]], YELLOW, [{"t": "ra", "v": 0, "a": 1, "b": 2, "size": 9}], [50, 55])
add("B", [[110, 90], [230, 50], [270, 130]], PURPLE, [{"t": "tick", "p": [0, 1]}, {"t": "tick", "p": [1, 2]}], [205, 95])
add("C", [[335, 20], [370, 30], [300, 170]], PINK, [{"t": "len", "p": [0, 1], "s": "6 cm", "off": -12, "size": 13},
                                                   {"t": "len", "p": [2, 0], "s": "15 cm", "off": -18, "size": 13},
                                                   {"t": "len", "p": [1, 2], "s": "15 cm", "off": -22, "size": 13}], [335, 85])
add("D", [[30, 180], [110, 210], [40, 255]], BLUE, [{"t": "ang", "v": 0, "a": 1, "b": 2, "s": "60°", "r": 14, "size": 12, "lr": 12},
                                                   {"t": "ang", "v": 1, "a": 0, "b": 2, "s": "60°", "r": 14, "size": 12, "lr": 14},
                                                   {"t": "ang", "v": 2, "a": 0, "b": 1, "s": "60°", "r": 14, "size": 12, "lr": 12}], [60, 220])
add("E", [[150, 160], [200, 235], [160, 280]], ORANGE, [{"t": "ra", "v": 1, "a": 0, "b": 2, "size": 9}], [168, 230])
add("F", [[255, 210], [350, 180], [330, 280]], GREEN, [{"t": "tick", "p": [0, 1]}, {"t": "tick", "p": [1, 2]}, {"t": "tick", "p": [2, 0]}], [315, 230])
add("G", [[80, 280], [50, 335], [80, 395]], PINK, [{"t": "ang", "v": 0, "a": 1, "b": 2, "s": "30°", "r": 18, "size": 12, "lr": 10},
                                                  {"t": "ang", "v": 1, "a": 0, "b": 2, "s": "120°", "r": 10, "size": 12, "lr": 18},
                                                  {"t": "ang", "v": 2, "a": 0, "b": 1, "s": "30°", "r": 18, "size": 12, "lr": 10}], [70, 350])
add("H", [[140, 360], [250, 320], [235, 380]], PURPLE, [{"t": "ra", "v": 2, "a": 0, "b": 1, "size": 9},
                                                       {"t": "len", "p": [0, 1], "s": "10 cm", "off": 14, "size": 13},
                                                       {"t": "len", "p": [1, 2], "s": "6 cm", "off": 22, "size": 13},
                                                       {"t": "len", "p": [2, 0], "s": "8 cm", "off": 16, "size": 13}], [205, 360])
for e in it:
    for f_ in ("v", "a", "b"):
        pass
fig10 = F(400, 410, g, it)
check(60 + 60 + 60, 180, "p.10 D")
check(30 + 120 + 30, 180, "p.10 G")
check(6 * 6 + 8 * 8, 10 * 10, "p.10 H is a right triangle (6, 8, 10)")
q71.append(Q("Exercise 2", 10,
             "Group the triangles and write the letters in the table correctly.<br>"
             "<table class='t'><tr><th>Equilateral triangle</th><th>Isosceles triangle</th><th>Right triangle</th></tr><tr><td>?</td><td>?</td><td>?</td></tr></table>",
             "Look for clues: tick marks (equal sides), equal lengths, 60° angles, and small squares (right angles).",
             ["<b>Equilateral</b> (3 equal sides or three 60° angles): D has three 60° angles. F has a tick mark on all 3 sides. So <b>D and F</b>.",
              "<b>Isosceles</b> (2 equal sides or 2 equal angles): B has 2 sides with tick marks. C has two sides of 15 cm. G has two angles of 30°. So <b>B, C and G</b>.",
              "<b>Right</b> (a small square): A, E and H each have a small square. So <b>A, E and H</b>."],
             "Equilateral: D, F · Isosceles: B, C, G · Right: A, E, H",
             "Tick marks and equal numbers show equal sides or angles. A small square shows a right angle.", fig10))

# Exercise p.11 Q3 (owl figure)
owl = {
    "a1": [120, 82], "a2": [345, 82], "a3": [232, 155],
    "b1": [15, 15], "b2": [105, 120], "c1": [450, 15], "c2": [360, 120],
    "d1": [95, 130], "d2": [95, 365], "d3": [232, 365],
    "e1": [370, 130], "e2": [370, 365],
    "k1": [155, 230], "k2": [310, 230],
    "f1": [142, 142], "f2": [160, 190], "f3": [202, 192],
    "g1": [322, 142], "g2": [304, 190], "g3": [262, 192],
    "h1": [212, 155], "h2": [254, 155], "h3": [232, 228],
    "w1": [110, 100], "w2": [355, 100], "w3": [355, 230], "w4": [110, 230],
}
owl_items = [
    {"t": "poly", "p": ["w1", "w2", "w3", "w4"], "fill": GREEN},
    {"t": "poly", "p": ["a1", "a2", "a3"], "fill": YELLOW},
    {"t": "poly", "p": ["b1", "b2", "a3"], "fill": PINK},
    {"t": "poly", "p": ["c1", "c2", "a3"], "fill": PINK},
    {"t": "poly", "p": ["d1", "d2", "d3"], "fill": ORANGE},
    {"t": "poly", "p": ["e1", "e2", "d3"], "fill": BLUE},
    {"t": "poly", "p": ["k1", "k2", "d3"], "fill": GREEN},
    {"t": "poly", "p": ["f1", "f2", "f3"], "fill": PURPLE},
    {"t": "poly", "p": ["g1", "g2", "g3"], "fill": PURPLE},
    {"t": "poly", "p": ["h1", "h2", "h3"], "fill": PURPLE},
    {"t": "ra", "v": "d2", "a": "d1", "b": "d3", "size": 10},
    {"t": "ra", "v": "e2", "a": "e1", "b": "d3", "size": 10},
]
for nm, at in [("A", [232, 115]), ("B", [100, 95]), ("C", [365, 95]), ("D", [140, 300]), ("E", [325, 300]),
               ("F", [168, 180]), ("G", [296, 180]), ("H", [232, 185]), ("K", [232, 290])]:
    owl_items.append({"t": "txt", "at": at, "s": nm, "size": 20, "bold": True})
fig11 = F(465, 380, owl, owl_items)
q71.append(Q("Exercise 3 (a)", 11,
             "Identify the triangles in the figure and write the letters in the table below.<br>"
             "<table class='t'><tr><th>Equilateral triangle</th><td>?</td></tr><tr><th>Isosceles triangle</th><td>?</td></tr><tr><th>Right triangle</th><td>?</td></tr></table>",
             "First find the triangles with a right angle (small square). Then look at the shape of each of the others.",
             ["The small squares are in D and E. So the <b>right triangles are D and E</b>.",
              "K has 3 sides that are the same length. So <b>K is equilateral</b>.",
              "A, B, C, F, H and G each have 2 sides that are the same length. So the <b>isosceles triangles are A, B, C, F, H and G</b>."],
             "Equilateral: K · Isosceles: A, B, C, F, H, G · Right: D, E",
             "Right triangles have a right angle, an equilateral triangle has 3 equal sides, and an isosceles triangle has 2 equal sides.", fig11))
q71.append(Q("Exercise 3 (b)", 11,
             "Identify the triangles in the figure and write the letters in the table below.<br>"
             "<table class='t'><tr><th>Acute triangle</th><td>?</td></tr><tr><th>Obtuse triangle</th><td>?</td></tr></table>",
             "An obtuse triangle has one wide angle (more than 90°). D and E have right angles, so they go in neither row.",
             ["D and E have a right angle, so they are not acute and not obtuse.",
              "K is equilateral (60°, 60°, 60°). H has 3 small, sharp angles. So the <b>acute triangles are K and H</b>.",
              "A, B, C, F and G each have one wide angle bigger than 90°. So the <b>obtuse triangles are A, B, C, F and G</b>."],
             "Acute: K, H · Obtuse: A, B, C, F, G",
             "In an acute triangle all angles are less than 90°. An obtuse triangle has 1 angle more than 90°.", fig11))

# Exercise p.12 Q4
sq = F(260, 170, {"a": [40, 20], "b": [190, 20], "c": [190, 150], "d": [40, 150]}, [
    {"t": "poly", "p": ["a", "b", "c", "d"], "fill": BLUE}, {"t": "seg", "p": ["a", "c"]},
    {"t": "ra", "v": "b", "a": "a", "b": "c", "size": 10}, {"t": "ra", "v": "d", "a": "a", "b": "c", "size": 10}])
q71.append(Q("Exercise 4 (a)", 12,
             "Put a tick (✓) in the box for each correct statement.<br>The square below is divided into halves.<br>There are:<br>"
             "• 2 equilateral triangles<br>• 2 isosceles triangles<br>• 2 right triangles",
             "A square has 4 equal sides and 4 right angles.",
             ["Each half has 2 sides of the square. The sides of a square are equal, so each half has <b>2 equal sides</b>. ✓ isosceles.",
              "Each half has 1 corner of the square. A square's corner is a right angle. ✓ right triangle.",
              "The long side (the cut) is longer than the square's sides, so the 3 sides are not all equal. ✗ equilateral."],
             "✓ 2 isosceles triangles, ✓ 2 right triangles (✗ 2 equilateral triangles)",
             "Each half has 2 equal sides and a right angle, but not 3 equal sides.", sq))
rect = F(260, 170, {"a": [20, 35], "b": [230, 35], "c": [230, 140], "d": [20, 140]}, [
    {"t": "poly", "p": ["a", "b", "c", "d"], "fill": ORANGE}, {"t": "seg", "p": ["d", "b"]},
    {"t": "ra", "v": "a", "a": "b", "b": "d", "size": 10}, {"t": "ra", "v": "c", "a": "b", "b": "d", "size": 10}])
q71.append(Q("Exercise 4 (b)", 12,
             "Put a tick (✓) in the box for each correct statement.<br>The rectangle below is divided into halves.<br>Each half is:<br>"
             "• an equilateral triangle<br>• an isosceles triangle<br>• a right triangle",
             "A rectangle has a long side and a short side.",
             ["Each half has a corner of the rectangle. That corner is a right angle. ✓ right triangle.",
              "Each half has a long side, a short side and the cut. All 3 are different lengths. ✗ isosceles.",
              "The sides are not all equal. ✗ equilateral."],
             "✓ a right triangle only",
             "The 3 sides of each half are all different, but each half has a right angle.", rect))
q71.append(Q("Exercise 5 (a)", 12, "Answer the following question.<br>What type of triangle has 3 different sides?",
             "Think: equilateral, isosceles or scalene?",
             ["Equilateral has 3 equal sides. Isosceles has 2 equal sides.",
              "A triangle with <b>no</b> equal sides (3 different sides) is a <b>scalene triangle</b>."],
             "Scalene triangle", "A scalene triangle has 3 different sides and 3 different angles."))
q71.append(Q("Exercise 5 (b)", 12, "Answer the following question.<br>What type of triangle has 1 obtuse angle?",
             "Think: acute, right or obtuse?",
             ["An obtuse angle is more than 90° but less than 180°.",
              "A triangle with 1 obtuse angle is an <b>obtuse triangle</b>."],
             "Obtuse triangle", "The name of the triangle comes from its biggest angle."))
q71.append(Q("Exercise 5 (c)", 12,
             "Answer the following question.<br>What type of triangle does not have only 1 acute angle or at least 1 obtuse angle?",
             "If a triangle has no obtuse angle (and no right angle), what are all its angles?",
             ["The triangle has no obtuse angle.",
              "It also does not have just 1 acute angle. So it has more acute angles: in fact all 3 angles are acute.",
              "A triangle with 3 acute angles is an <b>acute triangle</b>."],
             "Acute triangle", "All the angles in an acute triangle are acute angles."))

flash71 = [
    {"front": "Equilateral triangle", "back": "3 equal sides and 3 equal angles (each 60°)"},
    {"front": "Isosceles triangle", "back": "2 equal sides and 2 equal angles"},
    {"front": "Scalene triangle", "back": "3 different sides and 3 different angles"},
    {"front": "Right triangle", "back": "1 right angle (90°). The other 2 angles add up to 90°."},
    {"front": "Acute triangle", "back": "All 3 angles are less than 90°"},
    {"front": "Obtuse triangle", "back": "1 angle is more than 90° but less than 180°"},
    {"front": "Base of a triangle", "back": "The side at the bottom, opposite the vertex angle"},
    {"front": "Vertex angle", "back": "The angle opposite the base"},
    {"front": "Base angles", "back": "The 2 angles on the base"},
    {"front": "Height of a triangle", "back": "A line from the vertex that meets the base at 90°"},
    {"front": "What do tick marks on sides mean?", "back": "Sides with the same tick marks are equal"},
    {"front": "What does a small square in a corner mean?", "back": "A right angle (90°)"},
]
match71 = [
    ["Equilateral", "3 equal sides"], ["Isosceles", "2 equal sides"], ["Scalene", "No equal sides"],
    ["Right triangle", "One 90° angle"], ["Acute triangle", "All angles less than 90°"],
    ["Obtuse triangle", "One angle more than 90°"], ["Each angle of an equilateral triangle", "60°"],
    ["Height", "Meets the base at 90°"], ["Vertex angle", "Opposite the base"],
]
quiz71 = [
    {"q": "A triangle has 3 equal sides. What is it?", "options": ["Equilateral", "Isosceles", "Scalene", "Right"]},
    {"q": "A triangle has 2 equal sides. What is it?", "options": ["Isosceles", "Equilateral", "Scalene", "Obtuse"]},
    {"q": "A triangle has sides 4 cm, 5 cm and 6 cm. What is it?", "options": ["Scalene", "Isosceles", "Equilateral", "Right"]},
    {"q": "Each angle of an equilateral triangle is…", "options": ["60°", "90°", "45°", "180°"]},
    {"q": "A triangle has angles 50°, 60° and 70°. What is it?", "options": ["Acute triangle", "Obtuse triangle", "Right triangle", "Scalene only"]},
    {"q": "A triangle has angles 100°, 40° and 40°. What is it?", "options": ["Obtuse triangle", "Acute triangle", "Right triangle", "Equilateral"]},
    {"q": "A triangle has angles 90°, 30° and 60°. What is it?", "options": ["Right triangle", "Acute triangle", "Obtuse triangle", "Isosceles"]},
    {"q": "In a right triangle, the other 2 angles add up to…", "options": ["90°", "180°", "60°", "100°"]},
    {"q": "In an isosceles triangle, which angles are equal?", "options": ["The 2 angles opposite the equal sides", "All 3 angles", "No angles", "The vertex angle and one base angle"]},
    {"q": "The angle opposite the base is called the…", "options": ["Vertex angle", "Base angle", "Right angle", "Height"]},
    {"q": "Which triangle can be obtuse AND isosceles?", "options": ["120°, 30°, 30°", "60°, 60°, 60°", "90°, 45°, 45°", "50°, 60°, 70°"]},
    {"q": "Is every equilateral triangle an acute triangle?", "options": ["Yes, all angles are 60°", "No, it has a right angle", "No, it has an obtuse angle", "Only if it is big"]},
]
check(120 + 30 + 30, 180, "quiz 7.1"); check(100 + 40 + 40, 180, "quiz 7.1"); check(90 + 30 + 60, 180, "quiz 7.1")
check(50 + 60 + 70, 180, "quiz 7.1")

sections.append({"id": "7-1", "title": "Types of Triangles", "short": "1. Types of Triangles", "pages": "p.2 to 12",
                 "learn": learn71, "questions": q71, "flash": flash71, "match": match71, "quiz": quiz71})

# ==================================================================
# 7.2 ANGLES OF A TRIANGLE  (p.13 to 20)
# ==================================================================


def find_tri(names, angs, unknown_idx, label, fill, base=None, rights=(), ticks=(), up=True):
    """Triangle where one angle is a letter. angs: true angles; label list of strings for display."""
    B, C = base or ([50, 195], [270, 195])
    A = apex(B, C, angs[1], angs[2], up)
    P = [A, B, C]
    extra = []
    for k in range(3):
        v = names[k]
        a, b = [names[j] for j in range(3) if j != k]
        if k in rights:
            extra.append({"t": "ra", "v": v, "a": a, "b": b})
        elif label[k]:
            extra.append({"t": "ang", "v": v, "a": a, "b": b, "s": label[k], "r": 26})
    for tk in ticks:
        extra.append({"t": "tick", "p": list(tk)})
    return triangle(names, P, fill, extra)


# Learn figures
fx = find_tri("XZY", [30, 100, 50], 1, ["30°", "?", "50°"], GREEN)
fe = find_tri("FEG", [120, 25, 35], 1, ["120°", "?", "35°"], ORANGE)
fi = find_tri("ACB", [68, 56, 56], 1, ["68°", "?", ""], BLUE, ticks=[("A", "C"), ("A", "B")])
check(180 - 30 - 50, 100, "p.14 Q1(a)")
check(180 - 120 - 35, 25, "p.14 Q1(b)")
check((180 - 68) / 2, 56, "p.14 Q2")
# p.15 Q3: EFH right at H, EGH isosceles EH = GH, angle EHG = 66
check(180 - 90 - 66, 24, "p.15 Q3 b")
check((180 - 66) / 2, 57, "p.15 Q3 angle GEH")
check(90 - 57, 33, "p.15 Q3 a")
# p.15 Q4
check(180 - 48 - 72, 60, "p.15 Q4 angle ACD")
check(180 - 60, 120, "p.15 Q4 x")
check(180 - 48 - 26 - 72, 34, "p.15 Q4 method 2")
check(180 - 26 - 34, 120, "p.15 Q4 method 2 x")

H3, F3 = [60, 200], [300, 60]
E3 = [60, 60]
G3 = lerp(H3, F3, 0)  # placeholder
# G on HF such that HG = HE, angle EHG = 66 means HF direction makes 66 deg with HE
import math as _m
dirHF = [_m.sin(_m.radians(66)), -_m.cos(_m.radians(66))]  # from H, rotate from up (HE) by 66 deg towards right
HE = 140
G3 = [round(H3[0] + HE * dirHF[0], 1), round(H3[1] + HE * dirHF[1], 1)]
E3 = [H3[0], H3[1] - HE]
# F on line HG extended where EF is horizontal-ish: right angle at E between EH and EF -> F has y = E.y
tF = (E3[1] - H3[1]) / dirHF[1]
F3 = [round(H3[0] + tF * dirHF[0], 1), E3[1]]
fq3 = F(340, 230, {"E": E3, "F": F3, "G": G3, "H": H3}, [
    {"t": "poly", "p": ["E", "F", "H"], "fill": PINK}, {"t": "seg", "p": ["E", "G"]},
    {"t": "ra", "v": "E", "a": "H", "b": "F"},
    {"t": "tick", "p": ["E", "H"]}, {"t": "tick", "p": ["H", "G"]},
    {"t": "ang", "v": "H", "a": "E", "b": "G", "s": "66°", "r": 26},
    {"t": "ang", "v": "E", "a": "G", "b": "F", "s": "a", "r": 34},
    {"t": "ang", "v": "F", "a": "E", "b": "H", "s": "b", "r": 40, "lr": 14},
    {"t": "pl", "p": "E", "d": [-12, 0]}, {"t": "pl", "p": "F", "d": [12, 4]},
    {"t": "pl", "p": "G", "d": [6, 24]}, {"t": "pl", "p": "H", "d": [-12, 14]}])

D4, C4, B4 = [40, 170], [180, 170], [320, 170]
A4 = apex(D4, B4, 48, 26)
fq4 = F(350, 210, {"A": A4, "B": B4, "C": C4, "D": D4}, [
    {"t": "poly", "p": ["A", "D", "B"], "fill": GREEN}, {"t": "seg", "p": ["A", "C"]},
    {"t": "ang", "v": "D", "a": "A", "b": "C", "s": "48°", "r": 24},
    {"t": "ang", "v": "B", "a": "A", "b": "C", "s": "26°", "r": 34},
    {"t": "ang", "v": "A", "a": "D", "b": "C", "s": "72°", "r": 26},
    {"t": "ang", "v": "C", "a": "A", "b": "B", "s": "x", "r": 20},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [12, 8]},
    {"t": "pl", "p": "C", "d": [0, 26]}, {"t": "pl", "p": "D", "d": [-12, 8]}])
# keep the drawing honest: angle DAC really is 72
from geo import angle_at  # noqa: E402
C4 = foot(A4, D4, B4)
# move C so that angle DAC = 72
dirAD = _m.atan2(D4[1] - A4[1], D4[0] - A4[0])
dirAC = dirAD - _m.radians(72)
t = (D4[1] - A4[1]) / _m.sin(dirAC)
C4 = [round(A4[0] + t * _m.cos(dirAC), 1), D4[1]]
fq4["pts"]["C"] = C4
check(round(angle_at(A4, D4, C4)), 72, "p.15 Q4 drawing")

learn72 = [
    L("Idea", "Angles of a triangle add up to 180°",
      "<p>Tear off the 3 corners of any paper triangle and put them side by side. They make a <b>straight line</b>.</p>"
      "<p>A straight line is 180°. So the <b>3 angles of a triangle always add up to 180°</b>.</p>", None, 13),
    L("Example", "Try it with numbers",
      "<p>An equilateral triangle: 60° + 60° + 60° = <b>180°</b> ✓</p>"
      "<p>A right triangle with 90°, 30° and 60°: 90° + 30° + 60° = <b>180°</b> ✓</p>", None, 13),
    L("Idea", "Finding a missing angle",
      "<p>Start with 180°. Take away the angles you know. What is left is the missing angle.</p>"
      "<p><b>Missing angle = 180° - first angle - second angle</b></p>", None, 14),
    L("Example", "Find ∠XZY",
      "<p>The known angles are 30° and 50°.</p><p>∠XZY = 180° - 30° - 50°<br>= 150° - 50°<br>= <b>100°</b></p>", fx, 14),
    L("Example", "Find ∠FEG",
      "<p>The known angles are 120° and 35°.</p><p>∠FEG = 180° - 120° - 35°<br>= 60° - 35°<br>= <b>25°</b></p>", fe, 14),
    L("Idea", "Angles in an isosceles triangle",
      "<p>The 2 angles opposite the equal sides are equal.</p>"
      "<p>To find one of them: <b>(180° - the other angle) ÷ 2</b></p>", None, 14),
    L("Example", "ABC is isosceles. Find ∠ACB.",
      "<p>∠ACB = ∠ABC (they are opposite the equal sides).</p><p>∠ACB + ∠ABC = 180° - 68° = 112°</p>"
      "<p>∠ACB = 112° ÷ 2 = <b>56°</b></p>", fi, 14),
    L("Idea", "Two more helpful facts",
      "<p>In a <b>right triangle</b>, the other 2 angles add up to <b>90°</b>.</p>"
      "<p>Angles on a <b>straight line</b> add up to <b>180°</b>.</p>", None, 15),
    L("Example", "Find ∠a and ∠b",
      "<p>EFH is a right triangle. EGH is isosceles with EH = GH and ∠EHG = 66°.</p>"
      "<p>∠b = 180° - 90° - 66° = <b>24°</b></p><p>∠GEH = (180° - 66°) ÷ 2 = 114° ÷ 2 = 57°</p>"
      "<p>∠a = 90° - 57° = <b>33°</b></p>", fq3, 15),
    L("Example", "BCD is a straight line. Find ∠x.",
      "<p>∠DAC = 72°, ∠ADC = 48°.</p><p>In triangle ACD: ∠ACD = 180° - 48° - 72° = 60°</p>"
      "<p>∠x and ∠ACD are on a straight line: ∠x = 180° - 60° = <b>120°</b></p>", fq4, 15),
]

q72 = []
# Do and Learn p.16
check(180 - 105 - 48, 27, "p.16 a")
check(180 - 90 - 55, 35, "p.16 b")
check(180 / 3, 60, "p.16 e")
check(180 - 47 - 46, 87, "p.16 d")


def simple_find(label, page, names, angs, known_labels, unk_name, unk_idx, fill, ans, rights=(), ticks=(), hint=None, steps=None, why=None):
    lab = list(known_labels)
    lab[unk_idx] = unk_name
    fg = find_tri(names, angs, unk_idx, lab, fill, rights=rights, ticks=ticks)
    return fg


def angle_q(label, page, fg, unk, known, key, extra_note=None):
    """Standard 'find the missing angle' with 2 known angles."""
    a, b = known
    fg["items"] = [x for x in fg["items"] if x["t"] != "pl"]
    check(180 - a - b, key, f"p.{page} {label}")
    steps = [f"The 3 angles of a triangle add up to <b>180°</b>.",
             f"The angles we know are <b>{deg(a)}</b> and <b>{deg(b)}</b>." + (f" {extra_note}" if extra_note else ""),
             f"{unk} = 180° - {deg(a)} - {deg(b)}",
             f"180° - {deg(a)} = {deg(180 - a)}",
             f"{deg(180 - a)} - {deg(b)} = <b>{deg(180 - a - b)}</b>"]
    return Q(label, page, f"Find the unknown marked angle {unk}.", "Start with 180° and take away the angles you know.",
             steps, f"{unk} = {deg(key)}", f"{deg(a)} + {deg(b)} + {deg(key)} = 180°", fg)


q72.append(angle_q("Do and Learn (a)", 16, find_tri("aBC", [27, 105, 48], 0, ["a", "105°", "48°"], PINK), "∠a", (105, 48), 27))
q72.append(angle_q("Do and Learn (b)", 16, find_tri("bBC", [35, 90, 55], 0, ["b", "", "55°"], BLUE, rights=(1,)), "∠b", (90, 55), 35,
                   "The small square is a right angle, 90°."))
fe60 = find_tri("ABe", [60, 60, 60], 2, ["", "", "e"], YELLOW, ticks=[("A", "B"), ("B", "e"), ("A", "e")])
fe60["items"] = [x for x in fe60["items"] if x["t"] != "pl"]
check(180 / 3, 60, "p.16 c")
q72.append(Q("Do and Learn (c)", 16, "Find the unknown marked angle ∠e.", "All 3 sides have tick marks. What kind of triangle is it?",
             ["All 3 sides have the same tick mark, so the triangle is <b>equilateral</b>.",
              "An equilateral triangle has 3 equal angles. They add up to 180°.",
              "∠e = 180° ÷ 3 = <b>60°</b>"],
             "∠e = 60°", "Every angle in an equilateral triangle is 60°.", fe60))
q72.append(angle_q("Do and Learn (d)", 16, find_tri("dAB", [87, 47, 46], 0, ["d", "47°", "46°"], ORANGE), "∠d", (47, 46), 87))

# Exercise 1 p.17
for lab, nm, angs, labels, unk, known, key, fill, rights in [
    ("Exercise 1 (a)", "qAB", [70, 70, 40], ["q", "70°", "40°"], "∠q", (70, 40), 70, ORANGE, ()),
    ("Exercise 1 (b)", "rAB", [122, 30, 28], ["r", "30°", "28°"], "∠r", (30, 28), 122, GREEN, ()),
    ("Exercise 1 (c)", "sAB", [80, 65, 35], ["s", "65°", "35°"], "∠s", (65, 35), 80, PINK, ()),
    ("Exercise 1 (d)", "tAB", [73, 62, 45], ["t", "62°", "45°"], "∠t", (62, 45), 73, BLUE, ()),
    ("Exercise 1 (e)", "aAB", [58, 32, 90], ["a", "32°", ""], "∠a", (32, 90), 58, PURPLE, (2,)),
    ("Exercise 1 (f)", "bAB", [44, 78, 58], ["b", "78°", "58°"], "∠b", (78, 58), 44, ORANGE, ()),
]:
    fg = find_tri(nm, angs, 0, labels, fill, rights=rights)
    # hide helper corner names
    fg["items"] = [x for x in fg["items"] if not (x["t"] == "pl")]
    q72.append(angle_q(lab, 17, fg, unk, known, key, "The small square is a right angle, 90°." if rights else None))

# Exercise 2 p.18: ACD equilateral, BCD straight line
D2, C2, B2 = [40, 170], [170, 170], [300, 170]
A2 = apex(D2, C2, 60, 60)
f18a = F(340, 210, {"A": A2, "B": B2, "C": C2, "D": D2}, [
    {"t": "poly", "p": ["A", "D", "C"], "fill": YELLOW}, {"t": "poly", "p": ["A", "C", "B"], "fill": "#FFFDE7"},
    {"t": "tick", "p": ["A", "D"]}, {"t": "tick", "p": ["D", "C"]}, {"t": "tick", "p": ["A", "C"]},
    {"t": "ang", "v": "C", "a": "A", "b": "B", "s": "b", "r": 20},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [12, 8]}, {"t": "pl", "p": "C", "d": [0, 26]}, {"t": "pl", "p": "D", "d": [-12, 8]}])
check(180 - 60, 120, "p.18 Q2")
q72.append(Q("Exercise 2", 18, "ACD is an equilateral triangle and BCD is a straight line. Find ∠b.",
             "What is each angle of an equilateral triangle? What do angles on a straight line add up to?",
             ["ACD is equilateral, so each of its angles is 60°. So <b>∠ACD = 60°</b>.",
              "BCD is a straight line. Angles on a straight line add up to 180°.",
              "∠b and ∠ACD sit together on the straight line. So ∠b = 180° - 60°",
              "∠b = <b>120°</b>"],
             "∠b = 120°", "60° + 120° = 180°, a straight line.", f18a))

# Exercise 3 p.18: PSR straight, PSQ and PQR right angles, angle SQR = 26
Q3p, R3p = [220, 190], [70, 190]
P3p = [220, 20]
S3p = foot(Q3p, P3p, R3p)
f18b = F(300, 220, {"P": P3p, "Q": Q3p, "R": R3p, "S": S3p}, [
    {"t": "poly", "p": ["P", "R", "Q"], "fill": BLUE}, {"t": "seg", "p": ["Q", "S"]},
    {"t": "ra", "v": "Q", "a": "P", "b": "R"}, {"t": "ra", "v": "S", "a": "Q", "b": "P"},
    {"t": "ang", "v": "Q", "a": "S", "b": "R", "s": "26°", "r": 38, "lr": 16},
    {"t": "ang", "v": "R", "a": "S", "b": "Q", "s": "c", "r": 22},
    {"t": "ang", "v": "P", "a": "R", "b": "Q", "s": "d", "r": 36},
    {"t": "pl", "p": "P", "d": [0, -8]}, {"t": "pl", "p": "Q", "d": [12, 14]}, {"t": "pl", "p": "R", "d": [-12, 10]}, {"t": "pl", "p": "S", "d": [-14, -2]}])
check(90 - 26, 64, "p.18 Q3 c")
check(90 - 64, 26, "p.18 Q3 d")
q72.append(Q("Exercise 3", 18, "PSR is a straight line and ∠PSQ and ∠PQR are right angles. Find ∠c and ∠d.",
             "Look for right triangles. In a right triangle, the other 2 angles add up to 90°.",
             ["Triangle QSR has a right angle at S (∠PSQ = 90°, so ∠QSR = 90° too).",
              "So ∠c and 26° add up to 90°. ∠c = 90° - 26° = <b>64°</b>.",
              "Now look at the big triangle PQR. It has a right angle at Q.",
              "So ∠d and ∠c add up to 90°. ∠d = 90° - 64° = <b>26°</b>."],
             "∠c = 64°, ∠d = 26°", "Each right triangle's other 2 angles add up to 90°: 26° + 64° = 90° and 64° + 26° = 90°.", f18b))

# Exercise 4 p.18: EFH equilateral, EG perpendicular to HF
H4, F4 = [50, 190], [250, 190]
E4 = apex(H4, F4, 60, 60)
E4 = [E4[0] + 20, E4[1]]  # book picture is tilted a little; keep it close to equilateral
G4 = foot(E4, H4, F4)
f18c = F(300, 230, {"E": E4, "F": F4, "G": G4, "H": H4}, [
    {"t": "poly", "p": ["E", "H", "F"], "fill": ORANGE}, {"t": "seg", "p": ["E", "G"]},
    {"t": "ra", "v": "G", "a": "E", "b": "F"},
    {"t": "ang", "v": "E", "a": "G", "b": "F", "s": "g", "r": 34},
    {"t": "pl", "p": "E", "d": [0, -8]}, {"t": "pl", "p": "F", "d": [12, 10]}, {"t": "pl", "p": "G", "d": [0, 26]}, {"t": "pl", "p": "H", "d": [-12, 10]}])
check(90 - 60, 30, "p.18 Q4")
q72.append(Q("Exercise 4", 18, "EFH is an equilateral triangle. Find ∠g.",
             "Look at the small triangle EGF. It has a right angle at G.",
             ["EFH is equilateral, so <b>∠EFH = 60°</b>.",
              "Triangle EGF has a right angle at G. So ∠g and ∠EFG add up to 90°.",
              "∠g = 90° - 60° = <b>30°</b>"],
             "∠g = 30°", "In triangle EGF: 90° + 60° + 30° = 180°.", f18c))

# Exercise 5 p.19: KLM straight, JLM isosceles JL = LM, angle M = 30, angle K = 90
M5, L5, K5 = [40, 190], [200, 190], [290, 190]
J5 = [290, 190 - round((290 - 40) * _m.tan(_m.radians(30)), 1)]
f19a = F(330, 220, {"J": J5, "K": K5, "L": L5, "M": M5}, [
    {"t": "poly", "p": ["J", "M", "K"], "fill": ORANGE}, {"t": "seg", "p": ["J", "L"]},
    {"t": "ra", "v": "K", "a": "J", "b": "L"},
    {"t": "ang", "v": "M", "a": "J", "b": "K", "s": "30°", "r": 40, "lr": 16},
    {"t": "ang", "v": "J", "a": "L", "b": "K", "s": "f", "r": 34},
    {"t": "pl", "p": "J", "d": [0, -8]}, {"t": "pl", "p": "K", "d": [12, 12]}, {"t": "pl", "p": "L", "d": [0, 26]}, {"t": "pl", "p": "M", "d": [-12, 8]}])
check(180 - 90 - 30 - 30, 30, "p.19 Q5")
q72.append(Q("Exercise 5", 19, "KLM is a straight line. JLM is an isosceles triangle and JL = LM. Find ∠f.",
             "JL = LM, so two angles of triangle JLM are equal. Then look at the big triangle JKM.",
             ["In triangle JLM, JL = LM. The angles opposite these sides are equal, so <b>∠MJL = ∠JML = 30°</b>.",
              "Now look at the big triangle JMK. Its angles are 30° (at M), 90° (at K) and ∠MJK at J.",
              "∠MJK = ∠MJL + ∠f = 30° + ∠f.",
              "∠f = 180° - 90° - 30° - 30°",
              "180° - 90° = 90°, 90° - 30° = 60°, 60° - 30° = <b>30°</b>"],
             "∠f = 30°", "The big triangle: 30° + 90° + (30° + 30°) = 180°.", f19a))

# Exercise 6 p.19: PQR straight, PS = RS, angle P = 25, SQ perpendicular
P6, Q6, R6 = [40, 60], [180, 60], [320, 60]
S6 = [180, 60 + round(140 * _m.tan(_m.radians(25)), 1)]
f19b = F(360, 160, {"P": P6, "Q": Q6, "R": R6, "S": S6}, [
    {"t": "poly", "p": ["P", "S", "R"], "fill": GREEN}, {"t": "seg", "p": ["Q", "S"]},
    {"t": "ra", "v": "Q", "a": "S", "b": "R"},
    {"t": "tick", "p": ["P", "S"]}, {"t": "tick", "p": ["S", "R"]},
    {"t": "ang", "v": "P", "a": "R", "b": "S", "s": "25°", "r": 36, "lr": 18},
    {"t": "ang", "v": "S", "a": "Q", "b": "R", "s": "e", "r": 24},
    {"t": "pl", "p": "P", "d": [-12, 4]}, {"t": "pl", "p": "Q", "d": [0, -8]}, {"t": "pl", "p": "R", "d": [12, 4]}, {"t": "pl", "p": "S", "d": [0, 24]}])
check(90 - 25, 65, "p.19 Q6")
q72.append(Q("Exercise 6", 19, "PQR is a straight line and PS = RS. Find ∠e.",
             "PS = RS, so ∠SPQ and ∠SRQ are equal. Then use the right triangle SQR.",
             ["PS = RS, so triangle PSR is isosceles. The angles opposite the equal sides are equal: <b>∠SRQ = ∠SPQ = 25°</b>.",
              "Triangle SQR has a right angle at Q. So ∠e and ∠SRQ add up to 90°.",
              "∠e = 90° - 25° = <b>65°</b>"],
             "∠e = 65°", "In triangle SQR: 90° + 25° + 65° = 180°.", f19b))

# Exercise 7 p.19: ACD equilateral, ABC isosceles AB = AC, angle CAB = 36
A7 = [165, 30]
C7 = [165, 220]
D7 = [round(165 - 190 * _m.sin(_m.radians(60)), 1), round(30 + 190 * _m.cos(_m.radians(60)), 1)]
B7 = [round(165 + 190 * _m.sin(_m.radians(36)), 1), round(30 + 190 * _m.cos(_m.radians(36)), 1)]
f19c = F(330, 250, {"A": A7, "B": B7, "C": C7, "D": D7}, [
    {"t": "poly", "p": ["A", "D", "C", "B"], "fill": PURPLE}, {"t": "seg", "p": ["A", "C"]},
    {"t": "tick", "p": ["A", "D"]}, {"t": "tick", "p": ["D", "C"]}, {"t": "tick", "p": ["A", "C"]}, {"t": "tick", "p": ["A", "B"]},
    {"t": "ang", "v": "A", "a": "C", "b": "B", "s": "36°", "r": 34},
    {"t": "ang", "v": "C", "a": "D", "b": "B", "r": 20},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [14, 8]}, {"t": "pl", "p": "C", "d": [0, 26]}, {"t": "pl", "p": "D", "d": [-14, 8]}])
check(180 - 36, 144, "p.19 Q7 step")
check(144 / 2, 72, "p.19 Q7 ACB")
check(60 + 72, 132, "p.19 Q7")
q72.append(Q("Exercise 7", 19, "ACD is an equilateral triangle. ABC is an isosceles triangle and AB = AC. Find ∠BCD.",
             "∠BCD is made of 2 parts: ∠ACD and ∠ACB. Find each part.",
             ["ABC is isosceles with AB = AC, so ∠ACB = ∠ABC.",
              "∠ACB + ∠ABC = 180° - 36° = <b>144°</b>",
              "∠ACB = 144° ÷ 2 = <b>72°</b>",
              "ACD is equilateral, so ∠ACD = <b>60°</b>.",
              "∠BCD = ∠ACD + ∠ACB = 60° + 72° = <b>132°</b>"],
             "∠BCD = 132°", "∠BCD is the 60° angle and the 72° angle put together.", f19c))

# Exercise 8 p.20: JKL isosceles JK = JL, angle J = 70; MKL isosceles MK = ML, angle MLK = 25
L8, K8 = [40, 200], [300, 200]
J8 = apex(L8, K8, 55, 55)
M8 = apex(L8, K8, 25, 25)
f20a = F(340, 230, {"J": J8, "K": K8, "L": L8, "M": M8}, [
    {"t": "poly", "p": ["J", "L", "K"], "fill": BLUE}, {"t": "seg", "p": ["L", "M"]}, {"t": "seg", "p": ["M", "K"]},
    {"t": "tick", "p": ["J", "L"], "n": 2}, {"t": "tick", "p": ["J", "K"], "n": 2},
    {"t": "tick", "p": ["M", "L"]}, {"t": "tick", "p": ["M", "K"]},
    {"t": "ang", "v": "J", "a": "L", "b": "K", "s": "70°", "r": 24},
    {"t": "ang", "v": "L", "a": "M", "b": "K", "s": "25°", "r": 46, "lr": 18},
    {"t": "pl", "p": "J", "d": [0, -8]}, {"t": "pl", "p": "K", "d": [12, 10]}, {"t": "pl", "p": "L", "d": [-12, 10]}, {"t": "pl", "p": "M", "d": [0, -10]}])
check(180 - 70, 110, "p.20 Q8 step")
check(110 / 2, 55, "p.20 Q8 JLK")
check(55 - 25, 30, "p.20 Q8")
q72.append(Q("Exercise 8", 20, "JKL and MKL are isosceles triangles and JK = JL and MK = ML. Find ∠JLM.",
             "First find ∠JLK in the big triangle. Then take away ∠MLK.",
             ["JK = JL, so ∠JLK = ∠JKL.",
              "∠JLK + ∠JKL = 180° - 70° = <b>110°</b>",
              "∠JLK = 110° ÷ 2 = <b>55°</b>",
              "∠JLM = ∠JLK - ∠MLK = 55° - 25° = <b>30°</b>"],
             "∠JLM = 30°", "∠JLK (55°) is split into ∠JLM and ∠MLK (25°): 30° + 25° = 55°.", f20a))

# Exercise 9 p.20: STW equilateral; angle WST split into 3 equal parts by SV and SU
W9, T9 = [40, 200], [300, 200]
S9 = apex(W9, T9, 60, 60)
V9 = [round(S9[0] - (200 - S9[1]) * _m.tan(_m.radians(10)), 1), 200]
U9 = [round(S9[0] + (200 - S9[1]) * _m.tan(_m.radians(10)), 1), 200]
f20b = F(340, 230, {"S": S9, "T": T9, "U": U9, "V": V9, "W": W9}, [
    {"t": "poly", "p": ["S", "W", "T"], "fill": PURPLE}, {"t": "seg", "p": ["S", "V"]}, {"t": "seg", "p": ["S", "U"]},
    {"t": "ang", "v": "U", "a": "S", "b": "V", "r": 18},
    {"t": "pl", "p": "S", "d": [0, -8]}, {"t": "pl", "p": "T", "d": [12, 10]}, {"t": "pl", "p": "U", "d": [4, 26]}, {"t": "pl", "p": "V", "d": [-4, 26]}, {"t": "pl", "p": "W", "d": [-12, 10]}])
check(60 / 3, 20, "p.20 Q9 VSU")
check((180 - 20) / 2, 80, "p.20 Q9")
q72.append(Q("Exercise 9", 20, "STW is an equilateral triangle. SUV is an isosceles triangle. ∠VSW = ∠VSU = ∠UST. Find ∠SUV.",
             "The 60° angle at S is cut into 3 equal parts.",
             ["STW is equilateral, so ∠WST = 60°.",
              "∠WST is cut into 3 equal angles. ∠VSU = 60° ÷ 3 = <b>20°</b>",
              "SUV is isosceles, so ∠SUV = ∠SVU.",
              "∠SUV + ∠SVU = 180° - 20° = 160°",
              "∠SUV = 160° ÷ 2 = <b>80°</b>"],
             "∠SUV = 80°", "In triangle SUV: 20° + 80° + 80° = 180°.", f20b))

# Exercise 10 p.20: right angle at C, angle B = 38, AD bisects CAB
C10, B10 = [60, 200], [300, 200]
A10 = apex(C10, B10, 90, 38)
D10 = [round(60 + (200 - A10[1]) * _m.tan(_m.radians(26)), 1), 200]
f20c = F(340, 230, {"A": A10, "B": B10, "C": C10, "D": D10}, [
    {"t": "poly", "p": ["A", "C", "B"], "fill": ORANGE}, {"t": "seg", "p": ["A", "D"]},
    {"t": "ra", "v": "C", "a": "A", "b": "B"},
    {"t": "ang", "v": "B", "a": "A", "b": "C", "s": "38°", "r": 40, "lr": 16},
    {"t": "pl", "p": "A", "d": [-6, -8]}, {"t": "pl", "p": "B", "d": [12, 10]}, {"t": "pl", "p": "C", "d": [-12, 10]}, {"t": "pl", "p": "D", "d": [0, 26]}])
check(180 - 90 - 38, 52, "p.20 Q10 CAB")
check(Fraction(1, 2) * 52, 26, "p.20 Q10 CAD")
check(52 - 26, 26, "p.20 Q10")
q72.append(Q("Exercise 10", 20, "ABC is a right triangle such that ∠CAD = ½ ∠CAB. Find ∠DAB.",
             "First find the whole angle ∠CAB. ∠CAD is half of it.",
             ["Triangle ABC has a right angle at C and ∠ABC = 38°.",
              "∠CAB = 180° - 90° - 38° = <b>52°</b>",
              "∠CAD is half of ∠CAB: ½ of 52° = 52° ÷ 2 = <b>26°</b>",
              "∠CAB is cut into 2 halves, so the other half is the same: ∠DAB = ∠CAD = <b>26°</b>"],
             "∠DAB = 26°", "26° + 26° = 52° = ∠CAB.", f20c))

flash72 = [
    {"front": "Angles of a triangle add up to…", "back": "180°"},
    {"front": "Angles on a straight line add up to…", "back": "180°"},
    {"front": "In a right triangle, the other 2 angles add up to…", "back": "90°"},
    {"front": "Missing angle rule", "back": "180° - first angle - second angle"},
    {"front": "Base angle of an isosceles triangle", "back": "(180° - vertex angle) ÷ 2"},
    {"front": "Each angle of an equilateral triangle", "back": "60°"},
    {"front": "Find the missing angle: 40° and 60°", "back": "180° - 40° - 60° = 80°"},
    {"front": "Find the missing angle: 90° and 35°", "back": "180° - 90° - 35° = 55°"},
    {"front": "Isosceles triangle, vertex angle 40°. Each base angle?", "back": "(180° - 40°) ÷ 2 = 70°"},
    {"front": "One angle on a straight line is 130°. The other?", "back": "180° - 130° = 50°"},
]
for a, b, c in [(40, 60, 80), (90, 35, 55)]:
    check(180 - a - b, c, "flash 7.2")
check((180 - 40) / 2, 70, "flash 7.2 iso")
check(180 - 130, 50, "flash 7.2 line")
match72 = [
    ["50° and 60°", "70°"], ["90° and 25°", "65°"], ["100° and 30°", "50°"], ["45° and 45°", "90°"],
    ["120° and 20°", "40°"], ["35° and 85°", "60°"], ["70° and 70°", "40°"], ["15° and 75°", "90°"] ,
]
# make answers unique per round: remove duplicate answers
match72 = [["50° and 60°", "70°"], ["90° and 25°", "65°"], ["100° and 30°", "50°"], ["45° and 45°", "90°"],
           ["120° and 20°", "40°"], ["35° and 85°", "60°"], ["20° and 75°", "85°"], ["110° and 45°", "25°"]]
for pair in match72:
    a, b = [int(x.strip().rstrip("°")) for x in pair[0].split("and")]
    check(180 - a - b, int(pair[1].rstrip("°")), "match 7.2")
match72 = [[f"Missing angle: {p[0]}", p[1]] for p in match72]

quiz72 = []
for a, b, wrong in [(70, 40, [110, 80, 60]), (30, 28, [58, 112, 132]), (65, 35, [100, 70, 90]), (90, 32, [122, 68, 48]),
                    (55, 75, [130, 40, 60]), (120, 25, [145, 25, 45])]:
    ans = 180 - a - b
    check(a + b + ans, 180, "quiz 7.2")
    opts = [deg(ans)] + [deg(w) for w in wrong if w != ans]
    quiz72.append({"q": f"Two angles of a triangle are {deg(a)} and {deg(b)}. What is the third angle?", "options": opts[:4]})
quiz72 += [
    {"q": "An isosceles triangle has a vertex angle of 80°. What is each base angle?", "options": ["50°", "100°", "80°", "40°"]},
    {"q": "An isosceles triangle has a vertex angle of 20°. What is each base angle?", "options": ["80°", "160°", "20°", "70°"]},
    {"q": "One angle of a right triangle is 25°. What is the other small angle?", "options": ["65°", "155°", "75°", "25°"]},
    {"q": "One angle on a straight line is 60°. What is the other angle?", "options": ["120°", "60°", "30°", "300°"]},
    {"q": "The angles of a triangle add up to…", "options": ["180°", "360°", "90°", "100°"]},
    {"q": "Can a triangle have 2 right angles?", "options": ["No, 90° + 90° is already 180°", "Yes", "Only if it is big", "Only if it is isosceles"]},
]
check((180 - 80) / 2, 50, "quiz 7.2"); check((180 - 20) / 2, 80, "quiz 7.2"); check(90 - 25, 65, "quiz 7.2"); check(180 - 60, 120, "quiz 7.2")

sections.append({"id": "7-2", "title": "Angles of a Triangle", "short": "2. Angles of a Triangle", "pages": "p.13 to 20",
                 "learn": learn72, "questions": q72, "flash": flash72, "match": match72, "quiz": quiz72})

# ==================================================================
# 7.3 DRAWING TRIANGLES  (p.21 to 27)
# ==================================================================
CM = 30  # pixels per cm in drawings


def built(names, A, B, C, fill, angles=(), sides=(), rights=(), ticks=(), w=340, h=240):
    pts = {names[0]: A, names[1]: B, names[2]: C}
    items = [{"t": "poly", "p": list(names), "fill": fill}]
    for v, s in angles:
        o = [n for n in names if n != v]
        items.append({"t": "ang", "v": v, "a": o[0], "b": o[1], "s": s, "r": 24})
    for v in rights:
        o = [n for n in names if n != v]
        items.append({"t": "ra", "v": v, "a": o[0], "b": o[1]})
    for (a, b, s) in sides:
        items.append({"t": "len", "p": [a, b], "s": s})
    for (a, b) in ticks:
        items.append({"t": "tick", "p": [a, b]})
    cx = (A[0] + B[0] + C[0]) / 3
    cy = (A[1] + B[1] + C[1]) / 3
    for n, p in pts.items():
        dx, dy = p[0] - cx, p[1] - cy
        L_ = (dx * dx + dy * dy) ** 0.5 or 1
        items.append({"t": "pl", "p": n, "d": [round(dx / L_ * 18, 1), round(dy / L_ * 18 + 7, 1)]})
    return F(w, h, pts, items)


# Learn
grid_fig = F(320, 200, {"A": [40, 40], "C": [40, 160], "B": [160, 160], "D": [240, 40], "E": [200, 160], "F": [280, 160]}, [
    {"t": "grid", "x": 20, "y": 20, "cols": 14, "rows": 8, "size": 20},
    {"t": "poly", "p": ["A", "C", "B"], "fill": ORANGE}, {"t": "ra", "v": "C", "a": "A", "b": "B"},
    {"t": "poly", "p": ["D", "E", "F"], "fill": GREEN},
    {"t": "pl", "p": "A", "d": [-12, 4]}, {"t": "pl", "p": "C", "d": [-12, 14]}, {"t": "pl", "p": "B", "d": [10, 16]},
    {"t": "pl", "p": "D", "d": [0, -8]}, {"t": "pl", "p": "E", "d": [-10, 18]}, {"t": "pl", "p": "F", "d": [10, 18]}])
B3, C3 = [60, 190], [60 + 5 * CM * 1.2, 190]
A3 = apex(B3, C3, 50, 45)
draw_fig = built("ABC", A3, B3, C3, YELLOW, angles=[("B", "50°"), ("C", "45°")], sides=[("C", "B", "5 cm")])
Y4, Z4 = [80, 200], [80 + 150, 200]
X4 = [80, 50]
rt_fig = built("XYZ", X4, Y4, Z4, BLUE, rights=["Y"], sides=[("Z", "Y", "5 cm"), ("Y", "X", "5 cm")])

learn73 = [
    L("Idea", "Drawing triangles on square grids",
      "<p>Grid lines go straight across and straight up. So it is easy to make <b>right angles</b> and <b>equal sides</b> by counting squares.</p>", None, 21),
    L("Example", "Right triangle and isosceles triangle on a grid",
      "<p>Triangle ABC: AC goes down 6 squares and CB goes across 6 squares. AC = BC and ∠ACB is a right angle.</p>"
      "<p>Triangle DEF: D is right above the middle of EF. So DE = DF. It is isosceles.</p>", grid_fig, 21),
    L("Idea", "Your drawing tools",
      "<p><b>Ruler</b>: draws straight lines and measures length in cm.</p><p><b>Protractor</b>: measures and draws angles in degrees.</p>"
      "<p><b>Set square</b>: draws a right angle (90°).</p><p>Always draw a quick <b>sketch</b> first and write the measurements on it.</p>", None, 22),
    L("Example", "Draw ABC: BC = 5 cm, ∠ABC = 50°, ∠ACB = 45°",
      "<p><b>Step 1:</b> Draw a straight line BC 5 cm long.<br><b>Step 2:</b> Put the protractor at B. Draw an angle of 50°.<br>"
      "<b>Step 3:</b> Put the protractor at C. Draw an angle of 45°.<br><b>Step 4:</b> The 2 lines meet. Label this point A.</p>", draw_fig, 22),
    L("Idea", "Using a set square for a right angle",
      "<p>Put one edge of the set square on the line. The other edge makes a line at <b>90°</b>.</p>", None, 23),
    L("Example", "Draw XYZ: XY = YZ = 5 cm, ∠XYZ = 90°",
      "<p><b>Step 1:</b> Draw YZ 5 cm long.<br><b>Step 2:</b> Use the set square to draw a line at Y that makes 90° with YZ.<br>"
      "<b>Step 3:</b> Measure 5 cm up from Y. Mark X.<br><b>Step 4:</b> Join X and Z.</p>", rt_fig, 23),
]

q73 = []
check(180 - 40 - 55, 85, "p.24 third angle")
B24, C24 = [50, 200], [50 + 6 * 40, 200]
A24 = apex(B24, C24, 40, 55)
q73.append(Q("Do and Learn", 24, "Draw a triangle ABC in which BC = 6 cm, ∠ABC = 40° and ∠ACB = 55°.",
             "Draw the side you know first (BC). Then draw the 2 angles at B and at C.",
             ["Make a quick sketch. Write 6 cm on BC, 40° at B and 55° at C.",
              "Use your ruler. Draw a straight line <b>BC = 6 cm</b>.",
              "Put the centre of the protractor on B, with 0° on BC. Mark <b>40°</b>. Draw a long line from B through the mark.",
              "Put the centre of the protractor on C, with 0° on CB. Mark <b>55°</b>. Draw a long line from C through the mark.",
              "The 2 lines cross. Label this point <b>A</b>.",
              "Check: ∠BAC should be 180° - 40° - 55° = <b>85°</b>. Measure it with your protractor."],
             "Triangle ABC with BC = 6 cm, ∠ABC = 40°, ∠ACB = 55° (and ∠BAC = 85°)",
             "The side and the 2 angles fix the triangle. The 3 angles add up to 180°.",
             built("ABC", A24, B24, C24, YELLOW, angles=[("B", "40°"), ("C", "55°")], sides=[("C", "B", "6 cm")])))

C25, B25 = [70, 200], [70 + 4 * 45, 200]
A25 = apex(C25, B25, 60, 60)
q73.append(Q("Exercise 1", 25, "Draw a triangle ABC such that each side is equal to CB. (In your book, CB is 4 cm. Measure it with your ruler.)",
             "If all 3 sides are equal, what type of triangle is it? What are its angles?",
             ["Measure CB with your ruler. It is <b>4 cm</b>.",
              "Each side must be equal to CB, so <b>AB = AC = CB = 4 cm</b>. This is an equilateral triangle.",
              "An equilateral triangle has 3 angles of 60°.",
              "Draw CB 4 cm long. At C, draw an angle of <b>60°</b> with the protractor. At B, draw an angle of <b>60°</b>.",
              "The 2 lines meet at A. Measure AB and AC. Each should be <b>4 cm</b>."],
             "An equilateral triangle ABC with each side 4 cm and each angle 60°",
             "All 3 sides are equal to CB, so the triangle is equilateral.",
             built("ABC", A25, C25, B25, PINK, angles=[("A", "60°"), ("B", "60°"), ("C", "60°")],
                   sides=[("C", "A", "4 cm"), ("A", "B", "4 cm"), ("B", "C", "4 cm")])))

check(180 - 70 - 70, 40, "p.25 Q2")
M25, L25 = [70, 210], [250, 210]
K25 = apex(M25, L25, 70, 70)
q73.append(Q("Exercise 2", 25, "Draw a triangle KLM in which ∠KLM = 70° and ∠LMK = 70°.",
             "Draw the base ML first (any length). Then draw 70° at L and 70° at M.",
             ["Sketch first: base ML, with 70° at L and 70° at M.",
              "Draw a straight line ML. (Any length is fine, for example 6 cm.)",
              "At L, use the protractor to draw an angle of <b>70°</b>.",
              "At M, use the protractor to draw an angle of <b>70°</b>.",
              "The 2 lines meet. Label the point <b>K</b>.",
              "Check: ∠MKL = 180° - 70° - 70° = <b>40°</b>."],
             "Triangle KLM with ∠KLM = 70°, ∠LMK = 70° and ∠MKL = 40°",
             "2 equal angles make an isosceles triangle (KL = KM). 70° + 70° + 40° = 180°.",
             built("KML", K25, M25, L25, PURPLE, angles=[("K", "40°"), ("M", "70°"), ("L", "70°")])))

# p.26 Q3: three sides 6, 5.5, 3.5 -> angles 65, 80, 35 (as in the key sketch)
import math
EF, GF, EG = 6, 5.5, 3.5
angE = math.degrees(math.acos((EF ** 2 + EG ** 2 - GF ** 2) / (2 * EF * EG)))
angF = math.degrees(math.acos((EF ** 2 + GF ** 2 - EG ** 2) / (2 * EF * GF)))
angG = 180 - angE - angF
check(round(angE), 65, "p.26 Q3 angle E")
check(round(angF), 35, "p.26 Q3 angle F")
check(round(angG), 80, "p.26 Q3 angle G")
E26, F26 = [40, 200], [40 + 6 * 45, 200]
G26 = [round(40 + 3.5 * 45 * math.cos(math.radians(angE)), 1), round(200 - 3.5 * 45 * math.sin(math.radians(angE)), 1)]
q73.append(Q("Exercise 3", 26, "Draw a triangle EFG in which EF = 6 cm, GF = 5.5 cm and EG = 3.5 cm.",
             "You know all 3 sides. Use a compass to find point G.",
             ["Sketch first: EF = 6 cm, GF = 5.5 cm, EG = 3.5 cm.",
              "Draw a straight line <b>EF = 6 cm</b>.",
              "Open your compass to <b>3.5 cm</b>. Put the needle on E and draw an arc above the line.",
              "Open your compass to <b>5.5 cm</b>. Put the needle on F and draw an arc that crosses the first arc.",
              "The arcs cross at <b>G</b>. Join EG and FG with your ruler.",
              "Check with your protractor: ∠E is about 65°, ∠G is about 80° and ∠F is about 35°. 65° + 80° + 35° = 180°."],
             "Triangle EFG with EF = 6 cm, GF = 5.5 cm and EG = 3.5 cm (∠E ≈ 65°, ∠G ≈ 80°, ∠F ≈ 35°)",
             "G is 3.5 cm from E and 5.5 cm from F, so it is where the 2 arcs meet.",
             built("EFG", E26, F26, G26, ORANGE, angles=[("E", "65°"), ("F", "35°"), ("G", "80°")],
                   sides=[("F", "E", "6 cm"), ("E", "G", "3.5 cm"), ("G", "F", "5.5 cm")])))

J26, K26 = [70, 210], [70 + 5 * 40, 210]
L26 = apex(J26, K26, 60, 60)
q73.append(Q("Exercise 4", 26, "Draw an equilateral triangle JKL such that each side is 5 cm long.",
             "An equilateral triangle has three 60° angles.",
             ["Sketch first: 3 sides of 5 cm and three angles of 60°.",
              "Draw a straight line <b>JK = 5 cm</b>.",
              "At J, draw an angle of <b>60°</b>. At K, draw an angle of <b>60°</b>.",
              "The 2 lines meet at <b>L</b>.",
              "Check: JL and KL should both measure <b>5 cm</b>, and ∠L should be 60°."],
             "Equilateral triangle JKL with each side 5 cm and each angle 60°",
             "3 equal sides means 3 equal angles of 60°.",
             built("LJK", L26, J26, K26, GREEN, angles=[("L", "60°"), ("J", "60°"), ("K", "60°")],
                   sides=[("K", "J", "5 cm"), ("J", "L", "5 cm"), ("L", "K", "5 cm")])))

Y27, Z27 = [70, 210], [70 + 3 * 30, 210]
X27 = [70, 210 - 6 * 30]
q73.append(Q("Exercise 5", 27, "Draw a right triangle XYZ such that XY = 6 cm, YZ = 3 cm and ∠XYZ = 90°.",
             "Use a set square to make the right angle at Y.",
             ["Sketch first: right angle at Y, XY = 6 cm, YZ = 3 cm.",
              "Draw a straight line <b>YZ = 3 cm</b>.",
              "Put the set square on YZ with the corner at Y. Draw a line at <b>90°</b> to YZ.",
              "Measure <b>6 cm</b> along this line from Y. Mark X.",
              "Join X and Z with your ruler."],
             "Right triangle XYZ with XY = 6 cm, YZ = 3 cm and ∠XYZ = 90°",
             "The set square makes an exact right angle at Y.",
             built("XYZ", X27, Y27, Z27, BLUE, rights=["Y"], sides=[("Z", "Y", "3 cm"), ("Y", "X", "6 cm")], w=260)))

check((180 - 135) / 2, 22.5, "p.27 Q6 base angles")
Q27 = [170, 170]
P27 = [round(170 - 4 * 30, 1), 170]
R27 = [round(170 + 4 * 30 * math.cos(math.radians(45)), 1), round(170 - 4 * 30 * math.sin(math.radians(45)), 1)]
q73.append(Q("Exercise 6", 27, "Draw an isosceles triangle PQR in which PQ = QR = 4 cm and ∠PQR = 135°.",
             "Draw PQ first. The 135° angle is at Q, between the 2 equal sides.",
             ["Sketch first: PQ = 4 cm, QR = 4 cm, ∠PQR = 135°.",
              "Draw a straight line <b>PQ = 4 cm</b>.",
              "Put the protractor at Q, with 0° on QP. Mark <b>135°</b> and draw a line from Q.",
              "Measure <b>4 cm</b> along this line from Q. Mark R.",
              "Join P and R.",
              "Check: the other 2 angles are equal: (180° - 135°) ÷ 2 = 22.5° each."],
             "Isosceles triangle PQR with PQ = QR = 4 cm and ∠PQR = 135°",
             "2 equal sides with a 135° angle between them. It is isosceles and obtuse.",
             built("PQR", P27, Q27, R27, PINK, angles=[("Q", "135°")], sides=[("P", "Q", "4 cm"), ("Q", "R", "4 cm")], w=320, h=220)))

flash73 = [
    {"front": "Ruler", "back": "Draws straight lines and measures length (cm)"},
    {"front": "Protractor", "back": "Measures and draws angles (°)"},
    {"front": "Set square", "back": "Draws a right angle (90°)"},
    {"front": "Compass", "back": "Draws circles and arcs. Helps when you know all 3 sides."},
    {"front": "What do you draw first?", "back": "A quick sketch with all the measurements"},
    {"front": "Drawing with 1 side and 2 angles", "back": "Draw the side, then the angle at each end. Where the lines meet is the third corner."},
    {"front": "Drawing with 2 sides and the angle between", "back": "Draw one side, draw the angle, measure the second side, then join the ends."},
    {"front": "How to check your triangle", "back": "Measure the third angle. All 3 angles must add up to 180°."},
]
match73 = [["Ruler", "Straight lines"], ["Protractor", "Angles"], ["Set square", "Right angle"], ["Compass", "Arcs and circles"],
           ["Sketch", "Draw first with measurements"], ["Check", "Angles add up to 180°"], ["cm", "Unit for length"], ["°", "Unit for angles"]]
quiz73 = [
    {"q": "Which tool do you use to draw an angle of 50°?", "options": ["Protractor", "Ruler", "Compass", "Set square"]},
    {"q": "Which tool draws a right angle quickly?", "options": ["Set square", "Compass", "Protractor only", "Pencil"]},
    {"q": "What should you do before you draw a triangle?", "options": ["Make a sketch", "Draw a circle", "Colour it", "Measure the third angle"]},
    {"q": "Triangle ABC: ∠B = 40°, ∠C = 55°. What will ∠A measure?", "options": ["85°", "95°", "105°", "75°"]},
    {"q": "Triangle KLM: ∠L = 70°, ∠M = 70°. What will ∠K measure?", "options": ["40°", "70°", "140°", "110°"]},
    {"q": "You know all 3 sides of a triangle. Which tool helps you find the third corner?", "options": ["Compass", "Protractor", "Set square", "Eraser"]},
    {"q": "An equilateral triangle has sides of 5 cm. What angle do you draw at each end of the base?", "options": ["60°", "90°", "45°", "50°"]},
    {"q": "Triangle PQR: PQ = QR = 4 cm, ∠PQR = 135°. What type of triangle is it?", "options": ["Isosceles and obtuse", "Equilateral", "Right", "Scalene and acute"]},
    {"q": "To draw ∠XYZ = 90°, you put the set square corner at…", "options": ["Y", "X", "Z", "Any point"]},
    {"q": "Triangle XYZ: ∠X = 30°, ∠Y = 90°. What will ∠Z measure?", "options": ["60°", "90°", "120°", "30°"]},
]
check(180 - 40 - 55, 85, "quiz 7.3"); check(180 - 70 - 70, 40, "quiz 7.3"); check(180 - 30 - 90, 60, "quiz 7.3")

sections.append({"id": "7-3", "title": "Drawing Triangles", "short": "3. Drawing Triangles", "pages": "p.21 to 27",
                 "learn": learn73, "questions": q73, "flash": flash73, "match": match73, "quiz": quiz73})

# ==================================================================
# 7.4 PARTS OF A CIRCLE  (p.28 to 34)
# ==================================================================
O = [160, 120]
R = 90


def circ(extra, pts, fill=BLUE, w=320, h=240, c=O, r=R, center="O"):
    p = {center: c}
    p.update(pts)
    items = [{"t": "circle", "c": center, "r": r, "fill": fill}] + extra
    return F(w, h, p, items)


parts_fig = circ([
    {"t": "seg", "p": ["A", "B"]}, {"t": "seg", "p": ["O", "D"]}, {"t": "seg", "p": ["E", "F"]}, {"t": "dot", "p": "O"},
    {"t": "pl", "p": "O", "d": [-2, -10]}, {"t": "pl", "p": "A", "d": [-14, 0]}, {"t": "pl", "p": "B", "d": [14, 10]},
    {"t": "pl", "p": "D", "d": [12, -4]}, {"t": "pl", "p": "E", "d": [-10, 18]}, {"t": "pl", "p": "F", "d": [12, 18]},
    {"t": "txt", "at": [276, 30], "s": "circumference", "size": 14, "color": "#1565c0"}],
    {"A": polar(O, R, 200), "B": polar(O, R, 20), "D": polar(O, R, -50), "E": polar(O, R, 120), "F": polar(O, R, 60)})
d_fig = circ([{"t": "seg", "p": ["O", "P"]}, {"t": "dot", "p": "O"}, {"t": "len", "p": ["O", "P"], "s": "4 cm", "off": -14},
              {"t": "pl", "p": "O", "d": [0, 22]}], {"P": polar(O, R, 0)}, fill=PINK)
learn74 = [
    L("Idea", "Parts of a circle",
      "<p><b>Center</b> (O): the point in the middle.</p><p><b>Radius</b> (OD): a line from the center to the edge.</p>"
      "<p><b>Diameter</b> (AB): a line across the circle that goes through the center.</p>"
      "<p><b>Chord</b> (EF): any line joining 2 points on the edge.</p><p><b>Circumference</b>: the distance all the way around.</p>", parts_fig, 28),
    L("Example", "Is CD a diameter?",
      "<p>A diameter must go through the center O. If CD does not pass through O, it is only a <b>chord</b>.</p>"
      "<p>The diameter is the <b>longest chord</b> of a circle.</p><p>Radii is the plural of radius: one radius, two radii.</p>", parts_fig, 28),
    L("Idea", "Radius and diameter",
      "<p>A diameter is 2 radii joined in a straight line.</p><p><b>Diameter = 2 × Radius</b></p><p><b>Radius = Diameter ÷ 2</b></p>", None, 29),
    L("Example", "Radius 4 cm. Find the diameter.",
      "<p>Think of a pizza: from the middle to the edge is 4 cm. Across the whole pizza is 2 of those.</p>"
      "<p>Diameter = 2 × 4 = <b>8 cm</b></p>", d_fig, 29),
    L("Example", "Diameter 15 m. Find the radius.",
      "<p>Radius = Diameter ÷ 2</p><p>= 15 ÷ 2 = <b>7.5 m</b></p><p>Or: Radius = ½ × 15 = 7.5 m</p>", None, 29),
]
check(2 * 4, 8, "p.29 example"); check(15 / 2, 7.5, "p.29 example")

q74 = []
f30a = circ([{"t": "seg", "p": ["A", "B"]}, {"t": "seg", "p": ["C", "D"]}, {"t": "dot", "p": "O"},
             {"t": "pl", "p": "O", "d": [14, 6]}, {"t": "pl", "p": "A", "d": [10, -6]}, {"t": "pl", "p": "B", "d": [-10, 20]},
             {"t": "pl", "p": "C", "d": [-10, -6]}, {"t": "pl", "p": "D", "d": [10, 20]}],
            {"A": polar(O, R, -60), "B": polar(O, R, 120), "C": polar(O, R, -120), "D": polar(O, R, 60)})
check(18, 18, "p.30 Q1(a)")
q74.append(Q("Do and Learn 1 (a)", 30, "In the circle below, O is the center, AB and CD are the diameters.<br>AB = 18 cm<br>CD = ___ cm",
             "Are all the diameters of one circle the same length?",
             ["AB and CD both go through the center O, so both are diameters.",
              "All the diameters of the same circle are the same length.",
              "So CD = AB = <b>18 cm</b>."],
             "CD = 18 cm", "Every diameter of a circle has the same length.", f30a))
f30b = circ([{"t": "seg", "p": ["O", "A"]}, {"t": "seg", "p": ["O", "B"]}, {"t": "dot", "p": "O"},
             {"t": "pl", "p": "O", "d": [14, 6]}, {"t": "pl", "p": "A", "d": [-6, 22]}, {"t": "pl", "p": "B", "d": [0, -8]}],
            {"A": polar(O, R, 115), "B": polar(O, R, -100)}, fill=ORANGE)
q74.append(Q("Do and Learn 1 (b)", 30, "In the circle below, O is the center, OA and OB are the radii.<br>OA = 7 cm<br>OB = ___ cm",
             "Are all the radii of one circle the same length?",
             ["OA and OB both go from the center O to the edge, so both are radii.",
              "All the radii of the same circle are the same length.",
              "So OB = OA = <b>7 cm</b>."],
             "OB = 7 cm", "Every radius of a circle has the same length.", f30b))
check(2 * 6, 12, "p.30 Q2(a)")
q74.append(Q("Do and Learn 2 (a)", 30, "O is the center. Find the diameter of the circle.<br>Diameter = ___ cm",
             "The 6 cm line goes from the center to the edge. Is it a radius or a diameter?",
             ["The 6 cm line goes from O to the edge, so the <b>radius is 6 cm</b>.",
              "Diameter = 2 × Radius",
              "= 2 × 6 = <b>12 cm</b>"],
             "Diameter = 12 cm", "A diameter is 2 radii: 6 cm + 6 cm = 12 cm.",
             circ([{"t": "seg", "p": ["P", "O"]}, {"t": "dot", "p": "O"}, {"t": "len", "p": ["P", "O"], "s": "6 cm", "off": -14},
                   {"t": "pl", "p": "O", "d": [12, 20]}], {"P": polar(O, R, 200)}, fill=GREEN)))
check(24 / 2, 12, "p.30 Q2(b)")
q74.append(Q("Do and Learn 2 (b)", 30, "O is the center. Find the radius of the circle.<br>Radius = ___ cm",
             "The 24 cm line goes right across through O. Is it a radius or a diameter?",
             ["The 24 cm line goes across the circle through O, so the <b>diameter is 24 cm</b>.",
              "Radius = Diameter ÷ 2",
              "= 24 ÷ 2 = <b>12 cm</b>"],
             "Radius = 12 cm", "The radius is half of the diameter: 12 + 12 = 24.",
             circ([{"t": "seg", "p": ["P", "Q"]}, {"t": "dot", "p": "O"}, {"t": "len", "p": ["P", "Q"], "s": "24 cm", "off": -14},
                   {"t": "pl", "p": "O", "d": [0, 26]}], {"P": polar(O, R, 200), "Q": polar(O, R, 20)}, fill=PURPLE)))
check(2 * 13, 26, "p.30 Q3 W"); check(Fraction(13, 2), Fraction(13, 2), "p.30 Q3 X"); check(38 / 2, 19, "p.30 Q3 Y"); check(2 * 22, 44, "p.30 Q3 Z")
q74.append(Q("Do and Learn 3", 30,
             "What are the missing values in the table?<br><table class='t'><tr><th>Circle</th><th>Radius</th><th>Diameter</th></tr>"
             "<tr><td>W</td><td>13 cm</td><td>?</td></tr><tr><td>X</td><td>?</td><td>13 cm</td></tr>"
             "<tr><td>Y</td><td>?</td><td>38 cm</td></tr><tr><td>Z</td><td>22 cm</td><td>?</td></tr></table>",
             "Radius to diameter: × 2. Diameter to radius: ÷ 2.",
             ["W: Diameter = 2 × 13 = <b>26 cm</b>",
              "X: Radius = 13 ÷ 2 = <b>6½ cm</b> (half of 12 is 6, half of 1 is ½)",
              "Y: Radius = 38 ÷ 2 = <b>19 cm</b>",
              "Z: Diameter = 2 × 22 = <b>44 cm</b>"],
             "W: 26 cm, X: 6½ cm, Y: 19 cm, Z: 44 cm", "The diameter is always 2 times the radius."))

# Exercise p.31 Q1
f31 = circ([{"t": "seg", "p": ["A", "B"]}, {"t": "seg", "p": ["O", "C"]}, {"t": "seg", "p": ["D", "E"]}, {"t": "dot", "p": "O"},
            {"t": "txt", "at": [40, 40], "s": "1 ?", "size": 16, "bold": True, "color": "#EF6C00"},
            {"t": "seg", "p": [[58, 40], polar(O, R, 220)], "width": 1.5},
            {"t": "txt", "at": [40, 140], "s": "2 ?", "size": 16, "bold": True, "color": "#EF6C00"},
            {"t": "seg", "p": [[58, 136], lerp(polar(O, R, 110), polar(O, R, -70), 0.4)], "width": 1.5},
            {"t": "txt", "at": [110, 232], "s": "3 ?", "size": 16, "bold": True, "color": "#EF6C00"},
            {"t": "seg", "p": [[125, 220], lerp(polar(O, R, 40), polar(O, R, 140), 0.55)], "width": 1.5},
            {"t": "txt", "at": [290, 40], "s": "4 ?", "size": 16, "bold": True, "color": "#EF6C00"},
            {"t": "seg", "p": [[272, 40], lerp(O, polar(O, R, -20), 0.6)], "width": 1.5},
            {"t": "txt", "at": [292, 140], "s": "5 ?", "size": 16, "bold": True, "color": "#EF6C00"},
            {"t": "seg", "p": [[274, 136], [O[0] + 4, O[1] + 2]], "width": 1.5}],
           {"A": polar(O, R, 110), "B": polar(O, R, -70), "C": polar(O, R, -20), "D": polar(O, R, 40), "E": polar(O, R, 140)},
           fill="#FFF9C4", w=340, h=245, c=O)
q74.append(Q("Exercise 1", 31, "Use the words given to name the parts of a circle.<br>circumference · center · radius · diameter · chord",
             "A line through the center is special. A line from the center to the edge is special too.",
             ["Label 1 points to the line all the way around the circle: <b>circumference</b>.",
              "Label 2 points to the line across the circle through the center: <b>diameter</b> (it is also a chord).",
              "Label 3 points to a line joining 2 points on the edge, not through the center: <b>chord</b>.",
              "Label 4 points to the line from the center to the edge: <b>radius</b>.",
              "Label 5 points to the middle point: <b>center</b>."],
             "1 circumference, 2 diameter/chord, 3 chord, 4 radius, 5 center",
             "A diameter goes through the center, a radius starts at the center, and a chord joins any 2 points on the edge.", f31))

# p.31 Q2 (a)(b)(c)
f31a = circ([{"t": "seg", "p": ["A", "B"]}, {"t": "seg", "p": ["C", "O"]}, {"t": "seg", "p": ["E", "F"]}, {"t": "dot", "p": "O", "color": "#c62828"}]
            + [{"t": "pl", "p": n, "d": d} for n, d in [("O", [14, 10]), ("A", [2, -10]), ("B", [-8, 22]), ("C", [-10, -6]), ("E", [10, -8]), ("F", [8, 22])]],
            {"A": polar(O, R, -80), "B": polar(O, R, 100), "C": polar(O, R, -125), "E": polar(O, R, -55), "F": polar(O, R, 70)}, fill=GREEN)
q74.append(Q("Exercise 2 (a)", 31, "Fill in the blanks.<br>Center: ___<br>Diameter: ___<br>Radius: ___<br>Chord: ___ and ___",
             "Find the dot in the middle first. Then check which lines go through it.",
             ["The dot in the middle is <b>O</b>. That is the center.",
              "AB goes across the circle through O. So the diameter is <b>AB</b>.",
              "CO goes from the edge to the center. So the radius is <b>CO</b>.",
              "A chord joins 2 points on the edge: <b>EF</b> and <b>AB</b> (a diameter is also a chord)."],
             "Center: O; Diameter: AB; Radius: CO; Chord: EF and AB",
             "AB passes through O, so it is a diameter and also the longest chord.", f31a))
f31b = circ([{"t": "seg", "p": ["T", "U"]}, {"t": "seg", "p": ["S", "O"]}, {"t": "seg", "p": ["T", "P"]}, {"t": "dot", "p": "O", "color": "#c62828"}]
            + [{"t": "pl", "p": n, "d": d} for n, d in [("O", [6, 24]), ("S", [-10, -8]), ("U", [10, -8]), ("T", [-12, 18]), ("P", [14, 8])]],
            {"S": polar(O, R, -125), "U": polar(O, R, -50), "T": polar(O, R, 130), "P": polar(O, R, 10)}, fill=ORANGE)
q74.append(Q("Exercise 2 (b)", 31, "Fill in the blanks.<br>Center: ___<br>Diameter: ___<br>Radius: ___<br>Chord: ___ and ___",
             "Which line goes through O from one side to the other?",
             ["The dot in the middle is <b>O</b>. That is the center.",
              "TU goes across the circle through O. So the diameter is <b>TU</b>.",
              "SO goes from the edge to the center. So the radius is <b>SO</b>.",
              "The chords join 2 points on the edge: <b>TP</b> and <b>TU</b>."],
             "Center: O; Diameter: TU; Radius: SO; Chord: TP and TU",
             "TU passes through O, so it is a diameter and also a chord.", f31b))
Ac = O
Kc, Mc, Pc, Nc = polar(Ac, R, 200), polar(Ac, R, 20), polar(Ac, R, 135), polar(Ac, R, 75)


def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return [round(x1 + t * (x2 - x1), 1), round(y1 + t * (y2 - y1), 1)]


Uc = inter(Kc, Nc, Pc, Ac)
f31c = F(320, 240, {"A": Ac, "K": Kc, "M": Mc, "P": Pc, "N": Nc, "U": Uc}, [
    {"t": "circle", "c": "A", "r": R, "fill": "#FFF9C4"},
    {"t": "seg", "p": ["K", "M"]}, {"t": "seg", "p": ["P", "A"]}, {"t": "seg", "p": ["K", "N"]}, {"t": "dot", "p": "A", "color": "#c62828"}]
    + [{"t": "pl", "p": n, "d": d} for n, d in [("A", [4, -10]), ("K", [-14, 0]), ("M", [14, 14]), ("P", [-12, 18]), ("N", [8, 22]), ("U", [14, 12])]])
q74.append(Q("Exercise 2 (c)", 31, "Fill in the blanks.<br>Center: ___<br>Diameter: ___<br>Radius: ___<br>Chord: ___ and ___",
             "Careful! The center here is not called O. Find the dot in the middle.",
             ["The dot in the middle is <b>A</b>. That is the center.",
              "KM goes across the circle through A. So the diameter is <b>KM</b>.",
              "PA goes from the edge to the center. So the radius is <b>PA</b>.",
              "The chords join 2 points on the edge: <b>KN</b> and <b>KM</b>. (U is only where 2 lines cross, not on the edge.)"],
             "Center: A; Diameter: KM; Radius: PA; Chord: KN and KM",
             "KM passes through the center A, so it is a diameter and also a chord.", f31c))
q74.append(Q("Exercise 3", 32,
             "Fill in the blanks.<br>(a) ___ : The straight line joining any two points on the circumference of a circle<br>"
             "(b) ___ : The straight line joining the center and the circumference of a circle<br>"
             "(c) ___ : The distance around a circle<br>(d) ___ : The straight line that passes through the center of a circle<br>"
             "(e) ___ : The point in the middle of a circle",
             "Use the words: chord, radius, circumference, diameter, center.",
             ["(a) Any 2 points on the edge: <b>Chord</b>",
              "(b) From the center to the edge: <b>Radius</b>",
              "(c) All the way around: <b>Circumference</b>",
              "(d) Through the center: <b>Diameter</b>",
              "(e) The middle point: <b>Center</b>"],
             "(a) Chord (b) Radius (c) Circumference (d) Diameter (e) Center",
             "Each part of a circle has its own name."))
O4 = O
f32 = F(320, 240, {"A": O4, "B": polar(O4, R, 180), "C": polar(O4, R, 0), "D": polar(O4, R, -70), "E": polar(O4, R, 60), "F": polar(O4, R, 120)}, [
    {"t": "circle", "c": "A", "r": R, "fill": GREEN},
    {"t": "seg", "p": ["B", "C"]}, {"t": "seg", "p": ["A", "D"]}, {"t": "seg", "p": ["C", "E"]}, {"t": "seg", "p": ["B", "F"]}, {"t": "dot", "p": "A", "color": "#c62828"}]
    + [{"t": "pl", "p": n, "d": d} for n, d in [("A", [0, 24]), ("B", [-14, 6]), ("C", [14, 6]), ("D", [4, -8]), ("E", [6, 22]), ("F", [-6, 22])]])
q74.append(Q("Exercise 4", 32, "Draw the given parts of a circle. (Answers vary.)<br>Center: A<br>Diameter: BC<br>Radius: AD<br>Chord: CE and BF",
             "Mark the center A first. A diameter must pass through A.",
             ["Draw a circle. Mark the center and call it <b>A</b>.",
              "Draw a line across the circle through A. Call the ends <b>B</b> and <b>C</b>. That is the diameter BC.",
              "Draw a line from A to the edge. Call the end <b>D</b>. That is the radius AD.",
              "Mark points E and F on the edge. Join <b>C to E</b> and <b>B to F</b>. These are the chords CE and BF."],
             "One possible drawing is shown (answers vary)", "Any drawing is correct if BC goes through A, AD starts at A, and CE and BF join 2 points on the edge.", f32))

for lab, txt, d, key, fig_, hint in [
    ("Exercise 5 (a)", "O is the center and AB is the diameter of the circle. AB = 12 cm.", 12, 6, None, "AB is a diameter. Halve it."),
    ("Exercise 5 (b)", "O is the center and CD is the diameter of the circle. CD = 25 cm.", 25, 12.5, None, "CD is a diameter. Halve it."),
]:
    check(d / 2, key, f"p.33 {lab}")
    q74.append(Q(lab, 33, f"Find the radius of the circle.<br>{txt}<br>Radius = ___ cm", hint,
                 [f"The diameter is <b>{fmt(d)} cm</b>.", "Radius = Diameter ÷ 2", f"= {fmt(d)} ÷ 2 = <b>{fmt(key)} cm</b>"],
                 f"Radius = {fmt(key)} cm", f"{fmt(key)} + {fmt(key)} = {fmt(d)}, the diameter.",
                 circ([{"t": "seg", "p": ["P", "Q"]}, {"t": "dot", "p": "O"}, {"t": "len", "p": ["P", "Q"], "s": f"{fmt(d)} cm", "off": -14},
                       {"t": "pl", "p": "O", "d": [0, 26]}], {"P": polar(O, R, 210), "Q": polar(O, R, 30)}, fill=ORANGE if d == 12 else GREEN)))
check(18 / 2, 9, "p.33 Q5(c)")
fsq = F(320, 240, {"O": O, "a": [70, 30], "b": [250, 30], "c": [250, 210], "d": [70, 210]}, [
    {"t": "poly", "p": ["a", "b", "c", "d"], "fill": PURPLE}, {"t": "circle", "c": "O", "r": 90, "fill": "#FFF9C4"},
    {"t": "seg", "p": [[70, 18], [250, 18]], "width": 1.5}, {"t": "txt", "at": [160, 14], "s": "18 cm", "size": 16, "bold": True, "color": "#1565c0"}])
q74.append(Q("Exercise 5 (c)", 33, "Find the radius of the circle. The circle fits exactly inside a square of side 18 cm.<br>Radius = ___ cm",
             "The circle touches all 4 sides of the square. How wide is the circle?",
             ["The circle fits exactly inside the square, so the circle is as wide as the square.",
              "So the <b>diameter is 18 cm</b>.",
              "Radius = 18 ÷ 2 = <b>9 cm</b>"],
             "Radius = 9 cm", "The width of the square is the diameter of the circle.", fsq))
check(30 / 2, 15, "p.33 Q5(d)")
sqA, sqB, sqC, sqD = polar(O, R, 200), polar(O, R, -70), polar(O, R, 20), polar(O, R, 110)
fsd = F(320, 240, {"O": O, "A": sqA, "B": sqB, "C": sqC, "D": sqD}, [
    {"t": "circle", "c": "O", "r": R, "fill": PURPLE}, {"t": "poly", "p": ["A", "B", "C", "D"], "fill": "#FFE0B2"},
    {"t": "seg", "p": ["B", "D"], "dash": True}, {"t": "len", "p": ["D", "B"], "s": "30 cm", "off": 14},
    {"t": "pl", "p": "A", "d": [-14, 0]}, {"t": "pl", "p": "B", "d": [6, -8]}, {"t": "pl", "p": "C", "d": [14, 10]}, {"t": "pl", "p": "D", "d": [-4, 22]}])
q74.append(Q("Exercise 5 (d)", 33, "Find the radius of the circle. ABCD is a square in a circle. BD = 30 cm.<br>Radius = ___ cm",
             "BD goes from one corner of the square to the opposite corner. Does it go through the center of the circle?",
             ["The corners of the square are on the circle. BD joins opposite corners, so it goes through the center.",
              "So BD is a <b>diameter</b>: 30 cm.",
              "Radius = 30 ÷ 2 = <b>15 cm</b>"],
             "Radius = 15 cm", "The diagonal of the square passes through the center, so it is a diameter.", fsd))
check(32, 32, "p.33 Q6 OB"); check(2 * 32, 64, "p.33 Q6 CD")
f33 = circ([{"t": "seg", "p": ["O", "A"]}, {"t": "seg", "p": ["O", "B"]}, {"t": "seg", "p": ["C", "D"]}, {"t": "dot", "p": "O"},
            {"t": "len", "p": ["O", "A"], "s": "32 cm", "off": -14},
            {"t": "pl", "p": "O", "d": [-14, 20]}, {"t": "pl", "p": "A", "d": [14, 6]}, {"t": "pl", "p": "B", "d": [-12, 16]},
            {"t": "pl", "p": "C", "d": [0, -8]}, {"t": "pl", "p": "D", "d": [0, 24]}],
           {"A": polar(O, R, 0), "B": polar(O, R, 145), "C": polar(O, R, -90), "D": polar(O, R, 90)}, fill=ORANGE)
q74.append(Q("Exercise 6", 33, "O is the center of the circle. What are the lengths of OB and CD?<br>OA = 32 cm<br>OB = ___ cm<br>CD = ___ cm",
             "OA and OB are both radii. CD goes through O.",
             ["OA goes from the center to the edge, so the <b>radius is 32 cm</b>.",
              "OB is also a radius. So OB = <b>32 cm</b>.",
              "CD goes across through O, so it is a diameter.",
              "CD = 2 × 32 = <b>64 cm</b>"],
             "OB = 32 cm, CD = 64 cm", "All radii are equal, and a diameter is 2 radii.", f33))
check(60, 60, "p.33 Q7 diameter"); check(60 / 2, 30, "p.33 Q7 radius")
spokes = [{"t": "seg", "p": [O, polar(O, 80, a)], "width": 1.2} for a in range(0, 360, 20)]
fwheel = F(320, 240, {"O": O}, [{"t": "circle", "c": "O", "r": 92, "fill": "#E3F2FD"}, {"t": "circle", "c": "O", "r": 80}] + spokes + [
    {"t": "seg", "p": [[50, 28], [50, 212]], "width": 2}, {"t": "seg", "p": [[50, 28], [160, 28]], "dash": True, "width": 1.5},
    {"t": "seg", "p": [[50, 212], [160, 212]], "dash": True, "width": 1.5}, {"t": "txt", "at": [36, 126], "s": "h", "size": 20, "bold": True}])
q74.append(Q("Exercise 7", 33, "What are the lengths of the diameter and radius of the wheel?<br>h = 60 cm<br>diameter = ___ cm<br>radius = ___ cm",
             "h is the height of the wheel from the very bottom to the very top.",
             ["h goes from the bottom of the wheel to the top, straight through the middle. That is the <b>diameter</b>.",
              "So the diameter = <b>60 cm</b>.",
              "Radius = 60 ÷ 2 = <b>30 cm</b>"],
             "diameter = 60 cm, radius = 30 cm", "The height of a wheel is the same as its diameter.", fwheel))

for lab, txt, r, key, fill in [("Exercise 8 (a)", "OH is the radius of the circle. OH = 10 cm.", 10, 20, BLUE),
                                ("Exercise 8 (b)", "OR is the radius of the circle. OR = 14.5 cm.", 14.5, 29, ORANGE),
                                ("Exercise 8 (c)", "O is the center of the circle. The radius is 12 cm.", 12, 24, GREEN)]:
    check(2 * r, key, f"p.34 {lab}")
    q74.append(Q(lab, 34, f"Find the diameter of the circle.<br>{txt}<br>Diameter = ___ cm", "Diameter = 2 × Radius",
                 [f"The radius is <b>{fmt(r)} cm</b>.", "Diameter = 2 × Radius", f"= 2 × {fmt(r)} = <b>{fmt(key)} cm</b>"],
                 f"Diameter = {fmt(key)} cm", f"{fmt(r)} + {fmt(r)} = {fmt(key)}.",
                 circ([{"t": "seg", "p": ["O", "P"]}, {"t": "dot", "p": "O"}, {"t": "len", "p": ["O", "P"], "s": f"{fmt(r)} cm", "off": -14},
                       {"t": "pl", "p": "O", "d": [-14, -4]}], {"P": polar(O, R, 110 if r == 10 else 180 if r == 14.5 else 0)}, fill=fill)))
check(3.5 + 3.5, 7, "p.34 Q8(d)")
P8, Q8, R8, S8 = polar(O, R, -110), polar(O, R, -20), polar(O, R, 70), polar(O, R, 160)
f34d = F(320, 240, {"O": O, "P": P8, "Q": Q8, "R": R8, "S": S8}, [
    {"t": "circle", "c": "O", "r": R, "fill": "#FFF9C4"}, {"t": "poly", "p": ["P", "Q", "R", "S"], "fill": "#FFE0B2"},
    {"t": "seg", "p": ["P", "R"], "dash": True}, {"t": "seg", "p": ["S", "Q"], "dash": True},
    {"t": "len", "p": ["P", "O"], "s": "3.5 cm", "off": -14, "size": 14}, {"t": "len", "p": ["O", "Q"], "s": "3.5 cm", "off": -14, "size": 14},
    {"t": "ra", "v": "O", "a": "P", "b": "Q", "size": 10}]
    + [{"t": "pl", "p": n, "d": d} for n, d in [("P", [-6, -8]), ("Q", [14, 0]), ("R", [6, 22]), ("S", [-14, 10])]])
q74.append(Q("Exercise 8 (d)", 34, "Find the diameter of the circle. PQRS is a square in a circle. The 2 halves of the diagonal measure 3.5 cm each.<br>Diameter = ___ cm",
             "The corners of the square sit on the circle. A diagonal goes through the center.",
             ["The diagonal PR of the square goes through the center O, so it is a diameter.",
              "Each half of the diagonal is a radius: <b>3.5 cm</b>.",
              "Diameter = 3.5 + 3.5 = <b>7 cm</b>"],
             "Diameter = 7 cm", "The diagonal of the square is a diameter of the circle.", f34d))
check(2 * 4, 8, "p.34 Q9 row1"); check(2 * 9.5, 19, "p.34 Q9 row2"); check(40 / 2, 20, "p.34 Q9 row3"); check(28.6 / 2, 14.3, "p.34 Q9 row4")
q74.append(Q("Exercise 9", 34,
             "Complete the table.<br><table class='t'><tr><th>Radius</th><th>Diameter</th></tr><tr><td>4 cm</td><td>?</td></tr>"
             "<tr><td>9.5 cm</td><td>?</td></tr><tr><td>?</td><td>40 cm</td></tr><tr><td>?</td><td>28.6 cm</td></tr></table>",
             "Radius to diameter: × 2. Diameter to radius: ÷ 2.",
             ["Row 1: Diameter = 2 × 4 = <b>8 cm</b>",
              "Row 2: Diameter = 2 × 9.5 = <b>19 cm</b> (9 × 2 = 18, 0.5 × 2 = 1, 18 + 1 = 19)",
              "Row 3: Radius = 40 ÷ 2 = <b>20 cm</b>",
              "Row 4: Radius = 28.6 ÷ 2 = <b>14.3 cm</b> (28 ÷ 2 = 14, 0.6 ÷ 2 = 0.3)"],
             "8 cm, 19 cm, 20 cm, 14.3 cm", "The diameter is always double the radius."))

flash74 = [
    {"front": "Center", "back": "The point in the middle of a circle"},
    {"front": "Radius", "back": "A straight line from the center to the circumference"},
    {"front": "Diameter", "back": "A straight line through the center, joining 2 points on the circumference"},
    {"front": "Chord", "back": "A straight line joining any 2 points on the circumference"},
    {"front": "Circumference", "back": "The distance around a circle"},
    {"front": "Radii", "back": "More than one radius"},
    {"front": "Diameter = ?", "back": "2 × Radius"},
    {"front": "Radius = ?", "back": "Diameter ÷ 2"},
    {"front": "The longest chord of a circle", "back": "The diameter"},
    {"front": "Radius 9 cm. Diameter?", "back": "2 × 9 = 18 cm"},
    {"front": "Diameter 50 cm. Radius?", "back": "50 ÷ 2 = 25 cm"},
]
check(2 * 9, 18, "flash 7.4"); check(50 / 2, 25, "flash 7.4")
match74 = [["Center", "Middle point"], ["Radius", "Center to edge"], ["Diameter", "Edge to edge through center"],
           ["Chord", "Joins 2 points on the edge"], ["Circumference", "Distance around"], ["Radius 6 cm", "Diameter 12 cm"],
           ["Diameter 30 cm", "Radius 15 cm"], ["Radius 2.5 cm", "Diameter 5 cm"]]
check(2 * 6, 12, "match 7.4"); check(30 / 2, 15, "match 7.4"); check(2 * 2.5, 5, "match 7.4")
quiz74 = [
    {"q": "A circle has a radius of 7 cm. What is its diameter?", "options": ["14 cm", "3.5 cm", "7 cm", "21 cm"]},
    {"q": "A circle has a diameter of 18 cm. What is its radius?", "options": ["9 cm", "36 cm", "18 cm", "6 cm"]},
    {"q": "A circle has a radius of 4.5 cm. What is its diameter?", "options": ["9 cm", "8.5 cm", "2.25 cm", "4.5 cm"]},
    {"q": "A circle has a diameter of 25 cm. What is its radius?", "options": ["12.5 cm", "50 cm", "12 cm", "13 cm"]},
    {"q": "A line from the center to the edge of a circle is a…", "options": ["Radius", "Diameter", "Chord", "Circumference"]},
    {"q": "A line joining any 2 points on the edge is a…", "options": ["Chord", "Radius", "Center", "Circumference"]},
    {"q": "The distance around a circle is the…", "options": ["Circumference", "Diameter", "Radius", "Chord"]},
    {"q": "Which is the longest chord of a circle?", "options": ["The diameter", "The radius", "Any chord", "The circumference"]},
    {"q": "A wheel is 80 cm tall. What is its radius?", "options": ["40 cm", "80 cm", "160 cm", "20 cm"]},
    {"q": "A circle fits exactly inside a square of side 10 cm. What is the radius?", "options": ["5 cm", "10 cm", "20 cm", "2.5 cm"]},
    {"q": "OA and OB are radii of the same circle. OA = 11 cm. What is OB?", "options": ["11 cm", "22 cm", "5.5 cm", "We cannot tell"]},
]
check(2 * 7, 14, "quiz 7.4"); check(18 / 2, 9, "quiz 7.4"); check(2 * 4.5, 9, "quiz 7.4"); check(25 / 2, 12.5, "quiz 7.4")
check(80 / 2, 40, "quiz 7.4"); check(10 / 2, 5, "quiz 7.4")

sections.append({"id": "7-4", "title": "Parts of a Circle", "short": "4. Parts of a Circle", "pages": "p.28 to 34",
                 "learn": learn74, "questions": q74, "flash": flash74, "match": match74, "quiz": quiz74})

# ==================================================================
# 7.5 DRAWING CIRCLES  (p.35 to 40)
# ==================================================================


def drawn_circle(r_cm, label, extra=(), pts=None, scale=24):
    c = [160, 120]
    p = {label: c}
    if pts:
        p.update(pts)
    r = r_cm * scale
    edge = polar(c, r, -30)
    p["_e"] = edge
    items = [{"t": "circle", "c": label, "r": r, "fill": "#F3E5F5"}, {"t": "dot", "p": label},
             {"t": "seg", "p": [label, "_e"], "dash": True}, {"t": "len", "p": [label, "_e"], "s": f"{fmt(r_cm)} cm", "off": -14, "size": 15},
             {"t": "pl", "p": label, "d": [0, 24]}]
    return F(320, 240, p, items + list(extra))


compass_fig = F(320, 220, {"N": [120, 190], "P": [210, 190], "T": [165, 30]}, [
    {"t": "seg", "p": ["T", "N"], "width": 5, "color": "#546e7a"}, {"t": "seg", "p": ["T", "P"], "width": 5, "color": "#546e7a"},
    {"t": "circle", "c": "T", "r": 10, "fill": "#90a4ae"},
    {"t": "txt", "at": [85, 205], "s": "needle", "size": 16, "bold": True}, {"t": "txt", "at": [255, 205], "s": "pencil", "size": 16, "bold": True},
    {"t": "seg", "p": [[110, 200], [230, 200]], "dash": True, "color": "#1565c0"}, {"t": "txt", "at": [165, 218], "s": "radius", "size": 15, "color": "#1565c0", "bold": True}])
learn75 = [
    L("Idea", "Using a compass",
      "<p>A compass has a <b>needle</b> and a <b>pencil</b>. The gap between them is the <b>radius</b> of the circle.</p>"
      "<p>Use a ruler to set the gap.</p>", compass_fig, 35),
    L("Example", "Draw a circle with radius 1 cm",
      "<p><b>Step 1:</b> Mark O as the center.<br><b>Step 2:</b> Open the compass to 1 cm using a ruler.<br>"
      "<b>Step 3:</b> Put the needle on O and the pencil on the paper. Turn the compass.<br><b>Step 4:</b> Keep turning until the circle is complete.</p>",
      drawn_circle(1, "O", scale=60), 35),
    L("Idea", "Given the diameter? Find the radius first!",
      "<p>A compass is set to the <b>radius</b>, not the diameter.</p><p><b>Radius = Diameter ÷ 2</b></p>", None, 36),
    L("Example", "Draw a circle with diameter 4 cm",
      "<p>Radius = 4 ÷ 2 = <b>2 cm</b>.</p><p>Mark O. Open the compass to 2 cm. Put the needle on O and turn the compass all the way round.</p>"
      "<p>Make sure the circle joins up completely.</p>", drawn_circle(2, "O", scale=40), 36),
    L("Idea", "A string and a pin",
      "<p>Tie a string to a pin and a pencil. Hold the pin still and pull the string tight. Go round the pin with the pencil.</p>"
      "<p>The <b>length of the string</b> is the <b>radius</b>. (Be careful: pins are sharp!)</p>", None, 37),
]
check(4 / 2, 2, "p.36 example")

q75 = []


def circle_q(label, page, q, hint, steps, ans, why, fig):
    return Q(label, page, q, hint, steps, ans, why, fig)


q75.append(circle_q("Do and Learn", 37, "Draw a circle O in which its radius is 3 cm long.", "The compass gap is the radius.",
                    ["Mark a point and call it <b>O</b>. This is the center.",
                     "Use a ruler to open the compass to <b>3 cm</b>.",
                     "Put the needle on O. Turn the compass all the way round to draw the circle."],
                    "A circle with center O and radius 3 cm", "Every point on the circle is 3 cm from O.", drawn_circle(3, "O", scale=28)))
q75.append(circle_q("Exercise 1", 38, "Draw a circle A in which its radius is 2.5 cm long.", "Open the compass to the radius.",
                    ["Mark a point and call it <b>A</b>. This is the center.",
                     "Use a ruler to open the compass to <b>2.5 cm</b> (2 and a half cm).",
                     "Put the needle on A. Turn the compass all the way round."],
                    "A circle with center A and radius 2.5 cm", "The compass gap is the radius, 2.5 cm.", drawn_circle(2.5, "A", scale=32)))
check(7 / 2, 3.5, "p.38 Q2")
q75.append(circle_q("Exercise 2", 38, "Draw a circle B in which its diameter is 7 cm long.", "You are given the diameter. Find the radius first.",
                    ["Find the radius: 7 ÷ 2 = <b>3.5 cm</b>.",
                     "Mark the center <b>B</b>.",
                     "Open the compass to <b>3.5 cm</b>. Put the needle on B and draw the circle.",
                     "Check: measure across the circle through B. It should be 7 cm."],
                    "A circle with center B and radius 3.5 cm (diameter 7 cm)", "Radius = 7 ÷ 2 = 3.5 cm.", drawn_circle(3.5, "B", scale=26)))
fAB = drawn_circle(4, "E", scale=22)
fAB["items"] += [{"t": "seg", "p": [[30, 12], [118, 12]]}, {"t": "txt", "at": [22, 18], "s": "A", "size": 16, "bold": True},
                 {"t": "txt", "at": [128, 18], "s": "B", "size": 16, "bold": True}]
q75.append(circle_q("Exercise 3", 39, "Draw a circle E in which its radius is equal to AB. (Measure AB in your book. It is 4 cm.)",
                    "Measure AB first. That length is the radius.",
                    ["Measure AB with your ruler. AB = <b>4 cm</b>.",
                     "The radius must be equal to AB, so the radius is <b>4 cm</b>.",
                     "Mark the center <b>E</b>. Open the compass to 4 cm and draw the circle."],
                    "A circle with center E and radius 4 cm", "The radius is the same length as AB.", fAB))
check(6 / 2, 3, "p.39 Q4")
fGD = drawn_circle(3, "F", scale=28)
fGD["items"] += [{"t": "seg", "p": [[20, 12], [152, 12]]}, {"t": "txt", "at": [12, 18], "s": "G", "size": 16, "bold": True},
                 {"t": "txt", "at": [162, 18], "s": "D", "size": 16, "bold": True}]
q75.append(circle_q("Exercise 4", 39, "Draw a circle F in which its diameter is equal to GD. (Measure GD in your book. It is 6 cm.)",
                    "GD is the diameter. The compass needs the radius.",
                    ["Measure GD with your ruler. GD = <b>6 cm</b>. This is the diameter.",
                     "Radius = 6 ÷ 2 = <b>3 cm</b>.",
                     "Mark the center <b>F</b>. Open the compass to 3 cm and draw the circle."],
                    "A circle with center F and radius 3 cm (diameter 6 cm)", "The diameter is GD = 6 cm, so the radius is 3 cm.", fGD))
check(8 / 2, 4, "p.40 Q5")
c5 = [160, 120]
f40a = F(320, 240, {"E": c5, "A": [160 - 96, 120], "B": [160 + 96, 120]}, [
    {"t": "circle", "c": "E", "r": 96, "fill": "#F3E5F5"}, {"t": "seg", "p": ["A", "B"]}, {"t": "dot", "p": "E"},
    {"t": "len", "p": ["A", "B"], "s": "8 cm", "off": -14},
    {"t": "pl", "p": "A", "d": [-12, 6]}, {"t": "pl", "p": "B", "d": [12, 6]}, {"t": "pl", "p": "E", "d": [0, 24]}])
q75.append(circle_q("Exercise 5", 40, "Create a straight line AB of 8 cm long. Then draw a circle in which its center is E and its diameter is AB.",
                    "The center of a diameter is exactly in the middle of it.",
                    ["Draw a straight line <b>AB = 8 cm</b>.",
                     "AB is the diameter, so the center is in the middle. Measure 4 cm from A and mark <b>E</b>.",
                     "Radius = 8 ÷ 2 = <b>4 cm</b>.",
                     "Open the compass to 4 cm. Put the needle on E and draw the circle. It passes through A and B."],
                    "A circle with center E (the middle of AB) and radius 4 cm", "E is the middle of the diameter AB, so EA = EB = 4 cm.", f40a))
check(4 / 2, 2, "p.40 Q6")
c6 = [160, 120]
s6 = 2 * 45
f40b = F(320, 240, {"O": c6, "P": [160, 120 - s6], "Q": [160 + s6, 120], "R": [160, 120 + s6], "S": [160 - s6, 120]}, [
    {"t": "circle", "c": "O", "r": s6, "fill": "#F3E5F5"}, {"t": "poly", "p": ["P", "Q", "R", "S"], "fill": "#FFE0B2"},
    {"t": "seg", "p": ["P", "R"]}, {"t": "seg", "p": ["S", "Q"]}, {"t": "dot", "p": "O"},
    {"t": "len", "p": ["S", "Q"], "s": "4 cm", "off": 16}, {"t": "pl", "p": "O", "d": [12, -6]}])
q75.append(circle_q("Exercise 6", 40, "Draw a square in which its diagonals are 4 cm long. With O as the center, draw a circle such that its circumference meets all four vertices of the square.",
                    "The diagonals of a square cross in the middle at right angles. Each half is 2 cm.",
                    ["Draw 2 lines of <b>4 cm</b> that cross in the middle at right angles. Mark the middle point <b>O</b>.",
                     "Join the 4 ends. This is the square.",
                     "From O to each corner is half a diagonal: 4 ÷ 2 = <b>2 cm</b>. This is the radius.",
                     "Open the compass to 2 cm. Put the needle on O and draw the circle. It passes through all 4 corners."],
                    "A circle with center O and radius 2 cm passing through the 4 corners of the square",
                    "Each corner is 2 cm from O, so a circle of radius 2 cm touches all 4 corners.", f40b))

flash75 = [
    {"front": "Compass", "back": "A tool with a needle and a pencil for drawing circles"},
    {"front": "The compass gap is the…", "back": "Radius"},
    {"front": "Given a diameter of 10 cm, set the compass to…", "back": "5 cm (10 ÷ 2)"},
    {"front": "Where does the needle go?", "back": "On the center of the circle"},
    {"front": "String and pin: the string length is the…", "back": "Radius"},
    {"front": "Center of a diameter AB", "back": "Exactly in the middle of AB"},
    {"front": "Diameter 7 cm. Compass gap?", "back": "3.5 cm"},
    {"front": "Last step of drawing a circle", "back": "Keep turning until the circle joins up completely"},
]
check(10 / 2, 5, "flash 7.5"); check(7 / 2, 3.5, "flash 7.5")
match75 = [["Diameter 8 cm", "Compass 4 cm"], ["Diameter 5 cm", "Compass 2.5 cm"], ["Radius 3 cm", "Compass 3 cm"],
           ["Diameter 12 cm", "Compass 6 cm"], ["Diameter 9 cm", "Compass 4.5 cm"], ["Needle", "Goes on the center"],
           ["Pencil", "Draws the circumference"], ["String length", "Radius"]]
check(8 / 2, 4, "m"); check(5 / 2, 2.5, "m"); check(12 / 2, 6, "m"); check(9 / 2, 4.5, "m")
quiz75 = [
    {"q": "You want a circle with diameter 6 cm. Open the compass to…", "options": ["3 cm", "6 cm", "12 cm", "2 cm"]},
    {"q": "You want a circle with radius 5 cm. Open the compass to…", "options": ["5 cm", "10 cm", "2.5 cm", "15 cm"]},
    {"q": "You want a circle with diameter 9 cm. Open the compass to…", "options": ["4.5 cm", "9 cm", "18 cm", "4 cm"]},
    {"q": "Where do you put the needle of the compass?", "options": ["On the center", "On the circumference", "Anywhere", "On the diameter's end"]},
    {"q": "The gap between the needle and the pencil is the…", "options": ["Radius", "Diameter", "Chord", "Circumference"]},
    {"q": "AB is a diameter of 10 cm. Where is the center E?", "options": ["5 cm from A", "10 cm from A", "At A", "2 cm from A"]},
    {"q": "A square has diagonals of 4 cm. The circle through its corners has radius…", "options": ["2 cm", "4 cm", "8 cm", "1 cm"]},
    {"q": "With a string and a pin, the string length is the circle's…", "options": ["Radius", "Diameter", "Circumference", "Center"]},
    {"q": "You want a circle with diameter 13 cm. Open the compass to…", "options": ["6.5 cm", "13 cm", "26 cm", "6 cm"]},
    {"q": "Which tool is best for drawing a circle?", "options": ["Compass", "Protractor", "Set square", "Ruler only"]},
]
check(6 / 2, 3, "q"); check(9 / 2, 4.5, "q"); check(10 / 2, 5, "q"); check(4 / 2, 2, "q"); check(13 / 2, 6.5, "q")

sections.append({"id": "7-5", "title": "Drawing Circles", "short": "5. Drawing Circles", "pages": "p.35 to 40",
                 "learn": learn75, "questions": q75, "flash": flash75, "match": match75, "quiz": quiz75})

# ==================================================================
# UNIT 7 CHALLENGE  (p.41 to 46)
# ==================================================================
C41, B41 = [60, 220], [260, 220]
A41 = apex(C41, B41, 70, 70)
D41 = apex(C41, B41, 60, 60)
f41 = F(320, 250, {"A": A41, "B": B41, "C": C41, "D": D41}, [
    {"t": "poly", "p": ["A", "C", "B"], "fill": PURPLE}, {"t": "poly", "p": ["D", "C", "B"], "fill": ORANGE},
    {"t": "tick", "p": ["A", "C"], "n": 2}, {"t": "tick", "p": ["A", "B"], "n": 2},
    {"t": "tick", "p": ["D", "C"]}, {"t": "tick", "p": ["D", "B"]}, {"t": "tick", "p": ["C", "B"]},
    {"t": "ang", "v": "A", "a": "C", "b": "B", "s": "40°", "r": 30},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [12, 10]}, {"t": "pl", "p": "C", "d": [-12, 10]}, {"t": "pl", "p": "D", "d": [0, -8]}])
check(180 - 40, 140, "p.41 step"); check(140 / 2, 70, "p.41 ACB"); check(70 - 60, 10, "p.41")
# Problem solving p.43
A43, C43, D43 = [190, 20], [60, 300], [300, 300]
check(180 - 36 - 64, 80, "p.43 angle ADC")
check(180 - 36 - 64 - 38, 42, "p.44 BDC")
check(180 - 64 - 42, 74, "p.44 CBD")
check(180 - 38 - 74, 68, "p.44 ABE")
check(38 + 38, 76, "p.44 BEA")
check(76 + 36 + 68, 180, "p.44 check")
# draw: B on AC, E on AD with angle EBD = BDE = 38
B43 = lerp(A43, C43, 0.55)
dirBD = math.atan2(D43[1] - B43[1], D43[0] - B43[0])
a_be = dirBD - math.radians(38)
# intersect ray from B (angle a_be) with AD
ux, uy = math.cos(a_be), math.sin(a_be)
E43 = inter(B43, [B43[0] + ux, B43[1] + uy], A43, D43)
f43 = F(340, 330, {"A": A43, "B": B43, "C": C43, "D": D43, "E": E43}, [
    {"t": "poly", "p": ["A", "C", "D"], "fill": BLUE}, {"t": "seg", "p": ["B", "E"]}, {"t": "seg", "p": ["B", "D"]},
    {"t": "tick", "p": ["B", "E"]}, {"t": "tick", "p": ["E", "D"]},
    {"t": "ang", "v": "A", "a": "C", "b": "D", "s": "36°", "r": 34},
    {"t": "ang", "v": "C", "a": "A", "b": "D", "s": "64°", "r": 26},
    {"t": "ang", "v": "B", "a": "E", "b": "D", "s": "38°", "r": 36, "lr": 18},
    {"t": "pl", "p": "A", "d": [0, -8]}, {"t": "pl", "p": "B", "d": [-14, 0]}, {"t": "pl", "p": "C", "d": [-12, 12]},
    {"t": "pl", "p": "D", "d": [12, 12]}, {"t": "pl", "p": "E", "d": [14, 0]}])
qch = [
    Q("Let's Think Along", 41, "The figure shows 2 triangles. ABC is an isosceles triangle and DBC is an equilateral triangle. Find ∠ACD.",
      "∠ACD = ∠ACB - ∠DCB. Find both angles.",
      ["ABC is isosceles, so ∠ACB = ∠ABC.",
       "∠ACB + ∠ABC = 180° - 40° = <b>140°</b>",
       "∠ACB = 140° ÷ 2 = <b>70°</b>",
       "DBC is equilateral, so ∠DCB = <b>60°</b>.",
       "∠ACD = 70° - 60° = <b>10°</b>"],
      "∠ACD = 10°", "∠ACB (70°) is made of ∠ACD and ∠DCB (60°): 10° + 60° = 70°.", f41),
    Q("Problem Solving", 43, "In the figure below, ABC and AED are straight lines and BE = ED. Find ∠ABE.",
      "BE = ED, so triangle BED is isosceles. Use the angle sum of the big triangle ACD.",
      ["<b>Understand:</b> We know ∠A = 36°, ∠C = 64° and ∠EBD = 38°. We must find ∠ABE.",
       "BE = ED, so the angles opposite them are equal: <b>∠BDE = ∠EBD = 38°</b>.",
       "In the big triangle ACD: ∠ADC = 180° - 36° - 64° = 80°. So ∠BDC = 80° - 38° = <b>42°</b>.",
       "In triangle BCD: ∠CBD = 180° - 64° - 42° = <b>74°</b>.",
       "ABC is a straight line (180°): ∠ABE = 180° - 38° - 74° = <b>68°</b>.",
       "<b>Check:</b> ∠BEA = 38° + 38° = 76°. In triangle ABE: 76° + 36° + 68° = 180° ✓"],
      "∠ABE = 68°", "The angles on the straight line ABC add up to 180°: 68° + 38° + 74° = 180°.", f43),
    Q("Math Journal", 45,
      "Siti: Can I draw a triangle that has 1 obtuse angle and 2 acute angles?<br>"
      "Janice: Can I draw a triangle that has 1 obtuse angle and 1 right angle?<br>"
      "Peter: Can I draw a triangle that has 2 right angles?<br>Which child will be able to draw his or her triangle? Draw figures to help you explain the reasons.",
      "The 3 angles must add up to exactly 180°. Try some numbers.",
      ["Siti: try 120°, 30° and 30°. 120° + 30° + 30° = 180° ✓. So <b>Siti can</b> draw it.",
       "Janice: an obtuse angle is more than 90°. Add a right angle: more than 90° + 90° = more than 180°. That is too much. <b>Janice cannot</b>.",
       "Peter: 90° + 90° = 180° already. The third angle would be 0°. <b>Peter cannot</b>.",
       "In a right triangle, the other 2 angles add up to 90°, so they must both be acute."],
      "Only Siti can draw her triangle.",
      "The angle sum of a triangle is 180°. Janice's and Peter's triangles would need more than 180°.", obtuse_ex),
]
flash_ch = flash71[:6] + flash72[:4] + flash74[:6]
match_ch = [["Equilateral", "3 equal sides"], ["Isosceles", "2 equal sides"], ["Angle sum", "180°"],
            ["Right triangle", "One 90° angle"], ["Diameter", "2 × Radius"], ["Radius", "Diameter ÷ 2"],
            ["Chord", "Joins 2 points on the edge"], ["Compass", "Draws circles"]]
quiz_ch = [quiz71[0], quiz71[5], quiz72[0], quiz72[6], quiz72[9], quiz73[3], quiz74[0], quiz74[1], quiz74[5], quiz75[0],
           {"q": "ABC is isosceles with ∠A = 40°. DBC is equilateral inside it. What is ∠ACD?", "options": ["10°", "70°", "60°", "20°"]},
           {"q": "Can a triangle have 1 obtuse angle and 1 right angle?", "options": ["No, the sum would be more than 180°", "Yes", "Only if it is isosceles", "Only if it is small"]}]
sections.append({"id": "7-ch", "title": "Unit 7 Challenge", "short": "⭐ Challenge", "pages": "p.41 to 46",
                 "learn": [
                     L("Idea", "Unit 7 big ideas",
                       "<p>Sides: <b>equilateral</b> (3 equal), <b>isosceles</b> (2 equal), <b>scalene</b> (none equal).</p>"
                       "<p>Angles: <b>acute</b> (all less than 90°), <b>right</b> (one 90°), <b>obtuse</b> (one more than 90°).</p>", None, 46),
                     L("Idea", "Angle facts",
                       "<p>The angles of a triangle add up to <b>180°</b>. Angles on a straight line add up to <b>180°</b>.</p>"
                       "<p>In a right triangle, the other 2 angles add up to <b>90°</b>.</p>", None, 46),
                     L("Idea", "Circle facts",
                       "<p><b>Diameter = 2 × Radius</b> and <b>Radius = Diameter ÷ 2</b>. Set the compass to the radius.</p>", None, 46),
                     L("Example", "Problem solving plan",
                       "<p><b>Understand:</b> What is given? What must I find?<br><b>Plan:</b> Which facts can I use?<br>"
                       "<b>Solve:</b> Work step by step.<br><b>Check:</b> Do the angles add up to 180°?</p>", None, 43),
                 ],
                 "questions": qch, "flash": flash_ch, "match": match_ch, "quiz": quiz_ch})

unit = {"unit": "07", "title": "2D Shapes", "pages": "p.1 to 46", "sections": sections}

# ------------------------------------------------------------------
# Expected guided-answer pages (Do and Learn + Exercise + end pages)
# ------------------------------------------------------------------
unit["expectedPages"] = {
    "7-1": [8, 9, 10, 11, 12], "7-2": [16, 17, 18, 19, 20], "7-3": [24, 25, 26, 27],
    "7-4": [30, 31, 32, 33, 34], "7-5": [37, 38, 39, 40], "7-ch": [41, 43, 45],
}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written. Add these to content/CHECK-ME.md:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)

out = os.path.join(os.path.dirname(__file__), "..", "content", "unit07.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit07.json ({n} guided questions, {len(sections)} sections).")
