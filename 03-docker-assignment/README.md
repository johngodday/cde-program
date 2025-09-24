# 🚀 Dockerized Python ETL Pipeline

This project demonstrates a simple **ETL (Extract, Transform, Load)** pipeline built with Python and Docker, connected to a PostgreSQL database running in its own container.  


-------
## Steps Taken 

1. **Set Up PostgreSQL Container**: Created a Docker container for PostgreSQL with an initialization script to set up the database schema.

2. **Develop ETL Scripts**: Wrote Python scripts for each ETL step (extract, transform, load) and a main script to orchestrate the process.

3. **Dockerize ETL Process**: Created a Dockerfile for the ETL container, specifying the Python environment and dependencies.

4. **Networking**: Configured a Docker network to allow communication between the ETL and PostgreSQL containers.

5. **Automation Script**: Developed a Bash script to automate the setup and execution of the entire ETL pipeline.

6. **Environment Variables**: Used a `.env` file to manage sensitive information like database credentials.

---

## 🛠️ Prerequisites
- Docker installed on your machine
- Basic knowledge of Docker and Python
- PostgreSQL basics
- Bash scripting basics
- Sample CSV data for testing
- Python installed (if you want to run scripts locally)
- `psycopg2` library for PostgreSQL connection in Python
- `pandas` library for data manipulation in Python
- `dotenv` library for loading environment variables in Python



