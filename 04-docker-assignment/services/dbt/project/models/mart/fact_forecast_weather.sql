SELECT
    state,
    city,
    forecast_time,
    temp,
    feels_like,
    pressure,
    humidity,
    wind_speed,
    pop,
    clouds,
    run_time
FROM {{ ref('stg_forecast_weather') }}
