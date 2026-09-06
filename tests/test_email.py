"""Unit-Tests für die E-Mail-Validierung."""

import pytest

from validkit.email import is_valid_email


@pytest.mark.parametrize(
    "address",
    [
        "user@example.com",
        "first.last@example.com",
        "user+tag@example.org",
        "user_name@sub.example.co.uk",
        "user-name@example.com",
        "user%name@example.com",
        "a@b.co",
    ],
)
def test_valid_addresses_return_true(address):
    assert is_valid_email(address) is True


@pytest.mark.parametrize(
    "address",
    [
        "not-an-email",
        "user@",
        "@example.com",
        "user@example",
        "user@example.c",
        "user example@example.com",
        "user@example..com",
        "user@.example.com",
    ],
)
def test_invalid_addresses_return_false(address):
    assert is_valid_email(address) is False


def test_empty_input_returns_false():
    assert is_valid_email("") is False


def test_missing_at_returns_false():
    assert is_valid_email("userexample.com") is False


def test_missing_domain_dot_returns_false():
    assert is_valid_email("user@example") is False


def test_length_at_254_chars_is_valid():
    address = "a" * 242 + "@example.com"
    assert len(address) == 254
    assert is_valid_email(address) is True


def test_length_over_254_chars_is_invalid():
    address = "a" * 243 + "@example.com"
    assert len(address) == 255
    assert is_valid_email(address) is False


@pytest.mark.parametrize("value", [123, 3.14, None, ["user@example.com"], b"user@example.com"])
def test_non_string_input_raises_type_error(value):
    with pytest.raises(TypeError):
        is_valid_email(value)


def test_type_error_message_hides_input_and_is_meaningful():
    with pytest.raises(TypeError) as excinfo:
        is_valid_email(123)
    message = str(excinfo.value)
    assert "123" not in message
    assert message.strip() != ""
