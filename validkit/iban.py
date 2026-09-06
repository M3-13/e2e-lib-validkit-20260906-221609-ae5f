"""IBAN-Validierung."""


def is_valid_iban(text: str) -> bool:
    """Prüft, ob ``text`` eine gültige IBAN ist.

    Args:
        text: Die zu prüfende Zeichenkette (Leerzeichen sind erlaubt).

    Returns:
        ``True``, wenn ``text`` eine gültige IBAN ist, sonst ``False``.
    """
    raise NotImplementedError
