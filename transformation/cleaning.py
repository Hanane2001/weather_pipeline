import pandas as pd
import json
import os

def clean():
    source = "data/bronze/weather_api.json"
    out = "data/silver/weather_clean.csv"
    os.makedirs("data/silver", exist_ok=True)
    with open(source, "r", encoding="utf-8") as f:
        raw = json.load(f)
    all_dfs = []
    for item in raw:
        daily = pd.DataFrame(item["daily"])
        daily["latitude"] = item["latitude"]
        daily["longitude"] = item["longitude"]
        daily["city"] = item["city"]
        all_dfs.append(daily)

    df = pd.concat(all_dfs, ignore_index=True)
    float_cols = [
        "latitude", "longitude",
        "wind_gusts_10m_max", "wind_speed_10m_max",
        "precipitation_sum",
        "temperature_2m_min", "temperature_2m_max"
    ]
    for c in float_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["time"] = pd.to_datetime(df["time"]).dt.date
    df = df.drop_duplicates(subset=["city", "time"])
    df = df.dropna()
    df = df[df["temperature_2m_min"] <= df["temperature_2m_max"]]
    df.to_csv(out, index=False)
    print(f"Silver created: {out} ({len(df)} lines)")

if __name__ == "__main__":
    clean()