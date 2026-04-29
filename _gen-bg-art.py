"""Generate 15 background-art SVGs for the Hadeel Algheshaian portfolio.
Lean: Najdi / Arabic-geometric heavy.
  1-8  : Arabic-geometric tessellations + compass roses (8 pieces)
  9-13 : Architectural pieces — floor plans, elevations, dimension lines (5 pieces)
  14-15: Perspective room + furniture joinery (2 pieces)

All SVGs are 512x512, transparent background, stroke="black" with no fill,
designed to be used as CSS mask-image so the surrounding theme tints them
via background-color.
"""
from __future__ import annotations
import math
import os
from pathlib import Path

OUT = Path(__file__).parent / "brand" / "background-art"
OUT.mkdir(parents=True, exist_ok=True)

W = 512
HDR = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" '
    f'fill="none" stroke="black" stroke-width="1.4" stroke-linecap="round" '
    f'stroke-linejoin="round">\n'
)
FTR = "</svg>\n"


def write(idx: int, body: str) -> None:
    (OUT / f"{idx}.svg").write_text(HDR + body + FTR, encoding="utf-8")


# ---------- helpers ----------
def polyline(points: list[tuple[float, float]], close: bool = False) -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    tag = "polygon" if close else "polyline"
    return f'<{tag} points="{pts}" />\n'


def line(x1, y1, x2, y2) -> str:
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" />\n'


def circle(cx, cy, r) -> str:
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />\n'


def rect(x, y, w, h) -> str:
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" />\n'


def text(x, y, s, size=10, anchor="middle") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="serif" font-size="{size}" '
        f'text-anchor="{anchor}" fill="black" stroke="none">{s}</text>\n'
    )


# ---------- 1. Eight-pointed-star tessellation (Najdi classic) ----------
def gen_1():
    body = ""
    cell = 96
    cols = rows = W // cell + 1
    for r in range(rows):
        for c in range(cols):
            cx, cy = c * cell + cell / 2, r * cell + cell / 2
            # 8-point star: two overlaid squares rotated 45°
            sz = cell * 0.42
            body += (
                f'<rect x="{cx - sz:.2f}" y="{cy - sz:.2f}" width="{2 * sz:.2f}" '
                f'height="{2 * sz:.2f}" />\n'
            )
            body += (
                f'<rect x="{cx - sz:.2f}" y="{cy - sz:.2f}" width="{2 * sz:.2f}" '
                f'height="{2 * sz:.2f}" transform="rotate(45 {cx:.2f} {cy:.2f})" />\n'
            )
            body += circle(cx, cy, sz * 0.42)
    write(1, body)


# ---------- 2. Twelve-point Islamic rosette (single large) ----------
def gen_2():
    cx, cy = W / 2, W / 2
    R = 220
    body = circle(cx, cy, R)
    body += circle(cx, cy, R * 0.66)
    body += circle(cx, cy, R * 0.33)
    # 12 spokes
    for k in range(12):
        a = math.radians(k * 30)
        body += line(cx, cy, cx + R * math.cos(a), cy + R * math.sin(a))
    # Outer 12-pointed star
    pts = []
    for k in range(24):
        a = math.radians(k * 15 - 90)
        rr = R if k % 2 == 0 else R * 0.78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    body += polyline(pts, close=True)
    # Inner rosette petals
    for k in range(12):
        a = math.radians(k * 30)
        x1 = cx + R * 0.33 * math.cos(a)
        y1 = cy + R * 0.33 * math.sin(a)
        x2 = cx + R * 0.66 * math.cos(a + math.radians(15))
        y2 = cy + R * 0.66 * math.sin(a + math.radians(15))
        body += line(x1, y1, x2, y2)
    write(2, body)


# ---------- 3. Hexagonal lattice with star inserts ----------
def gen_3():
    body = ""
    side = 56
    h = side * math.sqrt(3) / 2
    for row in range(-1, int(W / h) + 2):
        for col in range(-1, int(W / (side * 1.5)) + 2):
            cx = col * side * 1.5
            cy = row * 2 * h + (h if col % 2 else 0)
            pts = [
                (cx + side * math.cos(math.radians(60 * k)),
                 cy + side * math.sin(math.radians(60 * k)))
                for k in range(6)
            ]
            body += polyline(pts, close=True)
            # Star insert at center of every other hex
            if (row + col) % 2 == 0:
                inner = [
                    (cx + side * 0.45 * math.cos(math.radians(60 * k + 30)),
                     cy + side * 0.45 * math.sin(math.radians(60 * k + 30)))
                    for k in range(6)
                ]
                body += polyline(inner, close=True)
    write(3, body)


