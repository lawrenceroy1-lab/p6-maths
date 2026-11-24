"""Builds content/unit10.json for Unit 10: Area and Perimeter of Polygons (book pages 105 to 146).

Every angle, perimeter and area is calculated here and compared with the answer key using check().
Run:  python3 tools/build_unit10.py
"""
import contextlib
import io
import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, PROBLEMS  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    from build_unit09 import FIG, poly, seg, lab, ra, tick, txt, grid_fig, num, Q, L  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
SQ = "²"
D = "°"


def ang(v, a, b, s, r=24, lr=None):
    d = {"t": "ang", "v": v, "a": a, "b": b, "s": s, "r": r}
    if lr:
        d["lr"] = lr
    return d


def half(x):
    return Fraction(str(x)) / 2


def angle_steps(lines, ans_label, ans, why, q, page, label, fig, hint):
    return Q(label, page, q, hint, lines, ans_label, why, fig)


def reg(n, cx, cy, r, start=-90):
    return [[round(cx + r * math.cos(math.radians(start + 360 * k / n)), 1), round(cy + r * math.sin(math.radians(start + 360 * k / n)), 1)] for k in range(n)]


sections = []


def off(pts, dx, dy, k=1.0):
    return [[round(dx + x * k, 1), round(dy + y * k, 1)] for x, y in pts]


def outline(pts, fill, labels=(), ticks=()):
    """pts: list of [x, y]; labels: (i, j, text); ticks: (i, j, n)."""
    items = [poly(pts, fill)]
    for i, j, t in labels:
        items.append(lab(pts[i], pts[j], t))
    for i, j, n in ticks:
        items.append(tick(pts[i], pts[j], n))
    return items

# ==================================================================
# 10.1 INTERIOR ANGLES OF POLYGONS (p.106 to 117, with Let's Recall)
# ==================================================================
for n, s in [(4, 360), (5, 540), (6, 720), (8, 1080)]:
    check((n - 2) * 180, s, f"p.108 sum {n}")
pent = reg(5, 160, 120, 90)
fsum = FIG({"A": pent[0], "B": pent[1], "C": pent[2], "D": pent[3], "E": pent[4]},
           [poly(["A", "B", "C", "D", "E"], GREEN), seg("A", "C", True), seg("A", "D", True)])
fpar = FIG({"A": [80, 40], "B": [280, 40], "C": [240, 180], "D": [40, 180]},
           [poly(["A", "B", "C", "D"], BLUE), ang("A", "D", "B", "140°", 22), ang("B", "A", "C", "b", 22), ang("C", "B", "D", "c", 22), ang("D", "C", "A", "d", 22)])
fkite = FIG({"A": [160, 30], "B": [250, 100], "C": [160, 210], "D": [70, 100]},
            [poly(["A", "B", "C", "D"], PINK), ang("B", "A", "C", "120°", 20), ang("D", "C", "A", "120°", 20), ra("A", "B", "D"), ang("C", "D", "B", "x", 30)])
check(180 - 140, 40, "p.110 b"); check(360 - 90 - 120 - 120, 30, "p.111 x")
learn101 = [
    L("Idea", "Angles in a triangle (recall)", "<p>The 3 angles of a triangle add up to <b>180°</b>.</p><p>Equilateral: each angle 60°. Isosceles: 2 equal angles. Right triangle: the other 2 angles add up to 90°.</p>", None, 109),
    L("Idea", "Sum of interior angles", "<p>Cut a polygon into triangles from one corner. Each triangle gives 180°.</p>"
      "<p>Quadrilateral (4 sides): 2 triangles → <b>360°</b><br>Pentagon (5): 3 triangles → <b>540°</b><br>Hexagon (6): 4 triangles → <b>720°</b><br>Octagon (8): 6 triangles → <b>1,080°</b></p>", fsum, 108),
    L("Example", "Why a pentagon is 540°", "<p>From corner A, draw lines to C and D. The pentagon splits into <b>3 triangles</b>.</p><p>3 × 180° = <b>540°</b></p>", fsum, 108),
    L("Idea", "Parallelograms and rhombuses", "<p>Angles between a pair of parallel sides add up to <b>180°</b>.</p><p><b>Opposite angles are equal.</b></p>"
      "<p>In a trapezium, the 2 angles between the parallel sides also add up to 180°.</p>", fpar, 110),
    L("Example", "ABCD is a parallelogram, ∠DAB = 140°", "<p>∠b = 180° - 140° = <b>40°</b></p><p>∠c = 140° (opposite ∠DAB)</p><p>∠d = ∠b = <b>40°</b></p>", fpar, 110),
    L("Example", "ABCD is a kite. Find ∠x.", "<p>A quadrilateral's angles add up to 360°.</p><p>∠x = 360° - 90° - 120° - 120° = <b>30°</b></p>", fkite, 111),
    L("Idea", "Angles at a point", "<p>Angles all the way round a point add up to <b>360°</b>.</p><p>So a reflex angle (bigger than 180°) inside a shape = 360° - the angle outside.</p>", None, 111),
]

q101 = []
# Let's Recall p.106
for lab_, sides, key, unit, fg in [
    ("Let's Recall 1 (a)", [18, 19.5, 26, 19.5], 83, "cm", FIG({"_A": [80, 40], "_B": [210, 40], "_C": [290, 180], "_D": [40, 180]}, [poly(["_A", "_B", "_C", "_D"], ORANGE), lab("_A", "_B", "18 cm"), lab("_B", "_C", "19.5 cm"), lab("_C", "_D", "26 cm"), lab("_D", "_A", "19.5 cm")], names=False)),
    ("Let's Recall 1 (b)", [6.5, 6.5, 6.5], 19.5, "m", FIG({"_A": [160, 30], "_B": [250, 190], "_C": [70, 190]}, [poly(["_A", "_B", "_C"], GREEN), lab("_B", "_C", "6.5 m"), tick("_A", "_B"), tick("_B", "_C"), tick("_C", "_A")], names=False)),
    ("Let's Recall 1 (c)", [17, 17, 13.5, 13.5], 61, "cm", FIG({"_A": [60, 60], "_B": [250, 60], "_C": [280, 170], "_D": [90, 170]}, [poly(["_A", "_B", "_C", "_D"], BLUE), lab("_A", "_B", "17 cm"), lab("_B", "_C", "13.5 cm")], names=False)),
    ("Let's Recall 1 (d)", [9, 5, 7.5], 21.5, "m", FIG({"_A": [60, 190], "_B": [260, 190], "_C": [60, 70]}, [poly(["_A", "_B", "_C"], PINK), lab("_A", "_B", "9 m"), lab("_C", "_A", "5 m"), lab("_B", "_C", "7.5 m")], names=False))]:
    check(round(sum(sides), 2), key, lab_)
    e = " + ".join(num(x) for x in sides)
    q101.append(Q(lab_, 106, "Find the perimeter of the figure.", "Add all the sides. Equal tick marks or a parallelogram's opposite sides help you find missing ones.",
                  ["The perimeter is the distance all the way round: add every side.", f"Perimeter = {e}", f"= <b>{num(key)} {unit}</b>"],
                  f"Perimeter = {num(key)} {unit}", f"{e} = {num(key)}", fg))
check(9.5 * 4, 38, "p.106 Q2")
q101.append(Q("Let's Recall 2", 106, "A playground is in the shape of a rhombus. Each side of it is 9.5 m long. If we want to fence this playground, what should be its length?",
              "A rhombus has 4 equal sides.", ["A rhombus has 4 equal sides of 9.5 m.", "Perimeter = 9.5 + 9.5 + 9.5 + 9.5", "= 19 + 19 = <b>38 m</b>"],
              "38 m", "The fence goes all the way round: 4 × 9.5 = 38 m.",
              {"img": "img/unit10/playground-fence.jpg", "alt": "a playground with a fence all the way round",
               "label": "A fence goes all the way round the playground. · รั้วล้อมรอบสนามเด็กเล่นทั้งหมด"}))
for lab_, how, val, key, unit, fg in [
    ("Let's Recall 3 (a)", "Area of parallelogram = height × base = 11 × 22", 11 * 22, 242, "cm",
     FIG({"_A": [90, 50], "_B": [290, 50], "_C": [240, 170], "_D": [40, 170], "_H": [90, 170]}, [poly(["_A", "_B", "_C", "_D"], ORANGE), seg("_A", "_H", True), ra("_H", "_A", "_C"), lab("_D", "_C", "22 cm", 16), lab("_A", "_H", "11 cm", -16), lab("_D", "_A", "13 cm", -24)], names=False)),
    ("Let's Recall 3 (b)", "Area of triangle = ½ × 18 × 15", Fraction(18 * 15, 2), 135, "cm",
     FIG({"_A": [120, 30], "_B": [40, 190], "_C": [280, 190], "_H": [120, 190]}, [poly(["_A", "_B", "_C"], GREEN), seg("_A", "_H", True), ra("_H", "_A", "_C"), lab("_B", "_C", "18 cm", 16), lab("_H", "_A", "15 cm", 16)], names=False)),
    ("Let's Recall 3 (c)", "Area of kite = ½ × the product of the diagonals = ½ × (11.5 × 20)", half(11.5) * 20, 115, "cm",
     FIG({"_A": [160, 20], "_B": [240, 70], "_C": [160, 210], "_D": [80, 70]}, [poly(["_A", "_B", "_C", "_D"], PINK), seg("_A", "_C", True), seg("_B", "_D", True), lab("_A", "_C", "20 cm", -18), lab("_D", "_B", "11.5 cm", -12)], names=False)),
    ("Let's Recall 3 (d)", "Area of triangle = ½ × 4 × 5", Fraction(4 * 5, 2), 10, "m",
     FIG({"_A": [60, 40], "_B": [60, 190], "_C": [220, 190]}, [poly(["_A", "_B", "_C"], BLUE), ra("_B", "_A", "_C"), lab("_B", "_C", "4 m", 16), lab("_A", "_B", "5 m", -16), lab("_A", "_C", "5.8 m")], names=False))]:
    check(val, key, lab_)
    q101.append(Q(lab_, 107, "Find the area of the figure.", "Pick the right formula for the shape. The height must meet the base at a right angle.",
                  [how, f"= <b>{num(key)} {unit}{SQ}</b>"], f"Area = {num(key)} {unit}{SQ}", "Use base and height, not the slanted side.", fg))
check(Fraction(26 * 25, 2), 325, "p.107 Q4")
q101.append(Q("Let's Recall 4", 107, "A piece of paper is in the shape of a right triangle as shown below. What is the area of this paper?",
              "Use the 2 sides that make the right angle.", ["The 2 sides at the right angle are 26 cm and 25 cm. (36.1 cm is the long slanted side.)",
                                                             "Area = ½ × 26 × 25", "26 × 25 = 650, and 650 ÷ 2 = <b>325 cm²</b>"],
              "325 cm²", "Half of a 26 cm by 25 cm rectangle.",
              FIG({"_A": [60, 30], "_B": [60, 190], "_C": [260, 190]}, [poly(["_A", "_B", "_C"], YELLOW), ra("_B", "_A", "_C"), lab("_B", "_C", "26 cm", 16), lab("_A", "_B", "25 cm", -16), lab("_A", "_C", "36.1 cm")], names=False)))

# Do and Learn p.114
check(180 - 108, 72, "p.114 ABC"); check(72 - 53, 19, "p.114 ABD"); check(180 - 108, 72, "p.114 CDA")
f114 = FIG({"A": [70, 40], "B": [290, 40], "C": [250, 170], "D": [30, 170]},
           [poly(["A", "B", "C", "D"], GREEN), seg("D", "B"), ang("B", "D", "C", "53°", 34), ang("C", "B", "D", "108°", 22)])
q101.append(Q("Do and Learn", 114, "ABCD is a parallelogram. ∠DBC = 53° and ∠BCD = 108°. Find ∠ABD and ∠CDA.",
              "Angles between a pair of parallel sides add up to 180°.",
              ["AB and DC are parallel, so ∠ABC + ∠BCD = 180°. ∠ABC = 180° - 108° = <b>72°</b>",
               "∠ABD = ∠ABC - ∠DBC = 72° - 53° = <b>19°</b>",
               "AD and BC are parallel, so ∠CDA + ∠BCD = 180°. ∠CDA = 180° - 108° = <b>72°</b>"],
              "∠ABD = 19°, ∠CDA = 72°", "Angles between parallel sides add up to 180°.", f114))

