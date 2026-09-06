"""Tests für die Akzent- und Diakritika-Entfernung."""

import pytest

from validkit.accents import strip_accents


def test_strip_accents_muenchen_cafe():
    assert strip_accents("München café") == "Munchen cafe"


def test_strip_accents_acute_e():
    assert strip_accents("é") == "e"


def test_strip_accents_umlaut_u():
    assert strip_accents("ü") == "u"


def test_strip_accents_unaccented_unchanged():
    assert strip_accents("abc XYZ 123") == "abc XYZ 123"


def test_strip_accents_empty_string():
    assert strip_accents("") == ""


def test_strip_accents_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        strip_accents(123)  # type: ignore[arg-type]
