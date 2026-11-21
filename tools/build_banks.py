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
    import build_unit10 as U10  # noqa: E402
    import build_unit11 as U11  # noqa: E402
    import build_unit12 as U12  # noqa: E402

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

# ==================================================================
# UNIT 10
# ==================================================================
b10 = []
hexf = FIG({"_%d" % k: p for k, p in enumerate(U10.reg(6, 160, 120, 90, -120))}, [U9.poly(["_%d" % k for k in range(6)], BLUE), U10.ang("_0", "_5", "_1", "120°", 20)], names=False)
check(120 * 6, 720, "R16a")
b10.append(B("Each interior angle of hexagon ABCDEF is 120°. What is the sum of its interior angles?", ["720°", "540°", "360°", "600°"],
             "120° × 6 = 720°. (A hexagon's angles always add up to 720°.)", "Review Q16(a), p.253", hexf))
check(84 + 48 + 48 + 90 * 4, 540, "R16b")
f16b = FIG({"I": [160, 20], "J": [240, 90], "K": [240, 200], "L": [80, 200], "M": [80, 90]},
           [U9.poly(["I", "J", "K", "L", "M"], GREEN), U9.seg("M", "J", True), U10.ang("I", "M", "J", "84°", 20), U10.ang("M", "I", "J", "48°", 26), U9.ra("K", "J", "L"), U9.ra("L", "K", "M")])
b10.append(B("Pentagon IJKLM is a triangle (84°, 48°, 48°) on top of a rectangle. What is the sum of its interior angles?", ["540°", "360°", "720°", "180°"],
             "(84° + 48° + 48°) + (90° × 4) = 180° + 360° = 540°.", "Review Q16(b), p.253", f16b))
check(round(15 + 16.2 + 16.2 + 15 + 15 + 15, 2), 92.4, "R17a")
b10.append(B("A figure is a 15 cm square with a triangle of sides 16.2 cm attached. Its outside edges are 15, 16.2, 16.2, 15, 15 and 15 cm. Perimeter?", ["92.4 cm", "76.2 cm", "108.6 cm", "92 cm"],
             "15 + 16.2 + 16.2 + 15 + 15 + 15 = 92.4 cm.", "Review Q17(a), p.253"))
check(18 + 16 + 18 + 7 * 6, 94, "R17b")
b10.append(B("A polygon has sides of 18 cm, 16 cm, 18 cm and six sides of 7 cm. Perimeter?", ["94 cm", "59 cm", "87 cm", "101 cm"],
             "18 + 16 + 18 = 52, and 6 × 7 = 42. 52 + 42 = 94 cm.", "Review Q17(b), p.253"))
check(7 * 7 + 11 * 11, 170, "R18a")
b10.append(B("A figure is made of a 7 cm square and an 11 cm square. What is its area?", ["170 cm²", "77 cm²", "36 cm²", "324 cm²"],
             "7 × 7 = 49 and 11 × 11 = 121. 49 + 121 = 170 cm².", "Review Q18(a), p.254"))
check(21 / 3, 7, "R18b unit"); check(24 - 7 - 7, 10, "R18b FG"); check(21 * 7 + 14 * 7 + 10 * 7, 315, "R18b")
b10.append(B("HG = FE = DC = 21 ÷ 3 = 7 cm. The figure is 24 cm tall. How long is FG?", ["10 cm", "17 cm", "14 cm", "7 cm"],
             "24 - 7 - 7 = 10 cm.", "Review Q18(b), p.254"))
b10.append(B("The figure is 3 rectangles: 21 × 7, 14 × 7 and 10 × 7 (all in cm). Total area?", ["315 cm²", "345 cm²", "245 cm²", "504 cm²"],
             "147 + 98 + 70 = 315 cm².", "Review Q18(b), p.254"))
check(20 * 18 - Fraction(12 * 14, 2) + Fraction(6 * 6, 2), 294, "R19")
b10.append(B("Rectangle ADEF is 20 cm × 18 cm. Take away triangle ABG (84 cm²) and add triangle BCD (18 cm²). Area of the sheet?", ["294 cm²", "258 cm²", "360 cm²", "462 cm²"],
             "360 - 84 = 276, and 276 + 18 = 294 cm².", "Review Q19, p.255"))
