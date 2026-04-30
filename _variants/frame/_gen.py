"""Generate all 8 project pages for the Frame variant.

Reads the project content folders at <repo>/<n>. <Folder>/ and walks them for
photographic images (skipping 2D drawings / floor plans which don't suit the
cinematic full-bleed frame). Each project page becomes a vertical scroll-snap
film reel: an opening title frame, full-bleed photo frames with caption cards,
a bilingual text spread, and an end frame.
"""
from __future__ import annotations
import re
from pathlib import Path

VARIANT = Path(__file__).parent
ROOT = VARIANT.parent.parent  # Hadeel Algheshaian/
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_FOLDER_RE = re.compile(r"(2d\s*drawing|floor\s*plan|cross\s*section|elevation|project\s*start)", re.I)
PREFIX = "../../"  # paths from this variant page to project content

PROJECTS = [
    dict(slug="almamlaka",  n="01", folder="2. ALMAMLAKA",                en="ALMAMLAKA",                ar="المملكة",         type_en="Cultural",    type_ar="ثقافي",  loc_en="Riyadh", loc_ar="الرياض", year="2026"),
    dict(slug="coffee-day", n="02", folder="3. International Coffee Day", en="International Coffee Day", ar="يوم القهوة العالمي", type_en="Commercial",  type_ar="تجاري",  loc_en="Riyadh", loc_ar="الرياض", year="2025"),
    dict(slug="courtyard",  n="03", folder="4. courtyard",                en="Courtyard",                ar="الفناء",          type_en="Cultural",    type_ar="ثقافي",  loc_en="Najd",   loc_ar="نجد",    year="2025"),
    dict(slug="lavender",   n="04", folder="5. Lavender Center",          en="Lavender Center",          ar="مركز الخزامى",    type_en="Commercial",  type_ar="تجاري",  loc_en="Riyadh", loc_ar="الرياض", year="2024"),
    dict(slug="almaarefa",  n="05", folder="6. AlMaarefa University",     en="AlMaarefa University",     ar="جامعة المعرفة",   type_en="Cultural",    type_ar="ثقافي",  loc_en="Riyadh", loc_ar="الرياض", year="2024"),
    dict(slug="awjaj",      n="06", folder="7. Awjaj hotel",              en="Awjaj Hotel",              ar="فندق أوجاج",      type_en="Hospitality", type_ar="ضيافة",  loc_en="Riyadh", loc_ar="الرياض", year="2023"),
    dict(slug="culinary",   n="07", folder="8. Culinary Arts Institute",  en="Culinary Arts Institute",  ar="معهد فنون الطهي", type_en="Cultural",    type_ar="ثقافي",  loc_en="Riyadh", loc_ar="الرياض", year="2023"),
    dict(slug="company",    n="08", folder="9. company",                  en="Company",                  ar="مقر الشركة",      type_en="Commercial",  type_ar="تجاري",  loc_en="Riyadh", loc_ar="الرياض", year="2022"),
]

