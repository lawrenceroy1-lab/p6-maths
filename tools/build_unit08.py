"""Builds content/unit08.json for Unit 8: 3D Shapes (book pages 47 to 70).

Checks: every cube net is tested by "rolling" a cube over it, face counts of
nets are compared with the solid, F + V - E and the volume are calculated.
Run:  python3 tools/build_unit08.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from geo import check, PROBLEMS  # noqa: E402

ORANGE, YELLOW, GREEN, BLUE, PINK, PURPLE = "#FFE0B2", "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#D1C4E9"
LINE = "#1f2a44"


def Q(label, page, q, hint, steps, answer, why, fig=None):
    return {"label": label, "page": page, "q": q, "fig": fig, "hint": hint, "steps": steps, "answer": answer, "why": why}


def L(tag, title, html, fig=None, page=None):
    return {"tag": tag, "title": title, "html": html, "fig": fig, "page": page}


def F(items, w=320, h=230):
    return {"w": w, "h": h, "pts": {}, "items": items}


def txt(x, y, s, size=16, bold=True, color=None):
    d = {"t": "txt", "at": [x, y], "s": s, "size": size, "bold": bold}
    if color:
        d["color"] = color
    return d


def seg(a, b, dash=False, width=None):
    d = {"t": "seg", "p": [a, b]}
    if dash:
        d["dash"] = True
    if width:
        d["width"] = width
    return d


def poly(pts, fill):
    return {"t": "poly", "p": [list(p) for p in pts], "fill": fill}


# ------------------------------------------------------------------
# Solid drawings (oblique view)
# ------------------------------------------------------------------
def cuboid(x, y, w, h, d, fill, hidden=True):
    """Front face top-left (x, y), width w, height h, depth offset d."""
    dx, dy = d * 0.7, -d * 0.6
    A, B, C, D = [x, y], [x + w, y], [x + w, y + h], [x, y + h]
    items = [poly([A, B, C, D], fill),
             poly([A, [A[0] + dx, A[1] + dy], [B[0] + dx, B[1] + dy], B], fill),
             poly([B, [B[0] + dx, B[1] + dy], [C[0] + dx, C[1] + dy], C], fill)]
    if hidden:
        H = [D[0] + dx, D[1] + dy]
        items += [seg(H, [A[0] + dx, A[1] + dy], True, 1.5), seg(H, [C[0] + dx, C[1] + dy], True, 1.5), seg(H, D, True, 1.5)]
    return items


def cylinder(cx, top, rx, ry, h, fill):
    return [poly([[cx - rx, top], [cx + rx, top], [cx + rx, top + h], [cx - rx, top + h]], fill),
            {"t": "ell", "c": [cx, top + h], "rx": rx, "ry": ry, "fill": fill},
            poly([[cx - rx, top], [cx + rx, top], [cx + rx, top + h], [cx - rx, top + h]], fill),
            {"t": "ell", "c": [cx, top + h], "rx": rx, "ry": ry, "half": "front"},
            {"t": "ell", "c": [cx, top + h], "rx": rx, "ry": ry, "half": "back", "dash": True},
            {"t": "ell", "c": [cx, top], "rx": rx, "ry": ry, "fill": fill}]


def cone(cx, apex_y, base_y, rx, ry, fill, flip=False):
    if flip:  # point down (ice cream)
        return [poly([[cx - rx, base_y], [cx + rx, base_y], [cx, apex_y]], fill),
                {"t": "ell", "c": [cx, base_y], "rx": rx, "ry": ry, "fill": fill}]
    return [poly([[cx - rx, base_y], [cx, apex_y], [cx + rx, base_y]], fill),
            {"t": "ell", "c": [cx, base_y], "rx": rx, "ry": ry, "half": "front", "fill": fill},
            {"t": "ell", "c": [cx, base_y], "rx": rx, "ry": ry, "half": "back", "dash": True}]


def sphere(cx, cy, r, fill, equator=True):
    items = [{"t": "circle", "c": [cx, cy], "r": r, "fill": fill}]
    if equator:
        items += [{"t": "ell", "c": [cx, cy], "rx": r, "ry": r * 0.3, "half": "front"},
                  {"t": "ell", "c": [cx, cy], "rx": r, "ry": r * 0.3, "half": "back", "dash": True}]
    return items


def pyramid(base, apex, fill, hidden_idx=()):
    """base: list of points (front ones first); hidden_idx: base corners hidden at the back."""
    items = []
    n = len(base)
    vis = [i for i in range(n) if i not in hidden_idx]
    # visible side faces
    for i in range(n):
        j = (i + 1) % n
        if i in vis and j in vis:
            items.append(poly([base[i], base[j], apex], fill))
    for i in range(n):
        j = (i + 1) % n
        if i in hidden_idx or j in hidden_idx:
            items.append(seg(base[i], base[j], True, 1.5))
    for i in hidden_idx:
        items.append(seg(base[i], apex, True, 1.5))
    for i in vis:
        items.append(seg(base[i], apex))
    return items


def prism(front, d, fill, hidden_idx=()):
    """front: polygon of the front end; d: depth offset."""
    dx, dy = d * 0.8, -d * 0.45
    back = [[p[0] + dx, p[1] + dy] for p in front]
    n = len(front)
    items = []
    for i in range(n):
        j = (i + 1) % n
        if i in hidden_idx or j in hidden_idx:
            continue
        items.append(poly([front[i], front[j], back[j], back[i]], fill))
    items.append(poly(front, fill))
    for i in range(n):
        j = (i + 1) % n
        if i in hidden_idx or j in hidden_idx:
            items.append(seg(back[i], back[j], True, 1.5))
    for i in hidden_idx:
        items.append(seg(front[i], back[i], True, 1.5))
    return items


def square_pyramid(cx, by, w, h, fill):
    base = [[cx - w / 2, by], [cx + w / 2 - 20, by], [cx + w / 2 + 20, by - 35], [cx - w / 2 + 40, by - 35]]
    return pyramid(base, [cx + 5, by - h], fill, hidden_idx=(3,))


def tri_pyramid(cx, by, w, h, fill):
    base = [[cx - w / 2, by], [cx + w / 2, by], [cx + 10, by - 30]]
    return pyramid(base, [cx, by - h], fill, hidden_idx=(2,))


def hex_pyramid(cx, by, r, h, fill):
    import math
    base = [[cx + r * math.cos(math.radians(a)), by + r * 0.35 * math.sin(math.radians(a))] for a in (180, 120, 60, 0, -60, -120)]
    # angles 120 and 60 are toward the front (positive y)
    return pyramid(base, [cx, by - h], fill, hidden_idx=(4, 5))


def pent_prism(fill):
    import math
    front = [[90 + 55 * math.cos(math.radians(a)), 150 + 55 * math.sin(math.radians(a))] for a in (-90, -18, 54, 126, 198)]
    return prism(front, 150, fill, hidden_idx=(4,))


def tri_prism(x, y, w, h, d, fill):
    front = [[x, y + h], [x + w, y + h], [x + w / 2, y]]
    return prism(front, d, fill, hidden_idx=(0,))


# ------------------------------------------------------------------
# Net tools
# ------------------------------------------------------------------
def roll(state, direction):
    D, U, N, S, E, W = state
    if direction == "E":
        return (E, W, N, S, U, D)
    if direction == "W":
        return (W, E, N, S, D, U)
    if direction == "N":
        return (N, S, U, D, E, W)
    return (S, N, D, U, E, W)  # "S"


def is_cube_net(cells):
    """Roll a cube over the cells. A net works if every square gets a different face."""
    cells = set(cells)
    if len(cells) != 6:
        return False
    start = sorted(cells)[0]
    seen = {start: (0, 1, 2, 3, 4, 5)}
    todo = [start]
    while todo:
        c = todo.pop()
        x, y = c
        for nb, dr in (((x + 1, y), "E"), ((x - 1, y), "W"), ((x, y - 1), "N"), ((x, y + 1), "S")):
            if nb in cells and nb not in seen:
                seen[nb] = roll(seen[c], dr)
                todo.append(nb)
    if len(seen) != 6:
        return False
    return len({s[0] for s in seen.values()}) == 6


def cells_fig(cells, fill, size=34, x0=20, y0=20, highlight=None, grid=None):
    items = []
    if grid:
        cols, rows = grid
        items.append({"t": "grid", "x": x0, "y": y0, "cols": cols, "rows": rows, "size": size})
    for (cx, cy) in cells:
        x, y = x0 + cx * size, y0 + cy * size
        f = fill
        if highlight and (cx, cy) in highlight:
            f = "#F48FB1"
        items.append(poly([[x, y], [x + size, y], [x + size, y + size], [x, y + size]], f))
    return items


def rect(x, y, w, h, fill):
    return poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], fill)


def eq_tri(x, y, s, up=True):
    import math
    h = s * math.sqrt(3) / 2
    return [[x, y + h], [x + s, y + h], [x + s / 2, y]] if up else [[x, y], [x + s, y], [x + s / 2, y + h]]


sections = []

# ==================================================================
# 8.1 CONES, CYLINDERS, SPHERES AND PYRAMIDS (p.48 to 53)
# ==================================================================
f_cube = F(cuboid(110, 80, 100, 100, 70, BLUE))
f_cuboid = F(cuboid(60, 100, 180, 70, 60, GREEN))
f_cone = F(cone(160, 30, 180, 70, 20, ORANGE))
f_cyl = F(cylinder(160, 45, 65, 18, 140, PURPLE))
f_sph = F(sphere(160, 115, 85, YELLOW) + [{"t": "dot", "p": [160, 115]}, seg([160, 115], [245, 115], True),
                                           txt(205, 108, "radius", 14, color="#1565c0"), txt(150, 132, "center", 14)])
f_pyr = F(square_pyramid(160, 200, 180, 170, PINK) + [txt(250, 215, "base", 15), txt(160, 20, "vertex", 15)])
f_prism = F(tri_prism(50, 70, 110, 100, 150, GREEN))

learn81 = [
    L("Idea", "Cubes (Let's Recall)", "<p>A <b>cube</b> has <b>6 square faces</b>. All the faces are the same size.</p>", f_cube, 48),
    L("Example", "Objects that are cubes", "<p>A dice 🎲 and a square wooden crate are cubes.</p><p>Every face is a square of the same size.</p>", f_cube, 48),
    L("Idea", "Cuboids (Let's Recall)", "<p>A <b>cuboid</b> can have <b>6 rectangular faces</b>.</p><p>It can also have <b>4 rectangular faces and 2 square faces</b>.</p>", f_cuboid, 48),
    L("Example", "Objects that are cuboids", "<p>A sponge and a juice carton are cuboids.</p><p>Their faces are rectangles.</p>", f_cuboid, 48),
    L("Idea", "Cone", "<p>A solid <b>cone</b> has <b>1 flat face</b> (a circle) and <b>1 curved face</b>.</p><p>It has 1 vertex (the point).</p>", f_cone, 49),
    L("Example", "Objects that are cones", "<p>An ice cream cone 🍦 and a party hat 🎉 are cones.</p>", f_cone, 49),
    L("Idea", "Cylinder", "<p>A solid <b>cylinder</b> has <b>2 flat faces</b> (circles) and <b>1 curved face</b>.</p>", f_cyl, 49),
    L("Example", "Objects that are cylinders", "<p>A can of drink 🥫, a chalk pastel and an oil drum are cylinders.</p>", f_cyl, 49),
    L("Idea", "Sphere", "<p>A <b>sphere</b> is perfectly round. It has <b>no flat face</b>.</p><p>Every point on it is the same distance (the radius) from the center. Half a sphere is a <b>hemisphere</b>.</p>", f_sph, 50),
    L("Example", "Objects that are spheres", "<p>A basketball 🏀 and a soccer ball ⚽ are spheres.</p>", f_sph, 50),
    L("Idea", "Pyramid", "<p>A <b>pyramid</b> has a flat <b>base</b>. Its other faces are <b>triangles</b> that meet at one point, the <b>vertex</b>.</p>"
      "<p>The base can be any shape with straight edges: a triangle, a square, a trapezium, a hexagon…</p>", f_pyr, 50),
    L("Example", "Naming pyramids", "<p>The base gives the name.</p><p>Square base → <b>square pyramid</b> (4 triangle faces).<br>Triangle base → <b>triangular pyramid</b> (3 other triangle faces).</p>", f_pyr, 50),
    L("Idea", "Prism", "<p>A <b>prism</b> has 2 faces of the <b>same shape and size</b> at opposite ends.</p><p>The other faces are rectangles.</p>", f_prism, 50),
    L("Example", "A triangular prism", "<p>The 2 end faces are triangles. The 3 other faces are rectangles.</p><p>A Toblerone box is a triangular prism.</p>", f_prism, 50),
]


def obj_fig(items, label, photo=None):
    """A real object. With photo, the website shows the picture img/unit08/<photo>.jpg (made in Canva) instead of the drawing."""
    if photo:
        return {"img": f"img/unit08/{photo}.jpg", "alt": label, "label": label}
    return F(items + [txt(160, 228, label, 17)], 320, 240)


q81 = []
dl = [
    ("Do and Learn (a)", obj_fig(tri_pyramid(160, 190, 200, 170, "#90CAF9"), "a puzzle toy", "puzzle-toy"), "Triangular pyramid",
     ["Look at the base: it is a <b>triangle</b>.", "All the other faces are triangles that meet at one point (a vertex).",
      "A pyramid with a triangle base is a <b>triangular pyramid</b>."], "Its base is a triangle and its triangle faces meet at a vertex."),
    ("Do and Learn (b)", obj_fig(cylinder(160, 50, 55, 15, 140, "#FFCC80"), "a glass of juice", "glass-of-juice"), "Cylinder",
     ["The top and the bottom are flat circles: <b>2 flat faces</b>.", "The side is curved: <b>1 curved face</b>.",
      "2 flat circle faces and 1 curved face make a <b>cylinder</b>."], "A cylinder has 2 flat faces and 1 curved face."),
    ("Do and Learn (c)", obj_fig(sphere(160, 115, 85, "#E6EE9C", False) + [{"t": "ell", "c": [160, 115], "rx": 85, "ry": 40, "half": "front"}], "a tennis ball", "tennis-ball"), "Sphere",
     ["The ball is round all over.", "It has <b>no flat face</b>.", "A round solid with no flat face is a <b>sphere</b>."], "A sphere is perfectly round with no flat face."),
]
for lab, fg, ans, steps, why in dl:
    q81.append(Q(lab, 51, "Name the type of solid figure of the object below.", "Count the flat faces. Are any faces curved?", steps, ans, why, fg))

ex1 = [
    ("(a)", "sandwich", "prism", obj_fig(tri_prism(70, 80, 120, 100, 120, "#FFE082"), "sandwich", "sandwich"),
     ["The 2 ends are triangles of the same shape and size.", "The other faces are rectangles.", "So it is a <b>prism</b> (a triangular prism)."],
     "A prism has the same shape at opposite ends."),
    ("(b)", "snooker ball", "sphere", obj_fig(sphere(160, 115, 85, "#424242", False) + [{"t": "circle", "c": [160, 105], "r": 28, "fill": "#fff"}, txt(160, 116, "8", 30)], "snooker ball", "snooker-ball"),
     ["The ball is round all over.", "It has no flat face.", "So it is a <b>sphere</b>."], "A sphere has no flat faces."),
    ("(c)", "ice cream", "cone", obj_fig(cone(160, 215, 50, 60, 18, "#FFCC80", flip=True) + [{"t": "circle", "c": [160, 38], "r": 45, "fill": "#FFF8E1"}], "ice cream", "ice-cream"),
     ["The wafer has 1 circle face at the top.", "It has 1 curved face that comes to a point.", "So it is a <b>cone</b>."], "A cone has 1 flat circle face, 1 curved face and 1 vertex."),
    ("(d)", "oil drum", "cylinder", obj_fig(cylinder(160, 45, 60, 16, 145, "#7B1FA2") + [txt(160, 130, "OIL", 26, color="#fff")], "oil drum", "oil-drum"),
     ["The top and bottom are flat circles: 2 flat faces.", "The side is curved: 1 curved face.", "So it is a <b>cylinder</b>."], "2 circle faces and 1 curved face make a cylinder."),
    ("(e)", "milk tin", "cylinder", obj_fig(cylinder(160, 55, 55, 15, 130, "#CFD8DC"), "milk tin", "milk-tin"),
     ["The top and bottom are flat circles: 2 flat faces.", "The side is curved: 1 curved face.", "So it is a <b>cylinder</b>."], "2 circle faces and 1 curved face make a cylinder."),
    ("(f)", "gift box", "pyramid", obj_fig(tri_pyramid(160, 195, 220, 170, "#4FC3F7"), "gift box", "gift-box"),
     ["The box has a flat base.", "The other faces are triangles that meet at one point at the top.", "So it is a <b>pyramid</b>."], "A pyramid's triangle faces meet at a vertex."),
]
for part, obj, ans, fg, steps, why in ex1:
    q81.append(Q(f"Exercise 1 {part}", 52, f"Fill in the blank with prism, cone, cylinder, sphere or pyramid.<br>{obj}: ___",
                 "Look for flat faces, curved faces and points (vertices).", steps, ans, why, fg))

ex2 = [
    ("(a)", "Round and no face", "a sphere", F(sphere(160, 115, 80, YELLOW)), "Round with no flat face is a sphere."),
    ("(b)", "1 circular base and 1 vertex", "a cone", F(cone(160, 30, 180, 70, 20, YELLOW)), "A circle base and one point is a cone."),
    ("(c)", "1 quadrilateral base, 1 vertex and triangle faces", "a pyramid with a 4-sided base", F(square_pyramid(160, 200, 180, 170, YELLOW)),
     "A 4-sided base with triangle faces meeting at a vertex is a pyramid."),
    ("(d)", "2 circular faces and 1 curved face", "a cylinder", F(cylinder(160, 45, 65, 18, 140, YELLOW)), "2 circles and 1 curved face is a cylinder."),
    ("(e)", "2 pentagonal bases and quadrilateral faces", "a pentagonal prism", F(pent_prism(YELLOW)), "2 pentagon ends with 4-sided faces between them is a pentagonal prism."),
    ("(f)", "1 hexagonal base, 1 vertex and triangle faces", "a hexagonal pyramid", F(hex_pyramid(160, 190, 80, 170, YELLOW)), "A hexagon base with triangle faces meeting at a vertex is a hexagonal pyramid."),
]
for part, clue, ans, fg, why in ex2:
    q81.append(Q(f"Exercise 2 {part}", 53, f"Read and draw the correct figure.<br>{clue}",
                 "First name the solid from the clue. Then draw it. Dashed lines show hidden edges.",
                 [f"Read the clue: <b>{clue}</b>.", f"This is <b>{ans}</b>.",
                  "Draw it. Use dashed lines for edges you cannot see at the back."],
                 f"Draw {ans} (see the picture)", why, fg))

flash81 = [
    {"front": "Cube", "back": "6 square faces, all the same size"},
    {"front": "Cuboid", "back": "6 rectangular faces (or 4 rectangles and 2 squares)"},
    {"front": "Cone", "back": "1 flat circle face, 1 curved face, 1 vertex"},
    {"front": "Cylinder", "back": "2 flat circle faces and 1 curved face"},
    {"front": "Sphere", "back": "Perfectly round, no flat face"},
    {"front": "Pyramid", "back": "A flat base and triangle faces that meet at a vertex"},
    {"front": "Prism", "back": "2 same faces at opposite ends; other faces are rectangles"},
    {"front": "Hemisphere", "back": "Half of a sphere"},
    {"front": "Vertex", "back": "A point where edges meet"},
    {"front": "Triangular pyramid", "back": "A pyramid with a triangle base"},
]
match81 = [["Cone", "Ice cream cone"], ["Cylinder", "Oil drum"], ["Sphere", "Soccer ball"], ["Cube", "Dice"],
           ["Cuboid", "Juice carton"], ["Pyramid", "Triangle faces meet at a vertex"], ["Prism", "Same shape at both ends"],
           ["Hemisphere", "Half a sphere"]]
quiz81 = [
    {"q": "Which solid has 2 flat circle faces and 1 curved face?", "options": ["Cylinder", "Cone", "Sphere", "Prism"]},
    {"q": "Which solid has 1 flat circle face and 1 vertex?", "options": ["Cone", "Cylinder", "Pyramid", "Sphere"]},
    {"q": "Which solid has no flat face?", "options": ["Sphere", "Cone", "Cylinder", "Cube"]},
    {"q": "A soccer ball is a…", "options": ["Sphere", "Cylinder", "Cone", "Hemisphere"]},
    {"q": "A party hat is a…", "options": ["Cone", "Pyramid", "Cylinder", "Prism"]},
    {"q": "A drink can is a…", "options": ["Cylinder", "Cone", "Cuboid", "Prism"]},
    {"q": "A pyramid with a square base has how many triangle faces?", "options": ["4", "3", "5", "6"]},
    {"q": "A pyramid with a triangle base has how many faces in total?", "options": ["4", "3", "5", "6"]},
    {"q": "A prism has the same shape at…", "options": ["Both opposite ends", "Only the top", "Every face", "No faces"]},
    {"q": "A triangular prism has how many rectangle faces?", "options": ["3", "2", "5", "6"]},
    {"q": "How many faces does a cube have?", "options": ["6", "4", "8", "12"]},
    {"q": "Half a sphere is called a…", "options": ["Hemisphere", "Semicircle", "Cone", "Half cube"]},
]
check(4 + 1, 5, "square pyramid faces")  # 4 triangles + base
check(3 + 1, 4, "triangular pyramid faces")
check(3, 3, "triangular prism rectangles")
sections.append({"id": "8-1", "title": "Cones, Cylinders, Spheres and Pyramids", "short": "1. Cones, Cylinders, Spheres, Pyramids",
                 "pages": "p.48 to 53", "learn": learn81, "questions": q81, "flash": flash81, "match": match81, "quiz": quiz81})

# ==================================================================
# 8.2 NETS OF SOLIDS (p.54 to 64)
# ==================================================================
cross = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)]
check(is_cube_net(cross), True, "cross cube net")
cube_net_fig = F(cells_fig(cross, BLUE, 40, 40, 30))
other_cube_nets = [[(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)], [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)]]
for n in other_cube_nets:
    check(is_cube_net(n), True, "learn cube net")
cube_nets2 = F(cells_fig(other_cube_nets[0], ORANGE, 26, 10, 30) + cells_fig(other_cube_nets[1], GREEN, 26, 170, 30), 320, 140)

# cuboid net 4 x 2 x 1 (length 4, width 2, height 1) drawn at 30 px per unit
u = 30


def cuboid_net(x, y, L_, W, H, fill):
    """Standard cross net: strip H, W, H, W (around the length) with the 2 end faces on the strip."""
    items = [rect(x, y + H * u, L_ * u, W * u, fill), rect(x, y, L_ * u, H * u, fill), rect(x, y + (H + W) * u, L_ * u, H * u, fill),
             rect(x, y + (2 * H + W) * u, L_ * u, W * u, fill), rect(x - H * u, y + H * u, H * u, W * u, fill),
             rect(x + L_ * u, y + H * u, H * u, W * u, fill)]
    return items


cuboid_net_fig = F(cuboid_net(60, 10, 6, 2, 1, YELLOW), 320, 210)
prism_net = [poly([[60, 60], [180, 60], [180, 100], [60, 100]], GREEN), poly([[60, 100], [180, 100], [180, 140], [60, 140]], GREEN),
             poly([[60, 140], [180, 140], [180, 180], [60, 180]], GREEN), poly([[60, 100], [60, 140], [26, 120]], GREEN),
             poly([[180, 100], [180, 140], [214, 120]], GREEN)]
prism_net_fig = F(prism_net, 260, 220)
sq_pyr_net = [rect(110, 80, 70, 70, PINK), poly([[110, 80], [180, 80], [145, 20]], PINK), poly([[180, 80], [180, 150], [240, 115]], PINK),
              poly([[110, 150], [180, 150], [145, 210]], PINK), poly([[110, 80], [110, 150], [50, 115]], PINK)]
sq_pyr_net_fig = F(sq_pyr_net, 300, 230)
cyl_net_fig = F([rect(90, 70, 150, 90, PURPLE), {"t": "circle", "c": [165, 42], "r": 28, "fill": PURPLE}, {"t": "circle", "c": [165, 188], "r": 28, "fill": PURPLE}], 320, 230)
cone_net_fig = F([{"t": "circle", "c": [90, 70], "r": 40, "fill": ORANGE},
                  {"t": "seg", "p": [[150, 200], [150, 60]]}, {"t": "seg", "p": [[150, 200], [270, 140]]},
                  txt(220, 110, "curved face", 14), txt(90, 76, "base", 14)], 320, 230)
# draw the sector as a polygon approximation
import math  # noqa: E402
sector = [[150, 200]] + [[150 + 140 * math.cos(math.radians(a)), 200 - 140 * math.sin(math.radians(a))] for a in range(26, 91, 4)]
cone_net_fig["items"].insert(0, poly(sector, ORANGE))
hex_pyr_net = []
for k in range(6):
    a1, a2 = math.radians(60 * k), math.radians(60 * (k + 1))
    p1 = [160 + 50 * math.cos(a1), 120 + 50 * math.sin(a1)]
    p2 = [160 + 50 * math.cos(a2), 120 + 50 * math.sin(a2)]
    mid = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    out_ = [160 + 105 * math.cos((a1 + a2) / 2), 120 + 105 * math.sin((a1 + a2) / 2)]
    hex_pyr_net.append(poly([p1, p2, out_], BLUE))
hex_pyr_net.append(poly([[160 + 50 * math.cos(math.radians(60 * k)), 120 + 50 * math.sin(math.radians(60 * k))] for k in range(6)], BLUE))
hex_pyr_net_fig = F(hex_pyr_net, 320, 240)

learn82 = [
    L("Idea", "What is a net?", "<p>Cut along some edges of a box and open it out flat. The flat shape is a <b>net</b>.</p>"
      "<p>A <b>net</b> of a solid is a flat figure that can be folded to make the solid.</p>", cube_net_fig, 54),
    L("Example", "A net of a cube", "<p>This cross shape has <b>6 squares</b>. Fold up the sides and it makes a cube.</p>"
      "<p>Each square becomes one face of the cube.</p>", cube_net_fig, 54),
    L("Idea", "A cube has more than one net", "<p>There are 11 different nets of a cube. They all have 6 squares joined edge to edge.</p>"
      "<p>But not every shape of 6 squares works! Two squares must never land on the same face.</p>", cube_nets2, 54),
    L("Example", "Is it a cube net? Try it!", "<p>Imagine folding. Pick one square as the bottom. Fold the squares around it up.</p>"
      "<p>If 2 squares want to be the same face, it is <b>not</b> a net of a cube. A row of 4 squares with 2 squares on the <b>same side</b> never works.</p>", cube_nets2, 54),
    L("Idea", "Nets of cuboids", "<p>A cuboid net has <b>6 rectangles</b>: 3 pairs of the same size.</p><p>A cuboid also has more than one net.</p>", cuboid_net_fig, 55),
    L("Example", "Check the pairs", "<p>This net has: 2 long wide rectangles (top and bottom), 2 long thin ones (front and back), 2 small ones (the ends).</p>"
      "<p>3 matching pairs ✓. It folds into a cuboid.</p>", cuboid_net_fig, 55),
    L("Idea", "Nets of prisms", "<p>A triangular prism net has <b>2 triangles</b> and <b>3 rectangles</b>.</p>"
      "<p>The triangles go on <b>opposite sides</b> so they become the 2 ends.</p>", prism_net_fig, 55),
    L("Example", "A net of a triangular prism", "<p>3 rectangles in a strip, with 1 triangle on the left and 1 triangle on the right.</p><p>Fold the strip into a tube and close the ends.</p>", prism_net_fig, 55),
    L("Idea", "Nets of pyramids", "<p>A pyramid net has the <b>base</b> in the middle with a <b>triangle on each edge</b>.</p>"
      "<p>Fold the triangles up and they meet at the vertex.</p>", sq_pyr_net_fig, 56),
    L("Example", "A hexagonal pyramid", "<p>The base is a hexagon (6 sides), so there are <b>6 triangles</b>.</p><p>This net makes a hexagonal pyramid.</p>", hex_pyr_net_fig, 57),
    L("Idea", "Nets of cylinders and cones", "<p><b>Cylinder</b>: a rectangle (the curved face rolled flat) and 2 circles.</p>"
      "<p><b>Cone</b>: a fan shape (the curved face) and 1 circle.</p>", cyl_net_fig, 57),
    L("Example", "A net of a cone", "<p>Roll the fan shape into a party hat. Put the circle on the bottom. It is a cone!</p>", cone_net_fig, 57),
]

q82 = []
# Do and Learn 1: nets of a cuboid E, F, G, H (L=4, W=2, H=1)
u = 20
fE = cuboid_net(30, 10, 4, 2, 1, YELLOW)
fF = [rect(30, 30, 80, 40, YELLOW), rect(30, 10, 80, 20, YELLOW), rect(30, 70, 80, 20, YELLOW), rect(30, 90, 80, 40, YELLOW), rect(10, 30, 20, 40, YELLOW)]
fG = cuboid_net(30, 10, 4, 2, 1, YELLOW) + [rect(130, 10, 20, 20, YELLOW)]
fH = [rect(30, 30, 80, 40, YELLOW), rect(30, 10, 80, 20, YELLOW), rect(30, 70, 80, 20, YELLOW), rect(30, 90, 80, 40, YELLOW),
      rect(-10, 30, 40, 40, YELLOW), rect(110, 30, 40, 40, YELLOW)]
nets_cuboid = {"E": (fE, [(4, 2)] * 2 + [(4, 1)] * 2 + [(2, 1)] * 2), "F": (fF, [(4, 2)] * 2 + [(4, 1)] * 2 + [(2, 1)]),
               "G": (fG, [(4, 2)] * 2 + [(4, 1)] * 2 + [(2, 1)] * 2 + [(1, 1)]), "H": (fH, [(4, 2)] * 2 + [(4, 1)] * 2 + [(2, 2)] * 2)}
need = sorted([(4, 2)] * 2 + [(4, 1)] * 2 + [(2, 1)] * 2)
for k, (_, faces) in nets_cuboid.items():
    check(sorted(faces) == need, k == "E", f"p.60 Q1 net {k}")


def shift(items, dx, dy):
    out = []
    for it in items:
        it2 = dict(it)
        it2["p"] = [[p[0] + dx, p[1] + dy] for p in it["p"]]
        out.append(it2)
    return out


fig60a = F(shift(fE, 10, 40) + [txt(80, 30, "E", 20)] + shift(fF, 190, 40) + [txt(260, 30, "F", 20)]
           + shift(fG, 10, 230) + [txt(80, 220, "G", 20)] + shift(fH, 200, 230) + [txt(270, 220, "H", 20)]
           + cuboid(380, 120, 80, 20, 40, YELLOW) + [txt(420, 175, "cuboid", 15)], 480, 380)
q82.append(Q("Do and Learn 1", 60, "Which of the following are the nets of a cuboid?",
             "The cuboid needs 6 faces in 3 matching pairs: 2 big tops, 2 long sides, 2 small ends.",
             ["The cuboid needs: 2 big rectangles, 2 long thin rectangles and 2 small end rectangles. That is 6 faces.",
              "<b>E</b>: 6 faces, 3 matching pairs, and the ends are on opposite sides ✓",
              "<b>F</b>: only 5 faces. One end is missing ✗",
              "<b>G</b>: 7 faces. There is an extra face ✗",
              "<b>H</b>: the 2 end faces are too big. They do not fit the ends of the cuboid ✗"],
             "E", "Only E has exactly the 6 faces of the cuboid, in the right places.", fig60a))

# Do and Learn 2: nets of a prism P, Q, R, S
def tri_l(x, y):
    return poly([[x, y], [x, y + 40], [x - 34, y + 20]], BLUE)


def tri_r(x, y):
    return poly([[x, y], [x, y + 40], [x + 34, y + 20]], BLUE)


def strip(x, y, n):
    return [rect(x, y + 40 * i, 80, 40, BLUE) for i in range(n)]


netP = strip(40, 10, 3) + [tri_l(40, 50), tri_r(120, 90)]          # triangles on opposite ends ✓
netQ = strip(40, 10, 3) + [tri_l(40, 10), tri_r(120, 50)]          # ✓
netR = strip(40, 10, 3) + [tri_l(40, 10), tri_l(40, 90)]           # both triangles on the left side: they land on the same end ✗
netS = strip(40, 10, 2) + [tri_l(40, 10), tri_r(120, 50)]          # only 2 rectangles ✗
prism_nets = {"P": (3, "opposite"), "Q": (3, "opposite"), "R": (3, "same"), "S": (2, "opposite")}
for k, (rects, sides) in prism_nets.items():
    check(rects == 3 and sides == "opposite", k in ("P", "Q"), f"p.60 Q2 net {k}")
fig60b = F(shift(netP, 0, 30) + [txt(80, 20, "P", 20)] + shift(netQ, 190, 30) + [txt(270, 20, "Q", 20)]
           + shift(netR, 0, 200) + [txt(80, 190, "R", 20)] + shift(netS, 190, 200) + [txt(270, 190, "S", 20)]
           + tri_prism(390, 120, 70, 60, 90, BLUE) + [txt(440, 210, "prism", 15)], 500, 340)
q82.append(Q("Do and Learn 2", 60, "Which of the following are the nets of a prism?",
             "A triangular prism needs 3 rectangles and 2 triangles. The triangles must end up at opposite ends.",
             ["The prism needs <b>3 rectangles</b> and <b>2 triangles</b>, one triangle at each end.",
              "<b>P</b>: 3 rectangles, 1 triangle on the left and 1 on the right ✓",
              "<b>Q</b>: 3 rectangles, triangles on opposite sides ✓",
              "<b>R</b>: both triangles are on the same side. When you fold it, they cover the same end ✗",
              "<b>S</b>: only 2 rectangles. The tube cannot close ✗"],
             "P and Q", "P and Q have 3 rectangles and a triangle at each end.", fig60b))

dl3 = [
    ("(a)", sq_pyr_net_fig, "Pyramid",
     ["The net has a flat base with triangles joined to it.", "When you fold up the triangles, they meet at one point.", "So it makes a <b>pyramid</b>."]),
    ("(b)", F([{"t": "circle", "c": [100, 60], "r": 38, "fill": ORANGE}] + [poly(sector, ORANGE)], 320, 240), "Cone",
     ["The net has a fan shape and a circle.", "The fan rolls into a curved face and the circle is the base.", "So it makes a <b>cone</b>."]),
    ("(c)", cyl_net_fig, "Cylinder",
     ["The net has a rectangle and 2 circles.", "The rectangle rolls into a tube. The circles close the top and bottom.", "So it makes a <b>cylinder</b>."]),
    ("(d)", F(shift(netQ, 60, 10), 320, 160), "Prism",
     ["The net has 3 rectangles and 2 triangles.", "The rectangles make the sides and the triangles make the 2 ends.", "So it makes a <b>prism</b>."]),
]
for part, fg, ans, steps in dl3:
    q82.append(Q(f"Do and Learn 3 {part}", 60, "Fill in the type of solid based on the given net.",
                 "Look at the shapes in the net: circles, triangles, rectangles or a fan?", steps, ans,
                 "The faces in the net are the faces of the solid.", fg))

# Exercise 1 (a): cube nets
cube_choices = [
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2)],
    [(2, 0), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1)],
    [(2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2), (1, 3)],
]
key_ticks = [True, True, False, True, True, True]
cols = [ORANGE, PURPLE, BLUE, GREEN, "#9FA8DA", "#FFAB91"]
items = []
for k, cells in enumerate(cube_choices):
    check(is_cube_net(cells), key_ticks[k], f"p.61 Q1(a) net {k + 1}")
    x0 = 20 + (k % 2) * 200
    y0 = 30 + (k // 2) * 200
    items += cells_fig(cells, cols[k], 28, x0, y0) + [txt(x0 - 6, y0 - 8, str(k + 1), 18)]
fig61 = F(items, 400, 600)
q82.append(Q("Exercise 1 (a)", 61, "Tick (✓) all the nets that form the given solid.<br>(a) Cube",
             "Imagine folding each net. If 2 squares land on the same face, it is not a cube net.",
             ["Each net has 6 squares. Now check how they fold.",
              "Nets 1, 2, 4, 5 and 6: fold them in your mind. Every square becomes a different face ✓",
              "Net 3: a row of 4 squares with 2 squares <b>under the same side</b>. The 2 squares underneath fold onto the <b>same face</b>, and one face stays open ✗",
              "So tick nets <b>1, 2, 4, 5 and 6</b>."],
             "Nets 1, 2, 4, 5 and 6 (not net 3)", "Net 3 has two squares that fold onto the same face, so the cube cannot close.", fig61))

# Exercise 1 (b): triangular pyramid nets
s = 50
tri_h = s * math.sqrt(3) / 2
strip4 = [poly(eq_tri(30, 20, s), ORANGE), poly([[30 + s / 2, 20], [30 + 1.5 * s, 20], [30 + s, 20 + tri_h]], ORANGE),
          poly(eq_tri(30 + s, 20, s), ORANGE), poly([[30 + 1.5 * s, 20], [30 + 2.5 * s, 20], [30 + 2 * s, 20 + tri_h]], ORANGE)]
big = [poly([[230, 20], [330, 20], [280, 20 + 2 * tri_h]], "#FFAB91"), seg([255, 20 + tri_h], [305, 20 + tri_h]),
       seg([255, 20 + tri_h], [280, 20]), seg([305, 20 + tri_h], [280, 20])]
sqnet = shift(sq_pyr_net, -60, 170)
five = [poly(eq_tri(230, 200, s), BLUE), poly([[255, 200], [305, 200], [280, 200 + tri_h]], BLUE), poly(eq_tri(280, 200, s), BLUE),
        poly([[305, 200], [355, 200], [330, 200 + tri_h]], BLUE), poly(eq_tri(330, 200, s), BLUE)]
pyr_nets = {"1": (4, "triangles only"), "2": (4, "triangles only"), "3": (5, "has a square"), "4": (5, "triangles only")}
for k, (faces, kind) in pyr_nets.items():
    check(faces == 4 and kind == "triangles only", k in ("1", "2"), f"p.62 net {k}")
fig62 = F(strip4 + [txt(20, 15, "1", 18)] + big + [txt(220, 15, "2", 18)] + sqnet + [txt(20, 185, "3", 18)] + five + [txt(220, 190, "4", 18)]
          + shift(tri_pyramid(160, 0, 140, 110, GREEN), 300, 130), 560, 400)
q82.append(Q("Exercise 1 (b)", 62, "Tick (✓) all the nets that form the given solid.<br>(b) Pyramid (a triangular pyramid)",
             "This pyramid has 4 faces, and all 4 are triangles.",
             ["The triangular pyramid has a triangle base and 3 triangle sides: <b>4 triangles</b>.",
              "Net 1: a strip of 4 triangles ✓", "Net 2: a big triangle made of 4 triangles ✓",
              "Net 3: it has a square base. That makes a square pyramid, not this one ✗",
              "Net 4: it has 5 triangles. That is one too many ✗"],
             "Nets 1 and 2", "Only nets 1 and 2 have exactly 4 triangles.", fig62))

# Exercise 1 (c): cuboid with square ends, length 4
u = 22
net_c = [rect(50, 10, u, u, ORANGE), rect(50 + u, 10, 4 * u, u, ORANGE), rect(50 + u, 10 + u, 4 * u, u, ORANGE), rect(50 + 5 * u, 10 + u, u, u, ORANGE),
         rect(50 + 5 * u, 10 + 2 * u, u, 4 * u, ORANGE), rect(50 + 6 * u, 10 + 2 * u, u, 4 * u, ORANGE)]
net_faces = sorted([(1, 1), (1, 1), (4, 1), (4, 1), (4, 1), (4, 1)])


def faces_of(a, b, c):
    return sorted([tuple(sorted(x, reverse=True)) for x in [(a, b), (a, b), (b, c), (b, c), (a, c), (a, c)]])


choices = [("1", (1, 1, 1)), ("2", (4, 3, 1)), ("3", (1, 1, 4)), ("4", (3, 1, 4))]
for k, dims in choices:
    check(faces_of(*dims) == sorted(tuple(sorted(x, reverse=True)) for x in net_faces), k == "3", f"p.63 cuboid {k}")
fig63 = F(net_c + cuboid(20, 260, 30, 30, 20, PURPLE) + [txt(40, 330, "1", 18)] + cuboid(90, 270, 110, 25, 70, ORANGE) + [txt(140, 330, "2", 18)]
          + cuboid(240, 190, 30, 110, 20, BLUE) + [txt(255, 330, "3", 18)] + cuboid(320, 200, 30, 100, 70, GREEN) + [txt(345, 330, "4", 18)], 420, 340)
q82.append(Q("Exercise 1 (c)", 63, "Tick (✓) the solid that the given net forms.<br>(c) Cuboid",
             "Look at the faces in the net: 2 small squares and 4 long rectangles.",
             ["The net has <b>2 small squares</b> (the ends) and <b>4 long thin rectangles</b> (the sides).",
              "So the cuboid must be <b>long and thin with square ends</b>.",
              "1 is a small cube (6 squares) ✗. 2 is wide and flat ✗. 4 is tall but its ends are not squares ✗.",
              "3 is tall and thin with square ends ✓"],
             "Solid 3 (the tall, thin cuboid)", "Its faces match the net: 2 squares and 4 long rectangles.", fig63))

# Exercise 2: prism net positions a, b, c
fig64 = F([rect(110, 80, 110, 40, BLUE), rect(110, 120, 110, 40, BLUE), poly([[110, 80], [110, 120], [70, 100]], BLUE),
           poly([[220, 120], [220, 160], [260, 140]], BLUE),
           {"t": "poly", "p": [[70, 100], [110, 80], [70, 0], [30, 20]], "fill": "none"}, txt(65, 50, "a", 18),
           {"t": "poly", "p": [[220, 80], [330, 80], [330, 120], [220, 120]], "fill": "none"}, txt(280, 106, "b", 18),
           {"t": "poly", "p": [[110, 160], [220, 160], [220, 200], [110, 200]], "fill": "none"}, txt(165, 186, "c", 18)], 360, 220)
for it in fig64["items"]:
    if it.get("fill") == "none":
        it["fill"] = "#ffffff"
q82.append(Q("Exercise 2", 64, "Janice wants to make a prism from a net. What are the possible positions, a, b or c, that she should place the rectangular face to complete the net of the prism?",
             "The net needs 3 rectangles in a ring. The new rectangle must join on to make the third side of the tube.",
             ["The net has 2 rectangles and 2 triangles. A triangular prism needs <b>3 rectangles</b>.",
              "<b>c</b>: below the bottom rectangle. The 3 rectangles make a strip that folds into a tube ✓",
              "<b>a</b>: joined to the slanted side of the left triangle. It folds round to become the third side ✓",
              "<b>b</b>: next to the top rectangle on the right. It would stick out past the end and cover the triangle's place ✗"],
             "a or c", "Positions a and c both make the 3 rectangles join edge to edge around the triangles.", fig64))

# Exercise 3: complete cube nets on a 7 x 7 grid
blue = [(3, 1), (3, 2), (3, 3), (3, 4)]
ex3 = [("(a)", [(2, 1), (4, 1)]), ("(b)", [(2, 1), (4, 2)]), ("(c)", [(2, 1), (4, 3)]), ("(d)", [(2, 1), (4, 4)])]
for part, pink in ex3:
    check(is_cube_net(blue + pink), True, f"p.64 Q3 {part}")
    fg = F([{"t": "grid", "x": 20, "y": 20, "cols": 7, "rows": 7, "size": 26}] + cells_fig(blue, BLUE, 26, 20, 20) + cells_fig(pink, "#F48FB1", 26, 20, 20), 230, 230)
    q82.append(Q(f"Exercise 3 {part}", 64, "Color 2 more squares in the grid to complete a net of a cube. (The blue squares are given.)",
                 "A column of 4 squares makes the 4 sides around the cube. You need a top and a bottom.",
                 ["The 4 blue squares in a column fold round into a ring: front, top, back, bottom.",
                  "You still need the 2 side faces: <b>one square on the left</b> of the column and <b>one on the right</b>.",
                  "They can be next to any of the 4 blue squares, one on each side.",
                  "The pink squares show the answer in the key. Fold it in your mind: all 6 faces are different ✓"],
                 "See the pink squares in the picture", "One square on each side of the column of 4 always makes a cube net.", fg))

flash82 = [
    {"front": "Net", "back": "A flat figure that folds to make a solid"},
    {"front": "Net of a cube", "back": "6 squares joined edge to edge"},
    {"front": "How many different nets does a cube have?", "back": "11"},
    {"front": "Net of a cuboid", "back": "6 rectangles in 3 matching pairs"},
    {"front": "Net of a triangular prism", "back": "3 rectangles and 2 triangles"},
    {"front": "Net of a square pyramid", "back": "1 square and 4 triangles"},
    {"front": "Net of a triangular pyramid", "back": "4 triangles"},
    {"front": "Net of a cylinder", "back": "1 rectangle and 2 circles"},
    {"front": "Net of a cone", "back": "1 fan shape (sector) and 1 circle"},
    {"front": "Net of a hexagonal pyramid", "back": "1 hexagon and 6 triangles"},
]
match82 = [["Cube", "6 squares"], ["Cylinder", "Rectangle + 2 circles"], ["Cone", "Fan shape + circle"],
           ["Square pyramid", "Square + 4 triangles"], ["Triangular prism", "3 rectangles + 2 triangles"],
           ["Triangular pyramid", "4 triangles"], ["Cuboid", "3 pairs of rectangles"], ["Hexagonal pyramid", "Hexagon + 6 triangles"]]
quiz82 = [
    {"q": "A net with 1 rectangle and 2 circles makes a…", "options": ["Cylinder", "Cone", "Prism", "Sphere"]},
    {"q": "A net with a fan shape and 1 circle makes a…", "options": ["Cone", "Cylinder", "Pyramid", "Sphere"]},
    {"q": "A net with 1 square and 4 triangles makes a…", "options": ["Square pyramid", "Cube", "Triangular prism", "Cone"]},
    {"q": "A net with 3 rectangles and 2 triangles makes a…", "options": ["Triangular prism", "Triangular pyramid", "Cuboid", "Square pyramid"]},
    {"q": "How many squares are in a net of a cube?", "options": ["6", "4", "8", "12"]},
    {"q": "How many triangles are in a net of a triangular pyramid?", "options": ["4", "3", "5", "6"]},
    {"q": "A row of 4 squares with 2 squares on the same side. Is it a cube net?", "options": ["No, 2 squares land on the same face", "Yes", "Only if they are big", "Yes, any 6 squares work"]},
    {"q": "A net of a hexagonal pyramid has how many triangles?", "options": ["6", "5", "7", "12"]},
    {"q": "How many different nets does a cube have?", "options": ["11", "6", "1", "24"]},
    {"q": "A cuboid net has 6 rectangles in…", "options": ["3 matching pairs", "2 matching groups of 3", "6 different sizes", "1 size only"]},
    {"q": "Which shape can NOT be part of a cylinder's net?", "options": ["Triangle", "Rectangle", "Circle", "None of these"]},
]
sections.append({"id": "8-2", "title": "Nets of Solids", "short": "2. Nets of Solids", "pages": "p.54 to 64",
                 "learn": learn82, "questions": q82, "flash": flash82, "match": match82, "quiz": quiz82})

# ==================================================================
# UNIT 8 CHALLENGE (p.65 to 70)
# ==================================================================
def prism_fve(n):
    return n + 2, 2 * n, 3 * n


def pyramid_fve(n):
    return n + 1, n + 1, 2 * n


rows = [("cube", (6, 8, 12), prism_fve(4)), ("cuboid", (6, 8, 12), prism_fve(4)), ("prism", (5, 6, 9), prism_fve(3)), ("pyramid", (5, 5, 8), pyramid_fve(4))]
for name, key, calc in rows:
    check(calc == key, True, f"p.65 {name} F, V, E")
    check(key[0] + key[1] - key[2], 2, f"p.65 {name} F + V - E")
check((26 - 10 - 10) / 2, 3, "p.68 shortest side")
check(12 * 10 * 3, 360, "p.68 volume")
check(360 / 3 / 10, 12, "p.68 check")

fig65 = F(cuboid(20, 70, 70, 70, 40, BLUE) + cuboid(130, 90, 100, 50, 40, GREEN) + tri_prism(270, 70, 70, 70, 60, ORANGE)
          + shift(square_pyramid(0, 0, 100, 110, PINK), 440, 150), 520, 180)
pts_ps = []
s10, s3, s12 = 10 * 8, 3 * 8, 12 * 8
x0, y0 = 30, 40
fig67 = F([rect(x0, y0 + s3, s10, s12, BLUE), rect(x0, y0, s10, s3, BLUE), rect(x0 + s10, y0 + s3, s3, s12, BLUE),
           rect(x0 + s10 + s3, y0 + s3, s10, s12, BLUE), rect(x0 + 2 * s10 + s3, y0 + s3, s3, s12, BLUE),
           rect(x0 + s10 + s3, y0 + s3 + s12, s10, s3, BLUE),
           txt(x0 + s10 / 2, y0 - 8, "10 cm", 15, color="#1565c0"), txt(x0 - 26, y0 + s3 + s12 / 2 + 5, "12 cm", 15, color="#1565c0"),
           seg([x0, y0 + s3 + s12 + s3 + 18], [x0 + 2 * s10 + 2 * s3, y0 + s3 + s12 + s3 + 18], width=1.5),
           txt(x0 + s10 + s3, y0 + s3 + s12 + s3 + 38, "26 cm", 15, color="#1565c0")], 300, 240)
fig69 = F(square_pyramid(110, 200, 160, 180, PINK) + [seg([62, 120], [150, 120], True, 1.5), seg([62, 120], [101, 103], True, 1.5),
                                                     seg([101, 103], [145, 104])], 320, 230)
qch = [
    Q("Let's Think Along", 65,
      "Find the number of faces (F), vertices (V) and edges (E) of a cube, a cuboid, a prism and a pyramid. "
      "Then find F + V - E for each one. What do you notice?",
      "Count carefully. Mark each face, vertex or edge as you count it.",
      ["<b>Cube</b>: F = 6, V = 8, E = 12. 6 + 8 - 12 = <b>2</b>",
       "<b>Cuboid</b>: F = 6, V = 8, E = 12. 6 + 8 - 12 = <b>2</b>",
       "<b>Triangular prism</b>: F = 5 (2 triangles + 3 rectangles), V = 6, E = 9. 5 + 6 - 9 = <b>2</b>",
       "<b>Square pyramid</b>: F = 5 (1 square + 4 triangles), V = 5, E = 8. 5 + 5 - 8 = <b>2</b>",
       "Every answer is 2!"],
      "F + V - E = 2 for all of them", "For these solids, faces + vertices - edges always equals 2.", fig65),
    Q("Problem Solving", 67, "The figure shows a net of a cuboid. Find the volume of the cuboid.",
      "The 26 cm is made of 4 sides: 10 cm, the short side, 10 cm, the short side.",
      ["<b>Understand:</b> The net is a cuboid. We know 10 cm, 12 cm and 26 cm. We must find the volume.",
       "Along the 26 cm there are 4 faces: 10 cm + short + 10 cm + short.",
       "Short side + short side = 26 - 10 - 10 = 6 cm",
       "Short side = 6 ÷ 2 = <b>3 cm</b>",
       "Volume of cuboid = Length × Width × Height = 12 × 10 × 3",
       "12 × 10 = 120, 120 × 3 = <b>360 cm³</b>",
       "<b>Check:</b> work backward. 360 ÷ 3 = 120 and 120 ÷ 10 = 12 ✓"],
      "360 cm³", "The cuboid is 12 cm by 10 cm by 3 cm, and 12 × 10 × 3 = 360.", fig67),
    Q("Math Journal", 69,
      "If Su Ling were to cut a pyramid into 2 pieces as shown below, would she get a pyramid and a prism? Give your reasons.",
      "A prism has 2 end faces that are the same shape AND size. Look at the bottom piece.",
      ["The top piece has a flat base and triangle faces that meet at a vertex. It <b>is a pyramid</b>.",
       "The bottom piece has a small square on top and a big square at the bottom. They are <b>not the same size</b>.",
       "Its side faces are not rectangles or parallelograms (they are trapeziums).",
       "So the bottom piece is <b>not a prism</b>."],
      "She would get a pyramid, but not a prism.",
      "A prism needs identical faces at opposite ends and rectangle (or parallelogram) sides. The bottom piece has neither.", fig69),
]
sections.append({"id": "8-ch", "title": "Unit 8 Challenge", "short": "⭐ Challenge", "pages": "p.65 to 70",
                 "learn": [
                     L("Idea", "Unit 8 big ideas", "<p><b>Cone</b>: 1 circle + 1 curved face. <b>Cylinder</b>: 2 circles + 1 curved face. "
                       "<b>Sphere</b>: no flat face.</p><p><b>Pyramid</b>: base + triangles meeting at a vertex. <b>Prism</b>: same shape at both ends.</p>", None, 70),
                     L("Idea", "Faces, vertices and edges", "<p><b>Face</b>: a flat surface. <b>Edge</b>: where 2 faces meet. <b>Vertex</b>: a corner point.</p>"
                       "<p>For these solids: <b>F + V - E = 2</b>.</p>", fig65, 65),
                     L("Example", "Volume of a cuboid (from Unit 12 ideas)", "<p>Volume = Length × Width × Height.</p><p>A 2 cm by 3 cm by 4 cm box: 2 × 3 × 4 = <b>24 cm³</b>.</p>", None, 68),
                 ],
                 "questions": qch, "flash": flash81[:6] + flash82[:6],
                 "match": [["Cube F + V - E", "6 + 8 - 12 = 2"], ["Square pyramid faces", "5"], ["Prism edges (triangle ends)", "9"],
                           ["Cuboid vertices", "8"], ["Net of a cone", "Fan + circle"], ["Net of a cylinder", "Rectangle + 2 circles"],
                           ["Pyramid", "Triangles meet at a vertex"], ["Prism", "Same ends"]],
                 "quiz": quiz81[:5] + quiz82[:5] + [
                     {"q": "A cube has 6 faces and 8 vertices. How many edges?", "options": ["12", "14", "8", "6"]},
                     {"q": "A cuboid is 12 cm by 10 cm by 3 cm. What is its volume?", "options": ["360 cm³", "25 cm³", "120 cm³", "36 cm³"]}]})
check(2 * 3 * 4, 24, "challenge example")
check(6 + 8 - 2, 12, "quiz edges")

unit = {"unit": "08", "title": "3D Shapes", "pages": "p.47 to 70", "sections": sections,
        "expectedPages": {"8-1": [51, 52, 53], "8-2": [60, 61, 62, 63, 64], "8-ch": [65, 67, 69]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written. Add these to content/CHECK-ME.md:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit08.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(unit, fh, ensure_ascii=False, separators=(",", ":"))
n = sum(len(s["questions"]) for s in sections)
print(f"OK: all checks passed. Wrote content/unit08.json ({n} guided questions, {len(sections)} sections).")
