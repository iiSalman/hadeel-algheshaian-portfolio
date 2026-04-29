"""Generate the 8 project pages for the Hadeel Algheshaian portfolio.

Walks each project folder, auto-discovers section subfolders, gathers images,
and emits `project-<slug>.html`. Each project gets its specific wildcard
(rotated edge / texture / marquee / sticker / chips / cross-section / room-hover)
injected into the template.

Re-run anytime — files are overwritten cleanly.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}

PROJECTS = [
    dict(slug="almamlaka",   n="01", folder="2. ALMAMLAKA",                 title_en="ALMAMLAKA",                title_ar="المملكة",                 year=2026, type_en="Cultural",    type_ar="ثقافي",  wildcard="rotated_edge"),
    dict(slug="coffee-day",  n="02", folder="3. International Coffee Day",  title_en="International Coffee Day", title_ar="يوم القهوة العالمي",         year=2025, type_en="Commercial",  type_ar="تجاري",  wildcard="texture_paper"),
    dict(slug="courtyard",   n="03", folder="4. courtyard",                 title_en="Courtyard",                title_ar="الفناء",                  year=2025, type_en="Cultural",    type_ar="ثقافي",  wildcard="texture_canvas"),
    dict(slug="lavender",    n="04", folder="5. Lavender Center",           title_en="Lavender Center",          title_ar="مركز الخزامى",             year=2024, type_en="Commercial",  type_ar="تجاري",  wildcard="program_marquee"),
    dict(slug="almaarefa",   n="05", folder="6. AlMaarefa University",      title_en="AlMaarefa University",     title_ar="جامعة المعرفة",            year=2024, type_en="Cultural",    type_ar="ثقافي",  wildcard="plan_hotspots"),
    dict(slug="awjaj",       n="06", folder="7. Awjaj hotel",               title_en="Awjaj Hotel",              title_ar="فندق أوجاج",               year=2023, type_en="Hospitality", type_ar="ضيافة",  wildcard="metadata_sticker"),
    dict(slug="culinary",    n="07", folder="8. Culinary Arts Institute",   title_en="Culinary Arts Institute",  title_ar="معهد فنون الطهي",          year=2023, type_en="Cultural",    type_ar="ثقافي",  wildcard="color_chips"),
    dict(slug="company",     n="08", folder="9. company",                   title_en="Company",                  title_ar="مقر الشركة",                year=2022, type_en="Commercial",  type_ar="تجاري",  wildcard="section_selfdraw"),
]

# Per-project metadata for wildcards
WILDCARD_DATA = {
    "almamlaka": {},
    "coffee-day": {},
    "courtyard": {},
    "lavender": {
        "tags_en": ["Treatment", "Lounge", "Yoga", "Massage", "Greenhouse", "Herbal", "Retail"],
        "tags_ar": ["علاج", "استراحة", "يوغا", "مساج", "بيت زجاجي", "أعشاب", "تجزئة"],
    },
    "almaarefa": {
        "rooms": [
            {"name_en": "Lecture Hall", "name_ar": "قاعة محاضرات", "x": 32, "y": 38},
            {"name_en": "Library",      "name_ar": "مكتبة",       "x": 64, "y": 30},
            {"name_en": "Studio",       "name_ar": "مرسم",        "x": 50, "y": 60},
            {"name_en": "Lounge",       "name_ar": "استراحة",     "x": 78, "y": 70},
        ],
    },
    "awjaj": {
        "meta_en": [("YEAR", "2023"), ("KEYS", "32"), ("LOCATION", "Riyadh")],
        "meta_ar": [("السنة", "2023"), ("غرف", "32"), ("الموقع", "الرياض")],
    },
    "culinary": {
        "chips": [
            {"hex": "#B87333", "name_en": "Copper",  "name_ar": "نحاس"},
            {"hex": "#7B5C36", "name_en": "Oak",     "name_ar": "بلوط"},
            {"hex": "#7E8489", "name_en": "Steel",   "name_ar": "فولاذ"},
            {"hex": "#E1D7C2", "name_en": "Linen",   "name_ar": "كتان"},
        ],
    },
    "company": {},
}

BIO_BY_SLUG = {
    "almamlaka":  {"en": "ALMAMLAKA gathers Najdi proportion and modern restraint into a single quiet civic interior. The brief was to make a building feel inevitable from the moment you cross its threshold.", "ar": "يجمع مشروع المملكة بين النسب النجدية والانضباط المعاصر في فضاء مدني هادئ. كان المطلوب أن يبدو المبنى وكأنه كان دائماً هنا منذ اللحظة التي تعبر فيها عتبته."},
    "coffee-day": {"en": "Three booths designed for International Coffee Day — French, Saudi, and Dopamicaffeine — each pulling material register from a different coffee tradition while sharing one structural language.", "ar": "ثلاثة أجنحة لمعرض يوم القهوة العالمي — فرنسي وسعودي ودوبامي‑كافين — كل جناح يستلهم مادته من تقليد قهوة مختلف بينما يتشاركون في لغة إنشائية واحدة."},
    "courtyard":  {"en": "A small open-air courtyard composed around a single tree and the way light moves through stone over the course of a day. The plan does little; the air does the work.", "ar": "فناء مفتوح صغير مُؤلَّف حول شجرة واحدة وحركة الضوء على الحجر خلال اليوم. المسقط يقوم بالقليل؛ الهواء يقوم بالباقي."},
    "lavender":   {"en": "A wellness center organized around the slow tempo of treatment — yoga, massage, herbal preparation, retail. The interior treats program transitions as moments of rest, not connectors.", "ar": "مركز عافية مُنظَّم حول إيقاع العلاج البطيء — يوغا، مساج، تحضير أعشاب، تجزئة. تعامل الفضاءات الداخلية الانتقال بين البرامج كلحظات راحة، لا كممرّات."},
    "almaarefa":  {"en": "Interiors for AlMaarefa University — lecture, library, studio, and lounge — designed to teach by atmosphere as much as by content. Materials carry the program where signage would intrude.", "ar": "فضاءات داخلية لجامعة المعرفة — محاضرات، مكتبة، مرسم، استراحة — مُصمَّمة لتُعلِّم بالأجواء كما تُعلِّم بالمحتوى. المواد تحمل البرنامج حيث يكون التوجيه دخيلاً."},
    "awjaj":      {"en": "Awjaj Hotel — thirty-two keys arranged to slow a guest's first hour. Lobby, suite, and back-of-house all share one stone palette and one rule about light: it should always feel late afternoon.", "ar": "فندق أوجاج — اثنان وثلاثون مفتاحاً مُرتَّبة لإبطاء أول ساعة للضيف. اللوبي، الجناح، والخدمات الخلفية تتشارك في خامة حجرية واحدة وقاعدة واحدة عن الضوء: يجب أن يبدو دائماً عند ما بعد العصر."},
    "culinary":   {"en": "An institute for culinary practice — practical kitchens, dish stores, cross-section storage, and the long counters they make possible. Material is the curriculum: copper, oak, steel, linen.", "ar": "معهد للممارسة الطهوية — مطابخ تطبيقية، مخازن أطباق، تخزين بمسقط مقطعي، والكاونترات الطويلة التي تتيحها. المادة هي المنهج: نحاس، بلوط، فولاذ، كتان."},
    "company":    {"en": "Corporate interior design for a Riyadh firm — reception, waiting, manager's office, and shared workfloor. The brief asked for restraint that still reads as branded; the answer was tone, not graphic.", "ar": "تصميم داخلي لمكاتب شركة في الرياض — استقبال، انتظار، مكتب مدير، وقاعة عمل مشتركة. كان المطلوب انضباطاً لا يخلو من هويّة الشركة؛ الجواب كان نبرة، لا جرافيك."},
}

NUM_PREFIX_RE = re.compile(r"^(\d+)\.\s*(.+)$")

def parse_order(name: str) -> tuple[int, str]:
    m = NUM_PREFIX_RE.match(name)
    if m:
        return (int(m.group(1)), m.group(2))
    return (10**6, name)


def collect_sections(folder: Path):
    """Return [(label, [image_relpaths])] for the project's section subfolders.
    Skips '1. Project start' (its hero photo is handled separately).
    Within each section, recursively gathers images and sorts by numeric prefix.
    """
    sections = []
    for sub in sorted(folder.iterdir(), key=lambda p: parse_order(p.name)[0]):
        if not sub.is_dir():
            continue
        order, label = parse_order(sub.name)
        if label.lower().startswith("project start"):
            continue
        images = []
        for f in sorted(sub.rglob("*")):
            if f.is_file() and f.suffix.lower() in IMG_EXT:
                rel = f.relative_to(ROOT).as_posix()
                images.append(rel)
        if images:
            sections.append({"label_en": label, "images": images})
    return sections


# Inject Arabic labels for common section names
SECTION_AR = {
    "FINAL OUTCOME": "النتيجة النهائية",
    "2D Drawing": "رسومات ثنائية الأبعاد",
    "3D shots": "لقطات ثلاثية الأبعاد",
    "3d shots": "لقطات ثلاثية الأبعاد",
    "3d Shots": "لقطات ثلاثية الأبعاد",
    "Floor plan": "المخطط الأرضي",
    "Floor Plan": "المخطط الأرضي",
    "floor plan": "المخطط الأرضي",
    "Cross sections": "مقاطع عرضية",
    "Cross section": "مقطع عرضي",
    "Elevations": "الواجهات",
    "French Coffee Booth": "جناح القهوة الفرنسية",
    "Saudi Coffee Booth": "جناح القهوة السعودية",
    "Dupamicaffeine booth": "جناح دوبامي‑كافين",
}


def section_ar(label_en: str) -> str:
    return SECTION_AR.get(label_en, label_en)


# ========== wildcard HTML/CSS injection per type ==========

WILDCARD_CSS = {
    "rotated_edge": """
