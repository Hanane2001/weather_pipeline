import pandas as pd
import os
import requests as rq

def get_cities():
    url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"
    out = "data/bronze/cities_raw.csv"
    os.makedirs("data/bronze", exist_ok=True)

    try:
        res = rq.get(url, timeout=30)
        res.raise_for_status()
        with open(out, "wb") as f:
            f.write(res.content)
        print(f"ok : {out}")
    except rq.Timeout:
        print("Erreur : timeout")
    except rq.HTTPError as e:
        print(f"Erreur HTTP : {e}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_cities()