# Exercise 1 p.115
check((180 - 105) / 2, 37.5, "p.115 a")
q101.append(Q("Exercise 1 (a)", 115, "Find the values of the following unknown angles.", "The tick marks show an isosceles triangle.",
              ["CE = CD, so the triangle is isosceles and ∠e = ∠d.", "∠e + ∠d = 180° - 105° = 75°", "∠e = 75° ÷ 2 = <b>37.5°</b>", "∠d = ∠e = <b>37.5°</b>"],
              "∠e = 37.5°, ∠d = 37.5°", "37.5° + 37.5° + 105° = 180°.",
              FIG({"C": [160, 50], "E": [40, 170], "D": [280, 170]}, [poly(["C", "E", "D"], ORANGE), tick("C", "E"), tick("C", "D"), ang("C", "E", "D", "105°", 22), ang("E", "C", "D", "e", 34), ang("D", "C", "E", "d", 34)])))
check(180 - 69, 111, "p.115 b")
q101.append(Q("Exercise 1 (b)", 115, "Find the values of the following unknown angles.", "Opposite angles of a rhombus are equal. Angles between parallel sides add up to 180°.",
              ["∠a is opposite the 69° angle, so <b>∠a = 69°</b>.", "∠b and the 69° angle are between parallel sides: ∠b = 180° - 69° = <b>111°</b>",
               "∠d is opposite ∠b, so <b>∠d = 111°</b>."],
              "∠a = 69°, ∠b = 111°, ∠d = 111°", "69° + 111° + 69° + 111° = 360°.",
              FIG({"A": [50, 110], "B": [160, 40], "C": [270, 110], "D": [160, 180]}, [poly(["A", "B", "C", "D"], BLUE), ang("A", "B", "D", "a", 22), ang("B", "A", "C", "b", 22), ang("C", "B", "D", "69°", 22), ang("D", "A", "C", "d", 22)])))
check((540 - 108 * 3) / 2, 108, "p.115 c")
pc = reg(5, 160, 125, 95)
q101.append(Q("Exercise 1 (c)", 115, "Find the values of the following unknown angles.", "The angles of a pentagon add up to 540°.",
              ["The angles of a pentagon add up to <b>540°</b>.", "3 angles are 108°: 108° × 3 = 324°", "∠i + ∠j = 540° - 324° = 216°",
               "All sides are equal, so all angles are equal: ∠i = ∠j = 216° ÷ 2 = <b>108°</b>"],
              "∠i = 108°, ∠j = 108°", "5 equal angles of 108°: 5 × 108° = 540°.",
              FIG({"I": pc[0], "J": pc[1], "K": pc[2], "L": pc[3], "M": pc[4]}, [poly(["I", "J", "K", "L", "M"], GREEN),
                  ang("I", "M", "J", "i", 22), ang("J", "I", "K", "j", 22), ang("K", "J", "L", "108°", 22), ang("L", "K", "M", "108°", 22), ang("M", "L", "I", "108°", 22)]
                  + [tick(a, b) for a, b in [("I", "J"), ("J", "K"), ("K", "L"), ("L", "M"), ("M", "I")]])))
check(360 - 114, 246, "p.115 h"); check(540 - 246 - 90 * 3, 24, "p.115 g")
q101.append(Q("Exercise 1 (d)", 115, "Find the values of the following unknown angles.", "∠h is the inside angle at H. The angles at a point add up to 360°.",
              ["The angle outside at H is 114°. Angles at a point add up to 360°.", "∠h = 360° - 114° = <b>246°</b>",
               "The angles of a pentagon add up to 540°. There are 3 right angles (at F, J and I): 3 × 90° = 270°.",
               "∠g = 540° - 246° - 270° = <b>24°</b>"],
              "∠h = 246°, ∠g = 24°", "24° + 246° + 270° = 540°.",
              FIG({"F": [60, 30], "G": [290, 30], "H": [120, 110], "I": [120, 200], "J": [60, 200]},
                  [poly(["F", "G", "H", "I", "J"], YELLOW), ra("F", "J", "G"), ra("J", "F", "I"), ra("I", "J", "H"),
                   ang("G", "F", "H", "g", 40, 14), ang("H", "G", "I", "114°", 20)])))
check((180 - 120) / 2, 30, "p.115 e a"); check(120 - 30, 90, "p.115 e c"); check(120 - 60 - 30, 30, "p.115 e d")
hx = reg(6, 160, 120, 95, -120)
q101.append(Q("Exercise 1 (e)", 115, "Find the values of the following unknown angles.",
              "Triangle RMN has 2 equal sides (RM = MN).",
              ["Each angle of the hexagon is <b>120°</b>.", "Triangle RMN is isosceles (RM = MN), so ∠a = ∠b = (180° - 120°) ÷ 2 = <b>30°</b>",
               "∠c = 120° - 30° = <b>90°</b>", "At R: 120° - 60° - 30° = <b>30°</b>, so ∠d = 30°."],
              "∠a = 30°, ∠b = 30°, ∠c = 90°, ∠d = 30°", "The key uses the hexagon's 120° angles and the 60° angle given at R.",
              FIG({"M": hx[0], "N": hx[1], "O": hx[2], "P": hx[3], "Q": hx[4], "R": hx[5]},
                  [poly(["M", "N", "O", "P", "Q", "R"], PURPLE), seg("R", "N"), seg("R", "O"), ang("M", "R", "N", "120°", 18),
                   ang("R", "M", "N", "a", 34), ang("N", "M", "R", "b", 34), ang("N", "R", "O", "c", 26), ang("R", "N", "O", "d", 44, 12),
                   ang("R", "O", "Q", "60°", 24), ang("Q", "P", "R", "120°", 18), ang("P", "O", "Q", "120°", 18)]
                  + [tick(a, b) for a, b in [("M", "N"), ("N", "O"), ("O", "P"), ("P", "Q"), ("Q", "R"), ("R", "M")]])))
check(135 - 90, 45, "p.115 f")
oc = reg(8, 160, 120, 100, -112.5)
q101.append(Q("Exercise 1 (f)", 115, "Find the values of the following unknown angles.",
              "Each octagon angle (135°) is split into a right angle and a small angle.",
              ["Each angle of the octagon is <b>135°</b>.", "Part of it is a corner of the rectangle: <b>90°</b>.",
               "So each small angle = 135° - 90° = <b>45°</b>", "∠a = ∠b = ∠c = ∠d = 45°"],
              "∠a = ∠b = ∠c = ∠d = 45°", "90° + 45° = 135°.",
              FIG({"_%d" % k: p for k, p in enumerate(oc)}, [poly(["_%d" % k for k in range(8)], PINK),
                  poly([oc[0], oc[1], oc[4], oc[5]], "#ffffff"), txt(160, 125, "rectangle", 15)], names=False)))
check(180 - 37, 143, "p.116 BCF"); check(180 - 50, 130, "p.116 FCD"); check(360 - 143 - 130, 87, "p.116 Q2")
q101.append(Q("Exercise 2", 116, "ABCF and CDEF are trapeziums. Find ∠DCB.", "In a trapezium, the 2 angles between the parallel sides add up to 180°.",
              ["AB ∥ FC, so ∠BCF = 180° - 37° = <b>143°</b>", "FC ∥ ED, so ∠FCD = 180° - 50° = <b>130°</b>",
               "Angles at the point C add up to 360°: ∠DCB = 360° - 143° - 130° = <b>87°</b>"],
              "∠DCB = 87°", "143° + 130° + 87° = 360°.",
              FIG({"A": [40, 30], "B": [250, 30], "C": [180, 110], "F": [80, 110], "E": [80, 190], "D": [260, 190]},
                  [poly(["A", "B", "C", "D", "E", "F"], BLUE), seg("F", "C", True), ang("B", "A", "C", "37°", 30), ang("D", "C", "E", "50°", 30), ra("F", "C", "E"), ra("E", "F", "D")])))
check((180 - 110) / 2, 35, "p.116 FDC"); check(180 - 58 - 35, 87, "p.116 Q3")
q101.append(Q("Exercise 3", 116, "ABCD is a trapezium and ECFD is a rhombus. AD = BC, ∠CFD = 110° and ∠DAB = 58°. Find ∠EDA.",
              "In a rhombus, the diagonal DC cuts the angles into equal halves.",
              ["In the rhombus, triangle DFC has FD = FC, so ∠FDC = (180° - 110°) ÷ 2 = <b>35°</b>",
               "The rhombus is the same on both sides of DC, so ∠EDC = <b>35°</b>",
               "AB ∥ DC, so ∠ADC = 180° - 58° = 122°", "∠EDA = 122° - 35° = <b>87°</b> (the key writes this as 180° - 58° - 35°)"],
              "∠EDA = 87°", "∠ADC (122°) = ∠EDA (87°) + ∠EDC (35°).",
              FIG({"A": [30, 30], "B": [290, 30], "C": [230, 150], "D": [90, 150], "E": [160, 100], "F": [160, 200]},
                  [poly(["A", "B", "C", "D"], YELLOW), poly(["E", "C", "F", "D"], "#ffffff"), seg("D", "C"), ang("A", "B", "D", "58°", 26), ang("F", "C", "D", "110°", 18),
                   tick("E", "C"), tick("C", "F"), tick("F", "D"), tick("D", "E")])))
check(180 - 23 - 32 - 105, 20, "p.116 Q4"); check(180 - 23 - 105, 52, "p.116 Q4 alt")
q101.append(Q("Exercise 4", 116, "ABC and AED are straight lines. BE = BC. ∠EAB = 23°, ∠CEB = 32° and ∠CDE = 105°. Find ∠ECD.",
              "BE = BC, so triangle BEC is isosceles.",
              ["BE = BC, so ∠BCE = ∠BEC = <b>32°</b>", "In the big triangle ACD: ∠ACD = 180° - 23° - 105° = <b>52°</b>",
               "∠ECD = ∠ACD - ∠BCE = 52° - 32° = <b>20°</b>"],
              "∠ECD = 20°", "The angles of triangle ACD: 23° + 105° + 52° = 180°.",
              FIG({"A": [60, 20], "B": [200, 190], "C": [250, 240], "D": [110, 240], "E": [100, 200]},
                  [poly(["A", "C", "D"], GREEN), seg("E", "C"), seg("E", "B"), ang("A", "D", "C", "23°", 40, 14), ang("E", "B", "C", "32°", 30), ang("D", "C", "A", "105°", 20), tick("B", "E"), tick("B", "C")])))
check((180 - 40) / 2, 70, "p.117 ABC"); check(360 - 255 - 70, 35, "p.117 CBE"); check(90 - 35, 55, "p.117 Q5")
q101.append(Q("Exercise 5", 117, "In the figure, DBEC is a rectangle and ABC is an isosceles triangle with AB = AC. ∠CAB = 40° and ∠ABE = 255°. Find ∠DBC.",
              "Find ∠ABC first. Then use the angles at point B (360°).",
              ["AB = AC, so ∠ABC = (180° - 40°) ÷ 2 = <b>70°</b>", "Angles at point B add up to 360°: ∠CBE = 360° - 255° - 70° = <b>35°</b>",
               "∠DBE is a corner of the rectangle (90°): ∠DBC = 90° - 35° = <b>55°</b>"],
              "∠DBC = 55°", "35° + 55° = 90°, the rectangle's corner.",
              FIG({"A": [30, 60], "B": [220, 50], "C": [170, 210], "D": [150, 80], "E": [260, 190]},
                  [poly(["A", "B", "C"], BLUE), poly(["D", "B", "E", "C"], "#ffffff00"), seg("D", "B"), seg("B", "E"), seg("E", "C"), seg("C", "D"),
                   ang("A", "B", "C", "40°", 30), tick("A", "B"), tick("A", "C"), txt(250, 30, "255°", 15, "#c2185b")])))
