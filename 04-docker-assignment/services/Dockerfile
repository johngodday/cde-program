FROM python:3.11-slim
WORKDIR /app
RUN pip install dbt-core dbt-postgres
COPY project /app
WORKDIR /app
CMD ["bash", "-lc", "dbt deps && dbt run && dbt test"]
