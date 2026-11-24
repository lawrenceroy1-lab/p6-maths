"""Builds content/unit12.json for Unit 12: Volume and Capacity (book pages 181 to 214).

Every volume, capacity, length and time is calculated here and compared with the answer key using check().
Run:  python3 tools/build_unit12.py
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
    from build_unit09 import poly, seg, txt, num, Q, L  # noqa: E402
    import build_unit08 as U8  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
WATER = "#81D4FA"
CU = "³"
SQ = "²"
LI = "ℓ"


def F(items, w=340, h=260):
    return {"w": w, "h": h, "pts": {}, "items": items}


def T(x, y, s, size=14, color="#1565c0"):
    return txt(x, y, s, size, color)


def solid(front_units, depth_px, k, ox, oy, fill, water=None, labels=()):
    """Draw a solid by pushing a front shape back (oblique view).
    front_units: corners in book units with y going UP; k: pixels per unit; (ox, oy): bottom-left on screen.
    water: optional polygon (same units) painted on the front face. labels: (x, y, text) in units, drawn at that spot."""
    pts = [[round(ox + x * k, 1), round(oy - y * k, 1)] for x, y in front_units]
    items = U8.prism(pts, depth_px, fill)
    if water:
        items.append(poly([[round(ox + x * k, 1), round(oy - y * k, 1)] for x, y in water], WATER))
    for x, y, s in labels:
        items.append(T(ox + x * k, oy - y * k, s))
    return items


def box(w, h, d, fill, ox=60, oy=200, labels=(), water_h=None):
    """A cuboid w x h (pixels) with depth d (pixels)."""
    items = U8.cuboid(ox, oy - h, w, h, d, fill, hidden=True)
    if water_h:
        items.insert(3, poly([[ox, oy - water_h], [ox + w, oy - water_h], [ox + w, oy], [ox, oy]], WATER))
    for x, y, s in labels:
        items.append(T(x, y, s))
    return items


def iso_cubes(cells, s=28, ox=60, oy=200, fill="#DCE775"):
    """Unit cubes at (x, y=depth, z=height). Drawn back to front so hidden parts are covered."""
    dx, dy = s * 0.55, -s * 0.45
    items = []
    for x, y, z in sorted(cells, key=lambda c: (-c[1], c[2], c[0])):
        X = ox + x * s + y * dx
        Y = oy - z * s + y * dy
        fr = [[X, Y], [X + s, Y], [X + s, Y - s], [X, Y - s]]
        top = [[X, Y - s], [X + s, Y - s], [X + s + dx, Y - s + dy], [X + dx, Y - s + dy]]
        rt = [[X + s, Y], [X + s + dx, Y + dy], [X + s + dx, Y - s + dy], [X + s, Y - s]]
        items += [poly(fr, fill), poly(top, fill), poly(rt, fill)]
    return items


def mult_steps(parts, unit):
    """parts: list of (label, a, b, c). Returns steps and total."""
    steps, total = [], 0
    for lab, a, b, c in parts:
        v = Fr(str(a)) * Fr(str(b)) * Fr(str(c))
        steps.append(f"{lab}: {num(a)} × {num(b)} × {num(c)} = <b>{num(v)} {unit}{CU}</b>")
        total += v
    return steps, total


sections = []

# ==================================================================
# 12.1 VOLUME OF 3D SHAPES MADE UP OF CUBES AND CUBOIDS (p.182 to 196)
# ==================================================================
check(2 * 2 * 2, 8, "p.183 Q2"); check(8 * 4 * 3, 96, "p.183 Q3")
check(Fr(2, 3) * 32 * 18 * 20, 7680, "p.183 Q4 water"); check(32 * 18 * 20, 11520, "p.183 Q4 cap")
check(Fr(840, 70), 12, "p.187 Q1"); check(Fr(1190, 85), 14, "p.187 Q2a"); check(Fr(448, 112), 4, "p.187 Q2b")
check(6 * 6, 36, "p.188 Q3"); check(14 * 14, 196, "p.188 Q4"); check(5 ** 3, 125, "p.188 Q5"); check(8 ** 3, 512, "p.188 Q6")
check(Fr("12") * Fr("1.5") * Fr("4.5") + 4 * Fr("1.5") * Fr("9.5"), 138, "p.189 m1"); check(16 * Fr("1.5") * Fr("4.5") + 4 * Fr("1.5") * 5, 138, "p.189 m2")
f189 = F(solid([(0, 0), (16, 0), (16, 9.5), (12, 9.5), (12, 4.5), (0, 4.5)], 30, 15, 40, 200, ORANGE,
               labels=[(8, -1.1, "16 cm"), (6, 5.2, "12 cm"), (17.6, 5, "9.5 cm"), (-1.6, 2.2, "4.5 cm")]) + [T(290, 210, "1.5 cm deep", 13)])
fcube = F(box(110, 110, 70, BLUE, 90, 210, labels=[(145, 228, "2 cm"), (70, 160, "2 cm"), (240, 205, "2 cm")]))
learn121 = [
    L("Idea", "Volume", "<p><b>Volume</b> is the space a solid takes up. We count it in <b>unit cubes</b> or in cm³ and m³.</p>"
      "<p>A 1 cm cube has a volume of <b>1 cm³</b>.</p>", F(iso_cubes([(0, 0, 0)], 60, 120, 180)), 182),
    L("Idea", "Volume of a cube and a cuboid", "<p><b>Cube:</b> length × length × length</p><p><b>Cuboid:</b> length × width × height</p>"
      "<p>Cube 2 cm by 2 cm by 2 cm: 2 × 2 × 2 = <b>8 cm³</b></p>", fcube, 183),
    L("Idea", "Base area × height", "<p>The area of the bottom face is the <b>base area</b> (length × width).</p>"
      "<p><b>Volume = base area × height</b>, so <b>height = volume ÷ base area</b>.</p>", None, 185),
    L("Example", "Find the height", "<p>Base area 70 cm², volume 840 cm³.</p><p>Height = 840 ÷ 70 = <b>12 cm</b></p>", None, 187),
    L("Idea", "Edge of a cube", "<p>Face area known: which number × itself makes it? 36 = 6 × 6, so the edge is <b>6 cm</b>.</p>"
      "<p>Volume known: which number × itself × itself makes it? 125 = 5 × 5 × 5, so the edge is <b>5 cm</b>.</p>", None, 188),
    L("Idea", "Solids made of cuboids", "<p>Split the solid into cuboids. Find each volume. <b>Add</b> them.</p>"
      "<p>Or find a big cuboid and <b>take away</b> the missing part.</p>", f189, 189),
    L("Example", "Split it into 2 parts", "<p>Part 1: 12 × 1.5 × 4.5 = 81 cm³<br>Part 2: 4 × 1.5 × 9.5 = 57 cm³</p><p>Volume = 81 + 57 = <b>138 cm³</b></p>", f189, 189),
    L("Idea", "Capacity", "<p><b>Capacity</b> is how much a container can hold when full.</p><p>1 ℓ = 1,000 cm³ and 1 m³ = 1,000,000 cm³.</p>", None, 190),
]

q121 = []
recall = [("(a)", [(x, y, z) for x in range(3) for y in range(2) for z in range(2)] + [(0, y, 2) for y in range(2)], 14, "#DCE775",
           "The front has 3 columns and 2 rows, and it is 2 cubes deep: 3 × 2 × 2 = 12. On top at the left there are 2 more cubes: 12 + 2 = <b>14</b>."),
          ("(b)", [(x, y, z) for x in range(2) for y in range(2) for z in range(2)] + [(x, 1, 2) for x in range(2)] + [(x, y, z) for x in (2, 3) for y in (1, 2) for z in range(2)], 18, "#81D4FA",
           "The left block is 2 × 2 × 2 = 8. On top of it at the back are 2 more. The right block is 2 × 2 × 2 = 8. 8 + 2 + 8 = <b>18</b>."),
          ("(c)", [(x, 0, z) for x in range(4) for z in range(4) if not (x in (1, 2) and z in (1, 2))], 12, "#FFCC80",
           "It is a 4 by 4 square of cubes (16) with a 2 by 2 hole in the middle: 16 - 4 = <b>12</b>.")]
for part, cells, key, col, how in recall:
    check(len(cells), key, f"p.182 {part}")
    q121.append(Q(f"Let's Recall 1 {part}", 182, "The following solid is made up of unit cubes. Find the number of unit cubes and the volume of the solid.",
                  "Count layer by layer, or row by row. Don't forget cubes hidden at the back!",
                  [how, f"Each unit cube is 1 cubic unit, so the volume = <b>{key} cubic units</b>."],
                  f"{key} unit cubes, volume = {key} cubic units", "The volume is the number of unit cubes.", F(iso_cubes(cells, 30, 60, 210, col))))
q121.append(Q("Let's Recall 2", 183, "A cube measures 2 cm by 2 cm by 2 cm. What is the volume of the cube?", "Volume of a cube = length × length × length.",
              ["Volume = 2 × 2 × 2", "2 × 2 = 4, 4 × 2 = <b>8 cm³</b>"], "8 cm³", "8 small 1 cm cubes fit inside.", fcube))
q121.append(Q("Let's Recall 3", 183, "A cuboid measures 8 m by 4 m by 3 m. What is the volume of the cuboid?", "Volume of a cuboid = length × width × height.",
              ["Volume = 8 × 4 × 3", "8 × 4 = 32, 32 × 3 = <b>96 m³</b>"], "96 m³", "Length × width × height.",
              F(box(200, 75, 80, GREEN, 50, 210, labels=[(150, 228, "8 m"), (285, 200, "4 m"), (30, 175, "3 m")]))))
q121.append(Q("Let's Recall 4", 183, "A rectangular tank measuring 32 cm by 18 cm by 20 cm is ⅔ filled with water. Find the volume of water in the tank and the capacity of the tank.",
              "Capacity = the volume when full. The water is ⅔ of that.",
              ["Capacity = 32 × 18 × 20", "32 × 18 = 576, 576 × 20 = <b>11,520 cm³</b>", "Water = ⅔ of 11,520: 11,520 ÷ 3 = 3,840, 3,840 × 2 = <b>7,680 cm³</b>"],
              "Water = 7,680 cm³, capacity = 11,520 cm³", "The tank holds 11,520 cm³ when full, and ⅔ of it is water.",
              F(box(190, 120, 80, "#E1F5FE", 50, 215, labels=[(145, 232, "32 cm"), (280, 205, "18 cm"), (25, 160, "20 cm")], water_h=80))))
check(5 * 4 * 15 + 20 * 4 * 8, 940, "p.191 cap"); check(5 * 4 * 6 + 20 * 4 * 8, 760, "p.191 water")
q121.append(Q("Do and Learn", 191, "Find the capacity of the container below and find the volume of water in it.",
              "Split the container into the tall column and the long base.",
              ["Capacity: column 5 × 4 × 15 = <b>300 m³</b>, base 20 × 4 × 8 = <b>640 m³</b>", "Capacity = 300 + 640 = <b>940 m³</b>",
               "Water: the base is full (640 m³) and the column has water 6 m high: 5 × 4 × 6 = <b>120 m³</b>", "Water = 120 + 640 = <b>760 m³</b>"],
              "Capacity = 940 m³, water = 760 m³", "The column is 15 m tall above the base, but the water fills only 6 m of it.",
              F(solid([(0, 0), (20, 0), (20, 8), (5, 8), (5, 23), (0, 23)], 26, 9, 40, 240, "#E1F5FE",
                      water=[(0, 0), (20, 0), (20, 8), (5, 8), (5, 14), (0, 14)],
                      labels=[(10, -1.8, "20 m"), (2.5, 24.2, "5 m"), (-2.2, 18.5, "9 m"), (-2.2, 11, "6 m"), (21.8, 4, "8 m"), (23, 0.5, "4 m")]), 340, 280)))
for part, vol, area, key, edge, unit in [("(a)", 2100, 700, 3, "height", "m"), ("(b)", 6480, 360, 18, "width", "cm"), ("(c)", 7644, 364, 21, "length", "cm")]:
    check(Fr(vol, area), key, f"p.192 {part}")
    q121.append(Q(f"Exercise 1 {part}", 192, f"Find the unknown edge of the cuboid. The volume of the cuboid is {num(vol)} {unit}{CU} and the area of its shaded face is {num(area)} {unit}{SQ}.",
                  "Volume = area of the shaded face × the edge going away from it. So edge = volume ÷ area.",
                  [f"The unknown edge is the {edge}.", f"{edge.capitalize()} = volume ÷ area of shaded face = {num(vol)} ÷ {num(area)}", f"= <b>{key} {unit}</b>",
                   f"Check: {num(area)} × {key} = {num(area * key)} ✓"],
                  f"{edge.capitalize()} = {key} {unit}", "Dividing the volume by the face area gives the third edge.",
                  F(box(150, 110, 70, GREEN, 70, 210, labels=[(145, 160, f"Area = {num(area)} {unit}{SQ}")]))))
for lab_, page, what, val, key, unit in [("Exercise 2 (a)", 193, "area of the shaded face is 169 cm²", 169, 13, "cm"), ("Exercise 2 (b)", 193, "area of the shaded face is 196 m²", 196, 14, "m")]:
    check(key * key, val, lab_)
    q121.append(Q(lab_, page, f"Find the length of one edge of the cube. The {what}.", "Which number times itself gives the face area?",
                  [f"A face of a cube is a square: edge × edge = {val}", f"{key} × {key} = {val}", f"So the edge = <b>{key} {unit}</b>"],
                  f"{key} {unit}", "The face of a cube is a square.", F(box(120, 120, 70, BLUE, 90, 210, labels=[(150, 160, f"{val} {unit}{SQ}")]))))
for lab_, val, key, unit in [("Exercise 3 (a)", 216, 6, "cm"), ("Exercise 3 (b)", 64, 4, "m")]:
    check(key ** 3, val, lab_)
    q121.append(Q(lab_, 193, f"Find the length of one edge of the cube. The volume of the cube is {val} {unit}{CU}.", "Which number × itself × itself gives the volume? Try 2, 3, 4, 5, 6…",
                  [f"edge × edge × edge = {val}", f"Try: {key} × {key} = {key * key}, {key * key} × {key} = {val} ✓", f"So the edge = <b>{key} {unit}</b>"],
                  f"{key} {unit}", f"{key} × {key} × {key} = {val}."))
ex4 = [("(a)", [("Part ①", 12, 9, 12), ("Part ②", 28, 9, 12)], 4320, "cm",
        solid([(0, 0), (28, 0), (28, 12), (12, 12), (12, 24), (0, 24)], 40, 7, 50, 220, YELLOW, labels=[(14, -2, "28 cm"), (6, 25.5, "12 cm"), (-3, 12, "24 cm"), (29.5, 6, "12 cm"), (30, -1, "9 cm")]), "add"),
       ("(b)", [("Part ①", 10, 5, 8), ("Part ②", 20, 5, 8), ("Part ③", 30, 5, 8)], 2400, "cm",
        solid([(0, 0), (30, 0), (30, 8), (25, 8), (25, 16), (20, 16), (20, 24), (10, 24), (10, 16), (5, 16), (5, 8), (0, 8)], 25, 8, 30, 220, ORANGE,
              labels=[(15, -2, "30 cm"), (15, 25.5, "10 cm"), (31.5, 4, "8 cm"), (2.5, 9.2, "5 cm"), (32.5, -1, "5 cm")]), "add"),
       ("(c)", [("Whole block", 10, 4, 15), ("Hole", 8, 4, 7)], 376, "m",
        solid([(0, 0), (10, 0), (10, 15), (0, 15)], 30, 12, 70, 230, PURPLE, labels=[(5, -1.6, "10 m"), (-2, 7.5, "15 m"), (11.5, -0.5, "4 m")])
        + [poly([[94, 166], [190, 166], [190, 82], [94, 82]], "#ffffff"), T(142, 180, "8 m"), T(205, 128, "7 m")], "sub")]
for part, parts, key, unit, items, how in ex4:
    steps, tot = mult_steps(parts, unit)
    if how == "sub":
        tot = Fr(10 * 4 * 15 - 8 * 4 * 7)
        steps.append(f"Take away the hole: 600 - 224 = <b>{num(tot)} {unit}{CU}</b>")
    else:
        steps.append(f"Add the parts: <b>{num(tot)} {unit}{CU}</b>")
    check(tot, key, f"p.194 {part}")
    q121.append(Q(f"Exercise 4 {part}", 194, "Find the volume of the solid.", "Split it into cuboids, or take a hole away from a big cuboid.",
                  ["Split the solid into cuboids."] + steps, f"{num(key)} {unit}{CU}", "The pieces add up to the whole solid.", F(items, 340, 260)))
ex5 = [("(a)", [("Left column ①", 6, 6, 11), ("Middle ②", 11, 6, 7), ("Right column ③", 6, 6, 11)], 1254, "cm",
        solid([(0, 0), (6, 0), (6, 4), (17, 4), (17, 0), (23, 0), (23, 22), (17, 22), (17, 11), (6, 11), (6, 22), (0, 22)], 30, 9, 40, 230, "#E1F5FE",
              water=[(0, 0), (6, 0), (6, 4), (17, 4), (17, 0), (23, 0), (23, 11), (0, 11)],
              labels=[(11.5, -2, "23 cm"), (3, 23.3, "6 cm"), (11.5, 12.3, "11 cm"), (20, 23.3, "6 cm"), (-2.6, 11, "22 cm"), (25, 6, "11 cm"), (11.5, 8, "7 cm"), (19, 2, "4 cm")])),
       ("(b)", [("Bottom cube ①", 1, 1, 1), ("Long part ②", 4, 1, 1)], 5, "m",
        solid([(0, 0), (1, 0), (1, 1), (4, 1), (4, 3), (3, 3), (3, 2), (0, 2)], 35, 55, 40, 230, "#E1F5FE", water=[(0, 0), (1, 0), (1, 1), (4, 1), (4, 2), (0, 2)],
              labels=[(0.5, -0.35, "1 m"), (2, 3.3, "3 m"), (-0.35, 0.5, "1 m"), (4.4, 2.5, "1 m")])),
       ("(c)", [("Part ①", 10, 20, 5), ("Part ②", 28, 12, 5), ("Part ③", 10, 20, 5)], 3680, "cm",
        box(60, 30, 90, WATER, 40, 220, labels=[(70, 238, "10 cm")]) + box(60, 30, 90, WATER, 180, 220, labels=[(210, 238, "10 cm")])
        + [poly([[90, 140], [260, 140], [260, 160], [90, 160]], WATER), T(175, 132, "28 cm"), T(40, 150, "20 cm"), T(285, 205, "5 cm"), T(175, 175, "12 cm")])]
for part, parts, key, unit, items in ex5:
    steps, tot = mult_steps(parts, unit)
    steps.append(f"Water = <b>{num(tot)} {unit}{CU}</b>")
    check(tot, key, f"p.195 {part}")
    q121.append(Q(f"Exercise 5 {part}", 195, "Find the volume of water in the container.", "Split the water into cuboids. Use the water height, not the container height!",
                  ["Split the water into cuboids."] + steps, f"{num(key)} {unit}{CU}", "Only the parts filled with water count.", F(items, 340, 270)))
check(1 * 2 * 2 + 4 * 2 * 2 + 1 * 2 * 4, 28, "p.196 pool"); check(32 - 28, 4, "p.196 Q6")
q121.append(Q("Exercise 6", 196, "Peter filled 32 m³ of water into the pool, but some of the water overflew the rim of the pool. What was the volume of the overflow water?",
              "Find the capacity of the pool. The extra water spilled over.",
              ["Part ①: 1 × 2 × 2 = <b>4 m³</b>", "Part ②: 4 × 2 × 2 = <b>16 m³</b>", "Part ③: 1 × 2 × 4 = <b>8 m³</b>",
               "Capacity of pool = 4 + 16 + 8 = <b>28 m³</b>", "Overflow = 32 - 28 = <b>4 m³</b>"],
              "4 m³", "The pool holds only 28 m³, so 4 m³ spilled.",
              F(solid([(0, 0), (6, 0), (6, 4), (5, 4), (5, 2), (0, 2)], 50, 38, 30, 230, "#E1F5FE",
                      labels=[(0.5, -0.35, "1 m"), (3, 2.35, "4 m"), (5.5, 4.3, "1 m"), (-0.4, 1, "2 m"), (6.8, 3, "2 m")]), 340, 270)))
check(5 * 4 * 10 - 3 * 3 * 4, 164, "p.196 green"); check(11 * 4 * 5 + 2 * 4 * 5, 260, "p.196 pink"); check(164 + 260, 424, "p.196 Q7")
q121.append(Q("Exercise 7", 196, "From the given figure, add more cubes and/or cuboids to make the whole figure reach a volume of 424 cm³. (Answers vary.)",
              "Find the volume you already have. How much more do you need?",
              ["The given block: 5 × 4 × 10 = 200 cm³, minus the 3 × 3 × 4 hole = 36 cm³. So it is <b>164 cm³</b>.",
               "You need 424 - 164 = <b>260 cm³</b> more.",
               "One way (the key's answer): a top bar 11 × 4 × 5 = 220 cm³ and a leg 2 × 4 × 5 = 40 cm³.", "220 + 40 = 260 ✓, and 164 + 260 = <b>424 cm³</b>"],
              "One answer: add an 11 × 4 × 5 cm bar and a 2 × 4 × 5 cm leg (260 cm³)", "Any extra pieces that add up to 260 cm³ work.",
              F(solid([(0, 0), (5, 0), (5, 10), (0, 10)], 30, 15, 30, 220, GREEN, labels=[(2.5, -1.3, "5 cm"), (-1.7, 5, "10 cm"), (6, -0.5, "4 cm")])
                + [poly([[45, 205], [90, 205], [90, 160], [45, 160]], "#ffffff"), T(68, 218, "3 cm"), T(105, 185, "3 cm")]
                + solid([(5, 5), (16, 5), (16, 10), (5, 10)], 30, 15, 30, 220, PINK) + solid([(14, 0), (16, 0), (16, 5), (14, 5)], 30, 15, 30, 220, PINK)
                + [T(30 + 10.5 * 15, 220 - 10.8 * 15, "11 cm"), T(30 + 15 * 15, 236, "2 cm")], 340, 260)))
flash121 = [
    {"front": "Volume of a cube", "back": "length × length × length"}, {"front": "Volume of a cuboid", "back": "length × width × height"},
    {"front": "Volume using base area", "back": "base area × height"}, {"front": "Height of a cuboid", "back": "volume ÷ base area"},
    {"front": "Capacity", "back": "How much a container holds when full"}, {"front": "1 ℓ = ? cm³", "back": "1,000 cm³"},
    {"front": "1 m³ = ? cm³", "back": "1,000,000 cm³"}, {"front": "Cube of volume 125 cm³. Edge?", "back": "5 cm"},
    {"front": "Cube face area 36 cm². Edge?", "back": "6 cm"}, {"front": "Solid made of cuboids", "back": "Split it, find each volume, add"},
]
match121 = [["2 × 2 × 2", "8 cm³"], ["8 × 4 × 3", "96 m³"], ["840 ÷ 70", "12 cm"], ["Cube 216 cm³", "Edge 6 cm"], ["Cube 64 m³", "Edge 4 m"],
            ["Face 169 cm²", "Edge 13 cm"], ["1 ℓ", "1,000 cm³"], ["1 m³", "1,000,000 cm³"]]
quiz121 = [
    {"q": "A cube has edges of 3 cm. Volume?", "options": ["27 cm³", "9 cm³", "18 cm³", "12 cm³"]},
    {"q": "A cuboid is 8 m × 4 m × 3 m. Volume?", "options": ["96 m³", "15 m³", "32 m³", "128 m³"]},
    {"q": "Volume 840 cm³, base area 70 cm². Height?", "options": ["12 cm", "910 cm", "770 cm", "14 cm"]},
    {"q": "A cube has volume 125 cm³. Edge?", "options": ["5 cm", "25 cm", "41.7 cm", "15 cm"]},
    {"q": "A cube's face has area 196 cm². Edge?", "options": ["14 cm", "98 cm", "49 cm", "16 cm"]},
    {"q": "A cube has volume 512 m³. Edge?", "options": ["8 m", "16 m", "64 m", "10 m"]},
    {"q": "Volume 2,100 m³, shaded face 700 m². The other edge?", "options": ["3 m", "1,400 m", "30 m", "7 m"]},
    {"q": "A solid is 12 × 9 × 12 plus 28 × 9 × 12 (cm). Volume?", "options": ["4,320 cm³", "3,024 cm³", "1,296 cm³", "4,230 cm³"]},
    {"q": "A pool holds 28 m³. 32 m³ of water is poured in. Overflow?", "options": ["4 m³", "60 m³", "28 m³", "32 m³"]},
    {"q": "A tank 32 × 18 × 20 cm is ⅔ full. Water?", "options": ["7,680 cm³", "11,520 cm³", "3,840 cm³", "5,760 cm³"]},
    {"q": "How many cm³ in 1 ℓ?", "options": ["1,000", "100", "10", "1,000,000"]},
]
check(27, 3 ** 3, "q"); check(1296 + 3024, 4320, "q")
sections.append({"id": "12-1", "title": "Volume of 3D Shapes Made up of Cubes and Cuboids", "short": "1. Volume of Solids", "pages": "p.182 to 196",
                 "learn": learn121, "questions": q121, "flash": flash121, "match": match121, "quiz": quiz121})

# ==================================================================
# 12.2 WORD PROBLEMS (p.197 to 208)
# ==================================================================
check(Fr(250, 10), 25, "p.197 Q1"); check(5 * 5, 25, "p.197 Q1"); check(3 ** 3, 27, "p.197 Q2"); check(12 ** 3, 1728, "p.197 Q2")
check(Fr(5472, 38 * 24), 6, "p.198"); check(15 - 6, 9, "p.198"); check(Fr(16 * 24 * 1000, 100 * 75), Fr("51.2"), "p.199 Q4")
check(12 * 4 * 7 + 42 * 4 * 7, 1512, "p.199 Q5"); check(3 * Fr("3.5") * Fr("1.5") * 6 + Fr("15.5") * Fr("1.5") * Fr("6.5"), Fr("245.625"), "p.200 Q6")
check(Fr("245.625") * 1000, Fr(245625), "p.200 litres")
learn122 = [
    L("Idea", "Water in tanks", "<p>Volume of water = <b>base area × water height</b>.</p><p>Water height = volume ÷ base area.</p>", None, 198),
    L("Example", "Emma pours water away", "<p>A tank is 38 cm × 24 cm, water 15 cm high. Emma pours away 5,472 cm³.</p>"
      "<p>Drop in height = 5,472 ÷ (38 × 24) = 5,472 ÷ 912 = 6 cm</p><p>Water left = 15 - 6 = <b>9 cm</b> high</p>", None, 198),
    L("Idea", "Litres and cm³", "<p>1 ℓ = 1,000 cm³ (× 1,000 to change ℓ into cm³).</p><p>1 m³ = 1,000,000 cm³ = 1,000 ℓ.</p>", None, 200),
    L("Example", "Draining a tank", "<p>Water drains at 16 ℓ a minute for 24 minutes: 16 × 24 = 384 ℓ = 384,000 cm³.</p>"
      "<p>Tank 100 cm × 75 cm: height = 384,000 ÷ 7,500 = <b>51.2 cm</b></p>", None, 199),
    L("Idea", "Cube puzzles", "<p>Cube A has volume 27 cm³: 3 × 3 × 3 = 27, so its edge is 3 cm.</p><p>Cube B's edge is 4 times longer: 12 cm. Volume = 12 × 12 × 12 = <b>1,728 cm³</b>.</p>", None, 197),
]
q122 = []
check(2 * Fr("1.25") * 4 * 2 + 8 * Fr("1.25") * 2, 40, "p.202")
q122.append(Q("Do and Learn", 202, "A piece of metal is in the shape and size as shown below. What is the volume of it?", "Split it into 3 cuboids: 2 end towers and the middle.",
              ["Part ① (left tower): 2 × 1.25 × 4 = <b>10 m³</b>", "Part ② (middle): 8 × 1.25 × 2 = <b>20 m³</b>", "Part ③ (right tower): 2 × 1.25 × 4 = <b>10 m³</b>",
               "Volume = 10 + 20 + 10 = <b>40 m³</b>"],
              "40 m³", "3 cuboids added together.",
              F(solid([(0, 0), (12, 0), (12, 4), (10, 4), (10, 2), (2, 2), (2, 4), (0, 4)], 35, 22, 30, 200, "#CFD8DC",
                      labels=[(1, 4.5, "2 m"), (6, 2.5, "8 m"), (-0.8, 2, "4 m"), (12.6, 1, "2 m"), (13.2, -0.4, "1.25 m")]), 340, 240)))
check(Fr(56, 8), 7, "p.203 Q1")
q122.append(Q("Exercise 1", 203, "A rectangular tank has a base area of 8 m². The tank contains 56 m³ of water. Find the height of the water level in the tank.",
              "Water height = volume ÷ base area.", ["Height = 56 ÷ 8", "= <b>7 m</b>"], "7 m", "8 × 7 = 56.",
              F(box(150, 120, 70, "#E1F5FE", 70, 210, labels=[(145, 228, "Area = 8 m²")], water_h=90))))
check(Fr("17.64") * 1000, 17640, "p.203 Q2"); check(Fr(17640, 980), 18, "p.203 Q2 h"); check(Fr(2, 3) * 18, 12, "p.203 Q2")
q122.append(Q("Exercise 2", 203, "A rectangular tank with a capacity of 17.64 ℓ has a base area of 980 cm². The tank is ⅔ filled with water. What is the height of the water level in the tank?",
              "Change ℓ to cm³ first (× 1,000). Find the tank's height, then take ⅔ of it.",
              ["17.64 ℓ = 17.64 × 1,000 = <b>17,640 cm³</b>", "Height of tank = 17,640 ÷ 980 = <b>18 cm</b>", "Water height = ⅔ of 18: 18 ÷ 3 = 6, 6 × 2 = <b>12 cm</b>"],
              "12 cm", "The full tank is 18 cm tall, and the water fills ⅔ of it.",
              {"img": "img/unit12/water-tank.jpg", "alt": "a glass rectangular tank partly filled with water",
               "label": "The water fills only part of the tank. · น้ำเต็มแค่บางส่วนของถัง"}))
check(36 * 1000, 36000, "p.204 Q3"); check(Fr(36000, 1600), Fr("22.5"), "p.204 Q3 water"); check(Fr("22.5") * 3, Fr("67.5"), "p.204 Q3")
q122.append(Q("Exercise 3", 204, "A rectangular tank has a square base of side 40 cm. The tank is ⅓ full and contains 36 ℓ of water. Find the height of the tank.",
              "Find the water height, then remember it is only ⅓ of the tank.",
              ["36 ℓ = 36 × 1,000 = <b>36,000 cm³</b>", "Base area = 40 × 40 = 1,600 cm²", "Water height = 36,000 ÷ 1,600 = <b>22.5 cm</b>",
               "The water is ⅓ of the height, so the tank is 3 times as tall: 22.5 × 3 = <b>67.5 cm</b>"],
              "67.5 cm", "22.5 cm is one third of 67.5 cm.", F(box(130, 150, 70, "#E1F5FE", 80, 220, labels=[(145, 238, "40 cm"), (250, 210, "40 cm")], water_h=50))))
check(12 * 30, 360, "p.204 Q4"); check(Fr(360000, 75 * 60), 80, "p.204 Q4 h")
q122.append(Q("Exercise 4", 204, "An empty rectangular tank is being filled with water at a rate of 12 ℓ per minute. It takes half an hour to fill the tank to the brim. What is the height of the tank?",
              "Half an hour = 30 minutes. Find the total water, change to cm³, then divide by the base area.",
              ["Water in 30 minutes = 12 × 30 = <b>360 ℓ</b>", "360 ℓ = 360 × 1,000 = <b>360,000 cm³</b>", "Base area = 75 × 60 = 4,500 cm²",
               "Height = 360,000 ÷ 4,500 = <b>80 cm</b>"],
              "80 cm", "4,500 × 80 = 360,000.", F(box(160, 130, 80, "#E1F5FE", 60, 220, labels=[(140, 238, "75 cm"), (275, 210, "60 cm")]))))
check(10 * 10 * 10 + 36 * 3 * 20 + 10 * 10 * 10, 4160, "p.205 Q5")
q122.append(Q("Exercise 5", 205, "A cut of marble is in the shape and size as shown below. What is its volume?", "Split it: 2 cubes and 1 big flat slab.",
              ["Part ① cube: 10 × 10 × 10 = <b>1,000 cm³</b>", "Part ② slab: 36 × 3 × 20 = <b>2,160 cm³</b>", "Part ③ cube: 10 × 10 × 10 = <b>1,000 cm³</b>",
               "Volume = 1,000 + 2,160 + 1,000 = <b>4,160 cm³</b>"],
              "4,160 cm³", "The 2 cubes and the slab added together.",
              F(box(216, 120, 18, BLUE, 80, 160, labels=[(190, 30, "36 cm"), (315, 100, "20 cm"), (70, 40, "3 cm")]) + box(60, 60, 30, BLUE, 50, 220, labels=[(80, 238, "10 cm")])
                + box(60, 60, 30, BLUE, 230, 220, labels=[(260, 238, "10 cm")]), 340, 260)))
check(9 * 9 * 24 + 9 * 9 * 16 + 9 * 9 * 8, 3888, "p.205 Q6")
q122.append(Q("Exercise 6", 205, "Mom has a vase in the shape and size as shown below. What is its capacity?", "It is 3 cuboids of width 9 cm and depth 9 cm, with heights 24, 16 and 8 cm.",
              ["Part ①: 9 × 9 × 24 = <b>1,944 cm³</b>", "Part ②: 9 × 9 × 16 = <b>1,296 cm³</b>", "Part ③: 9 × 9 × 8 = <b>648 cm³</b>",
               "Capacity = 1,944 + 1,296 + 648 = <b>3,888 cm³</b>"],
              "3,888 cm³", "The 3 steps of the vase added together.",
              F(solid([(0, 0), (27, 0), (27, 8), (18, 8), (18, 16), (9, 16), (9, 24), (0, 24)], 40, 8, 40, 230, GREEN,
                      labels=[(13.5, -2, "27 cm"), (4.5, 25.4, "9 cm"), (-3, 12, "24 cm"), (14, 17.4, "9 cm"), (19.5, 12, "16 cm"), (28.5, 4, "8 cm"), (29.5, -1, "9 cm")]), 340, 260)))
check(Fr("1.5") * Fr("0.5") * 7 + Fr("3.5") * Fr("0.5") * Fr("1.5"), Fr("7.875"), "p.206 Q7"); check(Fr("7.875") * 1000000, 7875000, "p.206 Q7 cm")
q122.append(Q("Exercise 7", 206, "Dad built a water pit in the shape and size as shown below. If he fills the pit with water to the brim, what is the volume of water in this pit? (Give the answer in cm³.)",
              "Split it into the tall part and the low part. Then change m³ to cm³ (× 1,000,000).",
              ["Part ① tall: 1.5 × 0.5 × 7 = <b>5.25 m³</b>", "Part ② low: 3.5 × 0.5 × 1.5 = <b>2.625 m³</b>", "Water = 5.25 + 2.625 = <b>7.875 m³</b>",
               "1 m³ = 1,000,000 cm³, so 7.875 × 1,000,000 = <b>7,875,000 cm³</b>"],
              "7,875,000 cm³", "Find m³ first, then change the unit.",
              F(solid([(0, 0), (5, 0), (5, 1.5), (1.5, 1.5), (1.5, 7), (0, 7)], 25, 27, 60, 230, "#E1F5FE",
                      labels=[(2.5, -0.6, "5 m"), (-0.7, 3.5, "7 m"), (3.3, 1.9, "3.5 m"), (5.7, 0.8, "1.5 m"), (6, -0.3, "0.5 m")]), 340, 260)))
check(25 * 8 * 16 - 15 * 8 * 10, 2000, "p.206 Q8")
q122.append(Q("Exercise 8", 206, "Siti owns a fish tank in the shape and size as shown below. What is the volume of water in this tank?",
              "The water fills the bottom box (16 cm high) except for a solid block inside it.",
              ["The water box: 25 × 8 × 16 = <b>3,200 cm³</b>", "The block inside (no water there): 15 × 8 × 10 = <b>1,200 cm³</b>",
               "Water = 3,200 - 1,200 = <b>2,000 cm³</b>"],
              "2,000 cm³", "The block takes up space, so subtract it.",
              F(box(200, 128, 50, WATER, 50, 220, labels=[(150, 238, "25 cm"), (275, 160, "16 cm"), (270, 215, "8 cm")])
                + [poly([[90, 210], [210, 210], [210, 130], [90, 130]], "#ffffff"), T(150, 225, "15 cm"), T(228, 172, "10 cm")], 340, 260)))
check(3 * 20 * 9 * 9 + 10 * 9 * 45, 8910, "p.207 a"); check(2 * 20 * 9 * 9 + 10 * 9 * 27, 5670, "p.207 b")
fE = F(solid([(0, 0), (30, 0), (30, 9), (10, 9), (10, 18), (30, 18), (30, 27), (10, 27), (10, 36), (30, 36), (30, 45), (0, 45)], 30, 5, 70, 245, "#E1F5FE",
             water=[(0, 0), (30, 0), (30, 9), (10, 9), (10, 18), (30, 18), (30, 27), (0, 27)],
             labels=[(15, -3, "30 cm"), (20, 37.5, "20 cm"), (-5, 22, "45 cm"), (-11, 13, "27 cm"), (33.5, 41, "9 cm")]), 340, 270)
q122.append(Q("Exercise 9 (a)", 207, "A fish tank in the shape of the letter E is in the size as shown below:<br>(a) What is the capacity of this tank?",
              "Split the E into the tall back (10 cm wide) and 3 arms (20 cm long).",
              ["Each arm ①②③: 20 × 9 × 9 = <b>1,620 cm³</b>, so 3 arms = 4,860 cm³", "The back ④: 10 × 9 × 45 = <b>4,050 cm³</b>",
               "Capacity = 1,620 + 1,620 + 1,620 + 4,050 = <b>8,910 cm³</b>"],
              "8,910 cm³", "3 arms and the back added together.", fE))
q122.append(Q("Exercise 9 (b)", 207, "A fish tank in the shape of the letter E is in the size as shown below:<br>(b) What is the volume of water in this tank?",
              "The water is 27 cm high. Which parts are full?",
              ["The water reaches 27 cm, so the bottom 2 arms ②③ are full: 1,620 + 1,620 = <b>3,240 cm³</b>",
               "The back up to 27 cm ⑤: 10 × 9 × 27 = <b>2,430 cm³</b>", "Water = 1,620 + 1,620 + 2,430 = <b>5,670 cm³</b>"],
              "5,670 cm³", "The top arm is above the water.", fE))
check(30 * 20 * 15, 9000, "p.208 B"); check(Fr(9, 10), Fr(9, 10), "p.208 a"); check(Fr(9000, 40 * 30), Fr("7.5"), "p.208 drop"); check(Fr("7.5") * 3, Fr("22.5"), "p.208 b")
check(Fr(40 * 30) * Fr("22.5"), 27000, "p.208 c vol"); check(Fr(27, 10), Fr(27, 10), "p.208 c")
fAB = F(box(110, 60, 60, "#E1F5FE", 40, 110, labels=[(95, 125, "40 cm"), (25, 85, "A"), (190, 80, "30 cm")], water_h=60)
        + box(90, 50, 40, "#ffffff", 180, 225, labels=[(225, 242, "30 cm"), (300, 210, "20 cm"), (300, 190, "15 cm"), (225, 200, "B")]), 340, 260)
for part, q, steps, ans, why in [
    ("(a)", "(a) How long was the tap turned on to drain water?",
     ["Volume of Tank B when full = 30 × 20 × 15 = <b>9,000 cm³</b>", "9,000 cm³ = 9,000 ÷ 1,000 = <b>9 ℓ</b>", "Time = 9 ÷ 10 = <b>9/10 min</b>"],
     "9/10 min", "At 10 ℓ a minute, 9 ℓ takes 9/10 of a minute."),
    ("(b)", "(b) What was the height of Tank A?",
     ["The 9,000 cm³ that left Tank A made its water drop by 9,000 ÷ (40 × 30) = 9,000 ÷ 1,200 = <b>7.5 cm</b>",
      "The water is now ⅔ of the height, so the drop is ⅓ of the height.", "Height of Tank A = 7.5 × 3 = <b>22.5 cm</b>"],
     "22.5 cm", "7.5 cm is one third of 22.5 cm."),
    ("(c)", "(c) How many minutes would it take to empty Tank A completely?",
     ["Tank A when full = 40 × 30 × 22.5 = <b>27,000 cm³</b>", "27,000 cm³ = 27,000 ÷ 1,000 = <b>27 ℓ</b>", "Time = 27 ÷ 10 = <b>2 7/10 min</b>"],
     "2 7/10 min", "27 ℓ at 10 ℓ a minute.")]:
    q122.append(Q(f"Exercise 10 {part}", 208, "Tank A and Tank B are rectangular tanks as shown below. At first, Tank A was completely filled with water and Tank B was empty. A tap was turned on to drain water from Tank A into Tank B at a rate of 10 ℓ per minute. When Tank B was completely filled with water, the height of the water level in Tank A became ⅔ of its original height.<br>" + q,
                  "Work in cm³, then change to ℓ (÷ 1,000) for the time.", steps, ans, why, fAB))
flash122 = [
    {"front": "Water height", "back": "Volume of water ÷ base area"}, {"front": "ℓ to cm³", "back": "× 1,000"}, {"front": "cm³ to ℓ", "back": "÷ 1,000"},
    {"front": "m³ to cm³", "back": "× 1,000,000"}, {"front": "Half an hour", "back": "30 minutes"}, {"front": "Time to fill", "back": "Volume (ℓ) ÷ rate (ℓ per minute)"},
    {"front": "Tank ⅓ full, water 22.5 cm. Tank height?", "back": "67.5 cm"}, {"front": "Block inside a tank", "back": "Subtract its volume from the water box"},
]
match122 = [["17.64 ℓ", "17,640 cm³"], ["36 ℓ", "36,000 cm³"], ["7.875 m³", "7,875,000 cm³"], ["9,000 cm³", "9 ℓ"], ["56 ÷ 8", "7 m"],
            ["12 ℓ × 30 min", "360 ℓ"], ["22.5 × 3", "67.5 cm"], ["27 ℓ at 10 ℓ/min", "2 7/10 min"]]
quiz122 = [
    {"q": "56 m³ of water, base area 8 m². Water height?", "options": ["7 m", "48 m", "64 m", "448 m"]},
    {"q": "36 ℓ = ? cm³", "options": ["36,000 cm³", "3,600 cm³", "360 cm³", "36,000,000 cm³"]},
    {"q": "9,000 cm³ = ? ℓ", "options": ["9 ℓ", "90 ℓ", "900 ℓ", "0.9 ℓ"]},
    {"q": "A tap fills 12 ℓ a minute for 30 minutes. Total?", "options": ["360 ℓ", "42 ℓ", "2.5 ℓ", "18 ℓ"]},
    {"q": "Tank base 75 cm × 60 cm holds 360,000 cm³. Height?", "options": ["80 cm", "800 cm", "48 cm", "8 cm"]},
    {"q": "A tank is ⅓ full with water 22.5 cm high. Tank height?", "options": ["67.5 cm", "7.5 cm", "45 cm", "22.5 cm"]},
    {"q": "Water box 3,200 cm³ with a 1,200 cm³ block inside. Water?", "options": ["2,000 cm³", "4,400 cm³", "3,200 cm³", "1,200 cm³"]},
    {"q": "1 m³ = ? cm³", "options": ["1,000,000", "1,000", "100", "10,000"]},
    {"q": "Cube A is 27 cm³. Cube B's edge is 4 times longer. Volume of B?", "options": ["1,728 cm³", "108 cm³", "432 cm³", "64 cm³"]},
    {"q": "27 ℓ drains at 10 ℓ a minute. Time?", "options": ["2 7/10 min", "27 min", "270 min", "2 min"]},
]
sections.append({"id": "12-2", "title": "Word Problems", "short": "2. Word Problems", "pages": "p.197 to 208",
                 "learn": learn122, "questions": q122, "flash": flash122, "match": match122, "quiz": quiz122})

# ==================================================================
# UNIT 12 CHALLENGE (p.209 to 214)
# ==================================================================
check(800 * 36, 28800, "p.209 water"); check(Fr(28800, 600), 48, "p.209 Y"); check(Fr(5, 6) * 48, 40, "p.209 X"); check(800 * 40 - 28800, 3200, "p.209")
check(Fr(480, 640), Fr(3, 4), "p.211 rate"); check(50 - 20, 30, "p.211 A"); check(Fr(3, 4) * 20, 15, "p.211 B"); check(480 * 30 + 640 * 15, 24000, "p.212 check"); check(50 * 480, 24000, "p.212")
check(20 - 9, 11, "p.213"); check(Fr(1320, 11 * 10), 12, "p.213 h")
qch = [
    Q("Let's Think Along", 209, "X and Y are two rectangular containers as shown below. The base area of X is 800 cm². The base area of Y is 600 cm². The height of X is ⅚ the height of Y. X contains water to a height of 36 cm. The volume of water in X will fill Y completely. How much more water is needed to fill X to the brim?",
      "Find the water in X. That is Y's capacity, so you can find Y's height, then X's height.",
      ["Water in X = 800 × 36 = <b>28,800 cm³</b>. This fills Y, so Y holds 28,800 cm³.", "Height of Y = 28,800 ÷ 600 = <b>48 cm</b>",
       "Height of X = ⅚ of 48: 48 ÷ 6 = 8, 8 × 5 = <b>40 cm</b>", "Capacity of X = 800 × 40 = <b>32,000 cm³</b>", "More water needed = 32,000 - 28,800 = <b>3,200 cm³</b>"],
      "3,200 cm³", "X holds 32,000 cm³ but has only 28,800 cm³.",
      F(box(110, 100, 60, "#E1F5FE", 30, 210, labels=[(85, 228, "X: 800 cm²")], water_h=90) + box(90, 120, 50, "#ffffff", 200, 210, labels=[(245, 228, "Y: 600 cm²")]))),
    Q("Problem Solving", 211, "A and B are rectangular containers. The base area of A is 480 cm² and that of B is 640 cm². At first, A contained water to a height of 50 cm and B was empty. Peter poured some water from A into B. The height of the water level in A became twice that of B. What was the height of the water level in B?",
      "Guess and check: when A drops 1 cm, B rises 480 ÷ 640 = ¾ cm.",
      ["Every 1 cm drop in A pours 480 cm³ into B, which raises B by 480 ÷ 640 = <b>¾ cm</b>.",
       "Try a drop of 8 cm: A = 42 cm, B = 6 cm. 42 is 7 times 6. Too big.", "Try a drop of 16 cm: A = 34 cm, B = 12 cm. Still more than twice.",
       "Try a drop of 20 cm: A = 30 cm, B = ¾ × 20 = 15 cm. 30 is twice 15 ✓", "So the water in B was <b>15 cm</b> high.",
       "<b>Check:</b> 480 × 30 + 640 × 15 = 14,400 + 9,600 = 24,000 = 480 × 50 ✓"],
      "15 cm", "The water in A (30 cm) is twice the water in B (15 cm), and no water is lost.",
      F(box(90, 110, 50, "#E1F5FE", 40, 210, labels=[(85, 228, "A: 480 cm²")], water_h=100) + box(110, 80, 50, "#ffffff", 190, 210, labels=[(245, 228, "B: 640 cm²")]))),
    Q("Math Journal", 213, "From the figure below, explain how you find the height of C.",
      "Find C's length first. Then height = volume ÷ (length × width).",
      ["The length of C = 20 - 9 = <b>11 cm</b>.", "We know C's volume, length and width, so we can find its height.",
       "Height = 1,320 ÷ (11 × 10) = 1,320 ÷ 110 = <b>12 cm</b>"],
      "12 cm (length 11 cm, then 1,320 ÷ 110)", "Volume ÷ (length × width) gives the height.",
      F(box(72, 150, 60, YELLOW, 40, 210, labels=[(76, 228, "9 cm"), (25, 140, "")]) + box(88, 96, 60, PINK, 112, 210, labels=[(156, 228, "11 cm"), (156, 160, "C"), (156, 180, "1,320 cm³"), (240, 205, "10 cm")])
        + [T(120, 20, "20 cm"), seg([40, 30], [200, 30])])),
]
sections.append({"id": "12-ch", "title": "Unit 12 Challenge", "short": "⭐ Challenge", "pages": "p.209 to 214",
                 "learn": [L("Idea", "Unit 12 big ideas", "<p><b>Volume</b> = length × width × height = base area × height.</p><p>Split solids into cuboids. 1 ℓ = 1,000 cm³. 1 m³ = 1,000,000 cm³.</p>", None, 214),
                           L("Example", "Pouring between tanks", "<p>Water keeps its volume when it is poured. If 480 cm³ leaves a tank with base 480 cm², the water drops 1 cm. In a tank with base 640 cm², it rises 480 ÷ 640 = ¾ cm.</p>", None, 211)],
                 "questions": qch, "flash": flash121[:5] + flash122[:5], "match": match121[:4] + match122[:4], "quiz": quiz121[:5] + quiz122[:5]})

unit = {"unit": "12", "title": "Volume and Capacity", "pages": "p.181 to 214", "sections": sections,
        "expectedPages": {"12-1": [182, 183, 191, 192, 193, 194, 195, 196], "12-2": [202, 203, 204, 205, 206, 207, 208], "12-ch": [209, 211, 213]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit12.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all maths checks passed. Wrote content/unit12.json ({n} guided questions, {len(sections)} sections).")
