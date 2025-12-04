import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=10))
def extract_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "weather_time": data.get("dt"),
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "weather_main": data["weather"][0]["main"],
        "weather_description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "wind_deg": data["wind"].get("deg"),
        "clouds": data["clouds"].get("all"),
        "sunrise": data["sys"].get("sunrise"),
        "sunset": data["sys"].get("sunset"),
    }

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=10))
def extract_forecast_weather(city):
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = []
    for entry in data.get("list", []):
        results.append({
            "forecast_time": entry.get("dt"),
            "temp": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "temp_min": entry["main"]["temp_min"],
            "temp_max": entry["main"]["temp_max"],
            "pressure": entry["main"]["pressure"],
            "humidity": entry["main"]["humidity"],
            "weather_main": entry["weather"][0]["main"],
            "weather_description": entry["weather"][0]["description"],
            "wind_speed": entry["wind"]["speed"],
            "wind_deg": entry["wind"].get("deg"),
            "clouds": entry["clouds"].get("all"),
            "pop": entry.get("pop")  # precipitation probability
        })
    return results
