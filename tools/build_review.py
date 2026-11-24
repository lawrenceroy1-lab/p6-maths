"""Builds content/unitreview.json for the Review section (book pages 245 to 264).

One tab per unit (Unit 7 to Unit 14). Every Review question is in book order, every answer is
worked out here and compared with the answer key using check().
Pictures: new ones are drawn here from the book's measurements; others are the same checked
pictures used in the unit banks. Flashcards, match pairs and quiz questions come from the
(already checked) unit files and banks.
Run:  python3 tools/build_review.py
"""
import contextlib
import io
import json
import math
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from geo import check as _check, PROBLEMS, polar  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


def check(value, expected, where):
    if isinstance(expected, Fr):
        if Fr(value) != expected:
            PROBLEMS.append(f"{where}: calculated {value}, answer key says {expected}")
        return value
    return _check(value, expected, where)


with contextlib.redirect_stdout(io.StringIO()):
    from build_unit09 import num, Q, L  # noqa: E402
    import build_unit07 as U7  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
WATER = "#90CAF9"
D = "°"


def load(name):
    return json.load(open(os.path.join(ROOT, "content", name), encoding="utf-8"))


BANK = {u: load(f"bank{u}.json")["questions"] for u in ["07", "08", "09", "10", "11", "12", "13", "14"]}
UNIT = {u: load(f"unit{u}.json") for u in ["07", "08", "09", "10", "11", "12", "13", "14"]}


def bfig(u, src):
    """The picture of a Review question already drawn for the unit bank."""
    for q in BANK[u]:
        if q["src"].startswith(src) and q["fig"]:
            return q["fig"]
    raise KeyError(src)


def F(items, w=320, h=230, pts=None):
    return {"w": w, "h": h, "pts": pts or {}, "items": items}


def t(x, y, s, size=15, color="#1565c0", anchor=None):
    d = {"t": "txt", "at": [round(x, 1), round(y, 1)], "s": s, "size": size, "bold": True, "color": color}
    if anchor:
        d["anchor"] = anchor
    return d


def P(p):
    return [round(p[0], 1), round(p[1], 1)]


def seg(a, b, dash=False, color=None, width=None):
    d = {"t": "seg", "p": [P(a), P(b)]}
    if dash:
        d["dash"] = True
    if color:
        d["color"] = color
    if width:
        d["width"] = width
    return d


def poly(pts, fill):
    return {"t": "poly", "p": [P(p) for p in pts], "fill": fill}


def lab(a, b, s, off):
    return {"t": "len", "p": [P(a), P(b)], "s": s, "off": off}


def tick(a, b, n=1):
    return {"t": "tick", "p": [P(a), P(b)], "n": n}


def ang(v, a, b, s, r=26):
    return {"t": "ang", "v": P(v), "a": P(a), "b": P(b), "s": s, "r": r}


def ra(v, a, b):
    return {"t": "ra", "v": P(v), "a": P(a), "b": P(b)}


def name(p, s, dx, dy):
    return t(p[0] + dx, p[1] + dy, s, 17, "#0D2B6B")


# ---------------- 3D solids made of boxes (oblique drawing) ----------------
K, AL = 0.5, math.radians(35)


class Solid:
    def __init__(self, s, x0=40, y0=None, h=230):
        self.s, self.x0, self.y0 = s, x0, (y0 if y0 is not None else h - 40)
        self.items = []

    def p(self, x, y, z):
        s = self.s
        return [self.x0 + x * s + z * s * K * math.cos(AL), self.y0 - y * s - z * s * K * math.sin(AL)]

    def box(self, x, y, z, w, h, d, fill):
        p = self.p
        front = [p(x, y, z), p(x + w, y, z), p(x + w, y + h, z), p(x, y + h, z)]
        top = [p(x, y + h, z), p(x + w, y + h, z), p(x + w, y + h, z + d), p(x, y + h, z + d)]
        right = [p(x + w, y, z), p(x + w, y, z + d), p(x + w, y + h, z + d), p(x + w, y + h, z)]
        self.items += [poly(front, fill), poly(top, fill), poly(right, fill)]

    def face(self, pts3, fill, clip=None):
        pts = [self.p(*q) for q in pts3]
        if clip:
            pts = clip_poly(pts, [self.p(*q) for q in clip])
        if len(pts) >= 3:
            self.items.append(poly(pts, fill))

    def label(self, a, b, s, off):
        self.items.append(lab(self.p(*a), self.p(*b), s, off))


def clip_poly(subject, clip):
    """Sutherland-Hodgman: the part of polygon subject inside convex polygon clip."""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-9

    def inter(p, q, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p, *q, *a, *b
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        tt = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return [x1 + tt * (x2 - x1), y1 + tt * (y2 - y1)]
    # make the clip polygon go the right way round
    area = sum(clip[i][0] * clip[(i + 1) % len(clip)][1] - clip[(i + 1) % len(clip)][0] * clip[i][1] for i in range(len(clip)))
    if area < 0:
        clip = clip[::-1]
    out = subject
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b):
                out.append(inter(s, e, a, b))
            s = e
    return out


sections = []


def section(sid, unit, title, pages, learn, questions, exp_pages, flash_from, quiz_src):
    """flash and match come from the unit file; the quiz comes from the unit bank (Review questions first)."""
    U = UNIT[flash_from]
    flash, match = [], []
    for s in U["sections"]:
        for f in s["flash"]:
            if f not in flash and len(flash) < 8:
                flash.append(f)
        for m in s["match"]:
            if m not in match and len(match) < 8 and not any(x in sum(match, []) for x in m):
                match.append(m)
    bank = BANK[quiz_src]
    rv = [q for q in bank if q["src"].startswith("Review")]
    rest = [q for q in bank if not q["src"].startswith("Review")]
    quiz = []
    for q in rv + rest:
        if len(quiz) == 10:
            break
        quiz.append({"q": q["q"], "options": q["options"], "fig": q["fig"]})
    sections.append({"id": sid, "title": title, "short": unit, "pages": pages, "learn": learn, "questions": questions,
                     "flash": flash, "match": match, "quiz": quiz})
    EXPECTED[sid] = exp_pages


EXPECTED = {}

# =====================================================================
# UNIT 7: 2D SHAPES (Review Q1 to Q7, p.245 to 247)
# =====================================================================
q7 = []
TICK = "Tick (✓) the correct properties of triangles, and cross (✗) the wrong ones. "
props = [
    ("(a)", "All sides of an isosceles triangle are equal.", False,
     "An isosceles triangle has only <b>2</b> equal sides. (All 3 sides equal is an equilateral triangle.)"),
    ("(b)", "Interior angles of an equilateral triangle are equal.", True,
     "An equilateral triangle has 3 equal sides and 3 equal angles: 180° ÷ 3 = <b>60°</b> each."),
    ("(c)", "An isosceles triangle has 2 equal sides.", True, "Yes. An isosceles triangle has <b>2 equal sides</b>."),
    ("(d)", "Interior angles of an obtuse triangle are all obtuse.", False,
     "An obtuse triangle has only <b>1</b> obtuse angle. The other 2 angles are acute. (3 obtuse angles would be more than 180°.)"),
    ("(e)", "There is 1 right angle inside a right triangle.", True, "Yes. A right triangle has exactly <b>1 right angle</b> (90°)."),
]
check(180 / 3, 60, "Review Q1(b)")
for part, text, ok, why in props:
    q7.append(Q(f"Review 1 {part}", 245, TICK + part + " " + text,
                "Think about what each type of triangle looks like. Draw one if it helps.",
                [why, "So the sentence is <b>" + ("right ✓" if ok else "wrong ✗") + "</b>."],
                ("✓ (correct)" if ok else "✗ (wrong)"), why.replace("<b>", "").replace("</b>", "")))

f2a, f2b, f2c = bfig("07", "Review Q2(a)"), bfig("07", "Review Q2(b)"), bfig("07", "Review Q2(c)")
check(180 / 3, 60, "Review Q2(a) angles")
q7.append(Q("Review 2 (a)", 245, "Fill in the blanks. (a) ABC is an equilateral triangle. ∠BAC = ___°, ∠ABC = ___°, AB = ___ cm, AC = ___ cm",
            "An equilateral triangle has 3 equal sides and 3 equal angles.",
            ["All 3 angles are equal and add up to 180°.", "180° ÷ 3 = <b>60°</b>, so ∠BAC = 60° and ∠ABC = 60°.",
             "All 3 sides are equal. CB = 10 cm, so AB = <b>10 cm</b> and AC = <b>10 cm</b>."],
            "∠BAC = 60°, ∠ABC = 60°, AB = 10 cm, AC = 10 cm", "Equilateral: all angles 60° and all sides equal (10 cm).", f2a))
deDEF = check((180 - 40) / 2, 70, "Review Q2(b)")
q7.append(Q("Review 2 (b)", 245, "Fill in the blanks. (b) DEF is an isosceles triangle. ∠DEF = ___°, DE = ___ cm",
            "The 2 base angles of an isosceles triangle are equal. The 2 equal sides are DE and DF.",
            ["The angles add up to 180°. Take away the top angle: 180° - 40° = <b>140°</b>.",
             "The 2 base angles are equal: 140° ÷ 2 = <b>70°</b>. So ∠DEF = 70°.",
             "DE and DF are the equal sides. DF = 12 cm, so DE = <b>12 cm</b>."],
            "∠DEF = 70°, DE = 12 cm", "(180° - 40°) ÷ 2 = 70°, and DE = DF = 12 cm.", f2b))
