from db import get_db

def seed_data():
    conn = get_db()
    c = conn.cursor()
    
    # 🏍️ Add Sample Bikes
    bikes = [
        ('Royal Enfield Classic 350', 2023, 'available'),
        ('Honda CB350RS', 2024, 'available'),
        ('Yamaha MT-15', 2022, 'repairing'),
        ('KTM Duke 390', 2023, 'rented')
    ]
    c.executemany("INSERT INTO bikes (model, year, status) VALUES (?, ?, ?)", bikes)
    
    # 👤 Add Sample Customers
    customers = [
        ('Sanjay Thapa', '9841234567'),
        ('Maya Gurung', '9801234568'),
        ('Ankita Rai', '9811234569')
    ]
    c.executemany("INSERT INTO customers (name, phone) VALUES (?, ?)", customers)
    
    # 📅 Add a Sample Rental
    # Assuming KTM Duke 390 (ID 4) is rented by Sanjay (ID 1)
    c.execute("INSERT INTO rentals (bike_id, customer_id, start_date, end_date) VALUES (4, 1, '2026-03-25', '2026-03-31')")
    
    # 🛠️ Add a Sample Repair
    # Assuming Yamaha MT-15 (ID 3) is in repair
    c.execute("INSERT INTO repairs (bike_id, description, status) VALUES (3, 'Brake pad replacement and engine check', 'pending')")
    
    conn.commit()
    conn.close()
    print("Database seeded with sample bikes, customers, rentals, and repairs.")

if __name__ == "__main__":
    seed_data()
