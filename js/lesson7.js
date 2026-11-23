// Unit 7 lesson slides (very simple steps) and easy class games for the projector.
// Every game question is made by code, and its answer is worked out by code, so it is always right.

const RED = "#E53935";
const view = () => document.getElementById("view");

// ---------- drawing helpers ----------
// A triangle with base BC and the 2 base angles given (both less than 90°). A is the top corner.
function triSpec(angB, angC, opt = {}) {
  const r = d => d * Math.PI / 180;
  const base = 240, Bx = 40, By = 200;
  const tB = Math.tan(r(angB)), tC = Math.tan(r(angC));
  const x = base * tC / (tB + tC), h = x * tB;
  let A = [Bx + x, By - h], B = [Bx, By], C = [Bx + base, By];
  const s = Math.min(1, 230 / h);            // keep tall triangles on the screen
  if (s < 1) { A = [Bx + x * s + (base - base * s) / 2, By - h * s]; B = [Bx + (base - base * s) / 2, By]; C = [Bx + (base + base * s) / 2, By]; }
  const items = [{ t: "poly", p: ["A", "B", "C"], fill: opt.fill || "#FFF59D" }];
  const angA = 180 - angB - angC;
  const lab = v => (opt.hide === v ? "?" : `${{ A: angA, B: angB, C: angC }[v]}°`);
  if (opt.angles) ["A", "B", "C"].forEach(v => {
    const o = { A: ["B", "C"], B: ["A", "C"], C: ["A", "B"] }[v];
    if (v === "A" && angA === 90 && opt.hide !== "A") items.push({ t: "ra", v: "A", a: "B", b: "C" });
    items.push({ t: "ang", v, a: o[0], b: o[1], s: lab(v), r: v === "A" ? 24 : 30 });
  });
  if (opt.ticks === "all") items.push({ t: "tick", p: ["A", "B"] }, { t: "tick", p: ["B", "C"] }, { t: "tick", p: ["A", "C"] });
  if (opt.ticks === "two") items.push({ t: "tick", p: ["A", "B"] }, { t: "tick", p: ["A", "C"] });
  if (opt.sides) opt.sides.forEach(([p, q, s]) => items.push({ t: "len", p: [p, q], s }));
  return { w: 320, h: 230, pts: { A, B, C }, items };
}

// A circle with one part painted red: "center", "radius", "diameter", "chord" or "all".
function circleSpec(part, opt = {}) {
  const O = [160, 115], R = 90;
  const at = d => [O[0] + R * Math.cos(d * Math.PI / 180), O[1] - R * Math.sin(d * Math.PI / 180)];
  const rot = opt.rot || 0;
  const items = [{ t: "circle", c: "O", r: R, fill: "#E3F2FD" }];
  const pts = { O };
  const red = (p, q) => items.push({ t: "seg", p: [p, q], color: RED, width: 6 });
  if (part === "radius" || part === "all" || part === "rd") { pts.P = at(30 + rot); red("O", "P"); }
  if (part === "diameter" || part === "all" || part === "rd") { pts.D1 = at(160 + rot); pts.D2 = at(340 + rot); red("D1", "D2"); }
  if (part === "chord" || part === "all") { pts.C1 = at(215 + rot); pts.C2 = at(300 + rot); red("C1", "C2"); }
  items.push({ t: "dot", p: "O", r: part === "center" ? 9 : 5, color: part === "center" ? RED : "#1f2a44" });
  if (opt.labels) {
    items.push({ t: "txt", at: [O[0] - 14, O[1] + 22], s: "O", size: 16 });
    if (pts.P) items.push({ t: "txt", at: [(O[0] + pts.P[0]) / 2 + 8, (O[1] + pts.P[1]) / 2 - 10], s: opt.labels.radius || "radius", size: 15 });
    if (pts.D1) items.push({ t: "txt", at: [(O[0] + pts.D1[0]) / 2 - 4, (O[1] + pts.D1[1]) / 2 - 16], s: opt.labels.diameter || "diameter", size: 15 });
    if (pts.C1) items.push({ t: "txt", at: [(pts.C1[0] + pts.C2[0]) / 2, (pts.C1[1] + pts.C2[1]) / 2 - 10], s: "chord", size: 15 });
  }
  if (opt.text) items.push({ t: "txt", at: [O[0], O[1] + R + 26], s: opt.text, size: 16 });
  return { w: 320, h: 240, pts, items };
}

const pic = spec => `<div class="pic">${Diagram.render(spec)}</div>`;

