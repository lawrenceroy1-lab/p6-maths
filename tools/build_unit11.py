"""Builds content/unit11.json for Unit 11: Circumference and Area of Circles (book pages 147 to 180).

Every circumference and area is calculated with the SAME value of pi the book uses for that
question (22/7 or 3.14) and compared with the answer key using check().
Run:  python3 tools/build_unit11.py
"""
import contextlib
import io
import json
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, PROBLEMS  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    from build_unit09 import FIG, poly, seg, lab, ra, tick, txt, num, Q, L  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
SQ = "²"
P7 = Fr(22, 7)
P314 = Fr("3.14")
PI_TXT = {P7: "22/7", P314: "3.14"}
TAKE = {P7: "(Take π ≈ 22/7.)", P314: "(Take π ≈ 3.14.)"}


def r2(x):
    """Round to 2 decimal places like the book."""
    return round(float(x) + 1e-12, 2)


def n2(x):
    return num(r2(x))


def times_pi(x, pi):
    """Steps for pi × x, the way a child would work it out. Returns (steps, exact value)."""
    x = Fr(str(x)) if not isinstance(x, Fr) else x
    v = pi * x
    if pi == P7:
        q = x / 7
        if q.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100):
            return [f"{num(x)} ÷ 7 = {num(q)}", f"22 × {num(q)} = <b>{n2(v)}</b>"], v
        return [f"22 × {num(x)} = {num(22 * x)}", f"{num(22 * x)} ÷ 7 ≈ <b>{n2(v)}</b>"], v
    return [f"3.14 × {num(x)} = <b>{n2(v)}</b>"], v


def circ(label, page, kind, val, pi, key, unit, fig, q=None, extra=None):
    """Circumference from a diameter (kind 'd') or a radius (kind 'r')."""
    val = Fr(str(val))
    steps = []
    if kind == "d":
        steps.append(f"The line goes right across through O, so the <b>diameter is {num(val)} {unit}</b>.")
        steps.append(f"Circumference = π × diameter ≈ {PI_TXT[pi]} × {num(val)}")
        s, v = times_pi(val, pi)
    else:
        steps.append(f"The line goes from O to the edge, so the <b>radius is {num(val)} {unit}</b>.")
        steps.append(f"Circumference = 2 × π × radius ≈ 2 × {PI_TXT[pi]} × {num(val)}")
        steps.append(f"2 × {num(val)} = {num(2 * val)} (that is the diameter)")
        s, v = times_pi(2 * val, pi)
    steps += s
    check(r2(v), key, f"p.{page} {label}")
    return Q(label, page, q or f"O is the center. Find the circumference of the circle. {TAKE[pi]}",
             "Circumference = π × diameter. If you have the radius, double it first.",
             steps + (extra or []), f"Circumference ≈ {num(key)} {unit}", f"The circumference is about {PI_TXT[pi]} times the diameter.", fig)


def area(label, page, kind, val, pi, key, unit, fig, q=None, part=Fr(1), part_name="circle", in_pi=False):
    """Area of a circle (or a half / quarter) from radius or diameter."""
    val = Fr(str(val))
    steps = []
    if kind == "d":
        r = val / 2
        steps.append(f"The diameter is {num(val)} {unit}. Radius = {num(val)} ÷ 2 = <b>{num(r)} {unit}</b>")
    else:
        r = val
        steps.append(f"The radius is <b>{num(r)} {unit}</b>.")
    frac = {Fr(1): "", Fr(1, 2): "½ × ", Fr(1, 4): "¼ × ", Fr(1, 3): "⅓ × "}[part]
    rr = r * r
    if in_pi:
        steps.append(f"Area = {frac}π × r × r = {frac}π × {num(r)} × {num(r)}")
        steps.append(f"{num(r)} × {num(r)} = {num(rr)}")
        v = part * rr
        steps.append(f"Area = <b>{num(v)}π {unit}{SQ}</b>")
        check(v, key, f"p.{page} {label}")
        ans = f"{num(key)}π {unit}{SQ}"
    else:
        steps.append(f"Area of {part_name} = {frac}π × r × r ≈ {frac}{PI_TXT[pi]} × {num(r)} × {num(r)}")
        steps.append(f"{num(r)} × {num(r)} = {num(rr)}")
        s, v = times_pi(rr, pi)
        steps += s
        if part != 1:
            v = v * part
            steps.append(f"{frac}{n2(pi * rr)} = <b>{n2(v)}</b>")
        check(r2(v), key, f"p.{page} {label}")
        ans = f"Area ≈ {num(key)} {unit}{SQ}"
    return Q(label, page, q or (f"O is the center. Find the area of the circle. {TAKE[pi]}" if not in_pi else "O is the center. Find the area of the circle. Leave the answer in terms of π."),
             "Area of a circle = π × radius × radius. If you have the diameter, halve it first!", steps, ans,
             "Area uses the radius, multiplied by itself, then by π.", fig)


def cfig(kind, val, unit, fill=BLUE, label_o=True):
    c = [160, 120]
    pts = {"O": c} if label_o else {"_O": c}
    items = [{"t": "circle", "c": c, "r": 90, "fill": fill}, {"t": "dot", "p": c}]
    if kind == "d":
        items += [seg([70, 120], [250, 120]), lab([70, 120], [250, 120], f"{num(val)} {unit}", -14)]
    else:
        items += [seg(c, [250, 120]), lab(c, [250, 120], f"{num(val)} {unit}", -14)]
    return FIG(pts, items, 320, 240, name_off={"O": [-12, 20]})


sections = []

