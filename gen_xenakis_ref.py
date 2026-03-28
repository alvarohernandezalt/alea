#!/usr/bin/env python3
"""Generate Xenakis -> Parameters technical reference PDF with vector diagrams."""

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import (
    Drawing, Rect, Line, String, Circle, Polygon, PolyLine, Group,
)

# ── Colors ──
C_DIST = HexColor("#2563EB")
C_MARKOV = HexColor("#16A34A")
C_SIEVE = HexColor("#EA580C")
C_WALK = HexColor("#9333EA")
C_BG_DIST = HexColor("#DBEAFE")
C_BG_MARKOV = HexColor("#DCFCE7")
C_BG_SIEVE = HexColor("#FFEDD5")
C_BG_WALK = HexColor("#F3E8FF")
C_GRAY = HexColor("#F3F4F6")
C_DARK = HexColor("#1F2937")
C_MED = HexColor("#6B7280")
C_LGRAY = HexColor("#E5E7EB")
C_DGRAY = HexColor("#4B5563")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
USABLE_W = PAGE_W - 2 * MARGIN

styles = getSampleStyleSheet()

s_title = ParagraphStyle("XT", parent=styles["Title"], fontSize=22, leading=26,
                          textColor=C_DARK, spaceAfter=4*mm)
s_subtitle = ParagraphStyle("XS", parent=styles["Normal"], fontSize=11, leading=14,
                             textColor=C_MED, spaceAfter=8*mm, alignment=TA_CENTER)
s_h1 = ParagraphStyle("XH1", parent=styles["Heading1"], fontSize=15, leading=18,
                       textColor=C_DARK, spaceBefore=6*mm, spaceAfter=3*mm)
s_h2 = ParagraphStyle("XH2", parent=styles["Heading2"], fontSize=12, leading=15,
                       textColor=C_DARK, spaceBefore=4*mm, spaceAfter=2*mm)
s_body = ParagraphStyle("XB", parent=styles["Normal"], fontSize=9, leading=12,
                         textColor=C_DARK, spaceAfter=2*mm, alignment=TA_JUSTIFY)
s_caption = ParagraphStyle("XCap", parent=styles["Normal"], fontSize=8, leading=10,
                            textColor=C_MED, alignment=TA_CENTER,
                            spaceAfter=3*mm, spaceBefore=1*mm)
s_cell = ParagraphStyle("XCell", parent=styles["Normal"], fontSize=7.5, leading=10,
                         textColor=C_DARK)
s_cell_bold = ParagraphStyle("XCB", parent=s_cell, fontName="Helvetica-Bold")
s_cell_header = ParagraphStyle("XCH", parent=s_cell, fontName="Helvetica-Bold",
                                textColor=white)


def P(t, s=s_cell):
    return Paragraph(t, s)

def PH(t):
    return Paragraph(t, s_cell_header)

def PB(t):
    return Paragraph(t, s_cell_bold)