jlk = check(180 - 90 - 50, 40, "Review Q2(c)")
check(jlk + 50, 90, "Review Q2(c) sum")
q7.append(Q("Review 2 (c)", 245, "Fill in the blanks. (c) JKL is a right triangle. ∠JKL = ___°, ∠JLK = ___°, ∠JLK + ∠KJL = ___°",
            "The little square at K means a right angle (90°). All 3 angles add up to 180°.",
            ["The little square at K shows ∠JKL = <b>90°</b>.", "∠KJL = 50°.", "∠JLK = 180° - 90° - 50° = <b>40°</b>",
             "∠JLK + ∠KJL = 40° + 50° = <b>90°</b>"],
            "∠JKL = 90°, ∠JLK = 40°, ∠JLK + ∠KJL = 90°", "180° - 90° - 50° = 40°, and 40° + 50° = 90°.", f2c))


def iso_fig(apex_deg, direction, apex_label, base_label, w=300, h=220, apex_text=None):
    """Isosceles triangle. Apex angle apex_deg, pointing in direction (degrees, 0 = right, 90 = down)."""
    Lg = 150 if apex_deg < 100 else 120
    V = [0, 0]
    a1, a2 = math.radians(direction - apex_deg / 2), math.radians(direction + apex_deg / 2)
    B1 = [Lg * math.cos(a1), Lg * math.sin(a1)]
    B2 = [Lg * math.cos(a2), Lg * math.sin(a2)]
    xs, ys = [V[0], B1[0], B2[0]], [V[1], B1[1], B2[1]]
    dx, dy = (w - (max(xs) - min(xs))) / 2 - min(xs), (h - (max(ys) - min(ys))) / 2 - min(ys)
    V, B1, B2 = [V[0] + dx, V[1] + dy], [B1[0] + dx, B1[1] + dy], [B2[0] + dx, B2[1] + dy]
    items = [poly([V, B1, B2], GREEN), tick(V, B1), tick(V, B2)]
    items.append(ang(V, B1, B2, apex_text or apex_label))
    if base_label:
        items.append(ang(B1, B2, V, base_label))
    return F(items, w, h)


fig3a = iso_fig(60, 90, "", "a")
fig3a["items"].insert(3, tick(fig3a["items"][0]["p"][1], fig3a["items"][0]["p"][2]))
fig3a["items"] = [i for i in fig3a["items"] if not (i["t"] == "ang" and i["s"] == "")]
three = [
    ("(a)", fig3a, None, 60, "a",
     ["All 3 sides have a tick mark, so they are all equal. It is an <b>equilateral</b> triangle.",
      "All 3 angles are equal: 180° ÷ 3 = <b>60°</b>"], "∠a = 60°", "An equilateral triangle has 3 equal angles: 180° ÷ 3 = 60°."),
    ("(b)", iso_fig(70, -90, "70°", "b", apex_text="70°"), 70, 55, "b", None, "∠b = 55°", "(180° - 70°) ÷ 2 = 55°."),
    ("(c)", iso_fig(24, 30, "24°", "c", apex_text="24°"), 24, 78, "c", None, "∠c = 78°", "(180° - 24°) ÷ 2 = 78°."),
    ("(d)", iso_fig(110, 160, "110°", "d", apex_text="110°"), 110, 35, "d", None, "∠d = 35°", "(180° - 110°) ÷ 2 = 35°."),
]
check(180 / 3, 60, "Review Q3(a)")
for part, fg, apex, key, letter, steps, ans, why in three:
    if apex is not None:
        rest = 180 - apex
        check(rest / 2, key, f"Review Q3{part}")
        steps = ["The 2 sides with tick marks are equal, so it is an <b>isosceles</b> triangle. Its 2 base angles are equal.",
                 f"Angles in a triangle add up to 180°. Take away the top angle: 180° - {apex}° = <b>{rest}°</b>",
                 f"Share it between the 2 equal angles: {rest}° ÷ 2 = <b>{num(rest / 2)}°</b>"]
    q7.append(Q(f"Review 3 {part}", 246, f"Find each unknown angle. {part}",
                "Look at the tick marks. Equal sides mean equal angles. Angles in a triangle add up to 180°.",
                steps, ans, why, fg))

# Q4: the finished drawings, drawn to scale (1 cm = 26 px)
S4 = 26
C4, B4, A4 = [50, 190], [50 + 5 * S4, 190], [50, 190 - 5 * S4]
ab = check(round(math.hypot(5, 5), 1), 7.1, "Review Q4(a) AB")
fig4a = F([poly([A4, B4, C4], PINK), ra(C4, A4, B4), lab(A4, C4, "5 cm", 16), lab(C4, B4, "5 cm", 16),
           lab(A4, B4, "about 7 cm", -18), name(A4, "A", -14, -4), name(B4, "B", 14, 14), name(C4, "C", -14, 14)], 260, 230)
G4, F4 = [70, 190], [70 + 4 * S4, 190]
E4 = [70 + 2 * S4, 190 - math.sqrt(25 - 4) * S4]
fig4b = F([poly([E4, F4, G4], PINK), lab(G4, F4, "4 cm", 16), lab(E4, G4, "5 cm", 16), lab(E4, F4, "5 cm", -22),
           tick(E4, G4), tick(E4, F4), name(E4, "E", 0, -10), name(F4, "F", 14, 14), name(G4, "G", -14, 14)], 260, 230)
q7.append(Q("Review 4 (a)", 246, "Draw the following triangles. (a) Draw a triangle ABC in which ∠ACB = 90° and AC and CB = 5 cm.",
            "Draw CB first. Then make a right angle at C with a protractor or a set square.",
            ["Use a ruler. Draw a line CB that is <b>5 cm</b> long.",
             "At C, use a protractor (or set square) to draw a line going straight up: <b>90°</b>.",
             "Measure <b>5 cm</b> up this line and mark A.", "Join A to B with the ruler.",
             "Check: AB is about <b>7 cm</b> long."],
            "Triangle ABC with a right angle at C, AC = 5 cm and CB = 5 cm (like the picture).",
            "Two sides of 5 cm with a 90° angle between them make a right isosceles triangle.", fig4a))
q7.append(Q("Review 4 (b)", 246, "Draw the following triangles. (b) Draw a triangle EFG in which EF and EG = 5 cm and GF = 4 cm.",
            "Draw GF first. Then use a compass set to 5 cm from G and from F.",
            ["Use a ruler. Draw a line GF that is <b>4 cm</b> long.", "Open your compass to <b>5 cm</b>.",
             "Put the needle on G and draw an arc above the line.", "Put the needle on F and draw another arc. The arcs cross at <b>E</b>.",
             "Join E to G and E to F. EG = EF = 5 cm."],
            "Triangle EFG with EF = EG = 5 cm and GF = 4 cm (like the picture).",
            "Arcs of 5 cm from G and from F meet at E, so EG and EF are both 5 cm.", fig4b))

O5 = [160, 120]
R5 = 85
pA, pB = polar(O5, R5, 190), polar(O5, R5, 10)
pD = polar(O5, R5, -120)
pE, pF = polar(O5, R5, 150), polar(O5, R5, 40)
fig5 = F([{"t": "circle", "c": P(O5), "r": R5, "fill": YELLOW}, seg(pA, pB), seg(O5, pD), seg(pE, pF), {"t": "dot", "p": P(O5)},
          t(O5[0] + 4, O5[1] - 26, "Center", 13), t(70, 60, "Radius", 13), t(54, 150, "Diameter", 13),
          t(232, 182, "Chord", 13), t(270, 40, "Circumference", 13)], 330, 240)
q7.append(Q("Review 5", 247, "Complete the diagram with parts of a circle.",
            "Use the words: center, radius, diameter, chord, circumference.",
            ["The middle point is the <b>center</b>.", "A line from the center to the edge is a <b>radius</b>.",
             "A line across the circle <b>through the center</b> is a <b>diameter</b>. (It is also a chord.)",
             "A line joining 2 points on the edge, not through the center, is a <b>chord</b>.",
             "The curved line all the way round is the <b>circumference</b>."],
            "Center, Radius, Diameter/Chord, Chord, Circumference (as labelled in the picture).",
            "A diameter goes through the center; a chord does not have to.", fig5))
fig6 = U7.drawn_circle(2, "J", scale=40)
check(4 / 2, 2, "Review Q6")
q7.append(Q("Review 6", 247, "Draw a circle J in which its diameter = 4 cm.",
            "A compass is set to the radius. Radius = diameter ÷ 2.",
            ["Radius = 4 ÷ 2 = <b>2 cm</b>", "Mark the center J.", "Open the compass to <b>2 cm</b> with a ruler.",
             "Put the needle on J and turn the compass all the way round."],
            "A circle with center J and radius 2 cm (diameter 4 cm).", "Diameter 4 cm means radius 2 cm.", fig6))
