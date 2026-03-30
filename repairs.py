import sqlite3
from datetime import datetime

DB = "rental.db"

def add_repair(bike_id, issue, mechanic):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO repairs (bike_id, issue, mechanic, status, start_date)
        VALUES (?, ?, ?, 'open', ?)
    """, (bike_id, issue, mechanic, datetime.now()))

    # update bike status
    cur.execute("UPDATE bikes SET status='under_repair' WHERE id=?", (bike_id,))

    conn.commit()
    conn.close()
    print("Repair job created.")

def close_repair(repair_id, cost):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        UPDATE repairs
        SET status='closed', end_date=?, cost=?
        WHERE id=?
    """, (datetime.now(), cost, repair_id))

    # make bike available again
    cur.execute("""
        UPDATE bikes
        SET status='available'
        WHERE id = (SELECT bike_id FROM repairs WHERE id=?)
    """, (repair_id,))

    conn.commit()
    conn.close()
    print("Repair closed.")