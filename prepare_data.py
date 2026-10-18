"""Build the all-India city-hour dataset used by AirShift (2020 to 2024).

Source: Kaggle dataset "India Air Quality Index (AQI) Dataset 2010-2024" (omsandeeppatil/indian-aqi-stations),
CPCB continuous monitoring stations, mostly 15-minute readings.

Steps
1. Read station metadata (stations.csv) and the dataset's file list.
2. Assign every station to the nearest target city (src/cities.py) if it lies within RADIUS_KM.
3. For each city take up to MAX_CANDIDATES stations (largest files first), download them one by one,
   convert to hourly means for 2020 to 2024 and compute coverage.
4. Keep stations with at least MIN_STATION_COVERAGE of hours with PM2.5; the city value for each hour is the
   mean of the kept stations that reported in that hour.
5. Write data/india_city_hour_2020_2024.csv.gz, data/city_meta.csv and data/station_selection.csv.

Run from the project folder:  python prepare_data.py   (needs internet; downloads about 1 to 2 GB, deletes raw files as it goes)
"""
import json
import math
import subprocess
import sys
import urllib.parse
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from cities import CITIES  # noqa: E402

REF = "omsandeeppatil/indian-aqi-stations"
API = "https://www.kaggle.com/api/v1/datasets"
RADIUS_KM, MAX_CANDIDATES, MIN_STATION_COVERAGE = 15, 3, 0.5
START, END = "2020-01-01 00:00", "2024-12-31 23:00"
DATA = Path("data"); RAW = DATA / "raw"; CACHE = DATA / "cache"
RAW.mkdir(parents=True, exist_ok=True); CACHE.mkdir(parents=True, exist_ok=True)
VARS = {"pm2.5": "PM2.5", "pm10": "PM10", "no2": "NO2", "co": "CO", "rh": "RH", "ws": "WS"}


def curl(url, out=None):
    cmd = ["curl", "-sSL", "-m", "600", url] + (["-o", str(out)] if out else [])
    r = subprocess.run(cmd, capture_output=True, text=out is None)
    if r.returncode != 0:
        raise RuntimeError(f"download failed: {url}")
    return r.stdout


def list_files():
    files, tok = [], None
    while True:
        url = f"{API}/list/{REF}?pageSize=200" + (f"&pageToken={urllib.parse.quote(tok)}" if tok else "")
        d = json.loads(curl(url))
        files += [(f["name"], f.get("totalBytes") or 0) for f in d.get("datasetFiles", [])]
        tok = d.get("nextPageToken")
        if not tok:
            return pd.DataFrame(files, columns=["path", "bytes"])


def haversine(a1, o1, a2, o2):
    a1, o1, a2, o2 = map(np.radians, (a1, o1, a2, o2))
    h = np.sin((a2 - a1) / 2) ** 2 + np.cos(a1) * np.cos(a2) * np.sin((o2 - o1) / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(h))


def station_hourly(path):
    d = pd.read_csv(path, usecols=lambda c: c in list(VARS) + ["timestamp"])
    d["timestamp"] = pd.to_datetime(d["timestamp"], errors="coerce")
    d = d.dropna(subset=["timestamp"]).drop_duplicates("timestamp").set_index("timestamp").sort_index()
    d = d.loc[START:"2024-12-31 23:59"].rename(columns=VARS)
    for c in VARS.values():
        if c not in d:
            d[c] = np.nan
    d = d[list(VARS.values())].apply(pd.to_numeric, errors="coerce")
    ceiling = int(((d["PM2.5"] >= 999) | (d["PM2.5"] < 0)).sum())
    for c in ["PM2.5", "PM10", "NO2"]:
        d.loc[(d[c] >= 999) | (d[c] < 0), c] = np.nan
    d.loc[(d["CO"] > 50) | (d["CO"] < 0), "CO"] = np.nan
    d.loc[(d["RH"] > 100) | (d["RH"] < 0), "RH"] = np.nan
    d.loc[(d["WS"] > 60) | (d["WS"] < 0), "WS"] = np.nan
    step = d.index.to_series().diff().median()
    per_hour = max(1, int(round(pd.Timedelta("1h") / step))) if pd.notna(step) and step > pd.Timedelta(0) else 1
    need = max(1, math.ceil(per_hour / 2))
    h = d.resample("h").mean()
    cnt = d.resample("h").count()
    h = h.where(cnt >= need)
    h = h.reindex(pd.date_range(START, END, freq="h"))
    s = h["PM2.5"]
    run = s.groupby((s != s.shift()).cumsum()).transform("size")
    stuck = s.notna() & (run >= 6)
    h.loc[stuck, "PM2.5"] = np.nan          # stuck sensor
    h.attrs["ceiling_readings"], h.attrs["stuck_hours"] = ceiling, int(stuck.sum())
    return h


