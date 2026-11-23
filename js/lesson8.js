// Unit 8 lesson slides (very simple steps, English and Thai) and easy class games for the projector.
// The pictures come from content/unit08.json, so they are the same pictures as the Unit 8 page.

const view = () => document.getElementById("view");
const pic = spec => (spec ? `<div class="pic">${Diagram.render(spec)}</div>` : "");
const TH = (en, th) => (th ? `${en}<span class="th">${th}</span>` : en);
let U8 = null;
// "L0.4" = section 0, Learn card 4. "Q0.6" = section 0, question 6.
function fg(ref) {
  if (!U8 || !ref) return null;
  const m = ref.match(/^([LQ])(\d+)\.(\d+)$/);
  const s = U8.sections[+m[2]];
  return (m[1] === "L" ? s.learn : s.questions)[+m[3]].fig;
}

// ---------- the lesson (follows the book: 8.1, 8.2, Challenge) ----------
const SECS = ["8.1 Solid shapes", "8.2 Nets of solids", "⭐ Faces, edges, vertices"];
const SEC_TH = ["8.1 รูปทรงสามมิติ", "8.2 รูปคลี่", "⭐ หน้า ขอบ จุดยอด"];
const SLIDES = [
  { s: 0, e: "🧊", p: 48, f: "L0.0", t: "Flat shapes and solid shapes", tt: "รูปแบนและรูปทรงสามมิติ",
    h: "<p>A square is <b>flat</b>. You can draw it on paper.</p><p>A box is <b>solid</b>. You can hold it in your hand. ✋</p><p>Solid shapes have <span class='word'>faces</span>, <span class='word'>edges</span> and <span class='word'>vertices</span> (corners).</p>",
    th: "สี่เหลี่ยมจัตุรัสเป็นรูปแบน วาดบนกระดาษได้ กล่องเป็นรูปทรงสามมิติ ถือไว้ในมือได้ รูปทรงสามมิติมีหน้า ขอบ และจุดยอด (มุม)" },
  { s: 0, e: "🎲", p: 48, f: "L0.0", t: "Cube", tt: "ลูกบาศก์",
    h: "<p>A <span class='word'>cube</span> has <b>6 faces</b>.</p><p>Every face is a <b>square</b>, all the same size.</p><p>Like a dice! 🎲</p>",
    th: "ลูกบาศก์มี 6 หน้า ทุกหน้าเป็นรูปสี่เหลี่ยมจัตุรัสขนาดเท่ากัน เหมือนลูกเต๋า!",
    a: "How many faces does a dice have?", at: "ลูกเต๋ามีกี่หน้า", n: "6 faces", nt: "6 หน้า" },
  { s: 0, e: "🧃", p: 48, f: "L0.2", t: "Cuboid", tt: "ทรงสี่เหลี่ยมมุมฉาก",
    h: "<p>A <span class='word'>cuboid</span> also has <b>6 faces</b>.</p><p>The faces are <b>rectangles</b> (or 4 rectangles and 2 squares).</p><p>Like a juice box! 🧃</p>",
    th: "ทรงสี่เหลี่ยมมุมฉากก็มี 6 หน้า หน้าเป็นรูปสี่เหลี่ยมผืนผ้า (หรือสี่เหลี่ยมผืนผ้า 4 หน้าและสี่เหลี่ยมจัตุรัส 2 หน้า) เหมือนกล่องน้ำผลไม้!" },
  { s: 0, e: "🍦", p: 49, f: "L0.4", t: "Cone", tt: "กรวย",
    h: "<p>A <span class='word'>cone</span> has:</p><p>🔵 <b>1 flat face</b> (a circle)</p><p>〰️ <b>1 curved face</b></p><p>📍 <b>1 vertex</b> (the point)</p>",
    th: "กรวยมีหน้าแบน 1 หน้า (วงกลม) หน้าโค้ง 1 หน้า และจุดยอด 1 จุด (ปลายแหลม)",
    a: "An ice cream cone and a party hat 🎉 are which solid?", at: "โคนไอศกรีมและหมวกงานเลี้ยงเป็นรูปทรงอะไร", n: "A cone", nt: "กรวย" },
  { s: 0, e: "🥫", p: 49, f: "L0.6", t: "Cylinder", tt: "ทรงกระบอก",
    h: "<p>A <span class='word'>cylinder</span> has:</p><p>🔵🔵 <b>2 flat faces</b> (circles, top and bottom)</p><p>〰️ <b>1 curved face</b> (round the side)</p><p>Like a can of drink! 🥫</p>",
    th: "ทรงกระบอกมีหน้าแบน 2 หน้า (วงกลม ด้านบนและด้านล่าง) และหน้าโค้ง 1 หน้า (รอบด้านข้าง) เหมือนกระป๋องน้ำ!" },
  { s: 0, e: "⚽", p: 50, f: "L0.8", t: "Sphere", tt: "ทรงกลม",
    h: "<p>A <span class='word'>sphere</span> is round all over.</p><p>It has <b>no flat face</b> at all.</p><p>Like a ball! ⚽ Half a sphere is a <b>hemisphere</b>.</p>",
    th: "ทรงกลมกลมทุกด้าน ไม่มีหน้าแบนเลย เหมือนลูกบอล! ครึ่งหนึ่งของทรงกลมเรียกว่าครึ่งทรงกลม",
    a: "Which solid has no flat face?", at: "รูปทรงใดไม่มีหน้าแบน", n: "A sphere", nt: "ทรงกลม" },
  { s: 0, e: "🔺", p: 50, f: "L0.10", t: "Pyramid", tt: "พีระมิด",
    h: "<p>A <span class='word'>pyramid</span> has a flat <b>base</b>.</p><p>All the other faces are <b>triangles</b>.</p><p>The triangles meet at <b>one point</b> at the top: the <b>vertex</b>.</p>",
    th: "พีระมิดมีฐานแบน หน้าอื่นทั้งหมดเป็นรูปสามเหลี่ยม สามเหลี่ยมมาพบกันที่จุดเดียวด้านบน คือจุดยอด" },
  { s: 0, e: "🏷️", p: 50, f: "L0.11", t: "Naming pyramids", tt: "การเรียกชื่อพีระมิด",
    h: "<p>Look at the <b>base</b>. The base gives the name!</p><p>Square base ➡ <b>square pyramid</b></p><p>Triangle base ➡ <b>triangular pyramid</b></p>",
    th: "ดูที่ฐาน ฐานบอกชื่อ! ฐานสี่เหลี่ยมจัตุรัส ➡ พีระมิดฐานสี่เหลี่ยมจัตุรัส ฐานสามเหลี่ยม ➡ พีระมิดฐานสามเหลี่ยม",
    a: "The base is a hexagon. What is the pyramid called?", at: "ฐานเป็นรูปหกเหลี่ยม พีระมิดนี้ชื่ออะไร", n: "A hexagonal pyramid", nt: "พีระมิดฐานหกเหลี่ยม" },
  { s: 0, e: "🍫", p: 50, f: "L0.13", t: "Prism", tt: "ปริซึม",
    h: "<p>A <span class='word'>prism</span> has the <b>same shape at both ends</b>.</p><p>The faces in between are <b>rectangles</b>.</p><p>Triangle ends ➡ <b>triangular prism</b>, like a Toblerone box.</p>",
    th: "ปริซึมมีรูปร่างเหมือนกันที่ปลายทั้งสองข้าง หน้าที่อยู่ระหว่างกลางเป็นรูปสี่เหลี่ยมผืนผ้า ปลายเป็นสามเหลี่ยม ➡ ปริซึมสามเหลี่ยม เหมือนกล่อง Toblerone",
    a: "Both ends are pentagons. What is the solid called?", at: "ปลายทั้งสองเป็นรูปห้าเหลี่ยม รูปทรงนี้ชื่ออะไร", n: "A pentagonal prism", nt: "ปริซึมห้าเหลี่ยม" },

  { s: 1, e: "📦", p: 54, f: "L1.0", t: "What is a net?", tt: "รูปคลี่คืออะไร",
    h: "<p>Cut a box along some edges. ✂️</p><p>Open it out <b>flat</b>.</p><p>The flat shape is called a <span class='word'>net</span>. Fold it up again and you get the box back!</p>",
    th: "ตัดกล่องตามขอบบางขอบ แล้วคลี่ออกให้แบน รูปแบนนั้นเรียกว่ารูปคลี่ พับกลับขึ้นมาก็จะได้กล่องเหมือนเดิม!" },
  { s: 1, e: "🎲", p: 54, f: "L1.1", t: "Net of a cube", tt: "รูปคลี่ของลูกบาศก์",
    h: "<p>A cube net has <b>6 squares</b>.</p><p>Each square becomes one face.</p><p>Fold the 4 sides up around the bottom, then close the lid.</p>",
    th: "รูปคลี่ของลูกบาศก์มีสี่เหลี่ยมจัตุรัส 6 รูป แต่ละรูปกลายเป็นหนึ่งหน้า พับ 4 ด้านขึ้นรอบฐาน แล้วปิดฝา",
    a: "How many squares are in a net of a cube?", at: "รูปคลี่ของลูกบาศก์มีสี่เหลี่ยมจัตุรัสกี่รูป", n: "6 squares", nt: "6 รูป" },
  { s: 1, e: "🤔", p: 54, f: "L1.3", t: "Does every 6 squares work?", tt: "สี่เหลี่ยม 6 รูปใช้ได้ทุกแบบหรือไม่",
    h: "<p><b>No!</b> Fold it in your head. 🧠</p><p>If 2 squares land on the <b>same face</b>, it is <b>not</b> a cube net.</p><p>A cube has 11 different nets.</p>",
    th: "ไม่! ลองพับในใจ ถ้ามีสี่เหลี่ยม 2 รูปไปทับหน้าเดียวกัน ก็ไม่ใช่รูปคลี่ของลูกบาศก์ ลูกบาศก์มีรูปคลี่ต่างกัน 11 แบบ" },
  { s: 1, e: "🧃", p: 55, f: "L1.4", t: "Net of a cuboid", tt: "รูปคลี่ของทรงสี่เหลี่ยมมุมฉาก",
    h: "<p>A cuboid net has <b>6 rectangles</b>.</p><p>They come in <b>3 pairs</b>: top and bottom, front and back, 2 ends.</p>",
    th: "รูปคลี่ของทรงสี่เหลี่ยมมุมฉากมีสี่เหลี่ยมผืนผ้า 6 รูป เป็นคู่ 3 คู่: บนกับล่าง หน้ากับหลัง และปลาย 2 ข้าง" },
  { s: 1, e: "🍫", p: 55, f: "L1.7", t: "Net of a triangular prism", tt: "รูปคลี่ของปริซึมสามเหลี่ยม",
    h: "<p><b>3 rectangles</b> in a strip.</p><p><b>2 triangles</b>, one at each end (on opposite sides).</p><p>Roll the strip into a tube, then close the ends.</p>",
    th: "สี่เหลี่ยมผืนผ้า 3 รูปเรียงเป็นแถบ สามเหลี่ยม 2 รูป ปลายละหนึ่งรูป (อยู่คนละด้าน) ม้วนแถบเป็นท่อ แล้วปิดปลาย",
    a: "How many rectangles are in this net?", at: "รูปคลี่นี้มีสี่เหลี่ยมผืนผ้ากี่รูป", n: "3 rectangles", nt: "3 รูป" },
  { s: 1, e: "🔺", p: 56, f: "L1.8", t: "Net of a pyramid", tt: "รูปคลี่ของพีระมิด",
    h: "<p>The <b>base</b> is in the middle.</p><p>A <b>triangle</b> is on every edge of the base.</p><p>Fold the triangles up. They meet at the vertex. 📍</p>",
    th: "ฐานอยู่ตรงกลาง มีสามเหลี่ยมติดอยู่ทุกขอบของฐาน พับสามเหลี่ยมขึ้น จะพบกันที่จุดยอด",
    a: "The base is a square. How many triangles does the net have?", at: "ฐานเป็นสี่เหลี่ยมจัตุรัส รูปคลี่มีสามเหลี่ยมกี่รูป", n: "4 triangles (1 for each side of the square)", nt: "4 รูป (ด้านละ 1 รูป)" },
  { s: 1, e: "🥫", p: 57, f: "L1.10", t: "Net of a cylinder", tt: "รูปคลี่ของทรงกระบอก",
    h: "<p><b>1 rectangle</b>: the curved side, rolled flat.</p><p><b>2 circles</b>: the top and the bottom.</p>",
    th: "สี่เหลี่ยมผืนผ้า 1 รูป: ด้านข้างที่โค้ง คลี่ให้แบน วงกลม 2 รูป: ด้านบนและด้านล่าง" },
  { s: 1, e: "🎉", p: 57, f: "L1.11", t: "Net of a cone", tt: "รูปคลี่ของกรวย",
    h: "<p><b>1 fan shape</b>: roll it into a party hat. 🎉</p><p><b>1 circle</b>: the base.</p>",
    th: "รูปพัด 1 รูป: ม้วนให้เป็นหมวกงานเลี้ยง วงกลม 1 รูป: ฐาน",
    a: "A net has a fan shape and 1 circle. Which solid?", at: "รูปคลี่มีรูปพัดและวงกลม 1 รูป เป็นรูปทรงอะไร", n: "A cone", nt: "กรวย" },

  { s: 2, e: "🔢", p: 65, f: "L0.0", t: "Faces, edges and vertices", tt: "หน้า ขอบ และจุดยอด",
    h: "<p><span class='word'>Face</span>: a flat side.</p><p><span class='word'>Edge</span>: where 2 faces meet (a line).</p><p><span class='word'>Vertex</span>: a corner point.</p><p>A cube: <b>6</b> faces, <b>12</b> edges, <b>8</b> vertices.</p>",
    th: "หน้า: ด้านที่แบน ขอบ: ที่ที่หน้า 2 หน้ามาพบกัน (เป็นเส้น) จุดยอด: จุดที่เป็นมุม ลูกบาศก์: 6 หน้า 12 ขอบ 8 จุดยอด" },
  { s: 2, e: "✨", p: 65, f: "L2.1", t: "A magic rule", tt: "กฎมหัศจรรย์",
    h: "<p>Faces + vertices - edges = <b>2</b></p><p>Cube: 6 + 8 - 12 = 2 ✓</p><p>Triangular prism: 5 + 6 - 9 = 2 ✓</p>",
    th: "หน้า + จุดยอด - ขอบ = 2 ลูกบาศก์: 6 + 8 - 12 = 2 ✓ ปริซึมสามเหลี่ยม: 5 + 6 - 9 = 2 ✓",
    a: "A square pyramid has 5 faces and 5 vertices. How many edges?", at: "พีระมิดฐานสี่เหลี่ยมจัตุรัสมี 5 หน้าและ 5 จุดยอด มีกี่ขอบ", n: "8 edges (4 around the base and 4 going up). 5 + 5 - 8 = 2 ✓", nt: "8 ขอบ (รอบฐาน 4 และขึ้นไปยอด 4) 5 + 5 - 8 = 2 ✓" },
  { s: 2, e: "🎉", p: 70, t: "Great job! Time to play", tt: "เก่งมาก! ได้เวลาเล่นเกมแล้ว",
    h: "<p>Solids: cube, cuboid, cone, cylinder, sphere, pyramid, prism.</p><p>Nets: fold them in your head!</p><p><button class='bigbtn dark' id='goGames'>🎮 Play the class games</button></p>",
    th: "รูปทรง: ลูกบาศก์ ทรงสี่เหลี่ยมมุมฉาก กรวย ทรงกระบอก ทรงกลม พีระมิด ปริซึม รูปคลี่: ลองพับในใจ!" },
];

