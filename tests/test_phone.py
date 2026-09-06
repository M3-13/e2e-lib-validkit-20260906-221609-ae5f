"""Tests für validkit.phone.normalize_phone."""

import pytest

from validkit.phone import normalize_phone


def test_national_number_gets_country_code():
    assert normalize_phone("030 1234567", "DE") == "+49301234567"


def test_international_plus_input_is_kept():
    assert normalize_phone("+49 30 1234567", "DE") == "+49301234567"


def test_international_00_input_is_kept():
    assert normalize_phone("0049 30 1234567", "DE") == "+49301234567"


def test_country_code_is_case_insensitive():
    assert normalize_phone("030 1234567", "de") == "+49301234567"


def test_trunk_zero_is_dropped_for_national_number():
    assert normalize_phone("030-1234567", "DE") == "+49301234567"


def test_separators_are_removed():
    assert normalize_phone("+49 (30) 123/4567", "DE") == "+49301234567"


def test_country_code_is_not_added_to_international_number():
    assert normalize_phone("+43 1 234567", "DE") == "+431234567"


def test_unknown_country_code_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("030 1234567", "ZZ")


def test_empty_number_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("", "DE")


def test_whitespace_only_number_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("   ", "DE")


def test_invalid_characters_raise_value_error():
    with pytest.raises(ValueError):
        normalize_phone("030 1234ABC", "DE")


def test_too_long_input_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("0" * 50, "DE")


def test_too_many_digits_raise_value_error():
    with pytest.raises(ValueError):
        normalize_phone("12345678901234567", "DE")


def test_non_string_text_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone(301234567, "DE")  # type: ignore


def test_non_string_country_code_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone("030 1234567", 49)  # type: ignore


@pytest.mark.parametrize(
    ("text", "country_code"),
    [
        ("030 1234ABC", "DE"),
        ("030 1234567", "ZZ"),
        ("0" * 50, "DE"),
    ],
)
def test_error_messages_never_contain_input(text, country_code):
    with pytest.raises(ValueError) as exc:
        normalize_phone(text, country_code)
    assert text not in str(exc.value)