check(180 - 30 - 25, 125, "p.117 DFB"); check(180 - 125, 55, "p.117 EFK"); check(180 - 55 - 45, 80, "p.117 FKE")
check(180 - 80, 100, "p.117 CKA"); check(180 - 100 - 40, 40, "p.117 Q6"); check(30 + 40 + 25 + 45 + 40, 180, "star sum")
st = reg(5, 160, 125, 105)
q101.append(Q("Exercise 6", 117, "In the figure, ∠EBD = 30°, ∠ACE = 40°, ∠BDA = 25° and ∠CEB = 45°. Find ∠DAC.",
              "Work through the small triangles one at a time, using 180° in a triangle and 180° on a straight line.",
              ["In triangle BDF: ∠DFB = 180° - 30° - 25° = <b>125°</b>", "On the straight line: ∠EFK = 180° - 125° = <b>55°</b>",
               "In triangle EFK: ∠FKE = 180° - 55° - 45° = <b>80°</b>", "On the straight line: ∠CKA = 180° - 80° = <b>100°</b>",
               "In triangle AKC: ∠DAC = 180° - 100° - 40° = <b>40°</b>"],
              "∠DAC = 40°", "The 5 point angles of this star add up to 180°: 30° + 40° + 25° + 45° + 40° = 180°.",
              FIG({"B": st[0], "C": st[1], "D": st[2], "E": st[3], "A": st[4]},
                  [poly(["B", "D", "A", "C", "E"], GREEN), ang("B", "E", "D", "30°", 34), ang("C", "A", "E", "40°", 34), ang("D", "B", "A", "25°", 34), ang("E", "C", "B", "45°", 34)])))

flash101 = [
    {"front": "Sum of angles in a triangle", "back": "180°"}, {"front": "Sum of angles in a quadrilateral", "back": "360°"},
    {"front": "Sum of angles in a pentagon", "back": "540°"}, {"front": "Sum of angles in a hexagon", "back": "720°"},
    {"front": "Sum of angles in an octagon", "back": "1,080°"}, {"front": "Angles at a point add up to…", "back": "360°"},
    {"front": "Parallelogram: opposite angles are…", "back": "Equal"}, {"front": "Angles between a pair of parallel sides add up to…", "back": "180°"},
    {"front": "Each angle of a regular pentagon", "back": "540° ÷ 5 = 108°"}, {"front": "Each angle of a regular hexagon", "back": "720° ÷ 6 = 120°"},
    {"front": "Each angle of a regular octagon", "back": "1,080° ÷ 8 = 135°"},
]
check(540 / 5, 108, "f"); check(720 / 6, 120, "f"); check(1080 / 8, 135, "f")
match101 = [["Triangle", "180°"], ["Quadrilateral", "360°"], ["Pentagon", "540°"], ["Hexagon", "720°"], ["Octagon", "1,080°"],
            ["Regular hexagon angle", "120°"], ["Regular octagon angle", "135°"], ["Regular pentagon angle", "108°"]]
quiz101 = [
    {"q": "The interior angles of a pentagon add up to…", "options": ["540°", "360°", "720°", "500°"]},
    {"q": "The interior angles of a hexagon add up to…", "options": ["720°", "540°", "600°", "360°"]},
    {"q": "Three angles of a quadrilateral are 90°, 120° and 120°. The fourth?", "options": ["30°", "60°", "150°", "210°"]},
    {"q": "ABCD is a parallelogram. ∠A = 140°. What is ∠B?", "options": ["40°", "140°", "220°", "50°"]},
    {"q": "A rhombus has an angle of 69°. The angle next to it is…", "options": ["111°", "69°", "21°", "291°"]},
    {"q": "Each angle of a regular octagon is…", "options": ["135°", "120°", "108°", "145°"]},
    {"q": "The outside angle at a point is 114°. The inside (reflex) angle is…", "options": ["246°", "66°", "114°", "156°"]},
    {"q": "Each angle of a regular pentagon is…", "options": ["108°", "120°", "100°", "72°"]},
    {"q": "Angles at a point add up to…", "options": ["360°", "180°", "90°", "540°"]},
    {"q": "Trapezium: the angle at one end of a parallel side is 112°. The other angle between the parallel sides?", "options": ["68°", "112°", "248°", "78°"]},
    {"q": "Isosceles triangle with vertex angle 105°. Each base angle?", "options": ["37.5°", "75°", "42.5°", "52.5°"]},
]
check(360 - 300, 60, "q"); check(180 - 112, 68, "q"); check((180 - 105) / 2, 37.5, "q")
sections.append({"id": "10-1", "title": "Interior Angles of Polygons", "short": "1. Interior Angles", "pages": "p.106 to 117",
                 "learn": learn101, "questions": q101, "flash": flash101, "match": match101, "quiz": quiz101})

# ==================================================================
# 10.2 FINDING PERIMETER OF A POLYGON (p.118 to 123)
# ==================================================================
check(9 + 12 + 21 + 13.5 + 12, 67.5, "p.118 Q1"); check(10.5 * 6 + 11.2 * 2 + 33.2, 118.6, "p.118 Q2")
check(round(11.6 * 2 + 10.5 * 2 + 29.2 * 2 + 3 + 26.2, 2), 131.8, "p.119 A"); check(round(6 * 3 + 8 * 4 + 7.2 * 2 + 14 * 2 + 32.4, 2), 124.8, "p.119 B")
check(round(131.8 - 124.8, 2), 7, "p.119 diff")
fpent = FIG({"A": [70, 40], "B": [190, 40], "C": [280, 120], "D": [190, 200], "E": [70, 200]},
            [poly(["A", "B", "C", "D", "E"], ORANGE), lab("A", "B", "12 cm"), lab("B", "C", "13.5 cm"), lab("C", "D", "21 cm"), lab("D", "E", "12 cm"), lab("E", "A", "9 cm")])
learn102 = [
    L("Idea", "Perimeter of a polygon", "<p>The perimeter is the <b>sum of all the side lengths</b>.</p><p>Tip: tick each side as you add it, so you don't miss one or add one twice.</p>", None, 118),
    L("Example", "Pentagon ABCDE", "<p>Perimeter = 9 + 12 + 21 + 13.5 + 12 = <b>67.5 cm</b></p>", fpent, 118),
    L("Idea", "Use multiplication for equal sides", "<p>Same tick marks = same length. Group them.</p><p>6 sides of 10.5 cm: 10.5 × 6 = 63 cm. Much faster than adding 6 times!</p>", None, 118),
    L("Example", "Equal sides", "<p>A polygon has 6 sides of 10.5 cm, 2 sides of 11.2 cm and 1 side of 33.2 cm.</p>"
      "<p>(10.5 × 6) + (11.2 × 2) + 33.2 = 63 + 22.4 + 33.2 = <b>118.6 cm</b></p>", None, 118),
    L("Idea", "Changing m to cm", "<p>1 m = 100 cm. Multiply by 100.</p><p>17.2 m = 17.2 × 100 = <b>1,720 cm</b></p>", None, 121),
    L("Example", "Difference between 2 perimeters", "<p>Polygon A = 131.8 m, Polygon B = 124.8 m.</p><p>Difference = 131.8 - 124.8 = <b>7 m</b></p>", None, 119),
]
q102 = []
check(round(15.2 * 2 + 11.5 * 2 + 15.9 + 10.1 + 26, 2), 105.4, "p.120 a"); check(round(23 * 2 + 23.8 * 4, 2), 141.2, "p.120 b")
q102.append(Q("Do and Learn (a)", 120, "Find the perimeter of the figure.", "Use the tick marks: equal marks mean equal lengths.",
              ["GA and GF have the same tick mark: 2 sides of <b>15.2 cm</b>.", "CD and DE have the same tick mark: 2 sides of <b>11.5 cm</b>.",
               "The other sides: AB = 15.9 cm, BC = 10.1 cm, FE = 26 cm.", "Perimeter = (15.2 × 2) + (11.5 × 2) + 15.9 + 10.1 + 26",
               "= 30.4 + 23 + 15.9 + 10.1 + 26 = <b>105.4 cm</b>"],
              "Perimeter = 105.4 cm", "Every side is counted once.",
              FIG({"A": [90, 30], "B": [200, 30], "C": [200, 100], "D": [250, 100], "E": [250, 190], "F": [90, 190], "G": [30, 110]},
                  [poly(["A", "B", "C", "D", "E", "F", "G"], YELLOW), lab("A", "B", "15.9 cm"), lab("B", "C", "10.1 cm"), lab("D", "E", "11.5 cm"), lab("E", "F", "26 cm"),
                   lab("G", "A", "15.2 cm"), tick("G", "A"), tick("F", "G"), tick("D", "E", 2), tick("C", "D", 2)])))
q102.append(Q("Do and Learn (b)", 120, "Find the perimeter of the figure.", "Use the tick marks to find equal sides.",
              ["IN and KL have the same mark: 2 sides of <b>23 cm</b>.", "IJ, JK, NM and ML have the same mark: 4 sides of <b>23.8 cm</b>.",
               "Perimeter = (23 × 2) + (23.8 × 4)", "= 46 + 95.2 = <b>141.2 cm</b>"],
              "Perimeter = 141.2 cm", "2 short sides and 4 slanted sides.",
              FIG({"I": [40, 40], "J": [160, 80], "K": [280, 40], "L": [280, 180], "M": [160, 140], "N": [40, 180]},
                  [poly(["I", "J", "K", "L", "M", "N"], PINK), lab("I", "J", "23.8 cm"), lab("K", "L", "23 cm"),
                   tick("I", "J", 2), tick("J", "K", 2), tick("L", "M", 2), tick("M", "N", 2), tick("K", "L"), tick("N", "I")])))
ex1 = [("(a)", "(2.1 × 2) + (5 × 2) + 3", 2.1 * 2 + 5 * 2 + 3, 17.2, ["AB and ED are 5 m each (same mark).", "BC and CD are 2.1 m each (same mark).", "AE = 3 m."],
        FIG({"A": [50, 40], "B": [200, 40], "C": [280, 110], "D": [200, 180], "E": [50, 180]}, [poly(["A", "B", "C", "D", "E"], ORANGE), lab("A", "B", "5 m"), lab("B", "C", "2.1 m"), lab("E", "A", "3 m"), tick("A", "B"), tick("E", "D"), tick("B", "C", 2), tick("C", "D", 2)])),
       ("(b)", "2 × 10", 2 * 10, 20, ["The star has <b>10 sides</b>, all with the same mark.", "Each side is 2 m."],
        FIG({"_%d" % k: p for k, p in enumerate([q for pair in zip(reg(5, 160, 120, 100), reg(5, 160, 120, 42, -54)) for q in pair])},
            [poly(["_%d" % k for k in range(10)], PINK), lab("_2", "_3", "2 m")], names=False)),
       ("(c)", "3.5 × 6", 3.5 * 6, 21, ["The hexagon has <b>6 equal sides</b> of 3.5 m."],
        FIG({"_%d" % k: p for k, p in enumerate(reg(6, 160, 120, 90, -120))}, [poly(["_%d" % k for k in range(6)], PURPLE), lab("_0", "_1", "3.5 m")], names=False)),
       ("(d)", "2.9 × 8", 2.9 * 8, 23.2, ["The octagon has <b>8 equal sides</b> of 2.9 m."],
        FIG({"_%d" % k: p for k, p in enumerate(reg(8, 160, 120, 90, -112.5))}, [poly(["_%d" % k for k in range(8)], GREEN), lab("_0", "_1", "2.9 m")], names=False)),
       ("(e)", "(2 × 4) + (2.6 × 8)", 2 * 4 + 2.6 * 8, 28.8, ["The cross has <b>4 short sides</b> of 2 m (the ends).", "It has <b>8 sides</b> of 2.6 m (same mark)."],
        FIG({"_%d" % k: p for k, p in enumerate([[130, 20], [190, 20], [190, 80], [250, 80], [250, 140], [190, 140], [190, 200], [130, 200], [130, 140], [70, 140], [70, 80], [130, 80]])},
            [poly(["_%d" % k for k in range(12)], GREEN), lab("_0", "_1", "2 m"), lab("_1", "_2", "2.6 m")], names=False)),
       ("(f)", "(1 × 2) + (6.2 × 2) + 7.2 + 2 + 9.2 + 8", 1 * 2 + 6.2 * 2 + 7.2 + 2 + 9.2 + 8, 40.8, ["The sides with the same marks: 2 sides of 1 m and 2 sides of 6.2 m.", "The other sides: 7.2 m, 2 m, 9.2 m and 8 m."],
        FIG({"A": [30, 30], "B": [110, 50], "C": [210, 50], "D": [210, 100], "E": [260, 100], "F": [260, 130], "G": [110, 140], "H": [30, 200]},
            [poly(["A", "B", "C", "D", "E", "F", "G", "H"], YELLOW), lab("A", "B", "6.2 m"), lab("B", "C", "7.2 m"), lab("C", "D", "2 m"), lab("E", "F", "1 m"), lab("F", "G", "9.2 m"), lab("H", "A", "8 m")]))]