def make_table(headers, rows, col_pcts, header_color=C_DARK):
    cw = [USABLE_W * p / 100 for p in col_pcts]
    data = [[PH(h) for h in headers]]
    for r in rows:
        data.append([P(str(c)) if not isinstance(c, Paragraph) else c for c in r])
    t = Table(data, colWidths=cw, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D1D5DB")),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), C_GRAY))
    t.setStyle(TableStyle(cmds))
    return t


# ─────────────────────────────────────────────
# VECTOR DIAGRAM HELPERS
# ─────────────────────────────────────────────

def _arrow_head(d, x, y, direction, size=6, color=black):
    """Draw a triangular arrow head. direction: 'down','up','right','left'."""
    s = size
    if direction == "down":
        d.add(Polygon(points=[x, y, x - s, y + s*1.5, x + s, y + s*1.5],
                       fillColor=color, strokeColor=color))
    elif direction == "up":
        d.add(Polygon(points=[x, y, x - s, y - s*1.5, x + s, y - s*1.5],
                       fillColor=color, strokeColor=color))
    elif direction == "right":
        d.add(Polygon(points=[x, y, x - s*1.5, y - s, x - s*1.5, y + s],
                       fillColor=color, strokeColor=color))
    elif direction == "left":
        d.add(Polygon(points=[x, y, x + s*1.5, y - s, x + s*1.5, y + s],
                       fillColor=color, strokeColor=color))


def draw_box(d, x, y, w, h, text, fill, stroke=C_DARK, font_size=8, text_color=None):
    """Rounded rect with centered text."""
    d.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    if text_color is None:
        # Auto: dark text on light bg, white on dark bg
        r, g, b = fill.red, fill.green, fill.blue
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = C_DARK if lum > 0.5 else white
    d.add(String(x + w / 2, y + h / 2 - font_size * 0.35, text,
                 textAnchor="middle", fontSize=font_size, fontName="Helvetica-Bold",
                 fillColor=text_color))


def draw_arrow_v(d, x, y1, y2, color=C_DARK):
    """Vertical arrow from y1 down to y2."""
    d.add(Line(x, y1, x, y2 + 8, strokeColor=color, strokeWidth=1.5))
    _arrow_head(d, x, y2, "down", color=color)


def draw_arrow_h(d, x1, x2, y, color=C_DARK):
    """Horizontal arrow from x1 to x2."""
    d.add(Line(x1, y, x2 - 8, y, strokeColor=color, strokeWidth=1.5))
    _arrow_head(d, x2, y, "right", color=color)


# ─────────────────────────────────────────────
# DIAGRAM BUILDERS
# ─────────────────────────────────────────────

def diagram_architecture():
    """Section 1: 3-layer architecture flowchart."""
    W = USABLE_W
    H = 210
    d = Drawing(W, H)

    # Background
    d.add(Rect(0, 0, W, H, fillColor=HexColor("#FAFAFA"), strokeColor=C_LGRAY, strokeWidth=0.5))

    # Layer 1: ARRANGER
    bw, bh = 360, 36
    bx = (W - bw) / 2
    by = H - 48
    draw_box(d, bx, by, bw, bh, "ARRANGER  (strategy + constraints + sources)", C_DGRAY, font_size=9)

    # Arrows down from arranger to 3 boxes
    mid = W / 2
    y_mid = by - 50
    box_w = 130
    gap = 15
    total = box_w * 3 + gap * 2
    x_start = (W - total) / 2

    # Vertical lines from arranger
    for i in range(3):
        bxi = x_start + i * (box_w + gap) + box_w / 2
        d.add(Line(mid, by, mid, by - 12, strokeColor=C_DARK, strokeWidth=1.5))
        # Horizontal spread line
    d.add(Line(x_start + box_w / 2, by - 12, x_start + 2 * (box_w + gap) + box_w / 2, by - 12,
               strokeColor=C_DARK, strokeWidth=1.5))
    for i in range(3):
        bxi = x_start + i * (box_w + gap) + box_w / 2
        d.add(Line(bxi, by - 12, bxi, y_mid + 36 + 8, strokeColor=C_DARK, strokeWidth=1.5))
        _arrow_head(d, bxi, y_mid + 36, "down", color=C_DARK)

    # Layer 2: 3 technique boxes
    colors_mid = [C_BG_MARKOV, C_BG_SIEVE, C_BG_WALK]
    strokes_mid = [C_MARKOV, C_SIEVE, C_WALK]
    labels_mid = ["STRATEGY\n+ Cadenas Markov", "CRIBAS\n(filtro modular)", "RANDOM WALKS\n(modificador)"]
    for i in range(3):
        bxi = x_start + i * (box_w + gap)
        d.add(Rect(bxi, y_mid, box_w, 36, rx=4, ry=4,
                    fillColor=colors_mid[i], strokeColor=strokes_mid[i], strokeWidth=1.5))
        lines = labels_mid[i].split("\n")
        d.add(String(bxi + box_w / 2, y_mid + 22, lines[0],
                     textAnchor="middle", fontSize=8, fontName="Helvetica-Bold",
                     fillColor=strokes_mid[i]))
        d.add(String(bxi + box_w / 2, y_mid + 10, lines[1],
                     textAnchor="middle", fontSize=7, fillColor=strokes_mid[i]))

    # Arrows down to RNG
    y_bot = y_mid - 50
    for i in range(3):
        bxi = x_start + i * (box_w + gap) + box_w / 2
        d.add(Line(bxi, y_mid, bxi, y_mid - 12, strokeColor=C_DARK, strokeWidth=1.5))
    d.add(Line(x_start + box_w / 2, y_mid - 12, x_start + 2 * (box_w + gap) + box_w / 2, y_mid - 12,
               strokeColor=C_DARK, strokeWidth=1.5))
    d.add(Line(mid, y_mid - 12, mid, y_bot + 36 + 8, strokeColor=C_DARK, strokeWidth=1.5))
    _arrow_head(d, mid, y_bot + 36, "down", color=C_DARK)

    # Layer 3: ControlledRandom
    rw = 280
    rx = (W - rw) / 2
    d.add(Rect(rx, y_bot, rw, 36, rx=4, ry=4,
               fillColor=C_BG_DIST, strokeColor=C_DIST, strokeWidth=1.5))
    d.add(String(rx + rw / 2, y_bot + 22, "ControlledRandom",
                 textAnchor="middle", fontSize=9, fontName="Helvetica-Bold", fillColor=C_DIST))
    d.add(String(rx + rw / 2, y_bot + 10, "+ Distribuciones de Xenakis",
                 textAnchor="middle", fontSize=7, fillColor=C_DIST))

    return d


def diagram_distribution_curve(label, color, curve_fn, width=220, height=80):
    """Mini distribution curve graph."""
    d = Drawing(width, height)
    # Axes
    ox, oy = 30, 15
    gw, gh = width - 50, height - 30
    d.add(Line(ox, oy, ox, oy + gh, strokeColor=C_DARK, strokeWidth=0.8))
    d.add(Line(ox, oy, ox + gw, oy, strokeColor=C_DARK, strokeWidth=0.8))
    # Axis labels
    d.add(String(ox - 15, oy + gh / 2, "P(x)", textAnchor="middle", fontSize=6,
                 fillColor=C_MED, fontName="Helvetica"))
    d.add(String(ox + gw / 2, oy - 10, "x", textAnchor="middle", fontSize=6,
                 fillColor=C_MED, fontName="Helvetica"))

    # Curve
    n_points = 50
    pts = []
    for i in range(n_points):
        t = i / (n_points - 1)
        val = curve_fn(t)
        px = ox + t * gw
        py = oy + val * gh * 0.9
        pts.extend([px, py])
    d.add(PolyLine(pts, strokeColor=color, strokeWidth=2))

    # Fill under curve (light)
    fill_pts = [ox, oy] + pts + [ox + gw, oy]
    d.add(Polygon(fill_pts, fillColor=color, strokeColor=None, fillOpacity=0.15))

    # Label
    d.add(String(ox + gw / 2, oy + gh + 2, label, textAnchor="middle",
                 fontSize=8, fontName="Helvetica-Bold", fillColor=color))
    return d


def diagram_five_distributions():
    """Section 2: All 5 distribution curves side by side in 2 rows."""
    W = USABLE_W
    H = 195
    d = Drawing(W, H)

    cw, ch = W / 3 - 10, 82
    curves = [
        ("Exponencial", C_DIST, lambda t: math.exp(-3 * t)),
        ("Cauchy", C_DIST, lambda t: 1 / (1 + ((t - 0.5) * 6) ** 2) * 0.7),
        ("Weibull (k=0.5,1,3)", C_DIST, lambda t: max(0, 1.5 * math.exp(-1.5 * t)) if t > 0.01 else 1),
        ("Poisson (discreta)", C_DIST, None),  # special: bar chart
        ("Lineal crec./decrec.", C_DIST, None),  # special: two triangles
    ]

    positions = [
        (5, H - ch - 5), (W / 3 + 2, H - ch - 5), (2 * W / 3 - 2, H - ch - 5),
        (W / 6 - cw / 2 + 20, 5), (W / 2 + 20, 5),
    ]

    for idx, (label, color, fn) in enumerate(curves):
        px, py = positions[idx]
        ox, oy = px + 30, py + 15
        gw, gh = cw - 45, ch - 30

        # Background
        d.add(Rect(px, py, cw, ch, rx=4, ry=4, fillColor=HexColor("#F8FAFC"),
                    strokeColor=C_LGRAY, strokeWidth=0.5))
        # Axes
        d.add(Line(ox, oy, ox, oy + gh, strokeColor=C_DARK, strokeWidth=0.8))
        d.add(Line(ox, oy, ox + gw, oy, strokeColor=C_DARK, strokeWidth=0.8))
        # Label
        d.add(String(px + cw / 2, py + ch - 8, label, textAnchor="middle",
                     fontSize=7, fontName="Helvetica-Bold", fillColor=C_DIST))

        if idx == 3:  # Poisson bar chart
            bars = [0.14, 0.27, 0.27, 0.18, 0.09, 0.04, 0.01]
            bw = gw / (len(bars) * 1.5)
            for i, v in enumerate(bars):
                bx = ox + i * gw / len(bars) + 2
                bh = v * gh * 3
                d.add(Rect(bx, oy, bw, bh, fillColor=C_DIST, strokeColor=white, strokeWidth=0.5,
                            fillOpacity=0.6))
                d.add(String(bx + bw / 2, oy - 7, str(i), textAnchor="middle", fontSize=5,
                             fillColor=C_MED))
        elif idx == 4:  # Linear ascending + descending
            # Ascending triangle
            half = gw / 2 - 5
            pts_asc = [ox, oy, ox + half, oy, ox + half, oy + gh * 0.8]
            d.add(Polygon(pts_asc, fillColor=C_DIST, strokeColor=C_DIST, fillOpacity=0.2,
                          strokeWidth=1.5))
            d.add(String(ox + half / 2, oy + gh * 0.15, "crec.", textAnchor="middle",
                         fontSize=6, fillColor=C_DIST))
            # Descending triangle
            ox2 = ox + half + 10
            pts_desc = [ox2, oy + gh * 0.8, ox2 + half, oy + gh * 0.8, ox2, oy]
            d.add(Polygon(pts_desc, fillColor=C_DIST, strokeColor=C_DIST, fillOpacity=0.2,
                          strokeWidth=1.5))
            d.add(String(ox2 + half / 2, oy + gh * 0.15, "decrec.", textAnchor="middle",
                         fontSize=6, fillColor=C_DIST))
        else:
            # Continuous curve
            n_pts = 40
            pts = []
            for i in range(n_pts):
                t = i / (n_pts - 1)
                val = fn(t)
                pts.extend([ox + t * gw, oy + val * gh * 0.85])
            d.add(PolyLine(pts, strokeColor=C_DIST, strokeWidth=2))
            # Fill
            fill_pts = [ox, oy] + pts + [ox + gw, oy]
            d.add(Polygon(fill_pts, fillColor=C_DIST, strokeColor=None, fillOpacity=0.1))

            # Weibull extra curves
            if idx == 2:
                # k=1 (exponential) — dashed
                pts2 = []
                for i in range(n_pts):
                    t = i / (n_pts - 1)
                    val = math.exp(-2 * t) if t > 0.01 else 1
                    pts2.extend([ox + t * gw, oy + val * gh * 0.85])
                d.add(PolyLine(pts2, strokeColor=C_DIST, strokeWidth=1.5,
                               strokeDashArray=[4, 3]))
                # k=3 (bell-ish)
                pts3 = []
                for i in range(n_pts):
                    t = i / (n_pts - 1)
                    val = 3 * (t ** 2) * math.exp(-(t * 2.5) ** 3) * 2 if t > 0.01 else 0
                    pts3.extend([ox + t * gw, oy + min(val, 1) * gh * 0.85])
                d.add(PolyLine(pts3, strokeColor=C_DIST, strokeWidth=1.5,
                               strokeDashArray=[2, 2]))

    # Axis labels for P(x) and x on first graph
    d.add(String(10, H - ch + 25, "P(x)", textAnchor="middle", fontSize=6, fillColor=C_MED))

    return d


def diagram_markov():
    """Section 3: Markov state machine with 5 states."""
    W = USABLE_W
    H = 165
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=HexColor("#FAFAFA"), strokeColor=C_LGRAY, strokeWidth=0.5))

    # 5 states arranged in a pentagon-like layout
    states = [
        ("SPARSE", W * 0.15, H * 0.7),
        ("MEDIUM", W * 0.38, H * 0.7),
        ("DENSE", W * 0.62, H * 0.7),
        ("CLIMAX", W * 0.77, H * 0.35),
        ("SILENCE", W * 0.25, H * 0.25),
    ]
    R = 22

    # Draw connections first (behind circles)
    connections = [
        (0, 1, "0.5"), (1, 2, "0.3"), (2, 3, "0.3"),
        (3, 4, "0.3"), (4, 0, "0.5"),
        (1, 0, "0.2"), (2, 1, "0.2"),
    ]
    for src, dst, prob in connections:
        sx, sy = states[src][1], states[src][2]
        dx, dy = states[dst][1], states[dst][2]
        # Offset from circle edge
        angle = math.atan2(dy - sy, dx - sx)
        sx2 = sx + R * math.cos(angle)
        sy2 = sy + R * math.sin(angle)
        dx2 = dx - R * math.cos(angle)
        dy2 = dy - R * math.sin(angle)

        # Slight curve offset for bidirectional
        offset = 4 if src > dst else 0
        ox = -offset * math.sin(angle)
        oy = offset * math.cos(angle)

        d.add(Line(sx2 + ox, sy2 + oy, dx2 + ox, dy2 + oy,
                   strokeColor=C_MARKOV, strokeWidth=1, strokeOpacity=0.6))
        _arrow_head(d, dx2 + ox, dy2 + oy,
                    "right" if abs(math.cos(angle)) > abs(math.sin(angle))
                    else ("up" if math.sin(angle) > 0 else "down"),
                    size=4, color=C_MARKOV)
        # Probability label
        mx = (sx2 + dx2) / 2 + ox * 2
        my = (sy2 + dy2) / 2 + oy * 2
        d.add(String(mx, my, prob, textAnchor="middle", fontSize=6,
                     fillColor=C_MARKOV, fontName="Helvetica"))

    # Draw state circles
    for name, cx, cy in states:
        d.add(Circle(cx, cy, R, fillColor=C_BG_MARKOV, strokeColor=C_MARKOV, strokeWidth=1.5))
        d.add(String(cx, cy - 3, name, textAnchor="middle", fontSize=6,
                     fontName="Helvetica-Bold", fillColor=C_MARKOV))

    # Title
    d.add(String(W / 2, H - 10, "Cadena de Markov actual (5 estados fijos)",
                 textAnchor="middle", fontSize=8, fontName="Helvetica-Bold", fillColor=C_DARK))

    return d


