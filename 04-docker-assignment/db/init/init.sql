-- CREATE SCHEMA IF NOT EXISTS cde;


-- CREATE TABLE IF NOT EXISTS cde.stg_current_weather (
-- id SERIAL PRIMARY KEY,
-- state TEXT,
-- city TEXT,
-- weather_time TIMESTAMP,
-- temp DOUBLE PRECISION,
-- temp_min DOUBLE PRECISION,
-- temp_max DOUBLE PRECISION,
-- humidity INT,
-- wind_speed DOUBLE PRECISION,
-- description TEXT,
-- lat DOUBLE PRECISION,
-- lon DOUBLE PRECISION,
-- run_time TIMESTAMP DEFAULT now()
-- );


-- CREATE TABLE IF NOT EXISTS cde.stg_forecast_weather (
-- id SERIAL PRIMARY KEY,
-- state TEXT,
-- city TEXT,
-- forecast_time TIMESTAMP,
-- temp DOUBLE PRECISION,
-- temp_min DOUBLE PRECISION,
-- temp_max DOUBLE PRECISION,
-- humidity INT,
-- wind_speed DOUBLE PRECISION,
-- description TEXT,
-- lat DOUBLE PRECISION,
-- lon DOUBLE PRECISION,
-- run_time TIMESTAMP DEFAULT now()
-- );


-- -- simple audit table
-- CREATE SCHEMA IF NOT EXISTS audit;
-- CREATE TABLE IF NOT EXISTS audit.job_runs (
-- id SERIAL PRIMARY KEY,
-- job_name TEXT,
-- started_at TIMESTAMP,
-- finished_at TIMESTAMP,
-- status TEXT,
-- details JSONB
-- );

-- Create schema
CREATE SCHEMA IF NOT EXISTS cde;

-- Table for current weather data
CREATE TABLE IF NOT EXISTS cde.current_weather (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    city VARCHAR(100),
    weather_time TIMESTAMP,
    temp NUMERIC,
    feels_like NUMERIC,
    temp_min NUMERIC,
    temp_max NUMERIC,
    pressure INT,
    humidity INT,
    weather_main VARCHAR(100),
    weather_description VARCHAR(255),
    wind_speed NUMERIC,
    wind_deg INT,
    clouds INT,
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    run_time TIMESTAMP DEFAULT NOW()
);

-- Table for forecast weather data
CREATE TABLE IF NOT EXISTS cde.forecast_weather (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    city VARCHAR(100),
    forecast_time TIMESTAMP,
    temp NUMERIC,
    feels_like NUMERIC,
    temp_min NUMERIC,
    temp_max NUMERIC,
    pressure INT,
    humidity INT,
    weather_main VARCHAR(100),
    weather_description VARCHAR(255),
    wind_speed NUMERIC,
    wind_deg INT,
    clouds INT,
    pop NUMERIC, -- Probability of precipitation
    run_time TIMESTAMP DEFAULT NOW()
);

-- Audit table for tracking ETL runs
CREATE TABLE IF NOT EXISTS cde.job_runs (
    id SERIAL PRIMARY KEY,
    run_start TIMESTAMP,
    run_end TIMESTAMP,
    status VARCHAR(20),
    rows_current INT,
    rows_forecast INT,
    error_message TEXT
);