for part, expr, val, key, notes, fg in ex1:
    check(round(val, 2), key, f"p.121 {part}")
    q102.append(Q(f"Exercise 1 {part}", 121, "Find the perimeter of the figure. Answer in centimeters.", "Find the perimeter in m first. Then × 100 to change it to cm.",
                  notes + [f"Perimeter = {expr} = <b>{num(key)} m</b>", f"In cm: {num(key)} × 100 = <b>{num(key * 100)} cm</b>"],
                  f"{num(key * 100)} cm", f"{num(key)} m = {num(key * 100)} cm because 1 m = 100 cm.", fg))
p122 = [("Figure 1 (chevron)", "(3.2 × 2) + (10 × 4)", 3.2 * 2 + 10 * 4, 46.4), ("Figure 2 (L shape)", "4 + 18.2 + 15.2 + 9.2 + 11.2 + 9", 4 + 18.2 + 15.2 + 9.2 + 11.2 + 9, 66.8),
        ("Figure 3 (arrow)", "(11 × 2) + (12.2 × 2) + (6 × 2) + 4", 22 + 24.4 + 12 + 4, 62.4), ("Figure 4 (house shape)", "24.4 + (5 × 2) + (8 × 2) + (6 × 2)", 24.4 + 10 + 16 + 12, 62.4),
        ("Figure 5 (W shape)", "14.8 + (15 × 2) + (11 × 2)", 14.8 + 30 + 22, 66.8), ("Figure 6 (upside-down T)", "15.6 + (0.5 × 2) + 5.2 + (7.1 × 2) + (5.2 × 2)", 15.6 + 1 + 5.2 + 14.2 + 10.4, 46.4)]
for nm, e, v, k in p122:
    check(round(v, 2), k, f"p.122 {nm}")
S1 = off([[0, 45], [60, 0], [120, 45], [120, 65], [60, 25], [0, 65]], 20, 30)
S2 = off([[60, 0], [90, 0], [90, 120], [0, 120], [0, 70], [60, 70]], 30, 180)
S3 = off([[0, 50], [45, 5], [45, 35], [130, 35], [130, 65], [45, 65], [45, 95]], 10, 330)
S4 = off([[0, 30], [40, 0], [80, 30], [100, 10], [125, 30], [125, 100], [0, 100]], 200, 30)
S5 = off([[0, 0], [60, 40], [120, 0], [120, 100], [0, 100]], 205, 190)
S6 = off([[0, 80], [45, 80], [45, 0], [80, 0], [80, 80], [125, 80], [125, 90], [0, 90]], 200, 330)
f122 = {"w": 340, "h": 450, "pts": {}, "items":
        outline(S1, YELLOW, [(1, 2, "10 cm"), (2, 3, "3.2 cm")], [(0, 1, 1), (1, 2, 1), (5, 4, 1), (4, 3, 1), (0, 5, 2), (2, 3, 2)])
        + outline(S2, YELLOW, [(0, 1, "4 cm"), (1, 2, "18.2 cm"), (2, 3, "15.2 cm"), (3, 4, "9.2 cm"), (4, 5, "11.2 cm"), (5, 0, "9 cm")])
        + outline(S3, YELLOW, [(0, 1, "11 cm"), (2, 3, "12.2 cm"), (3, 4, "4 cm"), (5, 6, "6 cm")], [(0, 1, 1), (6, 0, 1), (1, 2, 2), (5, 6, 2), (2, 3, 3), (4, 5, 3)])
        + outline(S4, PURPLE, [(0, 1, "8 cm"), (3, 4, "6 cm"), (4, 5, "5 cm"), (5, 6, "24.4 cm")], [(0, 1, 1), (1, 2, 1), (2, 3, 2), (3, 4, 2), (4, 5, 3), (6, 0, 3)])
        + outline(S5, PURPLE, [(0, 1, "11 cm"), (2, 3, "15 cm"), (3, 4, "14.8 cm")], [(0, 1, 1), (1, 2, 1), (2, 3, 2), (4, 0, 2)])
        + outline(S6, PURPLE, [(2, 3, "5.2 cm"), (3, 4, "7.1 cm"), (5, 6, "0.5 cm"), (6, 7, "15.6 cm")], [(0, 1, 1), (4, 5, 1), (1, 2, 2), (3, 4, 2), (5, 6, 3), (7, 0, 3)])}
q102.append(Q("Exercise 2", 122, "Find the perimeter of the following figures. Draw a line to match the perimeter of the same value.",
              "Use the tick marks to find the equal sides in each figure, then add.",
              [f"{nm}: {e} = <b>{num(k)} cm</b>" for nm, e, v, k in p122] + ["Match the equal perimeters: 46.4 cm ↔ 46.4 cm, 66.8 cm ↔ 66.8 cm, 62.4 cm ↔ 62.4 cm."],
              "Left figures: 46.4 cm, 66.8 cm, 62.4 cm. Right figures: 62.4 cm, 66.8 cm, 46.4 cm",
              "The chevron matches the upside-down T, the L matches the W, and the arrow matches the house.", f122))
check(round(3 + 6.2 + 9.8 + 11.7 + 12, 2), 42.7, "p.123 A"); check(round(1 * 2 + 2 * 4 + 2.2 * 4 + 4 * 2 + 3.8 * 2 + 1.5 + 3.5, 2), 39.4, "p.123 B"); check(round(42.7 - 39.4, 2), 3.3, "p.123 diff")
q102.append(Q("Exercise 3", 123, "Find the difference between the perimeter of polygons A and B.", "Find each perimeter, then subtract the smaller from the bigger.",
              ["Polygon A = 3 + 6.2 + 9.8 + 11.7 + 12 = <b>42.7 m</b>",
               "Polygon B = (1 × 2) + (2 × 4) + (2.2 × 4) + (4 × 2) + (3.8 × 2) + 1.5 + 3.5", "= 2 + 8 + 8.8 + 8 + 7.6 + 1.5 + 3.5 = <b>39.4 m</b>",
               "Difference = 42.7 - 39.4 = <b>3.3 m</b>"],
              "3.3 m", "Polygon A's perimeter is 3.3 m longer.",
              FIG({"_a": [40, 30], "_b": [80, 30], "_c": [80, 100], "_d": [150, 170], "_e": [40, 170]},
                  [poly(["_a", "_b", "_c", "_d", "_e"], GREEN), lab("_a", "_b", "3 m"), lab("_b", "_c", "6.2 m"), lab("_c", "_d", "9.8 m"), lab("_d", "_e", "11.7 m"), lab("_e", "_a", "12 m"), txt(95, 200, "(A)", 16, "#1f2a44")], names=False)))
k10 = 16
B123 = [[x * k10 + 175, y * k10 + 30] for x, y in [(0, 0), (1, 0), (1, 2.2), (3, 2.2), (3, 0), (4.5, 0), (4.5, 2.2), (6.5, 2.2), (6.5, 0), (7.5, 0), (7.5, 4),
                                                (5.5, 4), (5.5, 7.8), (2, 7.8), (2, 4), (0, 4)]]
for qq in q102:
    if qq["label"] == "Exercise 3":
        qq["fig"]["w"] = 320
        qq["fig"]["items"] += [poly(B123, ORANGE), lab(B123[0], B123[1], "1 m", -12), lab(B123[4], B123[5], "1.5 m", -12), lab(B123[2], B123[3], "2 m", 12),
                               lab(B123[9], B123[10], "4 m", -14), lab(B123[11], B123[12], "3.8 m", -18), lab(B123[13], B123[12], "3.5 m", 14), lab(B123[1], B123[2], "2.2 m", -18),
                               txt(235, 200, "(B)", 16, "#1f2a44")]
flash102 = [
    {"front": "Perimeter of a polygon", "back": "The sum of all its side lengths"}, {"front": "Same tick marks mean…", "back": "The sides are the same length"},
    {"front": "Regular hexagon, side 3.5 m. Perimeter?", "back": "3.5 × 6 = 21 m"}, {"front": "Regular octagon, side 2.9 m. Perimeter?", "back": "2.9 × 8 = 23.2 m"},
    {"front": "1 m = ? cm", "back": "100 cm"}, {"front": "17.2 m in cm", "back": "1,720 cm"},
    {"front": "A star with 10 sides of 2 m. Perimeter?", "back": "20 m"}, {"front": "Difference of 42.7 m and 39.4 m", "back": "3.3 m"},
]
match102 = [["Hexagon, side 3.5 m", "21 m"], ["Octagon, side 2.9 m", "23.2 m"], ["Star, 10 sides of 2 m", "20 m"], ["17.2 m", "1,720 cm"],
            ["Pentagon 9, 12, 21, 13.5, 12", "67.5 cm"], ["Rhombus, side 9.5 m", "38 m"], ["28.8 m", "2,880 cm"], ["Square, side 4.5 cm", "18 cm"]]
quiz102 = [
    {"q": "A regular hexagon has sides of 4 cm. Perimeter?", "options": ["24 cm", "20 cm", "16 cm", "28 cm"]},
    {"q": "A regular octagon has sides of 2.5 m. Perimeter?", "options": ["20 m", "15 m", "17.5 m", "10 m"]},
    {"q": "A pentagon has sides 9, 12, 21, 13.5 and 12 cm. Perimeter?", "options": ["67.5 cm", "55.5 cm", "66.5 cm", "68.5 cm"]},
    {"q": "23.2 m = ? cm", "options": ["2,320 cm", "232 cm", "23,200 cm", "23.2 cm"]},
    {"q": "6 sides of 10.5 cm. Total?", "options": ["63 cm", "60.5 cm", "16.5 cm", "65 cm"]},
    {"q": "Perimeter A = 131.8 m, Perimeter B = 124.8 m. Difference?", "options": ["7 m", "17 m", "256.6 m", "6 m"]},
    {"q": "A rhombus has sides of 9.5 m. Perimeter?", "options": ["38 m", "19 m", "28.5 m", "90.25 m"]},
    {"q": "2 sides of 23 cm and 4 sides of 23.8 cm. Perimeter?", "options": ["141.2 cm", "93.6 cm", "140.2 cm", "46.8 cm"]},
    {"q": "Which tells you two sides are equal?", "options": ["The same tick marks", "A right angle mark", "A dashed line", "A letter"]},
    {"q": "A star has 10 equal sides of 2 m. Perimeter in cm?", "options": ["2,000 cm", "200 cm", "20 cm", "1,000 cm"]},
]
check(4 * 6, 24, "q"); check(2.5 * 8, 20, "q"); check(10.5 * 6, 63, "q"); check(9.5 * 4, 38, "q"); check(round(46 + 95.2, 2), 141.2, "q")
sections.append({"id": "10-2", "title": "Finding Perimeter of a Polygon", "short": "2. Perimeter", "pages": "p.118 to 123",
                 "learn": learn102, "questions": q102, "flash": flash102, "match": match102, "quiz": quiz102})

# ==================================================================
# 10.3 FINDING AREA OF A POLYGON (p.124 to 131)
# ==================================================================
check(23 * 12 + 11 * 13, 419, "p.124 Q1"); check(Fraction(16 * 6, 2) + Fraction(27, 2) * 16, 264, "p.124 Q2")
check(Fraction(1, 2) * Fraction("2.2") * 4 * 8, Fraction("35.2"), "p.125 Q3"); check(Fraction(25 * 16, 2) + Fraction("21.8") * 13, Fraction("483.4"), "p.125 Q4")
fhex = FIG({"A": [40, 30], "B": [200, 30], "C": [200, 110], "D": [270, 110], "E": [270, 180], "F": [40, 180]},
           [poly(["A", "B", "C", "D", "E", "F"], BLUE), seg("C", [200, 180], True), txt(120, 110, "①", 22, "#1f2a44"), txt(235, 150, "②", 22, "#1f2a44"),
            lab("A", "B", "23 cm"), lab("F", "A", "12 cm"), lab("D", "E", "13 cm"), lab("C", "D", "11 cm")])