for q, ans, wrongs, why, src in [
    ("The interior angles of a pentagon add up to…", "540°", ["360°", "720°", "500°"], "A pentagon splits into 3 triangles: 3 × 180° = 540°.", "p.108"),
    ("The interior angles of an octagon add up to…", "1,080°", ["720°", "1,440°", "900°"], "An octagon splits into 6 triangles: 6 × 180° = 1,080°.", "p.108"),
    ("A quadrilateral has angles 90°, 120° and 120°. What is the fourth angle?", "30°", ["60°", "330°", "150°"], "360° - 90° - 120° - 120° = 30°.", "p.111"),
    ("ABCD is a parallelogram with ∠DAB = 140°. What is ∠ABC?", "40°", ["140°", "220°", "50°"], "Angles between parallel sides add up to 180°: 180° - 140° = 40°.", "p.110"),
    ("A rhombus has an angle of 60°. What is the angle next to it?", "120°", ["60°", "30°", "300°"], "180° - 60° = 120°.", "p.110"),
    ("A trapezium has ∠NKL = 112° between its parallel sides. What is the other angle on the same side?", "68°", ["112°", "248°", "78°"], "180° - 112° = 68°.", "p.110"),
    ("ABCD is a parallelogram. ∠BCD = 108° and ∠DBC = 53°. Find ∠ABD.", "19°", ["72°", "55°", "37°"], "∠ABC = 180° - 108° = 72°, and 72° - 53° = 19°.", "Do and Learn, p.114"),
    ("An isosceles triangle has a vertex angle of 105°. Each base angle is…", "37.5°", ["75°", "52.5°", "42.5°"], "(180° - 105°) ÷ 2 = 75° ÷ 2 = 37.5°.", "Exercise 1(a), p.115"),
    ("A rhombus has an angle of 69°. The angles next to it are…", "111°", ["69°", "21°", "291°"], "180° - 69° = 111°.", "Exercise 1(b), p.115"),
    ("The outside angle at a corner is 114°. The reflex angle inside is…", "246°", ["66°", "114°", "156°"], "Angles at a point add up to 360°: 360° - 114° = 246°.", "Exercise 1(d), p.115"),
    ("Each angle of a regular octagon is 135°. A rectangle corner inside uses 90°. What is left?", "45°", ["35°", "90°", "225°"], "135° - 90° = 45°.", "Exercise 1(f), p.115"),
    ("∠BCF = 143° and ∠FCD = 130°. Angles at point C add up to 360°. What is ∠DCB?", "87°", ["93°", "273°", "107°"], "360° - 143° - 130° = 87°.", "Exercise 2, p.116"),
    ("A rhombus ECFD has ∠CFD = 110°. Find ∠FDC.", "35°", ["70°", "55°", "110°"], "Triangle FDC has FD = FC: (180° - 110°) ÷ 2 = 35°.", "Exercise 3, p.116"),
    ("DBEC is a rectangle. ∠CBE = 35°. Find ∠DBC.", "55°", ["35°", "145°", "65°"], "∠DBE = 90°, so 90° - 35° = 55°.", "Exercise 5, p.117"),
    ("A pentagon has sides 9, 12, 21, 13.5 and 12 cm. Perimeter?", "67.5 cm", ["55.5 cm", "66.5 cm", "57 cm"], "9 + 12 + 21 + 13.5 + 12 = 67.5 cm.", "p.118"),
    ("A regular hexagon has sides of 3.5 m. Perimeter in cm?", "2,100 cm", ["21 cm", "210 cm", "1,750 cm"], "3.5 × 6 = 21 m = 2,100 cm.", "Exercise 1(c), p.121"),
    ("A regular octagon has sides of 2.9 m. Perimeter?", "23.2 m", ["17.4 m", "20.3 m", "29 m"], "2.9 × 8 = 23.2 m.", "Exercise 1(d), p.121"),
    ("A star has 10 equal sides of 2 m. Perimeter in cm?", "2,000 cm", ["200 cm", "1,000 cm", "20 cm"], "2 × 10 = 20 m = 2,000 cm.", "Exercise 1(b), p.121"),
    ("Polygon A has perimeter 42.7 m and polygon B 39.4 m. Difference?", "3.3 m", ["82.1 m", "13.3 m", "3.7 m"], "42.7 - 39.4 = 3.3 m.", "Exercise 3, p.123"),
    ("A figure is a triangle (½ × 5 × 4), a 6 m × 5 m rectangle and a 6 m square. Total area?", "76 m²", ["66 m²", "86 m²", "96 m²"], "10 + 30 + 36 = 76 m².", "Do and Learn, p.127"),
    ("A trapezium has height 5 m and parallel sides 19 m and 26 m. Area?", "112.5 m²", ["225 m²", "50 m²", "120 m²"], "½ × 5 × (19 + 26) = ½ × 5 × 45 = 112.5 m².", "Exercise 1(c), p.128"),
    ("A 12 m square has white parts of 36 m² and 72 m². Shaded area?", "36 m²", ["108 m²", "144 m²", "72 m²"], "144 - 36 - 72 = 36 m².", "Exercise 1(e), p.129"),
    ("A square has area 81 cm². How long is each side?", "9 cm", ["40.5 cm", "8 cm", "27 cm"], "9 × 9 = 81.", "Exercise 4, p.131"),
    ("Squares of 81 cm² and 49 cm² have sides that form a right triangle. Its area?", "31.5 cm²", ["63 cm²", "65 cm²", "16 cm²"], "Sides 9 cm and 7 cm: ½ × 9 × 7 = 31.5 cm².", "Exercise 4, p.131"),
    ("A regular hexagonal tray has perimeter 144 cm. Each side?", "24 cm", ["36 cm", "18 cm", "864 cm"], "144 ÷ 6 = 24 cm.", "p.132"),
    ("A square of area 144 m². How long is each side?", "12 m", ["72 m", "36 m", "14 m"], "12 × 12 = 144.", "p.134"),
    ("A 12 cm square paper has two corners cut off, each ½ × 6 × 6. Area of the pentagon left?", "108 cm²", ["126 cm²", "36 cm²", "144 cm²"], "144 - 18 - 18 = 108 cm².", "Do and Learn 2, p.135"),
    ("A plot of 156 m² costs 12,000 baht per m². Total cost?", "1,872,000 baht", ["187,200 baht", "168,000 baht", "18,720,000 baht"], "156 × 12,000 = 1,872,000 baht.", "Exercise 4, p.137"),
    ("A 150 cm wire makes 5 long and 5 short sides. One long + one short side is…", "30 cm", ["15 cm", "75 cm", "60 cm"], "150 ÷ 5 = 30 cm.", "Exercise 5, p.138"),
    ("A fence is 1,500 m all round; 1,392.5 m is finished. How much is left?", "107.5 m", ["117.5 m", "2,892.5 m", "100 m"], "1,500 - 1,392.5 = 107.5 m.", "Exercise 6, p.138"),
    ("8 right triangles, each with sides 3 cm and 4 cm at the right angle, make a hexagon. Area?", "48 cm²", ["96 cm²", "24 cm²", "84 cm²"], "½ × 3 × 4 = 6 cm², and 6 × 8 = 48 cm².", "Exercise 9(c), p.140"),
    ("Janice used the slanted side 5 cm as the height of a triangle with base 6 cm. The real height is 4 cm. Correct triangle area?", "12 cm²", ["15 cm²", "24 cm²", "30 cm²"], "½ × 6 × 4 = 12 cm². The height must meet the base at a right angle.", "Math Journal, p.145"),
]:
    b10.append(B(q, [ans] + wrongs, why, src))