# ---------- 4. Mamluk-style interlace ----------
def gen_4():
    body = ""
    cell = 128
    n = W // cell + 1
    for r in range(n):
        for c in range(n):
            cx, cy = c * cell + cell / 2, r * cell + cell / 2
            sz = cell * 0.42
            # Interlocking diamonds
            body += polyline(
                [(cx, cy - sz), (cx + sz, cy), (cx, cy + sz), (cx - sz, cy)],
                close=True,
            )
            body += polyline(
                [(cx, cy - sz * 0.6), (cx + sz * 0.6, cy),
                 (cx, cy + sz * 0.6), (cx - sz * 0.6, cy)],
                close=True,
            )
            # Connector ribs to neighbours
            body += line(cx, cy - sz, cx, cy - cell + sz)
            body += line(cx, cy + sz, cx, cy + cell - sz)
            body += line(cx - sz, cy, cx - cell + sz, cy)
            body += line(cx + sz, cy, cx + cell - sz, cy)
    write(4, body)


# ---------- 5. Najdi triangular window pattern ----------
def gen_5():
    body = ""
    # Vertical strips of stacked triangles, like the openings of mud-brick walls
    strip_w = 48
    tri_h = 56
    cols = W // strip_w + 1
    rows = W // tri_h + 1
    for c in range(cols):
        x = c * strip_w
        body += line(x, 0, x, W)  # vertical column line
        for r in range(rows):
            y = r * tri_h
            # Triangle pointing inward (alternating)
            if (c + r) % 2 == 0:
                body += polyline(
                    [(x, y), (x + strip_w, y), (x + strip_w / 2, y + tri_h * 0.7)],
                    close=True,
                )
            else:
                body += polyline(
                    [(x, y + tri_h), (x + strip_w, y + tri_h),
                     (x + strip_w / 2, y + tri_h * 0.3)],
                    close=True,
                )
    body += line(W, 0, W, W)
    body += line(0, 0, W, 0)
    body += line(0, W, W, W)
    write(5, body)


# ---------- 6. 8-point compass rose with cardinals ----------
def gen_6():
    cx, cy = W / 2, W / 2
    R = 220
    body = circle(cx, cy, R)
    body += circle(cx, cy, R * 0.85)
    body += circle(cx, cy, R * 0.45)
    body += circle(cx, cy, 8)
    # 8 long points + 8 short between
    pts = []
    for k in range(16):
        a = math.radians(k * 22.5 - 90)
        rr = R * 0.95 if k % 2 == 0 else R * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    body += polyline(pts, close=True)
    # Inner cardinals as triangles
    for k in range(4):
        a = math.radians(k * 90 - 90)
        a1 = a - math.radians(8)
        a2 = a + math.radians(8)
        body += polyline(
            [(cx + R * 0.95 * math.cos(a), cy + R * 0.95 * math.sin(a)),
             (cx + R * 0.30 * math.cos(a1), cy + R * 0.30 * math.sin(a1)),
             (cx + R * 0.30 * math.cos(a2), cy + R * 0.30 * math.sin(a2))],
            close=True,
        )
    # Cardinal letters
    for label, ang in [("N", -90), ("E", 0), ("S", 90), ("W", 180)]:
        a = math.radians(ang)
        body += text(cx + (R + 16) * math.cos(a),
                     cy + (R + 16) * math.sin(a) + 4,
                     label, size=14)
    # Ticks at 5° intervals
    for k in range(72):
        a = math.radians(k * 5 - 90)
        rr1 = R if k % 9 != 0 else R - 6
        rr2 = R + 6
        body += line(cx + rr1 * math.cos(a), cy + rr1 * math.sin(a),
                     cx + rr2 * math.cos(a), cy + rr2 * math.sin(a))
    write(6, body)


