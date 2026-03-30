from repairs import add_repair, close_repair
from reports import daily_rentals, overdue_rentals
from export import export_to_csv, backup_database

def menu():
    while True:
        print("\n--- Repair & Reports Menu ---")
        print("1. Add Repair")
        print("2. Close Repair")
        print("3. Daily Rentals Report")
        print("4. Overdue Rentals")
        print("5. Export Data")
        print("6. Backup DB")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            bike_id = input("Bike ID: ")
            issue = input("Issue: ")
            mechanic = input("Mechanic: ")
            add_repair(bike_id, issue, mechanic)

        elif choice == "2":
            repair_id = input("Repair ID: ")
            cost = float(input("Cost: "))
            close_repair(repair_id, cost)

        elif choice == "3":
            daily_rentals()

        elif choice == "4":
            overdue_rentals()

        elif choice == "5":
            table = input("Table name: ")
            export_to_csv(table)

        elif choice == "6":
            backup_database()

        elif choice == "0":
            break
        
if __name__ == "__main__":
  menu()