# ==================================================================
# 11.1 CIRCUMFERENCE OF A CIRCLE (p.148 to 156)
# ==================================================================
check(r2(2 * P7 * 7), 44, "p.150 Q2"); check(r2(P7 * 21), 66, "p.151 Q3"); check(r2(Fr(1, 2) * P314 * 10 + 10), 25.7, "p.151 semi")
check(r2(Fr(1, 4) * P314 * 10 + 10), 17.85, "p.152 quarter"); check(r2(Fr(3, 4) * 2 * P7 * 8 + 16), 53.71, "p.152 Q6")
fsemi = FIG({"_c": [160, 160]}, [{"t": "sector", "c": [160, 160], "r": 100, "a0": 180, "a1": 360, "fill": PINK}, lab([60, 160], [260, 160], "10 cm", 16)], names=False)
fquart = FIG({"_c": [80, 190]}, [{"t": "sector", "c": [80, 190], "r": 150, "a0": 270, "a1": 360, "fill": GREEN}, lab([80, 190], [230, 190], "5 cm", 16), lab([80, 40], [80, 190], "5 cm", 18)], names=False)
learn111 = [
    L("Idea", "What is π (pi)?", "<p>Measure any circle. Divide the <b>circumference</b> by the <b>diameter</b>. You always get about <b>3.14</b>.</p>"
      "<p>This number is called <b>π</b> (we say \"pie\"). We use π ≈ <b>3.14</b> or π ≈ <b>22/7</b>.</p>"
      "<p>The question always tells you which one to use.</p>", None, 150),
    L("Idea", "Circumference formula", "<p><b>Circumference = π × diameter</b></p><p>The diameter is 2 radii, so also: <b>Circumference = 2 × π × radius</b></p>"
      "<p>So the circumference is a bit more than <b>3 times</b> the diameter.</p>", cfig("r", 7, "m"), 150),
    L("Example", "Radius 7 m (π ≈ 22/7)", "<p>Circumference = 2 × 22/7 × 7</p><p>22/7 × 7 = 22, and 2 × 22 = <b>44 m</b></p>", cfig("r", 7, "m"), 150),
    L("Example", "Diameter 21 cm (π ≈ 22/7)", "<p>Circumference = 22/7 × 21</p><p>21 ÷ 7 = 3, and 22 × 3 = <b>66 cm</b></p>", cfig("d", 21, "cm", GREEN), 151),
    L("Idea", "Semicircles and quarter circles", "<p>An <b>arc</b> is part of the circumference.</p>"
      "<p>Semicircle: arc = ½ of the circumference. Perimeter = arc + diameter.</p><p>Quarter circle: arc = ¼ of the circumference. Perimeter = arc + radius + radius.</p>", fsemi, 151),
    L("Example", "Semicircle, diameter 10 cm (π ≈ 3.14)", "<p>Arc = ½ × 3.14 × 10 = 15.7 cm</p><p>Perimeter = 15.7 + 10 = <b>25.7 cm</b> (don't forget the straight edge!)</p>", fsemi, 151),
    L("Example", "Quarter circle, radius 5 cm (π ≈ 3.14)", "<p>Arc = ¼ × 3.14 × 10 = 7.85 cm</p><p>Perimeter = 7.85 + 5 + 5 = <b>17.85 cm</b></p>", fquart, 152),
]
q111 = []
q111.append(circ("Do and Learn (a)", 153, "r", 40, P314, 251.2, "cm", cfig("r", 40, "cm", ORANGE), q="Find the circumference of the object. Radius = 40 cm. (Take π ≈ 3.14.)"))
q111.append(circ("Do and Learn (b)", 153, "d", 20.5, P314, 64.37, "cm", cfig("d", 20.5, "cm", YELLOW), q="Find the circumference of the object. Diameter = 20.5 cm. (Take π ≈ 3.14.)"))
for part, kind, val, est, calc in [("(a)", "d", 10, 30, 31.4), ("(b)", "d", 17, 51, 53.38), ("(c)", "r", 6.5, 39, 40.82)]:
    d = val if kind == "d" else 2 * val
    check(3 * d, est, f"p.154 est {part}")
    q111.append(circ(f"Exercise 1 {part}", 154, kind, val, P314, calc, "cm", cfig(kind, val, "cm", GREEN),
                     q="O is the center. Estimate the circumference of the circle. Then use a calculator to find the circumference. (Take π ≈ 3.14.)",
                     extra=[f"<b>Estimate:</b> the circumference is about 3 times the diameter: 3 × {num(d)} = <b>{num(est)} cm</b>"]))
    q111[-1]["answer"] = f"Estimated ≈ {num(est)} cm, calculated ≈ {num(calc)} cm"
q111.append(circ("Exercise 2 (a)", 155, "d", 14, P7, 44, "cm", cfig("d", 14, "cm", PINK)))
q111.append(circ("Exercise 2 (b)", 155, "r", 8.4, P7, 52.8, "cm", cfig("r", 8.4, "cm", PINK)))
q111.append(circ("Exercise 3 (a)", 155, "d", 18, P314, 56.52, "cm", cfig("d", 18, "cm", BLUE)))
q111.append(circ("Exercise 3 (b)", 155, "r", 6, P314, 37.68, "cm", cfig("r", 6, "cm", BLUE)))
check(r2(Fr(3, 4) * 2 * P7 * 21 + 42), 141, "p.156 (a)"); check(r2(Fr(3, 4) * 2 * P7 * 14), 66, "p.156 (b) arc"); check(66 + 28, 94, "p.156 (b)")
f156a = FIG({"O": [150, 120]}, [{"t": "sector", "c": [150, 120], "r": 90, "a0": 180, "a1": 450, "fill": "#ffffff"}, seg([60, 120], [150, 120]),
                                lab([60, 120], [150, 120], "21 cm", 14), ra([150, 120], [150, 30], [240, 120])], name_off={"O": [8, -8]})
f156b = FIG({"O": [150, 120]}, [{"t": "sector", "c": [150, 120], "r": 90, "a0": 180, "a1": 360, "fill": "#ffffff"},
                                {"t": "sector", "c": [240, 120], "r": 90, "a0": 90, "a1": 180, "fill": "#ffffff"},
                                lab([60, 120], [150, 120], "14 cm", 14), lab([240, 120], [240, 210], "14 cm", -18)], name_off={"O": [0, -8]})
q111.append(Q("Exercise 4 (a)", 156, "Find the perimeter of the figure. (Take π ≈ 22/7.)<br>The figure is made up of 3 quarter circles. O is the center of a circle.",
              "3 quarter circles make ¾ of a whole circle. Then add the 2 straight radii.",
              ["The radius is <b>21 cm</b>.", "The curved part is ¾ of the circumference: ¾ × 2 × 22/7 × 21",
               "2 × 21 = 42, 42 ÷ 7 = 6, 22 × 6 = 132 (the whole circumference)", "¾ of 132: 132 ÷ 4 = 33, 33 × 3 = <b>99 cm</b>",
               "The 2 straight edges are radii: 21 + 21 = 42 cm", "Perimeter ≈ 99 + 42 = <b>141 cm</b>"],
              "Perimeter ≈ 141 cm", "Curved part + the 2 straight radii.", f156a))
