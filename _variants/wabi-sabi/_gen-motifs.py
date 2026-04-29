"""Generate 6 Wabi-Sabi motifs for the variant.
All hand-feeling brush gestures, single ink stroke per asset, transparent bg.
"""
from __future__ import annotations
import math
import random
from pathlib import Path

OUT = Path(__file__).parent / "brand" / "background-art"
OUT.mkdir(parents=True, exist_ok=True)

W = 600
HDR = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" '
    f'fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round">\n'
)
FTR = "</svg>\n"


def write(idx: int, body: str) -> None:
    (OUT / f"{idx}.svg").write_text(HDR + body + FTR, encoding="utf-8")


# ---------- 1. Ensō ----------
def gen_1():
    cx, cy = W / 2, W / 2
    r = 220
    rng = random.Random(1)
    pts = []
    for k in range(0, 340, 4):
        a = math.radians(k - 90)
        rr = r + rng.uniform(-6, 6)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    body = f'<path d="{d}" stroke-width="32" />\n'
    body += f'<path d="{d}" stroke-width="14" stroke="black" opacity="0.55" />\n'
    write(1, body)


# ---------- 2. Bamboo ----------
def gen_2():
    rng = random.Random(2)
    body = ""
    for i, x in enumerate([170, 300, 430]):
        x_jit = x + rng.uniform(-12, 12)
        d = f"M {x_jit + rng.uniform(-4, 4):.1f},80 "
        for y in range(120, W - 40, 30):
            d += f"L {x_jit + rng.uniform(-6, 6):.1f},{y} "
        body += f'<path d="{d}" stroke-width="14" />\n'
        for y in [150, 230, 320, 400, 480]:
            body += (
                f'<line x1="{x_jit - 18:.1f}" y1="{y + rng.uniform(-3, 3):.1f}" '
                f'x2="{x_jit + 18:.1f}" y2="{y + rng.uniform(-3, 3):.1f}" stroke-width="6" />\n'
            )
        for ly in [200, 380]:
            ang = rng.uniform(-30, 30)
            body += (
                f'<path d="M {x_jit:.1f},{ly:.1f} q 60 {-20 + rng.uniform(-10, 10):.1f}'
                f' 100 {-50 + rng.uniform(-15, 15):.1f}" stroke-width="8" '
                f'transform="rotate({ang:.1f} {x_jit} {ly})" />\n'
            )
    write(2, body)


# ---------- 3. Mountain silhouette ----------
def gen_3():
    rng = random.Random(3)
    pts_back = [(40, 380)]
    for x in range(40, W - 40, 30):
        y = 380 - (1 - abs((x - W/2) / (W/2))) * 60 + rng.uniform(-12, 12)
        pts_back.append((x, y))
    pts_back.append((W - 40, 380))
    pts_front = [(60, 460)]
    for bx in [120, 240, 360, 480]:
        pts_front.append((bx - 60, 460))
        pts_front.append((bx, 460 - rng.uniform(70, 130)))
        pts_front.append((bx + 60, 460))
    pts_front.append((W - 60, 460))
    def to_path(pts):
        d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
        for x, y in pts[1:]:
            d += f" L {x:.1f},{y:.1f}"
        return d
    body = f'<path d="{to_path(pts_back)}" stroke-width="6" stroke-opacity="0.55" />\n'
    body += f'<path d="{to_path(pts_front)}" stroke-width="10" />\n'
    body += '<circle cx="430" cy="160" r="46" stroke-width="3" stroke-opacity="0.6" />\n'
    write(3, body)


# ---------- 4. Single broad brush stroke ----------
def gen_4():
    rng = random.Random(4)
    pts = [(80, 320)]
    for k in range(1, 16):
        x = 80 + k * 28 + rng.uniform(-8, 8)
        y = 320 + rng.uniform(-30, 50) - k * 8
        pts.append((x, y))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in pts[1:])
    body = f'<path d="{d}" stroke-width="44" stroke-opacity="0.85" />\n'
    body += f'<path d="{d}" stroke-width="22" stroke-opacity="0.45" />\n'
    body += f'<path d="{d}" stroke-width="10" stroke-opacity="0.95" />\n'
    write(4, body)


# ---------- 5. Ink smudge ----------
def gen_5():
    rng = random.Random(5)
    body = ""
    cx, cy = 300, 300
    for _ in range(70):
        x = cx + rng.gauss(0, 90)
        y = cy + rng.gauss(0, 70)
        r = max(2, rng.gauss(8, 5))
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="black" stroke="none" opacity="{rng.uniform(0.3, 0.85):.2f}" />\n'
    body += '<path d="M 90,260 Q 280,140 510,330" stroke-width="20" stroke-opacity="0.6" />\n'
    write(5, body)


# ---------- 6. Plum branch with blossoms ----------
def gen_6():
    body = '<path d="M 60,500 Q 200,420 340,360 T 540,140" stroke-width="10" />\n'
    body += '<path d="M 280,380 q 50,-80 120,-90" stroke-width="6" stroke-opacity="0.7" />\n'
    body += '<path d="M 380,300 q 40,-30 90,-20" stroke-width="5" stroke-opacity="0.7" />\n'
    for cx, cy in [(120, 470), (240, 400), (360, 320), (450, 180), (520, 140), (310, 290), (420, 240)]:
        for k in range(5):
            a = math.radians(k * 72 - 90)
            px = cx + 9 * math.cos(a)
            py = cy + 9 * math.sin(a)
            body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="black" stroke="none" opacity="0.8" />\n'
        body += f'<circle cx="{cx}" cy="{cy}" r="3" fill="black" stroke="none" opacity="0.7" />\n'
    write(6, body)


for fn in [gen_1, gen_2, gen_3, gen_4, gen_5, gen_6]:
    fn()

print(f"Wrote 6 Wabi-Sabi motifs to {OUT}")
for f in sorted(OUT.glob("*.svg"), key=lambda p: int(p.stem)):
    print(f"  {f.name}: {f.stat().st_size} bytes")
