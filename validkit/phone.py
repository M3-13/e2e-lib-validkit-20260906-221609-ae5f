"""Telefonnummer-Normalisierung."""

import re

# Zuordnung gebräuchlicher ISO-3166-1-alpha-2-Ländercodes zu ihrer
# internationalen Ländervorwahl (E.164).
_COUNTRY_DIAL_CODES: dict[str, str] = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
    "FR": "33",
    "GB": "44",
    "IT": "39",
    "ES": "34",
    "NL": "31",
    "BE": "32",
    "PL": "48",
    "US": "1",
}

# Dokumentierte Maximallänge der Roheingabe in Zeichen. Sie wird VOR jedem
# regulären Ausdruck geprüft und begrenzt den Aufwand, den die Regex an einer
# unvertrauenswürdigen Zeichenkette treiben kann (ReDoS-Schutz). Eine E.164-
# Nummer hat höchstens 15 Ziffern; selbst vollständig formatierte Eingaben mit
# Trennzeichen bleiben deutlich unter diesem Wert.
_MAX_INPUT_LENGTH = 40

# E.164 begrenzt eine internationale Nummer auf 15 Ziffern (inkl. Vorwahl).
_MAX_DIGITS = 15

# Erlaubt sind Ziffern, übliche Trennzeichen und ein einzelnes führendes "+".
# Keine verschachtelten Quantoren: ``\+?`` (optionales Plus) und eine einzige,
# mit ``*`` suffigierte Zeichenklasse.
_PHONE_PATTERN = re.compile(r"\+?[0-9][0-9 .()/\-]*")
_NON_DIGIT_PATTERN = re.compile(r"\D+")


def normalize_phone(text: str, country_code: str) -> str:
    """Normalisiert eine Telefonnummer in das internationale E.164-Format.

    Args:
        text: Die zu normalisierende Telefonnummer.
        country_code: Der zweistellige ISO-Ländercode (z. B. ``"DE"``).

    Returns:
        Die normalisierte Telefonnummer im Format ``+<Ländervorwahl><Nummer>``.

    Raises:
        TypeError: Wenn ein Argument nicht vom Typ ``str`` ist.
        ValueError: Bei leerer Nummer, unbekanntem Ländercode oder ungültigen
            Zeichen. Die Fehlermeldung enthält niemals die Eingabe.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(country_code, str):
        raise TypeError("country_code must be a string")

    text = text.strip()
    if not text:
        raise ValueError("phone number must not be empty")

    # Längenprüfung VOR jedem regulären Ausdruck.
    if len(text) > _MAX_INPUT_LENGTH:
        raise ValueError("phone number is too long")

    dial_code = _COUNTRY_DIAL_CODES.get(country_code.strip().upper())
    if dial_code is None:
        raise ValueError("unknown country code")

    if not _PHONE_PATTERN.fullmatch(text):
        raise ValueError("phone number contains invalid characters")

    digits = _NON_DIGIT_PATTERN.sub("", text)

    if text.startswith("+"):
        number = digits
    elif text.startswith("00"):
        number = digits[2:]
    else:
        if digits.startswith("0"):
            digits = digits[1:]
        number = dial_code + digits

    if not number:
        raise ValueError("phone number has no digits")
    if len(number) > _MAX_DIGITS:
        raise ValueError("phone number has too many digits")

    return "+" + number