// ---------- the lesson (follows the book: 7.1 to 7.5) ----------
const SECS = ["7.1 Types of Triangles", "7.2 Angles of a Triangle", "7.3 Drawing Triangles", "7.4 Parts of a Circle", "7.5 Drawing Circles"];
const SLIDES = [
  { s: 0, e: "🔺", t: "What is a triangle?", p: 2, html: "<p>A triangle has <span class='word'>3 straight sides</span>.</p><p>It has <span class='word'>3 corners</span>.</p><p>Each corner has an <span class='word'>angle</span>.</p>", fig: triSpec(60, 60, { fill: "#FFE0B2" }) },
  { s: 0, e: "👀", t: "Look at the SIDES", p: 3, html: "<p>We can sort triangles by their sides.</p><p>Count the sides that are the <b>same length</b>.</p><p>Little <b>tick marks</b> show sides that are the same.</p>", fig: triSpec(65, 65, { ticks: "two" }) },
  { s: 0, e: "🟰", t: "Equilateral: all 3 the same", p: 3, html: "<p><span class='word'>3 sides</span> are the same.</p><p><span class='word'>3 angles</span> are the same.</p><p>Every angle is <b>60°</b>.</p>", fig: triSpec(60, 60, { ticks: "all", angles: true }), ask: "One side is 5 cm. How long are the other 2 sides?", ans: "5 cm and 5 cm. All 3 sides are the same!" },
  { s: 0, e: "✌️", t: "Isosceles: 2 the same", p: 4, html: "<p><span class='word'>2 sides</span> are the same.</p><p><span class='word'>2 angles</span> are the same.</p><p>The 2 same angles are at the bottom, across from the 2 same sides.</p>", fig: triSpec(70, 70, { ticks: "two", angles: true }), ask: "One bottom angle is 70°. What is the other bottom angle?", ans: "70°. They are the same!" },
  { s: 0, e: "🎨", t: "Scalene: none the same", p: 5, html: "<p>All <span class='word'>3 sides</span> are different.</p><p>All <span class='word'>3 angles</span> are different.</p><p>No tick marks!</p>", fig: triSpec(40, 70, { sides: [["A", "B", "4 cm"], ["B", "C", "6 cm"], ["A", "C", "3 cm"]] }), ask: "The sides are 3 cm, 4 cm and 6 cm. What kind of triangle?", ans: "Scalene. No 2 sides are the same." },
  { s: 0, e: "📐", t: "Now look at the ANGLES", p: 5, html: "<p><span class='word'>Acute</span> angle: small and sharp, less than 90°. 🔪</p><p><span class='word'>Right</span> angle: a square corner, exactly 90°. Like the corner of your book! 📘</p><p><span class='word'>Obtuse</span> angle: big and open, more than 90°. 🐊</p>" },
  { s: 0, e: "🔪", t: "Acute triangle", p: 6, html: "<p><b>All 3</b> angles are small (less than 90°).</p><p>60°, 70° and 50° are all small.</p>", fig: triSpec(70, 50, { angles: true, fill: "#C8E6C9" }) },
  { s: 0, e: "📘", t: "Right triangle", p: 5, html: "<p><b>1</b> angle is a square corner: <b>90°</b>.</p><p>The little square shows the right angle.</p><p>The other 2 angles add up to 90°: 30° + 60° = 90°.</p>", fig: triSpec(30, 60, { angles: true, fill: "#BBDEFB" }), ask: "A right triangle has a 35° angle. What is the other small angle?", ans: "90° - 35° = 55°" },
  { s: 0, e: "🐊", t: "Obtuse triangle", p: 6, html: "<p><b>1</b> angle is big and open (more than 90°).</p><p>120° is more than 90°.</p>", fig: triSpec(30, 30, { angles: true, fill: "#F8BBD0" }) },
  { s: 0, e: "🏷️", t: "One triangle, 2 names", p: 7, html: "<p>Name 1: look at the <b>sides</b>.</p><p>Name 2: look at the <b>angles</b>.</p><p>90°, 45°, 45°: a <b>right</b> triangle and an <b>isosceles</b> triangle!</p>", fig: triSpec(45, 45, { angles: true, ticks: "two", fill: "#D1C4E9" }), ask: "The angles are 120°, 30° and 30°. What are its 2 names?", ans: "Obtuse (120° is big) and isosceles (2 angles the same)." },

  { s: 1, e: "✨", t: "The magic number: 180°", p: 13, html: "<p>Cut off the 3 corners of a paper triangle. ✂️</p><p>Put them side by side. They make a <b>straight line</b>.</p><p>A straight line is <b>180°</b>. So the 3 angles of <b>every</b> triangle add up to <b>180°</b>.</p>" },
  { s: 1, e: "✅", t: "Let's check", p: 13, html: "<p>60° + 60° + 60° = 180° ✓</p><p>90° + 30° + 60° = 180° ✓</p><p>120° + 30° + 30° = 180° ✓</p><p>It always works!</p>" },
  { s: 1, e: "🔍", t: "Find the missing angle", p: 14, html: "<p>Step 1: Start with <b>180°</b>.</p><p>Step 2: Take away the first angle. 180° - 50° = 130°</p><p>Step 3: Take away the second angle. 130° - 60° = <b>70°</b></p>", fig: triSpec(50, 60, { angles: true, hide: "A" }) },
  { s: 1, e: "🙋", t: "Your turn!", p: 14, html: "<p>Two angles are 30° and 50°.</p><p>Start with 180°. Take away 30°. Take away 50°.</p>", fig: triSpec(30, 50, { angles: true, hide: "A", fill: "#FFE0B2" }), ask: "What is the missing angle?", ans: "180° - 30° = 150°, then 150° - 50° = 100°" },
  { s: 1, e: "✌️", t: "Isosceles trick", p: 14, html: "<p>The top angle is 40°. The 2 bottom angles are the same.</p><p>Step 1: 180° - 40° = 140°</p><p>Step 2: Share 140° into 2 equal parts: 140° ÷ 2 = <b>70°</b></p><p>Each bottom angle is 70°.</p>", fig: triSpec(70, 70, { angles: true, ticks: "two" }), ask: "The top angle is 68°. What is each bottom angle?", ans: "180° - 68° = 112°, then 112° ÷ 2 = 56°" },
  { s: 1, e: "➖", t: "Straight line = 180°", p: 15, html: "<p>Angles on a straight line also add up to <b>180°</b>.</p><p>If one part is 60°, the other part is 180° - 60° = <b>120°</b>.</p>",
    fig: { w: 320, h: 160, pts: { L: [20, 120], O: [160, 120], R: [300, 120], T: [230, 0] }, items: [{ t: "seg", p: ["L", "R"] }, { t: "seg", p: ["O", "T"] }, { t: "ang", v: "O", a: "R", b: "T", s: "60°", r: 34 }, { t: "ang", v: "O", a: "T", b: "L", s: "?", r: 30 }] },
    ask: "One part is 60°. What is the other part?", ans: "180° - 60° = 120°" },

  { s: 2, e: "🧰", t: "Our drawing tools", p: 22, html: "<p>📏 <b>Ruler</b>: draws straight lines and measures cm.</p><p>🌈 <b>Protractor</b>: measures and draws angles.</p><p>📐 <b>Set square</b>: draws a square corner (90°).</p><p>✏️ Always draw a quick sketch first!</p>" },
  { s: 2, e: "✏️", t: "Draw a triangle, step by step", p: 22, html: "<p><b>1.</b> Draw a line BC, 5 cm long.</p><p><b>2.</b> Protractor at B: draw 50°.</p><p><b>3.</b> Protractor at C: draw 45°.</p><p><b>4.</b> The 2 lines meet. Call it A. Done! 🎉</p>",
    fig: (() => { const f = triSpec(50, 45, { fill: "#FFFDE7" }); f.items.push({ t: "ang", v: "B", a: "A", b: "C", s: "50°", r: 30 }, { t: "ang", v: "C", a: "A", b: "B", s: "45°", r: 30 }, { t: "len", p: ["B", "C"], s: "5 cm" }, { t: "pl", p: "A" }, { t: "pl", p: "B" }, { t: "pl", p: "C" }); return f; })() },
  { s: 2, e: "📐", t: "A right angle with a set square", p: 23, html: "<p><b>1.</b> Draw YZ, 5 cm long.</p><p><b>2.</b> Put the set square on the line at Y. Draw straight up: that is 90°.</p><p><b>3.</b> Measure 5 cm up. Mark X.</p><p><b>4.</b> Join X and Z.</p>",
    fig: { w: 320, h: 230, pts: { X: [70, 30], Y: [70, 200], Z: [240, 200] }, items: [{ t: "poly", p: ["X", "Y", "Z"], fill: "#E1F5FE" }, { t: "ra", v: "Y", a: "X", b: "Z" }, { t: "len", p: ["Y", "Z"], s: "5 cm" }, { t: "len", p: ["X", "Y"], s: "5 cm" }, { t: "pl", p: "X" }, { t: "pl", p: "Y" }, { t: "pl", p: "Z" }] } },

  { s: 3, e: "🎯", t: "The center", p: 28, html: "<p>The <span class='word'>center</span> is the dot in the very middle of the circle.</p><p>We often call it <b>O</b>.</p>", fig: circleSpec("center", { labels: {} }) },
  { s: 3, e: "🍕", t: "Radius", p: 28, html: "<p>A <span class='word'>radius</span> goes from the <b>center</b> to the <b>edge</b>.</p><p>Like a pizza: from the middle to the crust.</p>", fig: circleSpec("radius", { labels: {} }) },
  { s: 3, e: "↔️", t: "Diameter", p: 28, html: "<p>A <span class='word'>diameter</span> goes from edge to edge, <b>through the center</b>.</p><p>It is 2 radii in a straight line.</p>", fig: circleSpec("diameter", { labels: {} }) },
  { s: 3, e: "〰️", t: "Chord", p: 28, html: "<p>A <span class='word'>chord</span> goes from edge to edge, but <b>not</b> through the center.</p><p>The diameter is the <b>longest</b> chord.</p>", fig: circleSpec("chord", { labels: {} }) },
  { s: 3, e: "✖️", t: "Radius and diameter", p: 29, html: "<p>Diameter = 2 × radius</p><p>Radius = diameter ÷ 2</p><p>Radius 4 cm ➡ diameter 2 × 4 = <b>8 cm</b></p>", fig: circleSpec("rd", { labels: { radius: "4 cm", diameter: "8 cm" } }), ask: "The diameter is 15 m. What is the radius?", ans: "15 ÷ 2 = 7.5 m" },

  { s: 4, e: "🧭", t: "The compass", p: 35, html: "<p>A compass has a <b>needle</b> and a <b>pencil</b>.</p><p>The gap between them is the <span class='word'>radius</span>.</p><p>Use a ruler to set the gap.</p>" },
  { s: 4, e: "⭕", t: "Draw a circle, step by step", p: 35, html: "<p><b>1.</b> Mark the center O.</p><p><b>2.</b> Open the compass to the radius (use a ruler).</p><p><b>3.</b> Put the needle on O.</p><p><b>4.</b> Turn the compass all the way round. Join up the ends!</p>", fig: circleSpec("radius", { labels: { radius: "1 cm" } }) },
  { s: 4, e: "➗", t: "Given the diameter? Halve it!", p: 36, html: "<p>The compass is set to the <b>radius</b>, not the diameter.</p><p>Diameter 4 cm ➡ radius 4 ÷ 2 = <b>2 cm</b>.</p><p>Open the compass to 2 cm.</p>", ask: "You must draw a circle with diameter 10 cm. How wide do you open the compass?", ans: "10 ÷ 2 = 5 cm" },
  { s: 4, e: "🎉", t: "Great job! Time to play", p: 46, html: "<p>Triangles: equilateral, isosceles, scalene. Acute, right, obtuse.</p><p>Angles in a triangle: 180°.</p><p>Circles: center, radius, diameter, chord.</p><p><button class='bigbtn dark' id='goGames'>🎮 Play the class games</button></p>" },
];


