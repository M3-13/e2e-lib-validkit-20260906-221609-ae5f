"""Tests für validkit.clamp.clamp."""

import pytest

from validkit.clamp import clamp


def test_value_within_range_is_unchanged():
    assert clamp(5, 0, 10) == 5


def test_value_below_range_is_clamped_to_low():
    assert clamp(-3, 0, 10) == 0


def test_value_above_range_is_clamped_to_high():
    assert clamp(15, 0, 10) == 10


def test_low_greater_than_high_raises_value_error():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def test_float_value_within_range_is_unchanged():
    assert clamp(5.5, 0.0, 10.0) == 5.5


def test_float_value_below_range_is_clamped_to_low():
    assert clamp(-3.5, 0.0, 10.0) == 0.0


def test_float_value_above_range_is_clamped_to_high():
    assert clamp(15.5, 0.0, 10.0) == 10.0


def test_float_bounds_also_raise_value_error_when_reversed():
    with pytest.raises(ValueError):
        clamp(5.0, 10.0, 0.0)


def test_int_input_returns_int():
    result = clamp(5, 0, 10)
    assert isinstance(result, int)
    result = clamp(15, 0, 10)
    assert isinstance(result, int)


def test_float_input_returns_float():
    result = clamp(5.0, 0, 10)
    assert isinstance(result, float)
    result = clamp(5.5, 0.0, 10.0)
    assert isinstance(result, float)


@pytest.mark.parametrize("value", ["5", None, [5]])
def test_non_numeric_value_raises_type_error(value):
    with pytest.raises(TypeError):
        clamp(value, 0, 10)


@pytest.mark.parametrize("low", ["0", None, [0]])
def test_non_numeric_low_raises_type_error(low):
    with pytest.raises(TypeError):
        clamp(5, low, 10)


@pytest.mark.parametrize("high", ["10", None, [10]])
def test_non_numeric_high_raises_type_error(high):
    with pytest.raises(TypeError):
        clamp(5, 0, high)


def test_bool_is_rejected_as_non_numeric():
    with pytest.raises(TypeError):
        clamp(True, 0, 10)
