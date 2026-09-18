import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load.postgres import get_connection


@st.cache_data(ttl=300, show_spinner=False) # Cache le résultat pendant 5 minutes et n'affiche pas automatiquement le spinner pendant le chargement
def fetch_weather_data(query: str) -> pd.DataFrame:
    connect = get_connection()
    return pd.read_sql(query, connect)

def get_cities():
    try:
        cities_df = fetch_weather_data("""select distinct city from cities order by city""")
        AVAILABLE_CITIES = cities_df["city"].tolist()
    except:
        AVAILABLE_CITIES = [
            "Casablanca",
            "Rabat",
            "Marrakech",
            "Fès",
            "Tanger",
            "Agadir",
            "Oujda",
            "Kénitra",
            "Tétouan",
            "Nador",
        ]
    return AVAILABLE_CITIES

# nombre de villes
def number_cities():
    AVAILABLE_CITIES = get_cities()
    nombre_cities = len(AVAILABLE_CITIES)
    return nombre_cities

# température maximale
def max_temp():
    max_tmp = fetch_weather_data("select max(temperature_2m_max) as max_tmp from weather")
    return max_tmp.iloc[0]["max_tmp"]

# précipitations maximales
def max_prec():
    max_prc = fetch_weather_data("select max(precipitation_probability_max) as max_prc from weather")
    return max_prc.iloc[0]["max_prc"]

# nombre de périodes à risque
def number_perRisk():
    nb_perRisk = fetch_weather_data("select count(*) as nb_perRisk from weather_features where risk_score in ('Medium', 'High)")
    return nb_perRisk.iloc[0]["nb_perRisk"]

# ville présentant le risque le plus élevé
def city_riskEleve():
    risk_el = fetch_weather_data("""select c.city_id, c.city, max(wf.risk_score) as max_risk from cities c
        join weather w on c.city_id = w.city_id
        join weather_features wf on wf.weather_id = w.weather_id 
        group by c.city_id, c.city 
        order by max_risk desc 
        limit 1
    """)
    return risk_el

def load_dashboard_data(USE_DB=False):

    if USE_DB:
        try:
            df = fetch_weather_data("""
                select c.city, c.lng, c.lat, w.weather_code, w.wind_gusts_10m_max, w.wind_speed_10m_max, w.precipitation_probability_max, w.precipitation_sum, w.temperature_2m_min, w.temperature_2m_max, w.time AS date, wf.temp_category, wf.prec_category, wf.wind_category, wf.risk_temp, wf.risk_prec, wf.risk_wind, wf.risk_score, wf.risk_level
                from cities c
                join weather w on c.city_id = w.city_id
                join weather_features wf on w.weather_id = wf.weather_id
            """)
            return df
        except Exception as e:
            st.error(f"Erreur PostgreSQL : {e}")
            st.stop()
    return pd.DataFrame()
    
def filter_data(df, selected_cities, selected_risk):
    risk_or = {"Low": 0, "Medium": 1, "High": 2}
    min_risk_level = risk_or[selected_risk]

    filtered_df = df.copy()
    if selected_cities:
        filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]

    risk_rank = filtered_df["risk_level"].map(risk_or).fillna(-1)
    filtered_df = filtered_df[risk_rank >= min_risk_level]
    return filtered_df

def display_metrics(filtered_df, empty_state, metric_card):
    if filtered_df.empty:
        empty_state("No data matches your filters", icon_name="inbox")
        return
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        nb = filtered_df["city"].nunique()
        metric_card("Average temperature", f"{filtered_df['temperature_2m_max'].mean():.1f}°C", f"for {len(filtered_df)} cities", icon_name="thermometer", variant="temp",)
    with col2:
        metric_card("Average precipitation probability", f"{filtered_df['precipitation_probability_max'].mean():.0f}%", "Current trend", icon_name="droplets", variant="humid",)
    with col3:
        metric_card("Average wind", f"{filtered_df['wind_speed_10m_max'].mean():.0f}km/h", "Current trend", icon_name="wind", variant="wind",)
    with col4:
        hr = (filtered_df["risk_level"] == "High").sum()
        metric_card("High-risk alerts", str(hr), f"for {len(filtered_df)} cities", icon_name="cloud-lightning", variant="alert",)   
