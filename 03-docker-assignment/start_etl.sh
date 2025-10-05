#!/usr/bin/env bash
set -euo pipefail

CLEANUP=false

# Parse args
if [[ $# -gt 0 && $1 == "--clean" ]]; then
  CLEANUP=true
fi

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "[ERROR] No .env file found"
  exit 1
fi

# Create Docker network if it doesn't exist
if ! docker network ls --format '{{.Name}}' | grep -q '^etl-net$'; then
  echo "[INFO] Creating Docker network: etl-net"
  docker network create etl-net
fi

# Stop/remove old DB if running
if docker ps -a --format '{{.Names}}' | grep -q '^etl_db$'; then
  echo "[INFO] Removing old Postgres container..."
  docker rm -f etl_db >/dev/null 2>&1 || true
fi

# Start Postgres container
echo "[INFO] Starting Postgres container..."
docker run -d \
  --name etl_db \
  --network etl-net \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -v "$(pwd)/db:/docker-entrypoint-initdb.d:ro" \
  postgres:15

# Wait for DB init
echo "[INFO] Waiting for Postgres to be ready..."
until docker exec etl_db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
  sleep 2
done
echo "[SUCCESS] Postgres is ready."



# Ensure sales table exists
echo "[INFO] Ensuring sales table exists..."
docker exec -i etl_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    item TEXT NOT NULL,
    amount INT NOT NULL,
    total_value INT NOT NULL
);
SQL



# Build ETL image
echo "[INFO] Building ETL image..."
docker build -t etl_image ./etl

# Run ETL container
echo "[INFO] Running ETL pipeline..."
docker run --rm \
  --name etl_pipeline \
  --network etl-net \
  -e DB_HOST=etl_db \
  -e DB_PORT=5432 \
  -e DB_NAME=$POSTGRES_DB \
  -e DB_USER=$POSTGRES_USER \
  -e DB_PASSWORD=$POSTGRES_PASSWORD \
  etl_image

# Show DB contents
echo "[INFO] Dumping sales table..."
docker exec -i etl_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM sales;"

# Optional cleanup
if [ "$CLEANUP" = true ]; then
  echo "[INFO] Cleaning up containers and network..."
  docker rm -f etl_db >/dev/null 2>&1 || true
  docker network rm etl-net >/dev/null 2>&1 || true
  echo "[SUCCESS] Cleanup complete."
else
  echo "[INFO] Containers are still running. Use './start_etl.sh --clean' to remove them."
fi