BIO = {
    "almamlaka": {
        "deck_en": "A civic interior that gathers Najdi proportion and modern restraint, and asks the visitor to slow down at the threshold.",
        "deck_ar": "فضاء داخلي مدني يجمع بين النسب النجدية والانضباط المعاصر، ويطلب من الزائر أن يبطئ عند العتبة.",
        "left_h_en": "A building that would feel inevitable.",
        "left_h_ar": "مبنى يبدو وكأنه كان دائماً هنا.",
        "left_p_en": "The first move was the threshold: a deep porch of brick coursing and tasselled pendants that does the labour of an actual masonry wall, even though it is only forty centimetres of frame.",
        "left_p_ar": "أول قرارٍ كان العتبة: شُرفة عميقة من طبقات الطوب والتعليقات المهدّبة تقوم بعمل جدارٍ بنّاءٍ كاملٍ، رغم أنها أربعون سنتيمتراً من الإطار فحسب.",
        "right_p_en": "Inside, the strategy is reduction. A single colour story — terracotta, brass, bone — and a single rule about light: it falls, never glares.",
        "right_p_ar": "في الداخل، الاستراتيجية اختزال. حكاية لونٍ واحدة — تيراكوتا، نحاس، عظم — وقاعدةٌ واحدة عن الضوء: يقع، لا يُبهر.",
    },
    "coffee-day": {
        "deck_en": "Three booths — French, Saudi, and a contemporary outlier — share one structural language.",
        "deck_ar": "ثلاثة أجنحة — فرنسية، سعودية، ومعاصرة — تتشارك لغة إنشائية واحدة.",
        "left_h_en": "One language; three accents.",
        "left_h_ar": "لغةٌ واحدة؛ ثلاث لهجات.",
        "left_p_en": "Each booth pulls material register from a different coffee tradition: marble and brass for the French, palm and copper for the Saudi, painted plywood and glass for the contemporary outlier.",
        "left_p_ar": "كل جناحٍ يستلهم مادته من تقليد قهوة مختلف: رخام ونحاس للفرنسي، سعف ونحاس للسعودي، خشبٌ معاكسٌ مدهون وزجاج للمعاصر.",
        "right_p_en": "Underneath, the structure is the same: an elevated plinth, a hovering canopy, a counter at standing height. Repetition makes the difference legible.",
        "right_p_ar": "تحتها، البنية واحدة: قاعدة مرتفعة، مظلّة معلّقة، طاولةٌ بارتفاع الوقوف. التكرار يجعل الفروق واضحة.",
    },
    "courtyard": {
        "deck_en": "An open-air courtyard composed around a single tree and the slow movement of light.",
        "deck_ar": "فناء مفتوح مُؤلَّف حول شجرة واحدة وحركة الضوء البطيئة.",
        "left_h_en": "The plan does little; the air does the work.",
        "left_h_ar": "المسقط يفعل القليل؛ الهواء يقوم بالباقي.",
        "left_p_en": "A square of stone, four shaded edges, one tree at the centre. The plan is almost diagrammatic — and the courtyard depends on what arrives from outside it: heat, light, evening cool.",
        "left_p_ar": "مربع من الحجر، أربع حواف مظللة، شجرة واحدة في المنتصف. المسقط شبه تخطيطي، والفناء يعتمد على ما يصله من خارجه: الحرارة، الضوء، برودة المساء.",
        "right_p_en": "The composition is sensitive to the hours: low sun on the west wall in the late afternoon, deep shadow at noon, a slow blue at dusk.",
        "right_p_ar": "التكوين حسّاسٌ للساعات: شمسٌ منخفضة على الجدار الغربي في ما بعد العصر، ظلٌّ عميق ظهراً، زرقةٌ بطيئة عند المغيب.",
    },
    "lavender": {
        "deck_en": "A wellness centre organised around the slow tempo of treatment.",
        "deck_ar": "مركز عافية مُنظَّم حول إيقاع العلاج البطيء.",
        "left_h_en": "Transitions as moments of rest.",
        "left_h_ar": "الانتقالات بوصفها لحظاتِ راحة.",
        "left_p_en": "Yoga, massage, herbal preparation, retail. The interior treats program transitions as places, not connectors — small ante-rooms, tea steps, threshold benches — so the day decelerates as you move through it.",
        "left_p_ar": "يوغا، مساج، تحضير أعشاب، تجزئة. تتعامل الفضاءات الداخلية مع الانتقالات بوصفها أماكن، لا ممرّات — غرفٌ تمهيدية صغيرة، درجات للشاي، مقاعد عتبة — حتى يتباطأ النهار وأنت تمرّ به.",
        "right_p_en": "The palette is olive, washed lavender, and oat. Lighting is layered and warm; sound is dampened by deep textile.",
        "right_p_ar": "الألوان زيتونيّة، خزامى مغسولة، شوفان. الإضاءة طبقاتٌ دافئة؛ الصوت مُخمَدٌ بنسيجٍ عميق.",
    },
    "almaarefa": {
        "deck_en": "Lecture, library, studio, lounge — designed to teach by atmosphere as much as content.",
        "deck_ar": "محاضرات، مكتبة، مرسم، استراحة — مُصمَّمة لتُعلِّم بالأجواء كما بالمحتوى.",
        "left_h_en": "Materials carry the program.",
        "left_h_ar": "المواد تحمل البرنامج.",
        "left_p_en": "Lecture is dense oak and dark felt. Library is paper, brass and quiet. Studio is concrete and washable surface. Lounge is wool and soft light. Where signage would intrude, material does the work.",
        "left_p_ar": "المحاضرات بلوطٌ كثيف ولبدٌ داكن. المكتبة ورقٌ ونحاس وصمت. المرسم خرسانة وسطحٌ قابل للغسل. الاستراحة صوفٌ وضوءٌ ناعم. حيث يكون التوجيه دخيلاً، تقوم المادة بالعمل.",
        "right_p_en": "Adjacencies were chosen so that students cross between registers — quiet and noisy, dense and open — many times a day. The plan is a curriculum.",
        "right_p_ar": "اختيرت الجوارات بحيث يمرّ الطلاب بين السجلات — هادئة وصاخبة، كثيفة ومفتوحة — مرّاتٍ عديدة في اليوم. المسقط منهج.",
    },
    "awjaj": {
        "deck_en": "Thirty-two keys, arranged to slow a guest's first hour.",
        "deck_ar": "اثنان وثلاثون مفتاحاً مُرتَّبة لإبطاء أول ساعة للضيف.",
        "left_h_en": "It should always feel late afternoon.",
        "left_h_ar": "يجب أن يبدو دائماً عند ما بعد العصر.",
        "left_p_en": "Lobby, suite, and back-of-house share one stone palette and one rule about light: it should always feel late afternoon. The first hour after a guest arrives is the entire design problem.",
        "left_p_ar": "اللوبي والجناح وخدمات الخلف يتشاركون في حكاية حجريّةٍ واحدة وقاعدةٍ واحدة عن الضوء: ينبغي أن يبدو دائماً عند ما بعد العصر. الساعة الأولى لوصول الضيف هي مشكلة التصميم بأكملها.",
        "right_p_en": "Joinery is quiet enough that the air conditioning is the loudest sound; carpet is hand-knotted, deep red, and runs from threshold to bed.",
        "right_p_ar": "النجارة هادئةٌ بما يكفي لتصبح المُكيِّف هي الصوت الأعلى؛ السجاد منسوجٌ يدوياً، أحمرَ عميق، يمتد من العتبة إلى السرير.",
    },
    "culinary": {
        "deck_en": "Practical kitchens, dish stores, and the long counters they make possible.",
        "deck_ar": "مطابخ تطبيقية، مخازن أطباق، والكاونترات الطويلة التي تتيحها.",
        "left_h_en": "Material is the curriculum.",
        "left_h_ar": "المادة هي المنهج.",
        "left_p_en": "Copper, oak, steel, linen. Four materials, each with a teaching role: copper for heat, oak for cut, steel for hygiene, linen for finishing. Students learn the building before the lesson.",
        "left_p_ar": "نحاس، بلوط، فولاذ، كتان. أربع موادّ، لكلٍّ منها دور تعليمي: النحاس للحرارة، البلوط للتقطيع، الفولاذ للنظافة، الكتان للتقديم. يتعلّم الطلاب المبنى قبل الدرس.",
        "right_p_en": "Plan is a long axis with stations on either side: prep, sauté, plate. Storage runs underneath; sightlines run through.",
        "right_p_ar": "المسقط محورٌ طويل بمحطّاتٍ على جانبيه: تحضير، قلي، تنضيد. التخزين تحته؛ خطوط النظر تمرّ عبره.",
    },
    "company": {
        "deck_en": "A corporate interior — restraint that still reads as branded.",
        "deck_ar": "تصميم مكاتب — انضباطٌ يحمل هويةً واضحة.",
        "left_h_en": "Tone, not graphic.",
        "left_h_ar": "نبرة، لا جرافيك.",
        "left_p_en": "Reception, waiting, manager's office, shared workfloor. The brief asked for restraint that still reads as branded; the answer was tone — a single olive, a single brass, a single oak — repeated everywhere.",
        "left_p_ar": "استقبال، انتظار، مكتب مدير، قاعة عمل مشتركة. طلب البرنامج انضباطاً لا يخلو من الهوية؛ الجواب كان نبرة — زيتونيٌّ واحد، نحاسٌ واحد، بلوطٌ واحد — مكرَّرة في كل مكان.",
        "right_p_en": "No logos on walls. The branding is in the way the rooms behave: how light arrives, what gets reflected, how the air smells.",
        "right_p_ar": "لا شعاراتٍ على الجدران. الهوية في كيفية تصرّف الغرف: كيف يصل الضوء، ماذا ينعكس، كيف تكون رائحة الهواء.",
    },
}

