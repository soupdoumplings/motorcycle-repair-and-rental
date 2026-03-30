import utils # From Dev 1

def add_customer(conn):
    name = utils.get_input("Enter Customer Name: ")
    contact = utils.get_input("Enter Contact Number: ")
    license_num = utils.get_input("Enter License Number: ")
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, contact, license) VALUES (?, ?, ?)", 
                   (name, contact, license_num))
    conn.commit()
    print("Customer added successfully!")

def list_customers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    print(f"{'ID':<5} | {'Name':<20} | {'Contact':<15} | {'License':<15}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15} | {r[3]:<15}")