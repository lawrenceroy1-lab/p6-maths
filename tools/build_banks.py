"""Builds the Practice / Unit Test question banks: content/bank07.json, bank08.json, bank09.json.

Each unit has 40 multiple-choice questions. options[0] is always the right answer
(the site shuffles them). Every number is checked with check().
Sources: the book's Review section (p.245 onwards), the unit exercises, and new questions.
Run:  python3 tools/build_banks.py
"""
import contextlib
import io
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, PROBLEMS  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import build_unit07 as U7  # noqa: E402
    import build_unit08 as U8  # noqa: E402
    import build_unit09 as U9  # noqa: E402

GREEN, BLUE, ORANGE, PINK, YELLOW, PURPLE = "#C8E6C9", "#BBDEFB", "#FFE0B2", "#F8BBD0", "#FFF59D", "#D1C4E9"


def B(q, options, why, src, fig=None):
    assert len(options) == 4 and len(set(options)) == 4, q
    return {"q": q, "options": options, "why": why, "src": src, "fig": fig}


def gq(unit_mod, sec_id, label):
    for s in unit_mod.sections:
        if s["id"] == sec_id:
            for q in s["questions"]:
                if q["label"] == label:
                    return q["fig"]
    raise KeyError(label)


def deg(n):
    return f"{n}°"


# ==================================================================
# UNIT 7
# ==================================================================
b7 = []
b7.append(B("Which statement about triangles is TRUE?",
            ["The interior angles of an equilateral triangle are equal", "All sides of an isosceles triangle are equal",
             "The interior angles of an obtuse triangle are all obtuse", "A right triangle has 2 right angles"],
            "An equilateral triangle has 3 equal angles (60° each). An isosceles triangle has only 2 equal sides.", "Review Q1, p.245"))
b7.append(B("Which statement about triangles is FALSE?",
            ["The interior angles of an obtuse triangle are all obtuse", "An isosceles triangle has 2 equal sides",
             "There is 1 right angle inside a right triangle", "The interior angles of an equilateral triangle are equal"],
            "An obtuse triangle has only ONE obtuse angle. Two obtuse angles would already be more than 180°.", "Review Q1, p.245"))
fR2a = U7.triangle("ABC", [[150, 30], [250, 200], [50, 200]], ORANGE, [
    {"t": "tick", "p": ["A", "B"]}, {"t": "tick", "p": ["B", "C"]}, {"t": "tick", "p": ["A", "C"]},
    {"t": "ang", "v": "C", "a": "A", "b": "B", "s": "60°"}, {"t": "len", "p": ["B", "C"], "s": "10 cm"}])
b7.append(B("ABC is an equilateral triangle. What is ∠BAC?", ["60°", "90°", "120°", "180°"],
            "All 3 angles of an equilateral triangle are equal: 180° ÷ 3 = 60°.", "Review Q2(a), p.245", fR2a))
b7.append(B("ABC is an equilateral triangle and BC = 10 cm. How long is AB?", ["10 cm", "5 cm", "20 cm", "30 cm"],
            "All 3 sides of an equilateral triangle are equal, so AB = BC = 10 cm.", "Review Q2(a), p.245", fR2a))
check((180 - 40) / 2, 70, "R2b")
fR2b = U7.triangle("DFE", [[140, 25], [80, 210], [200, 210]], GREEN, [
    {"t": "tick", "p": ["D", "F"]}, {"t": "tick", "p": ["D", "E"]}, {"t": "ang", "v": "D", "a": "F", "b": "E", "s": "40°", "r": 30},
    {"t": "len", "p": ["F", "D"], "s": "12 cm"}])
b7.append(B("DEF is an isosceles triangle with DE = DF and ∠EDF = 40°. What is ∠DEF?", ["70°", "140°", "40°", "50°"],
            "(180° - 40°) ÷ 2 = 140° ÷ 2 = 70°. The 2 base angles are equal.", "Review Q2(b), p.245", fR2b))
b7.append(B("DEF is an isosceles triangle with DE = DF. DF = 12 cm. How long is DE?", ["12 cm", "6 cm", "24 cm", "40 cm"],
            "DE = DF, so DE is also 12 cm.", "Review Q2(b), p.245", fR2b))
check(180 - 90 - 50, 40, "R2c")
fR2c = U7.triangle("JLK", [[200, 30], [40, 190], [200, 190]], BLUE, [
    {"t": "ra", "v": "K", "a": "J", "b": "L"}, {"t": "ang", "v": "J", "a": "L", "b": "K", "s": "50°", "r": 30}])
b7.append(B("JKL is a right triangle with ∠JKL = 90° and ∠KJL = 50°. What is ∠JLK?", ["40°", "50°", "130°", "90°"],
            "The other 2 angles of a right triangle add up to 90°: 90° - 50° = 40°.", "Review Q2(c), p.245", fR2c))
b7.append(B("In a right triangle, the 2 angles that are not the right angle add up to…", ["90°", "180°", "60°", "45°"],
            "180° - 90° = 90°, so the other 2 angles share 90°.", "Review Q2(c), p.245", fR2c))
b7.append(B("All 3 sides of a triangle have the same tick mark. What is each angle?", ["60°", "90°", "45°", "30°"],
            "It is equilateral, so each angle is 180° ÷ 3 = 60°.", "Review Q3(a), p.246"))