CAPTIONS = {
    "almamlaka":  [("Plate I — Threshold", "Najdi pendant work above brick coursing.", "اللوحة الأولى — العتبة", "تعليقات نجدية فوق طبقات الطوب."),
                   ("Plate II — Hall", "Looking toward the porch; brass and bone.", "اللوحة الثانية — القاعة", "نظرة نحو الشُرفة؛ نحاس وعظم."),
                   ("Plate III — Light", "It falls, never glares.", "اللوحة الثالثة — الضوء", "يقع، لا يُبهر."),
                   ("Plate IV — Detail", "Pendants, in repetition.", "اللوحة الرابعة — التفصيل", "التعليقات، في تكرار.")],
    "coffee-day": [("Plate I — French", "Marble and brass; reflective surfaces.", "اللوحة الأولى — الفرنسي", "رخامٌ ونحاس؛ أسطحٌ عاكسة."),
                   ("Plate II — Saudi", "Palm and copper; warm shadow.", "اللوحة الثانية — السعودي", "سعفٌ ونحاس؛ ظلٌّ دافئ."),
                   ("Plate III — Outlier", "Painted plywood, soft glass.", "اللوحة الثالثة — المعاصر", "خشبٌ معاكسٌ مدهون، زجاجٌ ناعم."),
                   ("Plate IV — Set", "Three plinths, one canopy.", "اللوحة الرابعة — المجموعة", "ثلاث قواعد، مظلّة واحدة.")],
    "courtyard":  [("Plate I — Stone", "Square plan, four edges.", "اللوحة الأولى — الحجر", "مسقطٌ مربع، أربع حواف."),
                   ("Plate II — Tree", "The single subject.", "اللوحة الثانية — الشجرة", "الموضوع الوحيد."),
                   ("Plate III — Light", "Late afternoon on the west wall.", "اللوحة الثالثة — الضوء", "ما بعد العصر على الجدار الغربي.")],
    "lavender":   [("Plate I — Threshold", "Lavender and oat at the door.", "اللوحة الأولى — العتبة", "خزامى وشوفان عند الباب."),
                   ("Plate II — Treatment", "Soft light, dense textile.", "اللوحة الثانية — العلاج", "ضوءٌ ناعم، نسيجٌ كثيف."),
                   ("Plate III — Tea step", "A bench between rooms.", "اللوحة الثالثة — درجة الشاي", "مقعدٌ بين الغرف."),
                   ("Plate IV — Retail", "Olive shelving, washed wood.", "اللوحة الرابعة — التجزئة", "رفوفٌ زيتونية، خشبٌ مغسول.")],
    "almaarefa":  [("Plate I — Lecture", "Dense oak; dark felt.", "اللوحة الأولى — المحاضرات", "بلوطٌ كثيف؛ لبدٌ داكن."),
                   ("Plate II — Library", "Paper, brass, quiet.", "اللوحة الثانية — المكتبة", "ورقٌ، نحاسٌ، صمت."),
                   ("Plate III — Studio", "Concrete; washable surface.", "اللوحة الثالثة — المرسم", "خرسانة؛ سطحٌ قابل للغسل."),
                   ("Plate IV — Lounge", "Wool and soft light.", "اللوحة الرابعة — الاستراحة", "صوفٌ وضوءٌ ناعم.")],
    "awjaj":      [("Plate I — Lobby", "Stone palette; horizontal brass.", "اللوحة الأولى — اللوبي", "حكاية حجرية؛ نحاسٌ أفقي."),
                   ("Plate II — Suite", "Threshold to bed in one carpet.", "اللوحة الثانية — الجناح", "من العتبة إلى السرير في سجادةٍ واحدة."),
                   ("Plate III — Light", "Always late afternoon.", "اللوحة الثالثة — الضوء", "دائماً ما بعد العصر."),
                   ("Plate IV — Back-of-house", "Same palette, different volume.", "اللوحة الرابعة — الخدمات", "نفس الحكاية، حجمٌ مختلف.")],
    "culinary":   [("Plate I — Copper", "For heat.", "اللوحة الأولى — النحاس", "للحرارة."),
                   ("Plate II — Oak", "For the cut.", "اللوحة الثانية — البلوط", "للتقطيع."),
                   ("Plate III — Steel", "For hygiene.", "اللوحة الثالثة — الفولاذ", "للنظافة."),
                   ("Plate IV — Linen", "For finishing.", "اللوحة الرابعة — الكتان", "للتقديم.")],
    "company":    [("Plate I — Reception", "Olive, brass, oak.", "اللوحة الأولى — الاستقبال", "زيتوني، نحاس، بلوط."),
                   ("Plate II — Waiting", "One repeated detail.", "اللوحة الثانية — الانتظار", "تفصيلٌ واحدٌ متكرر."),
                   ("Plate III — Manager", "Quiet wall, framed light.", "اللوحة الثالثة — المدير", "جدارٌ هادئ، ضوءٌ مؤطَّر."),
                   ("Plate IV — Workfloor", "Even ceiling; no centre.", "اللوحة الرابعة — قاعة العمل", "سقفٌ متجانس؛ لا مركز.")],
}