fdl = FIG({"T": [80, 30], "a": [40, 90], "b": [120, 90], "c": [250, 90], "d": [250, 210], "e": [40, 210]},
          [poly(["a", "T", "b"], ORANGE), poly(["a", "b", "c", "d", "e"], GREEN), seg("b", [120, 210], True), txt(80, 75, "A", 18, "#1f2a44"), txt(80, 160, "B", 18, "#1f2a44"),
           txt(185, 160, "C", 18, "#1f2a44"), lab("e", "a", "6 m", -16), lab([40, 210], [120, 210], "5 m", 16), lab([120, 210], "d", "6 m", 16), txt(25, 60, "4 m", 15)], names=False)
learn103 = [
    L("Idea", "Split it into shapes you know", "<p>Cut the polygon into <b>rectangles, squares, triangles and trapeziums</b>.</p><p>Find each area, then <b>add</b> them.</p>"
      "<p>Area of trapezium = ½ × height × (sum of the parallel sides)</p>", fhex, 124),
    L("Example", "Hexagon ABCDEF", "<p>① 23 × 12 = 276 cm²<br>② 11 × 13 = 143 cm²</p><p>Total = 276 + 143 = <b>419 cm²</b></p>", fhex, 124),
    L("Idea", "Equal pieces", "<p>A regular octagon splits into <b>8 equal triangles</b> from the middle.</p><p>Find one triangle, then × 8.</p>", None, 125),
    L("Example", "Octagon: 8 triangles of base 2.2 m, height 4 m", "<p>One triangle = ½ × 2.2 × 4 = 4.4 m²</p><p>Octagon = 4.4 × 8 = <b>35.2 m²</b></p>", None, 125),
    L("Idea", "Take away", "<p>Sometimes it's easier to find a <b>big rectangle</b> and <b>subtract</b> the parts that are not shaded.</p>", None, 128),
    L("Example", "Triangle + rectangle + square", "<p>A = ½ × 5 × 4 = 10 m²<br>B = 6 × 5 = 30 m²<br>C = 6 × 6 = 36 m²</p><p>Total = 10 + 30 + 36 = <b>76 m²</b></p>", fdl, 127),
]
q103 = []
check(Fraction(5 * 4, 2) + 6 * 5 + 6 * 6, 76, "p.127 DL")
q103.append(Q("Do and Learn", 127, "The figure is made up of a triangle, a rectangle and a square. Find the area of the figure.", "Find A, B and C separately, then add.",
              ["Triangle A: base 5 m, height 4 m. Area = ½ × 5 × 4 = <b>10 m²</b>", "Rectangle B: 6 m by 5 m. Area = 6 × 5 = <b>30 m²</b>",
               "Square C: 6 m by 6 m. Area = 6 × 6 = <b>36 m²</b>", "Total = 10 + 30 + 36 = <b>76 m²</b>"],
              "76 m²", "The figure is the 3 shapes added together.", fdl))
ex = [("(a)", "(½ × 2 × 8) + (8 × 8) + (½ × 2 × 8)", Fraction(16, 2) + 64 + Fraction(16, 2), 80, "cm",
       ["The middle is a square: 8 × 8 = <b>64 cm²</b>", "The 2 thin triangles each have base 2 cm and height 8 cm: ½ × 2 × 8 = <b>8 cm²</b> each"],
       FIG({"K": [40, 20], "E": [80, 50], "F": [200, 50], "G": [200, 170], "H": [80, 170], "J": [240, 200]},
           [poly(["K", "E", "H"], GREEN), poly(["E", "F", "G", "H"], GREEN), poly(["F", "J", "G"], GREEN), lab("E", "F", "8 cm"), lab("F", "G", "8 cm"), txt(55, 190, "2 cm", 14), txt(225, 40, "2 cm", 14), ra("E", "F", "H")])),
      ("(b)", "[(½ × 7 × 8) × 2] + (6 × 14)", Fraction(56, 2) * 2 + 84, 140, "cm",
       ["The bottom is a rectangle 14 cm by 6 cm: 6 × 14 = <b>84 cm²</b>", "There are 2 shaded triangles, each with base 7 cm and height 8 cm: ½ × 7 × 8 = 28 cm², so 2 × 28 = <b>56 cm²</b>"],
       FIG({"A": [40, 30], "C": [140, 30], "E": [240, 30], "B": [90, 130], "D": [190, 130], "F": [240, 200], "G": [40, 200]},
           [poly(["A", "B", "C", "D", "E", "F", "G"], BLUE), seg([40, 130], [240, 130], True), lab("A", "C", "7 cm", -14), lab("C", "E", "7 cm", -14), lab("E", [240, 130], "8 cm", -16), lab([240, 130], "F", "6 cm", -16), lab("G", "F", "14 cm", 16)])),
      ("(c)", "(½ × 5 × 6) + [½ × 5 × (19 + 26)]", Fraction(30, 2) + Fraction(5, 2) * 45, Fraction(255, 2), "m",
       ["The top-right part is a triangle with base 5 m and height 6 m: ½ × 5 × 6 = <b>15 m²</b>",
        "The bottom is a trapezium with height 5 m. Its parallel sides are 26 m and 26 - 7 = 19 m: ½ × 5 × (19 + 26) = <b>112.5 m²</b>"],
       FIG({"A": [80, 120], "B": [220, 120], "_F": [270, 120], "C": [270, 60], "D": [270, 170], "E": [10, 170]},
           [poly(["E", "A", "B", "C", "D"], PURPLE), seg("B", "_F", True), lab("E", "D", "26 m", 16), lab("A", "B", "14 m", -14), lab("_F", "C", "6 m", -16), lab("_F", "D", "5 m", -16), txt(45, 110, "7 m", 14)])),
      ("(d)", "4 × 6", 4 * 6, 24, "m", ["Cut the triangle off the right end and fit it into the notch on the left.", "The shape becomes a rectangle 6 m by 4 m."],
       FIG({"_a": [40, 50], "_b": [160, 50], "_c": [230, 120], "_d": [160, 190], "_e": [40, 190], "_f": [110, 120]},
           [poly(["_a", "_b", "_c", "_d", "_e", "_f"], YELLOW), lab("_a", "_b", "6 m", -14), lab("_e", "_d", "6 m", 16), seg("_b", "_d", True), txt(180, 125, "4 m", 14), lab("_b", "_c", "4 m")], names=False)),
      ("(e)", "(12 × 12) - (½ × 12 × 6) - [(½ × 6 × 12) × 2]", 144 - 36 - 72, 36, "m",
       ["The square WXYZ is 12 × 12 = <b>144 m²</b>", "The white triangle at the bottom middle: ½ × 12 × 6 = <b>36 m²</b>",
        "The 2 white side triangles: ½ × 6 × 12 = 36 m² each, so <b>72 m²</b>", "Shaded = 144 - 36 - 72"],
       FIG({"W": [60, 30], "X": [210, 30], "Y": [210, 180], "Z": [60, 180], "_T": [135, 30], "_M": [135, 105]},
           [poly(["W", "X", "Y", "Z"], "#ffffff"), poly(["Z", "_T", "Y", "_M"], ORANGE), lab("Z", "Y", "12 m", 16), seg("_T", [135, 180], True)])),
      ("(f)", "(18 × 10.2) + [(½ × 18 × 5) × 2]", Fraction("183.6") + Fraction(90), Fraction("273.6"), "m",
       ["The middle rectangle is 18 m by 10.2 m: 18 × 10.2 = <b>183.6 m²</b>", "The 2 side triangles have base 18 m and height 5 m: ½ × 18 × 5 = 45 m² each, so <b>90 m²</b>"],
       FIG({"A": [110, 30], "B": [210, 30], "C": [260, 120], "D": [210, 210], "E": [110, 210], "F": [60, 120]},
           [poly(["A", "B", "C", "D", "E", "F"], GREEN), poly(["A", "B", "D", "E"], GREEN), lab("A", "B", "10.2 m", -14), seg("F", [110, 120], True), seg([210, 120], "C", True), txt(85, 112, "5 m", 13), txt(160, 125, "18 m", 15)]))]
for part, expr, val, key, unit, notes, fg in ex:
    check(val, key, f"p.128 {part}")
    q103.append(Q(f"Exercise 1 {part}", 128 if part in ("(a)", "(b)", "(c)") else 129, "Find the area of the shaded part.",
                  "Split the shape into rectangles and triangles, or take the white parts away from a big shape.",
                  notes + [f"Area = {expr}", f"= <b>{num(key)} {unit}{SQ}</b>"], f"{num(key)} {unit}{SQ}", "Add the pieces (or take away the white parts).", fg))
check(Fraction(15, 2) + 75 + 15, Fraction(195, 2), "p.130 Q2")
q103.append(Q("Exercise 2", 130, "Identify the shapes that make up the figure below. Find the area of the figure.", "There is a triangle on top, a big rectangle and a small rectangle below.",
              ["Triangle A: base 5 cm, height 3 cm. Area = ½ × 5 × 3 = <b>7.5 cm²</b>", "Rectangle B: 15 cm by 5 cm. Area = 15 × 5 = <b>75 cm²</b>",
               "Rectangle C: 5 cm by 3 cm. Area = 5 × 3 = <b>15 cm²</b>", "Total = 7.5 + 75 + 15 = <b>97.5 cm²</b>"],
              "Triangle, 2 rectangles; area = 97.5 cm²", "7.5 + 75 + 15 = 97.5",
              FIG({"_t": [160, 20], "_a": [110, 70], "_b": [210, 70], "_c": [290, 70], "_d": [290, 150], "_e": [210, 150], "_f": [210, 200], "_g": [110, 200], "_h": [110, 150], "_i": [30, 150], "_j": [30, 70]},
                  [poly(["_j", "_a", "_t", "_b", "_c", "_d", "_e", "_f", "_g", "_h", "_i"], YELLOW), txt(160, 60, "A", 16, "#c2185b"), txt(160, 115, "B", 16, "#c2185b"), txt(160, 180, "C", 16, "#c2185b"),
                   lab("_i", "_d", "15 cm", 70), txt(305, 50, "3 cm", 14), txt(310, 115, "5 cm", 14), txt(240, 180, "3 cm", 14)], names=False)))
check(10 * 9 + Fraction(7 * 10, 2), 125, "p.130 Q3")
q103.append(Q("Exercise 3", 130, "VXYZ is a rectangle. VZ = 10 cm, YZ = 16 cm and WX = 7 cm. Find the area of the shaded part VWYZ.", "Split the shaded part into a rectangle A and a triangle B.",
              ["VW = 16 - 7 = <b>9 cm</b>", "Rectangle A: 10 × 9 = <b>90 cm²</b>", "Triangle B: base 7 cm, height 10 cm: ½ × 7 × 10 = <b>35 cm²</b>", "Shaded = 90 + 35 = <b>125 cm²</b>"],
              "125 cm²", "A rectangle plus a triangle.",
              FIG({"V": [40, 40], "W": [175, 40], "X": [280, 40], "Y": [280, 190], "Z": [40, 190]},
                  [poly(["V", "X", "Y", "Z"], "#ffffff"), poly(["V", "W", "Y", "Z"], GREEN), seg("W", [175, 190], True), lab("W", "X", "7 cm", -14), lab("Z", "V", "10 cm", 16), lab("Z", "Y", "16 cm", 16)])))
