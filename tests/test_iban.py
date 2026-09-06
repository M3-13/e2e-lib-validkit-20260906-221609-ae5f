"""Tests für die IBAN-Validierung."""

import pytest

from validkit import is_valid_iban


def test_valid_iban_with_spaces_returns_true():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_valid_iban_without_spaces_returns_true():
    assert is_valid_iban("DE89370400440532013000") is True


def test_iban_with_wrong_check_digit_returns_false():
    assert is_valid_iban("DE00 3704 0044 0532 0130 00") is False


def test_iban_with_invalid_characters_returns_false():
    assert is_valid_iban("DE89 3704 0044 0532 0130 0!") is False
    assert is_valid_iban("DE89-3704-0044-0532-0130-00") is False


def test_iban_with_lowercase_letters_returns_false():
    assert is_valid_iban("de89 3704 0044 0532 0130 00") is False


def test_iban_longer_than_34_characters_returns_false():
    assert is_valid_iban("DE89" + "0" * 31) is False


def test_empty_string_returns_false():
    assert is_valid_iban("") is False


def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(123)


def test_non_string_none_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(None)