S7 = 30
K7, O7 = [70, 110], [70 + 6 * S7, 110]
fig7 = F([{"t": "circle", "c": P(K7), "r": 3 * S7, "fill": PINK}, {"t": "circle", "c": P(O7), "r": 3 * S7, "fill": PINK},
          {"t": "dot", "p": P(K7)}, {"t": "dot", "p": P(O7)}, seg(K7, O7, dash=True), lab(K7, [K7[0] + 3 * S7, 110], "3 cm", -14),
          lab([K7[0] + 3 * S7, 110], O7, "3 cm", -14), name(K7, "K", 0, 24), name(O7, "O", 0, 24)], 340, 220)
check(3 + 3, 6, "Review Q7")
q7.append(Q("Review 7", 247, "Draw circles K and O in which their radius = 3 cm and that their circumferences touch each other.",
            "If two circles just touch, how far apart are their centers?",
            ["Each radius is 3 cm. Where the circles touch, the two radii join in a straight line.",
             "So the centers are 3 cm + 3 cm = <b>6 cm</b> apart.", "Draw a line 6 cm long. Mark K at one end and O at the other end.",
             "Set the compass to <b>3 cm</b>. Draw a circle around K, then a circle around O."],
            "Two circles of radius 3 cm with centers K and O 6 cm apart, touching at one point.",
            "The centers are 3 cm + 3 cm = 6 cm apart.", fig7))
learn7 = [
    L("Idea", "Unit 7 in one look",
      "<p>🔺 <b>Equilateral</b>: 3 equal sides, 3 angles of 60°.</p><p>🔺 <b>Isosceles</b>: 2 equal sides, 2 equal base angles.</p>"
      "<p>📐 Angles in a triangle add up to <b>180°</b>.</p><p>⭕ Radius = diameter ÷ 2. A compass is set to the radius.</p>", None, 245),
    L("Example", "Isosceles: find the base angle",
      "<p>Top angle 70°.</p><p>180° - 70° = 110°</p><p>110° ÷ 2 = <b>55°</b> for each base angle.</p>", three[1][1], 246),
]
section("R-07", "Unit 7", "Review: 2D Shapes", "p.245 to 247", learn7, q7, [245, 246, 247], "07", "07")

# =====================================================================
# UNIT 8: 3D SHAPES (Q8 and Q9, p.248 and 249)
# =====================================================================
q8 = []
SOLIDS = [("(a)", "pyramid", "It has a flat base with straight sides and triangle faces that meet at one point (the apex)."),
          ("(b)", "cone", "It has a circle base and a curved surface that comes to one point."),
          ("(c)", "cylinder", "It has 2 equal circle faces and a curved surface."),
          ("(d)", "pyramid", "Its base is a triangle and all the other faces are triangles that meet at one point."),
          ("(e)", "sphere", "It is round like a ball. It has only a curved surface."),
          ("(f)", "pyramid", "Its base has straight sides and the triangle faces meet at one point.")]
for part, ans, why in SOLIDS:
    q8.append(Q(f"Review 8 {part}", 248, f"Which of the following is a cone, cylinder, sphere or pyramid? Fill in the blanks. {part}",
                "Look at the faces. Are they flat or curved? Do they meet at one point?",
                [why, f"So it is a <b>{ans}</b>."], ans.capitalize(), why, bfig("08", f"Review Q8{part}")))
q8.append(Q("Review 9", 249, "Tick (✓) the solid that can be formed from the given net.",
            "Count the faces in the net. What shape is in the middle?",
            ["The net has <b>1 square</b> in the middle.", "It has <b>4 triangles</b>, one on each side of the square.",
             "Fold up the triangles: they meet at one point on top.", "A square base + 4 triangle faces = a <b>square pyramid</b>."],
            "The square pyramid ✓", "1 square and 4 triangles fold into a square pyramid.", bfig("08", "Review Q9")))
learn8 = [L("Idea", "Unit 8 in one look",
            "<p>🔺 <b>Pyramid</b>: flat base, triangle faces meet at one point.</p><p>🍦 <b>Cone</b>: circle base, curved surface, one point.</p>"
            "<p>🥫 <b>Cylinder</b>: 2 circle faces, curved surface.</p><p>⚽ <b>Sphere</b>: round like a ball.</p>"
            "<p>A <b>net</b> is the flat shape that folds up into a solid.</p>", None, 248)]
section("R-08", "Unit 8", "Review: 3D Shapes", "p.248 to 249", learn8, q8, [248, 249], "08", "08")

# =====================================================================
# UNIT 9: PERIMETER AND AREA OF TRIANGLES (Q10 to Q15, p.250 to 252)
# =====================================================================
q9 = []
T10 = [
    ("(a)", [6, 6, 6], 6, 5.2, 18, 15.6, "All 3 sides are 6 cm. The height on base CB is 5.2 cm."),
    ("(b)", [12, 11, 16.3], 11, 12, 39.3, 66, "It is a right triangle: base SP = 11 cm and height OS = 12 cm."),
    ("(c)", [9, 22, 20], 22, 8, 51, 88, "The sides are 9 cm, 22 cm and 20 cm. The height on the 22 cm base is 8 cm."),
    ("(d)", [23, 20, 11], 11, 18, 54, 99, "The sides are 23 cm, 20 cm and 11 cm. The height on the 11 cm base is 18 cm (it is outside the triangle)."),
]
for part, sides, base, hgt, per, area, see in T10:
    p_ = check(round(sum(sides), 2), per, f"Review Q10{part} perimeter")
    a_ = check(base * hgt / 2, area, f"Review Q10{part} area")
    q9.append(Q(f"Review 10 {part}", 250, f"Find the perimeter and area of each triangle. {part}",
                "Perimeter = add all 3 sides. Area = ½ × base × height (the height makes a right angle with the base).",
                [see, "Perimeter = " + " + ".join(num(s) for s in sides) + f" = <b>{num(p_)} cm</b>",
                 f"Area = ½ × base × height = ½ × {num(base)} × {num(hgt)}", f"½ × {num(base * hgt)} = <b>{num(a_)} cm²</b>"],
                f"Perimeter = {num(per)} cm, Area = {num(area)} cm²",
                f"Perimeter: {' + '.join(num(s) for s in sides)} = {num(per)} cm. Area: ½ × {num(base)} × {num(hgt)} = {num(area)} cm².",
                bfig("09", f"Review Q10{part}")))
grid = check(5 * 4, 20, "Review Q11 grid")
aA, aB, aC = check(3 * 4 / 2, 6, "Review Q11 A"), check(2 * 3 / 2, 3, "Review Q11 B"), check(5 * 1 / 2, 2.5, "Review Q11 C")
sh = check(grid - aA - aB - aC, 8.5, "Review Q11")
q9.append(Q("Review 11", 250, "Find the area of the shaded part.",
            "Find the area of the whole grid. Take away the 3 white triangles A, B and C.",
            ["Each square is 1 cm by 1 cm. The grid is 5 × 4 = <b>20 cm²</b>", "Triangle A = ½ × 3 × 4 = <b>6 cm²</b>",
             "Triangle B = ½ × 2 × 3 = <b>3 cm²</b>", "Triangle C = ½ × 5 × 1 = <b>2.5 cm²</b>",
             "Shaded triangle = 20 - 6 - 3 - 2.5 = <b>8.5 cm²</b>"],
            "8.5 cm²", "20 - 6 - 3 - 2.5 = 8.5 cm².", bfig("09", "Review Q11")))
a12 = check(6.4 * 10.6 / 2, 33.92, "Review Q12(a)")
check(6.4 * 5, 32, "Review Q12(b) row")
check(10.6 * 2, 21.2, "Review Q12(b) height")
n12 = check(5 * 2 * 2, 20, "Review Q12(b)")
Q12 = "The figure shows a right triangle. "
q9.append(Q("Review 12 (a)", 251, Q12 + "(a) Find the area of the triangle.", "Area = ½ × base × height.",
            ["Base = 6.4 cm, height = 10.6 cm.", "6.4 × 10.6 = <b>67.84</b>", "½ × 67.84 = <b>33.92 cm²</b>"],
            "33.92 cm²", "½ × 6.4 × 10.6 = 33.92 cm².", bfig("09", "Review Q12(a)")))
q9.append(Q("Review 12 (b)", 251, Q12 + "(b) Find the greatest number of such right triangles that can fit into a rectangular piece of cardboard measuring 32 cm by 22 cm.",
            "Two right triangles make a rectangle 6.4 cm by 10.6 cm. How many of those rectangles fit?",
            ["Along 32 cm: 6.4 × 5 = <b>32 cm</b>, so 5 fit in a row.", "Along 22 cm: 10.6 × 2 = <b>21.2 cm</b>, so 2 rows fit (3 rows would be 31.8 cm, too tall).",
             "Each 6.4 cm by 10.6 cm rectangle holds <b>2</b> right triangles.", "In 1 row: 5 × 2 = <b>10</b> triangles.",
             "In 2 rows: 10 × 2 = <b>20</b> triangles."],
            "20 right triangles", "5 rectangles across × 2 rows × 2 triangles each = 20.", bfig("09", "Review Q12(b)")))
