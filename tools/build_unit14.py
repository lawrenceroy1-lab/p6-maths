"""Builds content/unit14.json for Unit 14: Presentation of Data (book pages 231 to 244).

Every answer is worked out here and compared with the answer key using check().
The pie charts are drawn by code straight from the numbers, so each slice is exactly the
right size (slice angle = part ÷ total × 360°).
Run:  python3 tools/build_unit14.py
"""
import contextlib
import io
import json
import math
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from geo import check as _check, PROBLEMS  # noqa: E402


def check(value, expected, where):
    if isinstance(expected, list):
        if len(value) != len(expected):
            PROBLEMS.append(f"{where}: calculated {value}, answer key says {expected}")
        for i, (a, b) in enumerate(zip(value, expected)):
            _check(a, b, f"{where} [{i + 1}]")
        return value
    if isinstance(expected, Fr):
        if Fr(value) != expected:
            PROBLEMS.append(f"{where}: calculated {value}, answer key says {expected}")
        return value
    return _check(value, expected, where)


with contextlib.redirect_stdout(io.StringIO()):
    from build_unit09 import num, Q, L  # noqa: E402

YEL, GRN, BLU, RED, PUR, ORA, PNK, TEAL = ("#FFF59D", "#C8E6C9", "#BBDEFB", "#FFCDD2",
                                          "#D1C4E9", "#FFE0B2", "#F8BBD0", "#B2EBF2")
INK = "#1f2a44"


def fr(f):
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def t(x, y, s, size=14, color=INK):
    return {"t": "txt", "at": [round(x, 1), round(y, 1)], "s": s, "size": size, "bold": True, "color": color}


def pie(slices, r=92, cx=None, cy=None, start=-90, ra=(), w=None, h=None, title=None, x_off=0):
    """slices: list of (label lines, value, fill). Slices go clockwise from 12 o'clock.
    ra: indexes of slices that get a right-angle mark (they must be exactly 90°)."""
    total = sum(v for _, v, _ in slices)
    cx = cx if cx is not None else r + 30 + x_off
    top = 34 if title else 18
    cy = cy if cy is not None else r + top
    items, a = [], start
    if title:
        items.append(t(cx, 20, title, 15, "#0D2B6B"))
    angles = []
    for lines, v, fill in slices:
        sweep = Fr(v) / Fr(total) * 360
        a1 = a + float(sweep)
        items.append({"t": "sector", "c": [cx, cy], "r": r, "a0": round(a, 3), "a1": round(a1, 3), "fill": fill})
        angles.append((a, a1, float(sweep)))
        a = a1
    for i in ra:
        a0, a1, sw = angles[i]
        if abs(sw - 90) > 1e-9:
            PROBLEMS.append(f"pie: right-angle mark on a slice of {sw}°")
        p = lambda d: [cx + 40 * math.cos(math.radians(d)), cy + 40 * math.sin(math.radians(d))]
        items.append({"t": "ra", "v": [cx, cy], "a": p(a0), "b": p(a1), "size": 11})
    for (lines, v, fill), (a0, a1, sw) in zip(slices, angles):
        mid = math.radians((a0 + a1) / 2)
        lines = [lines] if isinstance(lines, str) else lines
        rr = r * (0.6 if sw >= 34 + 12 * (len(lines) - 1) else 1.3)
        x, y = cx + rr * math.cos(mid), cy + rr * math.sin(mid)
        n = len(lines)
        for k, s in enumerate(lines):
            items.append(t(x, y + 5 + (k - (n - 1) / 2) * 16, s, 13 if n > 2 else 14))
    return {"w": w or 2 * cx, "h": h or cy + r + 22, "pts": {}, "items": items}


def bars(names, values, title, ymax, w=330, h=230, ylab=None, numbers=True, fills=None):
    """A simple bar graph drawn with polygons (bars) and lines (axes)."""
    x0, y0, top = 58, h - 40, 40
    plot_h = y0 - top
    items = [t(w / 2 + 20, 20, title, 14, "#0D2B6B")]
    step = ymax // 5 if ymax >= 5 else 1
    for v in range(0, ymax + 1, step):
        y = y0 - plot_h * v / ymax
        items.append({"t": "seg", "p": [[x0, y], [w - 8, y]], "color": "#cfd8dc", "width": 1})
        if numbers:
            items.append({"t": "txt", "at": [x0 - 8, y + 5], "s": str(v), "size": 12, "bold": True, "color": "#37474f", "anchor": "end"})
    bw = (w - x0 - 20) / len(names)
    for i, (n, v) in enumerate(zip(names, values)):
        x = x0 + 10 + i * bw
        y = y0 - plot_h * v / ymax
        fill = fills[i] if fills else BLU
        items.append({"t": "poly", "p": [[x + 6, y0], [x + 6, y], [x + bw - 6, y], [x + bw - 6, y0]], "fill": fill})
        items.append(t(x + bw / 2, y0 + 18, n, 11 if bw < 70 else 12, "#37474f"))
    items.append({"t": "seg", "p": [[x0, top - 6], [x0, y0]], "width": 2.5})
    items.append({"t": "seg", "p": [[x0, y0], [w - 8, y0]], "width": 2.5})
    if ylab:
        items.append(t(x0 + 6, top - 14, ylab, 12, "#37474f"))
    return {"w": w, "h": h, "pts": {}, "items": items}


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="t"><tr>{h}</tr>{b}</table>'


