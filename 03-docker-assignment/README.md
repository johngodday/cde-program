# 🚀 Dockerized Python ETL Pipeline

This project demonstrates a simple **ETL (Extract, Transform, Load)** pipeline built with Python and Docker, connected to a PostgreSQL database running in its own container.  
The containers communicate via a Docker network, and the process is fully automated with a Bash script.

---

## 📂 Project Structure

docker-assignment/
├── etl/
│ ├── Dockerfile # ETL container definition
│ ├── requirements.txt # Python dependencies
│ ├── main_etl.py # Orchestration script
│ ├── extract.py # Extraction logic
│ ├── transform.py # Transformation logic
│ ├── load.py # Loading logic
│ └── data/
│ └── sample_sales.csv # Sample input data
├── db/
│ └── init.sql # Database schema (creates sales table)
├── start_etl.sh # Bash script to run everything
├── .env.example # Example env vars for Postgres
└── README.md # Documentation (this file)


