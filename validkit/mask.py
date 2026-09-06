"""Geheimnis-Maskierung."""


def mask_secret(text: str, keep: int = 4) -> str:
    """Maskiert ein Geheimnis und lässt höchstens die letzten ``keep`` Zeichen sichtbar.

    Args:
        text: Das zu maskierende Geheimnis.
        keep: Anzahl der unverändert sichtbaren Zeichen am Ende.

    Returns:
        Die maskierte Zeichenkette, z. B. ``"geheim123"`` mit ``keep=3`` → ``"******123"``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(keep, int):
        raise TypeError("keep must be an integer")
    if keep < 0:
        raise ValueError("keep must be a non-negative integer")
    if keep > len(text):
        raise ValueError("keep must not exceed the length of the text")
    return "*" * (len(text) - keep) + text[len(text) - keep :]