def htable(rows):
    """Table with the first column as headings (like the book's sideways tables)."""
    return '<table class="t">' + "".join(
        "<tr><th>" + r[0] + "</th>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows) + "</table>"


# =====================================================================
# 14.1 READING PIE CHARTS (p.231 to 238)
# =====================================================================
# p.231 favourite pets
pets = {"Hamster": 10, "Dog": 40, "Rabbit": 15, "Cat": 20}
fig_pets_bar = bars(["Hamster", "Dog", "Rabbit", "Cat"], [10, 40, 15, 20], "Favorite pets of students", 50,
                    ylab="Students", fills=[ORA, BLU, PNK, YEL])
fig_pets_pie = pie([("Cat", 20, YEL), ("Rabbit", 15, PNK), ("Hamster", 10, ORA), ("Dog", 40, BLU)])

# p.232 T-shirts and tarts
fig_shirts = pie([("Yellow", 15, YEL), ("Green", 15, GRN), ("Blue", 10, BLU)])
check(Fr(1, 4) + Fr(1, 4) + Fr(1, 2), Fr(1), "p.232 tarts")
fig_tarts = pie([(["Strawberry", "tarts", "1/4"], 1, PNK), (["Chocolate", "tarts", "1/4"], 1, ORA),
                 (["Pineapple", "tarts", "1/2"], 2, YEL)], ra=(0, 1))

# p.233 Janice and the concert
check(100 - 40 - 20, 40, "p.233 Janice savings %")
fig_janice = pie([(["Food and", "drinks 40%"], 40, ORA), (["Transport", "20%"], 20, BLU), (["Savings", "40%"], 40, GRN)])
concert = [("Adults", 60), ("Boys", 40), ("Girls", 60)]
ctot = check(sum(v for _, v in concert), 160, "p.233 concert total")
cfr = [Fr(v, ctot) for _, v in concert]
check(cfr, [Fr(3, 8), Fr(1, 4), Fr(3, 8)], "p.233 concert fractions")
cpc = [v / ctot * 100 for _, v in concert]
check(cpc, [37.5, 25, 37.5], "p.233 concert percentages")
fig_concert_n = pie([(["Adults", "60"], 60, PUR), (["Boys", "40"], 40, BLU), (["Girls", "60"], 60, PNK)])
fig_concert_f = pie([(["Adults", "3/8"], 60, PUR), (["Boys", "1/4"], 40, BLU), (["Girls", "3/8"], 60, PNK)])
fig_concert_p = pie([(["Adults", "37.5%"], 60, PUR), (["Boys", "25%"], 40, BLU), (["Girls", "37.5%"], 60, PNK)])

# p.234 burgers
cheese = check(750, 750, "p.234 (a)")
burg_total = check(750 * 4, 3000, "p.234 (b)")
check(Fr(1) - Fr(1, 4) - Fr(1, 4), Fr(1, 2), "p.234 (c) fraction")
cf = check(750 * 2, 1500, "p.234 (c)")
fish = check(cf // 3, 500, "p.234 (d)")
chicken = 2 * fish
fig_burger = pie([(["Chicken", "burgers"], chicken, PUR), (["Fish", "burgers"], fish, BLU),
                  (["Cheese", "burgers"], 750, ORA), (["Beef", "burgers", "750 baht"], 750, YEL)], ra=(2, 3))

# p.235 theater (Do and Learn)
th = {"Men": 60, "Women": 45, "Boys": 55}
th_total = check(45 * 4, 180, "p.235 (b)")
girls = check(th_total - 60 - 45 - 55, 20, "p.235 (c)")
check(60 - 45, 15, "p.235 (a)")
fig_theater = pie([(["Men", "60"], 60, YEL), (["Women", "45"], 45, BLU), (["Boys", "55"], 55, GRN), ("Girls", girls, ORA)],
                  start=-90 + 0, ra=(1,))
# Women is a quarter: 45 is 1/4 of 180, so the slice is exactly 90°.
fig_hobby = pie([(["Computer", "games"], 10, BLU), ("TV", 8, GRN), ("Read", 15, ORA), (["Ball", "games"], 7, YEL)])

# p.236 Exercise 1: four pie charts, C and D are right
col = {"Blue": 10, "Green": 15, "Red": 10, "Yellow": 5}
ctotal = sum(col.values())
check([Fr(col[c], ctotal) for c in ["Blue", "Red", "Green", "Yellow"]], [Fr(1, 4), Fr(1, 4), Fr(3, 8), Fr(1, 8)], "p.236 fractions")
pA = pie([(["Blue", "10"], 1, BLU), (["Red", "10"], 1, RED), (["Yellow", "5"], 1.5, YEL), (["Green", "15"], 0.5, GRN)], r=70, title="A", start=-60)
pB = pie([(["Blue", "10"], 2, BLU), (["Yellow", "5"], 0.6, YEL), (["Red", "10"], 0.7, RED), (["Green", "15"], 0.7, GRN)], r=70, title="B")
pC = pie([(["Green", "15"], 15, GRN), (["Yellow", "5"], 5, YEL), (["Red", "10"], 10, RED), (["Blue", "10"], 10, BLU)], r=70, title="C")
pD = pie([(["Red", "1/4"], 10, RED), (["Yellow", "1/8"], 5, YEL), (["Green", "3/8"], 15, GRN), (["Blue", "1/4"], 10, BLU)], r=70, title="D")


def row_figs(figs, gap=10, per_row=2):
    items, x, y, h, wmax = [], 0, 0, 0, 0
    for n, f in enumerate(figs):
        if n and n % per_row == 0:
            x, y = 0, y + h + gap

        for it in f["items"]:
            it = json.loads(json.dumps(it))
            if it["t"] == "sector":
                it["c"] = [it["c"][0] + x, it["c"][1] + y]
            elif it["t"] == "txt":
                it["at"] = [it["at"][0] + x, it["at"][1] + y]
            elif it["t"] == "ra":
                for k in ("v", "a", "b"):
                    it[k] = [it[k][0] + x, it[k][1] + y]
            items.append(it)
        x += f["w"] + gap
        wmax = max(wmax, x - gap)
        h = max(h, f["h"])
    return {"w": wmax, "h": y + h, "pts": {}, "items": items}


fig_ex1 = row_figs([pA, pB, pC, pD])

# p.237 Exercise 2 chess club
p6 = 28
check(p6, 28, "p.237 Ex2 (a)")
p4 = check(p6, 28, "p.237 Ex2 (b)")
p5 = check(p4 + p6, 56, "p.237 Ex2 (c)")
fig_chess = pie([("Primary 5", p5, BLU), (["Primary 6", "28"], p6, RED), ("Primary 4", p4, YEL)], ra=(1, 2))

# p.237 Exercise 3 fish: guppies + swordfish make half; angelfish + goldfish make the other half
sword, angel, gold = 16, 30, 20
check(sword, 16, "p.237 Ex3 (a)")
check(angel - gold, 10, "p.237 Ex3 (b)")
half = angel + gold
guppies = check(half - sword, 34, "p.237 Ex3 (c)")
fish_total = 2 * half
check(Fr(guppies, fish_total), Fr(17, 50), "p.237 Ex3 (d)")
fig_fish = pie([(["Swordfish", "16"], sword, RED), (["Angelfish", "30"], angel, YEL), (["Goldfish", "20"], gold, GRN),
                ("Guppies", guppies, BLU)], start=-88)

# p.238 Exercise 4 buttons
blue_pc, green_pc = 10, 40
red_pc = check(2 * blue_pc, 20, "p.238 Ex4 (a)")
yellow_pc = check(100 - red_pc - (blue_pc + green_pc), 30, "p.238 Ex4 (b)")
btn_total = check(100 * 100 // (blue_pc + green_pc), 200, "p.238 Ex4 (c)")
blue_n = check(blue_pc * btn_total // 100, 20, "p.238 Ex4 (d)")
g = math.gcd(green_pc, yellow_pc)
check([green_pc // g, yellow_pc // g], [4, 3], "p.238 Ex4 (e)")
check(Fr(3, 5) * 100, 60, "p.238 Ex4 (f) 3/5 as %")
check(red_pc + green_pc, 60, "p.238 Ex4 (f)")
fig_buttons = pie([(["Blue", "buttons", "10%"], 10, BLU), (["Green buttons", "40%"], 40, GRN), (["Yellow", "buttons"], 30, YEL),
                   (["Red", "buttons"], 20, RED)])

# ---------------- Learn cards ----------------
learn141 = [
    L("Idea", "Many ways to show data",
      "<p>We can show the same data in different ways:</p><p>📋 a <b>table</b> &nbsp; 📊 a <b>bar graph</b> &nbsp; 🥧 a <b>pie chart</b></p>"
      "<p>A pie chart is also called a <b>circle graph</b>.</p>"
      + table(["Favorite pet", "Cat", "Rabbit", "Hamster", "Dog"], [["Number of students", "20", "15", "10", "40"]]),
      fig_pets_bar, 231),
    L("Example", "The same pets in a pie chart",
      "<p>Here is the same pet data as a pie chart.</p><p>The <b>biggest slice</b> is Dog (40). The <b>smallest slice</b> is Hamster (10).</p>"
      "<p>More students = a bigger slice.</p>", fig_pets_pie, 231),
    L("Idea", "What is a pie chart?",
      "<p>A <b>pie chart</b> is a circle cut into slices, like a pizza 🍕.</p><p>The whole circle is <b>all</b> the data.</p>"
      "<p>Each slice (a <b>sector</b>) is one group. A bigger amount gets a bigger slice.</p>", None, 232),
    L("Example", "Class 6F T-shirts",
      table(["Color of T-shirt", "Yellow", "Green", "Blue"], [["Number of students", "15", "15", "10"]])
      + "<p>Yellow and Green both have <b>15</b>, so their slices are the <b>same size</b>.</p><p>Blue has only 10, so its slice is smaller.</p>",
      fig_shirts, 232),
    L("Example", "Tarts: pie charts with fractions",
      "<p>1/4 of the tarts are strawberry, 1/4 are chocolate and 1/2 are pineapple.</p>"
      "<p>The whole circle is <b>1 whole</b>, so all the fractions add up to 1:</p><p><b>1/4 + 1/4 + 1/2 = 1</b></p>"
      "<p>The little square means a <b>quarter</b> of the circle (1/4).</p>", fig_tarts, 232),
    L("Example", "Janice: pie charts with percentages",
      "<p>Janice spent 40% of her pocket money on food and drinks and 20% on transport. She saved the rest.</p>"
      "<p>The whole circle is <b>100%</b>.</p><p>Savings = 100% - 40% - 20% = <b>40%</b></p>", fig_janice, 233),
    L("Idea", "Numbers, fractions or percentages",
      "<p>The same data can use numbers, fractions or percentages.</p>"
      + table(["", "Adults", "Boys", "Girls", "Total"],
              [["Number", "60", "40", "60", "160"], ["Fraction", "60/160 = 3/8", "40/160 = 1/4", "60/160 = 3/8", "1"],
               ["Percentage", "37.5%", "25%", "37.5%", "100%"]])
      + "<p>Fraction = part ÷ total. Percentage = fraction × 100%.</p>", fig_concert_p, 233),
    L("Example", "Burgers (a) and (b)",
      "<p>Beef burgers is a <b>quarter</b> (1/4) of the circle and made 750 baht. Cheese burgers is also a quarter, so it made <b>750 baht</b>.</p>"
      "<p>4 quarters make the whole circle:</p><p>750 baht × 4 = <b>3,000 baht</b> in total.</p>", fig_burger, 234),
    L("Example", "Burgers (c) and (d)",
      "<p>Chicken + fish = 1 - 1/4 - 1/4 = <b>1/2</b> of the circle.</p><p>1/2 is 2 quarters: 750 baht × 2 = <b>1,500 baht</b>.</p>"
      "<p>Chicken is twice fish. Fish = 1 unit, chicken = 2 units, so 3 units = 1,500 baht.</p>"
      "<p>Fish: 1,500 baht ÷ 3 = <b>500 baht</b>. Chicken: 500 × 2 = <b>1,000 baht</b>.</p>", None, 234),
    L("Idea", "Hands-On: make your own pie chart",
      "<p>Ask your classmates a question, like <b>“What is your favorite hobby?”</b></p>"
      + table(["Favorite pastime", "Number"], [["Play computer games", "10"], ["Watch TV", "8"], ["Read", "15"], ["Play ball games", "7"]])
      + "<p>Type the table into a spreadsheet and make a pie chart. Then ask friends what it shows.</p>", fig_hobby, 235),
]

# ---------------- Guided questions ----------------
TH_Q = "The pie chart shows the number of people in a theater on a weekend."
q141 = [
    Q("Do and Learn (a)", 235, TH_Q + " (a) How many more men than women were there?",
      "Find Men and Women on the pie chart. Take away the smaller number.",
      ["Men: <b>60</b> people.", "Women: <b>45</b> people.", "More men than women: 60 - 45 = <b>15</b>"],
      "There were 15 more men than women.", "60 - 45 = 15.", fig_theater),
    Q("Do and Learn (b)", 235, TH_Q + " (b) How many people were in the theater?",
      "Look at the little square on the Women slice. What part of the circle is it?",
      ["The little square shows a right angle, so the Women slice is a <b>quarter</b> (1/4) of the circle.",
       "1 quarter = 45 people.", "The whole circle is 4 quarters.", "4 quarters = 45 × 4 = <b>180</b>"],
      "There were 180 people in the theater.", "Women is 1/4 of the circle, so the total is 45 × 4 = 180.", fig_theater),
    Q("Do and Learn (c)", 235, TH_Q + " (c) How many girls were there?",
      "Total people take away men, women and boys.",
      ["Total: <b>180</b> people (from part (b)).", "Men + Women + Boys = 60 + 45 + 55 = <b>160</b>", "Girls = 180 - 160 = <b>20</b>"],
      "There were 20 girls.", "180 - 60 - 45 - 55 = 20.", fig_theater),
    Q("Exercise 1", 236,
      "The table shows the favorite colors of students in Class 6D."
      + table(["Color", "Blue", "Green", "Red", "Yellow"], [["Number of students", "10", "15", "10", "5"]])
      + "Tick ( ✓ ) the pie chart that shows the information in the table correctly.",
      "Find the total. Then work out what fraction of the circle each color should be.",
      ["Total: 10 + 15 + 10 + 5 = <b>40</b> students.",
       "Blue: 10/40 = <b>1/4</b>. Red: 10/40 = <b>1/4</b>.", "Green: 15/40 = <b>3/8</b>. Yellow: 5/40 = <b>1/8</b>.",
       "So Green must be the <b>biggest</b> slice and Yellow the <b>smallest</b>. Blue and Red are each a quarter.",
       "Chart A: Yellow (5) is bigger than Green (15). Wrong ✗",
       "Chart B: Blue (10) is half of the circle. Wrong ✗",
       "Chart C: Blue and Red are quarters, Green is biggest, Yellow is smallest. Right ✓",
       "Chart D: 1/4, 1/4, 3/8 and 1/8. These are the right fractions. Right ✓"],
      "Charts C and D are correct. ✓", "Blue and Red are 1/4 each, Green is 3/8 and Yellow is 1/8. Only C and D show this.", fig_ex1),
]
CH = "The pie chart shows the different levels of students from Primary 4 to Primary 6 who join the Chess Club in a school."
q141 += [
    Q("Exercise 2 (a)", 237, CH + " (a) ___ Primary 6 students join the Chess Club.",
      "Read the number written in the Primary 6 slice.",
      ["Find the Primary 6 slice.", "The number written on it is <b>28</b>."],
      "28 Primary 6 students join the Chess Club.", "The pie chart shows 28 for Primary 6.", fig_chess),
    Q("Exercise 2 (b)", 237, CH + " (b) ___ Primary 4 students join the Chess Club.",
      "Primary 4 and Primary 6 both have a little square. What does that tell you?",
      ["Primary 6 and Primary 4 both have a right-angle mark, so each one is a <b>quarter</b> of the circle.",
       "Same size slice = same number.", "Primary 4 = Primary 6 = <b>28</b>"],
      "28 Primary 4 students join the Chess Club.", "Both slices are quarters, so they are equal: 28.", fig_chess),
    Q("Exercise 2 (c)", 237, CH + " (c) ___ Primary 5 students join the Chess Club.",
      "Primary 5 is half of the circle. Half = 2 quarters.",
      ["Primary 4 + Primary 6 = 2 quarters = half of the circle.", "Primary 5 is the other half.",
       "Primary 5 = 28 + 28 = <b>56</b>"],
      "56 Primary 5 students join the Chess Club.", "Half the circle is 2 quarters: 28 + 28 = 56.", fig_chess),
]
FI = "The pie chart shows the number of different types of fish in an aquarium."
q141 += [
    Q("Exercise 3 (a)", 237, FI + " (a) How many swordfish are there?", "Read the number on the Swordfish slice.",
      ["Find the Swordfish slice.", "The number on it is <b>16</b>."], "There are 16 swordfish.", "The chart shows 16 swordfish.", fig_fish),
    Q("Exercise 3 (b)", 237, FI + " (b) How many more angelfish than goldfish are there in the aquarium?",
      "Angelfish take away goldfish.",
      ["Angelfish: <b>30</b>.", "Goldfish: <b>20</b>.", "30 - 20 = <b>10</b>"],
      "There are 10 more angelfish than goldfish.", "30 - 20 = 10.", fig_fish),
    Q("Exercise 3 (c)", 237, FI + " (c) How many guppies are there?",
      "The straight line cuts the circle into 2 halves. Angelfish and goldfish make one half.",
      ["The straight line through the middle makes two <b>halves</b>.",
       "One half: Angelfish + Goldfish = 30 + 20 = <b>50</b>",
       "The other half (Guppies + Swordfish) is also <b>50</b>.", "Guppies = 50 - 16 = <b>34</b>"],
      "There are 34 guppies.", "Each half is 30 + 20 = 50, so guppies = 50 - 16 = 34.", fig_fish),
    Q("Exercise 3 (d)", 237, FI + " (d) What fraction of the fish are guppies?",
      "Fraction = guppies ÷ all the fish. Two halves of 50 make the whole.",
      ["All the fish: 50 + 50 = <b>100</b>", "Guppies: <b>34</b>", "Fraction = 34/100",
       "Simplify: divide the top and bottom by 2. 34 ÷ 2 = 17 and 100 ÷ 2 = 50.", "34/100 = <b>17/50</b>"],
      "17/50 of the fish are guppies.", "34 out of 100 fish, and 34/100 = 17/50.", fig_fish),
]
BT = ("The pie chart shows the percentages of buttons by color in a box. There are 100 blue buttons and green buttons altogether. "
      "The rest are yellow and red. There are twice as many red buttons as blue buttons.")
q141 += [
    Q("Exercise 4 (a)", 238, BT + " (a) What percentage of the buttons are red?",
      "Red is twice blue. Blue is 10%.",
      ["Blue buttons: <b>10%</b>.", "Red is twice as many as blue.", "Red: 2 × 10% = <b>20%</b>"],
      "20% of the buttons are red.", "Twice 10% is 20%.", fig_buttons),
    Q("Exercise 4 (b)", 238, BT + " (b) What percentage of the buttons are yellow?",
      "The whole circle is 100%. Take away the other colors.",
      ["Blue + Green = 10% + 40% = <b>50%</b>", "Red = <b>20%</b> (from part (a))", "Yellow = 100% - 20% - 50% = <b>30%</b>"],
      "30% of the buttons are yellow.", "100% - 20% - 50% = 30%.", fig_buttons),
    Q("Exercise 4 (c)", 238, BT + " (c) What is the total number of buttons in the box?",
      "Blue and green together are 50%, and that is 100 buttons.",
      ["Blue + Green = 50% of the buttons.", "50% = 100 buttons.", "50% is half. The whole (100%) is 2 halves.",
       "100% = 2 × 100 = <b>200</b> buttons"],
      "There are 200 buttons in the box.", "50% is 100 buttons, so 100% is 2 × 100 = 200.", fig_buttons),
    Q("Exercise 4 (d)", 238, BT + " (d) How many blue buttons are there?",
      "Blue is 10% of 200.",
      ["Total: <b>200</b> buttons.", "10% means 10 out of every 100.", "10/100 × 200 = <b>20</b>"],
      "There are 20 blue buttons.", "10% of 200 = 20.", fig_buttons),
    Q("Exercise 4 (e)", 238, BT + " (e) What is the ratio of the number of green buttons to the number of yellow buttons?",
      "Use the percentages, then simplify.",
      ["Green : Yellow", "= 40 : 30", "Divide both by 10: <b>4 : 3</b>"],
      "The ratio is 4 : 3.", "40 : 30 = 4 : 3.", fig_buttons),
    Q("Exercise 4 (f)", 238, BT + " (f) Which are the two colors of buttons that make up 3/5 of the total number of buttons in the box?",
      "Change 3/5 into a percentage. Then find two colors that add up to it.",
      ["3/5 = 60/100 = <b>60%</b>", "Try pairs: Red 20% + Green 40% = <b>60%</b> ✓"],
      "Green and red buttons make up 3/5 of the box.", "3/5 = 60% and 20% + 40% = 60%.", fig_buttons),
]

flash141 = [
    {"front": "Pie chart", "back": "A circle cut into slices to show data. Also called a circle graph."},
    {"front": "Sector (slice)", "back": "One part of a pie chart. A bigger amount has a bigger slice."},
    {"front": "The whole circle", "back": "All the data: 1 whole, or 100%."},
    {"front": "A quarter of the circle", "back": "1/4 = 25%. It has a little square (right angle) at the centre."},
    {"front": "Half of the circle", "back": "1/2 = 50%. A straight line through the centre cuts it in half."},
    {"front": "Fraction of a group", "back": "Part ÷ total. Example: 40 boys out of 160 = 40/160 = 1/4."},
    {"front": "Percentage of a group", "back": "Fraction × 100%. Example: 1/4 × 100% = 25%."},
    {"front": "Missing slice", "back": "Total take away all the other slices. Example: 100% - 40% - 20% = 40%."},
    {"front": "Finding the total", "back": "If a quarter is 45, the whole is 45 × 4 = 180."},
    {"front": "Same size slices", "back": "Same size slices show the same amount."},
]
match141 = [
    ["1/4 of the circle", "25%"], ["1/2 of the circle", "50%"], ["3/8", "37.5%"], ["1/8", "12.5%"],
    ["Whole circle", "100%"], ["3/5", "60%"], ["Quarter is 45", "Total 180"], ["Half is 50", "Total 100"],
]
for a, b in [(Fr(1, 4), 25), (Fr(1, 2), 50), (Fr(3, 8), 37.5), (Fr(1, 8), 12.5), (Fr(3, 5), 60)]:
    check(float(a * 100), b, "match % check")
quiz141 = [
    {"q": "What is another name for a pie chart?", "options": ["Circle graph", "Bar graph", "Line graph", "Table"]},
    {"q": "The whole circle of a pie chart is how many percent?", "options": ["100%", "50%", "360%", "10%"]},
    {"q": "A slice has a right-angle mark at the centre. What fraction of the circle is it?", "options": ["1/4", "1/2", "1/3", "3/4"]},
    {"q": "Savings 40%, food 35%, the rest is transport. What percent is transport?", "options": ["25%", "35%", "75%", "15%"]},
    {"q": "There are 40 boys out of 160 people. What fraction are boys?", "options": ["1/4", "1/3", "4/16", "2/5"]},
    {"q": "A quarter of the pie chart is 45 people. How many people in total?", "options": ["180", "90", "135", "49"]},
    {"q": "60 out of 160 people are adults. What percentage is that?", "options": ["37.5%", "60%", "35%", "3.75%"]},
    {"q": "Half of a pie chart is 50 fish. Swordfish are 16 of that half. The rest of that half is guppies. How many guppies?",
     "options": ["34", "66", "16", "50"]},
    {"q": "Blue is 10% of 200 buttons. How many blue buttons?", "options": ["20", "10", "2", "190"]},
    {"q": "Green is 40% and yellow is 30%. What is green : yellow?", "options": ["4 : 3", "3 : 4", "40 : 70", "1 : 3"]},
    {"q": "3/5 of the buttons is what percentage?", "options": ["60%", "35%", "30%", "53%"]},
]
check(100 - 40 - 35, 25, "quiz transport")
check(Fr(40, 160), Fr(1, 4), "quiz boys")
check(45 * 4, 180, "quiz total")
check(60 / 160 * 100, 37.5, "quiz adults")
check(50 - 16, 34, "quiz guppies")
check(200 * 10 // 100, 20, "quiz blue")

sections = [{"id": "14-1", "title": "Reading Pie Charts", "short": "1. Pie Charts", "pages": "p.231 to 238",
             "learn": learn141, "questions": q141, "flash": flash141, "match": match141, "quiz": quiz141}]

# =====================================================================
# CHALLENGE (p.239 to 244)
# =====================================================================
fr_books, fr_food, fr_trans = Fr(1, 3), Fr(1, 12), Fr(2, 12)
fr_clothes = check(1 - fr_books - fr_food - fr_trans, Fr(5, 12), "p.239 (a)")
unit_baht = 60  # food = 1/12 = 1 unit
clothes = check(5 * unit_baht, 300, "p.239 (b)")
check(fr_books / fr_food, 4, "p.239 (c) books units")
check(fr_books + fr_food, fr_clothes, "p.239 (c) books + food = clothes")
fig_mary = pie([(["Books", "1/3"], 4, BLU), (["Transport", "2/12"], 2, GRN), (["Food", "1/12"], 1, ORA), ("Clothes", 5, PNK)])

MA = "The pie chart shows how Mary spent her pocket money last week. She spent 60 baht on food."
dess = {"Cake": 80, "Tart": 20, "Cookies": 120, "Ice cream": 100}
dtot = check(sum(dess.values()), 320, "p.240 total")
check([Fr(v, dtot) for v in dess.values()], [Fr(1, 4), Fr(1, 16), Fr(3, 8), Fr(5, 16)], "p.240 (a)")
fig_dessert = pie([(["Cake", "1/4"], 80, ORA), (["Tart", "1/16"], 20, PNK), (["Cookies", "3/8"], 120, YEL), (["Ice cream", "5/16"], 100, BLU)])

fruits = {"Pineapples": 50, "Papayas": 30, "Pears": 40}
ppp = check(sum(fruits.values()), 120, "p.242 three fruits")
mango = ppp  # mangoes is a quarter, and pineapples + papayas + pears is the other quarter of that half
check(Fr(1, 2) - Fr(1, 4), Fr(1, 4), "p.242 half - quarter")
semi = check(ppp * 2, 240, "p.242 semicircle")
oranges = check(semi - 50, 190, "p.242 oranges")
apples = 50  # vertically opposite pineapples
check(ppp * 3, 360, "p.242 three quarters")
check(360 - 50 - 50 - 30 - 40, 190, "p.242 method 2")
fig_fruit = pie([(["Pineapples", "50"], 50, BLU), ("Oranges", oranges, YEL), ("Apples", apples, GRN), (["Pears", "40"], 40, TEAL),
                 ("Mangoes", mango, ORA), (["Papayas", "30"], 30, PNK)], r=100, ra=(4,), start=-118)
# check the two straight lines through the centre: pineapples + oranges = half, and oranges + apples = half
check(50 + oranges, 240, "p.242 line 1 is straight")
check(oranges + apples, 240, "p.242 line 2 is straight")

fig_shoes = pie([("Sandals", 3, YEL), ("Sneakers", 2, BLU), ("Boots", 3, PNK), (["Dress", "shoes"], 4, GRN)], r=80, ra=(0, 2))
barA = bars(["Sandals", "Sneakers", "Boots", "Dress"], [3, 2, 4, 4], "Bar Graph A", 5, w=300, h=200, numbers=False, fills=[YEL, BLU, PNK, GRN])
barB = bars(["Sandals", "Sneakers", "Boots", "Dress"], [3, 2, 3, 4], "Bar Graph B", 5, w=300, h=200, numbers=False, fills=[YEL, BLU, PNK, GRN])


def shift_bar(f, dx):
    out = []
    for it in f["items"]:
        it = json.loads(json.dumps(it))
        if it["t"] == "txt":
            it["at"][0] += dx
        else:
            for p in it["p"]:
                p[0] += dx
        out.append(it)
    return out


fig_bars2 = {"w": 610, "h": 200, "pts": {}, "items": shift_bar(barA, 0) + shift_bar(barB, 310)}

qch = [
    Q("Let's Think Along (a)", 239, MA + " (a) What fraction of her pocket money was spent on clothes?",
      "The whole circle is 1. Take away the other fractions. Make them all twelfths first.",
      ["Books = 1/3. Change it to twelfths: 1/3 = <b>4/12</b>", "Food = <b>1/12</b>. Transport = <b>2/12</b>.",
       "Books + Food + Transport = 4/12 + 1/12 + 2/12 = <b>7/12</b>", "Clothes = 1 - 7/12 = 12/12 - 7/12 = <b>5/12</b>"],
      "5/12 of her pocket money was spent on clothes.", "1 - 1/3 - 1/12 - 2/12 = 5/12.", fig_mary),
    Q("Let's Think Along (b)", 239, MA + " (b) How much money did she spend on clothes?",
      "Food is 1/12, that is 1 unit = 60 baht. Clothes is 5/12, that is 5 units.",
      ["Cut the circle into 12 equal units.", "Food = 1/12 = <b>1 unit = 60 baht</b>", "Clothes = 5/12 = <b>5 units</b>",
       "5 units = 5 × 60 baht = <b>300 baht</b>"],
      "She spent 300 baht on clothes.", "1 unit = 60 baht, so 5 units = 300 baht.", fig_mary),
    Q("Let's Think Along (c)", 239, MA + " (c) Was the total amount she spent on books and food the same as the amount spent on clothes? Explain.",
      "Count the units for books, food and clothes.",
      ["Books = 1/3 = 4/12 = <b>4 units</b>", "Food = 1/12 = <b>1 unit</b>", "Books + Food = 4 units + 1 unit = <b>5 units</b>",
       "Clothes = <b>5 units</b> (from part (b))", "5 units = 5 units ✓"],
      "Yes. Books and food are 4 units + 1 unit = 5 units, the same as clothes (5 units).",
      "Both are 5/12 of her pocket money (300 baht).", fig_mary),
    Q("Performance Task (a)", 240,
      "In a survey, 320 children were asked to name their favorite desserts. The table shows the number of children who chose each type of dessert."
      + table(["Type of dessert", "Cake", "Tart", "Cookies", "Ice cream"], [["Number of children", "80", "20", "120", "100"], ["Fraction", "?", "?", "?", "?"]])
      + "(a) Work out the fraction of children who like each type of dessert and fill in the table.",
      "Fraction = number of children ÷ 320. Then simplify.",
      ["Cake: 80/320. Divide top and bottom by 80: <b>1/4</b>", "Tart: 20/320. Divide top and bottom by 20: <b>1/16</b>",
       "Cookies: 120/320. Divide top and bottom by 40: <b>3/8</b>", "Ice cream: 100/320. Divide top and bottom by 20: <b>5/16</b>",
       "Check: 4/16 + 1/16 + 6/16 + 5/16 = 16/16 = 1 ✓"],
      "Cake 1/4, Tart 1/16, Cookies 3/8, Ice cream 5/16", "Each number ÷ 320, simplified. They add up to 1 whole."),
    Q("Performance Task (b)", 240,
      "Present the information in the given pie chart. Label the pie chart and use a different color for each type of dessert.",
      "The circle has 16 equal parts. Each part is 1/16.",
      ["Make the circle into <b>16</b> equal parts. Each part is 1/16.", "Cake 1/4 = 4/16: color <b>4</b> parts.",
       "Tart 1/16: color <b>1</b> part.", "Cookies 3/8 = 6/16: color <b>6</b> parts.", "Ice cream 5/16: color <b>5</b> parts.",
       "4 + 1 + 6 + 5 = 16 parts ✓"],
      "Cake 4 parts, Tart 1 part, Cookies 6 parts and Ice cream 5 parts, each in a different color, as in the pie chart.",
      "Each fraction out of 16 tells you how many of the 16 parts to color.", fig_dessert),
    Q("Problem Solving", 241, "The pie chart shows the number of fruits sold at a fruit stall. How many oranges are there?",
      "Mangoes has a little square, so it is a quarter. Pineapples, papayas and pears make the other quarter of that half.",
      ["Pineapples + Papayas + Pears = 50 + 30 + 40 = <b>120</b>",
       "The straight line makes a half. That half is Pineapples, Papayas, Mangoes and Pears.",
       "Mangoes is a quarter (1/4), so the rest of that half is 1/2 - 1/4 = <b>1/4</b>.",
       "So one quarter of the circle is <b>120</b> fruits.",
       "One semicircle (half) = 120 × 2 = <b>240</b>.",
       "The other half is Pineapples + Oranges = <b>240</b>.",
       "Oranges = 240 - 50 = <b>190</b>"],
      "There are 190 oranges.", "A quarter is 120, so a half is 240. Pineapples + oranges = 240, so oranges = 240 - 50 = 190.", fig_fruit),
    Q("Math Journal", 243,
      "The pie chart shows information on the different types of footwear Mr Tay sold on a Sunday. "
      "Explain which bar graph below best represents the information in the pie chart.",
      "Which slices are the same size? Which slice is the biggest?",
      ["In the pie chart, Sandals and Boots are the <b>same size</b> (both are quarters).",
       "So the Sandals and Boots bars must be the <b>same height</b>.",
       "Dress shoes is the <b>biggest</b> slice, so its bar must be the <b>tallest</b>.",
       "Bar Graph A: Boots is taller than Sandals. ✗", "Bar Graph B: Sandals = Boots, and Dress shoes is tallest. ✓"],
      "Bar graph B. The pie chart shows the same number of sandals and boots sold, so their bars should be the same height. "
      "The bar for dress shoes should be the tallest, as the most dress shoes were sold.",
      "Same size slices = same height bars. Biggest slice = tallest bar.",
      None),
]

# Math Journal figure: pie on top (moved to the middle), the two bar graphs below.
_mj = []
for it in fig_shoes["items"]:
    it = json.loads(json.dumps(it))
    if it["t"] == "sector":
        it["c"][0] += 195
    elif it["t"] == "txt":
        it["at"][0] += 195
    elif it["t"] == "ra":
        for k in ("v", "a", "b"):
            it[k][0] += 195
    _mj.append(it)
for it in fig_bars2["items"]:
    it = json.loads(json.dumps(it))
    if it["t"] == "txt":
        it["at"][1] += fig_shoes["h"] + 6
    else:
        for p in it["p"]:
            p[1] += fig_shoes["h"] + 6
    _mj.append(it)
qch[-1]["fig"] = {"w": 610, "h": fig_shoes["h"] + 206, "pts": {}, "items": _mj}

learn_ch = [
    L("Idea", "Unit 14 big ideas",
      "<p>🥧 A pie chart shows parts of a whole.</p><p>Whole circle = <b>1</b> = <b>100%</b>.</p>"
      "<p>Little square = a <b>quarter</b>. Straight line through the centre = two <b>halves</b>.</p>"
      "<p>Know one part? Use it to find the total, then the other parts.</p>", None, 239),
    L("Example", "Units in a pie chart",
      "<p>Mary: Books 1/3, Transport 2/12, Food 1/12.</p><p>Make them all twelfths: Books 4/12, Transport 2/12, Food 1/12.</p>"
      "<p>Clothes = 12/12 - 7/12 = <b>5/12</b>.</p><p>Food 1 unit = 60 baht, so Clothes 5 units = <b>300 baht</b>.</p>", fig_mary, 239),
    L("Example", "Vertically opposite slices",
      "<p>When two straight lines cross at the centre, the opposite angles are <b>equal</b>.</p>"
      "<p>Equal angles = equal slices. Apples is opposite Pineapples, so Apples = <b>50</b>.</p>"
      "<p>Another way: 3 quarters = 120 × 3 = 360. Oranges = 360 - 50 - 50 - 30 - 40 = <b>190</b>.</p>", fig_fruit, 242),
    L("Example", "Math in Real Life: food waste",
      "<p>A survey asked 1,016 people about food waste. 90% feel it is a waste of money to throw food away.</p>"
      "<p>Work in groups. Ask your class a question about food waste and make a pie chart of the answers.</p>", None, 244),
]
quiz_ch = [
    {"q": "Books 1/3, transport 2/12, food 1/12. What fraction is clothes?", "options": ["5/12", "7/12", "4/12", "1/2"]},
    {"q": "Food is 1/12 = 60 baht. Clothes is 5/12. How much is clothes?", "options": ["300 baht", "60 baht", "720 baht", "250 baht"]},
    {"q": "80 out of 320 children like cake. What fraction is that?", "options": ["1/4", "1/8", "1/3", "8/32"]},
    {"q": "120 out of 320 children like cookies. What fraction is that?", "options": ["3/8", "1/3", "3/4", "12/32"]},
    {"q": "One quarter of a pie chart is 120 fruits. How many fruits in a half?", "options": ["240", "60", "480", "360"]},
    {"q": "Two lines cross at the centre. Pineapples is 50. The slice opposite it is…", "options": ["50", "100", "130", "25"]},
    {"q": "Sandals and boots are the same size slices. In a bar graph their bars are…", "options": ["the same height", "different heights", "always the tallest", "always the shortest"]},
    {"q": "The biggest slice in a pie chart shows…", "options": ["the most", "the least", "half of the data", "nothing"]},
    {"q": "Half a pie chart is 240. Pineapples in that half is 50. The rest of that half is oranges. How many?", "options": ["190", "290", "120", "240"]},
    {"q": "100% - 20% - 50% = ?", "options": ["30%", "70%", "50%", "20%"]},
]
check(Fr(80, 320), Fr(1, 4), "quiz cake")
check(Fr(120, 320), Fr(3, 8), "quiz cookies")
check(240 - 50, 190, "quiz oranges")
sections.append({"id": "14-ch", "title": "Unit 14 Challenge", "short": "⭐ Challenge", "pages": "p.239 to 244",
                 "learn": learn_ch, "questions": qch, "flash": flash141[:6] + [
                     {"front": "Units", "back": "Change fractions to the same bottom number. 1/12 = 1 unit, 5/12 = 5 units."},
                     {"front": "Vertically opposite", "back": "Two straight lines cross: the opposite slices are the same size."}],
                 "match": match141[:6] + [["1/16", "Tart: 20 of 320"], ["5/12", "Clothes"]],
                 "quiz": quiz_ch})

unit = {"unit": "14", "title": "Presentation of Data", "pages": "p.231 to 244", "sections": sections,
        "expectedPages": {"14-1": [235, 236, 237, 238], "14-ch": [239, 240, 241, 243]}}

if PROBLEMS:
    print("MATHS CHECK FAILED. Nothing was written:")
    for p in PROBLEMS:
        print("  -", p)
    sys.exit(1)
out = os.path.join(os.path.dirname(__file__), "..", "content", "unit14.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(unit, f, ensure_ascii=False, separators=(",", ":"))
print("Unit 14 written: every answer matches the answer key ✅")