# ---------- 7. 16-point classical compass rose ----------
def gen_7():
    cx, cy = W / 2, W / 2
    R = 220
    body = circle(cx, cy, R)
    body += circle(cx, cy, R * 0.6)
    body += circle(cx, cy, R * 0.25)
    # 16 long points
    pts = []
    for k in range(32):
        a = math.radians(k * 11.25 - 90)
        rr = R if k % 2 == 0 else R * 0.55
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    body += polyline(pts, close=True)
    # 4 main diamond-arms
    for k in range(4):
        a = math.radians(k * 90 - 90)
        a1 = a - math.radians(6)
        a2 = a + math.radians(6)
        body += polyline(
            [(cx, cy),
             (cx + R * math.cos(a1), cy + R * math.sin(a1)),
             (cx + R * 0.95 * math.cos(a), cy + R * 0.95 * math.sin(a)),
             (cx + R * math.cos(a2), cy + R * math.sin(a2))],
            close=True,
        )
    # Crosshair through centre
    body += line(cx - R, cy, cx + R, cy)
    body += line(cx, cy - R, cx, cy + R)
    write(7, body)


# ---------- 8. Square-rotated 4-fold tessellation ----------
def gen_8():
    body = ""
    cell = 80
    n = W // cell + 2
    for r in range(n):
        for c in range(n):
            cx, cy = c * cell, r * cell
            sz = cell * 0.5
            # Outer square
            body += rect(cx - sz, cy - sz, 2 * sz, 2 * sz)
            # Rotated inner square (45°)
            body += polyline(
                [(cx, cy - sz), (cx + sz, cy), (cx, cy + sz), (cx - sz, cy)],
                close=True,
            )
            # Inner cross
            body += line(cx - sz * 0.5, cy, cx + sz * 0.5, cy)
            body += line(cx, cy - sz * 0.5, cx, cy + sz * 0.5)
    write(8, body)


# ---------- 9. Floor plan (residential, axonometric) ----------
def gen_9():
    body = ""
    # Outer envelope
    body += rect(48, 64, 416, 384)
    # Inner walls — partitions
    body += line(48, 224, 280, 224)         # horizontal divider
    body += line(280, 64, 280, 448)         # vertical divider
    body += line(280, 320, 464, 320)        # second floor partition
    body += line(160, 224, 160, 448)        # bedroom split
    # Door arcs
    def door(cx, cy, r, a_start, a_end):
        steps = 12
        pts = []
        for i in range(steps + 1):
            a = math.radians(a_start + (a_end - a_start) * i / steps)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return polyline(pts)
    body += door(170, 224, 32, 180, 270)    # bedroom door
    body += door(280, 230, 32, 270, 360)    # passage door
    body += door(380, 320, 32, 180, 270)    # kitchen door
    # Furniture stubs
    body += rect(80, 96, 80, 50)            # sofa
    body += rect(80, 156, 80, 50)
    body += rect(190, 96, 70, 110)          # console
    body += rect(310, 96, 130, 80)          # dining table
    body += rect(310, 200, 50, 100)         # bed
    body += rect(370, 200, 50, 100)
    body += circle(380, 380, 22)            # kitchen island circle
    body += rect(80, 260, 60, 60)           # bath fixtures
    body += rect(80, 340, 60, 60)
    body += rect(180, 260, 80, 50)
    # Dimension ticks
    for x in [48, 160, 280, 464]:
        body += line(x, 30, x, 50)
    body += line(48, 40, 464, 40)
    body += text(256, 26, "FLOOR PLAN — RESIDENCE", size=11)
    write(9, body)


# ---------- 10. Architectural elevation with dimensions ----------
def gen_10():
    body = ""
    # Building profile
    body += rect(64, 160, 384, 256)
    # Ground line with hatching
    for x in range(0, W, 12):
        body += line(x, 416, x - 8, 432)
    body += line(0, 416, W, 416)
    # Storey divisions
    body += line(64, 248, 448, 248)
    body += line(64, 336, 448, 336)
    # Windows — 3 storeys × 5 bays
    for sy in [180, 268, 356]:
        for bx in range(5):
            x = 88 + bx * 72
            body += rect(x, sy, 36, 48)
            body += line(x + 18, sy, x + 18, sy + 48)
            body += line(x, sy + 24, x + 36, sy + 24)
    # Roof parapet
    body += polyline([(56, 160), (456, 160), (456, 144), (56, 144)], close=True)
    # Dimension lines top
    body += line(64, 100, 448, 100)
    body += line(64, 96, 64, 156)
    body += line(448, 96, 448, 156)
    body += line(64, 100, 70, 96)
    body += line(64, 100, 70, 104)
    body += line(448, 100, 442, 96)
    body += line(448, 100, 442, 104)
    body += text(256, 92, "12.000", size=11)
    # Vertical dim
    body += line(490, 160, 490, 416)
    body += line(486, 160, 494, 160)
    body += line(486, 416, 494, 416)
    body += text(498, 290, "8.0", size=11, anchor="start")
    body += text(256, 60, "NORTH ELEVATION", size=11)
    write(10, body)


