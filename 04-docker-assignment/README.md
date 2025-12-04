# Weather Data Pipeline for Nigeria

A containerized ETL + transformation pipeline that extracts **current** and **5-day forecast** weather data for all 36 states of Nigeria using the OpenWeather API, loads into PostgreSQL, transforms with dbt, and automates via cron inside Docker.

---

## 🧩 Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Setup & Installation](#setup--installation)  
- [Run Locally via Docker](#run-locally-via-docker)  
- [Automated Scheduling with Cron](#automated-scheduling-with-cron)  
- [Pushing & Using Docker Image](#pushing--using-docker-image)  
- [Database Schema](#database-schema)  
- [Project Structure](#project-structure)  

---

## 🏷️ Features

- Extracts **current weather** and **5-day / 3-hour forecast** for all 36 Nigerian states  
- Loads raw data into PostgreSQL (`cde` schema)  
- Transforms data using **dbt** (staging and fact models)  
- Automates via **cron inside Docker** to run daily  
- Dockerized services for easy deployment  
- Docker Hub image available for reuse

---

## 🏗 Architecture

- Python service queries OpenWeather, normalizes JSON, and writes to staging tables  
- dbt reads staging tables and builds clean models  
- ETL runs automatically at **00:00 UTC daily** via cron in container

                +----------------------+
                |  OpenWeather API     |
                +----------+-----------+
                           |
                           v
                 +---------+---------+
                 |  Python Extractor  |
                 +---------+---------+
                           |
                           v
                 +---------+---------+
                 |  PostgreSQL DB    |
                 +---------+---------+
                           |
                           v
                 +---------+---------+
                 |   DBT Transform   |
                 +---------+---------+
                           |
                           v
                 +---------+---------+
                 |   Clean Data       |
                 +--------------------+


---


## 🧰 Tech Stack

| Component | Tool / Library |
|----------|----------------|
| Extraction & Load | Python, `requests`, `psycopg2` |
| Scheduling | `cron` inside Docker |
| Transformation | dbt Core + dbt-postgres |
| Database | PostgreSQL |
| Containerization | Docker & docker-compose |
| API | OpenWeather (free tier) |

---

## ⚙️ Prerequisites

1. A running PostgreSQL instance accessible by the Docker containers (host machine or remote)  
2. An API key from [OpenWeather](https://openweathermap.org/)  
3. Docker & docker-compose installed  
4. A GitHub account and repository for this project

---

## 🚀 Setup & Installation

1. Fork or clone your repo under `https://github.com/johngodday/cde-program`  (and go to 04-docker-assignment folder)
2. Copy `.env` from `.env.example` and fill in:

   ```env
   POSTGRES_HOST=<your_host_ip_or_host.docker.internal>
   POSTGRES_PORT=5432
   POSTGRES_DB=<your_db>
   POSTGRES_USER=<your_user>
   POSTGRES_PASSWORD=<your_pwd>
   OPENWEATHER_API_KEY=<your_api_key>

3. psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f db/init/init.sql

---

## Run Locally via Docker

1. Build the Service
     docker-compose build
2. Run ETL Once (extract + Load)
     docker compose run --rm py-etl
3. Run dbt
     docker compose run --rm dbt 
4. Check if the table are available 
     SELECT * FROM cde.current_weather LIMIT 5;
     SELECT * FROM cde.fact_current_weather LIMIT 5;


----

## Automated Scheduling with Cron

0 0 * * * python /app/run_once.py >> /app/cron.log 2>&1


-----

## Project Structure

04-docker-assignment/
├── .env.example
├── docker-compose.yml
├── db/
│   └── init/
│       └── init.sql
├── services/
│   ├── py-etl/
│   │   ├── Dockerfile
│   │   └── app/
│   │       ├── run_once.py
│   │       ├── extract.py
│   │       └── load.py
│   └── dbt/
│       ├── Dockerfile
│       └── project/
│           ├── dbt_project.yml
│           ├── profiles.yml
│           └── models/
│               ├── staging/
│               └── marts/
├── logs/
│   ├── python/
│   └── dbt/
└── data/
    └── raw/


--------

## Docker Hub Usage

You can pull the pre-built image from Docker Hub

   - docker pull johngodday/python-etl-docker:latest

Then in your docker-compose.yml, replace build section with 

   - py-etl:
       image: johngodday/python-etl-docker:latest
 -----

## Database Schema (cde)

Your key tables/views include:

    cde.current_weather (raw current)
    cde.forecast_weather (raw forecast)
    cde.job_runs (audit)

Views via dbt:

    cde.stg_current_weather, cde.stg_forecast_weather
    cde.fact_current_weather, cde.fact_forecast_weather

## Visualization of the top 5 Hotest State 

<p align="center">
  <img src="Metabase-Top 5 Hottest States Today.png" width="200" />
</p>