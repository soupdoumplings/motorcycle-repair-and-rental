import sqlite3
import os

DB_NAME = "rental.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    # Bikes table
    c.execute('''CREATE TABLE IF NOT EXISTS bikes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    year INTEGER,
                    daily_rate REAL DEFAULT 500.0,
                    status TEXT DEFAULT 'available'
                )''')

    # Customers table  (name + contact + license — all required per Dev 2 spec)
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    license TEXT NOT NULL
                )''')

    # Rentals table
    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bike_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    total_cost REAL,
                    returned INTEGER DEFAULT 0,
                    FOREIGN KEY(bike_id) REFERENCES bikes(id),
                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                )''')

    # Repairs table
    c.execute('''CREATE TABLE IF NOT EXISTS repairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bike_id INTEGER NOT NULL,
                    issue TEXT NOT NULL,
                    mechanic TEXT,
                    status TEXT DEFAULT 'pending',
                    start_date TEXT,
                    end_date TEXT,
                    cost REAL,
                    FOREIGN KEY(bike_id) REFERENCES bikes(id)
                )''')

    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    c = conn.cursor()

    # Only seed if bikes table is empty
    c.execute("SELECT COUNT(*) FROM bikes")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    bikes = [
        ('Royal Enfield Classic 350', 2023, 800.0, 'available'),
        ('Honda CB350RS',            2024, 700.0, 'available'),
        ('Yamaha MT-15',             2022, 600.0, 'available'),
        ('KTM Duke 390',             2023, 900.0, 'available'),
    ]
    c.executemany(
        "INSERT INTO bikes (model, year, daily_rate, status) VALUES (?, ?, ?, ?)",
        bikes
    )

    customers = [
        ('Sanjay Thapa', '9841234567', 'LIC-001'),
        ('Maya Gurung',  '9801234568', 'LIC-002'),
        ('Ankita Rai',   '9811234569', 'LIC-003'),
    ]
    c.executemany(
        "INSERT INTO customers (name, contact, license) VALUES (?, ?, ?)",
        customers
    )

    conn.commit()
    conn.close()
    print("Database seeded with sample bikes and customers.")


if __name__ == "__main__":
    init_db()
    seed_db()
    print("Database and tables initialized.")
