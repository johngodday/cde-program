
  create view "postgres"."cde_cde"."stg_current_weather__dbt_tmp"
    
    
  as (
    WITH source AS (
    SELECT *
    FROM cde.current_weather
)
SELECT
    id,
    state,
    city,
    weather_time,
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
    sunrise,
    sunset,
    run_time
FROM source
  );