q111.append(Q("Exercise 4 (b)", 156, "Find the perimeter of the figure. (Take π ≈ 22/7.)<br>The figure is made up of a semicircle and a quarter circle. O is the center of a circle.",
              "A semicircle and a quarter circle with the same radius make ¾ of a circle.",
              ["The radius is <b>14 cm</b>.", "Half + a quarter = ¾ of the circumference: ¾ × 2 × 22/7 × 14",
               "2 × 14 = 28, 28 ÷ 7 = 4, 22 × 4 = 88 (the whole circumference)", "¾ of 88: 88 ÷ 4 = 22, 22 × 3 = <b>66 cm</b>",
               "Add the 2 straight edges: 14 + 14 = 28 cm", "Perimeter ≈ 66 + 28 = <b>94 cm</b>"],
              "Perimeter ≈ 94 cm", "¾ of the circumference plus 2 radii.", f156b))
flash111 = [
    {"front": "π (pi)", "back": "Circumference ÷ diameter ≈ 3.14 or 22/7"}, {"front": "Circumference formula", "back": "π × diameter (or 2 × π × radius)"},
    {"front": "Arc", "back": "A curved part of the circumference"}, {"front": "Perimeter of a semicircle", "back": "½ of the circumference + the diameter"},
    {"front": "Perimeter of a quarter circle", "back": "¼ of the circumference + radius + radius"},
    {"front": "Diameter 14 cm, π ≈ 22/7. Circumference?", "back": "44 cm"}, {"front": "Diameter 10 cm, π ≈ 3.14. Circumference?", "back": "31.4 cm"},
    {"front": "Quick estimate of a circumference", "back": "About 3 × the diameter"},
]
check(r2(P7 * 14), 44, "f"); check(r2(P314 * 10), 31.4, "f")
match111 = [["d = 14 cm (22/7)", "44 cm"], ["d = 21 cm (22/7)", "66 cm"], ["r = 7 m (22/7)", "44 m"], ["d = 10 cm (3.14)", "31.4 cm"],
            ["d = 18 cm (3.14)", "56.52 cm"], ["r = 6 cm (3.14)", "37.68 cm"], ["r = 40 cm (3.14)", "251.2 cm"], ["d = 20 cm (3.14)", "62.8 cm"]]
match111[2] = ["r = 3.5 m (22/7)", "22 m"]
for a, b in match111:
    v = float(a.split("=")[1].split()[0]); pi = P7 if "22/7" in a else P314
    c = pi * Fr(str(v)) * (2 if a.startswith("r") else 1)
    check(r2(c), float(b.split()[0]), "match 11.1")
quiz111 = [
    {"q": "Diameter 14 cm. Circumference? (π ≈ 22/7)", "options": ["44 cm", "88 cm", "22 cm", "154 cm"]},
    {"q": "Radius 7 m. Circumference? (π ≈ 22/7)", "options": ["44 m", "22 m", "154 m", "88 m"]},
    {"q": "Diameter 10 cm. Circumference? (π ≈ 3.14)", "options": ["31.4 cm", "62.8 cm", "78.5 cm", "15.7 cm"]},
    {"q": "Radius 6 cm. Circumference? (π ≈ 3.14)", "options": ["37.68 cm", "18.84 cm", "113.04 cm", "36 cm"]},
    {"q": "Circumference ÷ diameter is about…", "options": ["3.14", "2", "0.5", "6.28"]},
    {"q": "A semicircle has diameter 10 cm. Its perimeter is the arc plus…", "options": ["The diameter", "Nothing", "The radius", "2 diameters"]},
    {"q": "Semicircle, diameter 10 cm. Perimeter? (π ≈ 3.14)", "options": ["25.7 cm", "15.7 cm", "31.4 cm", "20.7 cm"]},
    {"q": "Quarter circle, radius 5 cm. Perimeter? (π ≈ 3.14)", "options": ["17.85 cm", "7.85 cm", "12.85 cm", "31.4 cm"]},
    {"q": "Estimate the circumference of a circle with diameter 17 cm.", "options": ["About 51 cm", "About 17 cm", "About 34 cm", "About 289 cm"]},
    {"q": "3 quarter circles of radius 21 cm. Curved length? (π ≈ 22/7)", "options": ["99 cm", "132 cm", "66 cm", "141 cm"]},
]
check(r2(2 * P314 * 6), 37.68, "q"); check(r2(Fr(3, 4) * 2 * P7 * 21), 99, "q")
sections.append({"id": "11-1", "title": "Circumference of a Circle", "short": "1. Circumference", "pages": "p.148 to 156",
                 "learn": learn111, "questions": q111, "flash": flash111, "match": match111, "quiz": quiz111})

# ==================================================================
# 11.2 AREA OF A CIRCLE (p.157 to 165)
# ==================================================================
check(49, 7 * 7, "p.160 a"); check(r2(P7 * 49), 154, "p.160 b"); check(r2(P314 * 25), 78.5, "p.160 Q2")
check(r2(P314 * 225 - P314 * 64), 505.54, "p.160 Q3"); check(r2(Fr(1, 2) * P7 * 441), 693, "p.161 Q4"); check(r2(Fr(1, 4) * P314 * 16), 12.56, "p.161 Q5")
fring = FIG({"_c": [160, 120]}, [{"t": "circle", "c": [160, 120], "r": 100, "fill": ORANGE}, {"t": "circle", "c": [160, 120], "r": 53, "fill": "#ffffff"},
                                 seg([160, 120], [260, 120]), lab([213, 120], [260, 120], "15 cm", -14), seg([160, 120], [160, 67]), lab([160, 120], [160, 67], "8 cm", 18)], names=False)
