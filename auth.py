from utils import get_input

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

def login():
    username = get_input("Username: ")
    password = get_input("Password: ")
    
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Welcome {username}!")
        return user["role"]
    print("Login failed!")
    return None