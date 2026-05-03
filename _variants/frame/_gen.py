"""Generate project pages for the elegant Frame variant.

Each project page is a long editorial spread: opening with title and meta,
a lead plate, a bilingual description, and a paginated sequence of plates
with captions. No scroll-snap; smooth continuous reading.
"""
from __future__ import annotations
import re
from pathlib import Path

VARIANT = Path(__file__).parent
ROOT = VARIANT.parent.parent  # Hadeel Algheshaian/
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_FOLDER_RE = re.compile(r"(2d\s*drawing|floor\s*plan|cross\s*section|elevation|project\s*start)", re.I)
PREFIX = "../../"

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
        "h_en": "A building that would feel inevitable.",
        "h_ar": "مبنى يبدو وكأنه كان دائماً هنا.",
        "p1_en": "The brief for ALMAMLAKA was unusual in that it asked, in different words, for a building that would feel inevitable. The site is a corner of a contemporary mall — bright, hurried, indifferent to history — and the client wanted a counter-current. The interior had to carry the gravity of a place that had been there for a while, while remaining, of course, very new.",
        "p1_ar": "كان البرنامج لمشروع المملكة غير مألوف، إذ طلب — بكلماتٍ مختلفة — مبنىً يبدو وكأنه كان دائماً هنا. الموقع زاوية في مولٍّ معاصر — مضيءٍ، مستعجل، لا مبالٍ بالتاريخ — وأراد العميل تياراً معاكساً. كان على الفضاء الداخلي أن يحمل ثقل مكانٍ كان موجوداً منذ زمنٍ، مع أنه — بطبيعة الحال — جديد تماماً.",
        "p2_en": "The first move was the threshold: a deep porch of brick coursing and tasselled pendants that does the labour of an actual masonry wall, even though it is, in plan, only forty centimetres of frame. From this porch, sightlines slow. Inside, the strategy is reduction — a single colour story, terracotta, brass, bone, and a single rule about light: it falls, never glares.",
        "p2_ar": "كان أول قرارٍ هو العتبة: شُرفة عميقة من طبقات الطوب والتعليقات المهدّبة، تقوم بعمل جدارٍ بنّاءٍ كاملٍ، رغم أنها في المسقط أربعون سنتيمتراً من الإطار فحسب. من هذه الشُرفة، تتباطأ خطوط النظر. في الداخل، الاستراتيجية اختزال — حكاية لونٍ واحدة، تيراكوتا، نحاس، عظم، وقاعدةٌ واحدة عن الضوء: يقع، لا يُبهر.",
    },
    "coffee-day": {
        "deck_en": "Three booths designed for International Coffee Day — French, Saudi, and a contemporary outlier — share one structural language.",
        "deck_ar": "ثلاثة أجنحة لمعرض يوم القهوة العالمي — فرنسي، سعودي، ومعاصر — تتشارك لغة إنشائية واحدة.",
        "h_en": "One language; three accents.",
        "h_ar": "لغةٌ واحدة؛ ثلاث لهجات.",
        "p1_en": "Each booth pulls material register from a different coffee tradition: marble and brass for the French, palm and copper for the Saudi, painted plywood and glass for the contemporary outlier. Underneath, the structure is the same: an elevated plinth, a hovering canopy, a counter at standing height.",
        "p1_ar": "كل جناحٍ يستلهم مادته من تقليد قهوة مختلف: رخامٌ ونحاس للفرنسي، سعفٌ ونحاس للسعودي، خشبٌ معاكسٌ مدهون وزجاج للمعاصر. تحتها، البنية واحدة: قاعدة مرتفعة، مظلّة معلّقة، طاولةٌ بارتفاع الوقوف.",
        "p2_en": "Repetition makes the difference legible. A visitor moving between the three booths reads the structural language as a constant and the material variation as the argument — a small lesson, in passing, about how interior design works.",
        "p2_ar": "التكرار يجعل الفروق واضحة. الزائر الذي ينتقل بين الأجنحة الثلاثة يقرأ اللغة الإنشائية ثابتةً والتنوّع الماديَّ هو الحجّة — درسٌ صغير، عابر، عن كيفية عمل التصميم الداخلي.",
    },
    "courtyard": {
        "deck_en": "A small open-air courtyard composed around a single tree and the slow movement of light over stone.",
        "deck_ar": "فناء مفتوح صغير مُؤلَّف حول شجرةٍ واحدة وحركة الضوء البطيئة على الحجر.",
        "h_en": "The plan does little; the air does the work.",
        "h_ar": "المسقط يفعل القليل؛ الهواء يقوم بالباقي.",
        "p1_en": "A square of stone, four shaded edges, one tree at the centre. The plan is almost diagrammatic — and the courtyard depends entirely on what arrives from outside it: the heat of the day, the angle of light, evening cool, and the quiet that gathers when nothing in particular is happening.",
        "p1_ar": "مربع من الحجر، أربع حوافٍّ مظللة، شجرةٌ واحدة في المنتصف. المسقط شبه تخطيطي، والفناء يعتمد كلّياً على ما يصله من خارجه: حرارة النهار، زاوية الضوء، برودة المساء، والصمت الذي يتجمّع حين لا يحدث شيءٌ بعينه.",
        "p2_en": "The composition is sensitive to the hours: a low sun on the west wall in the late afternoon, a deep shadow at noon, a slow blue at dusk. We chose stone of varied warmth across the four edges, so that the same hour reads differently depending on which wall you are sitting against.",
        "p2_ar": "التكوين حسّاسٌ للساعات: شمسٌ منخفضة على الجدار الغربي في ما بعد العصر، ظلٌّ عميق ظهراً، زرقةٌ بطيئة عند المغيب. اخترنا حجراً متفاوت الدفء بين الحواف الأربع، حتى تقرأ الساعة الواحدة بشكلٍ مختلف بحسب الجدار الذي تجلس مسنداً إليه.",
    },
    "lavender": {
        "deck_en": "A wellness centre organised around the slow tempo of treatment — yoga, massage, herbal preparation, retail.",
        "deck_ar": "مركز عافية مُنظَّم حول إيقاع العلاج البطيء — يوغا، مساج، تحضير أعشاب، تجزئة.",
        "h_en": "Transitions are places, not connectors.",
        "h_ar": "الانتقالات أماكنُ، لا ممرّات.",
        "p1_en": "The interior treats program transitions as places rather than connectors — small ante-rooms, tea steps, threshold benches — so the day decelerates as you move through it. By the time a guest reaches the treatment room, the city is, intentionally, several rooms behind them.",
        "p1_ar": "تتعامل الفضاءات مع الانتقالات بوصفها أماكنَ لا ممرّات — غرفٌ تمهيدية صغيرة، درجاتٌ للشاي، مقاعد عتبة — حتى يتباطأ النهار وأنت تمرّ به. مع وصول الضيف إلى غرفة العلاج، تكون المدينة — بقصدٍ — عدّة غرفٍ خلفه.",
        "p2_en": "The palette is olive, washed lavender, and oat. Lighting is layered and warm; sound is dampened by deep textile. The retail at the front of the building is, on purpose, the noisiest space — a small offering of activity that protects the quieter rooms behind it.",
        "p2_ar": "الألوان زيتونيّة، خزامى مغسولة، شوفان. الإضاءة طبقاتٌ دافئة؛ الصوت مُخمَدٌ بنسيجٍ عميق. التجزئة في مقدمة المبنى هي — بقصدٍ — الفضاء الأكثر صخباً، عرضٌ صغيرٌ للنشاط يحمي الغرفَ الأهدأ خلفه.",
    },
    "almaarefa": {
        "deck_en": "Lecture, library, studio, lounge — interiors that teach by atmosphere as much as by content.",
        "deck_ar": "محاضرات، مكتبة، مرسم، استراحة — فضاءاتٌ تُعلِّم بالأجواء كما بالمحتوى.",
        "h_en": "Materials carry the program.",
        "h_ar": "المواد تحمل البرنامج.",
        "p1_en": "Lecture is dense oak and dark felt. Library is paper, brass, and quiet. Studio is concrete and washable surface. Lounge is wool and soft light. Where signage would intrude, material does the work — students learn to recognise where they are by what the room is made of.",
        "p1_ar": "المحاضرات بلوطٌ كثيف ولبدٌ داكن. المكتبة ورقٌ ونحاس وصمت. المرسم خرسانة وسطحٌ قابل للغسل. الاستراحة صوفٌ وضوءٌ ناعم. حيث يكون التوجيه دخيلاً، تقوم المادة بالعمل — يتعلّم الطلاب التعرّف إلى أماكنهم من خامات الغرفة.",
        "p2_en": "Adjacencies were chosen so that students cross between registers — quiet and noisy, dense and open — many times a day. The plan is, in this sense, a curriculum: the building teaches the same lesson to a hundred people simultaneously.",
        "p2_ar": "اختيرت الجوارات بحيث يمرّ الطلاب بين السجلات — هادئة وصاخبة، كثيفة ومفتوحة — مرّاتٍ عديدة في اليوم. المسقط، بهذا المعنى، منهج: يُعلِّم المبنى الدرسَ ذاته لمئة شخصٍ في الوقت نفسه.",
    },
    "awjaj": {
        "deck_en": "Thirty-two keys arranged to slow a guest's first hour. One stone palette and one rule about light.",
        "deck_ar": "اثنان وثلاثون مفتاحاً مُرتَّبة لإبطاء أول ساعة للضيف. حكاية حجريةٌ واحدة وقاعدةٌ واحدة عن الضوء.",
        "h_en": "It should always feel late afternoon.",
        "h_ar": "يجب أن يبدو دائماً عند ما بعد العصر.",
        "p1_en": "Lobby, suite, and back-of-house all share one stone palette and one rule about light: it should always feel late afternoon. The first hour after a guest arrives is the entire design problem — by the time they reach their room, they should already be on holiday.",
        "p1_ar": "اللوبي، الجناح، الخدمات الخلفية — جميعها تتشارك في حكاية حجرية واحدة وقاعدةٍ واحدة عن الضوء: ينبغي أن يبدو دائماً عند ما بعد العصر. الساعة الأولى لوصول الضيف هي مشكلة التصميم بأكملها — مع وصوله إلى غرفته، ينبغي أن يكون قد دخل عطلته بالفعل.",
        "p2_en": "Joinery is quiet enough that the air conditioning is the loudest sound; the carpet, hand-knotted in a deep red, runs from the threshold all the way to the bed without an interruption. We removed every visual obstacle between the door and the window.",
        "p2_ar": "النجارة هادئةٌ بما يكفي لتصبح المُكيِّفُ هي الصوت الأعلى؛ السجاد، منسوجٌ يدوياً بحُمرة عميقة، يمتد من العتبة وحتى السرير دون انقطاع. أزلنا كل عقبةٍ بصرية بين الباب والنافذة.",
    },
    "culinary": {
        "deck_en": "Practical kitchens, dish stores, and the long counters they make possible. Material is the curriculum.",
        "deck_ar": "مطابخ تطبيقية، مخازن أطباق، والكاونترات الطويلة التي تتيحها. المادة هي المنهج.",
        "h_en": "Material is the curriculum.",
        "h_ar": "المادة هي المنهج.",
        "p1_en": "Copper, oak, steel, linen. Four materials, each with a teaching role: copper for heat, oak for the cut, steel for hygiene, linen for finishing. Students learn the building before they learn the lesson; by week two, they know where to stand for each task without being told.",
        "p1_ar": "نحاس، بلوط، فولاذ، كتان. أربع موادّ، لكلٍّ منها دورٌ تعليمي: النحاس للحرارة، البلوط للتقطيع، الفولاذ للنظافة، الكتان للتقديم. يتعلّم الطلاب المبنى قبل أن يتعلّموا الدرس؛ في الأسبوع الثاني، يعرفون أين يقفون لكل مهمّةٍ دون أن يُقال لهم.",
        "p2_en": "Plan is a long axis with stations on either side: prep, sauté, plate. Storage runs underneath; sightlines run through. The instructor, standing at one end, can see every student at every station — a sentence diagrammed in space.",
        "p2_ar": "المسقط محورٌ طويل بمحطّاتٍ على جانبيه: تحضير، قلي، تنضيد. التخزين تحته؛ خطوط النظر تمرّ عبره. يستطيع المدرّس، الواقف في طرفٍ واحد، أن يرى كل طالبٍ في كل محطّة — جملةٌ مرسومةٌ في الفضاء.",
    },
    "company": {
        "deck_en": "A corporate interior — restraint that still reads as branded. The answer was tone, not graphic.",
        "deck_ar": "تصميمٌ داخلي لمكاتب شركة — انضباطٌ يحمل هويةً واضحة. الجواب كان نبرةً، لا جرافيك.",
        "h_en": "Tone, not graphic.",
        "h_ar": "نبرة، لا جرافيك.",
        "p1_en": "Reception, waiting, manager's office, shared workfloor. The brief asked for restraint that still read as branded; the answer was tone — a single olive, a single brass, a single oak — repeated everywhere, so that the building becomes the wordmark.",
        "p1_ar": "استقبال، انتظار، مكتب مدير، قاعة عمل مشتركة. طلب البرنامج انضباطاً لا يخلو من الهوية؛ الجواب كان نبرةً — زيتونيٌّ واحد، نحاسٌ واحد، بلوطٌ واحد — مكرَّرة في كل مكان، حتى يصبح المبنى نفسه هو الشعار.",
        "p2_en": "No logos on walls. The branding is in the way the rooms behave: how light arrives, what gets reflected, how the air smells. The first impression a visitor takes home is not a graphic but a register of materials.",
        "p2_ar": "لا شعاراتٍ على الجدران. الهويّة في كيفية تصرّف الغرف: كيف يصل الضوء، ماذا ينعكس، كيف تكون رائحة الهواء. الانطباع الأول الذي يأخذه الزائر معه ليس جرافيكاً بل سجلاً من المواد.",
    },
}