// Thai for each slide, in the same order: title, text, "Your turn" question, answer.
const SLIDE_TH = [
  { t: "รูปสามเหลี่ยมคืออะไร", h: "มี 3 ด้านที่เป็นเส้นตรง มี 3 มุม แต่ละมุมมีขนาดของมุม" },
  { t: "ดูที่ด้าน", h: "เราแบ่งรูปสามเหลี่ยมตามด้านได้ นับด้านที่ยาวเท่ากัน ขีดเล็ก ๆ บอกว่าด้านไหนยาวเท่ากัน" },
  { t: "ด้านเท่า: เท่ากันทั้ง 3", h: "ด้าน 3 ด้านยาวเท่ากัน มุม 3 มุมเท่ากัน ทุกมุมเท่ากับ 60°", a: "ด้านหนึ่งยาว 5 cm อีก 2 ด้านยาวเท่าไร", n: "5 cm และ 5 cm ทั้ง 3 ด้านยาวเท่ากัน!" },
  { t: "หน้าจั่ว: เท่ากัน 2", h: "ด้าน 2 ด้านยาวเท่ากัน มุม 2 มุมเท่ากัน มุมที่เท่ากันอยู่ข้างล่าง ตรงข้ามกับด้านที่ยาวเท่ากัน", a: "มุมล่างมุมหนึ่งเท่ากับ 70° อีกมุมล่างเท่าไร", n: "70° เท่ากัน!" },
  { t: "ด้านไม่เท่า: ไม่เท่ากันเลย", h: "ทั้ง 3 ด้านยาวไม่เท่ากัน ทั้ง 3 มุมไม่เท่ากัน ไม่มีขีดเลย", a: "ด้านยาว 3 cm, 4 cm และ 6 cm เป็นรูปสามเหลี่ยมชนิดใด", n: "ด้านไม่เท่า ไม่มี 2 ด้านไหนยาวเท่ากัน" },
  { t: "ทีนี้ดูที่มุม", h: "มุมแหลม: เล็กและแหลม น้อยกว่า 90° · มุมฉาก: มุมสี่เหลี่ยม เท่ากับ 90° พอดี เหมือนมุมหนังสือ · มุมป้าน: ใหญ่และกว้าง มากกว่า 90°" },
  { t: "รูปสามเหลี่ยมมุมแหลม", h: "ทั้ง 3 มุมเล็ก (น้อยกว่า 90°) 60°, 70° และ 50° เล็กทุกมุม" },
  { t: "รูปสามเหลี่ยมมุมฉาก", h: "มี 1 มุมเป็นมุมฉาก 90° สี่เหลี่ยมเล็ก ๆ บอกว่าเป็นมุมฉาก อีก 2 มุมรวมกันได้ 90°: 30° + 60° = 90°", a: "รูปสามเหลี่ยมมุมฉากมีมุม 35° อีกมุมเล็กเท่าไร", n: "90° - 35° = 55°" },
  { t: "รูปสามเหลี่ยมมุมป้าน", h: "มี 1 มุมที่ใหญ่และกว้าง (มากกว่า 90°) 120° มากกว่า 90°" },
  { t: "สามเหลี่ยมรูปเดียว มี 2 ชื่อ", h: "ชื่อที่ 1: ดูที่ด้าน ชื่อที่ 2: ดูที่มุม 90°, 45°, 45°: เป็นทั้งรูปสามเหลี่ยมมุมฉากและหน้าจั่ว!", a: "มุมคือ 120°, 30° และ 30° มี 2 ชื่ออะไร", n: "มุมป้าน (120° ใหญ่) และหน้าจั่ว (มี 2 มุมเท่ากัน)" },
  { t: "เลขมหัศจรรย์: 180°", h: "ตัดมุมทั้ง 3 ของรูปสามเหลี่ยมกระดาษ วางเรียงกันจะได้เส้นตรง เส้นตรงเท่ากับ 180° มุมทั้ง 3 ของทุกรูปสามเหลี่ยมจึงรวมกันได้ 180°" },
  { t: "มาตรวจสอบกัน", h: "60° + 60° + 60° = 180° ✓ · 90° + 30° + 60° = 180° ✓ · 120° + 30° + 30° = 180° ✓ ใช้ได้เสมอ!" },
  { t: "หามุมที่หายไป", h: "ขั้นที่ 1: เริ่มจาก 180° ขั้นที่ 2: ลบมุมแรก 180° - 50° = 130° ขั้นที่ 3: ลบมุมที่สอง 130° - 60° = 70°" },
  { t: "ถึงตาเธอแล้ว!", h: "มุมสองมุมคือ 30° และ 50° เริ่มจาก 180° ลบ 30° แล้วลบ 50°", a: "มุมที่หายไปเท่าไร", n: "180° - 30° = 150° แล้ว 150° - 50° = 100°" },
  { t: "เคล็ดลับหน้าจั่ว", h: "มุมยอด 40° มุมล่าง 2 มุมเท่ากัน ขั้นที่ 1: 180° - 40° = 140° ขั้นที่ 2: แบ่ง 140° เป็น 2 ส่วนเท่ากัน: 140° ÷ 2 = 70° มุมล่างแต่ละมุมเท่ากับ 70°", a: "มุมยอด 68° มุมล่างแต่ละมุมเท่าไร", n: "180° - 68° = 112° แล้ว 112° ÷ 2 = 56°" },
  { t: "เส้นตรง = 180°", h: "มุมบนเส้นตรงรวมกันได้ 180° ถ้าส่วนหนึ่งเท่ากับ 60° อีกส่วนเท่ากับ 180° - 60° = 120°", a: "ส่วนหนึ่งเท่ากับ 60° อีกส่วนเท่าไร", n: "180° - 60° = 120°" },
  { t: "อุปกรณ์วาดรูปของเรา", h: "📏 ไม้บรรทัด: ลากเส้นตรงและวัด cm · 🌈 ไม้โปรแทรกเตอร์: วัดและวาดมุม · 📐 ไม้ฉาก: วาดมุมฉาก (90°) · ✏️ วาดรูปคร่าว ๆ ก่อนเสมอ!" },
  { t: "สร้างรูปสามเหลี่ยมทีละขั้น", h: "1. ลากเส้น BC ยาว 5 cm 2. วางไม้โปรแทรกเตอร์ที่ B วาด 50° 3. วางที่ C วาด 45° 4. เส้นทั้งสองตัดกัน เรียกว่า A เสร็จแล้ว! 🎉" },
  { t: "ทำมุมฉากด้วยไม้ฉาก", h: "1. ลาก YZ ยาว 5 cm 2. วางไม้ฉากบนเส้นที่ Y ลากขึ้นตรง ๆ: นั่นคือ 90° 3. วัดขึ้นไป 5 cm ทำจุด X 4. ลากเชื่อม X กับ Z" },
  { t: "จุดศูนย์กลาง", h: "จุดศูนย์กลางคือจุดที่อยู่ตรงกลางของวงกลมพอดี เรามักเรียกว่า O" },
  { t: "รัศมี", h: "รัศมีลากจากจุดศูนย์กลางไปถึงขอบ เหมือนพิซซ่า: จากตรงกลางถึงขอบ" },
  { t: "เส้นผ่านศูนย์กลาง", h: "เส้นผ่านศูนย์กลางลากจากขอบถึงขอบ ผ่านจุดศูนย์กลาง เท่ากับรัศมี 2 เส้นต่อกันเป็นเส้นตรง" },
  { t: "คอร์ด", h: "คอร์ดลากจากขอบถึงขอบ แต่ไม่ผ่านจุดศูนย์กลาง เส้นผ่านศูนย์กลางคือคอร์ดที่ยาวที่สุด" },
  { t: "รัศมีและเส้นผ่านศูนย์กลาง", h: "เส้นผ่านศูนย์กลาง = 2 × รัศมี · รัศมี = เส้นผ่านศูนย์กลาง ÷ 2 · รัศมี 4 cm ➡ เส้นผ่านศูนย์กลาง 2 × 4 = 8 cm", a: "เส้นผ่านศูนย์กลาง 15 m รัศมีเท่าไร", n: "15 ÷ 2 = 7.5 m" },
  { t: "วงเวียน", h: "วงเวียนมีปลายเหล็กและดินสอ ระยะห่างระหว่างสองปลายคือรัศมี ใช้ไม้บรรทัดวัดระยะกาง" },
  { t: "สร้างวงกลมทีละขั้น", h: "1. ทำจุดศูนย์กลาง O 2. กางวงเวียนเท่ากับรัศมี (ใช้ไม้บรรทัด) 3. วางปลายเหล็กที่ O 4. หมุนวงเวียนจนครบรอบ ให้ปลายบรรจบกัน!" },
  { t: "โจทย์ให้เส้นผ่านศูนย์กลาง? แบ่งครึ่ง!", h: "กางวงเวียนตามรัศมี ไม่ใช่เส้นผ่านศูนย์กลาง เส้นผ่านศูนย์กลาง 4 cm ➡ รัศมี 4 ÷ 2 = 2 cm กางวงเวียน 2 cm", a: "ต้องวาดวงกลมที่มีเส้นผ่านศูนย์กลาง 10 cm ต้องกางวงเวียนเท่าไร", n: "10 ÷ 2 = 5 cm" },
  { t: "เก่งมาก! ได้เวลาเล่นเกมแล้ว", h: "รูปสามเหลี่ยม: ด้านเท่า หน้าจั่ว ด้านไม่เท่า มุมแหลม มุมฉาก มุมป้าน · มุมในรูปสามเหลี่ยม: 180° · วงกลม: จุดศูนย์กลาง รัศมี เส้นผ่านศูนย์กลาง คอร์ด" },
];
const SEC_TH = ["7.1 ชนิดของรูปสามเหลี่ยม", "7.2 มุมของรูปสามเหลี่ยม", "7.3 การสร้างรูปสามเหลี่ยม", "7.4 ส่วนต่าง ๆ ของวงกลม", "7.5 การสร้างวงกลม"];
const OPT_TH = { Equilateral: "ด้านเท่า", Isosceles: "หน้าจั่ว", Scalene: "ด้านไม่เท่า", Acute: "มุมแหลม", Right: "มุมฉาก", Obtuse: "มุมป้าน",
  Center: "จุดศูนย์กลาง", Radius: "รัศมี", Diameter: "เส้นผ่านศูนย์กลาง", Chord: "คอร์ด", "👍 True": "จริง", "👎 False": "เท็จ" };
