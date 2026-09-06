"""Geheimnis-Maskierung."""


def mask_secret(text: str, keep: int = 4) -> str:
    """Maskiert ein Geheimnis und lässt höchstens die letzten ``keep`` Zeichen sichtbar.

    Args:
        text: Das zu maskierende Geheimnis.
        keep: Anzahl der unverändert sichtbaren Zeichen am Ende.

    Returns:
        Die maskierte Zeichenkette, z. B. ``"geheim123"`` mit ``keep=3`` → ``"******123"``.
    """
    raise NotImplementedError