check(10.6 * 3 > 22, True, "Review Q12(b) 3 rows too tall")
w13 = check(24 * 3, 72, "Review Q13")
s13 = 140
fig13 = F([poly([[60, 190], [60 + s13, 190], [60 + s13 / 2, 190 - s13 * 0.866]], YELLOW), tick([60, 190], [60 + s13, 190]),
           tick([60, 190], [60 + s13 / 2, 190 - s13 * 0.866]), tick([60 + s13, 190], [60 + s13 / 2, 190 - s13 * 0.866]),
           lab([60, 190], [60 + s13, 190], "24 cm", 16)], 260, 220)
q9.append(Q("Review 13", 252, "Paul bent a wire into the shape of an equilateral triangle of side 24 cm. What was the length of this wire?",
            "The wire goes all the way round the triangle. That is the perimeter.",
            ["An equilateral triangle has <b>3 equal sides</b> of 24 cm.", "Perimeter = 24 + 24 + 24 = <b>72 cm</b>"],
            "The wire was 72 cm long.", "3 sides of 24 cm: 24 + 24 + 24 = 72 cm.", fig13))
a14 = check(48 * 20 / 2, 480, "Review Q14")
B14 = [[30, 180], [270, 180], [110, 80]]
fig14 = F([poly(B14, ORANGE), seg([110, 80], [110, 180], dash=True), ra([110, 180], [110, 80], [270, 180]),
           lab([30, 180], [270, 180], "48 cm", 16), t(92, 136, "20 cm", 14, "#1565c0", "end")], 300, 210)
q9.append(Q("Review 14", 252, "A triangular tray is of height 20 cm and of base 48 cm. Find the area of this tray.",
            "Area of a triangle = ½ × base × height.",
            ["Base = 48 cm, height = 20 cm.", "48 × 20 = <b>960</b>", "½ × 960 = <b>480 cm²</b>"],
            "The area of the tray is 480 cm².", "½ × 48 × 20 = 480 cm².", fig14))
unit15 = check(18 / 3, 6, "Review Q15 unit")
a15 = check(18 * unit15 / 2, 54, "Review Q15")
q9.append(Q("Review 15", 252, "The figure is made up of 2 squares, ABCD and EFGD. AG = 18 cm and CE = ED. ADG is a straight line. Find the area of triangle AEG.",
            "CE = ED, so the small square's side is half of the big square's side. Use units.",
            ["The small square EFGD has side ED = <b>1 unit</b>.", "CE = ED, so the big square's side CD = <b>2 units</b>. So AD = 2 units.",
             "AG = AD + DG = 2 units + 1 unit = <b>3 units</b> = 18 cm.", "1 unit = 18 ÷ 3 = <b>6 cm</b>",
             "Triangle AEG: base AG = 18 cm, height ED = 6 cm.", "Area = ½ × 18 × 6 = <b>54 cm²</b>"],
            "The area of triangle AEG is 54 cm².", "3 units = 18 cm, so 1 unit = 6 cm. ½ × 18 × 6 = 54 cm².", bfig("09", "Review Q15")))
learn9 = [L("Idea", "Unit 9 in one look",
            "<p>📏 <b>Perimeter</b> = add all the sides.</p><p>🔺 <b>Area of a triangle</b> = ½ × base × height.</p>"
            "<p>The height always makes a <b>right angle</b> with the base. Sometimes it is outside the triangle.</p>"
            "<p>Shaded part = whole area - the white parts.</p>", None, 250)]
section("R-09", "Unit 9", "Review: Perimeter and Area of Triangles", "p.250 to 252", learn9, q9, [250, 251, 252], "09", "09")

# =====================================================================
# UNIT 10: AREA AND PERIMETER OF POLYGONS (Q16 to Q19, p.253 to 255)
# =====================================================================
q10 = []
s16a = check(120 * 6, 720, "Review Q16(a)")
check((6 - 2) * 180, 720, "Review Q16(a) by triangles")
q10.append(Q("Review 16 (a)", 253, "Find the interior angles of each figure. (a)",
             "All 6 sides are equal (tick marks) and each angle is 120°. Add all 6 angles.",
             ["ABCDEF has <b>6</b> angles. Each one is <b>120°</b>.", "Sum = 120° × 6 = <b>720°</b>",
              "Check: a 6-sided shape cuts into 4 triangles: 4 × 180° = 720° ✓"],
             "The interior angles of ABCDEF add up to 720°.", "120° × 6 = 720°.", bfig("10", "Review Q16(a)")))
s16b = check((84 + 48 + 48) + 90 * 4, 540, "Review Q16(b)")
q10.append(Q("Review 16 (b)", 253, "Find the interior angles of each figure. (b)",
             "The figure is a triangle on top of a rectangle. Add the triangle's angles and the rectangle's 4 right angles.",
             ["Triangle IMJ: 84° + 48° + 48° = <b>180°</b>", "Rectangle MJKL: 4 right angles = 90° × 4 = <b>360°</b>",
              "Total = 180° + 360° = <b>540°</b>", "Check: a 5-sided shape cuts into 3 triangles: 3 × 180° = 540° ✓"],
             "The interior angles of IJKLM add up to 540°.", "(84° + 48° + 48°) + (90° × 4) = 540°.", bfig("10", "Review Q16(b)")))
check((5 - 2) * 180, 540, "Review Q16(b) by triangles")

S17 = 6
o17 = [40, 20]
pt = lambda x, y: [o17[0] + x * S17, o17[1] + y * S17]
cx17 = 15 + math.sqrt(16.2 ** 2 - 15 ** 2)
A17, B17, E17, F17, D17, C17 = pt(0, 0), pt(15, 0), pt(15, 15), pt(0, 15), pt(15, 30), pt(cx17, 15)
fig17a = F([poly([A17, B17, E17, F17], ORANGE), poly([B17, C17, D17], ORANGE), seg(B17, D17),
            lab(A17, B17, "15 cm", -14), t(C17[0] + 6, C17[1] - 34, "16.2 cm", 14, "#1565c0", "start"), tick(C17, D17), tick(B17, C17), tick(A17, F17, 2),
            tick(F17, E17, 2), tick(E17, D17, 2), tick(A17, B17, 2),
            name(A17, "A", -12, 0), name(B17, "B", 4, -8), name(C17, "C", 14, 6), name(D17, "D", 0, 20), name(E17, "E", -14, 18),
            name(F17, "F", -14, 6)], 230, 220)
p17a = check(15 + 16.2 + 16.2 + 15 + 15 + 15, 92.4, "Review Q17(a)")
q10.append(Q("Review 17 (a)", 253, "Find the perimeter of this figure. (a)",
             "Go all the way round the outside: A, B, C, D, E, F and back to A. Use the tick marks to find equal sides.",
             ["Sides with 2 ticks are all <b>15 cm</b>: AB, ED, EF and FA.", "Sides with 1 tick are both <b>16.2 cm</b>: BC and CD.",
              "BE is inside the figure, so it is not part of the perimeter.",
              "Perimeter = 15 + 16.2 + 16.2 + 15 + 15 + 15 = <b>92.4 cm</b>"],
             "The perimeter is 92.4 cm.", "15 + 16.2 + 16.2 + 15 + 15 + 15 = 92.4 cm.", fig17a))
# Q17(b): 9-sided polygon, OP = 18 cm, PQ = 16 cm, QR = 18 cm, the other 6 sides are 7 cm
Pp, Qp = [262, 40], [262, 168]
Op, Rp = [118, 40], [118, 168]
left = [Op, [72, 18], [30, 46], [18, 104], [30, 162], [72, 190], Rp]
names17 = ["O", "N", "M", "U", "T", "S", "R"]
its = [poly([Pp, Qp] + left[::-1], BLUE)]
for a, b in zip(left, left[1:]):
    its.append(tick(a, b))
its += [lab(Op, Pp, "18 cm", -14), lab(Pp, Qp, "16 cm", 26), t(96, 18, "7 cm", 13, "#1565c0", "start"), ra(Pp, Op, Qp), ra(Qp, Pp, Rp),
        name(Pp, "P", 12, -4), name(Qp, "Q", 12, 14)]
for p_, n_ in zip(left, names17):
    its.append(name(p_, n_, -12 if p_[0] < 100 else 0, -8 if p_[1] < 104 else 20))
fig17b = F(its, 300, 220)
p17b = check(18 + 16 + 18 + 7 * 6, 94, "Review Q17(b)")
q10.append(Q("Review 17 (b)", 253, "Find the perimeter of this figure. (b)",
             "The tick marks show 6 equal sides of 7 cm. QR is opposite OP.",
             ["OP = <b>18 cm</b> and PQ = <b>16 cm</b>.", "QR is the same length as OP: <b>18 cm</b>.",
              "The 6 sides with tick marks (RS, ST, TU, UM, MN, NO) are each <b>7 cm</b>: 6 × 7 = <b>42 cm</b>",
              "Perimeter = 18 + 16 + 18 + 42 = <b>94 cm</b>"],
             "The perimeter is 94 cm.", "18 + 16 + 18 + 7 + 7 + 7 + 7 + 7 + 7 = 94 cm.", fig17b))

S18 = 11
o18 = [40, 40]
q = lambda x, y: [o18[0] + x * S18, o18[1] + y * S18]
fig18a = F([poly([q(0, 0), q(7, 0), q(7, 7), q(0, 7)], ORANGE), poly([q(7, 0), q(18, 0), q(18, 11), q(7, 11)], YELLOW),
            lab(q(0, 0), q(7, 0), "7 cm", -14), lab(q(7, 0), q(18, 0), "11 cm", -14), t(*q(3.5, 4.3), "A", 17, "#0D2B6B"),
            t(*q(12.5, 6.3), "B", 17, "#0D2B6B")], 280, 200)