learn112 = [
    L("Idea", "Area of a circle", "<p>Cut a circle into many thin slices and line them up. They make a shape like a <b>rectangle</b>.</p>"
      "<p>Its length is half the circumference (π × r) and its width is the radius (r).</p><p><b>Area of a circle = π × r × r</b> (we write πr²)</p>", None, 158),
    L("Example", "Radius 7 cm", "<p>In terms of π: π × 7 × 7 = <b>49π cm²</b></p><p>With π ≈ 22/7: 22/7 × 49 = 22 × 7 = <b>154 cm²</b></p>", cfig("r", 7, "cm", GREEN), 160),
    L("Example", "A circle on a 10 cm square", "<p>The circle fits the square, so the diameter is 10 cm and the radius is 5 cm.</p><p>Area ≈ 3.14 × 5 × 5 = 3.14 × 25 = <b>78.5 cm²</b></p>", None, 160),
    L("Idea", "Watch out: radius, not diameter!", "<p>The formula uses the <b>radius</b>. If you are given the diameter, <b>halve it first</b>.</p>"
      "<p>Diameter 42 cm → radius 21 cm.</p>", None, 161),
    L("Example", "Shaded ring", "<p>Big circle: 3.14 × 15 × 15 = 706.5 cm²<br>Small circle: 3.14 × 8 × 8 = 200.96 cm²</p><p>Shaded part = 706.5 - 200.96 = <b>505.54 cm²</b></p>", fring, 160),
    L("Example", "Semicircle and quarter circle", "<p>Semicircle, diameter 42 cm (π ≈ 22/7): ½ × 22/7 × 21 × 21 = <b>693 cm²</b></p>"
      "<p>Quarter circle, radius 4 cm (π ≈ 3.14): ¼ × 3.14 × 4 × 4 = <b>12.56 cm²</b></p>", None, 161),
]
q112 = []
q112.append(area("Do and Learn 1", 162, "d", 6, P314, 9, "cm", cfig("d", 6, "cm", YELLOW, False), q="Find the area of a circular coaster of diameter 6 cm. Give the answer in terms of π.", in_pi=True))
q112.append(area("Do and Learn 2 (a)", 162, "r", 14, P7, 616, "cm", cfig("r", 14, "cm", GREEN)))
q112.append(area("Do and Learn 2 (b)", 162, "d", 42, P7, 1386, "m", cfig("d", 42, "m", GREEN)))
q112.append(area("Do and Learn 3 (a)", 162, "r", 18, P314, 1017.36, "cm", cfig("r", 18, "cm", BLUE)))
q112.append(area("Do and Learn 3 (b)", 162, "d", 26, P314, 530.66, "m", cfig("d", 26, "m", BLUE)))
for part, kind, val, key, unit in [("(a)", "r", 7, 49, "cm"), ("(b)", "r", 9.2, 84.64, "cm"), ("(c)", "d", 12, 36, "cm"), ("(d)", "d", 38, 361, "m")]:
    q112.append(area(f"Exercise 1 {part}", 163, kind, val, P314, key, unit, cfig(kind, val, unit, PINK), in_pi=True))
q112.append(area("Exercise 2 (a)", 164, "r", 7.7, P7, 186.34, "cm", cfig("r", 7.7, "cm", ORANGE)))
q112.append(area("Exercise 2 (b)", 164, "d", 28, P7, 616, "m", cfig("d", 28, "m", ORANGE)))
q112.append(area("Exercise 3", 164, "r", 4, P314, 50.24, "m", cfig("r", 4, "m", PURPLE, False), q="Find the area of the circle of radius 4 m. (Take π ≈ 3.14.)"))
q112.append(area("Exercise 4", 164, "d", 34, P314, 907.46, "cm", cfig("d", 34, "cm", PURPLE, False), q="Find the area of the circle of diameter 34 cm. (Take π ≈ 3.14.)"))
q112.append(area("Exercise 5 (a)", 165, "d", 28, P7, 308, "cm",
                 FIG({"_c": [160, 150]}, [{"t": "sector", "c": [160, 150], "r": 110, "a0": 180, "a1": 360, "fill": BLUE}, lab([50, 150], [270, 150], "28 cm", 16)], names=False),
                 q="Find the area of the semicircle. (Take π ≈ 22/7.)", part=Fr(1, 2), part_name="semicircle"))
q112.append(area("Exercise 5 (b)", 165, "r", 21, P7, 346.5, "cm",
                 FIG({"_c": [80, 190]}, [{"t": "sector", "c": [80, 190], "r": 150, "a0": 270, "a1": 360, "fill": PURPLE}, lab([80, 190], [230, 190], "21 cm", 16)], names=False),
                 q="Find the area of the quarter circle. (Take π ≈ 22/7.)", part=Fr(1, 4), part_name="quarter circle"))
check(r2(P314 * 36), 113.04, "p.165 Q6")
f165 = FIG({"_c": [160, 120]}, [{"t": "sector", "c": [160, 120], "r": 100, "a0": 90, "a1": 270, "fill": GREEN},
                                {"t": "sector", "c": [160, 20], "r": 100, "a0": 0, "a1": 90, "fill": GREEN},
                                {"t": "sector", "c": [160, 220], "r": 100, "a0": 270, "a1": 360, "fill": GREEN},
                                seg([160, 20], [160, 220]), lab([160, 20], [160, 220], "12 m", -18)], names=False)
q112.append(Q("Exercise 6", 165, "The figure is made up of a semicircle and 2 identical quarter circles. Find the area of the figure. (Take π ≈ 3.14.)",
              "Move the 2 quarter circles to fill the missing half. What whole shape do you get?",
              ["The 2 quarter circles make another semicircle. With the big semicircle, the figure has the same area as <b>1 whole circle</b>.",
               "The diameter is 12 m, so the radius = 12 ÷ 2 = <b>6 m</b>.", "Area ≈ 3.14 × 6 × 6", "6 × 6 = 36", "3.14 × 36 = <b>113.04 m²</b>"],
              "Area ≈ 113.04 m²", "The pieces fit together into one circle of radius 6 m.", f165))
flash112 = [
    {"front": "Area of a circle", "back": "π × r × r (πr²)"}, {"front": "Area of a semicircle", "back": "½ × π × r × r"},
    {"front": "Area of a quarter circle", "back": "¼ × π × r × r"}, {"front": "Given the diameter, first…", "back": "Halve it to get the radius"},
    {"front": "Radius 7 cm. Area in terms of π?", "back": "49π cm²"}, {"front": "Radius 7 cm, π ≈ 22/7. Area?", "back": "154 cm²"},
    {"front": "Radius 10 cm, π ≈ 3.14. Area?", "back": "314 cm²"}, {"front": "Shaded ring", "back": "Big circle - small circle"},
]
check(r2(P314 * 100), 314, "f")
match112 = [["r = 7 (22/7)", "154"], ["r = 14 (22/7)", "616"], ["r = 5 (3.14)", "78.5"], ["r = 10 (3.14)", "314"],
            ["r = 4 (3.14)", "50.24"], ["r = 6 (3.14)", "113.04"], ["r = 21 (22/7)", "1,386"], ["r = 3 in terms of π", "9π"]]
for a, b in match112[:7]:
    v = Fr(a.split("=")[1].split()[0]); pi = P7 if "22/7" in a else P314
    check(r2(pi * v * v), float(b.replace(",", "")), "match 11.2")
