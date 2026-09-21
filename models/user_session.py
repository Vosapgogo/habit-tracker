from functools import wraps
import json
import os
import datetime
import uuid
import hashlib

from pages.utils.errors import UserNotFoundError, ValidationError, DataStorageError
from pages.utils.helpers import strip_whitespaces

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "users.json")
SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "session.json")


def get_today():
    return str(datetime.date.today())


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def log_habit_count(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        email = kwargs.get("email")
        if not email and len(args) > 0:
            email = args[0]

        if isinstance(email, str) and "@" in email:
            users = load_users()
            if email in users:
                habit_count = len(users[email].get("habits", []))

                print("\n" + "-" * 60)
                print(f"[ACTION] '{func.__name__}' executed successfully.")
                print(f"[UPDATE] User '{email}' now has {habit_count} habit(s).")
                print("-" * 60 + "\n")

        return result

    return wrapper


# User actions
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise DataStorageError(
                "users.json is corrupted or contains invalid JSON"
            ) from e
        except OSError as e:
            raise DataStorageError("Unable to read users.json") from e
    return {}


def save_users(users):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise DataStorageError("Unable to write to users.json") from e


@strip_whitespaces
def register_user(name, email, password):
    users = load_users()
    if email in users:
        raise ValidationError("Email already registered")

    users[email] = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "habits": [],
        "goals": [],
    }
    save_users(users)
    save_session(email)
    return True


@strip_whitespaces
def login_user(email, password):
    users = load_users()
    if email not in users:
        raise ValidationError("Email not found")

    if users[email]["password"] != hash_password(password):
        raise ValidationError("Wrong password")

    save_session(email)
    return True


@strip_whitespaces
def update_user(old_email, new_name, new_email, new_password):
    users = load_users()

    if old_email not in users:
        raise UserNotFoundError()

    if old_email != new_email and new_email in users:
        raise ValidationError("Email already registered")

    user_data = users[old_email]

    user_data["name"] = new_name
    user_data["email"] = new_email
    if new_password:
        user_data["password"] = hash_password(new_password)

    if old_email != new_email:
        users[new_email] = user_data
        del users[old_email]

    save_users(users)
    save_session(new_email)

    return True


def delete_user(email):
    users = load_users()

    if email not in users:
        raise UserNotFoundError()

    del users[email]

    save_users(users)

    return True


def get_current_user():
    return load_session()


# Habit actions
@log_habit_count
@strip_whitespaces
def create_goal_habit(email, goal, habit_name, period, habit_type):
    users = load_users()
    if email not in users:
        raise UserNotFoundError()

    habit_id = str(uuid.uuid4())
    today = get_today()

    new_goal = {
        "id": str(uuid.uuid4()),
        "goal": goal,
        "habit_id": habit_id,
        "habit_name": habit_name,
        "type": habit_type,
        "total_days": period,
        "progress": 0.0,
        "done_count": 0,
        "created_date": today,
        "finished": "",
        "done": False,
    }
    new_habit = {
        "id": habit_id,
        "name": habit_name,
        "created_date": today,
        "done_date": [],
        "done": False,
    }

    users[email]["goals"].append(new_goal)
    users[email]["habits"].append(new_habit)
    save_users(users)
    return True


def mark_habit_done(email, habit_id):
    users = load_users()
    if email not in users:
        raise UserNotFoundError()

    today = get_today()
    newly_marked = False

    for habit in users[email]["habits"]:
        if habit.get("id") == habit_id and today not in habit["done_date"]:
            habit["done_date"].append(today)
            newly_marked = True

    # Advance the goal only if today was actually recorded above
    if newly_marked:
        for goal in users[email]["goals"]:
            if goal.get("habit_id") == habit_id and not goal.get("done"):
                goal["done_count"] += 1
                goal["progress"] = round(goal["done_count"] / goal["total_days"], 2)
                if goal["done_count"] >= goal["total_days"]:
                    goal["done"] = True
                    goal["finished"] = today

    save_users(users)


