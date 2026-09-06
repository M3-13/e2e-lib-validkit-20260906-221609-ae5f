# validkit

**validkit** ist eine kleine, eigenständige Python-Bibliothek mit neun voneinander
unabhängigen, reinen Prüf- und Normalisierungsfunktionen. Sie nutzt ausschließlich
die Standardbibliothek, hat keine externen Laufzeit-Abhängigkeiten, keine CLI, keine
UI und keinen Netzwerkzugriff. Alle Funktionen sind typannotiert, einzeln nutzbar und
über die öffentliche API importierbar.

## Tech-Stack

- **Sprache**: Python
- **Runtime**: Python 3.10+
- **Tests**: pytest
- **Abhängigkeiten**: keine (nur Standardbibliothek)

## Installation

```bash
pip install -e .
```

## Ausführung / Tests

```bash
pytest
```

Für die Entwicklung mit pytest als einzige Entwicklungs-Abhängigkeit:

```bash
pip install -e ".[dev]"
pytest
```

## Funktionen

### `is_valid_email(text: str) -> bool`

Prüft, ob eine Zeichenkette eine syntaktisch gültige E-Mail-Adresse ist.

```python
>>> from validkit import is_valid_email
>>> is_valid_email('anna@example.com')
True
```

### `luhn_check(digits: str) -> bool`

Prüft eine Ziffernfolge anhand des Luhn-Algorithmus.

```python
>>> from validkit import luhn_check
>>> luhn_check('4111 1111 1111 1111')
True
```

### `is_valid_iban(text: str) -> bool`

Prüft, ob eine Zeichenkette eine gültige IBAN ist.

```python
>>> from validkit import is_valid_iban
>>> is_valid_iban('DE89 3704 0044 0532 0130 00')
True
```

### `is_valid_isbn13(text: str) -> bool`

Prüft, ob eine Zeichenkette eine gültige ISBN-13 ist.

```python
>>> from validkit import is_valid_isbn13
>>> is_valid_isbn13('978-3-16-148410-0')
True
```

### `normalize_phone(text: str, country_code: str) -> str`

Normalisiert eine Telefonnummer in das internationale E.164-Format.

```python
>>> from validkit import normalize_phone
>>> normalize_phone('030 1234567', 'DE')
'+49301234567'
```

### `strip_accents(text: str) -> str`

Entfernt Akzente und Diakritika aus einer Zeichenkette.

```python
>>> from validkit import strip_accents
>>> strip_accents('München café')
'Munchen cafe'
```

### `mask_secret(text: str, keep: int = 4) -> str`

Maskiert ein Geheimnis und lässt höchstens die letzten `keep` Zeichen sichtbar.

```python
>>> from validkit import mask_secret
>>> mask_secret('geheim123', keep=3)
'******123'
```

### `slugify(text: str) -> str`

Erzeugt aus einer Zeichenkette einen URL-freundlichen Slug.

```python
>>> from validkit import slugify
>>> slugify('Über das Wetter!')
'uber-das-wetter'
```

### `clamp(value: int | float, low: int | float, high: int | float) -> int | float`

Begrenzt einen Wert auf den Bereich `[low, high]`.

```python
>>> from validkit import clamp
>>> clamp(5, 0, 10)
5
```

## Feature-Liste

- `is_valid_email` — E-Mail-Syntaxprüfung
- `luhn_check` — Luhn-Prüfziffer
- `is_valid_iban` — IBAN-Validierung
- `is_valid_isbn13` — ISBN-13-Prüfung
- `normalize_phone` — Telefonnummer-Normalisierung (E.164)
- `strip_accents` — Akzent-/Diakritika-Entfernung
- `mask_secret` — Geheimnis-Maskierung
- `slugify` — Slug-Erzeugung
- `clamp` — Wertbegrenzung
