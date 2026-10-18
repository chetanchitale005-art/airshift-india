"""AirShift live mode: plan today or tomorrow with current air-quality data.

Data source: Open-Meteo Air Quality API (no API key needed), which serves hourly PM2.5 from the
Copernicus Atmosphere Monitoring Service (CAMS) global model. These are modelled values on a
grid of roughly 40 km, not CPCB station measurements, so absolute levels can differ from local
monitors. Attribution: air-quality data by Open-Meteo.com, based on CAMS.

Why not the trained Random Forest? It needs the last seven days of hourly CPCB station
measurements as input, which are not available without registering for an API key. Live mode
therefore uses the CAMS forecast as its forecast and applies AirShift's dose model, optimizer,
confidence label and advisory cards unchanged.
"""
import dataclasses
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

import airshift_core as ac

API = "https://air-quality-api.open-meteo.com/v1/air-quality"
IST = timezone(timedelta(hours=5, minutes=30))

from cities import CITIES  # noqa: E402

LOCATIONS = {c: (v[2], v[3]) for c, v in sorted(CITIES.items())}  # approximate city-centre coordinates


def now_ist():
    return datetime.now(IST)


def fetch_pm25(lat, lon, past_days=7, forecast_days=2, timeout=20):
    """Hourly PM2.5 (ug/m3) in Indian Standard Time, from past_days ago to the end of the forecast."""
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "hourly": "pm2_5", "past_days": past_days,
                                "forecast_days": forecast_days, "timezone": "Asia/Kolkata"})
    with urllib.request.urlopen(f"{API}?{q}", timeout=timeout) as r:
        d = json.load(r)
    s = pd.Series(d["hourly"]["pm2_5"], index=pd.to_datetime(d["hourly"]["time"]), dtype=float, name="pm25")
    return s.interpolate(limit=2, limit_area="inside")


def day_vector(s, day):
    v = s[s.index.normalize() == pd.Timestamp(day)]
    out = np.full(24, np.nan)
    out[v.index.hour] = v.to_numpy()
    return out


def recent_week(s, before_day, days=7):
    """Mean and 25th to 75th percentile band of each clock hour over the days before `before_day`."""
    start = pd.Timestamp(before_day) - pd.Timedelta(days=days)
    past = s[(s.index >= start) & (s.index < pd.Timestamp(before_day))]
    g = past.groupby(past.index.hour)
    mean, q25, q75 = (np.full(24, np.nan) for _ in range(3))
    mean[g.mean().index] = g.mean().to_numpy()
    q25[g.quantile(0.25).index] = g.quantile(0.25).to_numpy()
    q75[g.quantile(0.75).index] = g.quantile(0.75).to_numpy()
    return mean, q25, q75


def restrict_to_remaining(scenario, earliest_hour):
    """For planning the rest of today: start no earlier than the next full hour."""
    first, end = scenario.window
    new_first = max(first, earliest_hour)
    if new_first + scenario.total_hours > end:
        return None
    return dataclasses.replace(scenario, window=(new_first, end))


def live_plan(forecast24, scenario, references):
    """Plan with the forecast; confidence = agreement of plan start times across forecast and reference profiles.

    references: dict name -> 24-hour profile (for example the last week's mean, or the CPCB typical day).
    """
    plans, W = ac.enumerate_plans(scenario)
    hrs = np.where(W.sum(axis=0) > 0)[0]
    if np.isnan(forecast24[hrs]).any():
        raise ValueError("The forecast has missing hours inside the planning window.")
    fd = ac.plan_doses(forecast24[None, :], W)[0]
    best = int(np.argmin(fd))
    starts = [plans[best]["start"]]
    for prof in references.values():
        if prof is not None and not np.isnan(prof[hrs]).any():
            starts.append(plans[int(np.argmin(ac.plan_doses(prof[None, :], W)[0]))]["start"])
    spread = max(starts) - min(starts)
    conf = "high" if spread <= 1 else ("medium" if spread <= 3 else "low")
    try:
        fi = ac.fixed_plan_index(scenario, plans)
        saving = (1 - fd[best] / fd[fi]) * 100
    except ValueError:
        fi, saving = None, None
    return {"plan": plans[best], "dose": float(fd[best]), "fixed_index": fi, "expected_saving_pct": saving,
            "confidence": conf, "worst": ac.worst_block(forecast24, scenario), "n_references": len(starts) - 1}