.gallery-item.rotated-edge { transform: rotate(-3deg); margin: 0 -8px; z-index: 2; }
.gallery-item.rotated-edge img { box-shadow: 0 8px 28px rgba(0,0,0,0.35); }
""",
    "texture_paper": """
.chapter-block { position: relative; }
.chapter-block::before {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(circle at 30% 40%, rgba(85, 60, 35, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 75% 65%, rgba(85, 60, 35, 0.10) 0%, transparent 55%),
    radial-gradient(circle at 50% 80%, rgba(85, 60, 35, 0.08) 0%, transparent 40%);
  mix-blend-mode: multiply;
  opacity: 0.85;
}
.chapter-block::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 0; opacity: 0.18;
  background-image: repeating-linear-gradient(45deg, rgba(0,0,0,0.04) 0 2px, transparent 2px 6px),
                    repeating-linear-gradient(-45deg, rgba(0,0,0,0.04) 0 2px, transparent 2px 6px);
}
""",
    "texture_canvas": """
.chapter-block { position: relative; }
.chapter-block::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: 0; opacity: 0.16;
  background-image:
    repeating-linear-gradient(0deg,   rgba(232,228,216,0.15) 0 1px, transparent 1px 4px),
    repeating-linear-gradient(90deg,  rgba(232,228,216,0.15) 0 1px, transparent 1px 4px);
}
:root[data-theme="light"] .chapter-block::after { opacity: 0.22; background-image:
    repeating-linear-gradient(0deg,   rgba(44,34,24,0.10) 0 1px, transparent 1px 4px),
    repeating-linear-gradient(90deg,  rgba(44,34,24,0.10) 0 1px, transparent 1px 4px); }
