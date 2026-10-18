"""AirShift core: dose model, scenario presets, plan optimizer and advisory text.

Shared by the notebook and the Streamlit dashboard so both use exactly the same logic.

Dose model
----------
Inhaled dose over a plan = sum over hours h of  C_h * BR_h * 1 hour
    C_h  : PM2.5 concentration in hour h (ug/m3)
    BR_h : breathing (inhalation) rate of the task done in hour h (m3/hour)
Result is in micrograms (ug) of PM2.5 inhaled.

Breathing rates are the mean short-term inhalation rates from U.S. EPA (2011),
Exposure Factors Handbook, Table 6-2 (males and females combined), converted
from m3/minute to m3/hour.
"""
from dataclasses import dataclass, field
from itertools import permutations

import numpy as np

FORECAST_HOURS = list(range(6, 22))  # target hours 06:00 to 21:00 on the planned day

# EPA EFH 2011 Table 6-2, mean values in m3/minute, converted to m3/hour (x 60)
BREATHING_RATE_M3_PER_H = {
    "adult": {"sedentary": 4.2e-3 * 60, "light": 1.2e-2 * 60, "moderate": 2.6e-2 * 60, "high": 5.0e-2 * 60},  # 21 to <31 years
    "youth": {"sedentary": 5.3e-3 * 60, "light": 1.2e-2 * 60, "moderate": 2.6e-2 * 60, "high": 4.9e-2 * 60},  # 16 to <21 years
}


@dataclass
class Task:
    name: str
    hours: int
    intensity: str  # sedentary, light, moderate, high


@dataclass
class Scenario:
    key: str
    label: str
    group: str               # "adult" or "youth"
    tasks: list
    window: tuple            # (first allowed start hour, end hour exclusive)
    fixed_start: int         # the usual schedule used as a comparison
    noun: dict = field(default_factory=dict)  # phrase per language for the advisory card

    @property
    def total_hours(self):
        return sum(t.hours for t in self.tasks)


WORK = {"en": "for your work", "mr": "कामासाठी", "hi": "काम के लिए", "ta": "வேலைக்காக"}
SPORT = {"en": "for sports practice", "mr": "खेळाच्या सरावासाठी", "hi": "खेल के अभ्यास के लिए", "ta": "விளையாட்டுப் பயிற்சிக்காக"}

SCENARIOS = {
    "construction": Scenario("construction", "Construction worker", "adult",
                             [Task("Heavy lifting", 2, "high"), Task("Site work", 4, "moderate")],
                             (6, 20), 9, WORK),
    "delivery": Scenario("delivery", "Delivery rider", "adult",
                         [Task("Delivery riding", 8, "moderate")], (6, 22), 10, WORK),
    "vendor": Scenario("vendor", "Street vendor", "adult",
                       [Task("Vending", 6, "light")], (6, 22), 16, WORK),
    "student_sports": Scenario("student_sports", "Student: sports practice", "youth",
                               [Task("Sports", 1, "high"), Task("Warm-up and drills", 1, "moderate")],
                               (6, 19), 17, SPORT),
}


def enumerate_plans(scenario):
    """All feasible plans: a start hour plus an order of the tasks, done back to back.

    Returns (plans, W) where W[p, h] is the breathing rate (m3/h) in clock hour h under plan p.
    """
    br = BREATHING_RATE_M3_PER_H[scenario.group]
    first, end = scenario.window
    orders = sorted(set(permutations(range(len(scenario.tasks)))))
    plans, rows = [], []
    for start in range(first, end - scenario.total_hours + 1):
        for order in orders:
            w = np.zeros(24)
            h = start
            for i in order:
                t = scenario.tasks[i]
                w[h:h + t.hours] = br[t.intensity]
                h += t.hours
            plans.append({"start": start, "order": order})
            rows.append(w)
    return plans, np.array(rows)


def fixed_plan_index(scenario, plans):
    natural = tuple(range(len(scenario.tasks)))
    for i, p in enumerate(plans):
        if p["start"] == scenario.fixed_start and p["order"] == natural:
            return i
    raise ValueError("fixed schedule is not feasible for this scenario")


