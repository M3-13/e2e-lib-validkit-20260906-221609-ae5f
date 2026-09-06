"""Import- und Signaturtests für die öffentliche validkit-API."""

import inspect

from validkit import (
    clamp,
    is_valid_email,
    is_valid_iban,
    is_valid_isbn13,
    luhn_check,
    mask_secret,
    normalize_phone,
    slugify,
    strip_accents,
)


def test_all_nine_functions_are_importable_and_callable():
    for fn in (
        is_valid_email,
        luhn_check,
        is_valid_iban,
        is_valid_isbn13,
        normalize_phone,
        strip_accents,
        mask_secret,
        slugify,
        clamp,
    ):
        assert callable(fn)


def test_is_valid_email_signature():
    sig = inspect.signature(is_valid_email)
    assert list(sig.parameters) == ["text"]
    assert sig.parameters["text"].annotation is str
    assert sig.return_annotation is bool


def test_luhn_check_signature():
    sig = inspect.signature(luhn_check)
    assert list(sig.parameters) == ["digits"]
    assert sig.parameters["digits"].annotation is str
    assert sig.return_annotation is bool


def test_is_valid_iban_signature():
    sig = inspect.signature(is_valid_iban)
    assert list(sig.parameters) == ["text"]
    assert sig.parameters["text"].annotation is str
    assert sig.return_annotation is bool


def test_is_valid_isbn13_signature():
    sig = inspect.signature(is_valid_isbn13)
    assert list(sig.parameters) == ["text"]
    assert sig.parameters["text"].annotation is str
    assert sig.return_annotation is bool


def test_normalize_phone_signature():
    sig = inspect.signature(normalize_phone)
    assert list(sig.parameters) == ["text", "country_code"]
    assert sig.parameters["text"].annotation is str
    assert sig.parameters["country_code"].annotation is str
    assert sig.return_annotation is str


def test_strip_accents_signature():
    sig = inspect.signature(strip_accents)
    assert list(sig.parameters) == ["text"]
    assert sig.parameters["text"].annotation is str
    assert sig.return_annotation is str


def test_mask_secret_signature():
    sig = inspect.signature(mask_secret)
    assert list(sig.parameters) == ["text", "keep"]
    assert sig.parameters["text"].annotation is str
    assert sig.parameters["keep"].default == 4
    assert sig.return_annotation is str


def test_slugify_signature():
    sig = inspect.signature(slugify)
    assert list(sig.parameters) == ["text"]
    assert sig.parameters["text"].annotation is str
    assert sig.return_annotation is str


def test_clamp_signature():
    sig = inspect.signature(clamp)
    assert list(sig.parameters) == ["value", "low", "high"]
    assert sig.parameters["value"].annotation == int | float
    assert sig.parameters["low"].annotation == int | float
    assert sig.parameters["high"].annotation == int | float
    assert sig.return_annotation == int | float
