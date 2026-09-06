"""Tests für die Slug-Erzeugung."""

import pytest

from validkit.slug import slugify


def test_slugify_ueber_das_wetter():
    assert slugify("Über das Wetter!") == "uber-das-wetter"


def test_slugify_special_characters_replaced():
    assert slugify("Hallo, Welt!") == "hallo-welt"
    assert slugify("a@b#c$d") == "a-b-c-d"


def test_slugify_multiple_hyphens_collapsed():
    assert slugify("hello--world") == "hello-world"
    assert slugify("hello   world") == "hello-world"


def test_slugify_leading_trailing_hyphens_removed():
    assert slugify("-hello-world-") == "hello-world"
    assert slugify("!!!") == ""


def test_slugify_uppercase_lowered():
    assert slugify("Hello WORLD") == "hello-world"


def test_slugify_accents_removed():
    assert slugify("München café") == "munchen-cafe"


def test_slugify_digits_preserved():
    assert slugify("Version 2.0 Beta") == "version-2-0-beta"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        slugify(123)  # type: ignore[arg-type]


def test_slugify_too_long_raises_value_error():
    with pytest.raises(ValueError):
        slugify("a" * 2001)