const TH = (en, th) => (th ? `${en}<span class="th">${th}</span>` : en);

let cur = 0;
function lesson() {
  const sl = SLIDES[cur], T = SLIDE_TH[cur];
  view().innerHTML = `
    <div class="jump">${SECS.map((t, i) => `<button data-s="${i}" class="${sl.s === i ? "on" : ""}">${TH(t, SEC_TH[i])}</button>`).join("")}</div>
    <div class="slide">
      <span class="sec">${SECS[sl.s]} · ${SEC_TH[sl.s]}</span> <span class="badge">📖 p.${sl.p}</span>
      <h2>${sl.e} ${TH(sl.t, T.t)}</h2>
      <div class="two"><div class="big">${sl.html}<p class="th">${T.h}</p></div>${sl.fig ? pic(sl.fig) : "<div></div>"}</div>
      ${sl.ask ? `<div class="turn">🙋 Your turn: ${TH(sl.ask, "ถึงตาเธอ: " + T.a)}<div class="reveal"><button class="bigbtn" id="reveal">${TH("👀 Show answer", "ดูคำตอบ")}</button></div></div>` : ""}
    </div>
    <div class="slide-nav">
      <button class="bigbtn" id="prev" ${cur === 0 ? "disabled" : ""}>${TH("⬅ Back", "ย้อนกลับ")}</button>
      <span class="count">${cur + 1} / ${SLIDES.length}</span>
      <button class="bigbtn dark" id="next" ${cur === SLIDES.length - 1 ? "disabled" : ""}>${TH("Next ➡", "ถัดไป")}</button>
    </div>`;
  view().querySelectorAll(".jump button").forEach(b => b.onclick = () => { cur = SLIDES.findIndex(x => x.s === Number(b.dataset.s)); lesson(); });
  document.getElementById("prev").onclick = () => { if (cur > 0) { cur--; lesson(); } };
  document.getElementById("next").onclick = () => { if (cur < SLIDES.length - 1) { cur++; lesson(); } };
  const rv = document.getElementById("reveal");
  if (rv) rv.onclick = () => { rv.parentElement.outerHTML = `<div class="ans">✅ ${TH(sl.ans, T.n)}</div>`; };
  const gg = document.getElementById("goGames");
  if (gg) gg.onclick = () => setMode("games");
}