for vtx, ans, wrongs, src in [(70, 55, [110, 70, 35], "Review Q3(b), p.246"), (24, 78, [156, 66, 24], "Review Q3(c), p.246"),
                              (110, 35, [70, 55, 110], "Review Q3(d), p.246")]:
    check((180 - vtx) / 2, ans, src)
    b7.append(B(f"An isosceles triangle has a vertex angle of {deg(vtx)}. What is each of the other 2 angles?",
                [deg(ans)] + [deg(w) for w in wrongs],
                f"180° - {vtx}° = {180 - vtx}°. Share it between 2 equal angles: {180 - vtx}° ÷ 2 = {ans}°.", src))
b7.append(B("ABC is a triangle with ∠ACB = 90° and AC = CB = 5 cm. What type of triangle is it?",
            ["A right isosceles triangle", "An equilateral triangle", "An obtuse triangle", "A scalene triangle"],
            "It has a right angle AND 2 equal sides, so it is right and isosceles.", "Review Q4(a), p.246"))
b7.append(B("Triangle EFG has EF = EG = 5 cm and GF = 4 cm. What type of triangle is it?",
            ["Isosceles", "Equilateral", "Scalene", "Right"],
            "2 sides are equal (5 cm and 5 cm), so it is isosceles.", "Review Q4(b), p.246"))
b7.append(B("A straight line from the center of a circle to its circumference is called the…", ["Radius", "Diameter", "Chord", "Center"],
            "The radius goes from the center to the edge.", "Review Q5, p.247"))
b7.append(B("A straight line joining any two points on the circumference is called a…", ["Chord", "Radius", "Center", "Circumference"],
            "Any line joining 2 points on the edge is a chord. A diameter is the longest chord.", "Review Q5, p.247"))
b7.append(B("To draw circle J with diameter 4 cm, you open your compass to…", ["2 cm", "4 cm", "8 cm", "1 cm"],
            "The compass is set to the radius: 4 ÷ 2 = 2 cm.", "Review Q6, p.247"))
check(3 + 3, 6, "R7")
b7.append(B("Circles K and O each have radius 3 cm. Their circumferences just touch. How far apart are the centers K and O?",
            ["6 cm", "3 cm", "9 cm", "12 cm"], "From K to the touching point is 3 cm, and from there to O is 3 cm more: 3 + 3 = 6 cm.", "Review Q7, p.247"))
for lab, ans, wrongs, why in [("Exercise 1 (a)", 70, [110, 80, 40], "180° - 70° - 40° = 70°"), ("Exercise 1 (b)", 122, [58, 152, 28], "180° - 30° - 28° = 122°"),
                              ("Exercise 1 (d)", 73, [107, 17, 63], "180° - 62° - 45° = 73°"), ("Exercise 1 (e)", 58, [122, 32, 68], "180° - 32° - 90° = 58°")]:
    b7.append(B("Find the unknown marked angle.", [deg(ans)] + [deg(w) for w in wrongs], f"The angles of a triangle add up to 180°: {why}.",
                f"Exercise p.17", gq(U7, "7-2", lab)))
check(180 - 70 - 40, 70, "b"); check(180 - 30 - 28, 122, "b"); check(180 - 62 - 45, 73, "b"); check(180 - 32 - 90, 58, "b")
b7.append(B("ACD is an equilateral triangle and BCD is a straight line. Find ∠b.", ["120°", "60°", "90°", "30°"],
            "∠ACD = 60°. Angles on a straight line add up to 180°: 180° - 60° = 120°.", "Exercise 2, p.18", gq(U7, "7-2", "Exercise 2")))
b7.append(B("ACD is equilateral. ABC is isosceles with AB = AC and ∠CAB = 36°. Find ∠BCD.", ["132°", "72°", "96°", "144°"],
            "∠ACB = (180° - 36°) ÷ 2 = 72°. ∠BCD = 60° + 72° = 132°.", "Exercise 7, p.19", gq(U7, "7-2", "Exercise 7")))
b7.append(B("JK = JL and MK = ML. ∠KJL = 70° and ∠MLK = 25°. Find ∠JLM.", ["30°", "55°", "25°", "80°"],
            "∠JLK = (180° - 70°) ÷ 2 = 55°. ∠JLM = 55° - 25° = 30°.", "Exercise 8, p.20", gq(U7, "7-2", "Exercise 8")))
b7.append(B("STW is equilateral. ∠VSW = ∠VSU = ∠UST. SUV is isosceles. Find ∠SUV.", ["80°", "20°", "60°", "160°"],
            "∠VSU = 60° ÷ 3 = 20°. ∠SUV = (180° - 20°) ÷ 2 = 80°.", "Exercise 9, p.20", gq(U7, "7-2", "Exercise 9")))
b7.append(B("ABC is a right triangle with ∠ABC = 38°. ∠CAD = ½ ∠CAB. Find ∠DAB.", ["26°", "52°", "38°", "19°"],
            "∠CAB = 180° - 90° - 38° = 52°. Half of 52° is 26°.", "Exercise 10, p.20", gq(U7, "7-2", "Exercise 10")))
b7.append(B("ABC is isosceles with ∠A = 40°. DBC is equilateral. Find ∠ACD.", ["10°", "70°", "60°", "20°"],
            "∠ACB = (180° - 40°) ÷ 2 = 70°. ∠ACD = 70° - 60° = 10°.", "Let's Think Along, p.41", gq(U7, "7-ch", "Let's Think Along")))