def plan_doses(conc, W):
    """conc: (n_days, 24) concentrations; NaN allowed only where W is zero. Returns (n_days, n_plans) doses in ug."""
    c = np.where(np.isnan(conc), 0.0, conc)
    return c @ W.T


def best_plan(conc_24, scenario):
    """Best plan for a single day's 24-hour concentration vector."""
    plans, W = enumerate_plans(scenario)
    d = plan_doses(conc_24[None, :], W)[0]
    i = int(np.argmin(d))
    return plans[i], float(d[i]), plans, W, d


def worst_block(conc_24, scenario):
    """Contiguous block of the same total length with the highest forecast concentration (to avoid)."""
    first, end = scenario.window
    L = scenario.total_hours
    best_s, best_v = first, -np.inf
    for s in range(first, end - L + 1):
        v = np.nansum(conc_24[s:s + L])
        if v > best_v:
            best_s, best_v = s, v
    return best_s, best_s + L


def confidence_label(start_lo, start_mid, start_hi):
    """Agreement of the plans chosen with the lower bound, point forecast and upper bound."""
    spread = max(start_lo, start_mid, start_hi) - min(start_lo, start_mid, start_hi)
    return "high" if spread <= 1 else ("medium" if spread <= 3 else "low")


# ---------------------------------------------------------------- advisory text
CITY_NAMES = {
    "mr": {"Delhi": "दिल्ली", "Gurugram": "गुरुग्राम", "Lucknow": "लखनौ", "Kanpur": "कानपूर", "Varanasi": "वाराणसी", "Agra": "आग्रा", "Jaipur": "जयपूर", "Jodhpur": "जोधपूर", "Chandigarh": "चंदीगड", "Amritsar": "अमृतसर", "Ludhiana": "लुधियाना", "Dehradun": "डेहराडून", "Shimla": "शिमला", "Srinagar": "श्रीनगर", "Kolkata": "कोलकाता", "Patna": "पाटणा", "Muzaffarpur": "मुझफ्फरपूर", "Ranchi": "रांची", "Bhubaneswar": "भुवनेश्वर", "Raipur": "रायपूर", "Guwahati": "गुवाहाटी", "Shillong": "शिलाँग", "Aizawl": "ऐझॉल", "Agartala": "आगरतळा", "Imphal": "इंफाळ", "Gangtok": "गंगटोक", "Mumbai": "मुंबई", "Pune": "पुणे", "Nagpur": "नागपूर", "Ahmedabad": "अहमदाबाद", "Surat": "सुरत", "Bhopal": "भोपाळ", "Indore": "इंदूर", "Gwalior": "ग्वाल्हेर", "Chennai": "चेन्नई", "Coimbatore": "कोइंबतूर", "Tiruchirappalli": "तिरुचिरापल्ली", "Vellore": "वेल्लोर", "Salem": "सेलम", "Bengaluru": "बेंगळुरू", "Mysuru": "म्हैसूर", "Hyderabad": "हैदराबाद", "Visakhapatnam": "विशाखापट्टणम", "Vijayawada": "विजयवाडा", "Thiruvananthapuram": "तिरुवनंतपुरम", "Kochi": "कोची", "Your location": "तुमचे ठिकाण"},
    "hi": {"Delhi": "दिल्ली", "Gurugram": "गुरुग्राम", "Lucknow": "लखनऊ", "Kanpur": "कानपुर", "Varanasi": "वाराणसी", "Agra": "आगरा", "Jaipur": "जयपुर", "Jodhpur": "जोधपुर", "Chandigarh": "चंडीगढ़", "Amritsar": "अमृतसर", "Ludhiana": "लुधियाना", "Dehradun": "देहरादून", "Shimla": "शिमला", "Srinagar": "श्रीनगर", "Kolkata": "कोलकाता", "Patna": "पटना", "Muzaffarpur": "मुज़फ़्फ़रपुर", "Ranchi": "रांची", "Bhubaneswar": "भुवनेश्वर", "Raipur": "रायपुर", "Guwahati": "गुवाहाटी", "Shillong": "शिलांग", "Aizawl": "आइज़ोल", "Agartala": "अगरतला", "Imphal": "इंफाल", "Gangtok": "गंगटोक", "Mumbai": "मुंबई", "Pune": "पुणे", "Nagpur": "नागपुर", "Ahmedabad": "अहमदाबाद", "Surat": "सूरत", "Bhopal": "भोपाल", "Indore": "इंदौर", "Gwalior": "ग्वालियर", "Chennai": "चेन्नई", "Coimbatore": "कोयंबटूर", "Tiruchirappalli": "तिरुचिरापल्ली", "Vellore": "वेल्लोर", "Salem": "सेलम", "Bengaluru": "बेंगलुरु", "Mysuru": "मैसूर", "Hyderabad": "हैदराबाद", "Visakhapatnam": "विशाखापत्तनम", "Vijayawada": "विजयवाड़ा", "Thiruvananthapuram": "तिरुवनंतपुरम", "Kochi": "कोच्चि", "Your location": "आपका स्थान"},
    "ta": {"Delhi": "டெல்லி", "Gurugram": "குருகிராம்", "Lucknow": "லக்னோ", "Kanpur": "கான்பூர்", "Varanasi": "வாராணசி", "Agra": "ஆக்ரா", "Jaipur": "ஜெய்ப்பூர்", "Jodhpur": "ஜோத்பூர்", "Chandigarh": "சண்டிகர்", "Amritsar": "அமிர்தசரஸ்", "Ludhiana": "லுதியானா", "Dehradun": "டேராடூன்", "Shimla": "சிம்லா", "Srinagar": "ஸ்ரீநகர்", "Kolkata": "கொல்கத்தா", "Patna": "பாட்னா", "Muzaffarpur": "முசாஃபர்பூர்", "Ranchi": "ராஞ்சி", "Bhubaneswar": "புவனேஸ்வர்", "Raipur": "ராய்ப்பூர்", "Guwahati": "குவாஹாட்டி", "Shillong": "ஷில்லாங்", "Aizawl": "ஐஸ்வால்", "Agartala": "அகர்தலா", "Imphal": "இம்பால்", "Gangtok": "காங்டாக்", "Mumbai": "மும்பை", "Pune": "புனே", "Nagpur": "நாக்பூர்", "Ahmedabad": "அகமதாபாத்", "Surat": "சூரத்", "Bhopal": "போபால்", "Indore": "இந்தூர்", "Gwalior": "குவாலியர்", "Chennai": "சென்னை", "Coimbatore": "கோயம்புத்தூர்", "Tiruchirappalli": "திருச்சிராப்பள்ளி", "Vellore": "வேலூர்", "Salem": "சேலம்", "Bengaluru": "பெங்களூரு", "Mysuru": "மைசூரு", "Hyderabad": "ஹைதராபாத்", "Visakhapatnam": "விசாகப்பட்டினம்", "Vijayawada": "விஜயவாடா", "Thiruvananthapuram": "திருவனந்தபுரம்", "Kochi": "கொச்சி", "Your location": "உங்கள் இடம்"},
}
DAY_WORDS = {"tomorrow": {"en": "Tomorrow", "mr": "उद्या", "hi": "कल", "ta": "நாளை"},
             "today": {"en": "Today", "mr": "आज", "hi": "आज", "ta": "இன்று"}}
