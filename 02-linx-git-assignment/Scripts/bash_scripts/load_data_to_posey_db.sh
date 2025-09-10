#!/usr/bin/env bash
################################################
##### LOAD DATA TO DATABASE SCRIPT
################################################

if [ -f .env ]; then
    source .env
else
    echo "ERROR: .env file not found!"
    exit 1
fi

container="$POSTGRES_CONTAINER"

###############################################################
##### DOWNLOAD DATA FROM SOURCE
###############################################################

raw_folder="$RAW_FOLDER"
processed_folder="$PROCESSED_FOLDER"
source_url="$SOURCE_URL"


mkdir -p "$raw_folder" "$processed_folder"

files=("accounts.csv" "region.csv" "sales_reps.csv" "orders.csv" "web_events.csv")

# 1. Download each CSV
for file in "${files[@]}"; do
    echo "Downloading --- $file"
    curl -s -L "$source_url/$file" -o "$raw_folder/$file"
done

# 2. Move CSVs to processed if they exist
csv_files=("$raw_folder"/*.csv)

if [ ${#csv_files[@]} -eq 0 ]; then
    echo "No CSV files found in $raw_folder"
    exit 0
else
    for file in "${csv_files[@]}"; do
        mv "$file" "$processed_folder/"
        echo "Moved $(basename "$file") → $processed_folder"
    done

    # 3. Clean RAW folder
    echo "Cleaning RAW folder..."
    find "$raw_folder" -type f ! -name "*.csv" -exec rm -f {} \;
fi


###################################################################
### Load CSVs into PostgreSQL database
###################################################################

#database connection details
DB_HOST="$PGHOST"
DB_PORT="$PGPORT"
DB_NAME="$DB_NAME"
DB_USER="$PGUSER"
DB_PASSWORD="$DB_PASSWORD"



# Declare create table statements
declare -A create_statements

create_statements[accounts]="
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    name TEXT,
    website TEXT,
    lat NUMERIC,
    long NUMERIC,
    primary_poc TEXT,
    sales_rep_id INT
);"

create_statements[region]="
DROP TABLE IF EXISTS region;
CREATE TABLE region (
    id INT PRIMARY KEY,
    name TEXT
);"

create_statements[sales_reps]="
DROP TABLE IF EXISTS sales_reps;
CREATE TABLE sales_reps (
    id INT PRIMARY KEY,
    name TEXT,
    region_id INT
);"

create_statements[orders]="
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id INT PRIMARY KEY,
    account_id INT,
    occurred_at TIMESTAMP,
    standard_qty INT,
    gloss_qty INT,
    poster_qty INT,
    total INT,
    standard_amt_usd NUMERIC,
    gloss_amt_usd NUMERIC,
    poster_amt_usd NUMERIC,
    total_amt_usd NUMERIC
);"

create_statements[web_events]="
DROP TABLE IF EXISTS web_events;
CREATE TABLE web_events (
    id INT PRIMARY KEY,
    account_id INT,
    occurred_at TIMESTAMP,
    channel TEXT
);"


# ==============================
# Load each table
# ==============================

echo "Checking if connection is okay..."

if docker exec -i "$container" psql -U "$DB_USER" -d "$DB_NAME" -c "\conninfo"; then
    echo "Connected to database $DB_NAME as user $DB_USER"
else
    echo "Failed to connect to database $DB_NAME"
    exit 1
fi

for table in "${!create_statements[@]}"; do
    file="$processed_folder/$table.csv"
    echo $file

    if [ -f "$file" ]; then
        echo "Processing $table ..."

        # 1. Drop & Create table
        docker exec -i "$container" psql -U "$DB_USER" -d "$DB_NAME" -c "${create_statements[$table]}"
        echo ${create_statements[$table]}

        # 2. Load CSV into table
        docker exec -i "$container" psql -U "$DB_USER" -d "$DB_NAME" -c "\COPY $table FROM STDIN WITH CSV HEADER;" < "$file"
        echo "Loaded $file into $table"
    else
        echo "Skipping $table (no CSV found in $processed_folder)"
    fi
done

echo "All available CSVs loaded into $DB_NAME database"


## END OF SCRIPT ##
