import sqlite3

DB = "rental.db"

def daily_rentals():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT DATE(start_date), COUNT(*)
        FROM rentals
        GROUP BY DATE(start_date)
    """)

    data = cur.fetchall()
    conn.close()

    print("Date | Rentals")
    print("-" * 20)
    for row in data:
        print(row[0], "|", row[1])


def overdue_rentals():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, customer_id, due_date
        FROM rentals
        WHERE status='active' AND due_date < DATE('now')
    """)

    data = cur.fetchall()
    conn.close()

    print("Overdue Rentals:")
    for r in data:
        print(r)