// ---------- games ----------
const rnd = (a, b, step = 1) => a + step * Math.floor(Math.random() * (Math.floor((b - a) / step) + 1));
const pick = arr => arr[Math.floor(Math.random() * arr.length)];
function opts(right, wrongs) {
  const o = [right];
  for (const w of wrongs) if (!o.includes(w) && o.length < 4) o.push(w);
  return shuffle(o);
}

const GAMES = {
  sides: { e: "🟰", name: "Count the same sides", desc: "Is it equilateral, isosceles or scalene?", make() {
    const k = pick(["Equilateral", "Isosceles", "Scalene"]);
    let fig, why;
    if (k === "Equilateral") { fig = triSpec(60, 60, { ticks: "all", fill: "#FFE0B2" }); why = "All 3 sides have a tick mark, so all 3 are the same."; }
    if (k === "Isosceles") { const b = pick([40, 50, 65, 70]); fig = triSpec(b, b, { ticks: "two", fill: "#C8E6C9" }); why = "2 sides have tick marks, so 2 sides are the same."; }
    if (k === "Scalene") { const b = pick([35, 40, 45]), c = pick([65, 70, 75]); fig = triSpec(b, c, { fill: "#BBDEFB" }); why = "No tick marks: all 3 sides are different."; }
    return { q: "What kind of triangle is this? (Look at the tick marks.) · รูปสามเหลี่ยมนี้เป็นชนิดใด (ดูขีดบนด้าน)", fig, options: shuffle(["Equilateral", "Isosceles", "Scalene"]), right: k, why };
  } },
  angles: { e: "📐", name: "Small, square or big?", desc: "Is it an acute, right or obtuse triangle?", make() {
    const k = pick(["Acute", "Right", "Obtuse"]);
    let b, c;
    if (k === "Acute") { b = rnd(50, 70, 5); c = rnd(50, 70, 5); }
    if (k === "Right") { b = rnd(30, 60, 5); c = 90 - b; }
    if (k === "Obtuse") { b = rnd(20, 35, 5); c = rnd(20, 35, 5); }
    const a = 180 - b - c;
    const why = k === "Acute" ? `${a}°, ${b}° and ${c}° are all less than 90°.` : k === "Right" ? "It has a square corner: 90°." : `${a}° is more than 90°.`;
    return { q: "What kind of triangle is this? (Look at the angles.) · รูปสามเหลี่ยมนี้เป็นชนิดใด (ดูที่มุม)", fig: triSpec(b, c, { angles: true, fill: "#FFF59D" }), options: shuffle(["Acute", "Right", "Obtuse"]), right: k, why };
  } },
  missing: { e: "🔍", name: "Find the missing angle", desc: "Start with 180°, take away the 2 angles.", make() {
    let b, c;
    do { b = rnd(30, 70, 10); c = rnd(30, 70, 10); } while (b + c > 130);
    const a = 180 - b - c;
    return { q: `Two angles are ${b}° and ${c}°. What is the missing angle? · มุมสองมุมคือ ${b}° และ ${c}° มุมที่หายไปเท่าไร`, fig: triSpec(b, c, { angles: true, hide: "A", fill: "#FFE0B2" }),
      options: opts(`${a}°`, [`${180 - b}°`, `${b + c}°`, `${a + 10}°`, `${a - 10}°`]), right: `${a}°`, why: `180° - ${b}° = ${180 - b}°, then ${180 - b}° - ${c}° = ${a}°.` };
  } },
  circle: { e: "⭕", name: "Circle parts", desc: "Center, radius, diameter or chord? Plus × 2 and ÷ 2.", make() {
    const t = pick(["part", "part", "r2d", "d2r"]);
    if (t === "part") {
      const k = pick(["center", "radius", "diameter", "chord"]);
      const why = { center: "The dot in the very middle is the center.", radius: "It goes from the center to the edge.", diameter: "It goes edge to edge, through the center.", chord: "It goes edge to edge, but not through the center." }[k];
      const name = k[0].toUpperCase() + k.slice(1);
      return { q: "What is the red part called? · ส่วนสีแดงเรียกว่าอะไร", fig: circleSpec(k, { rot: rnd(0, 90, 15) }), options: shuffle(["Center", "Radius", "Diameter", "Chord"]), right: name, why };
    }
    if (t === "r2d") {
      const r = rnd(2, 12);
      return { q: `The radius is ${r} cm. What is the diameter? · รัศมี ${r} cm เส้นผ่านศูนย์กลางยาวเท่าไร`, fig: circleSpec("radius", { labels: { radius: `${r} cm` } }),
        options: opts(`${2 * r} cm`, [`${r / 2} cm`, `${r} cm`, `${r + 2} cm`]), right: `${2 * r} cm`, why: `Diameter = 2 × radius = 2 × ${r} = ${2 * r} cm.` };
    }
    const d = rnd(4, 30, 2);
    return { q: `The diameter is ${d} cm. What is the radius? · เส้นผ่านศูนย์กลาง ${d} cm รัศมียาวเท่าไร`, fig: circleSpec("diameter", { labels: { diameter: `${d} cm` } }),
      options: opts(`${d / 2} cm`, [`${2 * d} cm`, `${d} cm`, `${d - 2} cm`]), right: `${d / 2} cm`, why: `Radius = diameter ÷ 2 = ${d} ÷ 2 = ${d / 2} cm.` };
  } },
  tf: { e: "👍", name: "True or false?", desc: "Thumbs up or thumbs down!", make() {
    const [s, t, why] = pick(TF);
    return { q: s, options: ["👍 True", "👎 False"], right: t ? "👍 True" : "👎 False", why };
  } },
};
const TF = [
  ["The 3 angles of a triangle add up to 180°.", true, "Every triangle: 180°."],
  ["An equilateral triangle has 3 equal sides.", true, "Equilateral: all 3 sides the same."],
  ["An isosceles triangle has 3 equal sides.", false, "Isosceles has 2 equal sides."],
  ["A scalene triangle has no equal sides.", true, "Scalene: all different."],
  ["A right triangle has a 90° angle.", true, "Right angle = square corner = 90°."],
  ["A triangle can have 2 right angles.", false, "90° + 90° = 180° already. No room for a third angle!"],
  ["An obtuse triangle has 1 big angle (more than 90°).", true, "Only 1 angle can be more than 90°."],
  ["Every angle in an equilateral triangle is 60°.", true, "180° ÷ 3 = 60°."],
  ["The diameter goes through the center.", true, "Edge to edge, through the middle."],
  ["The radius is longer than the diameter.", false, "The diameter is 2 radii, so it is longer."],
  ["Diameter = 2 × radius.", true, "2 radii make 1 diameter."],
  ["A chord always goes through the center.", false, "Only the diameter does. A chord does not have to."],
  ["We open the compass to the diameter.", false, "We open it to the radius."],
  ["Angles on a straight line add up to 180°.", true, "A straight line is 180°."],
  ["An acute triangle has all 3 angles less than 90°.", true, "Acute = all small."],
  ["The longest chord of a circle is the diameter.", true, "The diameter goes all the way across through the center."],
];