def diagram_sieve():
    """Section 4: Number line with sieve filtering."""
    W = USABLE_W
    H = 130
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=HexColor("#FAFAFA"), strokeColor=C_LGRAY, strokeWidth=0.5))

    ox = 40
    num_w = (W - 80) / 16

    sieves = [
        ("Sieve(3,0)", lambda n: n % 3 == 0, H - 25),
        ("Sieve(5,0)", lambda n: n % 5 == 0, H - 55),
        ("Union", lambda n: n % 3 == 0 or n % 5 == 0, H - 85),
    ]

    for label, test_fn, y_row in sieves:
        d.add(String(ox - 5, y_row - 3, label, textAnchor="end", fontSize=7,
                     fontName="Helvetica-Bold",
                     fillColor=C_SIEVE if "Union" in label else C_DARK))
        # Number line
        x_start = ox + 5
        d.add(Line(x_start, y_row, x_start + 16 * num_w, y_row,
                   strokeColor=C_LGRAY, strokeWidth=0.5))
        for n in range(16):
            cx = x_start + n * num_w + num_w / 2
            passes = test_fn(n)
            d.add(Circle(cx, y_row, 7,
                         fillColor=C_SIEVE if passes else white,
                         strokeColor=C_SIEVE, strokeWidth=1,
                         fillOpacity=1 if passes else 0))
            d.add(String(cx, y_row - 3, str(n), textAnchor="middle", fontSize=5,
                         fillColor=white if passes else C_MED,
                         fontName="Helvetica-Bold" if passes else "Helvetica"))

    # Legend
    d.add(Circle(ox + 10, 10, 5, fillColor=C_SIEVE, strokeColor=C_SIEVE))
    d.add(String(ox + 20, 7, "= pasa la criba", fontSize=6, fillColor=C_DARK))
    d.add(Circle(ox + 110, 10, 5, fillColor=white, strokeColor=C_SIEVE))
    d.add(String(ox + 120, 7, "= no pasa", fontSize=6, fillColor=C_DARK))

    return d