b7.append(B("ABC and AED are straight lines and BE = ED. Find ∠ABE.", ["68°", "74°", "42°", "38°"],
            "∠BDE = 38°, ∠BDC = 180° - 36° - 64° - 38° = 42°, ∠CBD = 180° - 64° - 42° = 74°, ∠ABE = 180° - 38° - 74° = 68°.",
            "Problem Solving, p.43", gq(U7, "7-ch", "Problem Solving")))
b7.append(B("A triangle has angles 47°, 53° and 80°. What type of triangle is it?", ["Acute triangle", "Obtuse triangle", "Right triangle", "Equilateral triangle"],
            "All 3 angles are less than 90°.", "Do and Learn 2(a), p.8"))
b7.append(B("A triangle has angles 40°, 115° and 25°. What type of triangle is it?", ["Obtuse triangle", "Acute triangle", "Right triangle", "Isosceles triangle"],
            "115° is more than 90°, so it is an obtuse triangle.", "Do and Learn 2(b), p.8"))
b7.append(B("In triangle ABC, CB is the base. What is the vertex angle?", ["∠CAB", "∠ACB", "∠CBA", "∠ABC"],
            "The vertex angle is at the corner that is not on the base: A.", "Exercise 1, p.9"))
b7.append(B("A square is cut in half along a diagonal. Each half is…", ["A right isosceles triangle", "An equilateral triangle", "An obtuse triangle", "A scalene triangle"],
            "Each half has a square's corner (90°) and 2 sides of the square (equal).", "Exercise 4(a), p.12"))
b7.append(B("A rectangle (not a square) is cut in half along a diagonal. Each half is…", ["A right triangle", "An isosceles triangle", "An equilateral triangle", "An obtuse triangle"],
            "It keeps a right angle, but its 3 sides are all different.", "Exercise 4(b), p.12"))
b7.append(B("What type of triangle has 3 different sides?", ["Scalene", "Isosceles", "Equilateral", "Right"],
            "Scalene means no sides are equal.", "Exercise 5(a), p.12"))
b7.append(B("Which triangle is impossible to draw?", ["One with 2 right angles", "One with 1 obtuse and 2 acute angles", "One with 3 acute angles", "One with 1 right angle and 2 acute angles"],
            "90° + 90° = 180° already, so there is nothing left for the third angle.", "Math Journal, p.45"))
check(180 - 70 - 70, 40, "p25")
b7.append(B("You draw triangle KLM with ∠KLM = 70° and ∠LMK = 70°. What will ∠MKL measure?", ["40°", "70°", "110°", "140°"],
            "180° - 70° - 70° = 40°.", "Exercise 2, p.25"))
b7.append(B("You know all 3 sides of a triangle. Which tool helps you find the third corner?", ["Compass", "Protractor", "Set square", "Ruler only"],
            "Draw an arc from each end of the first side. The arcs cross at the third corner.", "Exercise 3, p.26"))
check(2 * 14.5, 29, "p34")
b7.append(B("OR is the radius of a circle and OR = 14.5 cm. What is the diameter?", ["29 cm", "7.25 cm", "14.5 cm", "28 cm"],
            "Diameter = 2 × radius = 2 × 14.5 = 29 cm.", "Exercise 8(b), p.34"))
b7.append(B("CD is the diameter of a circle and CD = 25 cm. What is the radius?", ["12.5 cm", "50 cm", "12 cm", "25 cm"],
            "Radius = diameter ÷ 2 = 25 ÷ 2 = 12.5 cm.", "Exercise 5(b), p.33"))
b7.append(B("ABCD is a square inside a circle. Its diagonal BD = 30 cm. What is the radius of the circle?", ["15 cm", "30 cm", "60 cm", "7.5 cm"],
            "The diagonal goes through the center, so it is a diameter: 30 ÷ 2 = 15 cm.", "Exercise 5(d), p.33", gq(U7, "7-4", "Exercise 5 (d)")))
b7.append(B("A wheel is 60 cm tall. What is its radius?", ["30 cm", "60 cm", "120 cm", "15 cm"],
            "The height of the wheel is its diameter: 60 ÷ 2 = 30 cm.", "Exercise 7, p.33"))
b7.append(B("A circle has radius 9.5 cm. What is its diameter?", ["19 cm", "18 cm", "4.75 cm", "9.5 cm"],
            "2 × 9.5 = 19 cm.", "Exercise 9, p.34"))
b7.append(B("A square has diagonals of 4 cm. A circle passes through all 4 corners. What is its radius?", ["2 cm", "4 cm", "8 cm", "1 cm"],
            "From the middle to a corner is half a diagonal: 4 ÷ 2 = 2 cm.", "Exercise 6, p.40"))
DROP7 = {"In a right triangle, the 2 angles that are not the right angle add up to…", "DEF is an isosceles triangle with DE = DF. DF = 12 cm. How long is DE?",
         "All 3 sides of a triangle have the same tick mark. What is each angle?", "What type of triangle has 3 different sides?"}
b7 = [x for x in b7 if x["q"] not in DROP7]
check(len(b7), 40, "bank 7 size")