aA18, aB18 = check(7 * 7, 49, "Review Q18(a) A"), check(11 * 11, 121, "Review Q18(a) B")
check(aA18 + aB18, 170, "Review Q18(a)")
q10.append(Q("Review 18 (a)", 254, "Find the area of each figure. (All lines meet at right angles.) (a)",
             "Cut the figure into 2 squares, A and B.",
             ["Square A: 7 × 7 = <b>49 cm²</b>", "Square B: 11 × 11 = <b>121 cm²</b>", "Total = 49 + 121 = <b>170 cm²</b>"],
             "170 cm²", "7 × 7 + 11 × 11 = 49 + 121 = 170 cm².", fig18a))
S18b = 7.5
o18b = [75, 30]
r = lambda x, y: [o18b[0] + x * S18b, o18b[1] + y * S18b]
pA, pB, pC, pD, pE, pF, pG, pH = r(0, 0), r(21, 0), r(21, 7), r(14, 7), r(14, 14), r(7, 14), r(7, 24), r(0, 24)
fig18b = F([poly([pA, pB, pC, pD, pE, pF, pG, pH], BLUE), seg(r(0, 7), pD, dash=True), seg(r(0, 14), pF, dash=True),
            lab(pA, pB, "21 cm", -14), lab(pA, pH, "24 cm", 30), tick(pC, pD), tick(pE, pF), tick(pG, pH),
            t(*r(10.5, 4.6), "A", 17, "#0D2B6B"), t(*r(7, 11.6), "B", 17, "#0D2B6B"), t(*r(3.5, 20), "C", 17, "#0D2B6B")]
           + [name(p_, n_, dx, dy) for p_, n_, dx, dy in [(pA, "A", -12, -4), (pB, "B", 12, -4), (pC, "C", 12, 12), (pD, "D", -10, -6),
                                                           (pE, "E", 12, 12), (pF, "F", -10, -6), (pG, "G", 12, 14), (pH, "H", -12, 14)]], 280, 240)
hg = check(21 / 3, 7, "Review Q18(b) HG")
fg = check(24 - 7 - 7, 10, "Review Q18(b) FG")
rA, rB, rC = check(21 * 7, 147, "Review Q18(b) A"), check(14 * 7, 98, "Review Q18(b) B"), check(10 * 7, 70, "Review Q18(b) C")
check(rA + rB + rC, 315, "Review Q18(b)")
q10.append(Q("Review 18 (b)", 254, "Find the area of each figure. (All lines meet at right angles.) (b)",
             "HG, FE and DC have tick marks, so they are equal and together make 21 cm. Cut the figure into 3 rectangles.",
             ["HG + FE + DC = 21 cm and they are equal: 21 ÷ 3 = <b>7 cm</b> each.",
              "The heights: AH = 24 cm. The top 2 steps are 7 cm each, so FG = 24 - 7 - 7 = <b>10 cm</b>.",
              "Rectangle A: 21 × 7 = <b>147 cm²</b>", "Rectangle B: 14 × 7 = <b>98 cm²</b> (21 - 7 = 14 cm wide)",
              "Rectangle C: 10 × 7 = <b>70 cm²</b>", "Total = 147 + 98 + 70 = <b>315 cm²</b>"],
             "315 cm²", "147 + 98 + 70 = 315 cm².", fig18b))

S19 = 7.5
o19 = [40, 200]
u = lambda x, y: [o19[0] + x * S19, o19[1] - y * S19]
F19, E19, D19, A19, G19, B19, C19, H19 = u(0, 0), u(20, 0), u(20, 18), u(0, 18), u(0, 6), u(14, 18), u(14, 24), u(20, 24)
fig19 = F([poly([F19, G19, B19, C19, D19, E19], ORANGE), seg(A19, B19, dash=True), seg(A19, G19, dash=True), seg(C19, H19, dash=True),
           seg(H19, D19, dash=True), lab(A19, G19, "12 cm", 26), lab(D19, E19, "18 cm", -26), lab(F19, E19, "20 cm", 16)]
          + [name(p_, n_, dx, dy) for p_, n_, dx, dy in [(A19, "A", -12, -2), (B19, "B", -10, 18), (C19, "C", -10, -6), (H19, "H", 10, -6),
                                                          (D19, "D", 12, 12), (E19, "E", 12, 14), (F19, "F", -12, 14), (G19, "G", -12, 6)]], 250, 230)
rect19 = check(20 * 18, 360, "Review Q19 rectangle")
bc = check(18 - 12, 6, "Review Q19 BC")
tri_bcd = check(6 * 6 / 2, 18, "Review Q19 BCD")
ab19 = check(20 - 6, 14, "Review Q19 AB")
tri_abg = check(12 * 14 / 2, 84, "Review Q19 ABG")
check(rect19 - tri_abg + tri_bcd, 294, "Review Q19")
q10.append(Q("Review 19", 255, "Joe cut an aluminum sheet into the shape and size as shown below. Find the area of this aluminum sheet. Given that BC = CH = HD = GF, AG = 12 cm and DE = 18 cm.",
             "Start with rectangle ADEF. Take away triangle ABG. Add triangle BCD on top.",
             ["Rectangle ADEF = 20 × 18 = <b>360 cm²</b>", "GF = AF - AG = 18 - 12 = <b>6 cm</b>, so BC = CH = HD = <b>6 cm</b>.",
              "BCHD is a square, so BD = <b>6 cm</b> too. AB = 20 - 6 = <b>14 cm</b>.",
              "White triangle ABG = ½ × 12 × 14 = <b>84 cm²</b>", "Shaded triangle BCD = ½ × 6 × 6 = <b>18 cm²</b>",
              "360 - 84 = <b>276 cm²</b>", "276 + 18 = <b>294 cm²</b>"],
             "The area of the aluminum sheet is 294 cm².", "360 - 84 + 18 = 294 cm².", fig19))
learn10 = [L("Idea", "Unit 10 in one look",
             "<p>📐 Sum of the interior angles = (number of sides - 2) × 180°.</p><p>📏 Perimeter: go all the way round the <b>outside</b>.</p>"
             "<p>Tick marks = equal sides.</p><p>🧩 Area: cut the figure into rectangles, squares and triangles, then add (or take away).</p>", None, 253)]
section("R-10", "Unit 10", "Review: Area and Perimeter of Polygons", "p.253 to 255", learn10, q10, [253, 254, 255], "10", "10")

# =====================================================================
# UNIT 11: CIRCUMFERENCE AND AREA OF CIRCLES (Q20 to Q24, p.256 to 258)
# =====================================================================
q11 = []
for part, kind, v, ans in [("(a)", "r", 8, 16), ("(b)", "r", 7, 14), ("(c)", "d", 31, 31), ("(d)", "r", 8.5, 17)]:
    k = check(2 * v if kind == "r" else v, ans, f"Review Q20{part}")
    steps = ([f"The radius is <b>{num(v)} cm</b>.", "Circumference = 2 × π × radius", f"= 2 × π × {num(v)} = <b>{num(k)}π cm</b>"]
             if kind == "r" else [f"The diameter is <b>{num(v)} cm</b>.", "Circumference = π × diameter", f"= π × {num(v)} = <b>{num(k)}π cm</b>"])
    q11.append(Q(f"Review 20 {part}", 256, f"For each circle, O is the center. Find the circumference of each circle. Leave the answer in terms of π. {part}",
                 "Circumference = 2 × π × radius, or π × diameter. Keep π as π.", steps, f"{num(k)}π cm",
                 f"{'2 × π × ' + num(v) if kind == 'r' else 'π × ' + num(v)} = {num(k)}π cm.", bfig("11", f"Review Q20{part}")))
for part, rr, unit, ans in [("(a)", 42, "cm", 264), ("(b)", 35, "m", 220)]:
    c = check(2 * Fr(22, 7) * rr, ans, f"Review Q21{part}")
    q11.append(Q(f"Review 21 {part}", 257, f"Find the circumference of each circle. (Take π ≈ 22/7.) {part}",
                 "Circumference = 2 × π × radius. Divide by 7 first to make it easy.",
                 [f"Radius = <b>{rr} {unit}</b>", f"Circumference = 2 × 22/7 × {rr}", f"{rr} ÷ 7 = <b>{rr // 7}</b>",
                  f"2 × 22 × {rr // 7} = <b>{num(c)} {unit}</b>"],
                 f"{num(c)} {unit}", f"2 × 22/7 × {rr} = {num(c)} {unit}.", bfig("11", f"Review Q21{part}")))
a22 = check(round(3.14 * 6 * 6, 2), 113.04, "Review Q22(a)")
q11.append(Q("Review 22 (a)", 257, "Find the area of each figure. (Take π ≈ 3.14.) (a)", "Area of a circle = π × radius × radius.",
             ["Radius = <b>6 m</b>", "6 × 6 = <b>36</b>", "3.14 × 36 = <b>113.04 m²</b>"], "113.04 m²", "3.14 × 6 × 6 = 113.04 m².",
             bfig("11", "Review Q22(a)")))
