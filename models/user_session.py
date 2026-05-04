import json
import os
import hashlib

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users.json")
SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "session.json")


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    """Returns (success, error_message)"""
    users = load_users()
    if email in users:
        return False, "Email already registered"
    users[email] = {
        "name": name,
        "email": email,
        "password": _hash_password(password),
    }
    save_users(users)
    save_session(email)
    return True, ""


def login_user(email: str, password: str) -> tuple[bool, str]:
    """Returns (success, error_message)"""
    users = load_users()
    if email not in users:
        return False, "Email not found"
    if users[email]["password"] != _hash_password(password):
        return False, "Wrong password"
    save_session(email)
    return True, ""


def save_session(email: str):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"email": email}, f)


def load_session() -> dict | None:
    """Return full user dict if session exists"""
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            email = data.get("email")

        if not email:
            return None

        users = load_users()

        return users.get(email)

    except Exception:
        return None


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def get_current_user() -> dict | None:
    email = load_session()
    if not email:
        return None
    users = load_users()
    return users.get(email)