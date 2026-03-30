from db import init_db, seed_db, get_db
from auth import login
from utils import print_menu
import customer
import rentals
import repairs


# ─── Menu definitions ───────────────────────────────────────────────
ADMIN_MENU = [
    "Add Customer",
    "List Customers",
    "List Bikes",
    "Rent a Bike",
    "Return a Bike",
    "Log a Repair",
    "Update Repair Status",
    "List Repairs",
    "Exit",
]

STAFF_MENU = [
    "List Customers",
    "List Bikes",
    "Rent a Bike",
    "Return a Bike",
    "Exit",
]


def run_menu(role):
    menu = ADMIN_MENU if role == "admin" else STAFF_MENU
    while True:
        choice = print_menu(menu)

        if choice == "Add Customer":
            customer.add_customer()

        elif choice == "List Customers":
            customer.list_customers()

        elif choice == "List Bikes":
            rentals.list_bikes()

        elif choice == "Rent a Bike":
            rentals.rent_bike()

        elif choice == "Return a Bike":
            rentals.return_bike()

        elif choice == "Log a Repair":
            repairs.log_repair()

        elif choice == "Update Repair Status":
            repairs.update_repair_status()

        elif choice == "List Repairs":
            repairs.list_repairs()

        elif choice == "Exit":
            print("Goodbye!")
            break


def main():
    # Initialize DB on every startup (safe — uses CREATE IF NOT EXISTS)
    init_db()
    seed_db()

    # Login loop — keep asking until valid credentials
    role = None
    while role is None:
        role = login()
        if role is None:
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != "y":
                print("Exiting.")
                return

    run_menu(role)


if __name__ == "__main__":
    main()