for a, b_ in [(3 * 180, 540), (6 * 180, 1080), (360 - 330, 30), (180 - 140, 40), (180 - 60, 120), (180 - 112, 68), (72 - 53, 19), ((180 - 105) / 2, 37.5),
              (180 - 69, 111), (360 - 114, 246), (135 - 90, 45), (360 - 143 - 130, 87), ((180 - 110) / 2, 35), (90 - 35, 55), (9 + 12 + 21 + 13.5 + 12, 67.5),
              (3.5 * 6 * 100, 2100), (round(2.9 * 8, 2), 23.2), (2 * 10 * 100, 2000), (round(42.7 - 39.4, 2), 3.3), (10 + 30 + 36, 76), (2.5 * 45, 112.5),
              (144 - 36 - 72, 36), (9 * 9, 81), (9 * 7 / 2, 31.5), (144 / 6, 24), (12 * 12, 144), (144 - 36, 108), (156 * 12000, 1872000), (150 / 5, 30),
              (1500 - 1392.5, 107.5), (6 * 8, 48), (6 * 4 / 2, 12)]:
    check(a, b_, "bank 10")
check(len(b10), 40, "bank 10 size")

# ==================================================================
# UNIT 11
# ==================================================================
P7, P314, r2 = U11.P7, U11.P314, U11.r2
Fr = Fraction
b11 = []
for part, kind, v, ans, wrongs in [("(a)", "r", 8, "16π cm", ["8π cm", "64π cm", "32π cm"]), ("(b)", "r", 7, "14π cm", ["7π cm", "49π cm", "28π cm"]),
                                   ("(c)", "d", 31, "31π cm", ["62π cm", "15.5π cm", "961π cm"]), ("(d)", "r", 8.5, "17π cm", ["8.5π cm", "72.25π cm", "34π cm"])]:
    b11.append(B("O is the center. Find the circumference of the circle. Leave the answer in terms of π.", [ans] + wrongs,
                 ("Circumference = π × diameter = π × " + U9.num(v) if kind == "d" else f"Circumference = 2 × π × radius = 2 × π × {U9.num(v)}") + f" = {ans}.",
                 f"Review Q20{part}, p.256", U11.cfig(kind, v, "cm", ORANGE)))