check(9 * 9, 81, "p.131 A"); check(7 * 7, 49, "p.131 B"); check(Fraction(7 * 9, 2), Fraction(63, 2), "p.131 C")
q103.append(Q("Exercise 4", 131, "The figure is made up of 2 squares, A and B, and a right triangle, C. The area of Square A is 81 cm² and the area of Square B is 49 cm². Find the area of Triangle C.",
              "Which number times itself makes 81? And 49?",
              ["9 × 9 = 81, so each side of Square A is <b>9 cm</b>.", "7 × 7 = 49, so each side of Square B is <b>7 cm</b>.",
               "The 2 short sides of triangle C are sides of the squares: 9 cm and 7 cm, at a right angle.", "Area of C = ½ × 7 × 9 = 63 ÷ 2 = <b>31.5 cm²</b>"],
              "31.5 cm²", "The squares' sides are the triangle's base and height.",
              FIG({"_p": [170, 140], "_u": [93.6, 63.6], "_v": [229.4, 80.6]},
                  [poly([[170, 140], [93.6, 63.6], [17.2, 140], [93.6, 216.4]], BLUE), poly([[170, 140], [229.4, 80.6], [288.8, 140], [229.4, 199.4]], BLUE),
                   poly(["_p", "_u", "_v"], PURPLE), ra("_p", "_u", "_v"), txt(93.6, 146, "A", 20, "#1f2a44"), txt(229.4, 146, "B", 20, "#1f2a44"), txt(165, 100, "C", 18, "#1f2a44")], names=False)))
check(Fraction(1, 2) * 7 * Fraction("14.2") + 12 * Fraction("16.2") + Fraction(1, 2) * 10 * Fraction("2.6"), Fraction("257.1"), "p.131 Q5")
q103.append(Q("Exercise 5", 131, "Given that GE = 10 m and HF = 2.6 m. Find the total area of the shaded parts.", "There are 3 shaded parts: a triangle on top, a parallelogram, and a small shape on the left.",
              ["Triangle AHB: base 14.2 m, height 7 m: ½ × 7 × 14.2 = <b>49.7 m²</b>", "Parallelogram HBCD: base 16.2 m, height 12 m: 12 × 16.2 = <b>194.4 m²</b>",
               "The blue shape GHEF: ½ × 10 × 2.6 = <b>13 m²</b>", "Total = 49.7 + 194.4 + 13 = <b>257.1 m²</b>"],
              "257.1 m²", "Add the 3 shaded parts.",
              FIG({"A": [60, 30], "B": [170, 30], "C": [290, 100], "D": [180, 170], "H": [60, 90], "G": [20, 130], "F": [60, 170], "E": [120, 140]},
                  [poly(["A", "B", "H"], ORANGE), poly(["H", "B", "C", "D"], GREEN), poly(["G", "H", "E", "F"], BLUE), ra("A", "B", "H"),
                   lab("A", "B", "14.2 m", -14), lab("H", "A", "7 m", 16), lab("B", "C", "16.2 m", -14), txt(270, 150, "12 m", 14)])))
flash103 = [
    {"front": "Area of rectangle", "back": "length × width"}, {"front": "Area of triangle", "back": "½ × base × height"},
    {"front": "Area of parallelogram", "back": "base × height"}, {"front": "Area of trapezium", "back": "½ × height × (sum of the parallel sides)"},
    {"front": "Area of kite", "back": "½ × the product of the diagonals"}, {"front": "How to find the area of a polygon", "back": "Split it into shapes you know and add"},
    {"front": "Square of area 81 cm². Side?", "back": "9 cm"}, {"front": "Regular octagon = 8 triangles of 4.4 m². Area?", "back": "35.2 m²"},
]
match103 = [["Rectangle 6 × 5", "30 m²"], ["Square 6 × 6", "36 m²"], ["Triangle ½ × 5 × 4", "10 m²"], ["Trapezium ½ × 5 × (19 + 26)", "112.5 m²"],
            ["Parallelogram 22 × 11", "242 cm²"], ["Kite ½ × 11.5 × 20", "115 cm²"], ["Square area 49", "Side 7"], ["Square area 81", "Side 9"]]
quiz103 = [
    {"q": "A triangle (10 m²), a rectangle (30 m²) and a square (36 m²) make a figure. Total area?", "options": ["76 m²", "66 m²", "86 m²", "46 m²"]},
    {"q": "Trapezium: height 5 m, parallel sides 19 m and 26 m. Area?", "options": ["112.5 m²", "225 m²", "50 m²", "130 m²"]},
    {"q": "A square has area 81 cm². How long is each side?", "options": ["9 cm", "40.5 cm", "8 cm", "20.25 cm"]},
    {"q": "Parallelogram: base 22 cm, height 11 cm. Area?", "options": ["242 cm²", "121 cm²", "66 cm²", "286 cm²"]},
    {"q": "Kite with diagonals 20 cm and 11.5 cm. Area?", "options": ["115 cm²", "230 cm²", "31.5 cm²", "63 cm²"]},
    {"q": "Square 12 m × 12 m, white parts 108 m². Shaded?", "options": ["36 m²", "144 m²", "108 m²", "252 m²"]},
    {"q": "Rectangle 18 m × 10.2 m. Area?", "options": ["183.6 m²", "28.2 m²", "56.4 m²", "180 m²"]},
    {"q": "8 equal triangles of 4.4 m² each. Total?", "options": ["35.2 m²", "12.4 m²", "32.2 m²", "44 m²"]},
    {"q": "Rectangle 15 cm × 5 cm. Area?", "options": ["75 cm²", "20 cm²", "40 cm²", "150 cm²"]},
    {"q": "Right triangle with short sides 7 cm and 9 cm. Area?", "options": ["31.5 cm²", "63 cm²", "16 cm²", "32 cm²"]},
]
check(15 * 5, 75, "q"); check(144 - 108, 36, "q"); check(4.4 * 8, 35.2, "q")
sections.append({"id": "10-3", "title": "Finding Area of a Polygon", "short": "3. Area", "pages": "p.124 to 131",
                 "learn": learn103, "questions": q103, "flash": flash103, "match": match103, "quiz": quiz103})

# ==================================================================
# 10.4 WORD PROBLEMS (p.132 to 140)
# ==================================================================
check(144 / 6, 24, "p.132 Q1"); check(6.25 * 8, 50, "p.132 Q2"); check(Fraction(8 * 9, 2) + 7 * Fraction("8.2") + 41 * Fraction("11.3"), Fraction("556.7"), "p.133 Q3")
check(144 - 4 * 0, 144, "x"); check(12 - 4, 8, "p.134 CG"); check(16 * 2 / 8, 4, "p.134 JE")
check(12 * 6, 72, "p.133 Q4 perim"); check(Fraction(1, 2) * 12 * Fraction("10.4"), Fraction("62.4"), "p.133 Q4 tri"); check(Fraction("62.4") * 6, Fraction("374.4"), "p.133 Q4 area")
FHEX = FIG({"_o": [150, 130], "_p0": [250, 130], "_p1": [200, 43.4], "_p2": [100, 43.4], "_p3": [50, 130], "_p4": [100, 216.6], "_p5": [200, 216.6], "_m": [150, 216.6]},
           [poly(["_p0", "_p1", "_p2", "_p3", "_p4", "_p5"], ORANGE), seg("_o", "_p0"), seg("_o", "_p1"), seg("_o", "_p2"), seg("_o", "_p3"), seg("_o", "_p4"), seg("_o", "_p5"),
            seg("_o", "_m", True), lab("_p4", "_p5", "12 cm", 16), txt(186, 185, "10.4 cm", 14)], names=False)
learn104 = [
    L("Idea", "Read, draw, solve", "<p>1. Read the problem twice.<br>2. Draw or look at the shape and write the numbers on it.<br>3. Perimeter → add the sides. Area → split into shapes.<br>4. Write the unit!</p>", None, 132),
    L("Example", "A hexagonal tray", "<p>The perimeter of a regular hexagonal tray is 144 cm. Each side?</p><p>6 equal sides share 144 cm: 144 ÷ 6 = <b>24 cm</b></p>", None, 132),
    L("Example", "Fencing an octagon", "<p>Emma's octagon playground has sides of 6.25 m. Fence length?</p><p>6.25 × 8 = <b>50 m</b></p>", None, 132),
    L("Idea", "Working backward", "<p>If you know an area, you can find a length.</p><p>Square of 144 m²: 12 × 12 = 144, so the side is 12 m.</p>"
      "<p>Triangle of 16 m² with base 8 m: ½ × 8 × height = 16, so 4 × height = 16 and height = <b>4 m</b>.</p>", None, 134),
    L("Example", "Garden in 3 parts", "<p>① triangle ½ × 8 × 9 = 36 m²<br>② rectangle 7 × 8.2 = 57.4 m²<br>③ rectangle 41 × 11.3 = 463.3 m²</p><p>Total = <b>556.7 m²</b></p>", None, 133),
    L("Example", "6 triangles make a hexagon", "<p>John has 6 acrylic sheets in the shapes of equilateral triangles. Each side of each triangle is 12 cm long with the height of 10.4 cm. "
      "If he made a hexagon out of these triangles, find the perimeter and area of this hexagon.</p>"
      "<p class=\"small\">The book says 10 cm, but the picture and the working use 10.4 cm.</p>"
      "<p>Perimeter: the hexagon has 6 outside sides of 12 cm. 12 × 6 = <b>72 cm</b></p>"
      "<p>Area of 1 triangle: ½ × 12 × 10.4 = 62.4 cm²<br>Area of 6 triangles: 62.4 × 6 = <b>374.4 cm²</b></p>", FHEX, 133),
]
q104 = []
check(29 * Fraction("64.5") + 26 * Fraction("10.2"), Fraction("2135.7"), "p.135 area"); check(round(38.5 * 2 + 32 * 4 + 10.2 * 2, 2), 225.4, "p.135 perim")
fplank = FIG({"_a": [30, 20], "_b": [270, 20], "_c": [230, 110], "_d": [230, 140], "_e": [270, 230], "_f": [30, 230], "_g": [70, 140], "_h": [70, 110]},
             [poly(["_a", "_b", "_c", "_d", "_e", "_f", "_g", "_h"], ORANGE), seg("_h", "_c", True), seg("_g", "_d", True), lab("_a", "_b", "38.5 cm", -14), lab("_h", "_c", "26 cm", 14),
              lab("_g", "_h", "10.2 cm", 22), lab("_d", "_e", "32 cm", -16), tick("_a", "_h", 3), tick("_b", "_c", 3), tick("_d", "_e", 3), tick("_f", "_g", 3), txt(290, 70, "29 cm", 14)], names=False)
q104.append(Q("Do and Learn 1", 135, "A wooden plank is in the shape as shown below. Find its area and perimeter.",
              "The top and bottom are the same trapezium. The middle is a rectangle.",
              ["Top trapezium: height 29 cm, parallel sides 38.5 cm and 26 cm.", "½ × 29 × (38.5 + 26) = ½ × 29 × 64.5 = 935.25 cm². The bottom one is the same: 2 × 935.25 = <b>1,870.5 cm²</b>",
               "Middle rectangle: 26 × 10.2 = <b>265.2 cm²</b>", "Area = 1,870.5 + 265.2 = <b>2,135.7 cm²</b>",
               "Perimeter: 2 sides of 38.5 cm, 4 slanted sides of 32 cm, 2 sides of 10.2 cm.", "(38.5 × 2) + (32 × 4) + (10.2 × 2) = 77 + 128 + 20.4 = <b>225.4 cm</b>"],
              "Area = 2,135.7 cm², perimeter = 225.4 cm", "2 trapeziums and a rectangle make the plank.", fplank))
check(2 * Fraction(6 * 6, 2), 36, "p.135 cut"); check(144 - 36, 108, "p.135 pent")
q104.append(Q("Do and Learn 2", 135, "Peter cut a square piece of paper into the shape of a pentagon as shown below. Find the area of the pieces of paper that he cut off and the area of the pentagon.",
              "The cuts go from the middle of the top to the middle of each side. Each cut-off piece is a right triangle.",
              ["The square has sides of 12 cm. The middle of each side is 6 cm from the corner.", "Each cut-off triangle: ½ × 6 × 6 = <b>18 cm²</b>",
               "2 pieces were cut off: 2 × 18 = <b>36 cm²</b>", "Square = 12 × 12 = 144 cm². Pentagon = 144 - 36 = <b>108 cm²</b>"],
              "Cut-off paper = 36 cm², pentagon = 108 cm²", "144 - 36 = 108.",
              FIG({"_a": [60, 30], "_b": [240, 30], "_c": [240, 210], "_d": [60, 210], "_m": [150, 30], "_l": [60, 120], "_r": [240, 120]},
                  [poly(["_a", "_b", "_c", "_d"], "#ffffff"), poly(["_m", "_r", "_c", "_d", "_l"], BLUE), lab("_a", "_b", "12 cm", -14), tick("_a", "_m"), tick("_m", "_b"), tick("_a", "_l"), tick("_b", "_r")], names=False)))
