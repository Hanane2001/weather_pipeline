import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def load_data():
    cities_df = pd.read_csv("data/bronze/cities_raw.csv")
    weather_df = pd.read_csv("data/silver/weather_clean.csv")
    features_df = pd.read_csv("data/gold/weather_features.csv")
    connect = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("connection with postgres is succesful") 
    cursor = connect.cursor()
    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        sc = f.read()
    cursor.execute(sc)
    
    print("Tables created successfully!")
    data_cities = cities_df[[
        "city",
        "lat",
        "lng",
        "country",
        "iso2",
        "admin_name",
        "capital",
        "population",
        "population_proper"
    ]].values.tolist()

    cursor.executemany("""
        INSERT INTO cities(city, lat, lng, country, iso2, admin_name, capital, population, population_proper) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data_cities)

    cursor.execute("""
        select city_id, city from cities
    """)

    city_ids = {}
    for city_id, city in cursor.fetchall():
        city_ids[city] = city_id

    data_weather = []
    for _, row in weather_df.iterrows():
        city_id = city_ids[row["city"]]
        data_weather.append([
            city_id,
            row["weather_code"],
            row["wind_gusts_10m_max"],
            row["wind_speed_10m_max"],
            row["precipitation_probability_max"],
            row["precipitation_sum"],
            row["temperature_2m_min"],
            row["temperature_2m_max"],
            row["time"]
        ])

    cursor.executemany("""
        INSERT INTO weather(city_id, weather_code, wind_gusts_10m_max, wind_speed_10m_max, precipitation_probability_max, precipitation_sum, temperature_2m_min, temperature_2m_max, time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data_weather)

    cursor.execute("""
        select weather_id from weather order by weather_id
    """)

    weather_ids = []
    for row in cursor.fetchall():
        weather_ids.append(row[0])

    data_features = []
    for i, (_, row) in enumerate(features_df.iterrows()):
        weather_id = weather_ids[i]
        data_features.append([
            weather_id,
            row["temp_category"],
            row["prec_category"],
            row["wind_category"],
            row["risk_temp"],
            row["risk_prec"],
            row["risk_wind"],
            row["risk_score"],
            row["risk_level"]
        ])


    cursor.executemany("""
        INSERT INTO weather_features(weather_id, temp_category, prec_category, wind_category, risk_temp, risk_prec, risk_wind, risk_score, risk_level) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data_features)

    connect.commit()
    cursor.close()
    connect.close()
    print("Data loaded successfully!")

    

load_data()