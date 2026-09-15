import pandas as pd
import numpy as np

def category_risk(df):
    df["temp_category"] = pd.cut(df["temperature_2m_max"], bins=[-float("inf"), 15, 25, 35, float("inf")], labels=["Cold", "Normal", "Hot", "Very hot"])
    df["prec_category"] = pd.cut(df["precipitation_sum"], bins=[-0.1, 0, 5, 20, float("inf")], labels=["None", "Low", "Medium", "High"])
    df["wind_category"] = pd.cut(df["wind_gusts_10m_max"], bins=[-float("inf"), 30, 50, 70, float("inf")], labels=["Weak", "Moderate", "Strong", "Very strong"])
    
    df["risk_temp"] = (df["temperature_2m_max"] > 35).astype(int)
    df["risk_prec"] = pd.cut(df["precipitation_sum"], bins=[-float("inf"), 5, 20, float("inf")], labels=[0, 1, 2]).astype(int)
    df["risk_wind"] = pd.cut(df["wind_gusts_10m_max"], bins=[-float("inf"), 50, 70, float("inf")], labels=[0, 1, 2]).astype(int)
    df["risk_score"] = df["risk_temp"] + df["risk_prec"] + df["risk_wind"]

    df["risk_level"] = pd.cut(df["risk_score"], bins=[-1, 1, 3, 5], labels=["Low", "Medium", "High"])
    return df

def feature():
    source = "data/silver/weather_clean.csv"
    destination = "data/gold/weather_features.csv"
    df = pd.read_csv(source)
    df = df.rename(columns={"time": "date"})
    res = category_risk(df)
    res.to_csv(destination, index=False)

feature()
    