""",
    "program_marquee": """
.marquee {
  position: relative; overflow: hidden;
  border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  margin: 32px 0;
  font-family: var(--font-serif); font-style: italic; font-weight: 400;
  font-size: 22px; color: var(--accent);
  height: 60px; display: flex; align-items: center;
}
.marquee-track { display: flex; gap: 56px; padding-left: 56px; animation: marquee-scroll 38s linear infinite; white-space: nowrap; }
.marquee-track span::after { content: " · "; color: var(--muted); margin-left: 56px; }
@keyframes marquee-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .marquee-track { animation: none; } }
""",
    "plan_hotspots": """
.plan-wrap { position: relative; max-width: 980px; margin: 0 auto 72px; }
.plan-wrap img { width: 100%; display: block; filter: brightness(0.95) contrast(1.04); }
.plan-hotspot {
  position: absolute; width: 18px; height: 18px;
  border: 1.5px solid var(--accent); border-radius: 50%;
  background: var(--bg); cursor: pointer;
  transform: translate(-50%, -50%);
  transition: transform 0.25s, background 0.25s;
}
.plan-hotspot::before {
  content: ""; position: absolute; inset: 4px; background: var(--accent); border-radius: 50%; opacity: 0.7;
}
.plan-hotspot:hover { transform: translate(-50%, -50%) scale(1.4); background: var(--accent); }
.plan-hotspot .plan-label {
  position: absolute; left: 50%; top: -28px; transform: translateX(-50%);
  font-family: var(--font-serif); font-style: italic; font-size: 14px;
  color: var(--text); background: var(--bg); padding: 4px 12px;
  border: 1px solid var(--border);
  white-space: nowrap; opacity: 0; transition: opacity 0.25s;
  pointer-events: none;
}
.plan-hotspot:hover .plan-label { opacity: 1; }
""",
    "metadata_sticker": """
.meta-sticker {
  position: fixed; pointer-events: none;
  width: 168px; padding: 14px 16px;
  background: var(--bg); border: 1px solid var(--accent);
  font-family: var(--font-en); font-size: 10px; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--text);
  z-index: 80;
  opacity: 0; transition: opacity 0.4s;
  transform: translate(20px, 20px);
}
.meta-sticker.live { opacity: 0.95; }
.meta-sticker dl { margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 14px; }
.meta-sticker dt { color: var(--muted); margin: 0; font-size: 9px; }
.meta-sticker dd { color: var(--accent); margin: 0; font-family: var(--font-serif); font-style: italic; font-size: 14px; letter-spacing: 0; text-transform: none; }
""",
    "color_chips": """
