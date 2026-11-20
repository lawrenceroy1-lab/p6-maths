// ============================================================
//  SITE SETTINGS  (T. Roy: this is the only file you edit)
// ============================================================

// Paste your Google Apps Script web app URL between the quotes.
// Leave it empty ("") and scores are only saved in the browser.
const SHEET_URL = "";

// Units shown on the home page. "ready: true" means the data file exists.
const UNITS = [
  { id: "07", title: "2D Shapes",                        pages: "p.1 to 46",   icon: "🔺", ready: true  },
  { id: "08", title: "3D Shapes",                        pages: "p.47 to 70",  icon: "🧊", ready: true  },
  { id: "09", title: "Perimeter and Area of Triangles",  pages: "p.71 to 104", icon: "📐", ready: true  },
  { id: "10", title: "Area and Perimeter of Polygons",   pages: "p.105 to 146",icon: "⬟",  ready: true  },
  { id: "11", title: "Circumference and Area of Circles",pages: "p.147 to 180",icon: "⭕", ready: false },
  { id: "12", title: "Volume and Capacity",              pages: "p.181 to 214",icon: "🥤", ready: false },
  { id: "13", title: "Patterns",                         pages: "p.215 to 230",icon: "🔢", ready: false },
  { id: "14", title: "Presentation of Data",             pages: "p.231 to 244",icon: "🥧", ready: false },
  { id: "review", title: "Review",                       pages: "p.245 to 264",icon: "⭐", ready: false }
];

const CLASSES = ["6/1", "6/2", "6/3"];
