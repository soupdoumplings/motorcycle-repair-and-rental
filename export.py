import sqlite3
import csv
import shutil

DB = "rental.db"

def export_to_csv(table_name):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()

    with open(f"{table_name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    conn.close()
    print(f"{table_name} exported to CSV.")


def backup_database():
    shutil.copy(DB, "backup_rental.db")
    print("Database backup created.")