from db import init_db, get_db
from auth import login
from utils import print_menu, get_input

# Test DB
init_db()

# Test Auth
print("\n--- Test Login ---")
role = login()
print(f"Role: {role}")

# Test Utils
print("\n--- Test Menu ---")
if role == "admin":
    menu = ["Manage Cars", "Manage Customers", "View Rentals", "View Repairs", "Exit"]
else:
    menu = ["View Cars", "Create Rental", "Exit"]

choice = print_menu(menu)
print(f"You chose: {choice}")