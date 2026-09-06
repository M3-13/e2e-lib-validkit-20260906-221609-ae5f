"""ISBN-13-Prüfung."""


def is_valid_isbn13(text: str) -> bool:
    """Prüft, ob ``text`` eine gültige ISBN-13 ist.

    Bindestriche und Leerzeichen werden ignoriert. Nach deren Entfernung müssen
    genau 13 Ziffern übrig bleiben. Die Prüfziffer wird über die gewichtete
    Summe validiert (Gewichte 1-3-1-3-…), die durch 10 teilbar sein muss.

    Args:
        text: Die zu prüfende Zeichenkette (Bindestriche/Leerzeichen erlaubt).

    Returns:
        ``True``, wenn ``text`` eine gültige ISBN-13 ist, sonst ``False``.

    Raises:
        TypeError: Wenn ``text`` kein ``str`` ist.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    digits = text.replace("-", "").replace(" ", "")

    if len(digits) != 13 or not digits.isdigit():
        return False

    total = 0
    for index, char in enumerate(digits):
        weight = 1 if index % 2 == 0 else 3
        total += int(char) * weight

    return total % 10 == 0