def url_encode(p: str) -> str:
    return p.replace(" ", "%20")


def collect_photo_paths(project_dir: Path) -> list[str]:
    paths = []
    for sub in sorted(project_dir.iterdir(), key=lambda p: p.name):
        if not sub.is_dir() or SKIP_FOLDER_RE.search(sub.name):
            continue
        for f in sorted(sub.iterdir(), key=lambda p: p.name):
            if f.is_file() and f.suffix.lower() in IMG_EXT:
                rel = f"{PREFIX}{project_dir.name}/{sub.name}/{f.name}"
                paths.append(url_encode(rel))
    return paths


PAGE = """<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_en} — Hadeel Algheshaian</title>
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500&family=Tajawal:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --paper: oklch(96% 0.008 80); --paper-2: oklch(94% 0.008 75);
    --ink: oklch(22% 0.005 250); --graphite: oklch(38% 0.005 250); --quiet: oklch(58% 0.005 250);
    --rule: oklch(80% 0.008 80); --copper: oklch(56% 0.06 50);
    --display: 'Cormorant Garamond', Georgia, serif;
    --sans: 'Inter', system-ui, -apple-system, sans-serif;
    --ar: 'Tajawal', system-ui, sans-serif;
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{ background: var(--paper); color: var(--ink); font-family: var(--sans); font-weight: 300; font-size: 16px; line-height: 1.65; -webkit-font-smoothing: antialiased; overflow-x: hidden; }}
  html[lang="ar"] body {{ font-family: var(--ar); }}
  html[lang="ar"] *, html[lang="ar"] *::before, html[lang="ar"] *::after {{ letter-spacing: 0 !important; text-transform: none !important; }}
  a {{ color: inherit; text-decoration: none; }}
  ::selection {{ background: var(--ink); color: var(--paper); }}
  img {{ display: block; max-width: 100%; }}

  .bar {{
    position: sticky; top: 0; z-index: 50;
    display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 24px;
    padding: 22px 56px;
    background: oklch(96% 0.008 80 / 0.92); backdrop-filter: saturate(1.2) blur(8px); -webkit-backdrop-filter: saturate(1.2) blur(8px);
    border-bottom: 1px solid var(--rule);
    font-family: var(--sans); font-size: 11px; color: var(--graphite); letter-spacing: 0.32em; text-transform: uppercase;
  }}
  .bar-left {{ font-style: italic; font-family: var(--display); font-size: 17px; letter-spacing: 0; text-transform: none; color: var(--ink); }}
  .bar-center {{ color: var(--quiet); }}
  .bar-right {{ display: flex; gap: 22px; justify-content: flex-end; align-items: center; }}
  .bar-right a {{ font-size: 11px; letter-spacing: 0.18em; transition: color .25s; }}
  .bar-right a:hover {{ color: var(--copper); }}
  .bar button.toggle {{ background: transparent; border: 1px solid var(--rule); color: var(--graphite); font: inherit; font-size: 10px; letter-spacing: 0.18em; padding: 5px 11px; border-radius: 999px; cursor: pointer; }}
  .bar button.toggle:hover {{ border-color: var(--copper); color: var(--copper); }}

  /* opening */
  .opening {{
    padding: 9vh 80px 7vh;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: end;
    border-bottom: 1px solid var(--rule);
  }}
  .opening-eyebrow {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--copper); margin-bottom: 20px; display: flex; align-items: center; gap: 14px; }}
  .opening-eyebrow::before {{ content: ""; width: 32px; height: 1px; background: var(--copper); }}
  .opening-title {{
    font-family: var(--display); font-weight: 400; font-style: normal;
    font-size: clamp(56px, 7vw, 116px); line-height: 0.96; letter-spacing: -0.018em; margin: 0 0 12px; color: var(--ink);
  }}
  .opening-title em {{ font-style: italic; color: var(--copper); }}
  .opening-title-ar {{ font-family: var(--ar); font-size: clamp(28px, 3.5vw, 48px); line-height: 1.1; color: var(--quiet); margin: 0 0 28px; }}
  .opening-deck {{ font-family: var(--display); font-style: italic; font-size: 22px; line-height: 1.5; color: var(--graphite); max-width: 38ch; margin: 0; }}
  .opening-meta {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 28px 36px; align-self: end; }}
  .opening-meta dt {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--copper); margin: 0 0 6px; }}
  .opening-meta dd {{ margin: 0; font-family: var(--display); font-style: italic; font-size: 22px; color: var(--ink); }}
  .opening-meta dt::before {{ content: ""; display: inline-block; width: 18px; height: 1px; background: var(--copper); margin-right: 10px; vertical-align: 4px; }}

  /* lead plate */
  .lead {{
    padding: 0 80px;
    margin-top: -1px;
  }}
  .lead figure {{ margin: 0; aspect-ratio: 16/10; overflow: hidden; }}
  .lead figure img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(0.04); }}
  .lead figcaption {{
    margin-top: 14px;
    display: grid; grid-template-columns: 80px 1fr; gap: 18px; align-items: baseline;
    font-family: var(--sans); font-size: 10px; letter-spacing: 0.32em; text-transform: uppercase; color: var(--quiet);
  }}
  .lead figcaption .num {{ color: var(--copper); }}
  .lead figcaption .text {{ font-family: var(--display); font-style: italic; font-size: 14px; letter-spacing: 0; text-transform: none; color: var(--graphite); }}

  /* description (essay) — header full-width, body two columns under it */
  .essay {{
    padding: 11vh 80px 9vh;
    display: grid; grid-template-columns: 80px 1fr; column-gap: 32px; row-gap: 36px;
    border-bottom: 1px solid var(--rule);
  }}
  .essay-marker {{ font-family: var(--sans); font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--copper); padding-top: 18px; }}
  .essay h2 {{
    font-family: var(--display); font-weight: 400; font-size: clamp(36px, 4.4vw, 64px); line-height: 1.05; letter-spacing: -0.012em; margin: 0; color: var(--ink); max-width: 22ch;
  }}
  .essay-body {{ grid-column: 2; columns: 2; column-gap: 56px; font-family: var(--sans); font-size: 16px; line-height: 1.75; color: var(--graphite); }}
  .essay-body p {{ margin: 0 0 1.1em; text-align: justify; hyphens: auto; break-inside: avoid; }}
  .essay-body p:first-child::first-letter {{
    font-family: var(--display); font-style: italic; font-size: 4em; line-height: 0.85;
    float: left; padding: 0.06em 0.2em 0 0; color: var(--copper);
  }}
  html[lang="ar"] .essay-body p {{ text-align: justify; direction: rtl; }}
  html[lang="ar"] .essay-body p:first-child::first-letter {{ float: right; padding: 0 0 0 0.2em; }}

  /* plates — alternating editorial layout */
  .plates {{
    padding: 0 80px 14vh;
  }}
  .plates-marker {{ padding: 14vh 0 64px; font-family: var(--sans); font-size: 10px; letter-spacing: 0.4em; text-transform: uppercase; color: var(--copper); display: flex; align-items: center; gap: 14px; }}
  .plates-marker::before {{ content: ""; width: 32px; height: 1px; background: var(--copper); }}
  .plate-row {{
    display: grid; grid-template-columns: repeat(12, 1fr); gap: 24px; margin-bottom: 96px;
  }}
  .plate {{ display: flex; flex-direction: column; gap: 14px; }}
  .plate figure {{ margin: 0; overflow: hidden; aspect-ratio: 4/3; }}
  .plate figure.tall {{ aspect-ratio: 4/5; }}
  .plate figure.wide {{ aspect-ratio: 16/10; }}
  .plate img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(0.05); transition: filter .8s, transform 1.6s cubic-bezier(0.16, 1, 0.3, 1); }}
  .plate:hover img {{ filter: grayscale(0); transform: scale(1.02); }}
  .plate figcaption {{
    display: grid; grid-template-columns: 56px 1fr; gap: 14px; align-items: baseline;
    font-family: var(--sans); font-size: 10px; letter-spacing: 0.32em; text-transform: uppercase; color: var(--quiet);
  }}
  .plate figcaption .num {{ color: var(--copper); }}
  .plate figcaption .text {{ font-family: var(--display); font-style: italic; font-size: 14px; letter-spacing: 0; text-transform: none; color: var(--graphite); }}
  /* row variants */
  .row-pair .plate:nth-child(1) {{ grid-column: 1 / span 6; }}
  .row-pair .plate:nth-child(2) {{ grid-column: 7 / span 6; }}
  .row-asym .plate:nth-child(1) {{ grid-column: 1 / span 7; }}
  .row-asym .plate:nth-child(2) {{ grid-column: 9 / span 4; align-self: end; }}
  .row-asym-r .plate:nth-child(1) {{ grid-column: 2 / span 4; align-self: end; }}
  .row-asym-r .plate:nth-child(2) {{ grid-column: 6 / span 7; }}
  .row-full .plate {{ grid-column: 2 / span 10; }}

  /* footer nav */
  .endnav {{
    padding: 56px 80px;
    background: var(--ink); color: var(--paper);
    display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 24px;
  }}
  .endnav a {{
    font-family: var(--sans); font-size: 11px; letter-spacing: 0.32em; text-transform: uppercase;
    background: linear-gradient(currentColor, currentColor) bottom left / 0% 1px no-repeat; padding-bottom: 4px;
    transition: background-size .6s cubic-bezier(0.16, 1, 0.3, 1), color .25s;
  }}
  .endnav a:hover {{ color: var(--copper); background-size: 100% 1px; }}
  .endnav .center {{ text-align: center; font-family: var(--display); font-style: italic; font-size: 18px; letter-spacing: 0; text-transform: none; color: oklch(85% 0.005 60); }}
  .endnav .right {{ text-align: right; }}

  @media (max-width: 1100px) {{
    .opening, .essay, .plates, .endnav {{ padding-left: 40px; padding-right: 40px; }}
    .lead {{ padding-left: 40px; padding-right: 40px; }}
  }}
  @media (max-width: 760px) {{
    .bar {{ padding: 16px 22px; gap: 12px; }}
    .bar-right a {{ display: none; }}
    .opening, .essay, .endnav {{ padding-left: 22px; padding-right: 22px; }}
    .opening {{ padding-top: 8vh; padding-bottom: 6vh; grid-template-columns: 1fr; gap: 28px; }}
    .opening-meta {{ grid-template-columns: 1fr 1fr; }}
    .lead {{ padding-left: 22px; padding-right: 22px; }}
    .essay {{ padding-top: 8vh; padding-bottom: 8vh; grid-template-columns: 1fr; row-gap: 18px; }}
    .essay-marker {{ padding-top: 0; }}
    .essay-body {{ grid-column: 1; columns: 1; }}
    .essay-body p {{ text-align: left; }}
    .plates {{ padding: 0 22px 8vh; }}
    .plates-marker {{ padding-top: 8vh; padding-bottom: 32px; }}
    .plate-row {{ grid-template-columns: 1fr; gap: 24px; margin-bottom: 32px; }}
    .row-pair .plate, .row-asym .plate, .row-asym-r .plate, .row-full .plate {{ grid-column: 1; }}
    .endnav {{ padding: 32px 22px; grid-template-columns: 1fr; row-gap: 14px; text-align: center; }}
    .endnav .right {{ text-align: center; }}
  }}
</style>
</head>
<body>

<header class="bar">
  <a class="bar-left" href="index.html">Hadeel Algheshaian</a>
  <div class="bar-center" data-en="Chapter {n} / VIII" data-ar="الفصل {n} / ٨">Chapter {n} / VIII</div>
  <div class="bar-right">
    <a href="index.html" data-en="All work" data-ar="كل الأعمال">All work</a>
    <a href="contact.html" data-en="Contact" data-ar="تواصل">Contact</a>
    <button class="toggle" id="lang-toggle">AR</button>
  </div>
</header>

<section class="opening">
  <div>
    <div class="opening-eyebrow" data-en="Chapter {n} — {type_en}, {year}" data-ar="الفصل {n} — {type_ar}، {year}">Chapter {n} — {type_en}, {year}</div>
    <h1 class="opening-title">{title_en}<em>.</em></h1>
    <p class="opening-title-ar">{title_ar}</p>
    <p class="opening-deck" data-en="{deck_en}" data-ar="{deck_ar}">{deck_en}</p>
  </div>
  <dl class="opening-meta">
    <div><dt data-en="Year" data-ar="السنة">Year</dt><dd>{year}</dd></div>
    <div><dt data-en="Type" data-ar="النوع">Type</dt><dd data-en="{type_en}" data-ar="{type_ar}">{type_en}</dd></div>
    <div><dt data-en="Location" data-ar="الموقع">Location</dt><dd data-en="{loc_en}" data-ar="{loc_ar}">{loc_en}</dd></div>
    <div><dt data-en="Plates" data-ar="اللوحات">Plates</dt><dd>{plate_count}</dd></div>
  </dl>
</section>

<section class="lead">
  <figure>
    <img src="{lead_src}" alt="" loading="eager">
  </figure>
  <figcaption><span class="num">PL. I.</span><span class="text" data-en="{lead_caption_en}" data-ar="{lead_caption_ar}">{lead_caption_en}</span></figcaption>
</section>

<section class="essay">
  <div class="essay-marker">§ Brief</div>
  <h2 data-en="{h_en}" data-ar="{h_ar}">{h_en}</h2>
  <div class="essay-body">
    <p data-en="{p1_en}" data-ar="{p1_ar}">{p1_en}</p>
    <p data-en="{p2_en}" data-ar="{p2_ar}">{p2_en}</p>
  </div>
</section>

<section class="plates">
  <div class="plates-marker">§ Plates</div>
  {plate_rows}
</section>

<nav class="endnav">
  <a class="left" href="index.html" data-en="← Back to all work" data-ar="→ العودة إلى كل الأعمال">← Back to all work</a>
  <span class="center">{title_en} · {title_ar}</span>
  <a class="right" href="contact.html" data-en="Contact →" data-ar="← تواصل">Contact →</a>
</nav>

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


PLATE_LAYOUTS = ["row-pair", "row-asym", "row-pair", "row-asym-r", "row-full"]
PLATE_ASPECTS = ["", "tall", "", "wide", ""]

CAPTIONS = {
    "almamlaka":  ["Threshold; pendant work above brick.", "Hall, looking toward porch.", "Detail; brass and bone.", "Light; falling, never glaring.", "Pendants in repetition."],
    "coffee-day": ["French booth; marble and brass.", "Saudi booth; palm and copper.", "Contemporary outlier; soft glass.", "Three plinths; one canopy.", "Counter at standing height."],
    "courtyard":  ["Stone square, four edges.", "The single tree.", "Late afternoon on the west wall.", "Shadow at noon.", "Slow blue at dusk."],
    "lavender":   ["Threshold; lavender and oat.", "Treatment room.", "Tea step between rooms.", "Retail at the front.", "Joinery in the back."],
    "almaarefa":  ["Lecture; dense oak and dark felt.", "Library; paper, brass, quiet.", "Studio; concrete and washable.", "Lounge; wool and soft light.", "Plan as curriculum."],
    "awjaj":      ["Lobby; one stone palette.", "Suite; threshold to bed.", "Light; always late afternoon.", "Detail; horizontal brass.", "Carpet running to the window."],
    "culinary":   ["Copper; for heat.", "Oak; for the cut.", "Steel; for hygiene.", "Linen; for finishing.", "Long axis; stations either side."],
    "company":    ["Reception; olive, brass, oak.", "Waiting; one repeated detail.", "Manager's office; framed light.", "Workfloor; even ceiling.", "Tone, not graphic."],
}
CAPTIONS_AR = {
    "almamlaka":  ["العتبة؛ التعليقات فوق الطوب.", "القاعة، نظرة نحو الشُرفة.", "التفصيل؛ نحاس وعظم.", "الضوء؛ يقع، لا يُبهر.", "التعليقات في تكرار."],
    "coffee-day": ["الجناح الفرنسي؛ رخام ونحاس.", "الجناح السعودي؛ سعفٌ ونحاس.", "الجناح المعاصر؛ زجاجٌ ناعم.", "ثلاث قواعد؛ مظلّة واحدة.", "كاونتر بارتفاع الوقوف."],
    "courtyard":  ["مربع الحجر، أربع حواف.", "الشجرة الواحدة.", "ما بعد العصر على الجدار الغربي.", "ظلٌّ ظهراً.", "زرقةٌ بطيئة عند المغيب."],
    "lavender":   ["العتبة؛ خزامى وشوفان.", "غرفة العلاج.", "درجة الشاي بين الغرف.", "التجزئة في المقدمة.", "النجارة في الخلف."],
    "almaarefa":  ["المحاضرات؛ بلوطٌ كثيف ولبدٌ داكن.", "المكتبة؛ ورقٌ، نحاسٌ، صمت.", "المرسم؛ خرسانة وقابلٌ للغسل.", "الاستراحة؛ صوفٌ وضوءٌ ناعم.", "المسقط بوصفه منهجاً."],
    "awjaj":      ["اللوبي؛ حكاية حجريّة واحدة.", "الجناح؛ من العتبة إلى السرير.", "الضوء؛ دائماً ما بعد العصر.", "تفصيل؛ نحاسٌ أفقي.", "السجاد إلى النافذة."],
    "culinary":   ["النحاس؛ للحرارة.", "البلوط؛ للتقطيع.", "الفولاذ؛ للنظافة.", "الكتان؛ للتقديم.", "محورٌ طويل؛ محطّات على الجانبين."],
    "company":    ["الاستقبال؛ زيتوني، نحاس، بلوط.", "الانتظار؛ تفصيلٌ متكرر.", "مكتب المدير؛ ضوءٌ مؤطَّر.", "قاعة العمل؛ سقفٌ متجانس.", "نبرة، لا جرافيك."],
}


def roman(n):
    return ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'][n - 1]


def build_plate_rows(slug, images_after_lead):
    cap_en = CAPTIONS.get(slug, [])
    cap_ar = CAPTIONS_AR.get(slug, [])
    rows = []
    plate_idx = 2
    img_idx = 0
    layout_idx = 0
    while img_idx < len(images_after_lead) and layout_idx < len(PLATE_LAYOUTS):
        layout = PLATE_LAYOUTS[layout_idx]
        # row-full takes 1 image, others take 2
        n_in_row = 1 if layout == "row-full" else 2
        if img_idx + n_in_row > len(images_after_lead):
            n_in_row = len(images_after_lead) - img_idx
        if n_in_row == 1 and layout != "row-full":
            layout = "row-full"  # collapse trailing single to full
        plates_html = []
        for k in range(n_in_row):
            img = images_after_lead[img_idx + k]
            aspect = PLATE_ASPECTS[(layout_idx + k) % len(PLATE_ASPECTS)]
            cap_seq = plate_idx - 1
            cap_e = cap_en[cap_seq - 1] if cap_seq - 1 < len(cap_en) else ""
            cap_a = cap_ar[cap_seq - 1] if cap_seq - 1 < len(cap_ar) else ""
            plates_html.append(
                f'<div class="plate"><figure class="{aspect}"><img src="{img}" alt="" loading="lazy"></figure>'
                f'<figcaption><span class="num">PL. {roman(plate_idx)}</span>'
                f'<span class="text" data-en="{cap_e}" data-ar="{cap_a}">{cap_e}</span></figcaption></div>'
            )
            plate_idx += 1
        rows.append(f'<div class="plate-row {layout}">{"".join(plates_html)}</div>')
        img_idx += n_in_row
        layout_idx += 1
    return "\n".join(rows), plate_idx - 1


def build_page(project):
    folder = ROOT / project["folder"]
    images = collect_photo_paths(folder)
    if not images:
        print(f"  [warn] no images for {project['slug']}")
        return None
    lead = images[0]
    rest = images[1:]
    plate_rows, total_plates = build_plate_rows(project["slug"], rest)
    bio = BIO[project["slug"]]
    cap_en = CAPTIONS.get(project["slug"], [])
    cap_ar = CAPTIONS_AR.get(project["slug"], [])
    return PAGE.format(
        n=project["n"], title_en=project["en"], title_ar=project["ar"],
        type_en=project["type_en"], type_ar=project["type_ar"],
        loc_en=project["loc_en"], loc_ar=project["loc_ar"], year=project["year"],
        deck_en=bio["deck_en"], deck_ar=bio["deck_ar"],
        h_en=bio["h_en"], h_ar=bio["h_ar"],
        p1_en=bio["p1_en"], p1_ar=bio["p1_ar"],
        p2_en=bio["p2_en"], p2_ar=bio["p2_ar"],
        lead_src=lead,
        lead_caption_en=cap_en[0] if cap_en else "",
        lead_caption_ar=cap_ar[0] if cap_ar else "",
        plate_count=str(total_plates).zfill(2),
        plate_rows=plate_rows,
    )


def main():
    for p in PROJECTS:
        html = build_page(p)
        if html is None:
            continue
        out = VARIANT / f"project-{p['slug']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  wrote {out.name}")
    print(f"Generated {len(PROJECTS)} project pages.")


if __name__ == "__main__":
    main()
