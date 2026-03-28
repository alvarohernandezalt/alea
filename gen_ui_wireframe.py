#!/usr/bin/env python3
"""Generate UI wireframe PDF with vector diagrams for Aleatoric Composer."""

import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)
from reportlab.graphics.shapes import (
    Drawing, Rect, Line, String, Circle, Polygon, PolyLine, Group,
)

C_DARK = HexColor("#1F2937")
C_MED = HexColor("#6B7280")
C_LIGHT = HexColor("#E5E7EB")
C_BG = HexColor("#F9FAFB")
C_BORDER = HexColor("#9CA3AF")
C_ACCENT = HexColor("#6366F1")
C_ACCENT_BG = HexColor("#EEF2FF")
C_TRACK1 = HexColor("#F59E0B")
C_TRACK2 = HexColor("#10B981")
C_TRACK3 = HexColor("#3B82F6")
C_TRACK4 = HexColor("#EF4444")
C_PANEL_BG = HexColor("#F3F4F6")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
USABLE_W = PAGE_W - 2 * MARGIN

styles = getSampleStyleSheet()

s_title = ParagraphStyle("WT", parent=styles["Title"], fontSize=20, leading=24,
                          textColor=C_DARK, spaceAfter=3*mm)
s_subtitle = ParagraphStyle("WS", parent=styles["Normal"], fontSize=10,
                             leading=13, textColor=C_MED, spaceAfter=6*mm,
                             alignment=TA_CENTER)
s_h1 = ParagraphStyle("WH1", parent=styles["Heading1"], fontSize=14, leading=17,
                       textColor=C_DARK, spaceBefore=5*mm, spaceAfter=3*mm)
s_h2 = ParagraphStyle("WH2", parent=styles["Heading2"], fontSize=11, leading=14,
                       textColor=C_DARK, spaceBefore=3*mm, spaceAfter=2*mm)
s_body = ParagraphStyle("WB", parent=styles["Normal"], fontSize=9, leading=12,
                         textColor=C_DARK, spaceAfter=2*mm)
s_caption = ParagraphStyle("WCap", parent=styles["Normal"], fontSize=8, leading=10,
                            textColor=C_MED, alignment=TA_CENTER,
                            spaceAfter=3*mm, spaceBefore=1*mm)
s_cell = ParagraphStyle("WCell", parent=styles["Normal"], fontSize=7.5,
                         leading=10, textColor=C_DARK)
s_cell_h = ParagraphStyle("WCH", parent=s_cell, fontName="Helvetica-Bold",
                           textColor=white)
s_cell_b = ParagraphStyle("WCB", parent=s_cell, fontName="Helvetica-Bold")


def P(t, s=s_cell): return Paragraph(t, s)
def PH(t): return Paragraph(t, s_cell_h)
def PB(t): return Paragraph(t, s_cell_b)


def make_table(headers, rows, col_pcts):
    cw = [USABLE_W * p / 100 for p in col_pcts]
    data = [[PH(h) for h in headers]]
    for r in rows:
        data.append([P(str(c)) if not isinstance(c, Paragraph) else c for c in r])
    t = Table(data, colWidths=cw, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), C_DARK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, C_BORDER),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), C_BG))
    t.setStyle(TableStyle(cmds))
    return t


def _arrow_head(d, x, y, direction, size=5, color=C_DARK):
    s = size
    if direction == "right":
        d.add(Polygon(points=[x, y, x - s*1.5, y - s, x - s*1.5, y + s],
                       fillColor=color, strokeColor=color))
    elif direction == "down":
        d.add(Polygon(points=[x, y, x - s, y + s*1.5, x + s, y + s*1.5],
                       fillColor=color, strokeColor=color))


def _draw_slider(d, x, y, w, val_pct=0.5):
    """Draw a horizontal slider widget."""
    d.add(Line(x, y, x + w, y, strokeColor=C_BORDER, strokeWidth=2))
    cx = x + w * val_pct
    d.add(Circle(cx, y, 3, fillColor=C_ACCENT, strokeColor=C_ACCENT))