CONF_WORDS = {"en": {"high": "high", "medium": "medium", "low": "low"},
              "mr": {"high": "जास्त", "medium": "मध्यम", "low": "कमी"},
              "hi": {"high": "ज़्यादा", "medium": "मध्यम", "low": "कम"},
              "ta": {"high": "அதிகம்", "medium": "நடுத்தரம்", "low": "குறைவு"}}
PERIODS = {"mr": ("सकाळी", "दुपारी", "संध्याकाळी", "रात्री"), "hi": ("सुबह", "दोपहर", "शाम", "रात"),
           "ta": ("காலை", "மதியம்", "மாலை", "இரவு")}


def _period(h):
    h %= 24
    if 4 <= h <= 11:
        return 0
    if 12 <= h <= 16:
        return 1
    if 17 <= h <= 19:
        return 2
    return 3


def _clock12(h):
    h %= 24
    return 12 if h % 12 == 0 else h % 12


def format_window(start, end, lang):
    if lang == "en":
        f = lambda h: f"{_clock12(h)} {'AM' if (h % 24) < 12 else 'PM'}"
        return f"{f(start)} to {f(end)}"
    p = PERIODS[lang]
    a = f"{p[_period(start)]} {_clock12(start)}"
    b = f"{_clock12(end)}" if _period(start) == _period(end) else f"{p[_period(end)]} {_clock12(end)}"
    if lang == "ta":
        return f"{a} மணி முதல் {b} மணி வரை"
    return f"{a} ते {b}" if lang == "mr" else f"{a} से {b} बजे तक"