let cur = 0;
function lesson() {
  const sl = SLIDES[cur];
  view().innerHTML = `
    <div class="jump">${SECS.map((t, i) => `<button data-s="${i}" class="${sl.s === i ? "on" : ""}">${TH(t, SEC_TH[i])}</button>`).join("")}</div>
    <div class="slide">
      <span class="sec">${SECS[sl.s]} · ${SEC_TH[sl.s]}</span> <span class="badge">📖 p.${sl.p}</span>
      <h2>${sl.e} ${TH(sl.t, sl.tt)}</h2>
      <div class="two"><div class="big">${sl.h}<p class="th">${sl.th}</p></div>${sl.f ? pic(fg(sl.f)) : "<div></div>"}</div>
      ${sl.a ? `<div class="turn">🙋 Your turn: ${TH(sl.a, "ถึงตาเธอ: " + sl.at)}<div class="reveal"><button class="bigbtn" id="reveal">${TH("👀 Show answer", "ดูคำตอบ")}</button></div></div>` : ""}
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
  if (rv) rv.onclick = () => { rv.parentElement.outerHTML = `<div class="ans">✅ ${TH(sl.n, sl.nt)}</div>`; };
  const gg = document.getElementById("goGames");
  if (gg) gg.onclick = () => setMode("games");
}

// ---------- games ----------
const pick = arr => arr[Math.floor(Math.random() * arr.length)];
function opts(right, wrongs) {
  const o = [right];
  for (const w of shuffle(wrongs)) if (!o.includes(w) && o.length < 4) o.push(w);
  return shuffle(o);
}
const SOLIDS = ["Cube", "Cuboid", "Cone", "Cylinder", "Sphere", "Pyramid", "Prism"];
const OPT_TH = { Cube: "ลูกบาศก์", Cuboid: "ทรงสี่เหลี่ยมมุมฉาก", Cone: "กรวย", Cylinder: "ทรงกระบอก", Sphere: "ทรงกลม", Pyramid: "พีระมิด", Prism: "ปริซึม",
  "👍 True": "จริง", "👎 False": "เท็จ" };
const WHY = {
  Cube: "6 square faces, all the same size.", Cuboid: "6 rectangle faces.", Cone: "1 circle face, 1 curved face and 1 point.",
  Cylinder: "2 circle faces and 1 curved face.", Sphere: "Round all over, no flat face.", Pyramid: "A base with triangles that meet at one point.",
  Prism: "The same shape at both ends, rectangles in between.",
};
// Pictures of solids and objects (all from the Unit 8 page) and their right answers
const PICS = [["L0.0", "Cube"], ["L0.2", "Cuboid"], ["L0.4", "Cone"], ["L0.6", "Cylinder"], ["L0.8", "Sphere"], ["L0.10", "Pyramid"], ["L0.13", "Prism"],
  ["Q0.0", "Pyramid"], ["Q0.1", "Cylinder"], ["Q0.2", "Sphere"], ["Q0.3", "Prism"], ["Q0.4", "Sphere"], ["Q0.5", "Cone"], ["Q0.6", "Cylinder"], ["Q0.7", "Cylinder"], ["Q0.8", "Pyramid"]];
const NETS = [["L1.1", "Cube"], ["L1.4", "Cuboid"], ["L1.7", "Prism"], ["L1.8", "Pyramid"], ["L1.9", "Pyramid"], ["L1.10", "Cylinder"], ["L1.11", "Cone"]];
const CLUES = [
  ["2 circle faces and 1 curved face", "หน้าวงกลม 2 หน้าและหน้าโค้ง 1 หน้า", "Cylinder"],
  ["1 circle face, 1 curved face and 1 point", "หน้าวงกลม 1 หน้า หน้าโค้ง 1 หน้า และปลายแหลม 1 จุด", "Cone"],
  ["Round all over, no flat face", "กลมทุกด้าน ไม่มีหน้าแบน", "Sphere"],
  ["6 square faces, all the same size", "หน้าสี่เหลี่ยมจัตุรัส 6 หน้า ขนาดเท่ากันทุกหน้า", "Cube"],
  ["6 rectangle faces", "หน้าสี่เหลี่ยมผืนผ้า 6 หน้า", "Cuboid"],
  ["A square base and 4 triangles that meet at the top", "ฐานสี่เหลี่ยมจัตุรัสและสามเหลี่ยม 4 รูปที่พบกันด้านบน", "Pyramid"],
  ["2 triangle ends and 3 rectangles", "ปลายเป็นสามเหลี่ยม 2 ข้างและสี่เหลี่ยมผืนผ้า 3 รูป", "Prism"],
  ["Like a can of drink", "เหมือนกระป๋องน้ำ", "Cylinder"],
  ["Like a party hat", "เหมือนหมวกงานเลี้ยง", "Cone"],
  ["Like a dice", "เหมือนลูกเต๋า", "Cube"],
  ["Like a football", "เหมือนลูกฟุตบอล", "Sphere"],
];
// Faces, edges and vertices (checked: faces + vertices - edges = 2 for every one)
const COUNTS = [
  ["cube", "ลูกบาศก์", 6, 12, 8], ["cuboid", "ทรงสี่เหลี่ยมมุมฉาก", 6, 12, 8], ["triangular prism", "ปริซึมสามเหลี่ยม", 5, 9, 6],
  ["square pyramid", "พีระมิดฐานสี่เหลี่ยมจัตุรัส", 5, 8, 5], ["triangular pyramid", "พีระมิดฐานสามเหลี่ยม", 4, 6, 4],
  ["pentagonal prism", "ปริซึมห้าเหลี่ยม", 7, 15, 10], ["hexagonal pyramid", "พีระมิดฐานหกเหลี่ยม", 7, 12, 7],
];
const COUNT_PIC = { cube: "L0.0", cuboid: "L0.2", "triangular prism": "L0.13", "square pyramid": "L0.10" };

const GAMES = {
  name: { e: "🔍", name: "Name the solid", th: "ทายชื่อรูปทรง", desc: "Look at the picture. Which solid is it?", make() {
    const [ref, right] = pick(PICS);
    return { q: "Which solid is this? · นี่คือรูปทรงอะไร", fig: fg(ref), options: opts(right, SOLIDS), right, why: WHY[right] };
  } },
  clue: { e: "🕵️", name: "Clue detective", th: "นักสืบคำใบ้", desc: "Read the clue. Which solid is it?", make() {
    const [en, th, right] = pick(CLUES);
    return { q: `Clue: ${en} · คำใบ้: ${th}`, options: opts(right, SOLIDS), right, why: WHY[right] };
  } },
  net: { e: "📦", name: "Fold the net", th: "พับรูปคลี่", desc: "Which solid does this net make?", make() {
    const [ref, right] = pick(NETS);
    return { q: "Fold it in your head. Which solid does this net make? · พับในใจ รูปคลี่นี้พับได้รูปทรงอะไร", fig: fg(ref), options: opts(right, SOLIDS), right, why: WHY[right] };
  } },
  count: { e: "🔢", name: "Count it", th: "นับดู", desc: "Faces, edges or vertices?", make() {
    const [en, th, f, e, v] = pick(COUNTS);
    const k = pick(["faces", "edges", "vertices"]);
    const val = { faces: f, edges: e, vertices: v }[k];
    const kth = { faces: "หน้า", edges: "ขอบ", vertices: "จุดยอด" }[k];
    const right = String(val);
    return { q: `How many ${k} does a ${en} have? · ${th}มีกี่${kth}`, fig: COUNT_PIC[en] ? fg(COUNT_PIC[en]) : null,
      options: opts(right, [val - 1, val + 1, val + 2, val - 2, f, e, v].filter(x => x > 0).map(String)), right,
      why: `A ${en} has ${f} faces, ${e} edges and ${v} vertices. ${f} + ${v} - ${e} = 2.` };
  } },
  tf: { e: "👍", name: "True or false?", th: "จริงหรือเท็จ", desc: "Thumbs up or thumbs down!", make() {
    const [s, t, why] = pick(TF);
    return { q: s, options: ["👍 True", "👎 False"], right: t ? "👍 True" : "👎 False", why };
  } },
};
const TF = [
  ["A cube has 6 faces. · ลูกบาศก์มี 6 หน้า", true, "Top, bottom, front, back, left and right."],
  ["A sphere has 1 flat face. · ทรงกลมมีหน้าแบน 1 หน้า", false, "A sphere has no flat face."],
  ["A cylinder has 2 circle faces. · ทรงกระบอกมีหน้าวงกลม 2 หน้า", true, "One at the top and one at the bottom."],
  ["A cone has 2 vertices. · กรวยมีจุดยอด 2 จุด", false, "A cone has 1 vertex, the point."],
  ["A pyramid's triangles meet at one point. · สามเหลี่ยมของพีระมิดพบกันที่จุดเดียว", true, "That point is the vertex."],
  ["A prism has the same shape at both ends. · ปริซึมมีรูปร่างเหมือนกันที่ปลายทั้งสองข้าง", true, "Like a Toblerone box."],
  ["A net of a cube has 5 squares. · รูปคลี่ของลูกบาศก์มีสี่เหลี่ยมจัตุรัส 5 รูป", false, "It has 6 squares, one for each face."],
  ["A net of a cylinder has a rectangle and 2 circles. · รูปคลี่ของทรงกระบอกมีสี่เหลี่ยมผืนผ้าและวงกลม 2 รูป", true, "The rectangle rolls into the curved side."],
  ["Any 6 squares joined together make a cube net. · สี่เหลี่ยมจัตุรัส 6 รูปต่อกันแบบไหนก็เป็นรูปคลี่ของลูกบาศก์", false, "Not always! 2 squares might land on the same face."],
  ["A cube has 12 edges. · ลูกบาศก์มี 12 ขอบ", true, "4 on top, 4 on the bottom and 4 going up."],
  ["A cube has 6 vertices. · ลูกบาศก์มีจุดยอด 6 จุด", false, "It has 8 vertices: 4 on top and 4 on the bottom."],
  ["A pyramid's name comes from its base. · ชื่อของพีระมิดมาจากฐาน", true, "Square base: square pyramid."],
];

let G = null;   // { game, teams:[{name, pts}], turn, n, total, q, done }
let gPick = "name", nTeams = 2;
function gamesMenu() {
  view().innerHTML = `
    <div class="panel"><h2>🎮 Pick a game · เลือกเกม</h2>
      <div class="games">${Object.entries(GAMES).map(([id, g]) => `<button class="gcard ${id === gPick ? "on" : ""}" data-g="${id}"><div class="gt">${g.e} ${g.name} · ${g.th}</div>${g.desc}</button>`).join("")}</div>
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
fetch("content/unit08.json", { cache: "no-cache" }).then(r => r.json()).then(d => { U8 = d; setMode(location.hash === "#games" ? "games" : "lesson"); })
  .catch(() => { view().innerHTML = `<div class="panel"><p>Could not load Unit 8. Please check the internet and reload.</p></div>`; });
