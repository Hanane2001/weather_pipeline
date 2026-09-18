import pandas as pd
import os

def risk_temp(t):
    if t > 40: return 3
    if t > 35: return 2
    if t > 30: return 1
    return 0

def risk_prec(p):
    if p > 20: return 3
    if p > 5:  return 2
    if p > 0:  return 1
    return 0
    
def risk_wind(w):
    if w > 70: return 3
    if w > 50: return 2
    if w > 30: return 1
    return 0

def features():
    source = "data/silver/weather_clean.csv"
    out = "data/gold/weather_features.csv"
    os.makedirs("data/gold", exist_ok=True)
    df = pd.read_csv(source)

    df["temp_category"] = pd.cut(df["temperature_2m_max"], bins=[-100, 15, 25, 35, 100], labels=["Cold", "Normal", "Hot", "Very hot"])
    df["prec_category"] = pd.cut(df["precipitation_sum"], bins=[-0.1, 0, 5, 20, 1000], labels=["None", "Low", "Medium", "High"])
    df["wind_category"] = pd.cut(df["wind_gusts_10m_max"], bins=[-1, 30, 50, 70, 1000], labels=["Weak", "Moderate", "Strong", "Very strong"])

    df["risk_temp"] = df["temperature_2m_max"].apply(risk_temp)
    df["risk_prec"] = df["precipitation_sum"].apply(risk_prec)
    df["risk_wind"] = df["wind_gusts_10m_max"].apply(risk_wind)

    df["risk_score"] = ((df["risk_temp"] + df["risk_prec"] + df["risk_wind"]) / 9 * 100).round(0).astype(int)
    df["risk_level"] = pd.cut(df["risk_score"], bins=[-1, 33, 66, 100], labels=["Low", "Medium", "High"])
    df.to_csv(out, index=False)
    print(f"Gold created: {out}")

if __name__ == "__main__":
    features()