def url_encode(p: str) -> str:
    """Path-encode for src attributes; spaces -> %20."""
    return p.replace(" ", "%20")


def collect_photo_paths(project_dir: Path) -> list[str]:
    """Walk subfolders, return relative paths to photographic images."""
    paths = []
    for sub in sorted(project_dir.iterdir(), key=lambda p: p.name):
        if not sub.is_dir():
            continue
        if SKIP_FOLDER_RE.search(sub.name):
            continue
        for f in sorted(sub.iterdir(), key=lambda p: p.name):
            if f.is_file() and f.suffix.lower() in IMG_EXT:
                rel = f"{PREFIX}{project_dir.name}/{sub.name}/{f.name}"
                paths.append(url_encode(rel))
    return paths


PAGE_TEMPLATE = """<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Frame {n} — {title_en} — Hadeel Algheshaian</title>
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500;600&family=Tajawal:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --char: oklch(14% 0.005 250); --paper: oklch(98% 0.005 60); --ink: oklch(18% 0.005 250);
    --vermillion: oklch(58% 0.20 28);
    --display: 'Cormorant Garamond', serif; --sans: 'Inter', system-ui, sans-serif;
    --ar: 'Tajawal', system-ui, sans-serif;
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    background: var(--char); color: var(--paper); font-family: var(--sans); font-weight: 300; font-size: 15px; line-height: 1.55;
    -webkit-font-smoothing: antialiased; scroll-snap-type: y mandatory; height: 100vh; overflow-y: auto;
  }}
  html[lang="ar"] body {{ font-family: var(--ar); }}
  html[lang="ar"] *, html[lang="ar"] *::before, html[lang="ar"] *::after {{ letter-spacing: 0 !important; text-transform: none !important; }}
  a {{ color: inherit; text-decoration: none; }}
  ::selection {{ background: var(--vermillion); color: var(--paper); }}

  .runner {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 50;
    display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 24px;
    padding: 18px 36px; mix-blend-mode: difference;
    font-family: var(--sans); font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--paper);
    pointer-events: none;
  }}
  .runner > * {{ pointer-events: auto; }}
  .runner .left {{ font-weight: 500; letter-spacing: 0.32em; }}
  .runner .center {{ font-family: var(--display); font-style: italic; font-size: 17px; letter-spacing: 0; text-transform: none; }}
  .runner .right {{ display: flex; gap: 20px; justify-content: flex-end; align-items: center; }}
  .runner button.toggle {{ background: transparent; border: 1px solid currentColor; color: inherit; font: inherit; font-size: 10px; padding: 6px 12px; border-radius: 999px; cursor: pointer; letter-spacing: 0.18em; }}
  .runner button.toggle:hover {{ border-color: var(--vermillion); color: var(--vermillion); }}

  .frame {{ height: 100vh; min-height: 720px; scroll-snap-align: start; scroll-snap-stop: always; position: relative; overflow: hidden; }}

  .open {{
    background: var(--char); color: var(--paper);
    display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: 64px; padding: 96px;
  }}
  .open-num {{
    font-family: var(--display); font-style: italic; font-size: clamp(120px, 18vw, 280px); line-height: 0.9;
    color: var(--vermillion); margin: 0;
  }}
  .open-text h1 {{
    font-family: var(--display); font-style: italic; font-weight: 400; font-size: clamp(56px, 7vw, 96px); line-height: 0.96; margin: 0 0 18px; letter-spacing: -0.012em;
  }}
  .open-text .ar {{ font-family: var(--ar); font-style: normal; font-size: clamp(40px, 5vw, 64px); margin: 0 0 32px; opacity: 0.78; }}
  .open-text .deck {{ font-family: var(--display); font-style: italic; font-size: 20px; line-height: 1.55; opacity: 0.78; max-width: 50ch; }}
  .open-meta {{
    position: absolute; bottom: 56px; left: 96px; right: 96px;
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;
    border-top: 1px solid oklch(98% 0.005 60 / 0.2); padding-top: 22px;
    font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.32em; text-transform: uppercase; opacity: 0.78;
  }}
  .open-meta dt {{ color: var(--vermillion); margin-bottom: 6px; }}
  .open-meta dd {{ margin: 0; font-family: var(--display); font-style: italic; font-size: 17px; letter-spacing: 0; text-transform: none; opacity: 1; }}

  .photo {{ background-size: cover; background-position: center; color: var(--paper); position: relative; }}
  .photo::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, oklch(8% 0.005 250 / 0.0) 30%, oklch(8% 0.005 250 / 0.7) 100%); }}
  .photo .frame-num {{
    position: absolute; top: 88px; left: 36px; z-index: 2;
    font-family: var(--display); font-style: italic; font-size: 80px; line-height: 1; color: var(--vermillion);
  }}
  .photo .frame-num .label {{
    display: block; font-family: var(--sans); font-style: normal; font-weight: 500; font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--paper); margin-top: 6px; opacity: 0.78;
  }}
  .photo .caption {{
    position: absolute; bottom: 64px; left: 36px; z-index: 2; max-width: 480px;
    font-family: var(--display); font-style: italic; font-size: 22px; line-height: 1.4;
  }}
  .photo .caption .stamp {{ display: block; font-family: var(--sans); font-style: normal; font-weight: 500; font-size: 10px; letter-spacing: 0.32em; text-transform: uppercase; color: var(--vermillion); margin-bottom: 12px; }}

  .spread {{
    background: var(--paper); color: var(--ink);
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; padding: 96px;
    align-content: center;
  }}
  .spread h2 {{ font-family: var(--display); font-style: italic; font-weight: 400; font-size: clamp(40px, 5vw, 64px); line-height: 1.05; margin: 0 0 28px; }}
  .spread .stamp {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--vermillion); margin-bottom: 14px; }}
  .spread p {{ margin: 0 0 1em; max-width: 60ch; line-height: 1.7; font-size: 16px; text-align: justify; hyphens: auto; }}

  .end {{
    background: var(--char); color: var(--paper);
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 28px; padding: 64px;
  }}
  .end .stamp {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.5em; text-transform: uppercase; opacity: 0.7; display: flex; align-items: center; gap: 12px; }}
  .end .stamp::before, .end .stamp::after {{ content: ""; width: 28px; height: 1px; background: currentColor; opacity: 0.6; }}
  .end h2 {{ font-family: var(--display); font-style: italic; font-size: clamp(48px, 7vw, 96px); margin: 0; }}
  .end .nav {{ margin-top: 32px; display: flex; gap: 32px; align-items: center; font-family: var(--sans); font-size: 11px; letter-spacing: 0.32em; text-transform: uppercase; }}
  .end .nav a {{ border-bottom: 1px solid currentColor; padding-bottom: 4px; }}
  .end .nav a:hover {{ color: var(--vermillion); border-color: var(--vermillion); }}
  .end .nav .accent {{ color: var(--vermillion); }}

  @media (max-width: 900px) {{
    .runner {{ padding: 14px 22px; }}
    .runner .right a {{ display: none; }}
    .open {{ padding: 72px 22px; grid-template-columns: 1fr; gap: 24px; }}
    .open-num {{ font-size: clamp(96px, 28vw, 180px); }}
    .open-meta {{ left: 22px; right: 22px; bottom: 32px; grid-template-columns: 1fr 1fr; gap: 14px; padding-top: 14px; }}
    .photo .frame-num {{ font-size: 56px; left: 22px; top: 80px; }}
    .photo .caption {{ left: 22px; right: 22px; bottom: 32px; font-size: 17px; }}
    .spread {{ padding: 64px 22px; grid-template-columns: 1fr; gap: 22px; }}
    .end .nav {{ flex-direction: column; gap: 14px; }}
  }}
</style>
</head>
<body>

<header class="runner">
  <div class="left">FRAME · {n} / 08</div>
  <div class="center">{title_en}</div>
  <div class="right">
    <a href="index.html" data-en="All frames" data-ar="كل الإطارات">All frames</a>
    <button class="toggle" id="lang-toggle">AR</button>
  </div>
</header>

<section class="frame open">
  <div><div class="open-num">{n}</div></div>
  <div class="open-text">
    <h1>{title_en}.</h1>
    <p class="ar">{title_ar}</p>
    <p class="deck" data-en="{deck_en}" data-ar="{deck_ar}">{deck_en}</p>
  </div>
  <dl class="open-meta">
    <div><dt>Year</dt><dd>{year}</dd></div>
    <div><dt>Type</dt><dd data-en="{type_en}" data-ar="{type_ar}">{type_en}</dd></div>
    <div><dt>Location</dt><dd data-en="{loc_en}" data-ar="{loc_ar}">{loc_en}</dd></div>
    <div><dt>Frames</dt><dd>{frames_count}</dd></div>
  </dl>
</section>

{photo_blocks}

<section class="frame spread">
  <div>
    <div class="stamp" data-en="On atmosphere" data-ar="عن الأجواء">On atmosphere</div>
    <h2 data-en="{left_h_en}" data-ar="{left_h_ar}">{left_h_en}</h2>
    <p data-en="{left_p_en}" data-ar="{left_p_ar}">{left_p_en}</p>
  </div>
  <div>
    <div class="stamp" data-en="On material" data-ar="عن المادة">On material</div>
    <p data-en="{right_p_en}" data-ar="{right_p_ar}">{right_p_en}</p>
  </div>
</section>

{tail_photos}

<section class="frame end">
  <div class="stamp" data-en="End of chapter {n}" data-ar="نهاية الفصل {n}">End of chapter {n}</div>
  <h2>{title_ar} · {title_en}</h2>
  <div class="nav">
    <a href="index.html" data-en="← All frames" data-ar="→ كل الإطارات">← All frames</a>
    <span class="accent">·</span>
    <a href="index.html#colophon" data-en="Contact →" data-ar="← تواصل">Contact →</a>
  </div>
</section>

<script>
  let lang = localStorage.getItem('lang') || 'en';
  function applyLanguage() {{
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    localStorage.setItem('lang', lang);
    document.querySelectorAll('[data-en]').forEach(el => {{
      const v = el.dataset[lang === 'ar' ? 'ar' : 'en'];
      if (v != null) el.textContent = v;
    }});
    document.getElementById('lang-toggle').textContent = lang === 'en' ? 'AR' : 'EN';
  }}
  document.addEventListener('DOMContentLoaded', () => {{
    applyLanguage();
    document.getElementById('lang-toggle').addEventListener('click', () => {{
      lang = lang === 'en' ? 'ar' : 'en'; applyLanguage();
    }});
  }});
</script>

</body>
</html>
"""