r22 = check(32 / 2, 16, "Review Q22(b) radius")
a22b = check(round(3.14 * 16 * 16 / 2, 2), 401.92, "Review Q22(b)")
fig22b = F([{"t": "sector", "c": [160, 150], "r": 120, "a0": 180, "a1": 360, "fill": YELLOW}, seg([40, 150], [280, 150]),
            lab([40, 150], [280, 150], "32 cm", 16), {"t": "dot", "p": [160, 150]}], 320, 190)
q11.append(Q("Review 22 (b)", 257, "Find the area of each figure. (Take π ≈ 3.14.) (b)",
             "It is half a circle. Find the radius first.",
             ["Radius = 32 ÷ 2 = <b>16 cm</b>", "Whole circle = 3.14 × 16 × 16 = 3.14 × 256 = <b>803.84 cm²</b>",
              "Half of it: 803.84 ÷ 2 = <b>401.92 cm²</b>"],
             "401.92 cm²", "½ × 3.14 × 16 × 16 = 401.92 cm².", fig22b))
check(round(3.14 * 256, 2), 803.84, "Review Q22(b) whole")
arc23 = check(round(2 * 3.14 * 5 / 2, 2), 15.7, "Review Q23 arcs")
p23 = check(round(arc23 + 12 + 12 + 5 + 5, 2), 49.7, "Review Q23")
S23 = 12
L23, R23, Y23 = 70, 70 + 12 * S23, 70
fig23 = F([poly([[L23, Y23], [R23, Y23], [R23, Y23 + 5 * S23], [L23, Y23 + 5 * S23]], YELLOW),
           {"t": "sector", "c": [L23, Y23 + 5 * S23], "r": 5 * S23, "a0": 180, "a1": 270, "fill": YELLOW},
           {"t": "sector", "c": [R23, Y23 + 5 * S23], "r": 5 * S23, "a0": 270, "a1": 360, "fill": YELLOW},
           seg([L23, Y23], [L23, Y23 + 5 * S23], dash=True), seg([R23, Y23], [R23, Y23 + 5 * S23], dash=True),
           lab([L23, Y23], [R23, Y23], "12 cm", -14), lab([R23, Y23 + 5 * S23], [R23 + 5 * S23, Y23 + 5 * S23], "5 cm", 16)], 340, 170)
q11.append(Q("Review 23", 258, "An acrylic sheet is made up of 2 identical quarter circles and a rectangle. Find the perimeter of the acrylic sheet. (Take π ≈ 3.14.)",
             "2 quarter circles make half a circle. Then add the straight edges.",
             ["The quarter circles have radius <b>5 cm</b>.", "2 quarter circles = half a circle.",
              "Half the circumference = ½ × 2 × 3.14 × 5 = <b>15.7 cm</b>",
              "Straight edges: top 12 cm, bottom 5 + 12 + 5 = 22 cm.", "Perimeter = 15.7 + 12 + 12 + 5 + 5 = <b>49.7 cm</b>"],
             "The perimeter is 49.7 cm.", "15.7 + 12 + 12 + 5 + 5 = 49.7 cm.", fig23))
w24 = check(round(3 * 3.14 * 10 / 2, 2), 47.1, "Review Q24")
S24 = 9
cL, cR = [90, 110], [90 + 10 * S24, 110]
r24 = 5 * S24
fig24 = F([{"t": "sector", "c": cL, "r": r24, "a0": 90, "a1": 270, "open": True},
           {"t": "sector", "c": cL, "r": r24, "a0": 270, "a1": 360, "open": True},
           {"t": "sector", "c": cR, "r": r24, "a0": 180, "a1": 360, "open": True},
           {"t": "sector", "c": cR, "r": r24, "a0": 0, "a1": 90, "open": True},
           seg([cL[0] - r24, 110], [cL[0] + r24, 110], dash=True), seg([cR[0] - r24, 110], [cR[0] + r24, 110], dash=True),
           lab([cL[0] - r24, 110], [cL[0] + r24, 110], "10 cm", -12), lab([cR[0] - r24, 110], [cR[0] + r24, 110], "10 cm", -12)], 320, 200)
q11.append(Q("Review 24", 258, "A wire is bent to form 2 semicircles and 2 quarter circles as shown below. What is the length of the wire? (Take π ≈ 3.14.)",
             "2 quarter circles make 1 semicircle. So how many semicircles are there in all?",
             ["2 quarter circles = <b>1 semicircle</b>.", "So the wire is 2 + 1 = <b>3 semicircles</b>, each with diameter 10 cm.",
              "1 semicircle = ½ × 3.14 × 10 = <b>15.7 cm</b>", "3 semicircles = 3 × 15.7 = <b>47.1 cm</b>"],
             "The wire is 47.1 cm long.", "3 × ½ × 3.14 × 10 = 47.1 cm.", fig24))
check(round(3.14 * 10 / 2, 2), 15.7, "Review Q24 one")
learn11 = [L("Idea", "Unit 11 in one look",
             "<p>⭕ Circumference = 2 × π × radius = π × diameter.</p><p>🟡 Area = π × radius × radius.</p>"
             "<p>Half circle = ½ of these. A quarter circle = ¼.</p><p>Use the π the question tells you: 22/7 or 3.14.</p>", None, 256)]
section("R-11", "Unit 11", "Review: Circumference and Area of Circles", "p.256 to 258", learn11, q11, [256, 257, 258], "11", "11")

# =====================================================================
# UNIT 12: VOLUME AND CAPACITY (Q25 and Q26, p.259 and 260)
# =====================================================================
q12 = []


def solid_a():
    s = Solid(11, 62, 170, 210)
    s.box(0, 0, 0, 15, 6, 6, PURPLE)
    s.box(0, 6, 0, 3, 3, 6, PURPLE)
    s.label((0, 0, 0), (15, 0, 0), "15 cm", 16)
    s.label((15, 0, 6), (15, 6, 6), "6 cm", 24)
    s.label((15, 0, 0), (15, 0, 6), "6 cm", 18)
    s.label((0, 6, 0), (0, 9, 0), "3 cm", -24)
    s.label((0, 9, 0), (3, 9, 0), "3 cm", -14)
    return F(s.items, 300, 200)


def solid_b():
    s = Solid(8, 50, 180, 220)
    s.box(0, 0, 0, 16, 16, 8, ORANGE)
    hole = [(4, 4, 0), (12, 4, 0), (12, 12, 0), (4, 12, 0)]
    s.face(hole, "#ffffff")
    s.face([(4, 4, 0), (12, 4, 0), (12, 4, 8), (4, 4, 8)], "#FFCC80", clip=hole)
    s.face([(4, 4, 0), (4, 4, 8), (4, 12, 8), (4, 12, 0)], "#FFB74D", clip=hole)
    s.label((0, 16, 8), (16, 16, 8), "16 cm", -14)
    s.label((4, 12, 0), (12, 12, 0), "8 cm", -12)
    s.label((16, 0, 0), (16, 0, 8), "8 cm", 18)
    s.label((0, 0, 0), (0, 16, 0), "16 cm", -26)
    return F(s.items, 260, 230)


def solid_c():
    s = Solid(6.5, 50, 200, 230)
    s.box(0, 0, 0, 12, 6, 6, BLUE)
    s.box(12, 0, 0, 15, 24, 6, BLUE)
    s.label((0, 0, 0), (27, 0, 0), "27 cm", 16)
    s.label((12, 24, 6), (27, 24, 6), "15 cm", -14)
    s.label((27, 0, 6), (27, 24, 6), "24 cm", 26)
    s.label((0, 0, 0), (0, 6, 0), "6 cm", -22)
    s.label((27, 0, 0), (27, 0, 6), "6 cm", 18)
    return F(s.items, 300, 240)


def solid_d():
    s = Solid(5.5, 58, 200, 230)
    s.box(0, 0, 0, 30, 11, 24, GREEN)
    s.box(0, 11, 12, 30, 11, 12, GREEN)
    s.label((0, 22, 24), (30, 22, 24), "30 cm", -14)
    s.label((30, 11, 24), (30, 22, 24), "11 cm", 24)
    s.label((30, 0, 0), (30, 0, 24), "24 cm", 22)
    s.label((0, 0, 0), (0, 11, 0), "11 cm", -26)
    s.label((0, 22, 12), (0, 22, 24), "12 cm", -18)
    return F(s.items, 330, 240)


def solid_e():
    s = Solid(6.5, 60, 250, 290)
    s.box(0, 0, 0, 12, 30, 18, YELLOW)
    hole = [(2, 30, 2), (10, 30, 2), (10, 30, 16), (2, 30, 16)]
    s.face(hole, "#ffffff")
    s.face([(2, 30, 16), (10, 30, 16), (10, 18, 16), (2, 18, 16)], "#FFF176", clip=hole)
    s.face([(2, 30, 2), (2, 30, 16), (2, 18, 16), (2, 18, 2)], "#FFEE58", clip=hole)
    s.label((0, 30, 0), (12, 30, 0), "12 m", 16)
    s.label((0, 30, 0), (0, 30, 18), "18 m", -18)
    s.label((2, 30, 16), (10, 30, 16), "8 m", -12)
    s.items.append(t(s.p(10, 30, 9)[0] + 8, s.p(10, 30, 9)[1] + 5, "14 m", 14, "#1565c0", "start"))
    s.label((0, 0, 0), (0, 30, 0), "30 m", -26)
    return F(s.items, 260, 290)