check(r2(2 * P7 * 42), 264, "R21a"); check(r2(P7 * 70), 220, "R21b")
b11.append(B("Radius 42 cm. Find the circumference. (Take π ≈ 22/7.)", ["264 cm", "132 cm", "5,544 cm", "528 cm"], "2 × 22/7 × 42: 84 ÷ 7 = 12, 22 × 12 = 264 cm.", "Review Q21(a), p.257", U11.cfig("r", 42, "cm", BLUE)))
b11.append(B("Radius 35 m. Find the circumference. (Take π ≈ 22/7.)", ["220 m", "110 m", "3,850 m", "440 m"], "2 × 22/7 × 35: 70 ÷ 7 = 10, 22 × 10 = 220 m.", "Review Q21(b), p.257", U11.cfig("r", 35, "m", ORANGE)))
check(r2(P314 * 36), 113.04, "R22a"); check(r2(Fr(1, 2) * P314 * 256), 401.92, "R22b")
b11.append(B("Radius 6 m. Find the area. (Take π ≈ 3.14.)", ["113.04 m²", "37.68 m²", "18.84 m²", "452.16 m²"], "3.14 × 6 × 6 = 3.14 × 36 = 113.04 m².", "Review Q22(a), p.257", U11.cfig("r", 6, "m", YELLOW)))
b11.append(B("A semicircle has diameter 32 cm. Find its area. (Take π ≈ 3.14.)", ["401.92 cm²", "803.84 cm²", "1,607.68 cm²", "50.24 cm²"], "Radius 16 cm: ½ × 3.14 × 16 × 16 = ½ × 803.84 = 401.92 cm².", "Review Q22(b), p.257"))
check(r2(Fr(1, 2) * 2 * P314 * 5 + 12 + 12 + 5 + 5), 49.7, "R23")
b11.append(B("An acrylic sheet is 2 quarter circles (radius 5 cm) and a 12 cm by 5 cm rectangle. Perimeter? (Take π ≈ 3.14.)", ["49.7 cm", "39.7 cm", "31.4 cm", "44.7 cm"],
             "The 2 quarter arcs make half a circle: ½ × 2 × 3.14 × 5 = 15.7 cm. Then 15.7 + 12 + 12 + 5 + 5 = 49.7 cm.", "Review Q23, p.258"))
check(r2(3 * Fr(1, 2) * P314 * 10), 47.1, "R24")
b11.append(B("A wire forms 2 semicircles and 2 quarter circles, each with diameter 10 cm. Length of wire? (Take π ≈ 3.14.)", ["47.1 cm", "31.4 cm", "62.8 cm", "94.2 cm"],
             "2 semicircles + 2 quarter circles = 3 half circles: 3 × ½ × 3.14 × 10 = 47.1 cm.", "Review Q24, p.258"))
