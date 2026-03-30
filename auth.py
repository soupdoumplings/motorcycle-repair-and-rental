from utils import get_input

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"},
}


def login():
    """Prompt for credentials; return role string or None on failure."""
    print("\n=== Motorcycle Rental & Repair System ===")
    username = get_input("Username: ")
    password = get_input("Password: ")

    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"\nWelcome, {username}! (Role: {user['role']})")
        return user["role"]

    print("Login failed — incorrect username or password.")
    return None