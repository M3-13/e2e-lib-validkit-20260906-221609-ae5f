"""Unit-Tests für validkit.luhn."""

import pytest

from validkit.luhn import luhn_check


@pytest.mark.parametrize(
    "digits",
    [
        "4111111111111111",
        "4111 1111 1111 1111",
        "4111-1111-1111-1111",
        "79927398713",
        "7992739871-3",
    ],
)
def test_luhn_check_accepts_valid_numbers(digits):
    assert luhn_check(digits) is True


@pytest.mark.parametrize(
    "digits",
    [
        "4111 1111 1111 1112",
        "4111111111111112",
        "79927398710",
        "79927398712",
        "49927398717",
        "1234 5678 9012 3456",
    ],
)
def test_luhn_check_rejects_manipulated_numbers(digits):
    assert luhn_check(digits) is False


@pytest.mark.parametrize(
    "digits",
    [
        "",
        "   ",
        "----",
        " - ",
    ],
)
def test_luhn_check_raises_value_error_on_empty_input(digits):
    with pytest.raises(ValueError):
        luhn_check(digits)


@pytest.mark.parametrize(
    "digits",
    [
        "4111 1111 1111 111x",
        "4111_1111_1111_1111",
        "abcdefgh",
        "41a1",
    ],
)
def test_luhn_check_raises_value_error_on_non_numeric_input(digits):
    with pytest.raises(ValueError):
        luhn_check(digits)


@pytest.mark.parametrize(
    "digits",
    [
        None,
        4111111111111111,
        ["4111", "1111"],
        42.0,
    ],
)
def test_luhn_check_raises_type_error_on_wrong_type(digits):
    with pytest.raises(TypeError):
        luhn_check(digits)


@pytest.mark.parametrize(
    "digits",
    [
        "   ",
        "4111_1111_1111_1111",
        "411111111111111x",
        "secret",
    ],
)
def test_luhn_check_error_messages_do_not_leak_input(digits):
    with pytest.raises(ValueError) as exc_info:
        luhn_check(digits)
    assert digits not in str(exc_info.value)
