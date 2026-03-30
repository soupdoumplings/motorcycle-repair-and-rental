from db import get_db
from utils import get_input
from datetime import datetime


def _parse_date(date_str):
    """Parse YYYY-MM-DD string to date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def list_bikes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, model, year, daily_rate, status FROM bikes")
    rows = cursor.fetchall()
    conn.close()

    print(f"\n{'ID':<5} | {'Model':<30} | {'Year':<6} | {'Rate/day':<10} | {'Status'}")
    print("-" * 68)
    for r in rows:
        print(f"{r[0]:<5} | {r[1]:<30} | {r[2]:<6} | Rs.{r[3]:<7.0f} | {r[4]}")


def rent_bike():
    list_bikes()
    bike_id = get_input("\nEnter Bike ID to rent: ")

    conn = get_db()
    cursor = conn.cursor()

    # Validate bike exists and is available
    cursor.execute("SELECT status, model FROM bikes WHERE id = ?", (bike_id,))
    bike = cursor.fetchone()

    if not bike:
        print("Error: Bike not found.")
        conn.close()
        return
    if bike[0] != 'available':
        print(f"Error: '{bike[1]}' is not available (status: {bike[0]}).")
        conn.close()
        return

    cust_id    = get_input("Enter Customer ID: ")
    start_date = get_input("Enter Start Date (YYYY-MM-DD): ")
    end_date   = get_input("Enter End Date   (YYYY-MM-DD): ")

    try:
        s = _parse_date(start_date)
        e = _parse_date(end_date)
        if e <= s:
            print("Error: End date must be after start date.")
            conn.close()
            return
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        conn.close()
        return

    # Validate customer exists
    cursor.execute("SELECT id FROM customers WHERE id = ?", (cust_id,))
    if not cursor.fetchone():
        print("Error: Customer not found. Add customer first.")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO rentals (bike_id, customer_id, start_date, end_date) VALUES (?, ?, ?, ?)",
        (bike_id, cust_id, start_date, end_date)
    )
    cursor.execute("UPDATE bikes SET status = 'rented' WHERE id = ?", (bike_id,))
    conn.commit()
    conn.close()
    print(f"✓ Rental confirmed for '{bike[1]}'!")


def return_bike():
    rental_id = get_input("Enter Rental ID to return: ")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, r.bike_id, b.model, b.daily_rate, r.start_date, r.end_date, r.returned
        FROM rentals r
        JOIN bikes b ON r.bike_id = b.id
        WHERE r.id = ?
    """, (rental_id,))
    data = cursor.fetchone()

    if not data:
        print("Error: Rental record not found.")
        conn.close()
        return

    _, bike_id, model, daily_rate, start_str, end_str, returned = data

    if returned:
        print(f"Error: Rental #{rental_id} has already been returned.")
        conn.close()
        return

    try:
        days = (_parse_date(end_str) - _parse_date(start_str)).days
        if days < 1:
            days = 1
    except Exception:
        days = 1

    total = days * daily_rate

    cursor.execute(
        "UPDATE rentals SET returned = 1, total_cost = ? WHERE id = ?",
        (total, rental_id)
    )
    cursor.execute("UPDATE bikes SET status = 'available' WHERE id = ?", (bike_id,))
    conn.commit()
    conn.close()

    print("\n---------- RECEIPT ----------")
    print(f"Rental ID  : {rental_id}")
    print(f"Bike       : {model}")
    print(f"Period     : {start_str} → {end_str} ({days} day(s))")
    print(f"Rate/day   : Rs.{daily_rate:.0f}")
    print(f"Total Cost : Rs.{total:.0f}")
    print("-----------------------------")
    print(f"✓ Bike '{model}' is now available.")
