SELECT
    state,
    city,
    weather_time,
    temp,
    feels_like,
    pressure,
    humidity,
    wind_speed,
    clouds,
    run_time
FROM {{ ref('stg_current_weather') }}