PHOTO_BLOCK = """<section class="frame photo" style="background-image:url('{src}')">
  <div class="frame-num">{seq}<span class="label">Frame</span></div>
  <div class="caption">
    <span class="stamp" data-en="{stamp_en}" data-ar="{stamp_ar}">{stamp_en}</span>
    <span data-en="{cap_en}" data-ar="{cap_ar}">{cap_en}</span>
  </div>
</section>
"""


def build_photo_block(images, captions, start_seq):
    blocks = []
    for i, src in enumerate(images):
        if i >= len(captions):
            break
        stamp_en, cap_en, stamp_ar, cap_ar = captions[i]
        blocks.append(PHOTO_BLOCK.format(
            src=src, seq=str(start_seq + i).zfill(2),
            stamp_en=stamp_en, cap_en=cap_en, stamp_ar=stamp_ar, cap_ar=cap_ar,
        ))
    return "\n".join(blocks)


def build_page(project):
    folder = ROOT / project["folder"]
    images = collect_photo_paths(folder)
    captions = CAPTIONS.get(project["slug"], [])
    bio = BIO[project["slug"]]
    n_caps = min(len(captions), len(images))
    half = max(1, (n_caps + 1) // 2)
    head_imgs = images[:half]
    head_caps = captions[:half]
    tail_imgs = images[half:n_caps]
    tail_caps = captions[half:n_caps]
    head_block = build_photo_block(head_imgs, head_caps, start_seq=2)
    tail_block = build_photo_block(tail_imgs, tail_caps, start_seq=2 + half + 1)
    frames_count = str(2 + n_caps + 1).zfill(2)  # open + photos + spread + end
    return PAGE_TEMPLATE.format(
        n=project["n"], title_en=project["en"], title_ar=project["ar"],
        type_en=project["type_en"], type_ar=project["type_ar"],
        loc_en=project["loc_en"], loc_ar=project["loc_ar"], year=project["year"],
        deck_en=bio["deck_en"], deck_ar=bio["deck_ar"],
        left_h_en=bio["left_h_en"], left_h_ar=bio["left_h_ar"],
        left_p_en=bio["left_p_en"], left_p_ar=bio["left_p_ar"],
        right_p_en=bio["right_p_en"], right_p_ar=bio["right_p_ar"],
        photo_blocks=head_block, tail_photos=tail_block,
        frames_count=frames_count,
    )


def main():
    for p in PROJECTS:
        if p["slug"] == "almamlaka":
            # already hand-written; preserve
            continue
        out = VARIANT / f"project-{p['slug']}.html"
        out.write_text(build_page(p), encoding="utf-8")
        print(f"  wrote {out.name}")
    print(f"Generated {len(PROJECTS) - 1} project pages.")


if __name__ == "__main__":
    main()