def diagram_random_walk():
    """Section 5: Independent vs random walk comparison."""
    W = USABLE_W
    H = 120
    d = Drawing(W, H)

    half = W / 2 - 10

    # --- Left: Independent random values ---
    d.add(Rect(5, 5, half, H - 10, rx=4, ry=4, fillColor=HexColor("#FFF7ED"),
               strokeColor=C_LGRAY, strokeWidth=0.5))
    d.add(String(half / 2 + 5, H - 18, "ACTUAL: Valores independientes",
                 textAnchor="middle", fontSize=7, fontName="Helvetica-Bold", fillColor=C_DARK))
    # Axes
    lox, loy = 30, 18
    lgw, lgh = half - 50, H - 50
    d.add(Line(lox, loy, lox, loy + lgh, strokeColor=C_DARK, strokeWidth=0.8))
    d.add(Line(lox, loy, lox + lgw, loy, strokeColor=C_DARK, strokeWidth=0.8))
    # Random scatter points
    import random
    rng = random.Random(42)
    vals_indep = [rng.random() for _ in range(12)]
    for i, v in enumerate(vals_indep):
        px = lox + (i + 0.5) * lgw / 12
        py = loy + v * lgh
        d.add(Circle(px, py, 3, fillColor=C_SIEVE, strokeColor=C_SIEVE, strokeWidth=1))

    d.add(String(lox - 10, loy + lgh / 2, "val", textAnchor="middle", fontSize=5,
                 fillColor=C_MED))
    d.add(String(lox + lgw / 2, loy - 9, "evento", textAnchor="middle", fontSize=5,
                 fillColor=C_MED))

    # --- Right: Random walk ---
    rx_off = half + 15
    d.add(Rect(rx_off, 5, half, H - 10, rx=4, ry=4, fillColor=C_BG_WALK,
               strokeColor=C_LGRAY, strokeWidth=0.5))
    d.add(String(rx_off + half / 2, H - 18, "NUEVO: Random Walk (conectado)",
                 textAnchor="middle", fontSize=7, fontName="Helvetica-Bold", fillColor=C_WALK))
    rox, roy = rx_off + 25, 18
    rgw, rgh = half - 50, H - 50
    d.add(Line(rox, roy, rox, roy + rgh, strokeColor=C_DARK, strokeWidth=0.8))
    d.add(Line(rox, roy, rox + rgw, roy, strokeColor=C_DARK, strokeWidth=0.8))
    # Random walk path
    walk_val = 0.5
    walk_pts = []
    rng2 = random.Random(42)
    for i in range(12):
        px = rox + (i + 0.5) * rgw / 12
        py = roy + walk_val * rgh
        walk_pts.extend([px, py])
        walk_val += rng2.gauss(0, 0.08)
        walk_val = max(0.05, min(0.95, walk_val))
    d.add(PolyLine(walk_pts, strokeColor=C_WALK, strokeWidth=2))
    # Points on walk
    for i in range(0, len(walk_pts), 2):
        d.add(Circle(walk_pts[i], walk_pts[i + 1], 3, fillColor=C_WALK, strokeColor=C_WALK))

    d.add(String(rox - 10, roy + rgh / 2, "val", textAnchor="middle", fontSize=5,
                 fillColor=C_MED))
    d.add(String(rox + rgw / 2, roy - 9, "evento", textAnchor="middle", fontSize=5,
                 fillColor=C_MED))

    return d


