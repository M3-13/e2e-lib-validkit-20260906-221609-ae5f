"""E-Mail-Validierung."""

import re

# RFC 5321 begrenzt eine E-Mail-Adresse (lokal@domäne) auf maximal 254 Zeichen.
MAX_LENGTH = 254

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def is_valid_email(text: str) -> bool:
    """Prüft, ob ``text`` eine syntaktisch gültige E-Mail-Adresse ist.

    Geprüft werden ein lokaler Teil, ``@``, eine Domain mit mindestens einem
    Punkt sowie ausschließlich gültige Zeichen. Vor der Auswertung des
    regulären Ausdrucks wird die Maximallänge von 254 Zeichen geprüft.

    Args:
        text: Die zu prüfende Zeichenkette.

    Returns:
        ``True``, wenn ``text`` eine gültige E-Mail-Adresse ist, sonst ``False``.

    Raises:
        TypeError: Wenn ``text`` keine Zeichenkette ist.
    """
    if not isinstance(text, str):
        raise TypeError("is_valid_email() erwartet eine Zeichenkette (str)")
    if len(text) > MAX_LENGTH:
        return False
    if _EMAIL_RE.fullmatch(text) is None:
        return False
    local, domain = text.split("@", 1)
    local_ok = not (local.startswith(".") or local.endswith(".") or ".." in local)
    domain_ok = not (domain.startswith(".") or domain.endswith(".") or ".." in domain)
    return local_ok and domain_ok
