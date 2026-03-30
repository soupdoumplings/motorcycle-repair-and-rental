def rent_bike(conn):
    bike_id = utils.get_input("Enter Bike ID: ")
    
    # Validation Check
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM bikes WHERE id = ?", (bike_id,))
    bike = cursor.fetchone()
    
    if not bike or bike[0] != 'available':
        print("Error: Bike is not available for rental.")
        return

    cust_id = utils.get_input("Enter Customer ID: ")
    start_date = utils.get_input("Enter Start Date (YYYY-MM-DD): ")
    end_date = utils.get_input("Enter End Date (YYYY-MM-DD): ")

    # Transaction: Create rental and Update bike status
    cursor.execute("INSERT INTO rentals (bike_id, customer_id, start_date, end_date) VALUES (?, ?, ?, ?)",
                   (bike_id, cust_id, start_date, end_date))
    cursor.execute("UPDATE bikes SET status = 'rented' WHERE id = ?", (bike_id,))
    conn.commit()
    print("Rental confirmed!")