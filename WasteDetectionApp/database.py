import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def get_user(username):
    users = load_users()
    return users.get(username)

def add_user(username, password):
    users = load_users()
    users[username] = {"password": password}
    save_users(users)
