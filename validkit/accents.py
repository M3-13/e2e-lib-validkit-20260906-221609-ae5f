"""Akzent- und Diakritika-Entfernung."""

import unicodedata


def strip_accents(text: str) -> str:
    """Entfernt Akzente und Diakritika aus ``text``.

    Args:
        text: Die zu verarbeitende Zeichenkette.

    Returns:
        Die Zeichenkette ohne Akzente/Diakritika (z. B. ``"é"`` → ``"e"``).

    Raises:
        TypeError: Wenn ``text`` kein ``str`` ist.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))
