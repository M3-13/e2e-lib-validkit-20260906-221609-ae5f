"""Luhn-Prüfziffer."""


def luhn_check(digits: str) -> bool:
    """Prüft eine Ziffernfolge anhand des Luhn-Algorithmus.

    Leerzeichen und Bindestriche innerhalb der Eingabe sind erlaubt und werden
    vor der Prüfung entfernt.

    Args:
        digits: Die zu prüfende Ziffernfolge (Leerzeichen und Bindestriche sind erlaubt).

    Returns:
        ``True``, wenn die Prüfziffer gültig ist, sonst ``False``.

    Raises:
        TypeError: Wenn ``digits`` keine Zeichenkette ist.
        ValueError: Wenn ``digits`` leer ist oder nach dem Entfernen von
            Leerzeichen und Bindestrichen keine reine Ziffernfolge ergibt.
    """
    if not isinstance(digits, str):
        raise TypeError("Eingabe muss eine Zeichenkette sein")

    cleaned = digits.replace(" ", "").replace("-", "")

    if not cleaned:
        raise ValueError("Eingabe enthält keine Ziffern")
    if not cleaned.isdigit():
        raise ValueError("Eingabe enthält ungültige Zeichen")

    total = 0
    for index, char in enumerate(reversed(cleaned)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value

    return total % 10 == 0
