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
    source = "data/gold/weather_features.csv"
    df = pd.read_csv(source)
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
    connect.commit()
    cursor.close()
    connect.close()
    print("Tables created successfully!")
    

load_data()