# ---------- 11. Drafting tools — compass + T-square + triangle ----------
def gen_11():
    body = ""
    # T-square horizontal
    body += rect(48, 96, 416, 18)
    body += rect(40, 88, 22, 80)
    # 45° triangle
    body += polyline([(120, 200), (320, 200), (120, 400)], close=True)
    # 30/60 triangle inside
    body += polyline([(180, 240), (300, 240), (180, 380)], close=True)
    # Draftsman's compass
    cx, cy = 380, 320
    body += line(cx, cy - 100, cx - 50, cy + 60)         # left leg
    body += line(cx, cy - 100, cx + 50, cy + 60)         # right leg
    body += circle(cx, cy - 100, 6)                      # hinge
    body += line(cx - 50, cy + 60, cx - 56, cy + 78)     # pencil tip
    body += line(cx + 50, cy + 60, cx + 56, cy + 78)
    # Arc the compass would draw
    pts = []
    for k in range(25):
        a = math.radians(120 + k * 60 / 24)
        pts.append((cx + 110 * math.cos(a), cy - 100 + 110 * math.sin(a)))
    body += polyline(pts)
    # Gridded paper
    for x in range(48, 465, 32):
        body += line(x, 440, x, 470)
    for y in range(440, 471, 8):
        body += line(48, y, 464, y)
    write(11, body)


# ---------- 12. Building section with hatching ----------
def gen_12():
    body = ""
    # Floor slab
    body += rect(48, 380, 416, 28)
    # Hatch slab
    for x in range(48, 464, 12):
        body += line(x, 380, x + 12, 408)
    # Walls
    body += rect(64, 96, 22, 284)
    body += rect(426, 96, 22, 284)
    # Roof slab
    body += polyline([(48, 80), (464, 80), (440, 96), (72, 96)], close=True)
    # Internal floors
    body += rect(86, 220, 340, 14)
    for x in range(86, 426, 10):
        body += line(x, 220, x + 10, 234)
    # Furniture in section
    body += rect(120, 332, 90, 48)         # sofa
    body += rect(240, 332, 70, 48)         # chair
    body += rect(330, 332, 80, 48)         # table
    body += rect(120, 172, 60, 48)
    body += rect(220, 172, 100, 48)
    # People silhouettes
    body += circle(170, 320, 8)
    body += line(170, 328, 170, 360)
    body += line(170, 336, 158, 354)
    body += line(170, 336, 182, 354)
    body += circle(360, 320, 8)
    body += line(360, 328, 360, 360)
    body += line(360, 336, 352, 354)
    body += line(360, 336, 368, 354)
    # Section line marker
    body += line(0, 96, 48, 96)
    body += line(0, 380, 48, 380)
    body += text(256, 60, "SECTION A–A", size=11)
    write(12, body)


# ---------- 13. Detailed dimension study ----------
def gen_13():
    body = ""
    # Plan piece
    body += rect(96, 160, 320, 200)
    body += line(96, 240, 416, 240)
    body += line(216, 160, 216, 360)
    body += line(316, 160, 316, 360)
    # Dimension stack
    def dim(y, x1, x2, label):
        s = ""
        s += line(x1, y, x2, y)
        s += line(x1, y - 6, x1, y + 6)
        s += line(x2, y - 6, x2, y + 6)
        s += text((x1 + x2) / 2, y - 4, label, size=10)
        return s
    body += dim(120, 96, 216, "1.200")
    body += dim(120, 216, 316, "1.000")
    body += dim(120, 316, 416, "1.000")
    body += dim(80, 96, 416, "3.200")
    # Side dimensions
    def vdim(x, y1, y2, label):
        s = ""
        s += line(x, y1, x, y2)
        s += line(x - 6, y1, x + 6, y1)
        s += line(x - 6, y2, x + 6, y2)
        s += f'<text x="{x + 4:.2f}" y="{(y1 + y2) / 2:.2f}" font-family="serif" font-size="10" fill="black" stroke="none">{label}</text>\n'
        return s
    body += vdim(440, 160, 240, "0.800")
    body += vdim(440, 240, 360, "1.200")
    body += vdim(470, 160, 360, "2.000")
    # Detail bubbles
    body += circle(216, 240, 18)
    body += text(216, 244, "01", size=10)
    body += circle(316, 240, 18)
    body += text(316, 244, "02", size=10)
    body += text(256, 400, "DIMENSION STUDY", size=11)
    write(13, body)


