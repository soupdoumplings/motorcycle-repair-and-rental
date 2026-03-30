USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}

def login():
    username = input("Username: ")
    password = input("Password: ")
    
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Welcome {username}!")
        return user["role"]
    print("Login failed!")
    return None