import pandas as pd
import numpy as np
import itertools

def clean():
    source = "data/bronze/data.json"
    res = pd.read_json(source)
    df =pd.DataFrame(res)
    all = []
    for i in df.itertuples():
        dfs = pd.DataFrame(i.daily)
        dfs["latitude"] = i.latitude
        dfs["longitude"] = i.longitude
        dfs["city"] = i.city
        all.append(dfs)
    print(dfs)
    res = pd.concat(all, ignore_index=True)
    inv = res[res.columns[::-1]]
    colonnes_float = [
        "longitude",
        "latitude",
        "wind_gusts_10m_max",
        "wind_speed_10m_max",
        "precipitation_sum",
        "temperature_2m_min",
        "temperature_2m_max",
    ]
    for col in colonnes_float:
        if inv[col].dtype != "float64":
            inv[col] = pd.to_numeric(inv[col], errors="coerce").astype(float)
    inv["time"] = pd.to_datetime(inv["time"])
    nombre_duplicate = inv.duplicated().sum()
    if nombre_duplicate != 0:
        inv = inv.drop_duplicates()
    nombre_na = inv.isna().sum().sum()
    if nombre_na != 0:
        inv = inv.fillna(0)
    # print(inv.info())
    # print(inv.isna().sum())
    # print(inv.duplicated().sum())
    # print(inv.shape)
    destination = "data/silver/weather_clean.csv"
    inv.to_csv(destination, index=False)
    print(f"silver cree: {destination}")


clean()