def _draw_button(d, x, y, w, h, text, accent=False):
    """Draw a button widget."""
    fill = C_ACCENT if accent else C_PANEL_BG
    stroke = C_ACCENT if accent else C_BORDER
    tc = white if accent else C_DARK
    d.add(Rect(x, y, w, h, rx=3, ry=3, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    d.add(String(x + w/2, y + h/2 - 3, text, textAnchor="middle", fontSize=6,
                 fontName="Helvetica-Bold", fillColor=tc))


def _draw_combo(d, x, y, w, h, text):
    """Draw a combo box widget."""
    d.add(Rect(x, y, w, h, rx=2, ry=2, fillColor=white, strokeColor=C_BORDER, strokeWidth=0.8))
    d.add(String(x + 4, y + h/2 - 3, text, fontSize=6, fillColor=C_DARK))
    # Down triangle
    tx = x + w - 8
    ty = y + h/2
    d.add(Polygon(points=[tx - 3, ty + 2, tx + 3, ty + 2, tx, ty - 2],
                   fillColor=C_MED, strokeColor=None))


def _draw_waveform(d, x, y, w, h, color):
    """Draw a mini waveform."""
    import random
    rng = random.Random(hash(str(color)) % 1000)
    d.add(Rect(x, y, w, h, fillColor=HexColor("#1a1a2e"), strokeColor=C_BORDER, strokeWidth=0.5))
    pts = []
    mid = y + h / 2
    for i in range(int(w)):
        amp = rng.random() * h * 0.35
        pts.extend([x + i, mid + amp * (1 if i % 2 else -1)])
    d.add(PolyLine(pts, strokeColor=color, strokeWidth=0.8))


# ─────────────────────────────────────────────
# DIAGRAM BUILDERS
# ─────────────────────────────────────────────

def diagram_layout():
    """Section 1: Main window layout."""
    W = USABLE_W
    H = 300
    d = Drawing(W, H)

    pad = 3
    # Outer window
    d.add(Rect(0, 0, W, H, rx=4, ry=4, fillColor=HexColor("#1e1e2e"),
               strokeColor=C_DARK, strokeWidth=2))

    # Menu bar
    menu_h = 18
    my = H - menu_h - pad
    d.add(Rect(pad, my, W - 2*pad, menu_h, fillColor=HexColor("#252536"),
               strokeColor=None))
    d.add(String(12, my + 5, "File  |  Composition", fontSize=7, fillColor=HexColor("#aaaacc")))
    d.add(String(W - 40, my + 5, "[_] [X]", fontSize=7, fillColor=HexColor("#aaaacc")))

    # Main content area
    content_top = my - 3
    transport_h = 28
    copyright_h = 14
    timeline_h = 100
    content_bot = pad + copyright_h + transport_h + 3
    panels_h = content_top - content_bot - timeline_h - 6

    # Sources panel (left)
    src_w = W * 0.22
    src_x = pad + 2
    src_y = content_bot + timeline_h + 6
    d.add(Rect(src_x, src_y, src_w, panels_h, rx=2, ry=2,
               fillColor=HexColor("#252536"), strokeColor=HexColor("#3a3a55"), strokeWidth=1))
    d.add(String(src_x + src_w/2, src_y + panels_h - 12, "SOURCES",
                 textAnchor="middle", fontSize=9, fontName="Helvetica-Bold",
                 fillColor=HexColor("#aaaacc")))
    # Source items
    for i, (name, color) in enumerate([("piano.wav", C_TRACK1), ("cello.wav", C_TRACK2), ("noise.wav", C_TRACK3)]):
        iy = src_y + panels_h - 35 - i * 42
        d.add(String(src_x + 8, iy + 24, name, fontSize=6, fontName="Helvetica-Bold", fillColor=color))
        d.add(String(src_x + 8, iy + 16, "12.3s | stereo | 44100", fontSize=5, fillColor=HexColor("#8888aa")))
        _draw_waveform(d, src_x + 6, iy + 2, src_w - 12, 12, color)

    # Splitter indicator
    d.add(Line(src_x + src_w + 2, src_y, src_x + src_w + 2, src_y + panels_h,
               strokeColor=HexColor("#3a3a55"), strokeWidth=1.5))
    d.add(String(src_x + src_w + 2, src_y + panels_h / 2, "||",
                 textAnchor="middle", fontSize=8, fillColor=HexColor("#555577")))

    # Tabs (right)
    tabs_x = src_x + src_w + 6
    tabs_w = W - tabs_x - pad - 2
    d.add(Rect(tabs_x, src_y, tabs_w, panels_h, rx=2, ry=2,
               fillColor=HexColor("#252536"), strokeColor=HexColor("#3a3a55"), strokeWidth=1))
    # Tab headers
    th = 16
    tab_y = src_y + panels_h - th
    d.add(Rect(tabs_x, tab_y, tabs_w / 2, th, fillColor=C_ACCENT,
               strokeColor=None))
    d.add(String(tabs_x + tabs_w / 4, tab_y + 4, "Composition",
                 textAnchor="middle", fontSize=7, fontName="Helvetica-Bold", fillColor=white))
    d.add(Rect(tabs_x + tabs_w / 2, tab_y, tabs_w / 2, th,
               fillColor=HexColor("#2a2a3e"), strokeColor=None))
    d.add(String(tabs_x + 3 * tabs_w / 4, tab_y + 4, "Effects Palette",
                 textAnchor="middle", fontSize=7, fillColor=HexColor("#8888aa")))
    # Content placeholder
    d.add(String(tabs_x + tabs_w / 2, src_y + panels_h / 2 - 10,
                 "Contenido de la pestana activa",
                 textAnchor="middle", fontSize=7, fillColor=HexColor("#666688")))
    d.add(String(tabs_x + tabs_w / 2, src_y + panels_h / 2 - 22,
                 "(scroll vertical)",
                 textAnchor="middle", fontSize=6, fillColor=HexColor("#555577")))

    # Timeline area
    tl_y = content_bot
    tl_h = timeline_h
    d.add(Rect(pad + 2, tl_y, W - 2*pad - 4, tl_h, rx=2, ry=2,
               fillColor=HexColor("#1a1a2e"), strokeColor=HexColor("#3a3a55"), strokeWidth=1))
    d.add(String(pad + 10, tl_y + tl_h - 12, "TIMELINE VIEW",
                 fontSize=8, fontName="Helvetica-Bold", fillColor=HexColor("#aaaacc")))

    # Mixer strips
    mixer_w = 50
    d.add(Rect(pad + 4, tl_y + 2, mixer_w, tl_h - 16, fillColor=HexColor("#252536"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=0.5))
    for i, name in enumerate(["Trk 1", "Trk 2", "Trk 3", "Trk 4"]):
        ty = tl_y + tl_h - 28 - i * 18
        d.add(String(pad + 10, ty, name, fontSize=5, fontName="Helvetica-Bold",
                     fillColor=HexColor("#aaaacc")))
        d.add(String(pad + 38, ty, "M S", fontSize=5, fillColor=HexColor("#666688")))

    # Track lanes with colored blocks
    lane_x = pad + mixer_w + 8
    lane_w = W - 2*pad - mixer_w - 12
    track_colors = [C_TRACK1, C_TRACK2, C_TRACK3, C_TRACK4]
    import random
    rng = random.Random(42)
    for i in range(4):
        ty = tl_y + tl_h - 28 - i * 18
        # Ruler ticks
        if i == 0:
            for sec in range(7):
                tx = lane_x + sec * lane_w / 7
                d.add(Line(tx, tl_y + tl_h - 14, tx, tl_y + tl_h - 18,
                           strokeColor=HexColor("#555577"), strokeWidth=0.5))
                d.add(String(tx, tl_y + tl_h - 12, f"{sec*10}s", fontSize=4,
                             fillColor=HexColor("#666688")))
        # Audio event blocks
        for j in range(rng.randint(2, 4)):
            bx = lane_x + rng.random() * lane_w * 0.7
            bw = 20 + rng.random() * 60
            d.add(Rect(bx, ty - 2, bw, 14, rx=2, ry=2,
                       fillColor=track_colors[i], strokeColor=None,
                       fillOpacity=0.6))

    # Horizontal splitter between panels and timeline
    d.add(Line(pad + 2, tl_y + tl_h + 2, W - pad - 2, tl_y + tl_h + 2,
               strokeColor=HexColor("#3a3a55"), strokeWidth=1))

    # Transport bar
    tr_y = pad + copyright_h
    d.add(Rect(pad + 2, tr_y, W - 2*pad - 4, transport_h, fillColor=HexColor("#252536"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=1))
    _draw_button(d, pad + 8, tr_y + 6, 50, 16, "Render", accent=True)
    # Progress bar
    pb_x = pad + 65
    pb_w = W - 2*pad - 200
    d.add(Rect(pb_x, tr_y + 8, pb_w, 12, rx=2, ry=2,
               fillColor=HexColor("#1a1a2e"), strokeColor=HexColor("#3a3a55"), strokeWidth=0.5))
    d.add(Rect(pb_x, tr_y + 8, pb_w * 0.6, 12, rx=2, ry=2,
               fillColor=C_ACCENT, strokeColor=None, fillOpacity=0.5))
    d.add(String(pb_x + pb_w / 2, tr_y + 11, "60%", textAnchor="middle",
                 fontSize=5, fillColor=white))
    _draw_button(d, W - pad - 120, tr_y + 6, 55, 16, "Export WAV")
    _draw_button(d, W - pad - 60, tr_y + 6, 55, 16, "Export MP3")

    # Copyright
    d.add(String(W / 2, pad + 3, "(c) Alvaro Hernandez Altozano 2026",
                 textAnchor="middle", fontSize=5, fillColor=HexColor("#666688")))

    # Zone labels with arrows (outside the app)
    # Not needed — the diagram is self-explanatory with internal labels

    return d


def diagram_sources_detail():
    """Section 2: Sources panel detail."""
    W = USABLE_W * 0.55
    H = 220
    d = Drawing(W, H)

    d.add(Rect(0, 0, W, H, rx=4, ry=4, fillColor=HexColor("#252536"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=1.5))

    # Title + buttons
    d.add(String(W/2, H - 14, "SOURCES", textAnchor="middle", fontSize=10,
                 fontName="Helvetica-Bold", fillColor=HexColor("#aaaacc")))
    _draw_button(d, 10, H - 32, 55, 14, "+ Add files")
    _draw_button(d, 70, H - 32, 50, 14, "- Remove")

    # Source items
    items = [
        ("piano.wav", "12.3s | stereo | 44100", C_TRACK1, 0.5),
        ("cello.wav", "8.7s | mono | 48000", C_TRACK2, 0.8),
        ("noise.wav", "5.0s | mono | 44100", C_TRACK3, 0.7),
    ]
    for i, (name, info, color, weight) in enumerate(items):
        iy = H - 55 - i * 56
        # Item background
        d.add(Rect(6, iy - 6, W - 12, 52, rx=3, ry=3,
                    fillColor=HexColor("#1e1e2e"), strokeColor=HexColor("#3a3a55"),
                    strokeWidth=0.5))
        d.add(Circle(14, iy + 37, 3, fillColor=color, strokeColor=color))
        d.add(String(22, iy + 33, name, fontSize=7, fontName="Helvetica-Bold", fillColor=color))
        d.add(String(14, iy + 24, info, fontSize=5, fillColor=HexColor("#8888aa")))
        _draw_waveform(d, 10, iy + 10, W - 20, 12, color)
        # Weight slider
        d.add(String(14, iy + 1, "Weight:", fontSize=5, fillColor=HexColor("#8888aa")))
        _draw_slider(d, 50, iy + 3, W - 90, weight)
        d.add(String(W - 20, iy, f"{weight:.1f}", fontSize=5, fillColor=HexColor("#aaaacc")))

    # Drag & drop hint
    d.add(String(W/2, 8, "drag & drop audio files", textAnchor="middle",
                 fontSize=6, fillColor=HexColor("#555577")))

    return d


def diagram_composition_tab():
    """Section 3: Composition tab detail."""
    W = USABLE_W * 0.6
    H = 340
    d = Drawing(W, H)

    d.add(Rect(0, 0, W, H, rx=4, ry=4, fillColor=HexColor("#252536"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=1.5))

    # Tab headers
    th = 16
    d.add(Rect(0, H - th, W/2, th, rx=0, ry=0, fillColor=C_ACCENT, strokeColor=None))
    d.add(String(W/4, H - th + 4, "Composition", textAnchor="middle",
                 fontSize=7, fontName="Helvetica-Bold", fillColor=white))
    d.add(Rect(W/2, H - th, W/2, th, fillColor=HexColor("#2a2a3e"), strokeColor=None))
    d.add(String(3*W/4, H - th + 4, "Effects Palette", textAnchor="middle",
                 fontSize=7, fillColor=HexColor("#8888aa")))

    # Groups
    groups = [
        ("General", H - 30, 68, [
            ("Strategy:", "combo", "scatter"),
            ("Seed:", "spin+btn", "42  [Random]"),
            ("Duration:", "spin", "120.0 s"),
            ("Tracks:", "spin", "4"),
        ]),
        ("Timing", H - 106, 50, [
            ("Event duration:", "range", "0.5 — 30.0 s"),
            ("Silence gap:", "range", "0.0 — 5.0 s"),
            ("Allow overlap:", "check", "[x]"),
        ]),
        ("Dynamics", H - 164, 56, [
            ("Amplitude:", "range", "0.3 — 1.0"),
            ("Pan:", "range", "-1.0 — 1.0"),
            ("Fade in:", "range", "0.01 — 0.5 s"),
            ("Fade out:", "range", "0.01 — 1.0 s"),
        ]),
        ("Effects", H - 228, 36, [
            ("Probability:", "slider", "0.70"),
            ("Max per event:", "spin", "3"),
        ]),
        ("Structure", H - 272, 48, [
            ("Density curve:", "combo", "constant"),
        ]),
    ]

    for gname, gy, gh, controls in groups:
        # Group box
        d.add(Rect(8, gy - gh, W - 16, gh, rx=3, ry=3,
                    fillColor=HexColor("#1e1e2e"), strokeColor=HexColor("#3a3a55"),
                    strokeWidth=0.8))
        d.add(String(16, gy - 10, gname, fontSize=7, fontName="Helvetica-Bold",
                     fillColor=HexColor("#aaaacc")))

        for ci, (label, ctype, value) in enumerate(controls):
            cy = gy - 22 - ci * 12
            d.add(String(16, cy, label, fontSize=5.5, fillColor=HexColor("#8888aa")))

            if ctype == "combo":
                _draw_combo(d, W * 0.45, cy - 3, W * 0.42, 11, value)
            elif ctype == "spin":
                d.add(Rect(W * 0.45, cy - 3, W * 0.3, 11, rx=2, ry=2,
                           fillColor=white, strokeColor=C_BORDER, strokeWidth=0.5))
                d.add(String(W * 0.47, cy, value, fontSize=5.5, fillColor=C_DARK))
            elif ctype == "spin+btn":
                d.add(Rect(W * 0.45, cy - 3, W * 0.22, 11, rx=2, ry=2,
                           fillColor=white, strokeColor=C_BORDER, strokeWidth=0.5))
                d.add(String(W * 0.47, cy, "42", fontSize=5.5, fillColor=C_DARK))
                _draw_button(d, W * 0.70, cy - 3, 35, 11, "Random")
            elif ctype == "range":
                _draw_slider(d, W * 0.45, cy + 2, W * 0.35, 0.3)
                d.add(Circle(W * 0.45 + W * 0.35 * 0.7, cy + 2, 3,
                             fillColor=C_ACCENT, strokeColor=C_ACCENT))
                d.add(String(W * 0.85, cy, value, fontSize=4.5, fillColor=HexColor("#8888aa")))
            elif ctype == "slider":
                _draw_slider(d, W * 0.45, cy + 2, W * 0.35, 0.7)
                d.add(String(W * 0.85, cy, value, fontSize=5, fillColor=HexColor("#aaaacc")))
            elif ctype == "check":
                d.add(Rect(W * 0.45, cy - 2, 9, 9, fillColor=C_ACCENT, strokeColor=C_ACCENT,
                           strokeWidth=0.5))
                d.add(String(W * 0.45 + 4, cy - 1, "x", textAnchor="middle",
                             fontSize=6, fillColor=white, fontName="Helvetica-Bold"))

    # Density curve preview
    d.add(Rect(16, 24, W - 32, 22, fillColor=HexColor("#1a1a2e"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=0.5))
    pts = []
    for i in range(int(W - 34)):
        pts.extend([16 + i, 35])  # constant line
    d.add(PolyLine(pts, strokeColor=C_ACCENT, strokeWidth=1))
    d.add(String(W / 2, 28, "preview", textAnchor="middle", fontSize=5,
                 fillColor=HexColor("#555577")))

    # Action buttons
    _draw_button(d, W * 0.15, 4, W * 0.3, 14, "Compose", accent=True)
    _draw_button(d, W * 0.55, 4, W * 0.3, 14, "Re-roll")

    return d


def diagram_timeline_detail():
    """Section 5: Timeline + mixer detail."""
    W = USABLE_W
    H = 170
    d = Drawing(W, H)

    d.add(Rect(0, 0, W, H, rx=4, ry=4, fillColor=HexColor("#1a1a2e"),
               strokeColor=HexColor("#3a3a55"), strokeWidth=1.5))

    # Mixer area
    mixer_w = 65
    d.add(Rect(3, 3, mixer_w, H - 6, rx=2, ry=2,
               fillColor=HexColor("#252536"), strokeColor=HexColor("#3a3a55"), strokeWidth=0.5))
    d.add(String(mixer_w / 2 + 3, H - 12, "MIXER", textAnchor="middle",
                 fontSize=7, fontName="Helvetica-Bold", fillColor=HexColor("#aaaacc")))

    track_colors = [C_TRACK1, C_TRACK2, C_TRACK3, C_TRACK4]
    lane_h = (H - 30) / 4
    lane_x = mixer_w + 10
    lane_w = W - mixer_w - 16

    import random
    rng = random.Random(99)

    for i in range(4):
        y_base = H - 22 - i * lane_h
        color = track_colors[i]

        # Mixer strip
        mx = 8
        my = y_base - lane_h + 5
        d.add(String(mx, y_base - 4, f"Track {i+1}", fontSize=6,
                     fontName="Helvetica-Bold", fillColor=color))
        # M/S buttons
        d.add(Rect(mx, my + lane_h - 18, 14, 10, rx=2, ry=2,
                    fillColor=HexColor("#333350"), strokeColor=C_BORDER, strokeWidth=0.5))
        d.add(String(mx + 7, my + lane_h - 15, "M", textAnchor="middle",
                     fontSize=5, fillColor=HexColor("#aaaacc")))
        d.add(Rect(mx + 17, my + lane_h - 18, 14, 10, rx=2, ry=2,
                    fillColor=HexColor("#333350"), strokeColor=C_BORDER, strokeWidth=0.5))
        d.add(String(mx + 24, my + lane_h - 15, "S", textAnchor="middle",
                     fontSize=5, fillColor=HexColor("#aaaacc")))
        # Volume slider (vertical)
        vol_x = mx + 42
        d.add(Line(vol_x, my + 4, vol_x, my + lane_h - 20,
                   strokeColor=C_BORDER, strokeWidth=1.5))
        d.add(Circle(vol_x, my + lane_h * 0.4, 3, fillColor=color, strokeColor=color))

        # Lane separator
        d.add(Line(lane_x, y_base - lane_h + 2, lane_x + lane_w, y_base - lane_h + 2,
                   strokeColor=HexColor("#2a2a3e"), strokeWidth=0.5))

        # Ruler (on top track only)
        if i == 0:
            for sec in range(8):
                tx = lane_x + sec * lane_w / 8
                d.add(Line(tx, H - 15, tx, H - 20,
                           strokeColor=HexColor("#555577"), strokeWidth=0.5))
                d.add(String(tx + 2, H - 13, f"{sec*10}s", fontSize=4,
                             fillColor=HexColor("#666688")))

        # Audio event blocks
        for j in range(rng.randint(2, 5)):
            bx = lane_x + rng.random() * lane_w * 0.75
            bw = 15 + rng.random() * 50
            by = y_base - lane_h + 6
            bh = lane_h - 12
            d.add(Rect(bx, by, bw, bh, rx=2, ry=2,
                       fillColor=color, strokeColor=None, fillOpacity=0.55))
            # Source name inside block
            names = ["piano", "cello", "noise"]
            d.add(String(bx + bw/2, by + bh/2 - 2, rng.choice(names),
                         textAnchor="middle", fontSize=4, fillColor=white))

    return d


def diagram_signal_flow():
    """Section 8: Data flow pipeline."""
    W = USABLE_W
    H = 75
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=HexColor("#FAFAFA"), strokeColor=C_LIGHT, strokeWidth=0.5))

    boxes = [
        ("Sources\n(audio files)", HexColor("#FEF3C7"), HexColor("#D97706")),
        ("Constraints\n(GUI params)", HexColor("#E0E7FF"), HexColor("#4F46E5")),
        ("Arranger\n+ Strategy", HexColor("#D1FAE5"), HexColor("#059669")),
        ("Composition\n(timeline)", HexColor("#FCE7F3"), HexColor("#DB2777")),
        ("Renderer\n(.render())", HexColor("#FEE2E2"), HexColor("#DC2626")),
        ("Export\n(.wav/.mp3)", HexColor("#F3F4F6"), C_DARK),
    ]

    bw = (W - 60) / len(boxes)
    gap = 6
    by = 18
    bh = 36

    for i, (label, fill, stroke) in enumerate(boxes):
        bx = 8 + i * (bw + gap)
        d.add(Rect(bx, by, bw, bh, rx=4, ry=4, fillColor=fill,
                    strokeColor=stroke, strokeWidth=1.2))
        lines = label.split("\n")
        d.add(String(bx + bw/2, by + bh/2 + 4, lines[0],
                     textAnchor="middle", fontSize=7, fontName="Helvetica-Bold",
                     fillColor=stroke))
        d.add(String(bx + bw/2, by + bh/2 - 6, lines[1],
                     textAnchor="middle", fontSize=6, fillColor=stroke))
        # Arrow
        if i < len(boxes) - 1:
            ax1 = bx + bw
            ax2 = bx + bw + gap
            ay = by + bh / 2
            d.add(Line(ax1, ay, ax2 - 4, ay, strokeColor=C_DARK, strokeWidth=1.5))
            _arrow_head(d, ax2, ay, "right", size=4, color=C_DARK)

    d.add(String(W/2, by + bh + 12, "Pipeline de datos: carga → composicion → render → exportacion",
                 textAnchor="middle", fontSize=7, fontName="Helvetica-Bold", fillColor=C_DARK))

    return d


# ─────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        "UI_Wireframe_AleatoricComposer.pdf",
        pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Aleatoric Composer - UI Wireframe",
    )
    story = []

    # ── COVER ──
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("Aleatoric Composer<br/>Esquema UI", s_title))
    story.append(Paragraph(
        "Wireframe completo de la interfaz actual (v0.1-beta)<br/>"
        "Documento de referencia para rediseno GUI", s_subtitle))

    for item in [
        "1. Layout General de la Ventana",
        "2. Panel SOURCES (izquierda)",
        "3. Tab COMPOSITION (pestana derecha)",
        "4. Tab EFFECTS PALETTE (pestana derecha)",
        "5. TIMELINE + Mixer (zona inferior)",
        "6. Transport Bar (barra inferior)",
        "7. Arbol de Widgets",
        "8. Flujo de Datos (signal flow)",
    ]:
        story.append(Paragraph(item, ParagraphStyle("toc", parent=s_body, leftIndent=5*mm)))
    story.append(PageBreak())

    # ── 1. LAYOUT GENERAL ──
    story.append(Paragraph("1. Layout General de la Ventana", s_h1))
    story.append(Paragraph(
        "Ventana principal: 1400x900px (redimensionable, minimo 1200x800). "
        "Tres zonas principales separadas por QSplitters.", s_body))
    story.append(diagram_layout())
    story.append(Paragraph(
        "<i>Wireframe 1: Layout general con las 3 zonas principales. "
        "Los colores de los bloques del timeline corresponden a cada source.</i>", s_caption))

    story.append(make_table(
        ["Zona", "Widget Qt", "Tamano", "Contenido"],
        [
            ["Panel SOURCES", "SourcePanel", "280-400px ancho", "Lista de audio + waveforms + pesos"],
            ["Pestanas derecha", "QTabWidget (2 tabs)", "Resto del ancho", "Composition + Effects Palette"],
            ["Timeline", "TimelineView", "Parte inferior (splitter V)", "Vista multipista + mixer strips"],
            ["Transport Bar", "QWidget + QHBoxLayout", "Ancho completo, 32px", "Render + progreso + Export"],
        ],
        [15, 22, 22, 41]))
    story.append(PageBreak())

    # ── 2. SOURCES ──
    story.append(Paragraph("2. Panel SOURCES (Izquierda)", s_h1))
    story.append(Paragraph(
        "Gestiona los archivos de audio cargados. Soporta drag &amp; drop. "
        "Cada source muestra nombre, info tecnica, waveform y slider de peso.", s_body))
    story.append(diagram_sources_detail())
    story.append(Paragraph(
        "<i>Wireframe 2: Panel Sources con 3 archivos cargados. Cada uno tiene waveform mini y slider de peso.</i>",
        s_caption))
    story.append(make_table(
        ["Control", "Widget Qt", "Funcion"],
        [
            ["+ Add files", "QPushButton", "Abre QFileDialog para .wav, .mp3, .flac, .ogg, .aiff"],
            ["- Remove", "QPushButton", "Elimina el source seleccionado"],
            ["Nombre archivo", "QLabel (bold, color)", "Color asignado de TRACK_COLORS"],
            ["Info tecnica", "QLabel", "Duracion | canales | sample rate"],
            ["Waveform", "WaveformWidget (custom)", "Miniatura de la onda, coloreada por source"],
            ["Weight slider", "QSlider (0-100)", "Peso relativo en la composicion (0.0-1.0)"],
            ["Drag &amp; drop", "dragEnterEvent", "Acepta archivos de audio soltados"],
        ],
        [18, 22, 60]))
    story.append(PageBreak())

    # ── 3. TAB COMPOSITION ──
    story.append(Paragraph("3. Tab COMPOSITION", s_h1))
    story.append(Paragraph(
        "Pestana principal de configuracion. Controles agrupados en 5 secciones (QGroupBox).",
        s_body))
    story.append(diagram_composition_tab())
    story.append(Paragraph(
        "<i>Wireframe 3: Tab Composition con todos los controles agrupados.</i>", s_caption))
    story.append(make_table(
        ["Grupo", "Control", "Widget", "Rango", "Default"],
        [
            ["General", "Strategy", "QComboBox", "scatter, structured, layer, canon", "scatter"],
            ["General", "Seed", "QSpinBox + QPushButton", "0-2,147,483,647", "42"],
            ["General", "Duration", "QDoubleSpinBox", "1.0-3600.0 s", "120.0"],
            ["General", "Tracks", "QSpinBox", "1-16", "4"],
            ["Timing", "Event duration", "RangeSlider", "0.01-60.0 s", "0.5-30.0"],
            ["Timing", "Silence gap", "RangeSlider", "0.0-30.0 s", "0.0-5.0"],
            ["Timing", "Allow overlap", "QCheckBox", "on/off", "on"],
            ["Dynamics", "Amplitude", "RangeSlider", "0.0-1.0", "0.3-1.0"],
            ["Dynamics", "Pan", "RangeSlider", "-1.0-1.0", "-1.0-1.0"],
            ["Dynamics", "Fade in", "RangeSlider", "0.001-2.0 s", "0.01-0.5"],
            ["Dynamics", "Fade out", "RangeSlider", "0.001-2.0 s", "0.01-1.0"],
            ["Effects", "Probability", "LabeledSlider", "0.0-1.0", "0.70"],
            ["Effects", "Max per event", "QSpinBox", "1-10", "3"],
            ["Structure", "Density curve", "QComboBox", "constant, cresc, decresc, arc, wave", "constant"],
        ],
        [12, 14, 18, 30, 26]))
    story.append(PageBreak())

    # ── 4. EFFECTS ──
    story.append(Paragraph("4. Tab EFFECTS PALETTE", s_h1))
    story.append(Paragraph(
        "Configura los parametros por defecto de cada tipo de efecto. "
        "Al seleccionar un efecto en el combo, aparecen sus sliders.", s_body))
    story.append(make_table(
        ["Efecto", "Parametros", "Rangos"],
        [
            ["reverb", "room_size, damping, wet_level, dry_level, width", "Todos 0.0-1.0"],
            ["delay", "delay_seconds, feedback, mix", "0.01-2.0s, 0-1, 0-1"],
            ["pitch_shift", "semitones", "-24 a +24"],
            ["distortion", "drive_db", "0-100 dB"],
            ["compressor", "threshold_db, ratio, attack_ms, release_ms", "-60-0dB, 1-20, 0.1-100ms"],
            ["gain", "gain_db", "-60 a +30 dB"],
            ["limiter", "threshold_db, release_ms", "-60-0dB, 10-1000ms"],
            ["chorus", "rate_hz, depth, mix", "0.1-10Hz, 0-1, 0-1"],
            ["phaser", "rate_hz, depth, mix", "0.1-10Hz, 0-1, 0-1"],
            ["highpass / lowpass", "cutoff_hz", "20-20000 Hz"],
            ["granular", "grain_size, density, spray, pitch_var, ...", "13 parametros"],
        ],
        [16, 42, 42]))

    # ── 5. TIMELINE ──
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("5. TIMELINE + Mixer Strips", s_h1))
    story.append(Paragraph(
        "La zona inferior muestra la composicion como bloques coloreados sobre un timeline horizontal.",
        s_body))
    story.append(diagram_timeline_detail())
    story.append(Paragraph(
        "<i>Wireframe 5: Timeline con 4 tracks, mixer strips (M/S/vol), y bloques de audio coloreados por source.</i>",
        s_caption))
    story.append(PageBreak())

    # ── 6. TRANSPORT ──
    story.append(Paragraph("6. Transport Bar", s_h1))
    story.append(Paragraph(
        "Barra fija en la parte inferior. Render, barra de progreso y botones de exportacion.", s_body))
    story.append(make_table(
        ["Control", "Widget", "Funcion", "Estado"],
        [
            ["Render", "QPushButton (#accent)", "Renderiza composicion a audio",
             "Se deshabilita durante render"],
            ["Progress Bar", "QProgressBar (0-100)", "Progreso del render",
             "Actualizado via signal"],
            ["Export WAV", "QPushButton", "Exporta a .wav", "Solo si hay audio renderizado"],
            ["Export MP3", "QPushButton", "Exporta a .mp3", "Solo si hay audio renderizado"],
        ],
        [14, 20, 30, 36]))

    # ── 7. WIDGET TREE ──
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("7. Arbol de Widgets", s_h1))
    story.append(Paragraph(
        "Jerarquia completa de widgets en la aplicacion:", s_body))

    tree_data = [
        ["MainWindow (QMainWindow)", "", "Ventana principal 1400x900"],
        ["  MenuBar", "", "File | Composition"],
        ["  QSplitter (Vertical)", "", "Separa panels / timeline"],
        ["    QSplitter (Horizontal)", "", "Separa sources / tabs"],
        ["      SourcePanel", "280-400px", "Lista de archivos + waveforms + weights"],
        ["      QTabWidget", "Resto", "2 pestanas"],
        ["        CompositionPanel", "Tab 1", "5 QGroupBox con controles"],
        ["        EffectsPalettePanel", "Tab 2", "Combo + sliders dinamicos"],
        ["    TimelineView", "Zona inferior", "Mixer + canvas multipista"],
        ["      MixerStrip (x N)", "80px c/u", "Nombre + M/S + vol + pan"],
        ["      ArrangementCanvas", "Resto", "paintEvent con bloques de audio"],
        ["  Transport Bar", "32px alto", "Render + progress + export"],
        ["  QLabel copyright", "14px", "(c) Alvaro Hernandez Altozano 2026"],
    ]
    story.append(make_table(
        ["Widget", "Tamano", "Contenido"],
        [[PB(r[0]), r[1], r[2]] for r in tree_data],
        [35, 15, 50]))

    story.append(PageBreak())

    # ── 8. SIGNAL FLOW ──
    story.append(Paragraph("8. Flujo de Datos (Signal Flow)", s_h1))
    story.append(Paragraph(
        "Como se comunican los componentes desde la carga de audio hasta la exportacion:", s_body))
    story.append(diagram_signal_flow())
    story.append(Paragraph(
        "<i>Diagrama: Pipeline de datos Sources → Arranger → Composition → Renderer → Export.</i>",
        s_caption))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("<b>Senales Qt principales:</b>", s_body))
    story.append(make_table(
        ["Accion usuario", "Signal", "Receptor"],
        [
            ["Click Compose", "compose_requested", "MainWindow._on_compose()"],
            ["Click Re-roll", "reroll_requested", "MainWindow._on_reroll()"],
            ["Click Render", "clicked", "MainWindow._on_render() → RenderWorker"],
            ["RenderWorker progreso", "progress(float)", "QProgressBar.setValue()"],
            ["RenderWorker fin", "finished(ndarray)", "Almacena audio renderizado"],
            ["Click Export WAV/MP3", "clicked", "QFileDialog + export()"],
            ["Cambiar density curve", "currentTextChanged", "DensityCurvePreview.set_curve()"],
            ["Mute/Solo toggle", "toggled", "track.muted / track.solo"],
        ],
        [22, 22, 56]))

    doc.build(story)
    print(f"PDF generado: {doc.filename}")


if __name__ == "__main__":
    build_pdf()
