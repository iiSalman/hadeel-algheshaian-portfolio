"""Patch Wabi-Sabi background motifs onto every variant HTML page.

Same idempotent pattern as the root gen-bg.py, but operates on the variant folder
and uses the 6 brush motifs in `brand/background-art/`.
"""
from __future__ import annotations
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
ART_DIR = ROOT / "brand" / "background-art"

HIGH = {"index.html"}
LOW = {"contact.html"}
PROJECT_PAGE_RE = re.compile(r"^project-.+\.html$")

HIGH_POSITIONS = [
    (1,   4,  16),
    (84,  6,  16),
    (2,  22,  18),
    (83, 26,  18),
    (1,  44,  18),
    (84, 48,  18),
    (2,  66,  16),
    (83, 70,  16),
    (3,  86,  16),
    (84, 88,  16),
]
LOW_POSITIONS = [
    (1,  10, 20),
    (84, 22, 18),
    (2,  60, 20),
    (84, 72, 18),
]

CSS_BLOCK = """
/* Dynamic Background System (Wabi-Sabi) */
main.dynamic-bg { position: relative; isolation: isolate; }
.bg-motif {
  position: absolute; aspect-ratio: 1;
  width: var(--size, 28vw); left: var(--x, 50%); top: var(--y, 50%);
  pointer-events: none; z-index: -1;
  background-color: #ECE4D0; opacity: 0.22;
  -webkit-mask: var(--art) center / contain no-repeat;
          mask: var(--art) center / contain no-repeat;
  transform: rotate(var(--rot, 0deg));
}
:root[data-theme="light"] .bg-motif { background-color: #1F1814; opacity: 0.18; }
@media (max-width: 700px) { .bg-motif { width: calc(var(--size, 28vw) * 0.7); opacity: 0.16; } }
"""

START = "<!-- BG-MOTIFS-START -->"
END = "<!-- BG-MOTIFS-END -->"
MOTIF_BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
CSS_MARKER = "/* Dynamic Background System (Wabi-Sabi) */"


def list_assets():
    files = sorted(ART_DIR.glob("*.svg"), key=lambda p: int(p.stem) if p.stem.isdigit() else 1e9)
    return [f"brand/background-art/{f.name}" for f in files if f.stem.isdigit()]


def is_high_density(html_path: Path, html_text: str) -> bool:
    name = html_path.name
    if name in HIGH:
        return True
    if name in LOW:
        return False
    if PROJECT_PAGE_RE.match(name):
        return html_text.count('class="section-header') >= 2
    return False


def build_motifs(rng: random.Random, assets, n: int) -> str:
    positions = HIGH_POSITIONS if n >= 3 else LOW_POSITIONS
    shuffled_assets = list(assets)
    rng.shuffle(shuffled_assets)
    n = min(n, len(positions))
    out = [START]
    for i in range(n):
        art = shuffled_assets[i % len(shuffled_assets)]
        x, y, sz = positions[i]
        x += rng.uniform(-3, 3)
        y += rng.uniform(-3, 3)
        sz += rng.uniform(-2, 2)
        rot = rng.uniform(-15, 15)
        out.append(
            f'  <div class="bg-motif" style="--art:url(\'{art}\'); '
            f'--x:{x:.0f}%; --y:{y:.0f}%; --size:{sz:.0f}vw; --rot:{rot:.0f}deg"></div>'
        )
    out.append(END)
    return "\n".join(out)


def wrap_main_if_needed(html: str) -> str:
    if 'class="dynamic-bg"' in html or 'dynamic-bg"' in html:
        return html
    if "<main" in html:
        html = re.sub(r"<main(\s+[^>]*)?>", lambda m: '<main class="dynamic-bg"' + (m.group(1) or "") + ">", html, count=1)
        return html
    nav_end = html.find("</nav>")
    if nav_end == -1:
        return html
    body_close = html.rfind("</body>")
    if body_close == -1:
        return html
    after_nav = nav_end + len("</nav>")
    chunk = html[after_nav:body_close]
    return html[:after_nav] + '\n<main class="dynamic-bg">\n' + chunk + '\n</main>\n' + html[body_close:]


def patch_css(html: str) -> str:
    if CSS_MARKER in html:
        return html
    head_close = html.find("</style>")
    if head_close == -1:
        return html
    return html[:head_close] + CSS_BLOCK + html[head_close:]


def patch_motifs(html: str, motif_html: str) -> str:
    if MOTIF_BLOCK_RE.search(html):
        return MOTIF_BLOCK_RE.sub(motif_html, html, count=1)
    m = re.search(r'(<main class="dynamic-bg"[^>]*>)', html)
    if m:
        idx = m.end()
        return html[:idx] + "\n" + motif_html + "\n" + html[idx:]
    return html


def main():
    assets = list_assets()
    if not assets:
        print("No motifs found.")
        return
    print(f"Asset pool: {assets}")
    targets = [p for p in ROOT.glob("*.html") if not p.name.startswith("_")]
    for path in sorted(targets):
        html = path.read_text(encoding="utf-8")
        original = html
        html = wrap_main_if_needed(html)
        html = patch_css(html)
        rng = random.Random(path.stem + "-wabi")
        n = 8 if is_high_density(path, html) else 1
        motif_html = build_motifs(rng, assets, n)
        html = patch_motifs(html, motif_html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"  patched {path.name}: {n} motif(s)")
        else:
            print(f"  unchanged {path.name}")


if __name__ == "__main__":
    main()