let G = null;   // { game, teams:[{name, pts}], turn, n, total, q, done }
let gPick = "sides", nTeams = 2;
function gamesMenu() {
  view().innerHTML = `
    <div class="panel"><h2>🎮 Pick a game · เลือกเกม</h2>
      <div class="games">${Object.entries(GAMES).map(([id, g]) => `<button class="gcard ${id === gPick ? "on" : ""}" data-g="${id}"><div class="gt">${g.e} ${g.name}</div>${g.desc}</button>`).join("")}</div>
      <h2 style="margin-top:16px">👥 How many teams? · กี่ทีม</h2>
      <div class="btnrow">${[2, 3, 4].map(n => `<button class="bigbtn ${n === nTeams ? "dark" : ""}" data-n="${n}">${n} teams</button>`).join("")}</div>
      <div class="team-setup">${Array.from({ length: nTeams }, (_, i) => `<input id="tn${i}" value="Team ${i + 1}" aria-label="Team ${i + 1} name">`).join("")}</div>
      <p class="small">Each team gets 3 questions, one at a time. Tap the team's answer. Right = 1 point.</p>
      <div class="btnrow"><button class="bigbtn dark" id="startG">▶ Start</button></div>
    </div>`;
  view().querySelectorAll(".gcard").forEach(b => b.onclick = () => { gPick = b.dataset.g; gamesMenu(); });
  view().querySelectorAll("[data-n]").forEach(b => b.onclick = () => { nTeams = Number(b.dataset.n); gamesMenu(); });
  document.getElementById("startG").onclick = () => {
    const teams = Array.from({ length: nTeams }, (_, i) => ({ name: (document.getElementById("tn" + i).value || `Team ${i + 1}`).slice(0, 20), pts: 0 }));
    G = { game: gPick, teams, turn: 0, n: 0, total: nTeams * 3, last: "" };
    nextQ();
  };
}

