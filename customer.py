from db import get_db
from utils import get_input


def add_customer():
    name        = get_input("Enter Customer Name: ")
    contact     = get_input("Enter Contact Number: ")
    license_num = get_input("Enter License Number: ")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, contact, license) VALUES (?, ?, ?)",
        (name, contact, license_num)
    )
    conn.commit()
    conn.close()
    print("✓ Customer added successfully!")


def list_customers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact, license FROM customers")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No customers found.")
        return

    print(f"\n{'ID':<5} | {'Name':<20} | {'Contact':<15} | {'License':<15}")
    print("-" * 62)
    for r in rows:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[3]:<15}")
