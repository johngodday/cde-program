import time
from datetime import datetime
from extract import extract_current_weather, extract_forecast_weather
from load import load_current_weather, load_forecast_weather, get_connection

# Dictionary of Nigerian states mapped to major cities
NIGERIA_STATES = {
    "Abia": "Umuahia",
    "Adamawa": "Yola",
    "Akwa Ibom": "Uyo",
    "Anambra": "Awka",
    "Bauchi": "Bauchi",
    "Bayelsa": "Yenagoa",
    "Benue": "Makurdi",
    "Borno": "Maiduguri",
    "Cross River": "Calabar",
    "Delta": "Asaba",
    "Ebonyi": "Abakaliki",
    "Edo": "Benin City",
    "Ekiti": "Ado Ekiti",
    "Enugu": "Enugu",
    "Gombe": "Gombe",
    "Imo": "Owerri",
    "Jigawa": "Dutse",
    "Kaduna": "Kaduna",
    "Kano": "Kano",
    "Katsina": "Katsina",
    "Kebbi": "Birnin Kebbi",
    "Kogi": "Lokoja",
    "Kwara": "Ilorin",
    "Lagos": "Lagos",
    "Nasarawa": "Lafia",
    "Niger": "Minna",
    "Ogun": "Abeokuta",
    "Ondo": "Akure",
    "Osun": "Osogbo",
    "Oyo": "Ibadan",
    "Plateau": "Jos",
    "Rivers": "Port Harcourt",
    "Sokoto": "Sokoto",
    "Taraba": "Jalingo",
    "Yobe": "Damaturu",
    "Zamfara": "Gusau"
}

def log_run(start_time, end_time, status, rows_current, rows_forecast, error_message=""):
    conn = get_connection()
    cur = conn.cursor()
    insert_sql = """
        INSERT INTO cde.job_runs (
            run_start, run_end, status, rows_current, rows_forecast, error_message
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_sql, (
        start_time,
        end_time,
        status,
        rows_current,
        rows_forecast,
        error_message
    ))
    conn.commit()
    cur.close()
    conn.close()

def main():
    start_time = datetime.now()
    rows_current = 0
    rows_forecast = 0
    error_message = ""
    
    try:
        for state, city in NIGERIA_STATES.items():
            # Current Weather
            current_data = extract_current_weather(city)
            load_current_weather(state, city, current_data)
            rows_current += 1

            # Forecast
            forecast_data = extract_forecast_weather(city)
            load_forecast_weather(state, city, forecast_data)
            rows_forecast += len(forecast_data)

            # Delay to avoid rate limit
            time.sleep(1)

        status = "success"

    except Exception as e:
        status = "failed"
        error_message = str(e)

    end_time = datetime.now()
    log_run(start_time, end_time, status, rows_current, rows_forecast, error_message)

if __name__ == "__main__":
    main()