function board() {
  const top = Math.max(...G.teams.map(t => t.pts));
  return `<div class="scoreboard">${G.teams.map((t, i) => `<div class="team t${i} ${top > 0 && t.pts === top ? "lead" : ""}">${esc(t.name)}<div class="pts">${t.pts}</div></div>`).join("")}</div>`;
}

function nextQ() {
  if (G.n >= G.total) return winner();
  let q, tries = 0;
  do { q = GAMES[G.game].make(); tries++; } while (q.q + q.right === G.last && tries < 10);
  G.last = q.q + q.right;
  G.q = q; G.done = false;
  drawQ();
}

function drawQ() {
  const q = G.q, team = G.teams[G.turn];
  const shapes = ["▲", "◆", "●", "■"];
  view().innerHTML = `${board()}
    <div class="turnbar team t${G.turn}">🎯 ${esc(team.name)}'s turn · Question ${G.n + 1} of ${G.total}</div>
    <div class="battle-q">${esc(q.q)}${q.fig ? pic(q.fig) : ""}</div>
    <div class="opts" style="margin-top:12px">${q.options.map((o, i) => `<button class="opt c${i}" data-o="${esc(o)}"><span class="shape">${shapes[i]}</span> <span>${esc(o)}${OPT_TH[o] ? `<span class="th">${OPT_TH[o]}</span>` : ""}</span></button>`).join("")}</div>
    <div id="res"></div>
    <div class="btnrow"><button class="linkbtn" id="quitG">⬅ Back to the game list</button></div>`;
  view().querySelectorAll(".opt").forEach(b => b.onclick = () => answer(b.dataset.o));
  document.getElementById("quitG").onclick = gamesMenu;
}

