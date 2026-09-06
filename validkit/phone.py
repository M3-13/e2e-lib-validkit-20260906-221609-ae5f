"""Telefonnummer-Normalisierung."""


def normalize_phone(text: str, country_code: str) -> str:
    """Normalisiert eine Telefonnummer in das internationale E.164-Format.

    Args:
        text: Die zu normalisierende Telefonnummer.
        country_code: Der zweistellige ISO-Ländercode (z. B. ``"DE"``).

    Returns:
        Die normalisierte Telefonnummer im Format ``+<Ländervorwahl><Nummer>``.
    """
    raise NotImplementedError