def solid_f():
    s = Solid(5, 30, 210, 240)
    s.box(0, 0, 0, 4, 32, 6, PINK)
    s.box(4, 8, 0, 22, 16, 6, PINK)
    s.box(26, 0, 0, 4, 32, 6, PINK)
    s.label((0, 32, 0), (0, 32, 6), "6 m", 18)
    s.label((26, 32, 6), (30, 32, 6), "4 m", -12)
    s.label((30, 0, 6), (30, 32, 6), "32 m", 26)
    s.label((4, 8, 0), (26, 8, 0), "22 m", 14)
    s.label((26, 8, 0), (26, 24, 0), "16 m", -22)
    return F(s.items, 260, 250)


V25 = [
    ("(a)", solid_a(), [("Big block", "15 × 6 × 6", 15 * 6 * 6), ("Small block", "3 × 3 × 6", 3 * 3 * 6)], "+", 594, "cm³",
     "Cut it into 2 blocks. The tick marks show which edges are equal."),
    ("(b)", solid_b(), [("Whole block", "16 × 16 × 8", 16 * 16 * 8), ("Hole", "8 × 8 × 8", 8 * 8 * 8)], "-", 1536, "cm³",
     "Find the volume of the whole block, then take away the square hole."),
    ("(c)", solid_c(), [("Short part", "12 × 6 × 6", 12 * 6 * 6), ("Tall part", "15 × 24 × 6", 15 * 24 * 6)], "+", 2592, "cm³",
     "Cut it into a short part and a tall part. The short part is 27 - 15 = 12 cm long."),
    ("(d)", solid_d(), [("Bottom block", "30 × 24 × 11", 30 * 24 * 11), ("Top block", "30 × 12 × 11", 30 * 12 * 11)], "+", 11880, "cm³",
     "Cut it into a bottom block and a top block. Each block is 11 cm high."),
    ("(e)", solid_e(), [("Whole block", "12 × 18 × 30", 12 * 18 * 30), ("Hole", "8 × 14 × 30", 8 * 14 * 30)], "-", 3120, "m³",
     "Find the volume of the whole block, then take away the hole that goes all the way down."),
    ("(f)", solid_f(), [("Left post", "4 × 6 × 32", 4 * 6 * 32), ("Right post", "4 × 6 × 32", 4 * 6 * 32),
                        ("Middle bar", "22 × 16 × 6", 22 * 16 * 6)], "+", 3648, "m³",
     "Cut the H into 2 posts and a middle bar."),
]
check(27 - 15, 12, "Review Q25(c) short part")
for part, fg, pieces, op, key, unit, hint in V25:
    tot = pieces[0][2] - pieces[1][2] if op == "-" else sum(p_[2] for p_ in pieces)
    check(tot, key, f"Review Q25{part}")
    steps = [f"{nm_}: {how} = <b>{num(v)} {unit}</b>" for nm_, how, v in pieces]
    sumtxt = (f" {op} ").join(num(p_[2]) for p_ in pieces)
    steps.append(f"Volume = {sumtxt} = <b>{num(tot)} {unit}</b>")
    q12.append(Q(f"Review 25 {part}", 259, f"Find the volume of each solid. {part}", hint, steps, f"{num(tot)} {unit}",
                 f"{sumtxt} = {num(tot)} {unit}.", fg))


def tank(s, x, w, d, h, water_h, title):
    s.x0 = x
    s.box(0, 0, 0, w, h, d, "#E3F2FD")
    s.box(0, 0, 0, w, water_h, d, WATER)
    if water_h < h:
        s.face([(0, water_h, 0), (w, water_h, 0), (w, h, 0), (0, h, 0)], "#E3F2FD")
        s.face([(w, water_h, 0), (w, water_h, d), (w, h, d), (w, h, 0)], "#E3F2FD")
    s.items.append(t(s.p(w / 2, 0, 0)[0], s.p(0, 0, 0)[1] + 34, title, 15, "#0D2B6B"))


s26 = Solid(3.2, 20, 175, 220)
tank(s26, 20, 30, 10, 20, 20, "Tank A")
s26.label((0, 0, 0), (30, 0, 0), "30 cm", 14)
s26.label((30, 0, 0), (30, 0, 10), "10 cm", 16)
s26.label((30, 0, 10), (30, 20, 10), "20 cm", -22)
tank(s26, 170, 50, 12, 30, 7.5, "Tank B")
s26.label((0, 0, 0), (50, 0, 0), "50 cm", 14)
s26.label((50, 0, 0), (50, 0, 12), "12 cm", 16)
s26.label((50, 0, 12), (50, 30, 12), "30 cm", -22)
fig26 = F(s26.items, 380, 220)
va = check(30 * 10 * 20, 6000, "Review Q26 A")
vb = check(50 * 12 * 30 / 4, 4500, "Review Q26 B quarter")
vnew = check(va + vb, 10500, "Review Q26(a)")
hnew = check(vnew / (50 * 12), 17.5, "Review Q26(b)")
check(vnew <= 50 * 12 * 30, True, "Review Q26 fits in tank B")
T26 = "Rectangular Tank A is completely filled with water. Rectangular Tank B is 1/4 filled with water. All the water from Tank A is poured into Tank B. "
q12.append(Q("Review 26 (a)", 260, T26 + "(a) What is the new volume of water in Tank B?",
             "Find the water in Tank A and the water already in Tank B. Then add.",
             ["Water in Tank A = 30 × 10 × 20 = <b>6,000 cm³</b>", "Tank B full = 50 × 12 × 30 = <b>18,000 cm³</b>",
              "Tank B is 1/4 full: 18,000 ÷ 4 = <b>4,500 cm³</b>", "New volume = 6,000 + 4,500 = <b>10,500 cm³</b>"],
             "The new volume of water in Tank B is 10,500 cm³.", "6,000 + 4,500 = 10,500 cm³.", fig26))
check(50 * 12 * 30, 18000, "Review Q26 B full")
q12.append(Q("Review 26 (b)", 260, T26 + "(b) What is the new height of the water level in Tank B?",
             "Height = volume ÷ (length × width).",
             ["New volume = <b>10,500 cm³</b> (from part (a)).", "Base of Tank B = 50 × 12 = <b>600 cm²</b>",
              "Height = 10,500 ÷ 600 = <b>17.5 cm</b>"],
             "The new height of the water is 17.5 cm.", "10,500 ÷ (50 × 12) = 17.5 cm.", fig26))
learn12 = [L("Idea", "Unit 12 in one look",
             "<p>🧊 Volume of a cuboid = length × width × height.</p><p>🧩 Odd shapes: cut into cuboids and add, or take away the holes.</p>"
             "<p>💧 Height of water = volume ÷ (length × width).</p><p>1 ℓ = 1,000 cm³.</p>", None, 259)]
section("R-12", "Unit 12", "Review: Volume and Capacity", "p.259 to 260", learn12, q12, [259, 260], "12", "12")

# =====================================================================
# UNIT 13: PATTERNS (Q27 and Q28, p.261)
# =====================================================================
q13 = []
t62 = check(5 + 61 * 9, 554, "Review Q27")
q13.append(Q("Review 27", 261, "5, 14, 23, 32, 41, … What is term 62?",
             "Find the jump. Term 62 has 1 jump less than 62.",
             ["The jump: 14 - 5 = <b>9</b>. The pattern adds 9 each time.",
              "Term 1 is 5 = 5<br>Term 2 is 14 = 5 + (1 × 9)<br>Term 3 is 23 = 5 + (2 × 9)<br>Term 4 is 32 = 5 + (3 × 9)<br>Term 5 is 41 = 5 + (4 × 9)",
              "Term 62 has 62 - 1 = <b>61 jumps</b>.", "Term 62 = 5 + (61 × 9) = 5 + 549 = <b>554</b>"],
             "Term 62 is 554.", "5 + (61 × 9) = 554."))
its28, x = [], 20
for n_ in range(1, 5):
    x_start = x
    for j in range(n_):
        a_, b_, c_ = [x, 70], [x + 26, 70], [x + 13, 47.5]
        its28 += [seg(a_, b_, color="#43A047", width=5), seg(b_, c_, color="#43A047", width=5), seg(c_, a_, color="#43A047", width=5)]
        x += 30
    its28.append(t((x_start + x - 4) / 2, 94, f"{3 * n_} toothpicks", 12, "#37474f"))
    x += 24 if n_ == 1 else 0
    x += 26
fig28 = F(its28, x, 110)
tp = check(28 * 3, 84, "Review Q28")
q13.append(Q("Review 28", 261, "Triangles are made up of toothpicks as shown below: If we want to make 28 triangles, how many toothpicks do we need?",
             "Each triangle is separate and needs its own 3 toothpicks.",
             ["1 triangle needs <b>3</b> toothpicks.", "2 triangles need 2 × 3 = <b>6</b> toothpicks.",
              "3 triangles need 3 × 3 = <b>9</b> toothpicks. 4 triangles need 4 × 3 = <b>12</b>.",
              "28 triangles need 28 × 3 = <b>84</b> toothpicks."],
             "We need 84 toothpicks.", "Each triangle needs 3 toothpicks: 28 × 3 = 84.", fig28))