def diagram_boundary_types():
    """Section 5: Three boundary mode mini graphs."""
    W = USABLE_W
    H = 90
    d = Drawing(W, H)

    import random
    third = W / 3 - 8
    titles = ["REFLECTANTE", "ABSORBENTE", "ENVOLVENTE (wrap)"]
    colors_b = [C_WALK, C_WALK, C_WALK]

    for idx in range(3):
        px = idx * (third + 12) + 5
        d.add(Rect(px, 5, third, H - 10, rx=4, ry=4,
                    fillColor=HexColor("#FAFAFA"), strokeColor=C_LGRAY, strokeWidth=0.5))
        d.add(String(px + third / 2, H - 15, titles[idx],
                     textAnchor="middle", fontSize=7, fontName="Helvetica-Bold", fillColor=C_WALK))
        # Axes
        ox, oy = px + 15, 15
        gw, gh = third - 30, H - 40
        d.add(Line(ox, oy, ox, oy + gh, strokeColor=C_DARK, strokeWidth=0.5))
        d.add(Line(ox, oy, ox + gw, oy, strokeColor=C_DARK, strokeWidth=0.5))
        # Min/max lines
        d.add(Line(ox, oy + gh, ox + gw, oy + gh, strokeColor=C_MED, strokeWidth=0.5,
                   strokeDashArray=[2, 2]))
        d.add(Line(ox, oy, ox + gw, oy, strokeColor=C_MED, strokeWidth=0.5,
                   strokeDashArray=[2, 2]))
        d.add(String(ox - 8, oy + gh - 3, "max", fontSize=5, fillColor=C_MED))
        d.add(String(ox - 8, oy - 1, "min", fontSize=5, fillColor=C_MED))

        # Walk path
        rng_b = random.Random(idx * 10 + 1)
        val = 0.5
        pts = []
        for i in range(10):
            step = rng_b.gauss(0, 0.2)
            val += step
            if idx == 0:  # reflecting
                if val > 1: val = 2 - val
                if val < 0: val = -val
            elif idx == 1:  # absorbing
                val = max(0, min(1, val))
            else:  # wrapping
                val = val % 1.0
            pts.extend([ox + (i + 0.5) * gw / 10, oy + val * gh])
        d.add(PolyLine(pts, strokeColor=C_WALK, strokeWidth=1.5))

    return d


def diagram_pipeline():
    """Section 7: Horizontal pipeline flowchart."""
    W = USABLE_W
    H = 85
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=HexColor("#FAFAFA"), strokeColor=C_LGRAY, strokeWidth=0.5))

    boxes = [
        ("MARKOV\ncontexto", C_BG_MARKOV, C_MARKOV),
        ("DISTRIBUCION\nvalor crudo", C_BG_DIST, C_DIST),
        ("CRIBA\nfiltrado", C_BG_SIEVE, C_SIEVE),
        ("RANDOM WALK\nsuavizado", C_BG_WALK, C_WALK),
    ]

    bw = (W - 80) / 4
    gap = 12
    total_w = 4 * bw + 3 * gap
    x_start = (W - total_w) / 2
    by = 22
    bh = 40

    for i, (label, fill, stroke) in enumerate(boxes):
        bx = x_start + i * (bw + gap)
        d.add(Rect(bx, by, bw, bh, rx=4, ry=4, fillColor=fill,
                    strokeColor=stroke, strokeWidth=1.5))
        lines = label.split("\n")
        d.add(String(bx + bw / 2, by + bh / 2 + 4, lines[0],
                     textAnchor="middle", fontSize=8, fontName="Helvetica-Bold",
                     fillColor=stroke))
        d.add(String(bx + bw / 2, by + bh / 2 - 8, lines[1],
                     textAnchor="middle", fontSize=7, fillColor=stroke))

        # Arrow to next
        if i < 3:
            ax1 = bx + bw
            ax2 = bx + bw + gap
            ay = by + bh / 2
            d.add(Line(ax1, ay, ax2 - 6, ay, strokeColor=C_DARK, strokeWidth=1.5))
            _arrow_head(d, ax2, ay, "right", size=4, color=C_DARK)

    # Top label
    d.add(String(W / 2, by + bh + 14, "Pipeline de generacion por evento",
                 textAnchor="middle", fontSize=8, fontName="Helvetica-Bold", fillColor=C_DARK))
    # Step numbers
    for i in range(4):
        bx = x_start + i * (bw + gap)
        d.add(String(bx + bw / 2, by - 10, f"Paso {i + 1}",
                     textAnchor="middle", fontSize=6, fillColor=C_MED))

    return d


