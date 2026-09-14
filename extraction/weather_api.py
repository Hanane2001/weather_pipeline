import pandas as pd
import requests as rq
import json

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=33.5883&longitude=-7.6114&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_gusts_10m_max,precipitation_probability_max,precipitation_sum,weather_code&timezone=auto&forecast_days=1"
    out = "data/bronze/weather_api.json"
    source = "data/bronze/cities_raw.csv"
    df = pd.read_csv(source)
    try:
        for i in range(len(df)):
            city = df["city"].iloc[i]
            lat = df["lat"].iloc[i]
            lng = df["lng"].iloc[i]

            params = {
                "latitude": lat,
                "longitude": lng,
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
                "forecast_days": 1
            }

            res = rq.get(url, params=params, timeout=30)
            if res.status_code != 200:
                raise Exception("request problem")
            data = res.json()
            print(data)
    except Exception as e:
        print(f"erreur: {e}")
    except rq.Timeout:
        print("request time out")
    except rq.ConnectionError:
        print("connection timed out")
    except rq.ReadTimeout:
        print("server took too long to respond")


get_weather()