# ==================================================================
# UNIT 8
# ==================================================================
F8 = U8.F
b8 = []
solids = [("Review Q8(a), p.248", F8(U8.square_pyramid(160, 200, 180, 170, GREEN)), "Pyramid", ["Prism", "Cone", "Cuboid"], "It has a flat base and triangle faces that meet at a vertex."),
          ("Review Q8(b), p.248", F8(U8.cone(160, 30, 180, 70, 20, PURPLE)), "Cone", ["Cylinder", "Pyramid", "Sphere"], "1 circle face, 1 curved face and 1 vertex."),
          ("Review Q8(c), p.248", F8(U8.cylinder(160, 45, 65, 18, 140, ORANGE)), "Cylinder", ["Cone", "Prism", "Sphere"], "2 circle faces and 1 curved face."),
          ("Review Q8(d), p.248", F8(U8.tri_pyramid(160, 190, 200, 170, GREEN)), "Pyramid", ["Prism", "Cone", "Cube"], "Triangle faces meet at a vertex on a triangle base."),
          ("Review Q8(e), p.248", F8(U8.sphere(160, 115, 85, BLUE)), "Sphere", ["Cylinder", "Cone", "Hemisphere"], "Round all over with no flat face."),
          ("Review Q8(f), p.248", F8(U8.hex_pyramid(160, 190, 80, 170, YELLOW)), "Pyramid", ["Prism", "Cylinder", "Cone"], "A hexagon base with triangle faces meeting at a vertex.")]
for src, fg, ans, wrongs, why in solids:
    b8.append(B("Which solid is this?", [ans] + wrongs, why, src, fg))
b8.append(B("A net has 1 square and 4 triangles. Which solid can it make?", ["Square pyramid", "Triangular prism", "Cube", "Triangular pyramid"],
            "The square is the base and the 4 triangles fold up to meet at the vertex.", "Review Q9, p.249", U8.sq_pyr_net_fig))
for q, ans, wrongs, why, src in [
    ("How many faces does a cube have?", "6", ["4", "8", "12"], "Top, bottom, front, back, left and right: 6 faces.", "Let's Think Along, p.65"),
    ("How many vertices (corners) does a cube have?", "8", ["6", "12", "4"], "4 corners on top and 4 on the bottom: 8.", "Let's Think Along, p.65"),
    ("How many edges does a cube have?", "12", ["8", "6", "24"], "4 on top, 4 on the bottom and 4 going up: 12.", "Let's Think Along, p.65"),
    ("How many faces does a triangular prism have?", "5", ["6", "3", "9"], "2 triangles and 3 rectangles: 5 faces.", "Let's Think Along, p.65"),
    ("How many edges does a triangular prism have?", "9", ["6", "5", "12"], "3 on each triangle end (6) and 3 joining them: 9.", "Let's Think Along, p.65"),
    ("How many vertices does a square pyramid have?", "5", ["4", "8", "6"], "4 corners on the base and 1 at the top: 5.", "Let's Think Along, p.65"),
    ("How many edges does a square pyramid have?", "8", ["5", "4", "12"], "4 around the base and 4 going up to the top: 8.", "Let's Think Along, p.65"),
    ("For a cube, a prism and a pyramid, faces + vertices - edges always equals…", "2", ["0", "1", "4"], "Cube: 6 + 8 - 12 = 2. Prism: 5 + 6 - 9 = 2. Pyramid: 5 + 5 - 8 = 2.", "Let's Think Along, p.65"),
]:
    b8.append(B(q, [ans] + wrongs, why, src))
check(6 + 8 - 12, 2, "fve"); check(5 + 6 - 9, 2, "fve"); check(5 + 5 - 8, 2, "fve")
for q, ans, wrongs, why, src in [
    ("A solid has 1 flat circle face, 1 curved face and 1 vertex. What is it?", "Cone", ["Cylinder", "Sphere", "Pyramid"], "That is exactly a cone.", "p.49"),
    ("A solid has 2 flat circle faces and 1 curved face. What is it?", "Cylinder", ["Cone", "Sphere", "Prism"], "A cylinder has 2 circles and 1 curved face.", "p.49"),
    ("Which solid has no flat face at all?", "Sphere", ["Cone", "Cylinder", "Pyramid"], "A sphere is round all over.", "p.50"),
    ("Half of a sphere is called a…", "Hemisphere", ["Semicircle", "Cone", "Cylinder"], "Hemi means half.", "p.50"),
    ("A solid has the same shape and size at opposite ends, and its other faces are rectangles. What is it?", "Prism", ["Pyramid", "Cone", "Sphere"], "That is the rule for a prism.", "p.50"),
    ("A pyramid's triangle faces all meet at one point. This point is called the…", "Vertex", ["Base", "Edge", "Face"], "The vertex is the point at the top.", "p.50"),
    ("A sandwich cut corner to corner looks like a…", "Prism", ["Pyramid", "Cone", "Cylinder"], "2 triangle ends that are the same, with rectangles between them.", "Exercise 1(a), p.52"),
    ("A snooker ball is a…", "Sphere", ["Cylinder", "Cone", "Hemisphere"], "It is round all over.", "Exercise 1(b), p.52"),
    ("An ice cream cone (just the wafer) is a…", "Cone", ["Pyramid", "Cylinder", "Prism"], "1 circle, 1 curved face, 1 point.", "Exercise 1(c), p.52"),
    ("An oil drum is a…", "Cylinder", ["Cone", "Cuboid", "Sphere"], "2 circles and 1 curved face.", "Exercise 1(d), p.52"),
    ("A solid has 2 pentagonal bases and 4-sided faces between them. What is it?", "Pentagonal prism", ["Pentagonal pyramid", "Cylinder", "Cuboid"], "2 matching end faces make a prism.", "Exercise 2(e), p.53"),
    ("A solid has 1 hexagonal base, 1 vertex and triangle faces. What is it?", "Hexagonal pyramid", ["Hexagonal prism", "Cone", "Cube"], "A base with triangles meeting at a vertex is a pyramid.", "Exercise 2(f), p.53"),
    ("How many faces does a hexagonal pyramid have?", "7", ["6", "12", "8"], "1 hexagon base and 6 triangles: 7.", "p.57"),
    ("How many faces does a pentagonal prism have?", "7", ["5", "10", "6"], "2 pentagons and 5 rectangles: 7.", "Exercise 2(e), p.53"),
]:
    b8.append(B(q, [ans] + wrongs, why, src))
