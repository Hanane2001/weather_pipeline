import pandas as pd
# import numpy as np
import requests as rq

def get_cities():
    url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"
    out = "data/bronze/cities_raw.csv"

    try:
        res = rq.get(url, timeout=30)
        if res.status_code != 200:
            raise Exception("request problem")
        with open(out, "wb") as f:
            f.write(res.content)
    except Exception as e:
        print(f"erreur: {e}")
    except rq.Timeout:
        print("request time out")
    except rq.ConnectionError:
        print("connection timed out")
    except rq.ReadTimeout:
        print("server took too long to respond")


get_cities()