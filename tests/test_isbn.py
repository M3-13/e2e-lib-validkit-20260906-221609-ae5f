"""Tests für die ISBN-13-Prüfung."""

import pytest

from validkit.isbn import is_valid_isbn13

VALID_ISBN13 = "9783161484100"


def test_valid_isbn13_plain():
    assert is_valid_isbn13(VALID_ISBN13) is True


def test_valid_isbn13_with_hyphens():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn13_with_spaces():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_valid_isbn13_mixed_separators():
    assert is_valid_isbn13("978-3 16-148410 0") is True


def test_wrong_check_digit_returns_false():
    assert is_valid_isbn13("9783161484101") is False


def test_wrong_length_returns_false():
    assert is_valid_isbn13("97831614841") is False


def test_too_many_digits_returns_false():
    assert is_valid_isbn13("97831614841001") is False


def test_non_numeric_characters_return_false():
    assert is_valid_isbn13("97831614841X0") is False


def test_empty_string_returns_false():
    assert is_valid_isbn13("") is False


def test_only_separators_return_false():
    assert is_valid_isbn13("---  ") is False


def test_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)  # type: ignore[arg-type]