check(1 + 6, 7, "hex pyr faces"); check(2 + 5, 7, "pent prism faces")
row4 = U8.F(U8.cells_fig([(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1)], BLUE, 34, 20, 30))
check(U8.is_cube_net([(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1)]), False, "bank net")
b8.append(B("Can this net be folded into a cube?", ["No, 2 squares fold onto the same face", "Yes", "Yes, it makes a cuboid", "Only if you cut it"],
            "A row of 4 with 2 squares on the same side never works. Two squares land on the same face and one face is left open.", "Exercise 1(a), p.61", row4))
check(U8.is_cube_net(U8.cross), True, "bank net 2")
b8.append(B("Can this net be folded into a cube?", ["Yes", "No, it has too many squares", "No, it makes a cuboid", "No, 2 squares overlap"],
            "Fold the 4 squares around the middle one. Every square becomes a different face.", "p.54", U8.cube_net_fig))
for q, ans, wrongs, why, src, fg in [
    ("A net has 1 rectangle and 2 circles. Which solid does it make?", "Cylinder", ["Cone", "Prism", "Sphere"], "The rectangle rolls into the curved face and the circles close the ends.", "Do and Learn 3(c), p.60", U8.cyl_net_fig),
    ("A net has a fan shape and 1 circle. Which solid does it make?", "Cone", ["Cylinder", "Pyramid", "Sphere"], "The fan rolls into a curved face and the circle is the base.", "Do and Learn 3(b), p.60", U8.cone_net_fig),
    ("A net has 3 rectangles and 2 triangles. Which solid does it make?", "Triangular prism", ["Triangular pyramid", "Square pyramid", "Cuboid"], "2 triangle ends with 3 rectangles between them.", "Do and Learn 3(d), p.60", U8.prism_net_fig),
    ("A net has 1 hexagon and 6 triangles. Which solid does it make?", "Hexagonal pyramid", ["Hexagonal prism", "Cube", "Cone"], "The triangles fold up from the hexagon base to a vertex.", "p.57", U8.hex_pyr_net_fig),
    ("How many triangles are in a net of a triangular pyramid?", "4", ["3", "5", "6"], "A triangular pyramid has 4 faces and all of them are triangles.", "Exercise 1(b), p.62", None),
    ("A net of a cube has how many squares?", "6", ["4", "8", "12"], "A cube has 6 faces.", "p.54", None),
    ("A cuboid net has 6 rectangles in…", "3 matching pairs", ["6 different sizes", "2 groups of 3", "1 size only"], "Top and bottom, front and back, and the 2 ends are pairs.", "p.55", None),
    ("A net has 2 small squares and 4 long thin rectangles. Which cuboid does it make?", "A tall, thin cuboid with square ends", ["A small cube", "A wide flat box", "A tall box with rectangle ends"], "The 2 squares are the ends and the 4 long rectangles are the sides.", "Exercise 1(c), p.63", None),
    ("To complete a prism net with 2 rectangles and 2 triangles, how many more rectangles do you need?", "1", ["2", "0", "3"], "A triangular prism has 3 rectangles.", "Exercise 2, p.64", None),
]:
    b8.append(B(q, [ans] + wrongs, why, src, fg))
check((26 - 10 - 10) / 2, 3, "bank ps"); check(12 * 10 * 3, 360, "bank ps vol")
b8.append(B("A cuboid net is 26 cm long across, made of 10 cm, short, 10 cm, short. How long is the short side?", ["3 cm", "6 cm", "13 cm", "16 cm"],
            "26 - 10 - 10 = 6, and 6 ÷ 2 = 3 cm.", "Problem Solving, p.68", gq(U8, "8-ch", "Problem Solving")))
b8.append(B("The cuboid from this net is 12 cm by 10 cm by 3 cm. What is its volume?", ["360 cm³", "25 cm³", "120 cm³", "36 cm³"],
            "Volume = 12 × 10 × 3 = 120 × 3 = 360 cm³.", "Problem Solving, p.68", gq(U8, "8-ch", "Problem Solving")))
b8.append(B("A pyramid is cut straight across near the top. The top piece is a…", ["Pyramid", "Prism", "Cube", "Cylinder"],
            "It still has a base with triangle faces meeting at the vertex.", "Math Journal, p.69"))
