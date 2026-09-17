DROP TABLE IF EXISTS weather_features;
DROP TABLE IF EXISTS weather;
DROP TABLE IF EXISTS cities;

CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    country VARCHAR(100),
    iso2 VARCHAR(2),
    admin_name VARCHAR(100),
    capital VARCHAR(50),
    population BIGINT,
    population_proper BIGINT
);


CREATE TABLE IF NOT EXISTS weather (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    weather_code INTEGER,
    wind_gusts_10m_max DOUBLE PRECISION,
    wind_speed_10m_max DOUBLE PRECISION,
    precipitation_probability_max INTEGER,
    precipitation_sum DOUBLE PRECISION,
    temperature_2m_min DOUBLE PRECISION,
    temperature_2m_max DOUBLE PRECISION,
    time DATE
);

CREATE TABLE IF NOT EXISTS weather_features (
    feature_id SERIAL PRIMARY KEY,
    weather_id INTEGER REFERENCES weather(weather_id),
    temp_category VARCHAR(20),
    prec_category VARCHAR(20),
    wind_category VARCHAR(20),
    risk_temp INTEGER,
    risk_prec INTEGER,
    risk_wind INTEGER,
    risk_score INTEGER,
    risk_level VARCHAR(20)
);

-- SELECT COUNT(*) FROM cities;
-- SELECT COUNT(*) FROM weather;
-- SELECT COUNT(*) FROM weather_features;