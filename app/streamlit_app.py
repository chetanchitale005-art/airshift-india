"""AirShift India dashboard (simple version, in English, Tamil, Marathi and Hindi).

From the project folder:  streamlit run app/streamlit_app.py
Photos: drop real JPG or PNG files named like the SVGs in app/assets/ (for example construction.jpg) and they replace the drawings.
"""
import base64
import html
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "src"))
import airshift_core as ac  # noqa: E402
import live  # noqa: E402
from ui_text import CATEGORY_NAMES, EFFORT, LANG_LABELS, ROLES, T, task_name  # noqa: E402

OUT = BASE / "outputs"
APP, FIG, TAB = OUT / "app", OUT / "figures", OUT / "tables"
ASSETS = BASE / "app" / "assets"
CAT_COLORS = ["#3C9D4E", "#9ACD52", "#F2C330", "#F08A24", "#D7301F", "#7F1416"]
BINS = [-0.001, 30, 60, 90, 120, 250, np.inf]
SEASON_COLORS = {"Winter": "#2A6F97", "Pre-monsoon": "#C98A14", "Monsoon": "#2F8F5B", "Post-monsoon": "#A23B3B"}
ROLE_BY_LABEL = {sc.label: k for k, sc in ac.SCENARIOS.items()}

st.set_page_config(page_title="AirShift", page_icon="☀️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800&family=Noto+Sans+Tamil:wght@400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap');
html { font-size: 17px; }
html, body, .stApp, .stApp p, .stApp li, .stApp label, .stApp button, .stApp input, .stApp textarea,
.stApp h1, .stApp h2, .stApp h3, .stApp [data-baseweb] {
  font-family: 'Noto Sans', 'Noto Sans Tamil', 'Noto Sans Devanagari', sans-serif !important;
}
.block-container { padding-top: 1.2rem; max-width: 100%; padding-left: 3rem; padding-right: 3rem; }
.hero { border-radius: 22px; background-size: cover; background-position: center; padding: 1.6rem 1.8rem 1.4rem;
        margin: .4rem 0 1rem; border: 1px solid #D9E2E7; }
.brand { font-weight: 800; font-size: 2.6rem; letter-spacing: -.01em; color: #1E2A32; line-height: 1; margin: 0; }
.brand span { color: #2A6F97; }
.tagline { font-size: 1.2rem; color: #2B3B45; margin: .45rem 0 0 0; font-weight: 600; }
.intro { font-size: 1.12rem; color: #2B3B45; margin: .2rem 0 .8rem; }
.stTabs [data-baseweb="tab"] { font-size: 1.08rem; font-weight: 600; padding: .6rem 1rem; }
.stTabs [aria-selected="true"] { color: #2A6F97 !important; }
.section { font-weight: 700; font-size: 1.35rem; color: #1E2A32; margin: 1.5rem 0 .4rem; }
.stButton > button { border-radius: 14px; min-height: 3.1rem; font-weight: 700; font-size: 1.05rem; }
.stButton > button[kind="primary"] { background: #2F8F5B; border-color: #2F8F5B; }
.rolecard { margin-bottom: .6rem; }
.rolecard img { width: 100%; aspect-ratio: 4 / 3; object-fit: contain; background: #EEF3F6; border-radius: 16px; border: 3px solid #D9E2E7; display: block; }
.rolecard.on img { border-color: #2F8F5B; box-shadow: 0 0 0 3px #CDEBD8; }
.answer { background: #FFFFFF; border: 1px solid #D9E2E7; border-left: 8px solid #2F8F5B; border-radius: 16px; padding: 1.2rem 1.5rem 1.1rem; }
.answer .where { color: #2B3B45; font-size: 1.05rem; margin-bottom: .2rem; }
.answer .label { color: #2F8F5B; font-weight: 700; font-size: 1.1rem; margin-top: .3rem; }
.answer .time { font-weight: 800; font-size: 2.8rem; letter-spacing: -.01em; line-height: 1.15; color: #1E2A32; margin: .1rem 0 .35rem; }
.answer .order { color: #1E2A32; font-size: 1.1rem; margin-bottom: .8rem; }
.answer .row { display: flex; gap: .6rem; align-items: baseline; margin: .35rem 0; font-size: 1.08rem; color: #1E2A32; }
.answer .dot { width: .8rem; height: .8rem; border-radius: 50%; display: inline-block; flex: none; transform: translateY(1px); }
.answer .conf { margin-top: .9rem; color: #2B3B45; font-size: 1rem; }
.answer .conf b { color: #1E2A32; letter-spacing: .12em; }
.strip { display: grid; grid-template-columns: repeat(16, minmax(0, 1fr)); column-gap: 5px; row-gap: 5px; margin: .5rem 0 .2rem; }
.barcell { height: 80px; display: flex; flex-direction: column; justify-content: flex-end; align-items: stretch; }
.bar { border-radius: 6px 6px 2px 2px; min-height: 6px; }
.val { text-align: center; font-size: .8rem; color: #2B3B45; margin-bottom: 2px; }
.hr { text-align: center; font-weight: 700; font-size: 1.05rem; color: #1E2A32; line-height: 1.05; }
.hr small { display: block; font-weight: 400; font-size: .72rem; color: #44545E; }
.dim { opacity: .35; }
.bracket { border-radius: 8px; font-size: .92rem; padding: .2rem .45rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bracket.plan { background: #2F8F5B; color: #FFFFFF; font-weight: 700; }
.bracket.usual { background: transparent; color: #2B3B45; border: 1.5px dashed #8A9AA4; }
.period { font-size: .9rem; color: #44545E; border-top: 1px solid #D9E2E7; padding-top: .15rem; }
.legend { display: flex; flex-wrap: wrap; gap: .3rem .95rem; font-size: .95rem; color: #2B3B45; margin-top: .6rem; }
.legend i { display: inline-block; width: .85rem; height: .85rem; border-radius: 4px; margin-right: .3rem; vertical-align: -1px; }
.note { color: #44545E; font-size: .95rem; }
@media (max-width: 640px) {
  .brand { font-size: 2rem; }
  .answer .time { font-size: 2.1rem; }
  .hr { font-size: .9rem; }
  .hr small, .val { display: none; }
  .barcell { height: 60px; }
  .bracket { font-size: .75rem; }
  .hero { padding: 1.1rem 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

if not (APP / "summary.json").exists():
    st.error("Results are missing from outputs/app. Run AirShift_India.ipynb from start to finish, then reload this page.")
    st.stop()


@st.cache_data
def load():
    summary = json.loads((APP / "summary.json").read_text())
    return (summary, pd.read_csv(APP / "forecasts.csv.gz"), pd.read_csv(APP / "profiles.csv"),
            pd.read_csv(APP / "city_meta.csv").set_index("City"))


@st.cache_data
def image_uri(name):
    """Photo or drawing for a name: app/assets/<name>.jpg, .png or .svg (first one found), as a data URI."""
    for ext, mime in ((".jpg", "image/jpeg"), (".png", "image/png"), (".svg", "image/svg+xml")):
        p = ASSETS / f"{name}{ext}"
        if p.exists():
            return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    return ""


@st.cache_data
def example_dates():
    """A typical good day per city (construction worker, high confidence, saving near the 75th percentile)."""
    p = TAB / "22_backtest_daily.csv.gz"
    if not p.exists():
        return {}
    b = pd.read_csv(p)
    b = b[(b["scenario"] == "Construction worker") & (b["period"].isin(["test", "newcity"])) & (b["confidence"] == "high")].copy()
    b["gain"] = 1 - b["AirShift"] / b["Usual schedule"]
    out = {}
    for c, g in b.groupby("City"):
        out[c] = str(g.iloc[(g["gain"] - g["gain"].quantile(0.75)).abs().argsort().iloc[0]]["date"])[:10]
    return out


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_live(lat, lon):
    return live.fetch_pm25(lat, lon), live.now_ist().strftime("%d %b %Y, %H:%M IST")


S, FC, PROF, META = load()
CORE, NEW = S["core_cities"], S["new_cities"]
CITIES = CORE + NEW
PROFILE_CITIES = set(PROF["City"].unique())


def table(name, **kw):
    p = TAB / f"{name}.csv"
    return pd.read_csv(p, **kw) if p.exists() else pd.DataFrame()


def figure(name, caption=None):
    p = FIG / f"{name}.png"
    if p.exists():
        st.image(str(p), caption=caption)


def city_name(c, lang):
    return c if lang == "en" else ac.CITY_NAMES.get(lang, {}).get(c, c)


def city_label(c, lang):
    tx = T[lang]
    return f"{city_name(c, lang)}, {META.loc[c, 'State']}" + ("" if c in CORE else f" {tx['new_tag']}")


def typical_day(city, month):
    if city not in PROFILE_CITIES:
        return None
    season = "Winter" if month in (1, 2) else "Pre-monsoon" if month <= 5 else "Monsoon" if month <= 9 else "Post-monsoon"
    return PROF[(PROF["City"] == city) & (PROF["season"] == season)].set_index("hour")["median"].reindex(range(24)).to_numpy(dtype=float)


def hour_label(h, lang):
    n = 12 if h % 12 == 0 else h % 12
    return f"{n}<small>{'AM' if h < 12 else 'PM'}</small>" if lang == "en" else f"{n}"


def category(v):
    return int(np.digitize(v, BINS[1:-1], right=True)) if not np.isnan(v) else None


def day_strip(values, plan_start, length, usual_start, lang, window, actual=None, now_hour=None):
    """Bars from 06:00 to 21:00: height = PM2.5, colour = official category; plan and usual time marked."""
    tx = T[lang]
    hours = list(range(6, 22))
    col = lambda h: h - 5
    top = np.nanmax(values[6:22]) if np.isfinite(values[6:22]).any() else 1.0
    parts = [f'<div class="bracket plan" style="grid-row:1;grid-column:{col(plan_start)} / span {length}">{tx["your_plan"]}</div>']
    for h in hours:
        v, k = values[h], category(values[h])
        dim = " dim" if (h < window[0] or h >= window[1] or (now_hour is not None and h <= now_hour)) else ""
        if k is None:
            bar = '<div class="bar" style="background:#E3E9EC;height:6px"></div>'
            tip = f"{h:02d}:00"
        else:
            hpx = int(8 + 52 * v / top) if top > 0 else 8
            bar = f'<div class="val">{v:.0f}</div><div class="bar" style="background:{CAT_COLORS[k]};height:{hpx}px"></div>'
            tip = f"{h:02d}:00, {v:.0f} µg/m³, {CATEGORY_NAMES[lang][k]}"
        parts.append(f'<div class="barcell{dim}" title="{html.escape(tip)}" style="grid-row:2;grid-column:{col(h)}">{bar}</div>')
        parts.append(f'<div class="hr{dim}" style="grid-row:3;grid-column:{col(h)}">{hour_label(h, lang)}</div>')
    row = 4
    if usual_start is not None:
        parts.append(f'<div class="bracket usual" style="grid-row:{row};grid-column:{col(usual_start)} / span {length}">{tx["usual"]}</div>')
        row += 1
    if actual is not None:
        for h in hours:
            k = category(actual[h])
            bg = CAT_COLORS[k] if k is not None else "#E3E9EC"
            tip = f"{h:02d}:00, measured {actual[h]:.0f} µg/m³" if k is not None else f"{h:02d}:00, no measurement"
            parts.append(f'<div title="{html.escape(tip)}" style="grid-row:{row};grid-column:{col(h)};height:12px;border-radius:4px;background:{bg}"></div>')
        row += 1
    for (start, n), name in zip([(6, 6), (12, 5), (17, 3), (20, 2)], tx["periods"]):
        parts.append(f'<div class="period" style="grid-row:{row};grid-column:{col(start)} / span {n}">{name}</div>')
    legend = "".join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in zip(CAT_COLORS, CATEGORY_NAMES[lang]))
    return f'<div class="strip">{"".join(parts)}</div><div class="legend">{legend}</div>'


def section(text):
    st.markdown(f'<div class="section">{text}</div>', unsafe_allow_html=True)


def order_text(sc, order, lang):
    names = [html.escape(task_name(sc.tasks[i].name, lang)) for i in order]
    if lang == "en" and len(names) > 1:
        names = [n[:1].lower() + n[1:] for n in names]
    if len(names) == 1:
        return f"{names[0]}, {sc.tasks[order[0]].hours} h"
    if len(names) == 2:
        return T[lang]["first_then"].format(a=names[0], b=names[1])
    return f" {T[lang]['then']} ".join(names)


def answer_card(place, day_word, date_str, sc, plan, worst, saving_pct, confidence, lang):
    tx = T[lang]
    best = ac.format_window(plan["start"], plan["start"] + sc.total_hours, lang)
    avoid = ac.format_window(worst[0], worst[1], lang)
    rows = [f'<div class="row"><span class="dot" style="background:#D7301F"></span><span>{tx["avoid"]}: {avoid}</span></div>']
    if saving_pct is not None:
        fixed = ac.format_window(sc.fixed_start, sc.fixed_start + sc.total_hours, lang)
        text = tx["saving"].format(pct=int(round(saving_pct)), fixed=fixed) if saving_pct >= 5 else tx["usual_ok"]
        rows.append(f'<div class="row"><span class="dot" style="background:#2F8F5B"></span><span>{text}</span></div>')
    dots = {"high": "●●●", "medium": "●●○", "low": "●○○"}[confidence]
    return (f'<div class="answer"><div class="where">{html.escape(city_name(place, lang))}, {day_word} {date_str}</div>'
            f'<div class="label">{tx["best"]}</div><div class="time">{best}</div>'
            f'<div class="order">{order_text(sc, plan["order"], lang)}</div>{"".join(rows)}'
            f'<div class="conf">{tx["confidence"]}: <b>{dots}</b> {ac.CONF_WORDS[lang][confidence]}</div></div>')


def pick_role(state, k):
    st.session_state[state] = k


def choose_role(lang, key, default=None):
    """Five picture cards. The chosen one is green; each card has a big button under it. None until one is picked."""
    tx = T[lang]
    section(tx["who"])
    state = f"role_{key}"
    st.session_state.setdefault(state, default)
    cur = st.session_state[state]
    cols = st.columns(len(ROLES))
    for col, k in zip(cols, ROLES):
        with col:
            st.markdown(f'<div class="rolecard{" on" if k == cur else ""}"><img src="{image_uri(k)}" alt="{ROLES[k][lang]}"></div>',
                        unsafe_allow_html=True)
            st.button(ROLES[k][lang], key=f"pick_{key}_{k}", on_click=pick_role, args=(state, k),
                      type="primary" if k == cur else "secondary", use_container_width=True)
    if cur is None:
        return None
    if cur != "custom":
        return ac.SCENARIOS[cur]
    with st.container(border=True):
        st.markdown(f"**{tx['custom_title']}**")
        a, b, c, d = st.columns(4)
        group = a.selectbox(tx["group"], ["adult", "youth"], key=f"grp_{key}", format_func=lambda g: tx[g])
        start_w = b.number_input(tx["start_w"], 6, 21, 6, key=f"sw_{key}")
        end_w = c.number_input(tx["end_w"], 7, 22, 20, key=f"ew_{key}")
        usual = d.number_input(tx["usual_start"], 6, 21, 9, key=f"us_{key}")
        tasks = []
        for i in range(3):
            x, y_, z = st.columns([2, 1, 1])
            name = x.text_input(f"{tx['task']} {i + 1}", value=[tx["work"], "", ""][i], key=f"tn{i}_{key}")
            hrs = y_.number_input(tx["hours"], 0, 12, [4, 0, 0][i], key=f"th{i}_{key}")
            eff = z.selectbox(tx["effort"], list(EFFORT), index=2, key=f"ti{i}_{key}", format_func=lambda e: EFFORT[e][lang])
            if name.strip() and hrs > 0:
                tasks.append(ac.Task(name.strip(), int(hrs), eff))
        kind = st.radio(tx["wording"], ["work", "sport"], horizontal=True, key=f"kind_{key}", format_func=lambda k: tx[k])
    total = sum(t.hours for t in tasks)
    if not tasks:
        st.info(tx["add_task"]); return None
    if total > end_w - start_w:
        st.info(tx["too_long"].format(n=total, w=end_w - start_w)); return None
    if not (start_w <= usual and usual + total <= end_w):
        st.info(tx["bad_usual"]); return None
    return ac.Scenario("custom", "Custom", group, tasks, (int(start_w), int(end_w)), int(usual), ac.WORK if kind == "work" else ac.SPORT)


# ------------------------------------------------------------------ language and header
lang = st.segmented_control("Language", list(LANG_LABELS), default="en", key="lang_ui",
                            format_func=lambda k: LANG_LABELS[k], label_visibility="collapsed") or "en"
tx = T[lang]
st.markdown(f'<div class="hero" style="background-image:linear-gradient(rgba(255,255,255,.80),rgba(255,255,255,.45)),url({image_uri("hero")})">'
            f'<div class="brand">Air<span>Shift</span></div><div class="tagline">{tx["tagline"]}</div></div>',
            unsafe_allow_html=True)

tab_plan, tab_past, tab_india, tab_eval, tab_about = st.tabs([tx["tab_plan"], tx["tab_past"], tx["tab_india"], tx["tab_eval"], tx["tab_about"]])

# ------------------------------------------------------------------ my day (live)
with tab_plan:
    st.markdown(f'<p class="intro">{tx["plan_intro"]}</p>', unsafe_allow_html=True)
    names = list(live.LOCATIONS)
    c1, c2 = st.columns([1.3, 1])
    loc = c1.selectbox(tx["where"], names, index=None, placeholder=tx["pick_city"], key="loc_live",
                       format_func=lambda c: city_name(c, lang))
    when = c2.segmented_control(tx["when"], ["tomorrow", "today"], default="tomorrow", key="when_live",
                                format_func=lambda k: tx[k]) or "tomorrow"
    sc = choose_role(lang, "live")
    if loc is None or sc is None:
        st.info(tx["hint_steps"])
    if loc is not None and sc is not None:
        try:
            s_live, fetched = fetch_live(*[round(x, 4) for x in live.LOCATIONS[loc]])
        except Exception:
            st.error(tx["no_net"])
            s_live = None
        if s_live is not None:
            now = live.now_ist()
            target = (now + pd.Timedelta(days=1)).date() if when == "tomorrow" else now.date()
            sc_use = sc if when == "tomorrow" else live.restrict_to_remaining(sc, now.hour + 1)
            if sc_use is None:
                st.info(tx["no_time"])
            else:
                f24 = live.day_vector(s_live, target)
                wk_mean, wk_q25, wk_q75 = live.recent_week(s_live, target)
                typ = typical_day(loc, target.month)
                try:
                    res = live.live_plan(f24, sc_use, {"last 7 days": wk_mean, "typical day": typ})
                except ValueError:
                    st.error(tx["no_net"]); res = None
                if res is not None:
                    day_word = ac.DAY_WORDS[when][lang]
                    date_str = pd.Timestamp(target).strftime("%d %b")
                    section(tx["result_title"])
                    st.markdown(answer_card(loc, day_word, date_str, sc_use, res["plan"], res["worst"],
                                            res["expected_saving_pct"], res["confidence"], lang), unsafe_allow_html=True)
                    section(tx["hourly"])
                    st.markdown(day_strip(f24, res["plan"]["start"], sc_use.total_hours,
                                          sc_use.fixed_start if res["expected_saving_pct"] is not None else None, lang, sc_use.window,
                                          now_hour=now.hour if when == "today" else None), unsafe_allow_html=True)
                    section(tx["share"])
                    st.caption(tx["share_help"])
                    st.code(ac.advisory_card(loc, pd.Timestamp(target).strftime("%d %b %Y"), sc_use, res["plan"]["start"], res["worst"],
                                             res["expected_saving_pct"] or 0, res["confidence"], lang, day=when,
                                             show_saving=res["expected_saving_pct"] is not None), language=None, wrap_lines=True)
                    with st.expander(tx["details"]):
                        hh = list(range(6, 22))
                        fig, ax = plt.subplots(figsize=(8.5, 3.2))
                        ax.fill_between(hh, wk_q25[6:22], wk_q75[6:22], color="#BFD7E6", alpha=.7, label="last 7 days (middle 50%)")
                        ax.plot(hh, f24[6:22], color="#2A6F97", marker="o", ms=4, label="forecast")
                        if typ is not None:
                            ax.plot(hh, typ[6:22], color="#6B7B85", ls=":", label="typical day, CPCB 2020 to 2024")
                        ax.set_xlabel("hour (IST)"); ax.set_ylabel("PM2.5 (µg/m³)"); ax.legend(fontsize=8)
                        for sp in ("top", "right"):
                            ax.spines[sp].set_visible(False)
                        st.pyplot(fig)
                        st.caption(f"{tx['source']} {tx['updated_on'].format(t=fetched)} {tx['dose_note'].format(d=res['dose'])}")

# ------------------------------------------------------------------ a past day
with tab_past:
    st.markdown(f'<p class="intro">{tx["past_intro"]}</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.3, 1])
    city = c1.selectbox(tx["city"], CITIES, index=CITIES.index("Chennai"), key="city_past",
                        format_func=lambda c: city_label(c, lang))
    dates = sorted(FC.loc[FC["City"] == city, "date"].unique())
    ex_d = example_dates().get(city)
    date = c2.selectbox(tx["day"], dates, index=dates.index(ex_d) if ex_d in dates else len(dates) // 2, key="date_past",
                        format_func=lambda d: pd.Timestamp(d).strftime("%a %d %b %Y"))
    sc = choose_role(lang, "past", "construction")
    if sc is not None:
        d = FC[(FC["City"] == city) & (FC["date"] == date)].set_index("hour").reindex(range(24))
        v = {k: d[k].to_numpy(dtype=float) for k in ["y", "pred", "lo", "hi", "clim"]}
        plans, W = ac.enumerate_plans(sc)
        pick = {k: int(np.argmin(ac.plan_doses(np.nan_to_num(v[k])[None, :], W)[0])) for k in ["pred", "lo", "hi"]}
        conf = ac.confidence_label(plans[pick["lo"]]["start"], plans[pick["pred"]]["start"], plans[pick["hi"]]["start"])
        chosen, fi = pick["pred"], ac.fixed_plan_index(sc, plans)
        fd = ac.plan_doses(np.nan_to_num(v["pred"])[None, :], W)[0]
        plan = plans[chosen]
        st.markdown(answer_card(city, ac.DAY_WORDS["tomorrow"][lang], pd.Timestamp(date).strftime("%d %b %Y"), sc, plan,
                                ac.worst_block(v["pred"], sc), (1 - fd[chosen] / fd[fi]) * 100, conf, lang), unsafe_allow_html=True)
        reveal = st.toggle(tx["reveal"], key="reveal_past")
        section(tx["hourly"])
        st.markdown(day_strip(v["pred"], plan["start"], sc.total_hours, sc.fixed_start, lang, sc.window,
                              actual=v["y"] if reveal else None), unsafe_allow_html=True)
        if reveal:
            st.markdown(f'<p class="note">{tx["reveal_note"]}</p>', unsafe_allow_html=True)
            hrs = np.where(W.sum(axis=0) > 0)[0]
            if np.isnan(v["y"][hrs]).any():
                st.info(tx["no_meas"])
            else:
                td = ac.plan_doses(v["y"][None, :], W)[0]
                diff = (1 - td[chosen] / td[fi]) * 100
                m = st.columns(3)
                m[0].metric(tx["m_with"], f"{td[chosen]:,.0f} µg", f"{-diff:+.0f}% {tx['vs_usual']}", delta_color="inverse")
                m[1].metric(tx["m_usual"], f"{td[fi]:,.0f} µg")
                m[2].metric(tx["m_best"], f"{td.min():,.0f} µg")
        if city not in CORE:
            st.caption(tx["new_note"])

# ------------------------------------------------------------------ city patterns
with tab_india:
    st.markdown(f'<p class="intro">{tx["india_intro"]}</p>', unsafe_allow_html=True)
    city = st.selectbox(tx["city"], CITIES, index=CITIES.index("Delhi"), key="city_pat",
                        format_func=lambda c: city_label(c, lang))
    fig, ax = plt.subplots(figsize=(9, 3.6))
    for s_, colr in SEASON_COLORS.items():
        p = PROF[(PROF["City"] == city) & (PROF["season"] == s_)]
        ax.plot(p["hour"], p["median"], color=colr, lw=2, label=s_)
        ax.fill_between(p["hour"], p["q25"], p["q75"], color=colr, alpha=.10)
    ax.axvspan(6, 21, color="#E3E9EC", alpha=.6, zorder=0)
    ax.set_xlabel("hour of day"); ax.set_ylabel("PM2.5 (µg/m³)"); ax.legend(fontsize=8, frameon=False)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    st.pyplot(fig)
    if city in S["median_within_day_ratio"]:
        st.markdown(tx["ratio"].format(city=city_name(city, lang), r=f"**{S['median_within_day_ratio'][city]:.1f}**"))
    st.caption(tx["cleanest_cap"])
    figure("04_cleanest_hour_map")
    with st.expander(tx["rhythm"]):
        figure("03_daily_rhythm")
    with st.expander(tx["eigen"]):
        figure("10_eigendays")

# ------------------------------------------------------------------ how accurate
with tab_eval:
    st.markdown(f'<p class="intro">{tx["eval_intro"].format(n=len(CORE), m=len(NEW))}</p>', unsafe_allow_html=True)
    t = S["test_2024"]
    m = st.columns(3)
    m[0].metric(tx["m_mae"], f"{t['MAE']:.1f} µg/m³", tx["m_mae_help"].format(x=f"{t['skill_vs_best_baseline_%']:.0f}"), delta_color="off")
    m[1].metric(tx["m_cover"], f"{S['conformal_coverage_2024']:.1%}", tx["m_cover_help"], delta_color="off")
    m[2].metric(tx["m_new"], f"{S['conformal_coverage_newcities']:.1%}", tx["m_new_help"], delta_color="off")
    rows = []
    for k, v_ in S["backtest_2024"].items():
        who = ROLES[ROLE_BY_LABEL[k]][lang] if k in ROLE_BY_LABEL else k
        rows.append({tx["col_who"]: who, tx["col_saving"]: v_["saving_vs_usual_pct"], tx["col_best"]: v_["oracle_saving_vs_usual_pct"],
                     tx["col_airshift"]: v_["captured_pct"], tx["col_typical"]: v_["captured_pct_climatology"]})
    section(tx["avoid_q"])
    st.dataframe(pd.DataFrame(rows).set_index(tx["col_who"]))
    st.caption(tx["captured_help"])
    figure("12_backtest_results")
    with st.expander(tx["new_expander"].format(n=len(NEW))):
        st.dataframe(table("32_newcity_by_city", index_col=0))
    with st.expander(tx["conf_expander"]):
        st.dataframe(table("28_confidence_vs_regret", index_col=0))

# ------------------------------------------------------------------ about
with tab_about:
    st.markdown(tx["about_body"].format(model=S["selected_model"], n=len(CITIES)))
    credits = ASSETS / "CREDITS.md"
    if credits.exists():
        with st.expander("Photo credits"):
            st.markdown(credits.read_text(encoding="utf-8"))
