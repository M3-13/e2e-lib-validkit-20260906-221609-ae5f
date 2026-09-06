"""IBAN-Validierung."""

import re

_MAX_IBAN_LENGTH = 34

_IBAN_RE = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+")


def is_valid_iban(text: str) -> bool:
    """Prüft, ob ``text`` eine gültige IBAN ist.

    Args:
        text: Die zu prüfende Zeichenkette (Leerzeichen sind erlaubt).

    Returns:
        ``True``, wenn ``text`` eine gültige IBAN ist, sonst ``False``.

    Raises:
        TypeError: Wenn ``text`` kein ``str`` ist.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    normalized = text.replace(" ", "")

    if len(normalized) > _MAX_IBAN_LENGTH:
        return False

    if _IBAN_RE.fullmatch(normalized) is None:
        return False

    rearranged = normalized[4:] + normalized[:4]

    digits = "".join(str(ord(ch) - ord("A") + 10) if ch.isalpha() else ch for ch in rearranged)

    return int(digits) % 97 == 1