quiz112 = [
    {"q": "Radius 7 cm. Area? (π ≈ 22/7)", "options": ["154 cm²", "44 cm²", "49 cm²", "308 cm²"]},
    {"q": "Diameter 14 cm. Area? (π ≈ 22/7)", "options": ["154 cm²", "616 cm²", "44 cm²", "88 cm²"]},
    {"q": "Radius 10 cm. Area? (π ≈ 3.14)", "options": ["314 cm²", "62.8 cm²", "31.4 cm²", "628 cm²"]},
    {"q": "Radius 6 cm. Area in terms of π?", "options": ["36π cm²", "12π cm²", "6π cm²", "72π cm²"]},
    {"q": "Diameter 12 cm. Area in terms of π?", "options": ["36π cm²", "144π cm²", "12π cm²", "24π cm²"]},
    {"q": "Semicircle with radius 14 cm. Area? (π ≈ 22/7)", "options": ["308 cm²", "616 cm²", "154 cm²", "44 cm²"]},
    {"q": "Quarter circle with radius 4 cm. Area? (π ≈ 3.14)", "options": ["12.56 cm²", "50.24 cm²", "6.28 cm²", "25.12 cm²"]},
    {"q": "Radius 5 cm. Area? (π ≈ 3.14)", "options": ["78.5 cm²", "31.4 cm²", "15.7 cm²", "314 cm²"]},
    {"q": "To find the area, you multiply π by…", "options": ["radius × radius", "diameter × diameter", "radius × 2", "the circumference"]},
    {"q": "A semicircle and 2 quarter circles of the same radius make…", "options": ["1 whole circle", "Half a circle", "2 circles", "A square"]},
]
check(r2(P7 * 196 / 2), 308, "q"); check(r2(P314 * 16 / 4), 12.56, "q")
sections.append({"id": "11-2", "title": "Area of a Circle", "short": "2. Area", "pages": "p.157 to 165",
                 "learn": learn112, "questions": q112, "flash": flash112, "match": match112, "quiz": quiz112})

# ==================================================================
# 11.3 WORD PROBLEMS (p.166 to 174)
# ==================================================================
check(r2(P314 * 49), 153.86, "p.166 Q1"); check(r2(P314 * Fr("12.5")), 39.25, "p.166 Q2"); check(r2(P7 * 42 * 2), 264, "p.167 a")
check(r2(Fr(1, 2) * P7 * 42 * 42 - P7 * 21 * 21), 1386, "p.168 b"); check(r2(P314 * 26 * 26 - P314 * 24 * 24 + 400), 714, "p.168 Q4")
check(r2(Fr(1, 2) * P7 * 16) + r2(Fr(1, 2) * P7 * 9) + r2(Fr(1, 2) * P7 * 25) + 24, 102.57, "p.169 a"); check(r2(Fr(1, 2) * P7 * (8 + 6 + 10)), 37.71, "p.169 b")
ftrack = FIG({"_a": [80, 40], "_b": [240, 40]}, [{"t": "sector", "c": [80, 120], "r": 80, "a0": 90, "a1": 270, "fill": ORANGE}, {"t": "sector", "c": [240, 120], "r": 80, "a0": 270, "a1": 450, "fill": ORANGE},
                                                poly([[80, 40], [240, 40], [240, 200], [80, 200]], ORANGE), {"t": "sector", "c": [80, 120], "r": 70, "a0": 90, "a1": 270, "fill": GREEN},
                                                {"t": "sector", "c": [240, 120], "r": 70, "a0": 270, "a1": 450, "fill": GREEN}, poly([[80, 50], [240, 50], [240, 190], [80, 190]], GREEN),
                                                txt(160, 125, "100 m", 15), txt(40, 125, "48 m", 14), txt(160, 35, "2 m", 13)], names=False)
learn113 = [
    L("Idea", "Circumference or area?", "<p>Going <b>around</b> the edge (a fence, a trim, a wheel turning) → <b>circumference</b>.</p>"
      "<p>Covering the <b>inside</b> (paint, paper, grass) → <b>area</b>.</p>", None, 166),
    L("Example", "Emma's paper circle", "<p>Diameter 14 cm, so radius 7 cm. Area ≈ 3.14 × 7 × 7 = <b>153.86 cm²</b></p>", None, 166),
    L("Example", "A circular field", "<p>Diameter 12.5 m. Circumference ≈ 3.14 × 12.5 = <b>39.25 m</b></p>", None, 166),
    L("Idea", "Wheels", "<p>In <b>1 complete turn</b>, a wheel rolls a distance equal to its <b>circumference</b>.</p><p>Distance = circumference × number of turns</p>", None, 172),
    L("Idea", "Running tracks", "<p>The 2 curved ends of a track make <b>1 whole ring</b>. The straight parts are rectangles.</p>"
      "<p>Track area = (big circle - small circle) + the rectangles.</p>", ftrack, 168),
    L("Example", "Track 2 m wide", "<p>Big circle radius 26 m, small circle radius 24 m.</p><p>Curved parts ≈ 3.14 × 26 × 26 - 3.14 × 24 × 24 = 2,122.64 - 1,808.64 = 314 m²</p>"
      "<p>Straight parts = 2 × 100 × 2 = 400 m². Track ≈ 314 + 400 = <b>714 m²</b></p>", ftrack, 168),
]
q113 = []
check(r2(Fr(1, 2) * P7 * 100 - 100), 57.14, "p.170 Q1")
q113.append(Q("Do and Learn 1", 170, "The figure shows a triangle inside a semicircle. The base of the triangle is 20 cm. Find the shaded area of the figure. (Correct to 2 decimal places.) (Take π ≈ 22/7.)",
              "Shaded = semicircle - triangle. The triangle's height is a radius.",
              ["The base (20 cm) is the diameter, so the radius = <b>10 cm</b>.", "Semicircle = ½ × 22/7 × 10 × 10 = ½ × 2,200/7 = 1,100/7 ≈ <b>157.14 cm²</b>",
               "Triangle: base 20 cm, height 10 cm (a radius). ½ × 20 × 10 = <b>100 cm²</b>", "Shaded ≈ 157.14 - 100 = <b>57.14 cm²</b>"],
              "≈ 57.14 cm²", "Semicircle minus the triangle inside it.",
              FIG({"_c": [160, 160]}, [{"t": "sector", "c": [160, 160], "r": 120, "a0": 180, "a1": 360, "fill": GREEN}, poly([[40, 160], [280, 160], [160, 40]], "#ffffff"),
                                       seg([160, 40], [160, 160], True), lab([40, 160], [280, 160], "20 cm", 16)], names=False)))