for q, ans, wrongs, why, src, a, b_ in [
    ("Radius 7 m. Circumference? (π ≈ 22/7)", "44 m", ["22 m", "154 m", "88 m"], "2 × 22/7 × 7 = 2 × 22 = 44 m.", "p.150", r2(2 * P7 * 7), 44),
    ("Diameter 21 cm. Circumference? (π ≈ 22/7)", "66 cm", ["33 cm", "132 cm", "1,386 cm"], "21 ÷ 7 = 3, 22 × 3 = 66 cm.", "p.151", r2(P7 * 21), 66),
    ("Semicircle, diameter 10 cm. Perimeter? (π ≈ 3.14)", "25.7 cm", ["15.7 cm", "31.4 cm", "20.7 cm"], "Arc 15.7 cm + diameter 10 cm = 25.7 cm.", "p.151", r2(P314 * 5 + 10), 25.7),
    ("Quarter circle, radius 5 cm. Perimeter? (π ≈ 3.14)", "17.85 cm", ["7.85 cm", "12.85 cm", "31.4 cm"], "Arc 7.85 cm + 5 + 5 = 17.85 cm.", "p.152", r2(P314 * Fr(10, 4) + 10), 17.85),
    ("Radius 40 cm. Circumference? (π ≈ 3.14)", "251.2 cm", ["125.6 cm", "5,024 cm", "502.4 cm"], "2 × 3.14 × 40 = 3.14 × 80 = 251.2 cm.", "Do and Learn (a), p.153", r2(P314 * 80), 251.2),
    ("Diameter 20.5 cm. Circumference? (π ≈ 3.14)", "64.37 cm", ["128.74 cm", "32.19 cm", "41 cm"], "3.14 × 20.5 = 64.37 cm.", "Do and Learn (b), p.153", r2(P314 * Fr("20.5")), 64.37),
    ("Estimate the circumference of a circle with diameter 13 cm.", "About 39 cm", ["About 13 cm", "About 26 cm", "About 169 cm"], "About 3 × the diameter: 3 × 13 = 39 cm.", "Exercise 1(c), p.154", 39, 39),
    ("Radius 8.4 cm. Circumference? (π ≈ 22/7)", "52.8 cm", ["26.4 cm", "221.76 cm", "16.8 cm"], "2 × 8.4 = 16.8, 16.8 ÷ 7 = 2.4, 22 × 2.4 = 52.8 cm.", "Exercise 2(b), p.155", r2(P7 * Fr("16.8")), 52.8),
    ("Diameter 18 cm. Circumference? (π ≈ 3.14)", "56.52 cm", ["113.04 cm", "28.26 cm", "254.34 cm"], "3.14 × 18 = 56.52 cm.", "Exercise 3(a), p.155", r2(P314 * 18), 56.52),
    ("3 quarter circles of radius 21 cm plus 2 radii. Perimeter? (π ≈ 22/7)", "141 cm", ["99 cm", "132 cm", "174 cm"], "¾ × 132 = 99 cm, then 99 + 21 + 21 = 141 cm.", "Exercise 4(a), p.156", r2(Fr(3, 4) * 2 * P7 * 21 + 42), 141),
    ("A coaster has diameter 6 cm. Area in terms of π?", "9π cm²", ["36π cm²", "6π cm²", "3π cm²"], "Radius 3 cm: π × 3 × 3 = 9π cm².", "Do and Learn 1, p.162", 9, 9),
    ("Radius 14 cm. Area? (π ≈ 22/7)", "616 cm²", ["88 cm²", "308 cm²", "1,232 cm²"], "22/7 × 14 × 14: 14 ÷ 7 = 2, 22 × 2 × 14 = 616 cm².", "Do and Learn 2(a), p.162", r2(P7 * 196), 616),
    ("Diameter 42 m. Area? (π ≈ 22/7)", "1,386 m²", ["5,544 m²", "132 m²", "693 m²"], "Radius 21 m: 22/7 × 21 × 21 = 66 × 21 = 1,386 m².", "Do and Learn 2(b), p.162", r2(P7 * 441), 1386),
    ("Radius 18 cm. Area? (π ≈ 3.14)", "1,017.36 cm²", ["113.04 cm²", "254.34 cm²", "56.52 cm²"], "3.14 × 18 × 18 = 3.14 × 324 = 1,017.36 cm².", "Do and Learn 3(a), p.162", r2(P314 * 324), 1017.36),
    ("Diameter 26 m. Area? (π ≈ 3.14)", "530.66 m²", ["2,122.64 m²", "81.64 m²", "40.82 m²"], "Radius 13 m: 3.14 × 13 × 13 = 530.66 m².", "Do and Learn 3(b), p.162", r2(P314 * 169), 530.66),
    ("Radius 9.2 cm. Area in terms of π?", "84.64π cm²", ["18.4π cm²", "9.2π cm²", "42.32π cm²"], "π × 9.2 × 9.2 = 84.64π cm².", "Exercise 1(b), p.163", 84.64, 84.64),
    ("Diameter 38 m. Area in terms of π?", "361π m²", ["1,444π m²", "38π m²", "19π m²"], "Radius 19 m: π × 19 × 19 = 361π m².", "Exercise 1(d), p.163", 361, 361),
    ("Radius 4 m. Area? (π ≈ 3.14)", "50.24 m²", ["25.12 m²", "12.56 m²", "200.96 m²"], "3.14 × 4 × 4 = 3.14 × 16 = 50.24 m².", "Exercise 3, p.164", r2(P314 * 16), 50.24),
    ("Diameter 34 cm. Area? (π ≈ 3.14)", "907.46 cm²", ["3,629.84 cm²", "106.76 cm²", "453.73 cm²"], "Radius 17 cm: 3.14 × 17 × 17 = 3.14 × 289 = 907.46 cm².", "Exercise 4, p.164", r2(P314 * 289), 907.46),
    ("Semicircle with diameter 28 cm. Area? (π ≈ 22/7)", "308 cm²", ["616 cm²", "1,232 cm²", "44 cm²"], "Radius 14 cm: ½ × 22/7 × 14 × 14 = ½ × 616 = 308 cm².", "Exercise 5(a), p.165", r2(P7 * 98), 308),
    ("Quarter circle with radius 21 cm. Area? (π ≈ 22/7)", "346.5 cm²", ["1,386 cm²", "693 cm²", "33 cm²"], "¼ × 22/7 × 21 × 21 = ¼ × 1,386 = 346.5 cm².", "Exercise 5(b), p.165", r2(P7 * Fr(441, 4)), 346.5),
    ("A circular paper has diameter 14 cm. Area? (π ≈ 3.14)", "153.86 cm²", ["615.44 cm²", "43.96 cm²", "21.98 cm²"], "Radius 7 cm: 3.14 × 49 = 153.86 cm².", "p.166", r2(P314 * 49), 153.86),
    ("A circular field has diameter 12.5 m. Circumference? (π ≈ 3.14)", "39.25 m", ["78.5 m", "122.66 m", "19.63 m"], "3.14 × 12.5 = 39.25 m.", "p.166", r2(P314 * Fr("12.5")), 39.25),
    ("A semicircle (radius 10 cm) has a triangle (base 20 cm, height 10 cm) inside. Shaded area? (π ≈ 22/7)", "57.14 cm²", ["157.14 cm²", "100 cm²", "214.29 cm²"], "157.14 - 100 = 57.14 cm².", "Do and Learn 1, p.170", r2(P7 * 50 - 100), 57.14),
    ("A table has radius 26.5 cm. Length of cloth around it? (π ≈ 22/7)", "166.57 cm", ["83.29 cm", "2,207.07 cm", "53 cm"], "2 × 22/7 × 26.5 = 1,166 ÷ 7 ≈ 166.57 cm.", "Exercise 1, p.171", r2(2 * P7 * Fr("26.5")), 166.57),
    ("A wheel of radius 25 cm makes 50 turns. Distance in meters? (π ≈ 3.14)", "78.5 m", ["7,850 m", "157 m", "39.25 m"], "1 turn = 157 cm. 50 × 157 = 7,850 cm = 78.5 m.", "Exercise 3, p.172", r2(P314 * 50 * 50 / 100), 78.5),
    ("A wheel of diameter 49 cm rolls 924 cm. How many complete turns? (π ≈ 22/7)", "6", ["154", "19", "3"], "1 turn = 154 cm. 924 ÷ 154 = 6.", "Exercise 4, p.172", r2(924 / (P7 * 49)), 6),
    ("⅓ of a circle with radius 9 cm. Perimeter of that part? (π ≈ 3.14)", "36.84 cm", ["18.84 cm", "56.52 cm", "27.84 cm"], "Arc = ⅓ × 56.52 = 18.84 cm, plus 9 + 9 = 36.84 cm.", "Exercise 5(a), p.173", r2(Fr(1, 3) * P314 * 18 + 18), 36.84),
    ("A 28 cm square handkerchief with 8 semicircles of radius 7 cm. Area? (π ≈ 22/7)", "1,400 cm²", ["784 cm²", "2,016 cm²", "1,092 cm²"], "784 + 4 × 154 = 784 + 616 = 1,400 cm².", "Exercise 6, p.173", r2(784 + 4 * P7 * 49), 1400),
    ("2 wheels (radius 7 cm) close 88 cm every 2 seconds and must cover 704 cm. Time? (π ≈ 22/7)", "16 seconds", ["8 seconds", "32 seconds", "4 seconds"], "704 ÷ 88 = 8 turns, 8 × 2 = 16 seconds.", "Problem Solving, p.177", 704 / 88 * 2, 16),
]:
    check(a, b_, f"bank 11 {src}")
    b11.append(B(q, [ans] + wrongs, why, src))
