import pytest

from pages.utils.errors import ValidationError
from pages.utils.helpers import validate_account_data

VALID_NAME = "Alice"
VALID_EMAIL = "alice123@gmail.com"
VALID_PWD = "secret1"


def test_accepts_valid_data():
    assert validate_account_data(VALID_NAME, VALID_EMAIL, VALID_PWD, VALID_PWD) is True


def test_only_supplied_fields_are_validated():
    # Log-in checks email + password only; other callers pass just one field
    assert validate_account_data(email=VALID_EMAIL, pwd=VALID_PWD) is True
    assert validate_account_data(name=VALID_NAME) is True


def test_surrounding_whitespace_is_ignored():
    assert (
        validate_account_data(" Alice ", " alice123@gmail.com ", " secret1 ", " secret1 ")
        is True
    )


# Name
@pytest.mark.parametrize(
    "name, message",
    [
        ("", "enter your name"),
        ("   ", "enter your name"),
        ("alice", "uppercase"),
        ("1lice", "uppercase"),
    ],
)
def test_rejects_invalid_name(name, message):
    with pytest.raises(ValidationError, match=message):
        validate_account_data(name=name)


# Email
@pytest.mark.parametrize(
    "email, message",
    [
        ("Alice123@gmail.com", "lowercase"),
        ("", "valid @gmail.com"),
        ("alice123", "valid @gmail.com"),
        ("alice123@yahoo.com", "valid @gmail.com"),
        ("abcde@gmail.com", "6-30 characters"),
        ("a" * 31 + "@gmail.com", "6-30 characters"),
        ("alice_123@gmail.com", "6-30 characters"),
    ],
)
def test_rejects_invalid_email(email, message):
    with pytest.raises(ValidationError, match=message):
        validate_account_data(email=email)


@pytest.mark.parametrize("username", ["a" * 6, "a" * 30, "a.b.c.1.2.3"])
def test_accepts_email_username_at_boundaries(username):
    assert validate_account_data(email=f"{username}@gmail.com") is True


# Password
@pytest.mark.parametrize(
    "pwd, message",
    [
        ("", "enter your password"),
        ("ab1", "at least 6 characters"),
        ("123456", "at least 1 letter"),
        ("abcdef", "at least 1 number"),
    ],
)
def test_rejects_weak_password(pwd, message):
    with pytest.raises(ValidationError, match=message):
        validate_account_data(pwd=pwd)


def test_rejects_mismatched_confirmation():
    with pytest.raises(ValidationError, match="do not match"):
        validate_account_data(pwd="secret1", pwd2="secret2")
