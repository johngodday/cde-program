FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir dbt-core dbt-postgres

COPY project/ /app/

CMD ["bash", "-lc", "dbt run && dbt test"]
