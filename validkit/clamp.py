"""Wertbegrenzung."""


def clamp(value: int | float, low: int | float, high: int | float) -> int | float:
    """Begrenzt ``value`` auf den Bereich ``[low, high]``.

    Args:
        value: Der zu begrenzende Wert.
        low: Untere Grenze.
        high: Obere Grenze (muss ``>= low`` sein).

    Returns:
        ``value``, wenn innerhalb des Bereichs, sonst ``low`` bzw. ``high``.
        Der Rückgabetyp folgt dem Typ von ``value`` (``int`` bleibt ``int``,
        ``float`` bleibt ``float``).

    Raises:
        TypeError: Wenn eine der Eingaben kein ``int``/``float`` ist.
        ValueError: Wenn ``low`` größer als ``high`` ist.
    """
    for name, operand in (("value", value), ("low", low), ("high", high)):
        if isinstance(operand, bool) or not isinstance(operand, (int, float)):
            raise TypeError(f"{name} must be an int or a float")

    if low > high:
        raise ValueError("low must not be greater than high")

    result = min(max(value, low), high)
    if isinstance(value, int):
        return int(result)
    return float(result)
