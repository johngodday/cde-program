import os
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def load_current_weather(state, city, data):
    conn = get_connection()
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO cde.current_weather (
            state, city, weather_time, temp, feels_like, temp_min, temp_max,
            pressure, humidity, weather_main, weather_description, wind_speed,
            wind_deg, clouds, sunrise, sunset
        )
        VALUES (
            %(state)s, %(city)s, to_timestamp(%(weather_time)s), %(temp)s,
            %(feels_like)s, %(temp_min)s, %(temp_max)s, %(pressure)s,
            %(humidity)s, %(weather_main)s, %(weather_description)s,
            %(wind_speed)s, %(wind_deg)s, %(clouds)s,
            to_timestamp(%(sunrise)s), to_timestamp(%(sunset)s)
        )
    """

    params = {
        "state": state,
        "city": city,
        **data
    }

    cur.execute(insert_sql, params)
    conn.commit()
    cur.close()
    conn.close()

def load_forecast_weather(state, city, records):
    conn = get_connection()
    cur = conn.cursor()

    insert_sql = """
        INSERT INTO cde.forecast_weather (
            state, city, forecast_time, temp, feels_like, temp_min, temp_max,
            pressure, humidity, weather_main, weather_description, wind_speed,
            wind_deg, clouds, pop
        )
        VALUES %s
    """

    values = [
        (
            state,
            city,
            datetime.utcfromtimestamp(r["forecast_time"]),
            r["temp"],
            r["feels_like"],
            r["temp_min"],
            r["temp_max"],
            r["pressure"],
            r["humidity"],
            r["weather_main"],
            r["weather_description"],
            r["wind_speed"],
            r["wind_deg"],
            r["clouds"],
            r["pop"]
        )
        for r in records
    ]

    execute_values(cur, insert_sql, values)
    conn.commit()
    cur.close()
    conn.close()