check(len(b11), 40, "bank 11 size")

# ==================================================================
# UNIT 12
# ==================================================================
b12 = []
b12_items = [
    ("An L-shaped solid is 6 cm deep. Its front is a 27 cm × 6 cm base with a 15 cm × 18 cm column on top. Volume?", "2,592 cm³", ["432 cm³", "1,620 cm³", "2,952 cm³"],
     "Front area = 27 × 6 + 15 × 18 = 162 + 270 = 432 cm². Volume = 432 × 6 = 2,592 cm³.", "Review Q25(c), p.259", 27 * 6 * 6 + 15 * 18 * 6, 2592),
    ("A step solid: a 30 × 24 × 11 block with a 30 × 12 × 11 block on top (cm). Volume?", "11,880 cm³", ["7,920 cm³", "3,960 cm³", "15,840 cm³"],
     "30 × 24 × 11 = 7,920 and 30 × 12 × 11 = 3,960. 7,920 + 3,960 = 11,880 cm³.", "Review Q25(d), p.259", 30 * 24 * 11 + 30 * 12 * 11, 11880),
    ("A 12 m × 18 m × 30 m block has an 8 m × 14 m hole all the way down. Volume?", "3,120 m³", ["6,480 m³", "3,360 m³", "9,840 m³"],
     "12 × 18 × 30 = 6,480. Hole: 8 × 14 × 30 = 3,360. 6,480 - 3,360 = 3,120 m³.", "Review Q25(e), p.259", 12 * 18 * 30 - 8 * 14 * 30, 3120),
    ("Tank A (30 × 10 × 20 cm) is full. Tank B (50 × 12 × 30 cm) is ¼ full. All of A is poured into B. New volume in B?", "10,500 cm³", ["6,000 cm³", "4,500 cm³", "18,000 cm³"],
     "A = 30 × 10 × 20 = 6,000 cm³. B had ¼ × 50 × 12 × 30 = 4,500 cm³. 6,000 + 4,500 = 10,500 cm³.", "Review Q26(a), p.260", 6000 + 4500, 10500),
    ("Tank B (base 50 cm × 12 cm) now holds 10,500 cm³. Water height?", "17.5 cm", ["175 cm", "21 cm", "7.5 cm"], "10,500 ÷ (50 × 12) = 10,500 ÷ 600 = 17.5 cm.", "Review Q26(b), p.260", 10500 / 600, 17.5),
    ("A solid has 14 unit cubes. Its volume is…", "14 cubic units", ["7 cubic units", "28 cubic units", "14 square units"], "Each unit cube is 1 cubic unit.", "Let's Recall 1, p.182", 14, 14),
    ("A cube is 2 cm by 2 cm by 2 cm. Volume?", "8 cm³", ["6 cm³", "4 cm³", "12 cm³"], "2 × 2 × 2 = 8 cm³.", "Let's Recall 2, p.183", 8, 8),
    ("A cuboid is 8 m by 4 m by 3 m. Volume?", "96 m³", ["15 m³", "32 m³", "88 m³"], "8 × 4 × 3 = 96 m³.", "Let's Recall 3, p.183", 96, 96),
    ("A tank 32 × 18 × 20 cm is ⅔ full. Volume of water?", "7,680 cm³", ["11,520 cm³", "3,840 cm³", "5,760 cm³"], "Capacity 11,520 cm³. ⅔ of it: 11,520 ÷ 3 × 2 = 7,680 cm³.", "Let's Recall 4, p.183", 11520 * 2 / 3, 7680),
    ("A cuboid has base area 70 cm² and volume 840 cm³. Height?", "12 cm", ["14 cm", "910 cm", "770 cm"], "840 ÷ 70 = 12 cm.", "p.187", 840 / 70, 12),
    ("Volume 1,190 cm³, shaded face 85 cm². The other edge?", "14 cm", ["1,105 cm", "17 cm", "12 cm"], "1,190 ÷ 85 = 14 cm.", "p.187", 1190 / 85, 14),
    ("A cube's face has area 36 cm². Edge?", "6 cm", ["18 cm", "9 cm", "12 cm"], "6 × 6 = 36.", "p.188", 6 * 6, 36),
    ("A cube has volume 512 m³. Edge?", "8 m", ["16 m", "64 m", "170.7 m"], "8 × 8 × 8 = 512.", "p.188", 8 ** 3, 512),
    ("A solid: 12 × 1.5 × 4.5 plus 4 × 1.5 × 9.5 (cm). Volume?", "138 cm³", ["81 cm³", "57 cm³", "128 cm³"], "81 + 57 = 138 cm³.", "p.189", 81 + 57, 138),
    ("A container: column 5 × 4 × 15 plus base 20 × 4 × 8 (m). Capacity?", "940 m³", ["640 m³", "300 m³", "760 m³"], "300 + 640 = 940 m³.", "Do and Learn, p.191", 300 + 640, 940),
    ("Volume 6,480 cm³, shaded face 360 cm². The other edge?", "18 cm", ["16 cm", "6,120 cm", "20 cm"], "6,480 ÷ 360 = 18 cm.", "Exercise 1(b), p.192", 6480 / 360, 18),
    ("Volume 7,644 cm³, shaded face 364 cm². The other edge?", "21 cm", ["12 cm", "7,280 cm", "24 cm"], "7,644 ÷ 364 = 21 cm.", "Exercise 1(c), p.192", 7644 / 364, 21),
    ("A cube's face has area 169 cm². Edge?", "13 cm", ["84.5 cm", "16 cm", "11 cm"], "13 × 13 = 169.", "Exercise 2(a), p.193", 13 * 13, 169),
    ("A cube has volume 216 cm³. Edge?", "6 cm", ["72 cm", "36 cm", "8 cm"], "6 × 6 × 6 = 216.", "Exercise 3(a), p.193", 6 ** 3, 216),
    ("Steps of 10 × 5 × 8, 20 × 5 × 8 and 30 × 5 × 8 (cm). Volume?", "2,400 cm³", ["1,200 cm³", "4,800 cm³", "2,000 cm³"], "400 + 800 + 1,200 = 2,400 cm³.", "Exercise 4(b), p.194", 400 + 800 + 1200, 2400),
    ("A 10 × 4 × 15 m block with an 8 × 4 × 7 m hole. Volume?", "376 m³", ["600 m³", "224 m³", "824 m³"], "600 - 224 = 376 m³.", "Exercise 4(c), p.194", 600 - 224, 376),
    ("Water: 6 × 6 × 11 twice, plus 11 × 6 × 7 (cm). Volume?", "1,254 cm³", ["858 cm³", "1,650 cm³", "1,045 cm³"], "396 + 462 + 396 = 1,254 cm³.", "Exercise 5(a), p.195", 396 * 2 + 462, 1254),
    ("A pool holds 28 m³. Peter pours in 32 m³. How much overflows?", "4 m³", ["60 m³", "28 m³", "2 m³"], "32 - 28 = 4 m³.", "Exercise 6, p.196", 32 - 28, 4),
    ("You have 164 cm³ and need 424 cm³. How much more?", "260 cm³", ["588 cm³", "160 cm³", "250 cm³"], "424 - 164 = 260 cm³.", "Exercise 7, p.196", 424 - 164, 260),
    ("A cuboid is 10 m long with volume 250 m³ and 2 square faces. Side of each square?", "5 m", ["25 m", "15 m", "2.5 m"], "250 ÷ 10 = 25 m², and 5 × 5 = 25.", "p.197", 250 / 10, 25),
    ("Cube A is 27 cm³. Cube B's edge is 4 times A's edge. Volume of B?", "1,728 cm³", ["108 cm³", "432 cm³", "144 cm³"], "A's edge is 3 cm, B's is 12 cm. 12 × 12 × 12 = 1,728 cm³.", "p.197", 12 ** 3, 1728),
    ("A tank 38 cm × 24 cm has water 15 cm high. 5,472 cm³ is poured away. New water height?", "9 cm", ["6 cm", "21 cm", "12 cm"], "Drop = 5,472 ÷ 912 = 6 cm. 15 - 6 = 9 cm.", "p.198", 15 - 5472 / 912, 9),
    ("A metal piece: 2 × 1.25 × 4 twice, plus 8 × 1.25 × 2 (m). Volume?", "40 m³", ["30 m³", "20 m³", "50 m³"], "10 + 20 + 10 = 40 m³.", "Do and Learn, p.202", 10 + 20 + 10, 40),
    ("A tank has base area 8 m² and holds 56 m³. Water height?", "7 m", ["48 m", "64 m", "8 m"], "56 ÷ 8 = 7 m.", "Exercise 1, p.203", 56 / 8, 7),
    ("17.64 ℓ in cm³?", "17,640 cm³", ["1,764 cm³", "176.4 cm³", "17,640,000 cm³"], "1 ℓ = 1,000 cm³: 17.64 × 1,000 = 17,640 cm³.", "Exercise 2, p.203", 17.64 * 1000, 17640),
    ("A tank (base 980 cm²) holds 17,640 cm³ when full. It is ⅔ full. Water height?", "12 cm", ["18 cm", "6 cm", "27 cm"], "Tank height 17,640 ÷ 980 = 18 cm. ⅔ of 18 = 12 cm.", "Exercise 2, p.203", 18 * 2 / 3, 12),
    ("A tank with a 40 cm square base is ⅓ full with 36 ℓ. Height of the tank?", "67.5 cm", ["22.5 cm", "45 cm", "90 cm"], "36,000 ÷ 1,600 = 22.5 cm of water. × 3 = 67.5 cm.", "Exercise 3, p.204", 36000 / 1600 * 3, 67.5),
    ("A tap fills 12 ℓ a minute for half an hour into a 75 cm × 60 cm tank. Tank height?", "80 cm", ["8 cm", "360 cm", "48 cm"], "12 × 30 = 360 ℓ = 360,000 cm³. 360,000 ÷ 4,500 = 80 cm.", "Exercise 4, p.204", 360000 / 4500, 80),
    ("A marble cut: 2 cubes of 10 cm plus a 36 × 3 × 20 cm slab. Volume?", "4,160 cm³", ["2,160 cm³", "3,160 cm³", "4,060 cm³"], "1,000 + 2,160 + 1,000 = 4,160 cm³.", "Exercise 5, p.205", 1000 + 2160 + 1000, 4160),
    ("A vase: 9 × 9 × 24 + 9 × 9 × 16 + 9 × 9 × 8 (cm). Capacity?", "3,888 cm³", ["1,944 cm³", "3,880 cm³", "4,212 cm³"], "1,944 + 1,296 + 648 = 3,888 cm³.", "Exercise 6, p.205", 1944 + 1296 + 648, 3888),
    ("7.875 m³ in cm³?", "7,875,000 cm³", ["7,875 cm³", "78,750 cm³", "787,500 cm³"], "1 m³ = 1,000,000 cm³: 7.875 × 1,000,000 = 7,875,000 cm³.", "Exercise 7, p.206", 7.875 * 1000000, 7875000),
    ("A water box of 3,200 cm³ has a 1,200 cm³ block inside. Water?", "2,000 cm³", ["4,400 cm³", "3,200 cm³", "1,200 cm³"], "3,200 - 1,200 = 2,000 cm³.", "Exercise 8, p.206", 3200 - 1200, 2000),
    ("An E-shaped tank: 3 arms of 20 × 9 × 9 and a back of 10 × 9 × 45 (cm). Capacity?", "8,910 cm³", ["5,670 cm³", "4,860 cm³", "8,100 cm³"], "1,620 × 3 + 4,050 = 8,910 cm³.", "Exercise 9(a), p.207", 1620 * 3 + 4050, 8910),
    ("Tank B (30 × 20 × 15 cm) is filled at 10 ℓ a minute. How long?", "9/10 min", ["9 min", "90 min", "1 1/2 min"], "30 × 20 × 15 = 9,000 cm³ = 9 ℓ. 9 ÷ 10 = 9/10 min.", "Exercise 10(a), p.208", 9000 / 1000 / 10, 0.9),
    ("Container X (base 800 cm²) has water 36 cm high. Volume of water?", "28,800 cm³", ["836 cm³", "22,800 cm³", "2,880 cm³"], "800 × 36 = 28,800 cm³.", "Let's Think Along, p.209", 800 * 36, 28800),
]
for q, ans, wrongs, why, src, a, b_ in b12_items:
    check(round(a, 4), b_, f"bank 12 {src}")
    b12.append(B(q, [ans] + wrongs, why, src))
check(len(b12), 40, "bank 12 size")

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
root = os.path.join(os.path.dirname(__file__), "..", "content")
for uid, bank in (("07", b7), ("08", b8), ("09", b9), ("10", b10), ("11", b11), ("12", b12)):
    with open(os.path.join(root, f"bank{uid}.json"), "w", encoding="utf-8") as fh:
        json.dump({"unit": uid, "questions": bank}, fh, ensure_ascii=False, separators=(",", ":"))
print(f"OK: banks written. Unit 7: {len(b7)}, Unit 8: {len(b8)}, Unit 9: {len(b9)}, Unit 10: {len(b10)}, Unit 11: {len(b11)}, Unit 12: {len(b12)} questions. All checks passed.")