# ---------- 14. 1-pt perspective room ----------
def gen_14():
    cx, cy = W / 2, W / 2 + 16
    body = ""
    # Outer frame (front of room)
    body += rect(48, 96, 416, 320)
    # Vanishing point
    body += circle(cx, cy, 3)
    # Ceiling, floor, side wall lines to VP
    corners = [(48, 96), (464, 96), (464, 416), (48, 416)]
    for x, y in corners:
        body += line(x, y, cx, cy)
    # Back wall (inset)
    bw = 0.42  # depth scale
    bx1 = 48 + (cx - 48) * bw
    by1 = 96 + (cy - 96) * bw
    bx2 = 464 + (cx - 464) * bw
    by2 = 416 + (cy - 416) * bw
    body += rect(bx1, by1, bx2 - bx1, by2 - by1)
    # Floor tiles
    for k in range(1, 6):
        f = k / 6
        y = 416 + (cy - 416) * f
        body += line(48 + (cx - 48) * f, y,
                     464 + (cx - 464) * f, y)
    # Picture frames on side walls
    body += rect(96, 180, 60, 80)
    body += rect(356, 180, 60, 80)
    # Furniture in back
    body += rect(bx1 + 28, by2 - 50, 40, 30)        # cabinet
    body += rect(bx2 - 70, by2 - 60, 50, 40)        # chair
    body += rect((bx1 + bx2) / 2 - 30, by2 - 26, 60, 16)
    # Window in back wall
    body += rect((bx1 + bx2) / 2 - 30, by1 + 14, 60, 50)
    body += line((bx1 + bx2) / 2, by1 + 14, (bx1 + bx2) / 2, by1 + 64)
    body += line((bx1 + bx2) / 2 - 30, by1 + 39, (bx1 + bx2) / 2 + 30, by1 + 39)
    write(14, body)


# ---------- 15. Chair joinery — orthographic blueprint ----------
def gen_15():
    body = ""
    # Top sheet — plan view
    body += rect(48, 56, 192, 128)
    body += rect(72, 80, 144, 80)               # seat outline
    body += rect(88, 92, 16, 16)                # leg pegs
    body += rect(184, 92, 16, 16)
    body += rect(88, 132, 16, 16)
    body += rect(184, 132, 16, 16)
    body += line(48, 184, 240, 184)
    body += text(144, 50, "PLAN", size=11)

    # Front elevation
    body += rect(272, 56, 192, 200)
    body += rect(304, 96, 128, 80)              # seat back
    body += rect(312, 176, 16, 60)              # legs
    body += rect(408, 176, 16, 60)
    # Joint detail lines
    body += line(304, 96, 304, 176)
    body += line(432, 96, 432, 176)
    body += line(304, 176, 432, 176)
    # Spindles in seat back
    for x in [328, 360, 392]:
        body += line(x, 100, x, 168)
    body += text(368, 50, "FRONT ELEVATION", size=11)

    # Side view
    body += rect(48, 280, 192, 196)
    body += polyline([(80, 312), (208, 312), (208, 432), (80, 432)], close=True)
    body += line(80, 312, 80, 296)
    body += line(80, 296, 96, 296)
    body += line(96, 296, 96, 312)              # seat back top
    body += line(80, 432, 80, 460)
    body += line(208, 432, 208, 460)
    body += text(144, 274, "SIDE", size=11)

    # Detail joint
    body += rect(272, 296, 192, 180)
    body += rect(312, 332, 32, 80)              # tenon
    body += rect(344, 348, 80, 64)              # mortise
    body += line(344, 348, 344, 412)
    body += line(376, 348, 376, 412)
    for y in range(348, 412, 6):
        body += line(344, y, 376, y + 4)
    body += text(368, 290, "MORTISE & TENON DETAIL", size=11)
    write(15, body)


for fn in [gen_1, gen_2, gen_3, gen_4, gen_5, gen_6, gen_7, gen_8,
           gen_9, gen_10, gen_11, gen_12, gen_13, gen_14, gen_15]:
    fn()

print(f"Wrote 15 SVGs to {OUT}")
for f in sorted(OUT.glob("*.svg"), key=lambda p: int(p.stem)):
    print(f"  {f.name}: {f.stat().st_size} bytes")
