"""Wertbegrenzung."""


def clamp(value: int | float, low: int | float, high: int | float) -> int | float:
    """Begrenzt ``value`` auf den Bereich ``[low, high]``.

    Args:
        value: Der zu begrenzende Wert.
        low: Untere Grenze.
        high: Obere Grenze (muss ``>= low`` sein).

    Returns:
        ``value``, wenn innerhalb des Bereichs, sonst ``low`` bzw. ``high``.
    """
    raise NotImplementedError
