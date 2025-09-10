#!/usr/bin/env bash

################################################
##### ETL BASH PIPELINE SCRIPT
################################################

#Activate .env environment variables
if [ -f .env ]; then
    source .env
else
    echo "ERROR: .env file not found!"
    exit 1
fi


# Define file paths
RAW_FILE_PATH="$RAW_DIR/$RAW_FILE"
TRANSFORMED_FILE_PATH="$TRANSFORMED_DIR/$TRANSFORMED_FILE"
GOLD_FILE_PATH="$GOLD_DIR/$GOLD_FILE"

# 1. Load CSV file from link

curl -s -L -o "$RAW_FILE_PATH" "$DATA_URL"

if [ -f "$RAW_FILE_PATH" ]; then
    echo "[Extract] File successfully downloaded to $RAW_FILE_PATH"
else
    echo "[Extract] ERROR: File not found in $RAW_DIR"
    exit 1
fi


####################################################################################################
####################################################################################################
# 2. Transform: Clean and process the data
####################################################################################################

awk -F',' '
NR==1 {
    for (i=1; i<=NF; i++) {
        if ($i=="Variable_code") $i="variable_code"
        col[$i]=i
    }
    print "year,Value,Units,variable_code"
    next
}
{
    print $col["year"]","$col["Value"]","$col["Units"]","$col["variable_code"]
}
' "$RAW_FILE_PATH" > "$TRANSFORMED_FILE_PATH"

if [ -f "$TRANSFORMED_FILE_PATH" ]; then
    echo "File successfully transformed and saved to $TRANSFORMED_FILE_PATH"
else
    echo "Transformation failed!"
    exit 1
fi

####################################################################################################
####################################################################################################
# 3. Load: Save the cleaned data to the gold directory
####################################################################################################

cp "$TRANSFORMED_FILE_PATH" "$GOLD_FILE_PATH"

if [ -f "$GOLD_FILE_PATH" ]; then
    echo "Load File successfully loaded into $GOLD_FILE_PATH"
else
    echo "Loading failed."
    exit 1
fi


echo "ETL Pipeline completed successfully."


########################################################################################################
# End of etl_bash_pipeline.sh
########################################################################################################    
