"""Slug-Erzeugung."""


def slugify(text: str) -> str:
    """Erzeugt aus ``text`` einen URL-freundlichen Slug.

    Args:
        text: Die zu verarbeitende Zeichenkette.

    Returns:
        Der Slug in Kleinbuchstaben, z. B. ``"Über das Wetter!"`` → ``"uber-das-wetter"``.
    """
    raise NotImplementedError