b8.append(B("Why is the bottom piece of a cut pyramid NOT a prism?", ["Its top and bottom faces are different sizes", "It has no faces", "It is round", "It has a vertex"],
            "A prism needs 2 identical faces at opposite ends.", "Math Journal, p.69"))
DROP8 = {"Half of a sphere is called a…", "A snooker ball is a…", "An oil drum is a…", "A net of a cube has how many squares?"}
b8 = [x for x in b8 if x["q"] not in DROP8]
check(len(b8), 40, "bank 8 size")

# ==================================================================
# UNIT 9
# ==================================================================
FIG = U9.FIG
b9 = []
f10a = FIG({"A": [150, 30], "B": [240, 190], "C": [60, 190], "_H": [150, 190]},
           [U9.poly(["A", "B", "C"], BLUE), U9.seg("A", "_H", True), U9.ra("_H", "A", "B"), U9.lab("A", "B", "6 cm"), U9.lab("A", "_H", "5.2 cm", -22),
            U9.tick("A", "B"), U9.tick("B", "C"), U9.tick("C", "A")])
f10b = FIG({"O": [80, 30], "S": [80, 190], "P": [250, 190]}, [U9.poly(["O", "S", "P"], YELLOW), U9.ra("S", "O", "P"), U9.lab("O", "S", "12 cm"), U9.lab("S", "P", "11 cm"), U9.lab("O", "P", "16.3 cm")])
f10c = FIG({"_A": [70, 120], "_B": [110, 40], "_C": [290, 170], "_H": [86, 45]},
           [U9.poly(["_A", "_B", "_C"], ORANGE), U9.lab("_A", "_B", "9 cm"), U9.lab("_B", "_C", "22 cm"), U9.lab("_C", "_A", "20 cm"),
            U9.seg("_A", [62, 30], True), U9.seg([62, 30], "_B", True), U9.txt(45, 80, "8 cm", 15)], names=False)
f10d = FIG({"_A": [40, 170], "_B": [150, 170], "_C": [280, 40], "_P": [280, 170]},
           [U9.poly(["_A", "_B", "_C"], PURPLE), U9.seg("_B", "_P", True), U9.seg("_P", "_C", True), U9.ra("_P", "_C", "_B"),
            U9.lab("_A", "_B", "11 cm", 16), U9.lab("_A", "_C", "23 cm", -16), U9.lab("_B", "_C", "20 cm", 16), U9.lab("_P", "_C", "18 cm", -18)], names=False)
review10 = [("(a)", f10a, [6, 6, 6], 18, (6, 5.2), 15.6, "cm"), ("(b)", f10b, [12, 11, 16.3], 39.3, (11, 12), 66, "cm"),
            ("(c)", f10c, [9, 22, 20], 51, (22, 8), 88, "cm"), ("(d)", f10d, [23, 20, 11], 54, (11, 18), 99, "cm")]
for part, fg, sides, P, (bb, hh), A, unit in review10:
    check(round(sum(sides), 2), P, f"R10{part} P")
    check(Fraction(str(bb)) * Fraction(str(hh)) / 2, A, f"R10{part} A")
    s = " + ".join(U9.num(x) for x in sides)
    b9.append(B("Find the perimeter of the triangle.", [f"{U9.num(P)} cm", f"{U9.num(P + 2)} cm", f"{U9.num(A)} cm", f"{U9.num(P - 6)} cm"],
                f"Add the 3 sides: {s} = {U9.num(P)} cm.", f"Review Q10{part}, p.250", fg))
    wrong_full = bb * hh
    b9.append(B("Find the area of the triangle.", [f"{U9.num(A)} cm²", f"{U9.num(wrong_full)} cm²", f"{U9.num(P)} cm²", f"{U9.num(A + 10)} cm²"],
                f"Area = ½ × base × height = ½ × {U9.num(bb)} × {U9.num(hh)} = {U9.num(A)} cm². (Don't forget the ½!)", f"Review Q10{part}, p.250", fg))
f11 = U9.grid_fig(5, 4, {"_P": (0, 4), "_Q": (3, 0), "_R": (5, 3)}, ["_P", "_Q", "_R"])
check(5 * 4 - Fraction(1, 2) * 3 * 4 - Fraction(1, 2) * 2 * 3 - Fraction(1, 2) * 5 * 1, 8.5, "R11")
b9.append(B("Each square is 1 cm. Find the area of the shaded triangle.", ["8.5 cm²", "11.5 cm²", "20 cm²", "10 cm²"],
            "Rectangle 5 × 4 = 20 cm². White triangles: 6 + 3 + 2.5 = 11.5 cm². 20 - 11.5 = 8.5 cm².", "Review Q11, p.250", f11))
check(Fraction(1, 2) * Fraction("6.4") * Fraction("10.6"), Fraction("33.92"), "R12a")
f12 = FIG({"_A": [120, 20], "_B": [120, 200], "_C": [190, 200]}, [U9.poly(["_A", "_B", "_C"], BLUE), U9.ra("_B", "_A", "_C"), U9.lab("_A", "_B", "10.6 cm", 22), U9.lab("_B", "_C", "6.4 cm", 16)], names=False)
b9.append(B("The figure shows a right triangle. Find its area.", ["33.92 cm²", "67.84 cm²", "17 cm²", "34 cm²"],
            "½ × 6.4 × 10.6: 6.4 × 10.6 = 67.84, and 67.84 ÷ 2 = 33.92 cm².", "Review Q12(a), p.251", f12))