check(r2(P314 * 20 + 40), 102.8, "p.170 Q2a"); check(r2(400 - P314 * 100), 86, "p.170 Q2b")
f170 = FIG({"_a": [70, 120], "_b": [170, 120]}, [poly([[70, 70], [170, 70], [170, 170], [70, 170]], PURPLE),
                                                 {"t": "circle", "c": [70, 120], "r": 50, "fill": "#ffffff"}, {"t": "circle", "c": [170, 120], "r": 50, "fill": "#ffffff"},
                                                 seg([70, 70], [170, 70]), seg([70, 170], [170, 170]), seg([170, 120], [170, 70], True), lab([170, 120], [170, 70], "10 cm", -16)], names=False)
q113.append(Q("Do and Learn 2 (a)", 170, "The figure shows 2 identical circles touching each other. The radius of each circle is 10 cm. (Take π ≈ 3.14.)<br>(a) Find the perimeter of the shaded part.",
              "The shaded part has 2 straight edges and 2 curved edges. The 2 curves make 1 whole circle.",
              ["The 2 curved edges are 2 half circles = 1 whole circumference.", "Diameter = 2 × 10 = 20 cm. Circumference ≈ 3.14 × 20 = <b>62.8 cm</b>",
               "The 2 straight edges are each a diameter: 20 + 20 = <b>40 cm</b>", "Perimeter ≈ 62.8 + 40 = <b>102.8 cm</b>"],
              "≈ 102.8 cm", "1 circumference plus 2 diameters.", f170))
q113.append(Q("Do and Learn 2 (b)", 170, "The figure shows 2 identical circles touching each other. The radius of each circle is 10 cm. (Take π ≈ 3.14.)<br>(b) Find the area of the shaded part.",
              "Shaded = the square between the centers - the 2 half circles (1 whole circle).",
              ["The square between the 2 centers is 20 cm by 20 cm: 20 × 20 = <b>400 cm²</b>", "The 2 white half circles make 1 circle: 3.14 × 10 × 10 = <b>314 cm²</b>",
               "Shaded ≈ 400 - 314 = <b>86 cm²</b>"],
              "≈ 86 cm²", "Square minus one whole circle.", f170))
check(r2(2 * P7 * Fr("26.5")), 166.57, "p.171 Q1")
q113.append(Q("Exercise 1", 171, "The radius of a circular dining table is 26.5 cm. If we want to decorate the circumference of the table with a piece of cloth skirting, how long should this cloth be? (Take π ≈ 22/7.) Correct your answer to 2 decimal places.",
              "The cloth goes all the way round, so find the circumference.",
              ["Circumference = 2 × π × radius ≈ 2 × 22/7 × 26.5", "2 × 26.5 = 53 (the diameter)", "22 × 53 = 1,166", "1,166 ÷ 7 ≈ <b>166.57 cm</b>"],
              "≈ 166.57 cm", "The cloth must be as long as the circumference."))
check(r2(P314 * 38), 119.32, "p.171 Q2 C"); check(r2(P314 * 361), 1133.54, "p.171 Q2 A")
q113.append(Q("Exercise 2", 171, "The diameter of a circular wood sheet is 38 cm. Find the circumference and area of this wood sheet. (Take π ≈ 3.14.)",
              "Circumference uses the diameter. Area uses the radius (halve the diameter).",
              ["Circumference ≈ 3.14 × 38 = <b>119.32 cm</b>", "Radius = 38 ÷ 2 = <b>19 cm</b>", "19 × 19 = 361", "Area ≈ 3.14 × 361 = <b>1,133.54 cm²</b>"],
              "Circumference ≈ 119.32 cm, area ≈ 1,133.54 cm²", "Two different formulas: π × d and π × r × r."))
check(r2(2 * P314 * 25), 157, "p.172 Q3 turn"); check(r2(157 * 50 / 100), 78.5, "p.172 Q3")
q113.append(Q("Exercise 3", 172, "A wheel of radius 25 cm made 50 complete turns. Find the distance covered. Give the answer in meters. (Take π ≈ 3.14.)",
              "1 turn = 1 circumference.", ["1 turn ≈ 2 × 3.14 × 25 = 3.14 × 50 = <b>157 cm</b>", "50 turns ≈ 50 × 157 = <b>7,850 cm</b>", "In meters: 7,850 ÷ 100 = <b>78.5 m</b>"],
              "≈ 78.5 m", "50 circumferences, changed from cm to m.", cfig("r", 25, "cm", "#E0E0E0", False)))
check(r2(P7 * 49), 154, "p.172 Q4 C"); check(924 / 154, 6, "p.172 Q4")
q113.append(Q("Exercise 4", 172, "A wheel of diameter 49 cm made some complete turns and covered a distance of 924 cm. How many complete turns did it make? (Take π ≈ 22/7.)",
              "Find the distance for 1 turn, then see how many fit into 924 cm.",
              ["1 turn = circumference ≈ 22/7 × 49", "49 ÷ 7 = 7, 22 × 7 = <b>154 cm</b>", "Number of turns = 924 ÷ 154 = <b>6</b>"],
              "6 complete turns", "6 × 154 = 924.", cfig("d", 49, "cm", "#E0E0E0", False)))
check(r2(Fr(1, 3) * 2 * P314 * 9 + 18), 36.84, "p.173 Q5a"); check(r2(Fr(1, 3) * P314 * 81), 84.78, "p.173 Q5b")
f173 = FIG({"_c": [160, 120]}, [{"t": "circle", "c": [160, 120], "r": 90, "fill": "#ffffff"}, {"t": "sector", "c": [160, 120], "r": 90, "a0": 270, "a1": 390, "fill": PURPLE},
                                {"t": "sector", "c": [160, 120], "r": 90, "a0": 30, "a1": 150, "fill": "none"}, lab([160, 120], [238, 165], "9 cm", -14)], names=False)
q113.append(Q("Exercise 5 (a)", 173, "A circle with radius 9 cm is divided into 3 equal parts and 1 part is cut out as shown. (Take π ≈ 3.14.)<br>(a) Find the perimeter of the shaded part.",
              "The shaded part has 1 arc (⅓ of the circumference) and 2 radii.",
              ["Whole circumference ≈ 2 × 3.14 × 9 = 3.14 × 18 = 56.52 cm", "Arc = ⅓ of 56.52 = <b>18.84 cm</b>", "Perimeter ≈ 18.84 + 9 + 9 = <b>36.84 cm</b>"],
              "≈ 36.84 cm", "Arc plus 2 radii.", f173))
