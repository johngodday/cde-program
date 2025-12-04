
  create view "postgres"."cde"."fact_current_weather__dbt_tmp"
    
    
  as (
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
FROM "postgres"."cde_cde"."stg_current_weather"
  );