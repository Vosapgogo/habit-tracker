import datetime
import types

import pytest

import models.user_session as us
from pages.utils.errors import DataStorageError, UserNotFoundError, ValidationError

EMAIL = "tester1@gmail.com"
PASSWORD = "secret1"
GHOST = "ghost01@gmail.com"


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Point the storage layer at a temp dir so tests never touch the real users.json."""
    monkeypatch.setattr(us, "USERS_FILE", str(tmp_path / "users.json"))
    monkeypatch.setattr(us, "SESSION_FILE", str(tmp_path / "session.json"))


@pytest.fixture
def user():
    us.register_user("Alice", EMAIL, PASSWORD)
    return EMAIL


@pytest.fixture
def set_today(monkeypatch):
    """Freeze 'today' inside the storage layer; call again to move the clock."""

    def _set(iso_day):
        frozen = datetime.date.fromisoformat(iso_day)

        class FrozenDate(datetime.date):
            @classmethod
            def today(cls):
                return frozen

        monkeypatch.setattr(us, "datetime", types.SimpleNamespace(date=FrozenDate))

    return _set


def add_habit(email=EMAIL, name="Read", goal="Read 10 pages", period=7, habit_type="Everyday"):
    us.create_goal_habit(email, goal, name, period, habit_type)
    data = us.load_users()[email]
    return data["habits"][-1], data["goals"][-1]


def habit_by_id(habit_id, email=EMAIL):
    return next(h for h in us.load_users()[email]["habits"] if h["id"] == habit_id)


def goal_for(habit_id, email=EMAIL):
    return next(g for g in us.load_users()[email]["goals"] if g["habit_id"] == habit_id)


# Password hashing
def test_hash_password_is_deterministic_sha256_hex():
    assert us.hash_password("abc123") == us.hash_password("abc123")
    assert len(us.hash_password("abc123")) == 64
    assert us.hash_password("abc123") != us.hash_password("abc124")


# Registration
def test_register_stores_hashed_password_not_plaintext():
    us.register_user("Alice", EMAIL, PASSWORD)
    stored = us.load_users()[EMAIL]["password"]
    assert stored == us.hash_password(PASSWORD)
    assert stored != PASSWORD


def test_register_creates_empty_profile_and_logs_user_in():
    us.register_user("Alice", EMAIL, PASSWORD)
    data = us.load_users()[EMAIL]
    assert data["name"] == "Alice"
    assert data["habits"] == []
    assert data["goals"] == []
    assert us.load_session()["email"] == EMAIL


def test_register_rejects_duplicate_email(user):
    with pytest.raises(ValidationError, match="already registered"):
        us.register_user("Bob", user, "another1")


def test_register_strips_surrounding_whitespace():
    us.register_user("  Alice ", f" {EMAIL} ", PASSWORD)
    assert us.load_users()[EMAIL]["name"] == "Alice"


# Login
def test_login_succeeds_with_correct_credentials(user):
    us.clear_session()
    assert us.login_user(EMAIL, PASSWORD) is True
    assert us.load_session()["email"] == EMAIL


def test_login_rejects_unknown_email():
    with pytest.raises(ValidationError, match="Email not found"):
        us.login_user("nobody1@gmail.com", PASSWORD)


def test_login_rejects_wrong_password_and_opens_no_session(user):
    us.clear_session()
    with pytest.raises(ValidationError, match="Wrong password"):
        us.login_user(EMAIL, "wrong123")
    assert us.load_session() is None


# Account update / delete
def test_update_user_moves_record_when_email_changes(user):
    add_habit()
    us.update_user(EMAIL, "Alicia", "alicia99@gmail.com", "")
    users = us.load_users()
    assert EMAIL not in users
    moved = users["alicia99@gmail.com"]
    assert moved["name"] == "Alicia"
    assert moved["email"] == "alicia99@gmail.com"
    assert len(moved["habits"]) == 1
    assert us.load_session()["email"] == "alicia99@gmail.com"


def test_update_user_keeps_password_when_new_one_is_empty(user):
    old_hash = us.load_users()[EMAIL]["password"]
    us.update_user(EMAIL, "Alice", EMAIL, "")
    assert us.load_users()[EMAIL]["password"] == old_hash


def test_update_user_rehashes_new_password(user):
    us.update_user(EMAIL, "Alice", EMAIL, "newpass2")
    assert us.load_users()[EMAIL]["password"] == us.hash_password("newpass2")


def test_update_user_rejects_email_taken_by_another_user(user):
    us.register_user("Bob", "bobby123@gmail.com", "bobpass1")
    with pytest.raises(ValidationError, match="already registered"):
        us.update_user(EMAIL, "Alice", "bobby123@gmail.com", "")


def test_update_user_unknown_user_raises():
    with pytest.raises(UserNotFoundError):
        us.update_user(GHOST, "Ghost", GHOST, "")


def test_delete_user_removes_record(user):
    assert us.delete_user(EMAIL) is True
    assert EMAIL not in us.load_users()


def test_delete_user_unknown_user_raises():
    with pytest.raises(UserNotFoundError):
        us.delete_user(GHOST)


# Creating and deleting habits
def test_create_goal_habit_links_goal_to_habit(user):
    habit, goal = add_habit(period=14, habit_type="Weekdays")
    assert goal["habit_id"] == habit["id"]
    assert goal["total_days"] == 14
    assert goal["type"] == "Weekdays"
    assert goal["done_count"] == 0
    assert goal["progress"] == 0.0
    assert goal["done"] is False
    assert habit["done_date"] == []


def test_create_goal_habit_unknown_user_raises():
    with pytest.raises(UserNotFoundError):
        us.create_goal_habit(GHOST, "goal", "habit", 7, "Everyday")


def test_delete_habit_removes_habit_and_its_goal_only(user):
    keep, _ = add_habit(name="Keep")
    drop, _ = add_habit(name="Drop")
    us.delete_habit(user, drop["id"])
    data = us.load_users()[user]
    assert [h["id"] for h in data["habits"]] == [keep["id"]]
    assert [g["habit_id"] for g in data["goals"]] == [keep["id"]]


# Marking habits done / undone
def test_mark_done_records_today_and_advances_goal(user):
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    assert habit_by_id(habit["id"])["done_date"] == [us.get_today()]
    goal = goal_for(habit["id"])
    assert goal["done_count"] == 1
    assert goal["progress"] == 0.25


def test_mark_done_twice_on_same_day_counts_once(user):
    """Regression: repeated calls used to bump the goal counter every time."""
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    us.mark_habit_done(user, habit["id"])
    assert habit_by_id(habit["id"])["done_date"] == [us.get_today()]
    goal = goal_for(habit["id"])
    assert goal["done_count"] == 1
    assert goal["progress"] == 0.25


def test_mark_done_on_different_days_accumulates(user, set_today):
    set_today("2026-01-01")
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    set_today("2026-01-02")
    us.mark_habit_done(user, habit["id"])
    goal = goal_for(habit["id"])
    assert goal["done_count"] == 2
    assert goal["progress"] == 0.5


def test_goal_completes_when_target_is_reached(user):
    habit, _ = add_habit(period=1)
    us.mark_habit_done(user, habit["id"])
    goal = goal_for(habit["id"])
    assert goal["done"] is True
    assert goal["progress"] == 1.0
    assert goal["finished"] == us.get_today()


def test_mark_done_unknown_user_raises():
    with pytest.raises(UserNotFoundError):
        us.mark_habit_done(GHOST, "any-id")


def test_mark_undone_reverts_todays_completion(user):
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    us.mark_habit_undone(user, habit["id"])
    assert habit_by_id(habit["id"])["done_date"] == []
    goal = goal_for(habit["id"])
    assert goal["done_count"] == 0
    assert goal["progress"] == 0.0


def test_mark_undone_twice_on_same_day_reverts_once(user, set_today):
    set_today("2026-01-01")
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    set_today("2026-01-02")
    us.mark_habit_done(user, habit["id"])
    us.mark_habit_undone(user, habit["id"])
    us.mark_habit_undone(user, habit["id"])
    assert goal_for(habit["id"])["done_count"] == 1


def test_mark_undone_when_not_done_today_changes_nothing(user, set_today):
    set_today("2026-01-01")
    habit, _ = add_habit(period=4)
    us.mark_habit_done(user, habit["id"])
    set_today("2026-01-02")
    us.mark_habit_undone(user, habit["id"])
    assert goal_for(habit["id"])["done_count"] == 1


# Updating habits
def test_update_habit_renames_habit_and_goal(user):
    habit, _ = add_habit()
    us.update_habit(user, habit["id"], "Run", "Run 5 km", 30, "Weekends")
    assert habit_by_id(habit["id"])["name"] == "Run"
    goal = goal_for(habit["id"])
    assert goal["habit_name"] == "Run"
    assert goal["goal"] == "Run 5 km"
    assert goal["total_days"] == 30
    assert goal["type"] == "Weekends"


def test_update_habit_shrinking_period_below_progress_completes_goal(user, set_today):
    habit, _ = add_habit(period=7)
    for day in ("2026-01-01", "2026-01-02", "2026-01-03"):
        set_today(day)
        us.mark_habit_done(user, habit["id"])
    us.update_habit(user, habit["id"], "Read", "Read", 2, "Everyday")
    goal = goal_for(habit["id"])
    assert goal["done_count"] == 2
    assert goal["progress"] == 1.0
    assert goal["done"] is True
    assert goal["finished"] == "2026-01-03"


def test_update_habit_extending_period_reopens_finished_goal(user):
    habit, _ = add_habit(period=1)
    us.mark_habit_done(user, habit["id"])
    us.update_habit(user, habit["id"], "Read", "Read", 5, "Everyday")
    goal = goal_for(habit["id"])
    assert goal["done"] is False
    assert goal["finished"] == ""
    assert goal["progress"] == 0.2


# Session loading
def test_load_session_without_session_file_returns_none():
    assert us.load_session() is None


def test_clear_session_is_safe_to_call_twice(user):
    us.clear_session()
    us.clear_session()
    assert us.load_session() is None


def test_load_session_lists_everyday_habit_as_due_today(user):
    habit, _ = add_habit(habit_type="Everyday")
    assert [h["id"] for h in us.load_session()["today_habits"]] == [habit["id"]]


@pytest.mark.parametrize(
    "day, expected",
    [
        ("2026-01-05", ["Gym"]),  # Monday
        ("2026-01-10", ["Hike"]),  # Saturday
    ],
)
def test_load_session_offers_only_habits_scheduled_for_today(user, set_today, day, expected):
    set_today(day)
    add_habit(name="Gym", habit_type="Weekdays")
    add_habit(name="Hike", habit_type="Weekends")
    assert [h["name"] for h in us.load_session()["today_habits"]] == expected


def test_load_session_flags_habits_done_today(user):
    habit, _ = add_habit(period=7)
    assert us.load_session()["today_habits"][0]["done"] is False
    us.mark_habit_done(user, habit["id"])
    session = us.load_session()
    assert session["today_habits"][0]["done"] is True
    assert us.get_today() in session["all_completed_dates"]


def test_load_session_hides_habits_of_finished_goals(user):
    habit, _ = add_habit(period=1)
    us.mark_habit_done(user, habit["id"])
    session = us.load_session()
    assert session["habits"] == []
    assert session["today_habits"] == []
    assert [g["done"] for g in session["goals"]] == [True]


# Corrupted storage
def test_corrupted_users_file_raises_data_storage_error(tmp_path):
    (tmp_path / "users.json").write_text("{not valid json", encoding="utf-8")
    with pytest.raises(DataStorageError, match="corrupted"):
        us.load_users()


def test_corrupted_session_file_raises_data_storage_error(tmp_path):
    (tmp_path / "session.json").write_text("nope", encoding="utf-8")
    with pytest.raises(DataStorageError, match="corrupted"):
        us.load_session()


def test_session_without_email_raises_data_storage_error(tmp_path):
    (tmp_path / "session.json").write_text("{}", encoding="utf-8")
    with pytest.raises(DataStorageError, match="malformed"):
        us.load_session()