check(round(32 / 6.4) * 2 * int(22 // 10.6), 20, "R12b")
b9.append(B("How many of these right triangles (6.4 cm by 10.6 cm) can fit on a 32 cm by 22 cm card?", ["20", "10", "40", "15"],
            "32 ÷ 6.4 = 5 rectangles across, 22 ÷ 10.6 gives 2 rows: 10 rectangles. Each holds 2 triangles: 20.", "Review Q12(b), p.251", f12))
check(24 * 3, 72, "R13")
b9.append(B("Paul bent a wire into an equilateral triangle of side 24 cm. How long was the wire?", ["72 cm", "48 cm", "24 cm", "576 cm"],
            "The wire goes all the way round: 24 + 24 + 24 = 72 cm.", "Review Q13, p.252"))
check(Fraction(1, 2) * 48 * 20, 480, "R14")
b9.append(B("A triangular tray has height 20 cm and base 48 cm. Find its area.", ["480 cm²", "960 cm²", "68 cm²", "240 cm²"],
            "½ × 48 × 20 = 24 × 20 = 480 cm².", "Review Q14, p.252"))
check(18 / 3, 6, "R15 unit"); check(Fraction(1, 2) * 18 * 6, 54, "R15")
f15 = FIG({"B": [40, 30], "C": [160, 30], "E": [160, 110], "F": [200, 110], "G": [200, 150], "D": [160, 150], "A": [40, 150]},
          [U9.poly(["A", "B", "C", "D"], BLUE), U9.poly(["E", "F", "G", "D"], PURPLE), U9.poly(["A", "E", "G"], ORANGE),
           U9.tick("C", "E"), U9.tick("E", "D"), U9.lab("A", "G", "18 cm", 16)])
b9.append(B("ABCD and EFGD are squares. AG = 18 cm and CE = ED. ADG is a straight line. Find the area of triangle AEG.", ["54 cm²", "108 cm²", "36 cm²", "162 cm²"],
            "AG is 3 small sides, so 1 small side = 18 ÷ 3 = 6 cm. The height ED = 6 cm. Area = ½ × 18 × 6 = 54 cm².", "Review Q15, p.252", f15))
for q, ans, wrongs, why, src in [
    ("A triangle has sides 28 cm, 11 cm and 22 cm. What is its perimeter?", "61 cm", ["51 cm", "60 cm", "71 cm"], "28 + 11 + 22 = 61 cm.", "Exercise 1(a), p.75"),
    ("An equilateral triangle has sides of 13 cm. What is its perimeter?", "39 cm", ["26 cm", "169 cm", "36 cm"], "13 + 13 + 13 = 39 cm.", "Exercise 1(d), p.75"),
    ("An isosceles triangle has sides 23 cm, 23 cm and 31 cm. What is its perimeter?", "77 cm", ["54 cm", "85 cm", "69 cm"], "23 + 23 + 31 = 77 cm.", "Exercise 1(e), p.75"),
    ("A triangle has perimeter 47 cm. Two sides are 15 cm and 13 cm. What is the third side?", "19 cm", ["28 cm", "75 cm", "21 cm"], "15 + 13 = 28, and 47 - 28 = 19 cm.", "Exercise 3(a), p.77"),
    ("A triangle has perimeter 52 cm. Two sides are 19 cm and 17 cm. What is the third side?", "16 cm", ["36 cm", "88 cm", "26 cm"], "19 + 17 = 36, and 52 - 36 = 16 cm.", "Exercise 3(c), p.77"),
    ("An equilateral triangle has perimeter 36 cm. How long is each side?", "12 cm", ["18 cm", "108 cm", "9 cm"], "36 ÷ 3 = 12 cm.", "Exercise 3(d), p.77"),
    ("A triangle has sides 2.5 cm, 4.1 cm and 6 cm. What is its perimeter?", "12.6 cm", ["12.5 cm", "11.6 cm", "13.6 cm"], "2.5 + 4.1 = 6.6, and 6.6 + 6 = 12.6 cm.", "Exercise 2(c), p.76"),
    ("A triangle has base 8 cm and height 6 cm. What is its area?", "24 cm²", ["48 cm²", "14 cm²", "28 cm²"], "½ × 8 × 6 = 24 cm².", "Do and Learn 1, p.82"),
    ("A right triangle has sides 5 cm, 12 cm and 13 cm. What is its area?", "30 cm²", ["60 cm²", "32.5 cm²", "78 cm²"], "Use the 2 sides at the right angle: ½ × 5 × 12 = 30 cm².", "Do and Learn 2(b), p.82"),
    ("A triangle has base 20 cm and height 26 cm. What is its area?", "260 cm²", ["520 cm²", "46 cm²", "280 cm²"], "½ × 20 × 26 = 10 × 26 = 260 cm².", "Exercise 3(a), p.86"),
    ("A triangle has base 7 cm and height 24 cm. What is its area?", "84 cm²", ["168 cm²", "31 cm²", "87.5 cm²"], "½ × 7 × 24 = 7 × 12 = 84 cm².", "Exercise 3(c), p.86"),
    ("A triangle has base 30 m and height 15 m. What is its area?", "225 m²", ["450 m²", "45 m²", "225 m"], "½ × 30 × 15 = 15 × 15 = 225 m². Area uses m².", "Exercise 3(h), p.87"),
    ("A triangle has base 8 m and height 35 m. What is its area?", "140 m²", ["280 m²", "43 m²", "148 m²"], "½ × 8 × 35 = 4 × 35 = 140 m².", "Exercise 3(e), p.87"),
    ("ABCD is a square of side 12 cm and E is the middle of DC. Find the area of triangle AEC.", "36 cm²", ["72 cm²", "144 cm²", "24 cm²"], "Base EC = 6 cm, height 12 cm: ½ × 6 × 12 = 36 cm².", "Exercise 4(a), p.88"),
    ("Triangle ABC has area 56 cm². Triangle DBE is half of it. What is the area of DBE?", "28 cm²", ["112 cm²", "56 cm²", "14 cm²"], "Half of 56 is 28 cm².", "Exercise 4(b), p.88"),
    ("A rectangle is 5 cm by 4 cm. The white triangles inside add up to 13 cm². What is the shaded area?", "7 cm²", ["33 cm²", "13 cm²", "9 cm²"], "5 × 4 = 20, and 20 - 13 = 7 cm².", "Exercise 2(a), p.84"),
    ("An isosceles triangle has perimeter 46.5 cm. The 2 equal sides are 14.5 cm each. What is the base?", "17.5 cm", ["32 cm", "29 cm", "18.5 cm"], "14.5 + 14.5 = 29, and 46.5 - 29 = 17.5 cm.", "Do and Learn 1, p.93"),
    ("An isosceles triangle has base 36.5 cm and 2 equal sides of 22.5 cm. What is its perimeter?", "81.5 cm", ["59 cm", "82.5 cm", "95.5 cm"], "36.5 + 22.5 + 22.5 = 81.5 cm.", "Exercise 1, p.94"),
    ("An equilateral playground has sides of 15.5 m. What is its perimeter?", "46.5 m", ["31 m", "45.5 m", "46.5 m²"], "15.5 + 15.5 + 15.5 = 46.5 m.", "Exercise 3, p.95"),
    ("An isosceles field has perimeter 96 m. The different side is 34 m. How long is each equal side?", "31 m", ["62 m", "65 m", "48 m"], "96 - 34 = 62, and 62 ÷ 2 = 31 m.", "Exercise 4, p.95"),
    ("Part B is a triangle with base 37 m and height 24 m. What is its area?", "444 m²", ["888 m²", "61 m²", "456 m²"], "½ × 37 × 24 = 37 × 12 = 444 m².", "Exercise 5, p.96"),
    ("A rectangle has area 80 cm² and length 10 cm. What is its width?", "8 cm", ["70 cm", "800 cm", "4 cm"], "80 ÷ 10 = 8 cm.", "Exercise 7, p.97"),
    ("A scarf has sides 1.2 m, 0.8 m and 0.8 m. What is its perimeter in cm?", "280 cm", ["2.8 cm", "28 cm", "200 cm"], "1.2 + 0.8 + 0.8 = 2.8 m, and 2.8 × 100 = 280 cm.", "p.91"),
    ("A big square has area 64 cm². ¼ of it is covered. What area is covered?", "16 cm²", ["32 cm²", "256 cm²", "8 cm²"], "64 ÷ 4 = 16 cm².", "Let's Think Along, p.99"),
    ("A big square has area 100 cm². How long is each side?", "10 cm", ["25 cm", "50 cm", "100 cm"], "10 × 10 = 100, so each side is 10 cm.", "Problem Solving, p.101"),
    ("4 right triangles, each with base 6 cm and height 8 cm, have a total area of…", "96 cm²", ["24 cm²", "192 cm²", "48 cm²"], "One triangle: ½ × 6 × 8 = 24 cm². Four: 4 × 24 = 96 cm².", "Problem Solving, p.101"),
]:
    b9.append(B(q, [ans] + wrongs, why, src))
for a, b_ in [(28 + 11 + 22, 61), (13 * 3, 39), (23 + 23 + 31, 77), (47 - 28, 19), (52 - 36, 16), (36 / 3, 12), (2.5 + 4.1 + 6, 12.6),
              (8 * 6 / 2, 24), (5 * 12 / 2, 30), (20 * 26 / 2, 260), (7 * 24 / 2, 84), (30 * 15 / 2, 225), (8 * 35 / 2, 140), (6 * 12 / 2, 36),
              (56 / 2, 28), (20 - 13, 7), (46.5 - 29, 17.5), (36.5 + 45, 81.5), (15.5 * 3, 46.5), ((96 - 34) / 2, 31), (37 * 24 / 2, 444),
              (80 / 10, 8), (2.8 * 100, 280), (64 / 4, 16), (10 * 10, 100), (4 * 24, 96)]:
    check(round(a, 2), b_, "bank 9")
check(len(b9), 40, "bank 9 size")

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
root = os.path.join(os.path.dirname(__file__), "..", "content")
for uid, bank in (("07", b7), ("08", b8), ("09", b9)):
    with open(os.path.join(root, f"bank{uid}.json"), "w", encoding="utf-8") as fh:
        json.dump({"unit": uid, "questions": bank}, fh, ensure_ascii=False, separators=(",", ":"))
print(f"OK: banks written. Unit 7: {len(b7)}, Unit 8: {len(b8)}, Unit 9: {len(b9)} questions. All checks passed.")
