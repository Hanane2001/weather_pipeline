import pandas as pd
import requests as rq
import json
import os

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    out = "data/bronze/weather_api.json"
    source = "data/bronze/cities_raw.csv"
    os.makedirs("data/bronze", exist_ok=True)

    df = pd.read_csv(source)
    results = []

    for _, row in df.iterrows():
        try:
            params = {
                "latitude": row["lat"],
                "longitude": row["lng"],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max",
                    "wind_speed_10m_max",
                    "wind_gusts_10m_max",
                    "weather_code"
                ],
                "timezone": "auto",
                "forecast_days": 7
            }

            res = rq.get(url, params=params, timeout=30)
            res.raise_for_status()
            data = res.json()
            data["city"] = row["city"]
            results.append(data)
            # print(f"OK : {row['city']}")
        except rq.Timeout:
            print(f"Timeout : {row['city']}")
        except rq.HTTPError as e:
            print(f"HTTP erreur {row['city']} : {e}")
        except Exception as e:
            print(f"Erreur {row['city']} : {e}")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)
    print(f"OK : {out}")

if __name__ == "__main__":
    get_weather()