.chips { display: flex; gap: 18px; margin: 32px 0; flex-wrap: wrap; }
.chip { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.chip-swatch { width: 64px; height: 64px; border: 1px solid var(--border); }
.chip-name { font-family: var(--font-serif); font-style: italic; font-size: 14px; color: var(--text); }
.chip-hex { font-family: var(--font-en); font-size: 9px; letter-spacing: 0.18em; color: var(--muted); }
""",
    "section_selfdraw": """
.selfdraw { display: block; max-width: 880px; margin: 32px auto 56px; }
.selfdraw path, .selfdraw line, .selfdraw rect, .selfdraw polygon {
  fill: none; stroke: var(--accent); stroke-width: 1.2;
  stroke-dasharray: 2000;
  stroke-dashoffset: 2000;
  transition: stroke-dashoffset 2.4s ease-out;
}
.selfdraw.live path, .selfdraw.live line, .selfdraw.live rect, .selfdraw.live polygon {
  stroke-dashoffset: 0;
}
""",
}


def wildcard_html(slug: str, project: dict) -> tuple[str, str, str]:
    """Return (head_extra_css, between_head_and_hero_html, after_gallery_html, end_of_body_js)."""
    return ("", "", "")  # legacy unused


# ========== template ==========

TEMPLATE = """<!doctype html>
<html lang="en" data-theme="dark" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE_EN__ — Hadeel Algheshaian</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500&family=Tajawal:wght@300;400;500&display=swap" rel="stylesheet">
<script>
  (function () {
    var l = localStorage.getItem('lang') || 'en';
    document.documentElement.setAttribute('lang', l);
    document.documentElement.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
    var t = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
<style>
  :root {
    --bg: #0E1418; --surface: #161D22; --border: #252e34;
    --text: #E8E4D8; --muted: #8a8475; --accent: #A98756;
    --nav-bg: rgba(14, 20, 24, 0.82);
    --hero-bg-filter: grayscale(100%) brightness(0.35);
    --about-fade: 14, 20, 24;
    --font-en: 'Inter', system-ui, sans-serif;
    --font-ar: 'Tajawal', system-ui, sans-serif;
    --font-serif: 'Cormorant Garamond', 'Times New Roman', serif;
  }
  :root[data-theme="light"] {
    --bg: #EFE8DA; --surface: #E1D7C2; --border: #B8A883;
    --text: #2C2218; --muted: #7A6E54; --accent: #A98756;
    --nav-bg: rgba(239, 232, 218, 0.92);
    --hero-bg-filter: sepia(0.18) saturate(0.85) brightness(0.95) contrast(0.96);
    --about-fade: 239, 232, 218;
  }
  *, *::before, *::after { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: var(--font-en); font-weight: 300; font-size: 15px; line-height: 1.65; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
  html[lang="ar"] body { font-family: var(--font-ar); }
  /* Arabic: never letter-space (breaks letter joining) and no uppercase (no case in Arabic) */
  html[lang="ar"] *, html[lang="ar"] *::before, html[lang="ar"] *::after {
    letter-spacing: 0 !important;
    text-transform: none !important;
  }
  a { color: inherit; text-decoration: none; }
  img { display: block; max-width: 100%; }

  .nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; direction: ltr;
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 40px; background: var(--nav-bg); backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--border); }
  .nav-logo { display: flex; align-items: center; gap: 14px; cursor: pointer; }
  .nav-logo-mark { display: block; width: 36px; height: 36px; background-color: var(--text);
    -webkit-mask: url("brand/logo-mark.png") center / contain no-repeat;
            mask: url("brand/logo-mark.png") center / contain no-repeat;
    animation: logo-spin 28s linear infinite; transform-origin: 50% 50%;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.35)); }
  .nav-logo-name { font-family: var(--font-serif); font-style: italic; font-weight: 400; font-size: 18px; letter-spacing: 0.02em; }
  .nav-links { display: flex; align-items: center; gap: 32px; font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); }
  .nav-links a:hover { color: var(--text); }
  .nav-toggles { display: flex; align-items: center; gap: 10px; }
  .toggle-btn { width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid var(--border); background: transparent; color: var(--text); border-radius: 50%;
    font-family: var(--font-en); font-size: 10px; font-weight: 500; letter-spacing: 0.08em; cursor: pointer;
    transition: border-color 0.2s, color 0.2s; }
  .toggle-btn:hover { border-color: var(--accent); color: var(--accent); }
  .theme-icon-light, .theme-icon-dark { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 1.5; }
  :root[data-theme="dark"] .theme-icon-dark { display: none; }
  :root[data-theme="light"] .theme-icon-light { display: none; }
  @keyframes logo-spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
  @media (prefers-reduced-motion: reduce) { .nav-logo-mark { animation: none; } }

  .project-hero-wrap {
    position: relative; isolation: isolate;
    margin-top: 68px;  /* clear the fixed nav */
    min-height: 86vh;
    overflow: hidden;
  }
  .project-hero { display: block; width: 100%; height: 86vh; min-height: 540px; object-fit: cover; }
  .project-hero-overlay-top {
    position: absolute; top: 0; left: 0; right: 0; height: 46%;
    pointer-events: none; z-index: 1;
    background: linear-gradient(to bottom, rgba(8, 12, 14, 0.65) 0%, rgba(8, 12, 14, 0.32) 55%, rgba(8, 12, 14, 0) 100%);
  }
  .project-hero-overlay-bottom {
    position: absolute; bottom: 0; left: 0; right: 0; height: 50%;
    pointer-events: none; z-index: 1;
    background: linear-gradient(to top, rgba(8, 12, 14, 0.82) 0%, rgba(8, 12, 14, 0.45) 35%, rgba(8, 12, 14, 0) 100%);
  }
  .project-hero-title {
    position: absolute; top: 56px; left: 0; right: 0; z-index: 3;
    text-align: center; padding: 0 40px;
  }
  .ph-num {
    font-family: var(--font-serif); font-style: italic;
    font-size: 13px; color: var(--accent); margin-bottom: 6px;
    text-shadow: 0 1px 4px rgba(0,0,0,0.55);
  }
  .ph-name {
    font-family: var(--font-serif); font-style: italic; font-weight: 400;
    font-size: clamp(44px, 6.5vw, 86px); line-height: 1.04;
    color: #E8E4D8; margin: 0;
    text-shadow: 0 2px 14px rgba(0,0,0,0.6);
  }
  .ph-rule { display: block; width: 1px; height: 44px; background: var(--accent); margin: 20px auto 0; opacity: 0.85; box-shadow: 0 1px 3px rgba(0,0,0,0.55); }
  .ph-year {
    margin-top: 14px;
    font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase;
    color: rgba(232, 228, 216, 0.82);
    text-shadow: 0 1px 4px rgba(0,0,0,0.55);
  }
  .project-hero-desc {
    position: absolute; left: 0; bottom: 0; z-index: 2;
    max-width: 62ch;
    padding: 36px 56px 44px;
    color: #E8E4D8;
  }
  .project-hero-desc .desc-eyebrow {
    font-family: var(--font-en);
    font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase;
    color: rgba(232, 228, 216, 0.82); margin-bottom: 14px;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.55);
  }
  .project-hero-desc .desc-body {
    font-family: var(--font-en); font-weight: 300;
    font-size: 14px; line-height: 1.75; color: #E8E4D8;
    margin: 0; max-width: 56ch;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.7);
  }
  @media (max-width: 700px) {
    .project-hero-wrap { min-height: 70vh; }
    .project-hero { height: 70vh; min-height: 460px; }
    .project-hero-title { top: 40px; padding: 0 20px; }
    .project-hero-desc { padding: 22px 20px 26px; max-width: 100%; }
    .project-hero-desc .desc-body { font-size: 13px; line-height: 1.65; }
  }

  /* sections */
  .section-header { text-align: center; padding: 96px 40px 24px; }
  .section-eyebrow { font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--muted); }
  .section-title { font-family: var(--font-serif); font-style: italic; font-weight: 400; font-size: 30px; margin: 8px 0 0; }

  /* gallery — justified rows: flex-grow = aspect-ratio gives equal heights with zero crop */
  .gallery { padding: 0 40px; max-width: 1480px; margin: 0 auto; }
  .gallery-row { display: flex; gap: 4px; margin-bottom: 4px; align-items: stretch; }
  .gallery-row > .gallery-item { flex: var(--ar, 1) 1 0; min-width: 0; cursor: pointer; overflow: hidden; position: relative; }
  .gallery-row > .gallery-item img { width: 100%; height: 100%; object-fit: cover; display: block; transition: filter 0.4s, transform 1.2s ease-out; }
  .gallery-row > .gallery-item:hover img { filter: brightness(1.05); transform: scale(1.02); }
  /* center: trailing odd image, half-width, natural aspect */
  .gallery-row.center { justify-content: center; align-items: flex-start; }
  .gallery-row.center > .gallery-item { flex: 0 0 calc(50% - 2px); }
  .gallery-row.center > .gallery-item img { height: auto; object-fit: unset; }
  /* full: single-image section (e.g. 2D drawing), spans full width and blends white */
  .gallery-row.full { align-items: flex-start; }
  .gallery-row.full > .gallery-item { flex: 0 0 100%; }
  .gallery-row.full > .gallery-item img { height: auto; object-fit: unset; }
  @media (max-width: 700px) {
    .gallery-row { flex-direction: column; }
    .gallery-row.center > .gallery-item, .gallery-row.full > .gallery-item { flex: 1 1 auto; }
  }

  /* description */
  .description { max-width: 64ch; margin: 0 auto; padding: 80px 40px 64px; }
  .description-eyebrow { font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--muted); margin-bottom: 18px; }
  .description-title { font-family: var(--font-serif); font-style: italic; font-weight: 400; font-size: 28px; margin: 0 0 20px; }
  .description-body { font-size: 15px; line-height: 1.85; color: var(--text); }

  /* lightbox */
  .lightbox { position: fixed; inset: 0; background: #000; display: none; z-index: 9000; flex-direction: column; cursor: zoom-out; }
  .lightbox.open { display: flex; }
  .lightbox-stage { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; padding: 24px; min-height: 0; }
  .lightbox-stage img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .lightbox-counter { position: absolute; top: 18px; left: 24px; color: #E8E4D8; font-family: var(--font-en); font-size: 11px; letter-spacing: 0.32em; }
  .lightbox-close { position: fixed; top: 22px; right: 24px; background: rgba(0,0,0,0.75); color: #fff; border: 2px solid #fff; width: 56px; height: 56px; cursor: pointer; font-size: 32px; line-height: 1; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 4px rgba(0,0,0,0.35), 0 6px 24px rgba(0,0,0,0.7); padding: 0; }
  .lightbox-close:hover { border-color: var(--accent); color: var(--accent); background: rgba(0,0,0,0.9); transform: scale(1.05); }
  .lightbox-prev, .lightbox-next { position: absolute; top: 50%; transform: translateY(-50%); background: transparent; border: 1px solid rgba(255,255,255,0.3); color: #E8E4D8; width: 48px; height: 48px; border-radius: 50%; cursor: pointer; font-size: 20px; }
  .lightbox-prev { left: 24px; } .lightbox-next { right: 24px; }
  .lightbox-prev:hover, .lightbox-next:hover { border-color: var(--accent); color: var(--accent); }
  .lightbox-strip { display: flex; gap: 6px; padding: 12px; overflow-x: auto; background: #050708; border-top: 1px solid #1a1a1a; height: 96px; flex-shrink: 0; }
  .lightbox-strip-thumb { flex-shrink: 0; width: 96px; height: 72px; cursor: pointer; opacity: 0.45; transition: opacity 0.2s; border: 1px solid transparent; overflow: hidden; }
  .lightbox-strip-thumb img { width: 100%; height: 100%; object-fit: cover; }
  .lightbox-strip-thumb.active { opacity: 1; border-color: var(--accent); }
  .lightbox-strip-thumb:hover { opacity: 0.85; }

  /* footer */
  .pf { padding: 48px 40px; text-align: center; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; gap: 24px; flex-wrap: wrap; max-width: 1280px; margin: 0 auto; }
  .pf a { color: var(--muted); font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; }
  .pf a:hover { color: var(--accent); }
  .pf .pf-title { font-family: var(--font-serif); font-style: italic; font-size: 16px; color: var(--text); }

  /* responsive */
  @media (max-width: 900px) {
    .nav { padding: 14px 20px; }
    .nav-links { display: none; }
    .nav-logo-name { font-size: 16px; }
    .project-head { padding: 100px 20px 36px; }
    .gallery { padding: 0 20px; }
    .description { padding: 56px 20px 48px; }
    .pf { padding: 32px 20px; }
    .lightbox-strip { height: 76px; }
    .lightbox-strip-thumb { width: 76px; height: 58px; }
  }

  /* per-project wildcard */
  __WILDCARD_CSS__
</style>
</head>
<body>

<nav class="nav">
  <a class="nav-logo" href="index.html" aria-label="Home">
    <span class="nav-logo-mark"></span>
    <span class="nav-logo-name">Hadeel</span>
  </a>
  <div class="nav-links">
    <a href="index.html#projects" data-en="Work" data-ar="الأعمال">Work</a>
    <a href="index.html#about" data-en="About" data-ar="نبذة">About</a>
    <a href="contact.html" data-en="Contact" data-ar="تواصل">Contact</a>
  </div>
  <div class="nav-toggles">
    <button class="toggle-btn" id="theme-toggle" aria-label="Toggle theme">
      <svg class="theme-icon-light" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
      <svg class="theme-icon-dark" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
    </button>
    <button class="toggle-btn" id="lang-toggle" aria-label="Toggle language">EN</button>
  </div>
</nav>

<div class="project-hero-wrap">
  <img class="project-hero" src="__HERO__" alt="__TITLE_EN__">
  <div class="project-hero-overlay-top"></div>
  <div class="project-hero-overlay-bottom"></div>
  <div class="project-hero-title">
    <div class="ph-num">__N__</div>
    <h1 class="ph-name" data-en="__TITLE_EN__" data-ar="__TITLE_AR__">__TITLE_EN__</h1>
    <div class="ph-rule"></div>
    <div class="ph-year">__YEAR__</div>
  </div>
  <div class="project-hero-desc">
    <div class="desc-eyebrow" data-en="— On the project —" data-ar="— عن المشروع —">— On the project —</div>
    <p class="desc-body" data-en="__BIO_EN__" data-ar="__BIO_AR__">__BIO_EN__</p>
  </div>
</div>

__BODY__

<footer class="pf">
  <a href="index.html" data-en="← All Work" data-ar="→ كل الأعمال">← All Work</a>
  <span class="pf-title">__TITLE_EN__</span>
  <a href="contact.html" data-en="Contact →" data-ar="← تواصل">Contact →</a>
</footer>

<div class="lightbox" id="lightbox" aria-hidden="true">
  <button class="lightbox-close" id="lightbox-close" aria-label="Close">×</button>
  <div class="lightbox-stage">
    <span class="lightbox-counter" id="lightbox-counter">1 / 1</span>
    <button class="lightbox-prev" id="lightbox-prev" aria-label="Previous">‹</button>
    <img id="lightbox-img" src="" alt="">
    <button class="lightbox-next" id="lightbox-next" aria-label="Next">›</button>
  </div>
  <div class="lightbox-strip" id="lightbox-strip"></div>
</div>

<script>
  const ALL_IMAGES = __ALL_IMAGES_JSON__;
  let lbIndex = 0;
  let lang = localStorage.getItem('lang') || 'en';

  // ========== gallery layout (uniform 2-column grid; trailing odd → span-2) ==========
  function balanceGallery(gallery) {
    /* column-flow handles layout; no balancing needed */
  }
  function layoutAll() { /* no-op */ }

  // ========== lightbox ==========
  function openLightbox(idx) {
    lbIndex = idx;
    document.getElementById('lightbox').classList.add('open');
    document.getElementById('lightbox').setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    paintLightbox();
    buildStrip();
  }
  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('open');
    document.getElementById('lightbox').setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  function paintLightbox() {
    const img = document.getElementById('lightbox-img');
    img.src = ALL_IMAGES[lbIndex];
    document.getElementById('lightbox-counter').textContent = (lbIndex + 1) + ' / ' + ALL_IMAGES.length;
    document.querySelectorAll('.lightbox-strip-thumb').forEach((t, i) => {
      t.classList.toggle('active', i === lbIndex);
      if (i === lbIndex) t.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    });
  }
  function buildStrip() {
    const strip = document.getElementById('lightbox-strip');
    strip.innerHTML = '';
    ALL_IMAGES.forEach((src, i) => {
      const t = document.createElement('div');
      t.className = 'lightbox-strip-thumb' + (i === lbIndex ? ' active' : '');
      t.innerHTML = `<img src="${src}" loading="lazy" alt="">`;
      t.addEventListener('click', () => { lbIndex = i; paintLightbox(); });
      strip.appendChild(t);
    });
  }
  function nextLb() { lbIndex = (lbIndex + 1) % ALL_IMAGES.length; paintLightbox(); }
  function prevLb() { lbIndex = (lbIndex - 1 + ALL_IMAGES.length) % ALL_IMAGES.length; paintLightbox(); }

  // ========== language ==========
  function applyLanguage() {
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    localStorage.setItem('lang', lang);
    document.querySelectorAll('[data-en]').forEach(el => {
      const v = el.dataset[lang === 'ar' ? 'ar' : 'en'];
      if (v != null) el.textContent = v;
    });
    document.getElementById('lang-toggle').textContent = lang === 'en' ? 'AR' : 'EN';
  }

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
  }

  // ========== boot ==========
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.gallery-item').forEach((el, i) => {
      el.addEventListener('click', () => {
        const idx = parseInt(el.dataset.idx, 10);
        if (!isNaN(idx)) openLightbox(idx);
      });
    });
    document.getElementById('lightbox-close').addEventListener('click', closeLightbox);
    document.getElementById('lightbox-next').addEventListener('click', nextLb);
    document.getElementById('lightbox-prev').addEventListener('click', prevLb);
    // Click anywhere in lightbox closes it, except on the image itself or interactive controls
    document.getElementById('lightbox').addEventListener('click', (e) => {
      if (e.target.closest('.lightbox-prev, .lightbox-next, .lightbox-close, .lightbox-strip')) return;
      if (e.target.id === 'lightbox-img') return;
      closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (!document.getElementById('lightbox').classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextLb();
      if (e.key === 'ArrowLeft') prevLb();
    });
    document.getElementById('theme-toggle').addEventListener('click', () => {
      applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
    document.getElementById('lang-toggle').addEventListener('click', () => {
      lang = lang === 'en' ? 'ar' : 'en';
      applyLanguage();
    });

    // Justified-rows: set --ar from each image's natural aspect on paired rows
    document.querySelectorAll('.gallery-row:not(.center):not(.full) > .gallery-item img').forEach(img => {
      const apply = () => {
        if (!img.naturalWidth) return;
        img.parentElement.style.setProperty('--ar', img.naturalWidth / img.naturalHeight);
      };
      if (img.complete && img.naturalWidth) apply();
      else img.addEventListener('load', apply, { once: true });
    });

    Promise.all([...document.images].filter(i => !i.complete).map(i => new Promise(r => i.addEventListener('load', r, { once: true })).catch(() => {})))
      .then(() => layoutAll());
    layoutAll();
    setTimeout(layoutAll, 400);
    setTimeout(layoutAll, 1200);
    let t;
    window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(layoutAll, 120); });

    applyLanguage();

    __WILDCARD_JS__
  });
</script>

</body>
</html>
"""


def gallery_html(sections, all_images_offset=0):
    """Build the section + gallery markup. Returns (html, total_images_so_far)."""
    out = []
    idx = all_images_offset
    for s in sections:
        out.append('<section class="section-header">')
        out.append(f'<h2 class="section-title" data-en="{s["label_en"]}" data-ar="{section_ar(s["label_en"])}">{s["label_en"]}</h2></section>')
        out.append('<div class="gallery">')
        imgs = s["images"]
        if len(imgs) == 1:
            out.append('<div class="gallery-row full">')
            out.append(f'<div class="gallery-item" data-idx="{idx}"><img src="{imgs[0]}" alt="" loading="eager"></div>')
            idx += 1
            out.append('</div>')
        else:
            i = 0
            while i < len(imgs):
                remaining = len(imgs) - i
                if remaining == 1:
                    out.append('<div class="gallery-row center">')
                    out.append(f'<div class="gallery-item" data-idx="{idx}"><img src="{imgs[i]}" alt="" loading="eager"></div>')
                    idx += 1
                    i += 1
                else:
                    out.append('<div class="gallery-row">')
                    for j in range(2):
                        out.append(f'<div class="gallery-item" data-idx="{idx}"><img src="{imgs[i+j]}" alt="" loading="eager"></div>')
                        idx += 1
                    i += 2
                out.append('</div>')
        out.append('</div>')
    return "\n".join(out), idx


def wildcard_for(slug: str, project: dict, sections, project_dir: Path):
    """Return (extra_css, body_extra_html_after_gallery_built, body_extra_js)."""
    css = WILDCARD_CSS.get(project["wildcard"], "")
    extra_html_before_galleries = ""
    extra_html_after_galleries = ""
    extra_js = ""

    if project["wildcard"] == "rotated_edge":
        extra_js = """
        // Rotate one gallery image (~3°) breaking the grid edge
        const gItems = document.querySelectorAll('.gallery .gallery-item');
        if (gItems.length >= 4) gItems[Math.floor(gItems.length / 2)].classList.add('rotated-edge');
        """
    elif project["wildcard"] == "program_marquee":
        d = WILDCARD_DATA["lavender"]
        spans_en = "".join(f"<span>{t}</span>" for t in d["tags_en"] * 2)
        extra_html_before_galleries = f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{spans_en}</div></div>'
    elif project["wildcard"] == "metadata_sticker":
        d = WILDCARD_DATA["awjaj"]
        rows_en = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in d["meta_en"])
        extra_html_before_galleries = f'<div class="meta-sticker" id="meta-sticker"><dl>{rows_en}</dl></div>'
        extra_js = """
        const sticker = document.getElementById('meta-sticker');
        if (sticker) {
          let rafId = null, mx = 0, my = 0;
          window.addEventListener('mousemove', (e) => {
            mx = e.clientX; my = e.clientY;
            sticker.classList.add('live');
            if (rafId) return;
            rafId = requestAnimationFrame(() => {
              sticker.style.transform = `translate(${mx + 24}px, ${my + 24}px)`;
              rafId = null;
            });
          });
          window.addEventListener('mouseleave', () => sticker.classList.remove('live'));
        }
        """
    elif project["wildcard"] == "color_chips":
        d = WILDCARD_DATA["culinary"]
        chips_html = "".join(
            f'<div class="chip"><div class="chip-swatch" style="background:{c["hex"]}"></div>'
            f'<div class="chip-name" data-en="{c["name_en"]}" data-ar="{c["name_ar"]}">{c["name_en"]}</div>'
            f'<div class="chip-hex">{c["hex"]}</div></div>'
            for c in d["chips"]
        )
        extra_html_after_galleries = f'<div style="text-align:center"><div class="chips" style="justify-content:center">{chips_html}</div></div>'
    elif project["wildcard"] == "section_selfdraw":
        # Cross-section SVG (architectural section drawing) that strokes draw on scroll
        extra_html_after_galleries = '''
<svg class="selfdraw" id="selfdraw" viewBox="0 0 800 280" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
  <line x1="40" y1="240" x2="760" y2="240"/>
  <line x1="60" y1="40" x2="60" y2="240"/>
  <line x1="740" y1="40" x2="740" y2="240"/>
  <line x1="60" y1="40" x2="740" y2="40"/>
  <line x1="60" y1="120" x2="740" y2="120"/>
  <line x1="60" y1="180" x2="740" y2="180"/>
  <rect x="120" y="180" width="80" height="60"/>
  <rect x="240" y="180" width="60" height="60"/>
  <rect x="340" y="180" width="120" height="60"/>
  <rect x="500" y="180" width="80" height="60"/>
  <rect x="620" y="180" width="80" height="60"/>
  <rect x="120" y="120" width="120" height="60"/>
  <rect x="280" y="120" width="180" height="60"/>
  <rect x="500" y="120" width="200" height="60"/>
  <rect x="120" y="40" width="200" height="80"/>
  <rect x="360" y="40" width="180" height="80"/>
  <rect x="580" y="40" width="120" height="80"/>
  <line x1="100" y1="240" x2="80" y2="260"/>
  <line x1="200" y1="240" x2="180" y2="260"/>
  <line x1="300" y1="240" x2="280" y2="260"/>
  <line x1="400" y1="240" x2="380" y2="260"/>
  <line x1="500" y1="240" x2="480" y2="260"/>
  <line x1="600" y1="240" x2="580" y2="260"/>
  <line x1="700" y1="240" x2="680" y2="260"/>
</svg>
'''
        extra_js = """
        const sd = document.getElementById('selfdraw');
        if (sd) {
          if ('IntersectionObserver' in window) {
            const o = new IntersectionObserver((entries) => {
              entries.forEach(e => { if (e.isIntersecting) { sd.classList.add('live'); o.unobserve(e.target); } });
            }, { threshold: 0.25 });
            o.observe(sd);
          } else { sd.classList.add('live'); }
        }
        """
    elif project["wildcard"] == "plan_hotspots":
        d = WILDCARD_DATA["almaarefa"]
        # Find a floor plan image to use
        plan_src = None
        for s in sections:
            if "plan" in s["label_en"].lower() or "floor" in s["label_en"].lower():
                if s["images"]:
                    plan_src = s["images"][0]
                    break
        if plan_src:
            hotspots_html = "".join(
                f'<div class="plan-hotspot" style="left:{r["x"]}%; top:{r["y"]}%">'
                f'<span class="plan-label" data-en="{r["name_en"]}" data-ar="{r["name_ar"]}">{r["name_en"]}</span></div>'
                for r in d["rooms"]
            )
            extra_html_before_galleries = (
                f'<div class="plan-wrap"><img src="{plan_src}" alt="Floor plan">'
                f'{hotspots_html}</div>'
            )

    return css, extra_html_before_galleries, extra_html_after_galleries, extra_js


def render_project(project: dict) -> str:
    folder = ROOT / project["folder"]
    sections = collect_sections(folder)

    # Hero (1. Project start/1. hero photo.png)
    hero_path = folder / "1. Project start" / "1. hero photo.png"
    hero_rel = hero_path.relative_to(ROOT).as_posix() if hero_path.exists() else ""

    # Wildcard fragments
    wc_css, wc_before, wc_after, wc_js = wildcard_for(project["slug"], project, sections, folder)

    # Galleries
    gallery_markup, total_imgs = gallery_html(sections, all_images_offset=0)

    # Build all-images list (for lightbox), in same order
    all_imgs = []
    for s in sections:
        all_imgs.extend(s["images"])

    body = wc_before + gallery_markup + wc_after

    bio = BIO_BY_SLUG.get(project["slug"], {"en": "", "ar": ""})

    out = TEMPLATE
    repls = {
        "__TITLE_EN__": project["title_en"],
        "__TITLE_AR__": project["title_ar"],
        "__N__": project["n"],
        "__YEAR__": str(project["year"]),
        "__HERO__": hero_rel,
        "__BODY__": body,
        "__ALL_IMAGES_JSON__": json.dumps(all_imgs),
        "__BIO_EN__": bio["en"],
        "__BIO_AR__": bio["ar"],
        "__WILDCARD_CSS__": wc_css,
        "__WILDCARD_JS__": wc_js,
    }
    for k, v in repls.items():
        out = out.replace(k, v)
    return out


def main():
    for p in PROJECTS:
        html = render_project(p)
        out_path = ROOT / f"project-{p['slug']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  wrote {out_path.name}")
    print(f"Generated {len(PROJECTS)} project pages.")


if __name__ == "__main__":
    main()
