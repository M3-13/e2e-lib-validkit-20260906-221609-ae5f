"""IBAN-Validierung."""

import re

# Obergrenze ohne Leerzeichen; wird vor dem regulären Ausdruck geprüft (AC-13).
_MAX_IBAN_LENGTH = 34

# Ländercode -> zulässige IBAN-Gesamtlänge (SWIFT-Register). Unbekannte Codes
# werden abgelehnt.
_IBAN_LENGTHS: dict[str, int] = {
    "AD": 24,
    "AE": 23,
    "AL": 28,
    "AT": 20,
    "AZ": 28,
    "BA": 20,
    "BE": 16,
    "BG": 22,
    "BH": 22,
    "BR": 29,
    "CH": 21,
    "CR": 22,
    "CY": 28,
    "CZ": 24,
    "DE": 22,
    "DK": 18,
    "DO": 28,
    "EE": 20,
    "EG": 29,
    "ES": 24,
    "FI": 18,
    "FO": 18,
    "FR": 27,
    "GB": 22,
    "GE": 22,
    "GI": 23,
    "GL": 18,
    "GR": 27,
    "GT": 28,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IL": 23,
    "IQ": 23,
    "IS": 26,
    "IT": 27,
    "JO": 30,
    "KW": 30,
    "KZ": 20,
    "LB": 28,
    "LC": 32,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "MC": 27,
    "MD": 24,
    "ME": 22,
    "MK": 19,
    "MR": 27,
    "MT": 31,
    "MU": 30,
    "NL": 18,
    "NO": 15,
    "PK": 24,
    "PL": 28,
    "PS": 29,
    "PT": 25,
    "QA": 29,
    "RO": 24,
    "RS": 22,
    "SA": 24,
    "SC": 31,
    "SE": 24,
    "SI": 19,
    "SK": 24,
    "SM": 27,
    "ST": 25,
    "SV": 28,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "VA": 22,
    "VG": 24,
    "XK": 20,
}

_IBAN_RE = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+")


def is_valid_iban(text: str) -> bool:
    """Prüft, ob ``text`` eine gültige IBAN ist.

    Args:
        text: Die zu prüfende Zeichenkette (Leerzeichen sind erlaubt).

    Returns:
        ``True``, wenn ``text`` eine gültige IBAN ist, sonst ``False``.

    Raises:
        TypeError: Wenn ``text`` kein ``str`` ist.

    Die Prüfung umfasst: Buchstaben-/Ziffernformat, die zulässige Länge
    anhand des Ländercodes (unbekannte Ländercodes werden abgelehnt) sowie
    die Modulo-97-Prüfung nach Umstellung der ersten vier Zeichen ans Ende.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    normalized = text.replace(" ", "")

    if len(normalized) > _MAX_IBAN_LENGTH:
        return False

    if _IBAN_RE.fullmatch(normalized) is None:
        return False

    country_code = normalized[:2]
    expected_length = _IBAN_LENGTHS.get(country_code)
    if expected_length is None or len(normalized) != expected_length:
        return False

    rearranged = normalized[4:] + normalized[:4]

    digits = "".join(str(ord(ch) - ord("A") + 10) if ch.isalpha() else ch for ch in rearranged)

    return int(digits) % 97 == 1
