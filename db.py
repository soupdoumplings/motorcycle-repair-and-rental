import sqlite3
import os

DB_NAME = "rental"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Create bikes table
    c.execute('''CREATE TABLE IF NOT EXISTS bikes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    year INTEGER,
                    status TEXT DEFAULT 'available'
                )''')
    
    # Create customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE
                )''')
    
    # Create rentals table
    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bike_id INTEGER,
                    customer_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    FOREIGN KEY(bike_id) REFERENCES bikes(id),
                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                )''')
    
    # Create repairs table
    c.execute('''CREATE TABLE IF NOT EXISTS repairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bike_id INTEGER,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY(bike_id) REFERENCES bikes(id)
                )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database and tables initialized.")