learn13 = [L("Idea", "Unit 13 in one look",
             "<p>🔢 Find the jump: second term - first term.</p><p>Term number - 1 = number of jumps.</p>"
             "<p>Term = first number + (jumps × jump).</p><p>Shape patterns: count what is added each time.</p>", None, 261)]
section("R-13", "Unit 13", "Review: Patterns", "p.261", learn13, q13, [261], "13", "13")

# =====================================================================
# UNIT 14: PRESENTATION OF DATA (Q29 to Q32, p.262 to 264)
# =====================================================================
q14 = []
B29 = "The pie chart shows the different types of buns sold by a bakery on Saturday. "
fb = bfig("14", "Review Q29")
check(100 - 25, 75, "Review Q29(a)")
tot29 = check(140 * 3, 420, "Review Q29(b)")
cf29 = check(tot29 // 4, 105, "Review Q29(c)")
check(1 - Fr(1, 3) - Fr(1, 4), Fr(5, 12), "Review Q29(d)")
jam = check(cf29 // 7 * 5, 75, "Review Q29(e)")
q14 += [
    Q("Review 29 (a)", 262, B29 + "(a) What was the total percentage of coconut buns, cheese buns and jam buns sold?",
      "Chicken floss buns have a little square: a quarter. The whole circle is 100%.",
      ["Chicken floss buns are a quarter: 1/4 = <b>25%</b>.", "The other buns = 100% - 25% = <b>75%</b>"], "75%", "100% - 25% = 75%.", fb),
    Q("Review 29 (b)", 262, B29 + "(b) There were 140 coconut buns sold. How many buns were sold altogether?",
      "Coconut buns are 1/3 of the circle.",
      ["Coconut buns = 1/3 of all the buns = <b>140</b>.", "3 thirds make the whole: 140 × 3 = <b>420</b>"], "420 buns", "140 × 3 = 420.", fb),
    Q("Review 29 (c)", 262, B29 + "(c) How many chicken floss buns were sold?", "Chicken floss buns are 1/4 of all 420 buns.",
      ["All the buns: <b>420</b>.", "1/4 × 420 = 420 ÷ 4 = <b>105</b>"], "105 chicken floss buns", "1/4 × 420 = 105.", fb),
    Q("Review 29 (d)", 262, B29 + "(d) What fraction of the total number of buns sold were cheese buns and jam buns?",
      "The whole is 1. Take away coconut (1/3) and chicken floss (1/4). Use twelfths.",
      ["1/3 = <b>4/12</b> and 1/4 = <b>3/12</b>.", "1 - 4/12 - 3/12 = 12/12 - 7/12 = <b>5/12</b>"], "5/12", "1 - 1/3 - 1/4 = 5/12.", fb),
    Q("Review 29 (e)", 262, B29 + "(e) The ratio of the number of jam buns to the number of chicken floss buns sold was 5 : 7. How many jam buns were sold?",
      "Chicken floss buns are 7 units = 105.",
      ["Chicken floss buns = 7 units = <b>105</b>.", "1 unit = 105 ÷ 7 = <b>15</b>", "Jam buns = 5 units = 5 × 15 = <b>75</b>"],
      "75 jam buns", "7 units = 105, so 1 unit = 15 and 5 units = 75.", fb),
]
K30 = "The pie chart shows how Mr Kumar spent his money in a month. He spent 5 times as much money on rent as on transport. "
fk = bfig("14", "Review Q30")
check(5 * Fr(1, 9), Fr(5, 9), "Review Q30(a)")
check(1 - Fr(5, 9) - Fr(1, 9), Fr(1, 3), "Review Q30(b)")
q14 += [
    Q("Review 30 (a)", 263, K30 + "(a) What fraction of his money was spent on rent?", "Transport is 1/9. Rent is 5 times as much.",
      ["Transport = <b>1/9</b>.", "Rent = 5 × 1/9 = <b>5/9</b>"], "5/9", "5 × 1/9 = 5/9.", fk),
    Q("Review 30 (b)", 263, K30 + "(b) What fraction of his money was spent on food? Give the answer in the simplest form.",
      "The whole is 1. Take away rent and transport.",
      ["1 - 5/9 = <b>4/9</b>", "4/9 - 1/9 = <b>3/9</b>", "Simplify: divide the top and bottom by 3. 3/9 = <b>1/3</b>"], "1/3",
      "1 - 5/9 - 1/9 = 3/9 = 1/3.", fk),
]
I31 = "The pie chart shows the favorite ice cream flavors of a group of students. 150 students like chocolate-flavored ice creams. "
fi = bfig("14", "Review Q31")
tot31 = check(150 * 2, 300, "Review Q31(a)")
check(tot31 // 4, 75, "Review Q31(b)")
q14 += [
    Q("Review 31 (a)", 263, I31 + "(a) How many students in all took part in the survey?", "Chocolate is half of the circle.",
      ["Chocolate = half of the circle = <b>150</b> students.", "2 halves make the whole: 150 × 2 = <b>300</b>"], "300 students",
      "150 × 2 = 300.", fi),
    Q("Review 31 (b)", 263, I31 + "(b) How many students like strawberry-flavored ice creams?",
      "Strawberry has a little square: it is a quarter of the circle.",
      ["Strawberry = 1/4 of the circle.", "1/4 × 300 = 300 ÷ 4 = <b>75</b>"], "75 students", "1/4 × 300 = 75.", fi),
]
TV = "The pie chart shows the favorite types of TV programs of a group of children. "
ft = bfig("14", "Review Q32")
cart = check(100 - 30 - 15 - 15, 40, "Review Q32(a)")
check(30 / 15, 2, "Review Q32(b)")
tot32 = check(240 * 100 / 40, 600, "Review Q32(c)")
check(15 // 5, 3, "Review Q32(d) drama")
check(40 // 5, 8, "Review Q32(d) cartoon")
q14 += [
    Q("Review 32 (a)", 264, TV + "(a) What percentage of the children like to watch cartoon?", "The whole circle is 100%.",
      ["Comedy 30%, Documentary 15%, Drama 15%.", "Cartoon = 100% - 30% - 15% - 15% = <b>40%</b>"], "40%", "100% - 30% - 15% - 15% = 40%.", ft),
    Q("Review 32 (b)", 264, TV + "(b) How many times as many children like to watch comedy compared to documentary?",
      "Divide comedy by documentary.", ["Comedy = <b>30%</b>, Documentary = <b>15%</b>.", "30 ÷ 15 = <b>2</b>"], "2 times as many",
      "30 ÷ 15 = 2.", ft),
    Q("Review 32 (c)", 264, TV + "(c) There are 240 children who like to watch cartoon. How many children took part in the survey altogether?",
      "Cartoon is 40% and that is 240 children. Find 1%, then 100%.",
      ["40% = <b>240</b> children.", "1% = 240 ÷ 40 = <b>6</b>", "100% = 6 × 100 = <b>600</b>"], "600 children", "240 ÷ 40 × 100 = 600.", ft),
    Q("Review 32 (d)", 264, TV + "(d) What is the ratio of the number of children who like to watch drama to the number of children who like to watch cartoon?",
      "Use the percentages. Drama first, then cartoon. Then simplify.",
      ["Drama : Cartoon", "= 15 : 40", "Divide both by 5: <b>3 : 8</b>"], "3 : 8", "15 : 40 = 3 : 8.", ft),
]
check(240 / 40, 6, "Review Q32(c) 1%")
learn14 = [L("Idea", "Unit 14 in one look",
             "<p>🥧 Whole circle = 1 = 100%.</p><p>Little square = a quarter (1/4 = 25%). Straight line through the centre = halves.</p>"
             "<p>Know one part? Find the total first, then the other parts.</p><p>Ratio: write the numbers in the order the question says, then simplify.</p>", None, 262)]
section("R-14", "Unit 14", "Review: Presentation of Data", "p.262 to 264", learn14, q14, [262, 263, 264], "14", "14")

unit = {"unit": "review", "title": "Review", "pages": "p.245 to 264", "sections": sections, "expectedPages": EXPECTED}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p_ in PROBLEMS:
        print("  -", p_)
    sys.exit(1)
# Practice / Unit Test bank: 5 Review questions from each unit bank (already checked there)
rbank = []
for u in ["07", "08", "09", "10", "11", "12", "13", "14"]:
    rv = [q for q in BANK[u] if q["src"].startswith("Review")]
    rv += [q for q in BANK[u] if not q["src"].startswith("Review")]
    step = max(1, len([q for q in BANK[u] if q["src"].startswith("Review")]) // 5)
    picked = rv[:5 * step:step] if step > 1 else rv[:5]
    for q in picked[:5]:
        rbank.append(dict(q, src=f"Unit {int(u)}: {q['src']}"))
check(len(rbank), 40, "Review bank size")
with open(os.path.join(ROOT, "content", "bankreview.json"), "w", encoding="utf-8") as fh:
    json.dump({"unit": "review", "questions": rbank}, fh, ensure_ascii=False, separators=(",", ":"))
with open(os.path.join(ROOT, "content", "unitreview.json"), "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
print(f"Review written: {sum(len(s['questions']) for s in sections)} questions in {len(sections)} tabs. Every answer matches the answer key ✅")
