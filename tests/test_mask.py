"""Tests für die Geheimnis-Maskierung mask_secret."""

import pytest

from validkit.mask import mask_secret


def test_mask_secret_keeps_last_three_characters():
    assert mask_secret("geheim123", keep=3) == "******123"


def test_mask_secret_default_keep_is_four():
    assert mask_secret("geheim123") == "*****m123"


def test_mask_secret_keep_zero_masks_everything():
    assert mask_secret("geheim123", keep=0) == "*********"


def test_mask_secret_keep_equal_to_length_masks_nothing():
    assert mask_secret("abc", keep=3) == "abc"


def test_mask_secret_keep_greater_than_length_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("abc", keep=10)


def test_mask_secret_negative_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("geheim123", keep=-1)


def test_mask_secret_wrong_text_type_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret(12345, keep=3)


def test_mask_secret_wrong_keep_type_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret("geheim123", keep="3")


def test_error_messages_never_contain_the_input():
    for bad_keep, expected in [(10, ValueError), (-1, ValueError)]:
        with pytest.raises(expected) as exc_info:
            mask_secret("geheim123", keep=bad_keep)
        assert "geheim123" not in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        mask_secret("geheim123", keep="3")
    assert "geheim123" not in str(exc_info.value)
