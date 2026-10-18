# AI-Powered Air Quality Intelligence
## AirShift India: a dose-aware planner of low-exposure time windows for outdoor workers and students

Foundations of Data Science final project, MSc Artificial Intelligence and Machine Learning, VIT Vellore.

Air-quality apps say *how bad* the air is. Outdoor workers and students often cannot avoid going outside, but they can shift *when*. AirShift forecasts tomorrow's hourly PM2.5 (issued at 21:00 the evening before), attaches a calibrated 90% range, converts it into the PM2.5 dose a person would inhale during their activity, and recommends the lowest-dose time window and task order. It is judged by how much exposure it would have avoided, not only by forecast accuracy.

## Data: CPCB stations, 2020 to 2024, 43 cities across India

* Source: Kaggle "India Air Quality Index (AQI) Dataset 2010-2024" (omsandeeppatil/indian-aqi-stations), CPCB continuous monitoring stations, mostly 15-minute readings.
* `prepare_data.py` matches stations to 46 target cities by coordinates (within 15 km), downloads up to three stations per city, converts readings to hourly means, cleans instrument ceilings and stuck sensors, and averages stations into one city series. Output: `data/india_city_hour_2020_2024.csv.gz` (PM2.5, PM10, NO2, CO, relative humidity, wind speed).
* **29 core cities** (data in at least 60% of hours every year 2020 to 2024): used for analysis, training (2020 to 2022), calibration (2023) and testing (2024).
* **14 new cities** (stations started later, including Vellore, Coimbatore and five north-eastern capitals): used only to test AirShift in cities it has never seen.
* Data ends on 31 December 2024; 2025 is not available in this source.

## Folder contents

```
airshift_india/
  AirShift_India.ipynb       Main notebook, already executed (10 phases, all outputs visible)
  AirShift_India.html        Same notebook as a web page
  prepare_data.py            Rebuilds the city-hour dataset from the Kaggle station files (needs internet, about 2 GB download)
  src/airshift_core.py       Dose model, scenarios, plan optimizer, advisory text (English, Marathi, Hindi)
  src/live.py                Live mode: current hourly PM2.5 for any place, plans today or tomorrow
  src/cities.py              Target cities with state, region and coordinates
  app/streamlit_app.py       Dashboard: plan my day (live), check a day in 2024, India patterns, how well it works, about
  src/ui_text.py             Dashboard text in English, Marathi and Hindi
  data/                      City-hour data (2020 to 2024), city list, station selection table
  outputs/figures/           Figures for the report and slides
  outputs/tables/            Result tables (CSV)
  outputs/app/               Forecasts, profiles and summary used by the dashboard
```

## How to run

1. `pip install -r requirements.txt` (Python 3.10 or newer; a virtual environment is recommended)
2. `streamlit run app/streamlit_app.py` from this folder. Results are already included, so the dashboard works straight away.
3. Optional: `jupyter notebook AirShift_India.ipynb`, then *Kernel > Restart Kernel and Run All Cells* to rebuild every result (about 10 to 15 minutes).
4. Optional: `python prepare_data.py` to rebuild the dataset from the original station files.

## Dashboard

* Switch the whole planner between English, मराठी and हिन्दी with one tap.
* Three choices only: where, when (tomorrow or the rest of today) and who (construction worker, delivery rider, street vendor, student sports, or your own plan).
* The answer is one large card: best time, task order, the time to avoid, the expected saving and a confidence level.
* An hour-by-hour bar strip shows how polluted each hour will be (height = PM2.5, colour = official category), with your plan and usual time marked.
* A ready-made message to copy into WhatsApp or SMS.
* Works on a phone screen. Everything except "Plan my day" works without internet.

## Key results (reference run, seed 42, scikit-learn 1.8.0)

| Item | Result |
|---|---|
| Why timing matters | Within 06:00 to 21:00 the dirtiest hour is typically 1.9 to 4.6 times the cleanest, depending on the city |
| Forecast (2024) | HistGradientBoosting MAE 13.7 ug/m3 vs 16.7 for "same hour yesterday" (18% better; better in all 29 core cities) |
| Uncertainty | Conformal 90% intervals cover 90.2% (core cities) and 88.6% (new cities) |
| Decisions (2024) | AirShift captures 53% to 59% of the achievable improvement vs 44% to 50% for a typical-day plan |
| Construction worker | 15.8% less PM2.5 inhaled than a 09:00 start (perfect knowledge: 24.4%) |
| New cities | 52% to 58% captured vs 40% to 46% for the region's typical day |
| Honest limitations | Weaker in the South and West; in Chennai, Coimbatore and Vellore the typical-day plan did as well or better |

## What this project claims, and what it does not

Claims: a reproducible, backtested planner with calibrated uncertainty and decision-focused evaluation, tested across India including cities it never saw.

Does not claim: medical advice, health-risk prediction, real-time deployment of the trained model, indoor exposure, or that it is the first such system.

## Sources to cite

* Data: Kaggle "India Air Quality Index (AQI) Dataset 2010-2024" (omsandeeppatil / Project Parisar), compiled from CPCB monitoring stations.
* Breathing rates: U.S. EPA (2011), Exposure Factors Handbook, Chapter 6, Table 6-2.
* PM2.5 categories: CPCB National Air Quality Index breakpoints. Seasons: India Meteorological Department.
* Live mode: air-quality data by Open-Meteo.com, based on the Copernicus Atmosphere Monitoring Service (CAMS).
* Conformalized quantile regression: confirm the original paper on Google Scholar before citing.