q113.append(Q("Exercise 5 (b)", 173, "A circle with radius 9 cm is divided into 3 equal parts and 1 part is cut out as shown. (Take π ≈ 3.14.)<br>(b) Find the area of the shaded part.",
              "The shaded part is ⅓ of the whole circle.",
              ["Whole circle ≈ 3.14 × 9 × 9 = 3.14 × 81 = 254.34 cm²", "Shaded = ⅓ of 254.34 = <b>84.78 cm²</b>"],
              "≈ 84.78 cm²", "One third of the circle's area.", f173))
check(r2(28 * 28 + 4 * P7 * 49), 1400, "p.173 Q6")
items = [poly([[60, 60], [200, 60], [200, 200], [60, 200]], GREEN)]
for cx, cy, a0 in [(95, 60, 180), (165, 60, 180), (95, 200, 0), (165, 200, 0), (60, 95, 90), (60, 165, 90), (200, 95, 270), (200, 165, 270)]:
    items.append({"t": "sector", "c": [cx, cy], "r": 35, "a0": a0, "a1": a0 + 180, "fill": GREEN})
items += [lab([60, 200], [130, 200], "14 cm", -16)]
q113.append(Q("Exercise 6", 173, "The figure below shows a handkerchief. Each side of the handkerchief is made up of 2 identical semicircles. Find the area of the handkerchief. (Take π ≈ 22/7.)",
              "A square in the middle, plus 8 semicircles (= 4 whole circles).",
              ["Each semicircle has diameter 14 cm, so the radius is <b>7 cm</b>. The square's side is 14 + 14 = <b>28 cm</b>.",
               "Square = 28 × 28 = <b>784 cm²</b>", "8 semicircles = 4 circles. 1 circle ≈ 22/7 × 7 × 7 = 22 × 7 = <b>154 cm²</b>",
               "4 circles ≈ 4 × 154 = <b>616 cm²</b>", "Handkerchief ≈ 784 + 616 = <b>1,400 cm²</b>"],
              "≈ 1,400 cm²", "A square plus 4 circles.", {"w": 260, "h": 260, "pts": {}, "items": items}))
check(r2(P314 * 169), 530.66, "p.174 big"); check(r2(P314 * 36), 113.04, "p.174 small"); check(4 * Fr(1, 2) * 6 * 6, 72, "p.174 sq")
check(r2(Fr("530.66") - Fr("113.04") + 72), 489.62, "p.174 Q7")
q113.append(Q("Exercise 7", 174, "The figure shows 2 circles and a square inside the smaller circle. The diameter of the bigger circle is 26 cm. The diameter of the smaller circle is 12 cm. Find the total area of the shaded parts. (Take π ≈ 3.14.)",
              "Shaded = big circle - small circle + the square.",
              ["Big circle: radius 13 cm. 3.14 × 13 × 13 = 3.14 × 169 = <b>530.66 cm²</b>", "Small circle: radius 6 cm. 3.14 × 6 × 6 = 3.14 × 36 = <b>113.04 cm²</b>",
               "The square's diagonals are 12 cm. It is 4 triangles of ½ × 6 × 6 = 18 cm², so 4 × 18 = <b>72 cm²</b>",
               "Shaded ≈ 530.66 - 113.04 + 72 = <b>489.62 cm²</b>"],
              "≈ 489.62 cm²", "The ring is shaded, and so is the square inside the small circle.",
              FIG({"_c": [160, 120]}, [{"t": "circle", "c": [160, 120], "r": 100, "fill": ORANGE}, {"t": "circle", "c": [160, 120], "r": 46, "fill": "#ffffff"},
                                       poly([[160, 74], [206, 120], [160, 166], [114, 120]], ORANGE), lab([60, 230], [260, 230], "26 cm", 12), lab([114, 20], [206, 20], "12 cm", -12)], names=False)))
flash113 = [
    {"front": "Fence or trim around a circle", "back": "Use the circumference"}, {"front": "Paint or cover a circle", "back": "Use the area"},
    {"front": "1 complete turn of a wheel", "back": "Rolls 1 circumference"}, {"front": "Distance for many turns", "back": "Circumference × number of turns"},
    {"front": "Number of turns", "back": "Distance ÷ circumference"}, {"front": "Ring area", "back": "Big circle - small circle"},
    {"front": "7,850 cm in m", "back": "78.5 m"}, {"front": "Square area from its diagonals 12 cm", "back": "4 × ½ × 6 × 6 = 72 cm²"},
]
match113 = [["Wheel d = 49 cm (22/7)", "154 cm per turn"], ["924 ÷ 154", "6 turns"], ["50 × 157 cm", "78.5 m"], ["28 × 28", "784 cm²"],
            ["4 × 154", "616 cm²"], ["400 - 314", "86 cm²"], ["3.14 × 38", "119.32 cm"], ["3.14 × 19 × 19", "1,133.54 cm²"]]
quiz113 = [
    {"q": "Lily wants a ribbon around a circular cake. She needs the…", "options": ["Circumference", "Area", "Radius only", "Diameter only"]},
    {"q": "A wheel has circumference 154 cm. How far does it roll in 6 turns?", "options": ["924 cm", "160 cm", "25.67 cm", "1,540 cm"]},
    {"q": "A wheel of radius 25 cm (π ≈ 3.14). Distance in 1 turn?", "options": ["157 cm", "78.5 cm", "1,962.5 cm", "314 cm"]},
    {"q": "Square 20 cm × 20 cm minus a circle of radius 10 cm (π ≈ 3.14)?", "options": ["86 cm²", "314 cm²", "114 cm²", "200 cm²"]},
    {"q": "Circular sheet, diameter 38 cm. Circumference? (π ≈ 3.14)", "options": ["119.32 cm", "59.66 cm", "1,133.54 cm", "238.64 cm"]},
    {"q": "⅓ of a circle with radius 9 cm. Area? (π ≈ 3.14)", "options": ["84.78 cm²", "254.34 cm²", "18.84 cm²", "28.26 cm²"]},
    {"q": "A wheel rolls 924 cm with circumference 154 cm. Turns?", "options": ["6", "7", "5", "8"]},
    {"q": "8 semicircles with the same radius make…", "options": ["4 whole circles", "8 whole circles", "2 whole circles", "16 circles"]},
    {"q": "7,850 cm = ? m", "options": ["78.5 m", "785 m", "7.85 m", "0.785 m"]},
    {"q": "Track: curved parts 314 m² and straight parts 400 m². Total?", "options": ["714 m²", "86 m²", "614 m²", "1,256 m²"]},
]
check(r2(Fr(1, 3) * P314 * 81), 84.78, "q"); check(314 + 400, 714, "q")
sections.append({"id": "11-3", "title": "Word Problems", "short": "3. Word Problems", "pages": "p.166 to 174",
                 "learn": learn113, "questions": q113, "flash": flash113, "match": match113, "quiz": quiz113})