function answer(o) {
  if (G.done) return;
  G.done = true;
  const ok = o === G.q.right;
  if (ok) G.teams[G.turn].pts++;
  view().querySelectorAll(".opt").forEach(b => { b.disabled = true; if (b.dataset.o === G.q.right) b.classList.add("right"); else b.classList.add("dim"); });
  view().querySelector(".scoreboard").outerHTML = board();
  document.getElementById("res").innerHTML = `<div class="result ${ok ? "ok" : "no"}">${ok ? "✅ Right! +1 point · ถูกต้อง! ได้ 1 คะแนน" : `❌ Not this time. The answer is ${esc(G.q.right)}.`}<div class="small">${esc(G.q.why)}</div></div>
    <div class="btnrow"><button class="bigbtn dark" id="nextG">${G.n + 1 >= G.total ? "🏆 See the winner · ดูผู้ชนะ" : "Next team ➡ · ทีมต่อไป"}</button></div>`;
  document.getElementById("nextG").onclick = () => { G.n++; G.turn = (G.turn + 1) % G.teams.length; nextQ(); };
  document.getElementById("nextG").focus();
}

function winner() {
  const top = Math.max(...G.teams.map(t => t.pts));
  const w = G.teams.filter(t => t.pts === top).map(t => esc(t.name));
  view().innerHTML = `${board()}<div class="panel"><div class="winner">🏆 ${w.length > 1 ? "It's a tie! " + w.join(" and ") : w[0] + " wins!"} 🎉</div>
    <div class="btnrow"><button class="bigbtn dark" id="again">🔁 Play again</button><button class="bigbtn" id="menuG">🎮 Another game</button></div></div>`;
  document.getElementById("again").onclick = () => { G.teams.forEach(t => t.pts = 0); G.n = 0; G.turn = 0; nextQ(); };
  document.getElementById("menuG").onclick = gamesMenu;
}

// ---------- page ----------
let mode = "lesson";
function setMode(m) {
  mode = m;
  document.querySelectorAll("#modeTabs button").forEach(b => b.classList.toggle("on", b.dataset.m === m));
  if (m === "lesson") lesson(); else gamesMenu();
  window.scrollTo(0, 0);
}
document.querySelectorAll("#modeTabs button").forEach(b => b.onclick = () => setMode(b.dataset.m));
document.addEventListener("keydown", e => {
  if (mode !== "lesson" || e.target.tagName === "INPUT") return;
  if (e.key === "ArrowRight" && cur < SLIDES.length - 1) { cur++; lesson(); }
  if (e.key === "ArrowLeft" && cur > 0) { cur--; lesson(); }
});
renderStudentBar();
setMode(location.hash === "#games" ? "games" : "lesson");
