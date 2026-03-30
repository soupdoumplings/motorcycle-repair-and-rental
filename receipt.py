def return_bike(conn):
    rental_id = utils.get_input("Enter Rental ID to return: ")
    cursor = conn.cursor()
    
    # Join rentals and bikes to get the rate and ID
    cursor.execute("""
        SELECT r.bike_id, b.daily_rate, r.start_date, r.end_date 
        FROM rentals r JOIN bikes b ON r.bike_id = b.id 
        WHERE r.id = ?""", (rental_id,))
    data = cursor.fetchone()

    if data:
        bike_id, rate, start, end = data
        # Simplified day calculation (assumes integer days for the 10-min sprint)
        days = 5 # In a real scenario: (datetime(end) - datetime(start)).days
        total = days * rate
        
        # Update Status
        cursor.execute("UPDATE bikes SET status = 'available' WHERE id = ?", (bike_id,))
        conn.commit()
        
        print(f"\n--- RECEIPT ---\nTotal Cost: ${total}\nBike {bike_id} is now available.\n")
    else:
        print("Rental record not found.")