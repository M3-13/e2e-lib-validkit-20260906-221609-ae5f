"""Slug-Erzeugung."""

import re

from validkit.accents import strip_accents

# Maximallängenprüfung vor der Regex (AC-13): 2000 Zeichen genügen für
# jeden realen Slug und begrenzen den Aufwand der Normalisierung.
_MAX_LENGTH = 2000

_NON_WORD_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Erzeugt aus ``text`` einen URL-freundlichen Slug.

    Args:
        text: Die zu verarbeitende Zeichenkette.

    Returns:
        Der Slug in Kleinbuchstaben, z. B. ``"Über das Wetter!"`` → ``"uber-das-wetter"``.
        Ein leeres Ergebnis ergibt einen leeren String.

    Raises:
        TypeError: Wenn ``text`` kein ``str`` ist.
        ValueError: Wenn ``text`` die Maximallänge von ``_MAX_LENGTH`` überschreitet.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > _MAX_LENGTH:
        raise ValueError("text exceeds maximum length")

    lowered = strip_accents(text).lower()
    return _NON_WORD_RE.sub("-", lowered).strip("-")