# ─────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        "Xenakis_Parametros_Referencia.pdf", pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Tecnicas de Xenakis - Parametros de Composicion",
    )
    story = []

    # ── COVER ──
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph("Tecnicas de Xenakis<br/>Parametros de Composicion", s_title))
    story.append(Paragraph(
        "Documento tecnico de referencia — Aleatoric Composer v0.1<br/>"
        "Como las 4 tecnicas estocasticas afectan a cada parametro del sistema", s_subtitle))

    # Color legend
    legend_data = [[
        P('<font color="#2563EB"><b>DISTRIBUCIONES</b></font>'),
        P('<font color="#16A34A"><b>MARKOV</b></font>'),
        P('<font color="#EA580C"><b>CRIBAS</b></font>'),
        P('<font color="#9333EA"><b>RANDOM WALKS</b></font>'),
    ]]
    legend = Table(legend_data, colWidths=[USABLE_W / 4] * 4)
    legend.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), C_BG_DIST),
        ("BACKGROUND", (1, 0), (1, 0), C_BG_MARKOV),
        ("BACKGROUND", (2, 0), (2, 0), C_BG_SIEVE),
        ("BACKGROUND", (3, 0), (3, 0), C_BG_WALK),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, C_LGRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, C_LGRAY),
    ]))
    story.append(legend)
    story.append(Spacer(1, 6 * mm))

    toc_items = [
        "1. Arquitectura General",
        "2. Distribuciones de Probabilidad",
        "3. Cadenas de Markov",
        "4. Cribas (Sieves)",
        "5. Paseos Aleatorios (Random Walks)",
        "6. Tabla Maestra de Interaccion",
        "7. Flujo de Datos Completo",
    ]
    story.append(Paragraph("INDICE", s_h2))
    for item in toc_items:
        story.append(Paragraph(item, ParagraphStyle("toc", parent=s_body, leftIndent=5*mm)))
    story.append(PageBreak())

    # ── SECTION 1: ARCHITECTURE ──
    story.append(Paragraph("1. Arquitectura General", s_h1))
    story.append(Paragraph(
        "El sistema tiene 3 capas: <b>Arranger</b> (orquesta), <b>Strategy</b> "
        "(algoritmo de colocacion) y <b>ControlledRandom</b> (generador). "
        "Las 4 tecnicas de Xenakis se insertan en capas diferentes:", s_body))
    story.append(diagram_architecture())
    story.append(Paragraph("<i>Diagrama 1: Las distribuciones enriquecen la capa base (RNG). "
        "Markov opera como Strategy. Cribas filtran valores. Random Walks suavizan evoluciones.</i>",
        s_caption))
    story.append(make_table(
        ["Tecnica", "Capa", "Rol", "Interaccion"],
        [
            [PB('<font color="#2563EB">Distribuciones</font>'),
             "ControlledRandom (base)", "Generan valores crudos",
             "Cualquier Strategy las usa via rng.exponential(), rng.cauchy(), etc."],
            [PB('<font color="#16A34A">Cadenas de Markov</font>'),
             "Strategy (algoritmo)", "Deciden transiciones entre estados",
             "Reemplazan o extienden StructuredStrategy con matrices editables"],
            [PB('<font color="#EA580C">Cribas (Sieves)</font>'),
             "Post-filtro (nuevo)", "Filtran valores invalidos",
             "Se aplican DESPUES de generar: si el valor no pasa la criba, se cuantiza"],
            [PB('<font color="#9333EA">Random Walks</font>'),
             "Modificador (nuevo)", "Suavizan evolucion temporal",
             "valor[n] = valor[n-1] + paso_aleatorio"],
        ],
        [18, 20, 22, 40]))
    story.append(PageBreak())

    # ── SECTION 2: DISTRIBUTIONS ──
    story.append(Paragraph("2. Distribuciones de Probabilidad", s_h1))
    story.append(Paragraph(
        "Actualmente el RNG solo ofrece <b>uniform</b> y <b>gaussian</b>. "
        "Xenakis uso 5 distribuciones adicionales, cada una con un caracter sonoro diferente. "
        "Se anaden como nuevos metodos a <b>ControlledRandom</b>.", s_body))
    story.append(diagram_five_distributions())
    story.append(Paragraph(
        "<i>Diagrama 2: Formas de las 5 distribuciones. Exponencial = rafagas agrupadas. "
        "Cauchy = colas extremas. Weibull = forma ajustable (3 variantes segun k). "
        "Poisson = conteos discretos. Lineal = sesgo creciente/decreciente.</i>", s_caption))

    story.append(Paragraph(
        '<font color="#2563EB"><b>Tabla: parametros afectados por cada distribucion</b></font>', s_body))
    story.append(make_table(
        ["Parametro", "Metodo actual", "Distribucion Xenakis", "Resultado sonoro"],
        [
            ["timeline_start (gaps)", "uniform", "Exponencial, Poisson",
             "Rafagas: muchos gaps cortos, pocos largos (como Achorripsis)"],
            ["event_duration", "gaussian", "Cauchy, Weibull",
             "Colas pesadas = eventos muy cortos/largos ocasionales"],
            ["amplitude", "uniform", "Lineal, Exponencial",
             "Sesga dinamicas hacia pp o ff"],
            ["pan", "uniform", "Cauchy",
             "Centro estable, saltos extremos L/R impredecibles"],
            ["fade_in / fade_out", "uniform", "Weibull",
             "Forma ajustable de ataques/colas"],
            ["n_events (por seccion)", "fijo", "Poisson",
             "Densidad variable: pocas notas vs masas sonoras"],
        ],
        [18, 14, 20, 48], header_color=C_DIST))

    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("<b>Resumen: RNG actual vs. ampliado</b>", s_body))
    story.append(make_table(
        ["Metodo actual", "Comportamiento", "Distribucion Xenakis nueva"],
        [
            ["rng.uniform(lo, hi)", "Todos los valores igual de probables",
             "rng.linear(lo, hi, slope) para sesgar"],
            ["rng.gaussian(mu, sigma)", "Campana simetrica",
             "rng.cauchy(x0, gamma) para colas extremas"],
            ["(no existe)", "--", "rng.exponential(lam) para rafagas agrupadas"],
            ["(no existe)", "--", "rng.weibull(k, lam) para forma ajustable"],
            ["(no existe)", "--", "rng.poisson(lam) para conteos discretos"],
        ],
        [22, 30, 48], header_color=C_DIST))
    story.append(PageBreak())

    # ── SECTION 3: MARKOV CHAINS ──
    story.append(Paragraph("3. Cadenas de Markov", s_h1))
    story.append(Paragraph(
        "Una cadena de Markov decide el <b>siguiente estado</b> basandose solo en el "
        "<b>estado actual</b>. Ya existe en StructuredStrategy con una matriz fija de 5 estados. "
        "La ampliacion permite <b>matrices editables</b> y aplicarlas a <b>cualquier parametro</b>.",
        s_body))
    story.append(diagram_markov())
    story.append(Paragraph(
        "<i>Diagrama 3: Cadena de Markov actual con 5 estados fijos y transiciones hardcodeadas.</i>",
        s_caption))

    story.append(make_table(
        ["Aspecto", "StructuredStrategy ACTUAL", "Markov Xenakis NUEVO"],
        [
            ["Estados", "5 fijos: sparse, medium, dense, climax, silence",
             "N estados definidos por el usuario"],
            ["Matriz", "Hardcodeada en Python", "Editable via GUI (tabla NxN)"],
            ["Que controla", "Solo tipo de seccion (densidad global)",
             "Cualquier parametro: source, efecto, dinamica..."],
            ["Orden", "Orden 1 (solo estado actual)", "Orden 1 o 2 (2 ultimos estados)"],
            ["Multiples cadenas", "1 sola cadena", "1 cadena por parametro, en paralelo"],
        ],
        [16, 32, 52], header_color=C_MARKOV))

    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        '<font color="#16A34A"><b>Parametros controlables por Markov:</b></font>', s_body))
    story.append(make_table(
        ["Parametro", "Estados posibles", "Ejemplo musical"],
        [
            ["source_selection", "Nombres de archivos de audio",
             "Despues de 'piano.wav' es 70% probable que suene 'cello.wav'"],
            ["density_state", "sparse, medium, dense, climax, silence",
             "Tras un climax, alta probabilidad de silencio"],
            ["dynamic_state", "pp, p, mp, mf, f, ff",
             "Crescendo probabilistico: cada estado tiende al siguiente mas fuerte"],
            ["effect_chain", "reverb, delay, granular...",
             "Despues de reverb es probable que venga delay"],
            ["register", "grave, medio, agudo",
             "Melodia estocastica que tiende a mantenerse en registro"],
        ],
        [18, 28, 54], header_color=C_MARKOV))
    story.append(PageBreak())

    # ── SECTION 4: SIEVES ──
    story.append(Paragraph("4. Cribas (Sieves)", s_h1))
    story.append(Paragraph(
        "Las cribas son <b>filtros de aritmetica modular</b>: Sieve(modulo, residuo) — "
        "un valor x pasa si x mod modulo == residuo. Se combinan con operaciones logicas "
        "(union, interseccion, complemento).", s_body))
    story.append(diagram_sieve())
    story.append(Paragraph(
        "<i>Diagrama 4: Sieve(3,0) pasa multiplos de 3. Sieve(5,0) pasa multiplos de 5. "
        "La union produce un patron irregular pero determinista.</i>", s_caption))

    story.append(make_table(
        ["Operacion", "Simbolo", "Resultado", "Uso musical"],
        [
            ["Union", "A U B", "Valores que pasan A O B", "Combinar dos patrones ritmicos"],
            ["Interseccion", "A n B", "Valores que pasan A Y B", "Solo puntos comunes"],
            ["Complemento", "~A", "Todo lo que NO pasa A", "Invertir un patron"],
        ],
        [16, 12, 30, 42], header_color=C_SIEVE))
    story.append(Spacer(1, 3 * mm))
    story.append(make_table(
        ["Parametro", "Unidad", "Ejemplo de criba", "Resultado sonoro"],
        [
            ["timeline_start", "centesimas de seg", "Sieve(25,0) U Sieve(33,0)",
             "Patron ritmico irregular: eventos solo en ciertos instantes"],
            ["event_duration", "decimas de seg", "Sieve(5,0) = 0.5, 1.0, 1.5...",
             "Solo ciertas duraciones permitidas"],
            ["amplitude", "10 niveles", "Sieve(3,0) n Sieve(2,0) = {0, 6}",
             "Solo pp y ff — sin dinamicas intermedias"],
            ["pan", "8 posiciones", "Sieve(2,0) = {0, 2, 4, 6}",
             "Sonido solo en 4 puntos espaciales fijos"],
        ],
        [16, 16, 28, 40], header_color=C_SIEVE))
    story.append(PageBreak())

    # ── SECTION 5: RANDOM WALKS ──
    story.append(Paragraph("5. Paseos Aleatorios (Random Walks)", s_h1))
    story.append(Paragraph(
        "Un random walk genera cada valor como <b>valor_anterior + paso</b>. "
        "A diferencia del sistema actual (valores independientes), crea <b>continuidad temporal</b>.",
        s_body))
    story.append(diagram_random_walk())
    story.append(Paragraph(
        "<i>Diagrama 5: Izquierda, valores independientes (saltos bruscos). "
        "Derecha, random walk (movimiento organico conectado).</i>", s_caption))

    story.append(Paragraph(
        '<font color="#9333EA"><b>Tipos de frontera:</b></font>', s_body))
    story.append(diagram_boundary_types())
    story.append(Paragraph(
        "<i>Diagrama 6: Reflectante rebota en los limites. Absorbente se queda. "
        "Envolvente salta al otro extremo.</i>", s_caption))

    story.append(make_table(
        ["Parametro", "step_size tipico", "Frontera ideal", "Resultado sonoro"],
        [
            ["pan", "0.05-0.2", "Reflectante",
             "Fuente que se mueve gradualmente en el estereo"],
            ["amplitude", "0.02-0.1", "Reflectante",
             "Dinamicas que suben/bajan organicamente"],
            ["density (gap)", "0.1-0.5 seg", "Reflectante",
             "Secciones que se densifican/rarifican naturalmente"],
            ["effect params (wet/dry)", "0.02-0.1", "Reflectante",
             "Efectos que mutan gradualmente"],
            ["source_start (offset)", "0.1-1.0 seg", "Envolvente",
             "Cursor que recorre el archivo como un scanner"],
        ],
        [18, 16, 16, 50], header_color=C_WALK))
    story.append(PageBreak())

    # ── SECTION 6: MASTER TABLE ──
    story.append(Paragraph("6. Tabla Maestra de Interaccion", s_h1))
    story.append(Paragraph(
        "<b>+++</b> = ajuste ideal | <b>++</b> = util | <b>+</b> = posible | <b>-</b> = no aplicable",
        s_body))

    master_data = [
        ["timeline_start", "+++", "++", "+++", "+"],
        ["event_duration", "+++", "+", "++", "++"],
        ["amplitude", "++", "++", "+", "+++"],
        ["pan", "++", "+", "+", "+++"],
        ["source_selection", "+", "+++", "+", "+"],
        ["effects_config", "+", "+++", "-", "++"],
        ["fade_in / fade_out", "++", "-", "+", "+"],
        ["is_reversed", "+", "++", "-", "-"],
        ["density", "++", "+++", "++", "+++"],
        ["source_start", "+", "+", "++", "+++"],
    ]
    headers_m = ["Parametro",
                 '<font color="#2563EB">Distribuc.</font>',
                 '<font color="#16A34A">Markov</font>',
                 '<font color="#EA580C">Cribas</font>',
                 '<font color="#9333EA">R. Walk</font>']
    cw = [USABLE_W * p / 100 for p in [30, 17, 17, 18, 18]]
    header_row = [PH(h) for h in headers_m]
    rows_m = [header_row]
    for row in master_data:
        rows_m.append([PB(row[0])] + [P(c) for c in row[1:]])
    mt = Table(rows_m, colWidths=cw, repeatRows=1)
    mt_style = [
        ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D1D5DB")),
    ]
    for i in range(1, len(rows_m)):
        if i % 2 == 0:
            mt_style.append(("BACKGROUND", (0, i), (-1, i), C_GRAY))
        for col_idx, bg in [(1, C_BG_DIST), (2, C_BG_MARKOV), (3, C_BG_SIEVE), (4, C_BG_WALK)]:
            if master_data[i - 1][col_idx] == "+++":
                mt_style.append(("BACKGROUND", (col_idx, i), (col_idx, i), bg))
    mt.setStyle(TableStyle(mt_style))
    story.append(mt)
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>Lectura rapida:</b> Los <b>+++</b> coloreados indican ajustes ideales. "
        "<b>pan</b> es ideal para Random Walk. <b>source_selection</b> para Markov. "
        "Las cribas brillan en <b>timeline_start</b>. Las distribuciones en <b>duracion</b> y <b>timing</b>.",
        s_body))

    # ── SECTION 7: COMPLETE PIPELINE ──
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("7. Flujo de Datos Completo", s_h1))
    story.append(Paragraph(
        "Las 4 tecnicas no son alternativas — son <b>capas composables</b> que se aplican "
        "en secuencia para generar cada AudioEvent:", s_body))
    story.append(diagram_pipeline())
    story.append(Paragraph(
        "<i>Diagrama 7: Cada tecnica responde a una pregunta diferente. "
        "Markov: que contexto. Distribucion: que valor. Criba: es valido. Walk: como evoluciona.</i>",
        s_caption))

    story.append(make_table(
        ["Tecnica", "Pregunta que responde", "Analogia"],
        [
            [PB('<font color="#16A34A">Markov</font>'),
             "En que contexto/estado estamos?", "El director que decide la seccion"],
            [PB('<font color="#2563EB">Distribucion</font>'),
             "Que valor concreto toma este parametro?", "Los dados para cada nota"],
            [PB('<font color="#EA580C">Criba</font>'),
             "Este valor esta permitido?", "El tamiz que filtra notas"],
            [PB('<font color="#9333EA">Random Walk</font>'),
             "Como evoluciona respecto al anterior?", "El musico que ajusta gradualmente"],
        ],
        [14, 38, 48]))

    doc.build(story)
    print(f"PDF generado: {doc.filename}")


if __name__ == "__main__":
    build_pdf()
