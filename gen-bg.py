"""Patch the dynamic-background motifs into all HTML pages.

Picks 1 motif (low-density pages: contact + single-section project pages)
or 3 motifs (high-density pages: index + multi-section project pages)
from /brand/background-art/*.svg and inserts them as positioned `.bg-motif`
divs inside <main class="dynamic-bg"> on each page.

Re-runs idempotently — replaces content between
  <!-- BG-MOTIFS-START --> ... <!-- BG-MOTIFS-END -->
and patches CSS only on first run (marker: `/* Dynamic Background System */`).
"""
from __future__ import annotations
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
ART_DIR = ROOT / "brand" / "background-art"

# Pages that need backgrounds, with density classification
HIGH = {"index.html"}  # always high-density
LOW = {"contact.html"}  # always low

# Project pages: high-density if multiple sections, low if one or fewer
PROJECT_PAGE_RE = re.compile(r"^project-.+\.html$")

# Wide-margin position envelopes (left%, top%, size_vw)
HIGH_POSITIONS = [
    (1,   4,  16),   # top-left gutter
    (84,  6,  16),   # top-right gutter
    (2,  22,  18),   # upper-left gutter
    (83, 26,  18),   # upper-right gutter
    (1,  44,  18),   # mid-left gutter
    (84, 48,  18),   # mid-right gutter
    (2,  66,  16),   # lower-left gutter
    (83, 70,  16),   # lower-right gutter
    (3,  86,  16),   # bottom-left gutter
    (84, 88,  16),   # bottom-right gutter
]
LOW_POSITIONS = [
    (1,  10, 20),
    (84, 22, 18),
    (2,  60, 20),
    (84, 72, 18),
]

CSS_BLOCK = """
/* Dynamic Background System */
main.dynamic-bg { position: relative; isolation: isolate; }
.bg-motif {
  position: absolute; aspect-ratio: 1;
  width: var(--size, 30vw); left: var(--x, 50%); top: var(--y, 50%);
  pointer-events: none; z-index: -1;
  background-color: #E8E4D8; opacity: 0.18;
  -webkit-mask: var(--art) center / contain no-repeat;
          mask: var(--art) center / contain no-repeat;
}
:root[data-theme="light"] .bg-motif { background-color: #1A1A1A; opacity: 0.14; }
@media (max-width: 700px) { .bg-motif { width: calc(var(--size, 30vw) * 0.7); opacity: 0.12; } }
"""

START = "<!-- BG-MOTIFS-START -->"
END = "<!-- BG-MOTIFS-END -->"
MOTIF_BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
CSS_MARKER = "/* Dynamic Background System */"


def list_assets():
    files = sorted(ART_DIR.glob("*.svg"), key=lambda p: int(p.stem) if p.stem.isdigit() else 1e9)
    return [f.relative_to(ROOT).as_posix() for f in files if f.stem.isdigit()]


def is_high_density(html_path: Path, html_text: str) -> bool:
    name = html_path.name
    if name in HIGH:
        return True
    if name in LOW:
        return False
    if PROJECT_PAGE_RE.match(name):
        # high if 2+ section-headers
        return html_text.count('class="section-header"') >= 2
    return False


def build_motifs(rng: random.Random, assets: list[str], n: int) -> str:
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
        out.append(
            f'  <div class="bg-motif" style="--art:url(\'{art}\'); '
            f'--x:{x:.0f}%; --y:{y:.0f}%; --size:{sz:.0f}vw"></div>'
        )
    out.append(END)
    return "\n".join(out)


def wrap_main_if_needed(html: str) -> str:
    """If page has no <main class="dynamic-bg">, wrap the content between </nav> and <footer> (or <script> if no footer)."""
    if 'class="dynamic-bg"' in html or 'class="dynamic-bg ' in html or 'dynamic-bg"' in html:
        return html
    if "<main" in html:
        # Add the class to existing <main>
        html = re.sub(r"<main(\s+[^>]*)?>", lambda m: '<main class="dynamic-bg"' + (m.group(1) or "") + ">", html, count=1)
        return html
    # Wrap content between </nav> and either <footer or end-of-body markers
    nav_end = html.find("</nav>")
    if nav_end == -1:
        return html
    body_close = html.rfind("</body>")
    if body_close == -1:
        return html
    # Find earliest of <footer or <script after </nav>
    after_nav = nav_end + len("</nav>")
    chunk = html[after_nav:body_close]
    insert_open = '\n<main class="dynamic-bg">\n'
    insert_close = '\n</main>\n'
    return html[:after_nav] + insert_open + chunk + insert_close + html[body_close:]


def patch_css(html: str) -> str:
    if CSS_MARKER in html:
        return html
    # Insert before </style> in the <head>
    head_close = html.find("</style>")
    if head_close == -1:
        return html
    return html[:head_close] + CSS_BLOCK + html[head_close:]


def patch_motifs(html: str, motif_html: str) -> str:
    if MOTIF_BLOCK_RE.search(html):
        return MOTIF_BLOCK_RE.sub(motif_html, html, count=1)
    # Insert just inside opening <main class="dynamic-bg">
    m = re.search(r'(<main class="dynamic-bg"[^>]*>)', html)
    if m:
        idx = m.end()
        return html[:idx] + "\n" + motif_html + "\n" + html[idx:]
    return html


def main():
    assets = list_assets()
    if not assets:
        print("No background-art assets found.")
        return
    print(f"Asset pool: {assets}")

    targets = []
    for p in ROOT.glob("*.html"):
        if p.name.startswith("_"):
            continue
        targets.append(p)

    for path in sorted(targets):
        html = path.read_text(encoding="utf-8")
        original = html

        # Skip print.html if it ever appears
        if path.name == "print.html":
            continue

        html = wrap_main_if_needed(html)
        html = patch_css(html)

        rng = random.Random(path.stem)
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
