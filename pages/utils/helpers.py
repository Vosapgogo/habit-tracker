import re
import time

from PySide6.QtGui import QPainterPath
from PySide6.QtCore import QRect
from functools import wraps

from pages.utils.errors import ValidationError


def rounded_rect_path(rect: QRect, r: int = 12):
    path = QPainterPath()
    path.addRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), r, r)
    return path


def strip_whitespaces(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cleaned_args = tuple(
            arg.strip() if isinstance(arg, str) else arg for arg in args
        )

        cleaned_kwargs = {
            k: (v.strip() if isinstance(v, str) else v) for k, v in kwargs.items()
        }

        return func(*cleaned_args, **cleaned_kwargs)

    return wrapper


def prevent_double_click(delay=1.0):
    def decorator(func):
        last_called = 0.0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            now = time.time()

            if now - last_called >= delay:
                last_called = now
                return func(*args, **kwargs)
            else:
                print(f"[UI SHIELD] Prevented double click on '{func.__name__}'")
                return None

        return wrapper

    return decorator


def check_streak_generator(habit_history):
    for day_record in habit_history:
        if day_record.get("is_completed", False):
            yield day_record
        else:
            break

@strip_whitespaces
def validate_account_data(name=None, email=None, pwd=None, pwd2=None):
    if name is not None:
        if not name:
            raise ValidationError("Please enter your name")
        if not re.match(r"^[A-Z]", name):
            raise ValidationError("First letter of the name must be in uppercase")

    if email is not None:
        if email != email.lower():
            raise ValidationError("Email must contain only lowercase letters")

        if not email or not email.endswith("@gmail.com"):
            raise ValidationError("Please enter a valid @gmail.com email")
        
        username = email.replace("@gmail.com", "")
        
        if not re.match(r"^[a-z0-9.]{6,30}$", username):
            raise ValidationError("Email name must be 6-30 characters long and contain only letters (a-z), numbers, and periods")

    if pwd is not None:
        if not pwd:
            raise ValidationError("Please enter your password")
        if len(pwd) < 6:
            raise ValidationError("Password must be at least 6 characters")
        if not re.match(r".*[A-Za-z].*", pwd):
            raise ValidationError("Password must contain at least 1 letter")
        if not re.match(r".*\d.*", pwd):
            raise ValidationError("Password must contain at least 1 number")

    if pwd is not None and pwd2 is not None:
        if pwd != pwd2:
            raise ValidationError("Passwords do not match")

    return True
