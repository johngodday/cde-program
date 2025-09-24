import psycopg2

def load(df):
    conn = psycopg2.connect(
        host="etl_db",
        database="etl_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO sales (id, item, amount, total_value) VALUES (%s, %s, %s, %s);",
            (int(row["id"]), row["item"], int(row["amount"]), int(row["total_value"]))
        )

    conn.commit()
    cur.close()
    conn.close()
    print("[load] Data successfully inserted into sales table")