def main():
    st = pd.read_csv(RAW / "stations.csv") if (RAW / "stations.csv").exists() else None
    if st is None:
        curl(f"{API}/download/{REF}/stations.csv", RAW / "stations.csv")
        st = pd.read_csv(RAW / "stations.csv")
    files = list_files()
    files = files[files["path"].str.contains("/")].copy()
    files["station_code"] = files["path"].str.split("/").str[1].str.replace(".csv", "", regex=False)
    st = st.merge(files, on="station_code", how="inner")
    names = list(CITIES)
    D = haversine(st["latitude"].to_numpy()[:, None], st["longitude"].to_numpy()[:, None],
                  np.array([CITIES[c][2] for c in names])[None, :], np.array([CITIES[c][3] for c in names])[None, :])
    st["city_target"] = np.array(names)[D.argmin(1)]
    st["dist_km"] = D.min(1)
    cand = (st[st["dist_km"] <= RADIUS_KM].sort_values("bytes", ascending=False)
              .groupby("city_target").head(MAX_CANDIDATES).sort_values(["city_target", "bytes"], ascending=[True, False]))
    print(f"{len(cand)} candidate stations for {cand['city_target'].nunique()} cities, {cand['bytes'].sum() / 1e6:,.0f} MB")

    rows, city_frames, tiers = [], [], {}
    for city, g in cand.groupby("city_target", sort=False):
        hs = {}
        for _, r in g.iterrows():
            tmp = RAW / f"{r['station_code']}.csv"
            cache = CACHE / f"{r['station_code']}.pkl"
            try:
                if cache.exists():
                    h = pd.read_pickle(cache)
                else:
                    curl(f"{API}/download/{REF}/{urllib.parse.quote(r['path'], safe='')}", tmp)
                    h = station_hourly(tmp)
                    h.to_pickle(cache)
            except Exception as exc:  # keep going; record the failure
                rows.append({"City": city, "station_code": r["station_code"], "error": str(exc)[:120]})
                continue
            finally:
                tmp.unlink(missing_ok=True)
            cov = h["PM2.5"].notna().groupby(h.index.year).mean()
            hs[r["station_code"]] = h
            rows.append({"City": city, "station_code": r["station_code"], "station_city_label": r["city"],
                         "dist_km": round(r["dist_km"], 1), "file_mb": round(r["bytes"] / 1e6, 1),
                         "ceiling_readings": h.attrs.get("ceiling_readings"), "stuck_hours": h.attrs.get("stuck_hours"),
                         "overall_cov": round(float(h["PM2.5"].notna().mean()), 3),
                         **{f"pm25_cov_{y}": round(float(cov.get(y, 0)), 3) for y in range(2020, 2025)}})
        # Long-record stations build a consistent 2020 to 2024 series; otherwise recent stations (2024) are used
        long_ = [c for c, h in hs.items() if h["PM2.5"].notna().mean() >= MIN_STATION_COVERAGE]
        recent = [c for c, h in hs.items() if h.loc["2024", "PM2.5"].notna().mean() >= MIN_STATION_COVERAGE]
        use, tier = (long_, "long record") if long_ else (recent, "recent only") if recent else ([], "none")
        tiers[city] = (tier, use)
        for rr in rows:
            if rr.get("City") == city and "station_code" in rr:
                rr["used"] = rr["station_code"] in use
        if use:
            stack = pd.concat([hs[c] for c in use], keys=range(len(use)))
            mean = stack.groupby(level=1).mean()
            mean["n_stations"] = stack["PM2.5"].notna().groupby(level=1).sum()
            mean.index.name = "Datetime"
            city_frames.append(mean.reset_index().assign(City=city))
        print(f"  {city:20s} {tier:12s} stations used: {', '.join(use) if use else '-'}", flush=True)
    sel = pd.DataFrame(rows)
    sel.to_csv(DATA / "station_selection.csv", index=False)
    out = pd.concat(city_frames, ignore_index=True)[["City", "Datetime"] + list(VARS.values()) + ["n_stations"]]
    num = list(VARS.values())
    out[num] = out[num].round(3)
    out.to_csv(DATA / "india_city_hour_2020_2024.csv.gz", index=False, compression="gzip")
    meta = pd.DataFrame([{"City": c, "State": CITIES[c][0], "Region": CITIES[c][1], "lat": CITIES[c][2], "lon": CITIES[c][3],
                          "tier": tiers.get(c, ("not in station list", []))[0], "stations_used": ", ".join(tiers.get(c, ("", []))[1])}
                         for c in names])
    meta.to_csv(DATA / "city_meta.csv", index=False)
    print("Done:", out.shape, "cities with data:", out["City"].nunique())


if __name__ == "__main__":
    main()