check(Fraction(7, 2) * Fraction("7.5") + 18 * 18, Fraction("350.25"), "p.136 Q1")
q104.append(Q("Exercise 1", 136, "Siti cut a piece of paper into the shape as shown below. What is the area of this piece of paper?", "It is a square (②) with a triangle (①) on top.",
              ["Square ②: 18 × 18 = <b>324 cm²</b>", "Triangle ①: the base is 18 - 11 = 7 cm and the height is 7.5 cm. ½ × 7 × 7.5 = <b>26.25 cm²</b>", "Total = 26.25 + 324 = <b>350.25 cm²</b>"],
              "350.25 cm²", "A square and a triangle added together.",
              FIG({"_a": [60, 70], "_b": [160, 70], "_c": [225, 20], "_d": [225, 70], "_e": [225, 210], "_f": [60, 210]},
                  [poly(["_a", "_b", "_c", "_d", "_e", "_f"], YELLOW), seg("_b", "_d", True), lab("_a", "_b", "11 cm", -14), lab("_f", "_e", "18 cm", 16), lab("_c", "_d", "7.5 cm", -16), txt(195, 60, "①", 16, "#c2185b"), txt(140, 145, "②", 22, "#c2185b")], names=False)))
check(round(12.5 + 8.2 + 12.5 + 9 + 19.8 + 8.2 + 19.8 + 9, 2), 99, "p.136 Q2")
q104.append(Q("Exercise 2", 136, "Dad has a wire in the shape of a polygon as shown below. Find the length of this wire.", "Use the tick marks. Add all 8 sides.",
              ["Pairs of equal sides: 12.5 cm (2), 9 cm (2), 19.8 cm (2), 8.2 cm (2).", "Length = 12.5 + 8.2 + 12.5 + 9 + 19.8 + 8.2 + 19.8 + 9", "= <b>99 cm</b>"],
              "99 cm", "(12.5 + 9 + 19.8 + 8.2) × 2 = 49.5 × 2 = 99.",
              {"w": 300, "h": 230, "pts": {}, "items": outline([[40, 20], [95, 90], [145, 90], [200, 20], [200, 70], [150, 190], [90, 190], [40, 70]], GREEN,
                [(0, 1, "12.5 cm"), (3, 4, "9 cm"), (4, 5, "19.8 cm"), (5, 6, "8.2 cm")], [(0, 1, 1), (2, 3, 1), (1, 2, 2), (5, 6, 2), (3, 4, 3), (7, 0, 3), (4, 5, 4), (6, 7, 4)])}))
check(9 + 4 + 6, 19, "p.137 h"); check(19 + 22 + 19 + 22, 82, "p.137 Q3")
q104.append(Q("Exercise 3", 137, "Peter joins 2 squares and a rectangle to make a figure as shown below. What is the perimeter of the figure?",
              "All the corners are right angles. Push the steps out to make a big rectangle: it has the same perimeter.",
              ["The total height = 9 + 4 + 6 = <b>19 m</b>.", "The total width = <b>22 m</b> (the rectangle).",
               "Every corner is a right angle, so the perimeter is the same as a 22 m by 19 m rectangle.", "19 + 22 + 19 + 22 = <b>82 m</b>"],
              "82 m", "Sliding the steps outward makes a 22 m by 19 m rectangle with the same perimeter.",
              {"w": 320, "h": 200, "pts": {}, "items": [poly([[60, 20], [132, 20], [132, 92], [60, 92]], GREEN), poly([[20, 92], [196, 92], [196, 124], [20, 124]], YELLOW),
                poly([[20, 124], [68, 124], [68, 172], [20, 172]], BLUE), txt(96, 62, "B", 18, "#1f2a44"), txt(108, 113, "C", 18, "#1f2a44"), txt(44, 153, "A", 18, "#1f2a44"),
                lab([60, 20], [132, 20], "9 m", -14), lab([20, 124], [68, 124], "6 m", 14), lab([20, 92], [196, 92], "22 m", -12), lab([196, 92], [196, 124], "4 m", -16)]}))
check(10 * 10 + 8 * 7, 156, "p.137 area"); check(156 * 12000, 1872000, "p.137 Q4")
q104.append(Q("Exercise 4", 137, "The measurements of a plot of land are given as shown below. Each square meter of land costs 12,000 baht. How much does the plot of land cost? (All sides of the plot of land meet at right angles.)",
              "Find the area of the square and the rectangle, then multiply by the price.",
              ["Square: 10 × 10 = <b>100 m²</b>", "Rectangle: 8 × 7 = <b>56 m²</b>", "Total area = 100 + 56 = <b>156 m²</b>", "Cost = 156 × 12,000 = <b>1,872,000 baht</b>"],
              "1,872,000 baht", "156 square meters at 12,000 baht each.",
              {"w": 300, "h": 180, "pts": {}, "items": [poly([[20, 20], [140, 20], [140, 140], [20, 140]], GREEN), poly([[140, 20], [236, 20], [236, 104], [140, 104]], GREEN),
                lab([20, 20], [140, 20], "10 m", -14), lab([140, 20], [236, 20], "8 m", -14), lab([20, 20], [20, 140], "10 m", 18), lab([236, 20], [236, 104], "7 m", -16)]}))
check(150 / 5, 30, "p.138 set"); check(2 * 30, 60, "p.138 Q5")
q104.append(Q("Exercise 5", 138, "A wire 150 cm long is bent to form 4 equilateral triangles as shown below. Triangles ABC and ACG have the same area. Triangles CDE and CEF have the same area. Find the length of ABCFE.",
              "Count how many long sides and how many short sides use up the 150 cm.",
              ["The big triangles use <b>5 long sides</b> (AB, BC, CG, GA and AC).", "The small triangles use <b>5 short sides</b> (CD, DE, EF, FC and CE).",
               "So 5 sets of (long + short) = 150 cm. 1 set = 150 ÷ 5 = <b>30 cm</b>.", "ABCFE = AB + BC + CF + FE = 2 long + 2 short = 2 sets = 2 × 30 = <b>60 cm</b>"],
              "60 cm", "ABCFE uses 2 long and 2 short sides.",
              FIG({"A": [20, 130], "B": [80, 26], "C": [140, 130], "G": [80, 234], "D": [170, 78], "E": [200, 130], "F": [170, 182]},
                  [poly(["A", "B", "C", "G"], GREEN), seg("A", "C"), poly(["C", "D", "E", "F"], GREEN), seg("C", "E")], 240, 250)))
check(350 + 62 + 70.5 + 62 + 70.5 + 62 + 79 + 96 + 70.5 + 470, 1392.5, "p.138 fence"); check(1500 - 1392.5, 107.5, "p.138 Q6")
q104.append(Q("Exercise 6", 138, "Alex owns a land in the shape as shown below. Its perimeter is 1,500 m. If she is fencing the land and only one part is left (AB), what is the length of this unfinished part of the fence?",
              "Add all the sides that are finished. Take that away from 1,500 m.",
              ["Finished fence = 350 + 62 + 70.5 + 62 + 70.5 + 62 + 79 + 96 + 70.5 + 470", "= <b>1,392.5 m</b>", "Unfinished part AB = 1,500 - 1,392.5 = <b>107.5 m</b>"],
              "107.5 m", "The whole fence is 1,500 m, and 1,392.5 m is done.",
              FIG({"_1": [100, 20], "_2": [240, 20], "_3": [240, 208], "_4": [212, 208], "_5": [212, 170], "B": [180, 170], "A": [120, 140], "_8": [120, 115], "_9": [148, 115], "_10": [148, 85], "_11": [100, 85]},
                  [seg("_1", "_2"), seg("_2", "_3"), seg("_3", "_4"), seg("_4", "_5"), seg("_5", "B"), seg("B", "A", True), seg("A", "_8"), seg("_8", "_9"), seg("_9", "_10"), seg("_10", "_11"), seg("_11", "_1"),
                   lab("_1", "_2", "350 m", -14), lab("_2", "_3", "470 m", -22), lab("_3", "_4", "70.5 m", 16), lab("_4", "_5", "96 m", 18), lab("_5", "B", "79 m", -14), lab("_11", "_1", "62 m", 18)], 300, 230)))
check(9 * 23 + Fraction(16, 2) * (41 + 33) + Fraction(12 * 7, 2), 841, "p.139 Q7")
q104.append(Q("Exercise 7", 139, "Janice has a wooden sheet in the shape of a polygon as shown below. Find its area.", "Split it into ① a rectangle, ② a trapezium and ③ a triangle.",
              ["① Rectangle: 9 × 23 = <b>207 cm²</b>", "② Trapezium: height 16 cm, parallel sides 15 + 12 + 14 = 41 cm and 42 - 9 = 33 cm.",
               "½ × 16 × (41 + 33) = 8 × 74 = <b>592 cm²</b>", "③ Triangle: base 12 cm, height 23 - 16 = 7 cm. ½ × 12 × 7 = <b>42 cm²</b>", "Total = 207 + 592 + 42 = <b>841 cm²</b>"],
              "841 cm²", "A rectangle, a trapezium and a triangle added together.",
              {"w": 340, "h": 190, "pts": {}, "items": [poly([[20, 20], [74, 20], [74, 62], [164, 62], [200, 20], [236, 62], [320, 62], [272, 158], [20, 158]], PURPLE),
                seg([74, 62], [74, 158], True), seg([164, 62], [236, 62], True), seg([272, 62], [272, 158], True), lab([20, 20], [74, 20], "9 cm", -14), lab([20, 158], [20, 20], "23 cm", 20),
                lab([74, 62], [164, 62], "15 cm", -12), lab([236, 62], [320, 62], "14 cm", -12), txt(200, 78, "12 cm", 13), lab([20, 158], [272, 158], "42 cm", 16), txt(300, 115, "16 cm", 13),
                txt(47, 100, "①", 18, "#c2185b"), txt(170, 115, "②", 18, "#c2185b"), txt(200, 50, "③", 15, "#c2185b")]}))
check(Fraction(17 * 4, 2), 34, "p.139 ABC"); check(Fraction(17 * 30, 2), 255, "p.139 AEG"); check(Fraction(13 * 13, 2), Fraction(169, 2), "p.139 CDE")
check(17 * 17 + 13 * 13 - 34 - 255 - Fraction(169, 2), Fraction(169, 2), "p.139 Q8")
q104.append(Q("Exercise 8", 139, "A polygonal piece of paper was painted with 2 colors as shown. Find the area of the green part. (The 2 squares have sides 17 cm and 13 cm.)",
              "Find the 2 squares. Take away the 3 orange triangles.",
              ["2 squares: (17 × 17) + (13 × 13) = 289 + 169 = <b>458 cm²</b>", "Triangle ABC: BC = 17 - 13 = 4 cm. ½ × 17 × 4 = <b>34 cm²</b>",
               "Triangle AEG: base GE = 17 + 13 = 30 cm, height 17 cm. ½ × 17 × 30 = <b>255 cm²</b>", "Triangle CDE: ½ × 13 × 13 = <b>84.5 cm²</b>",
               "Green = 458 - 34 - 255 - 84.5 = <b>84.5 cm²</b>"],
              "84.5 cm²", "The squares minus the 3 orange triangles.",
              FIG({"A": [20, 20], "B": [156, 20], "C": [156, 52], "D": [260, 52], "E": [260, 156], "F": [156, 156], "G": [20, 156]},
                  [poly(["A", "B", "C", "D", "E", "G"], ORANGE), poly(["A", "C", "E"], GREEN), seg("C", "F", True), lab("G", "F", "17 cm", 16), lab("F", "E", "13 cm", 16)])))
q104.append(Q("Exercise 9 (a)", 140, "Noah created a hexagon by using 8 right triangles as shown below. Find: (a) the length of AB", "Count the short sides along the top.",
              ["Along the top there are 3 short sides of the triangles.", "AB = 3 + 3 + 3 = <b>9 cm</b>"], "9 cm", "3 sides of 3 cm."))
