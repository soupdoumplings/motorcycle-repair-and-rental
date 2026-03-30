from db import get_db
from utils import get_input
from datetime import datetime


def log_repair():
    """Log a new repair — sets bike status to under_repair."""
    bike_id  = get_input("Enter Bike ID: ")
    issue    = get_input("Describe the issue: ")
    mechanic = input("Mechanic name (optional, press Enter to skip): ").strip() or "Unassigned"
    mechanic_val = mechanic

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT model, status FROM bikes WHERE id = ?", (bike_id,))
    bike = cursor.fetchone()
    if not bike:
        print("Error: Bike not found.")
        conn.close()
        return
    if bike[1] == 'rented':
        print(f"Warning: Bike '{bike[0]}' is currently rented.")

    cursor.execute(
        "INSERT INTO repairs (bike_id, issue, mechanic, status, start_date) VALUES (?, ?, ?, 'pending', ?)",
        (bike_id, issue, mechanic, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    cursor.execute("UPDATE bikes SET status = 'under_repair' WHERE id = ?", (bike_id,))
    conn.commit()
    conn.close()
    print(f"✓ Repair logged. Bike '{bike[0]}' marked as under_repair.")


def update_repair_status():
    """Advance a repair: pending → in_progress → completed."""
    repair_id = get_input("Enter Repair ID: ")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT bike_id, status FROM repairs WHERE id = ?", (repair_id,))
    repair = cursor.fetchone()

    if not repair:
        print("Error: Repair record not found.")
        conn.close()
        return

    bike_id, current_status = repair
    transitions = {"pending": "in_progress", "in_progress": "completed"}

    if current_status not in transitions:
        print(f"Repair is already '{current_status}'. No further updates possible.")
        conn.close()
        return

    new_status = transitions[current_status]
    print(f"  Advancing status: {current_status} → {new_status}")

    if new_status == "completed":
        cost_str = get_input("Enter repair cost (Rs): ")
        try:
            cost = float(cost_str)
        except ValueError:
            print("Invalid cost amount.")
            conn.close()
            return
        cursor.execute(
            "UPDATE repairs SET status = ?, end_date = ?, cost = ? WHERE id = ?",
            (new_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cost, repair_id)
        )
        cursor.execute("UPDATE bikes SET status = 'available' WHERE id = ?", (bike_id,))
        print(f"✓ Repair completed. Bike ID {bike_id} is now available.")
    else:
        cursor.execute("UPDATE repairs SET status = ? WHERE id = ?", (new_status, repair_id))
        print(f"✓ Repair status updated to '{new_status}'.")

    conn.commit()
    conn.close()


def list_repairs():
    """Display all repair records."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, b.model, r.issue, r.mechanic, r.status, r.start_date, r.cost
        FROM repairs r
        JOIN bikes b ON r.bike_id = b.id
        ORDER BY r.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No repair records found.")
        return

    print(f"\n{'ID':<5} | {'Bike':<25} | {'Issue':<25} | {'Mechanic':<15} | {'Status':<12} | {'Date':<12} | Cost")
    print("-" * 110)
    for r in rows:
        cost_str = f"Rs.{r[6]:.0f}" if r[6] is not None else "—"
        print(f"{r[0]:<5} | {r[1]:<25} | {r[2]:<25} | {r[3] or '—':<15} | {r[4]:<12} | {str(r[5])[:10]:<12} | {cost_str}")