def is_done_today(habit):
    return get_today() in habit.get("done_date", [])


def mark_habit_undone(email, habit_id):
    users = load_users()
    if email not in users:
        raise UserNotFoundError()

    today = get_today()
    was_marked = False

    for habit in users[email]["habits"]:
        if habit.get("id") == habit_id and today in habit["done_date"]:
            habit["done_date"].remove(today)
            was_marked = True

    # Roll the goal back only if today's completion was actually removed above
    if was_marked:
        for goal in users[email]["goals"]:
            if goal.get("habit_id") == habit_id and goal.get("done_count", 0) > 0:
                goal["done_count"] -= 1
                goal["progress"] = round(goal["done_count"] / goal["total_days"], 2)
                goal["done"] = False
                goal["finished"] = ""

    save_users(users)


@log_habit_count
def delete_habit(email, habit_id):
    users = load_users()
    if email not in users:
        raise UserNotFoundError()

    users[email]["habits"] = [
        habit for habit in users[email]["habits"] if habit.get("id") != habit_id
    ]
    users[email]["goals"] = [
        goal for goal in users[email]["goals"] if goal.get("habit_id") != habit_id
    ]
    save_users(users)
    return True


@strip_whitespaces
def update_habit(email, habit_id, new_name, new_goal, new_period, new_type):
    users = load_users()
    if email not in users:
        raise UserNotFoundError()

    for habit in users[email]["habits"]:
        if habit.get("id") == habit_id:
            habit["name"] = new_name

    for goal in users[email]["goals"]:
        if goal.get("habit_id") == habit_id:
            goal["goal"] = new_goal
            goal["habit_name"] = new_name
            goal["total_days"] = new_period
            goal["type"] = new_type

            if goal["done_count"] > new_period:
                goal["done_count"] = new_period

            goal["progress"] = (
                round(goal["done_count"] / new_period, 2) if new_period else 0.0
            )

            if goal["done_count"] >= new_period:
                goal["done"] = True
                goal["finished"] = get_today()
            else:
                goal["done"] = False
                goal["finished"] = ""

    save_users(users)
    return True


# Session actions
def save_session(email):
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"email": email}, f)
    except OSError as e:
        raise DataStorageError("Unable to write to session.json") from e


def load_session():
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise DataStorageError(
            "session.json is corrupted or contains invalid JSON"
        ) from e
    except OSError as e:
        raise DataStorageError("Unable to read session.json") from e

    email = data.get("email")
    if not email:
        raise DataStorageError("session.json is malformed: missing email")

    users = load_users()
    user = users.get(email)
    if user:
        user["email"] = email
        today = get_today()

        current_weekday = datetime.date.today().weekday()

        finished_goal_habit_ids = {
            g.get("habit_id")
            for g in user.get("goals", [])
            if g.get("done", True) is True
        }

        habit_types = {}
        for g in user.get("goals", []):
            habit_types[g.get("habit_id")] = g.get("type", "Everyday")

        def is_active_today(h_type):
            match h_type:
                case "Everyday":
                    return True
                case "Weekdays" if current_weekday < 5:
                    return True
                case "Weekends" if current_weekday >= 5:
                    return True
                case _:
                    return False

        # Streak
        valid_habits = []
        today_habits = []

        all_dates = set()
        for h in user.get("habits", []):
            all_dates.update(h.get("done_date", []))
        user["all_completed_dates"] = list(all_dates)

        for h in user.get("habits", []):
            if h.get("id") in finished_goal_habit_ids:
                continue

            if h.get("created_date", today) <= today:
                valid_habits.append(h)

                h_type = habit_types.get(h.get("id"), "Everyday")
                if is_active_today(h_type):
                    today_habits.append(h)

        user["habits"] = valid_habits
        user["today_habits"] = today_habits

        user["goals"] = sorted(
            [g for g in user.get("goals", []) if g.get("created_date", today) <= today],
            key=lambda x: x.get("done", False),
        )

        for habit in user.get("habits", []):
            habit["done"] = is_done_today(habit)

    return user


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