check(9 + 4 + 5 + 5 + 3 + 4, 30, "p.140 b")
q104.append(Q("Exercise 9 (b)", 140, "Noah created a hexagon by using 8 right triangles as shown below. Find: (b) the perimeter of hexagon ABCDEF", "Go round the outside: AB, BC, CD, DE, EF, FA.",
              ["AB = 9 cm, BC = 4 cm, CD = 5 cm, DE = 5 cm, EF = 3 cm, FA = 4 cm.", "Perimeter = 3 + 3 + 3 + 4 + 5 + 5 + 3 + 4 = <b>30 cm</b>"],
              "30 cm", "Only the outside edges count."))
check(Fraction(3 * 4, 2) * 8, 48, "p.140 c")
q104.append(Q("Exercise 9 (c)", 140, "Noah created a hexagon by using 8 right triangles as shown below. Find: (c) the area of hexagon ABCDEF", "The hexagon is made of 8 equal right triangles.",
              ["Each right triangle: ½ × 3 × 4 = <b>6 cm²</b>", "8 triangles: 6 × 8 = <b>48 cm²</b>"], "48 cm²", "8 triangles of 6 cm² each."))
u9 = 25
f140 = FIG({"A": [20, 20], "B": [20 + 9 * u9, 20], "C": [20 + 9 * u9, 20 + 4 * u9], "D": [20 + 6 * u9, 20 + 8 * u9], "E": [20 + 3 * u9, 20 + 4 * u9], "F": [20, 20 + 4 * u9],
            "_p": [20 + 3 * u9, 20], "_q": [20 + 6 * u9, 20], "_r": [20 + 6 * u9, 20 + 4 * u9]},
           [poly(["A", "B", "C", "D", "E", "F"], PINK), seg("A", "E"), seg("_p", "E"), seg("_q", "E"), seg("_q", "_r"), seg("_q", "C"), seg("D", "_r"),
            lab("A", "_p", "3 cm", -14), lab("_p", "_q", "3 cm", -14), lab("_q", "B", "3 cm", -14), lab("F", "A", "4 cm", 18), lab("B", "C", "4 cm", -18),
            lab("F", "E", "3 cm", 14), lab("E", "D", "5 cm", 16), lab("D", "C", "5 cm", 16)])
for qq in q104:
    if qq["label"].startswith("Exercise 9"):
        qq["fig"] = f140
flash104 = [
    {"front": "Regular hexagon, perimeter 144 cm. Each side?", "back": "144 ÷ 6 = 24 cm"}, {"front": "Octagon, side 6.25 m. Fence?", "back": "50 m"},
    {"front": "Square area 144 m². Side?", "back": "12 m"}, {"front": "Steps with all right angles: perimeter trick", "back": "Push the steps out to make a rectangle"},
    {"front": "Cost of land", "back": "Area × price for each m²"}, {"front": "Unfinished fence", "back": "Perimeter - finished part"},
    {"front": "8 right triangles of 6 cm²", "back": "48 cm²"}, {"front": "Trapezium area", "back": "½ × height × (sum of the parallel sides)"},
]
match104 = [["144 ÷ 6", "24 cm"], ["6.25 × 8", "50 m"], ["12 × 12", "144 m²"], ["156 × 12,000", "1,872,000 baht"], ["1,500 - 1,392.5", "107.5 m"],
            ["150 ÷ 5", "30 cm"], ["½ × 3 × 4 × 8", "48 cm²"], ["19 + 22 + 19 + 22", "82 m"]]
quiz104 = [
    {"q": "A regular hexagon has perimeter 144 cm. Each side?", "options": ["24 cm", "36 cm", "18 cm", "864 cm"]},
    {"q": "Sophie fences an octagon with sides of 6.25 m. Fence length?", "options": ["50 m", "37.5 m", "25 m", "48 m"]},
    {"q": "A square garden has area 144 m². Each side?", "options": ["12 m", "36 m", "72 m", "14 m"]},
    {"q": "Land of 156 m² costs 12,000 baht per m². Total?", "options": ["1,872,000 baht", "187,200 baht", "18,720,000 baht", "168,000 baht"]},
    {"q": "Fence perimeter 1,500 m; 1,392.5 m is done. Left?", "options": ["107.5 m", "117.5 m", "2,892.5 m", "100 m"]},
    {"q": "A triangle has area 16 m² and base 8 m. Height?", "options": ["4 m", "2 m", "8 m", "128 m"]},
    {"q": "A 12 cm square with two 18 cm² corners cut off. Area left?", "options": ["108 cm²", "126 cm²", "144 cm²", "36 cm²"]},
    {"q": "A shape with all right angles is 22 m wide and 19 m tall overall. Perimeter?", "options": ["82 m", "41 m", "418 m", "164 m"]},
    {"q": "8 right triangles, each ½ × 3 × 4. Total area?", "options": ["48 cm²", "96 cm²", "24 cm²", "12 cm²"]},
    {"q": "Square 18 cm × 18 cm. Area?", "options": ["324 cm²", "72 cm²", "36 cm²", "182 cm²"]},
]
check(16 / 4, 4, "q"); check(144 - 36, 108, "q"); check(18 * 18, 324, "q")
sections.append({"id": "10-4", "title": "Word Problems", "short": "4. Word Problems", "pages": "p.132 to 140",
                 "learn": learn104, "questions": q104, "flash": flash104, "match": match104, "quiz": quiz104})

# ==================================================================
# UNIT 10 CHALLENGE (p.141 to 146)
# ==================================================================
check(80 + 60, 140, "p.141 BCD"); check((180 - 140) / 2, 20, "p.141 DBC"); check((180 - 80) / 2, 50, "p.141 ABE"); check(180 - 80 - 50 - 20, 30, "p.141 EBD")
check(round(2.9 * 8 + 2 * 14, 2), 51.2, "p.143 P"); check(Fraction(2 * (2 + 6), 2) * 4 + 2 * 2 * 2 + 2 * 4, 48, "p.143 A")
check(Fraction(6 * 4, 2) + 10 * Fraction("9.5") + 6 * 19, 221, "p.145 right"); check(Fraction(6 * 5, 2) + 95 + 114, 224, "p.145 Janice")
u = 18
pts143 = {k: [20 + x * u, 20 + y * u] for k, (x, y) in {"A": (0, 2), "B": (2, 0), "C": (2, 2), "D": (4, 2), "E": (4, 0), "F": (6, 2), "G": (8, 2), "H": (10, 0), "I": (10, 2), "J": (12, 2),
                                                       "K": (12, 0), "L": (14, 2), "M": (14, 4), "N": (12, 6), "O": (10, 6), "P": (8, 4), "Q": (6, 4), "R": (4, 6), "S": (4, 4), "T": (2, 4), "U": (2, 6), "V": (0, 4)}.items()}
f143 = FIG(pts143, [poly(list("ABCDEFGHIJKLMNOPQRSTUV"), ORANGE), lab("E", "F", "2.9 m"), lab("F", "G", "2 m", -12), txt(20 + 7 * u, 20 + 6 * u + 34, "14 m", 15), txt(20 + 14 * u + 28, 20 + 3 * u + 5, "6 m", 15)],
           w=300, h=180, name_off={k: [0, -8] if pts143[k][1] <= 20 + 2 * u else [0, 22] for k in pts143})
f145 = FIG({"_a": [40, 50], "_t": [88, 18], "_b": [136, 50], "_c": [136, 130], "_d": [260, 130], "_e": [260, 210], "_f": [40, 210]},
           [poly(["_a", "_t", "_b", "_c", "_d", "_e", "_f"], BLUE), seg("_a", "_b", True), seg("_t", [88, 50], True), lab("_t", "_b", "5 cm"), txt(70, 46, "4 cm", 12), lab("_c", "_d", "10 cm", -14),
            lab("_d", "_e", "9.5 cm", -18), lab("_f", "_e", "16 cm", 16)], names=False)
qch = [
    Q("Let's Think Along", 141, "In the figure, ABCE is a rhombus and CDE is an equilateral triangle. ∠EAB = 80°. Find ∠EBD.", "Find ∠DBC and ∠ABE first. Then use the angles in triangle ABC... along the straight edge.",
      ["Opposite angles of a rhombus are equal: ∠BCE = 80°", "∠BCD = 80° + 60° = <b>140°</b> (CDE is equilateral)",
       "BC = CE = CD, so triangle BCD is isosceles: ∠DBC = (180° - 140°) ÷ 2 = <b>20°</b>", "Triangle ABE is isosceles (AB = AE): ∠ABE = (180° - 80°) ÷ 2 = <b>50°</b>",
       "∠ABC = 180° - 80° = 100°, so ∠EBD = 100° - 50° - 20° = <b>30°</b> (the key writes 180° - 80° - 50° - 20°)"],
      "∠EBD = 30°", "∠ABC (100°) = ∠ABE (50°) + ∠EBD (30°) + ∠DBC (20°).",
      FIG({"A": [40, 140], "B": [120, 30], "C": [250, 70], "D": [290, 190], "E": [170, 180]},
          [poly(["A", "B", "C", "E"], GREEN), poly(["C", "D", "E"], GREEN), seg("B", "E"), seg("B", "D"), ang("A", "E", "B", "80°", 22)])),
    Q("Problem Solving", 143, "Find the perimeter and area of the following figure.", "It is made of 4 trapeziums, 2 squares and 1 rectangle. Use the tick marks for the perimeter.",
      ["<b>Perimeter:</b> there are 8 slanted sides of 2.9 m and 14 sides of 2 m.", "(2.9 × 8) + (2 × 14) = 23.2 + 28 = <b>51.2 m</b>",
       "<b>Area:</b> 4 trapeziums ①③⑤⑦, each ½ × 2 × (2 + 6) = 8 m², so 4 × 8 = <b>32 m²</b>", "2 squares ②④, each 2 × 2 = 4 m², so <b>8 m²</b>",
       "1 rectangle ⑥: 2 × 4 = <b>8 m²</b>", "Area = 32 + 8 + 8 = <b>48 m²</b>"],
      "Perimeter = 51.2 m, area = 48 m²", "The figure is 22 sides long all round and made of 7 simple shapes.", f143),
    Q("Math Journal", 145, "Janice was finding the area of this polygon and got 224 cm². Do you think the solution done by Janice is correct? If not, in what part is not correct? Then correct it.",
      "Look at the triangle on top. Which number is its height?",
      ["Janice used 5 cm for the triangle's height. But 5 cm is the slanted side!", "The real height is the dashed line: <b>4 cm</b>.",
       "Triangle = ½ × 6 × 4 = <b>12 cm²</b>", "Area = 12 + (10 × 9.5) + (6 × 19) = 12 + 95 + 114 = <b>221 cm²</b>"],
      "No. She used the wrong height for the triangle. The correct area is 221 cm².", "The height must meet the base at a right angle.", f145),
]
sections.append({"id": "10-ch", "title": "Unit 10 Challenge", "short": "⭐ Challenge", "pages": "p.141 to 146",
                 "learn": [L("Idea", "Unit 10 big ideas", "<p><b>Angles:</b> triangle 180°, quadrilateral 360°, pentagon 540°, hexagon 720°, octagon 1,080°.</p>"
                             "<p><b>Perimeter:</b> add all sides (use × for equal sides).</p><p><b>Area:</b> split into shapes you know.</p>", None, 146),
                           L("Idea", "Check the height", "<p>The height of a triangle meets the base at a <b>right angle</b>. A slanted side is <b>not</b> the height.</p>", f145, 145)],
                 "questions": qch, "flash": flash101[:5] + flash103[:5],
                 "match": match101[:4] + match103[:4], "quiz": quiz101[:4] + quiz102[:3] + quiz103[:3] + quiz104[:2]})

unit = {"unit": "10", "title": "Area and Perimeter of Polygons", "pages": "p.105 to 146", "sections": sections,
        "expectedPages": {"10-1": [106, 107, 114, 115, 116, 117], "10-2": [120, 121, 122, 123], "10-3": [127, 128, 129, 130, 131],
                          "10-4": [135, 136, 137, 138, 139, 140], "10-ch": [141, 143, 145]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit10.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit10.json ({n} guided questions, {len(sections)} sections).")