# ==================================================================
# UNIT 11 CHALLENGE (p.175 to 180)
# ==================================================================
check(26 + 8, 34, "p.175 big d"); check(Fr(34) + Fr(13), 47, "p.175 Siti pi"); check(26 + 17, 43, "p.175 Janice pi"); check(47 - 43, 4, "p.175 diff")
check(718 - 14, 704, "p.177 dist"); check(r2(2 * P7 * 7 * 2), 88, "p.178 per 2s"); check(704 / 88, 8, "p.178 turns"); check(8 * 2, 16, "p.178 time")
fpath = FIG({"_a": [40, 40]}, [{"t": "sector", "c": [80, 120], "r": 40, "a0": 0, "a1": 180, "open": True, "color": "#c62828"},
                               {"t": "sector", "c": [160, 120], "r": 40, "a0": 180, "a1": 360, "open": True, "color": "#2e7d32"},
                               {"t": "sector", "c": [240, 120], "r": 40, "a0": 0, "a1": 180, "open": True, "color": "#c62828"},
                               txt(80, 115, "A 26 m", 13), txt(160, 135, "B 26 m", 13), txt(240, 115, "C 26 m", 13), txt(30, 100, "Siti", 14, "#c62828"), txt(295, 100, "Janice", 14, "#2e7d32")], names=False)
fwheels = FIG({"_a": [40, 120], "_b": [280, 120]}, [{"t": "circle", "c": [50, 120], "r": 30, "fill": "#E0E0E0"}, {"t": "circle", "c": [270, 120], "r": 30, "fill": "#E0E0E0"},
                                                    seg([50, 170], [270, 170]), lab([50, 170], [270, 170], "7.18 m", 16), txt(50, 125, "7 cm", 12), txt(270, 125, "7 cm", 12)], names=False)
qch = [
    Q("Let's Think Along", 175, "The figure below shows a path that is 4 m wide throughout. The path is made up of identical small semicircles where the distances A, B and C are 26 m each. Siti and Janice started walking from the opposite ends of the path. Siti walked along the red edge of the path and Janice walked along the green edge of the path. Find the difference in the distance that Siti and Janice walked. Give the answer in terms of π.",
      "Each edge has big semicircles (diameter 26 + 4 + 4) and small ones (diameter 26).",
      ["Big semicircle diameter = 26 + 4 + 4 = <b>34 m</b>. Small semicircle diameter = <b>26 m</b>.",
       "Siti (red) walks 2 big semicircles + 1 small one + the 2 straight ends (17 m + 17 m):",
       "π × 34 + ½ × π × 26 + 34 = 34π + 13π + 34 = <b>47π + 34 m</b>",
       "Janice (green) walks 2 small semicircles + 1 big one + 34 m: π × 26 + ½ × π × 34 + 34 = 26π + 17π + 34 = <b>43π + 34 m</b>",
       "Difference = (47π + 34) - (43π + 34) = <b>4π m</b>"],
      "4π m", "The 34 m of straight ends cancel out, leaving 47π - 43π = 4π.", fpath),
    Q("Problem Solving", 177, "2 identical wheels that are 7.18 m apart have radius 7 cm each as shown. They move toward each other. Each wheel takes 2 seconds to make 1 full turn. How long will it take for the 2 wheels to meet if they rotate at the same rate? (Take π ≈ 22/7.)",
      "Change 7.18 m to cm first. The wheels meet when their edges touch, not their centers.",
      ["7.18 m = 718 cm. The 2 radii (7 cm + 7 cm = 14 cm) are not covered: 718 - 14 = <b>704 cm</b> to cover.",
       "1 turn of 1 wheel ≈ 2 × 22/7 × 7 = 44 cm. Both wheels in 2 seconds: 44 × 2 = <b>88 cm</b>",
       "Number of turns = 704 ÷ 88 = <b>8</b>", "Time = 8 × 2 seconds = <b>16 seconds</b>",
       "<b>Check:</b> 8 turns × 88 cm = 704 cm ✓"],
      "16 seconds", "Together the wheels close 88 cm every 2 seconds, and 704 ÷ 88 = 8.", fwheels),
    Q("Math Journal", 179, "How is the area of a circle related to the area of a rectangle? Janice and Peter do an activity to find out. Both of them use an identical circle with radius r cm. Janice cuts her circle into parts and arranges them as shown. Peter cuts his circle into parts and arranges them as shown. Whose arrangement will show an area that is closer to the area of the rectangle? Explain.",
      "Who cut the circle into more, smaller pieces?",
      ["Peter cut his circle into many small slices. Janice cut hers into a few big slices.",
       "Small slices line up almost straight, so Peter's shape looks almost exactly like a rectangle.",
       "Janice's big slices leave wider gaps, so her shape is not as close to a rectangle."],
      "Peter's arrangement", "The smaller the slices, the closer the shape is to a rectangle of length πr and width r.")]
sections.append({"id": "11-ch", "title": "Unit 11 Challenge", "short": "⭐ Challenge", "pages": "p.175 to 180",
                 "learn": [L("Idea", "Unit 11 big ideas", "<p><b>Circumference</b> = π × d = 2 × π × r.</p><p><b>Area</b> = π × r × r.</p><p>Use the π the question gives: 22/7 or 3.14.</p>", None, 180),
                           L("Example", "Pizza puzzle (p.176)", "<p>A large pizza (diameter 16 cm) has radius 8 cm: area ≈ 3.14 × 64 = 200.96 cm².</p>"
                             "<p>A small pizza (diameter 8 cm) has radius 4 cm: area ≈ 3.14 × 16 = 50.24 cm².</p><p>Double the diameter gives <b>4 times</b> the area!</p>", None, 176)],
                 "questions": qch, "flash": flash111[:4] + flash112[:4] + flash113[:3],
                 "match": match111[:4] + match112[:4], "quiz": quiz111[:4] + quiz112[:4] + quiz113[:2]})
check(r2(P314 * 64), 200.96, "p.176"); check(r2(P314 * 16), 50.24, "p.176")

unit = {"unit": "11", "title": "Circumference and Area of Circles", "pages": "p.147 to 180", "sections": sections,
        "expectedPages": {"11-1": [153, 154, 155, 156], "11-2": [162, 163, 164, 165], "11-3": [170, 171, 172, 173, 174], "11-ch": [175, 177, 179]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit11.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit11.json ({n} guided questions, {len(sections)} sections).")
