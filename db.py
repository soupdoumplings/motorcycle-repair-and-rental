import sqlite3
import os

DB_NAME = "rental"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Create cars table
    c.execute('''CREATE TABLE IF NOT EXISTS cars (
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
                    car_id INTEGER,
                    customer_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    FOREIGN KEY(car_id) REFERENCES cars(id),
                    FOREIGN KEY(customer_id) REFERENCES customers(id)
                )''')
    
    # Create repairs table
    c.execute('''CREATE TABLE IF NOT EXISTS repairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_id INTEGER,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY(car_id) REFERENCES cars(id)
                )''')
    
    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()
    
    # 🚗 Add Sample Cars
    cars = [
        ('Tesla Model 3', 2023, 'available'),
        ('Toyota Camry', 2024, 'available'),
        ('Ford Mustang', 2022, 'repairing'),
        ('Honda Civic', 2023, 'rented')
    ]
    c.executemany("INSERT INTO cars (model, year, status) VALUES (?, ?, ?)", cars)
    
    # 👤 Add Sample Customers
    customers = [
        ('Sanjay Thapa', '9841234567'),
        ('Maya Gurung', '9801234568'),
        ('Ankita Rai', '9811234569')
    ]
    c.executemany("INSERT INTO customers (name, phone) VALUES (?, ?)", customers)
    
    # 📅 Add a Sample Rental
    c.execute("INSERT INTO rentals (car_id, customer_id, start_date, end_date) VALUES (4, 1, '2026-03-25', '2026-03-31')")
    
    # 🛠️ Add a Sample Repair
    c.execute("INSERT INTO repairs (car_id, description, status) VALUES (3, 'Brake pad replacement and engine check', 'pending')")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_db()
    print("Database initialized and seeded with sample car data.")