def advisory_card(city, date_str, scenario, best_start, worst, expected_saving_pct, confidence, lang="en",
                  day="tomorrow", show_saving=True):
    """Short advice in English, Marathi or Hindi. Set show_saving=False when the usual time is not comparable
    (for example when planning the rest of today and the usual start has already passed)."""
    best = format_window(best_start, best_start + scenario.total_hours, lang)
    avoid = format_window(worst[0], worst[1], lang)
    fixed = format_window(scenario.fixed_start, scenario.fixed_start + scenario.total_hours, lang)
    conf = CONF_WORDS[lang][confidence]
    pct = int(round(expected_saving_pct))
    noun = scenario.noun[lang]
    dw = DAY_WORDS[day][lang]
    if lang == "en":
        saving = (f"Compared with your usual time ({fixed}), this could cut the pollution you breathe in by about {pct}%."
                  if pct >= 5 else "Your usual time is already close to the best.")
        lines = [f"{city} | {dw}, {date_str}", f"Best time {noun}: {best}", f"Avoid if you can: {avoid}", saving,
                 f"Forecast confidence: {conf}"]
    elif lang == "mr":
        saving = (f"नेहमीच्या वेळेपेक्षा ({fixed}) श्वासातून जाणारे प्रदूषण सुमारे {pct}% कमी होऊ शकते."
                  if pct >= 5 else "तुमची नेहमीची वेळही जवळपास सर्वात चांगली आहे.")
        lines = [f"{CITY_NAMES['mr'].get(city, city)} | {dw}, {date_str}", f"{noun} सर्वात चांगली वेळ: {best}",
                 f"शक्य असल्यास टाळा: {avoid}", saving, f"अंदाजाची खात्री: {conf}"]
    elif lang == "ta":
        saving = (f"உங்கள் வழக்கமான நேரத்தை ({fixed}) விட, நீங்கள் சுவாசிக்கும் மாசு சுமார் {pct}% குறையலாம்."
                  if pct >= 5 else "உங்கள் வழக்கமான நேரமே ஏறக்குறைய சிறந்த நேரம்தான்.")
        lines = [f"{CITY_NAMES['ta'].get(city, city)} | {dw}, {date_str}", f"{noun} சிறந்த நேரம்: {best}",
                 f"முடிந்தால் இந்த நேரத்தைத் தவிர்க்கவும்: {avoid}", saving, f"முன்னறிவிப்பின் நம்பகத்தன்மை: {conf}"]
    else:
        saving = (f"सामान्य समय ({fixed}) की तुलना में साँस से अंदर जाने वाला प्रदूषण लगभग {pct}% कम हो सकता है।"
                  if pct >= 5 else "आपका सामान्य समय भी लगभग सबसे अच्छा है।")
        lines = [f"{CITY_NAMES['hi'].get(city, city)} | {dw}, {date_str}", f"{noun} सबसे अच्छा समय: {best}",
                 f"हो सके तो इस समय से बचें: {avoid}", saving, f"अनुमान पर भरोसा: {conf}"]
    if not show_saving:
        lines.pop(3)
    return "\n".join(lines)
