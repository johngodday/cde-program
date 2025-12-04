
  create view "postgres"."cde_cde"."stg_forecast_weather__dbt_tmp"
    
    
  as (
    WITH source AS (
    SELECT *
    FROM cde.forecast_weather
)
SELECT
    id,
    state,
    city,
    forecast_time,
    temp,
    feels_like,
    temp_min,
    temp_max,
    pressure,
    humidity,
    weather_main,
    weather_description,
    wind_speed,
    wind_deg,
    clouds,
    pop,
    run_time
FROM source
  );