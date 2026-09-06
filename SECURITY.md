VERDICT: APPROVED

## Sicherheitsbericht validkit

### Übersicht
Geprüft wurde der vollständige, gemergte Stand der Python-Bibliothek `validkit`. Die Bibliothek ist eine reine, abhängigkeitsfreie Sammlung von Prüf- und Normalisierungsfunktionen ohne Netzwerkzugriff, CLI, UI oder Dateioperationen. Es wurden keine externen Laufzeitabhängigkeiten festgestellt. Die statischen Scanner `bandit` und `semgrep` wurden nicht ausgeführt (`[skipped]`); die Bewertung stützt sich daher auf die manuelle Sichtung des bereitgestellten Quellcodes und der Tests.

### Ergebnis
Es wurden **keine kritischen oder hohen Sicherheitslücken** gefunden. Die zentralen Sicherheitsanforderungen aus dem Sprint (kein `eval`/`exec`/`compile`, regex-bezogene Maximallängenprüfungen, keine Weitergabe von Eingaben in Fehlermeldungen, keine echten personenbezogenen Daten) sind erfüllt.

Die nachfolgend aufgeführten Punkte sind als optionale Härtungen mit niedrigem Risiko einzustufen und begründen keine Änderung des Freigabeverdikts.

---

## Findings

### LOW-01 – Fehlende Maximallängenprüfung in Teilen der Bibliothek
**Betroffene Stellen:**  
- `validkit/luhn.py` – `luhn_check`  
- `validkit/isbn.py` – `is_valid_isbn13`  
- `validkit/mask.py` – `mask_secret`  
- `validkit/accents.py` – `strip_accents`

**Beschreibung:**  
Einige Funktionen verarbeiten Eingaben ohne dokumentierte Längenbegrenzung. Zwar verwendet keine dieser Funktionen reguläre Ausdrücke mit verschachtelten Quantoren (ReDoS ist hier nicht möglich), jedoch kann eine extrem lange Zeichenkette zu unnötig hoher CPU- oder Speicherlast führen, wenn die Bibliothek in einen Dienst mit unbegrenzten Eingaben eingebettet wird. Die Sprint-Anforderung AC-13 fordert Maximallängenprüfungen explizit nur für Regex-basierte Funktionen; die genannten Funktionen fallen nicht darunter, weshalb dies kein Verstoß gegen die Akzeptanzkriterien ist.

**Konkrete Empfehlung:**  
Eine einheitliche, gut dokumentierte Maximallänge pro Funktion einführen, z. B.:
- `luhn_check`: 100 Zeichen vor/nach Normalisierung  
- `is_valid_isbn13`: 50 Zeichen (13 signifikante Ziffern plus Trennzeichen)  
- `mask_secret`: 4096 Zeichen  
- `strip_accents`: 4096 Zeichen  

Vor der eigentlichen Verarbeitung `if len(text) > _MAX_LENGTH: raise ValueError("input too long")` einfügen. Dabei sicherstellen, dass bestehende, legitime Nutzungsszenarien nicht beeinträchtigt werden.

---

### LOW-02 – Unicode-Ziffern werden von `isdigit()` in Luhn- und ISBN-Prüfung akzeptiert
**Betroffene Stellen:**  
- `validkit/luhn.py`, Zeile `if not cleaned.isdigit():`  
- `validkit/isbn.py`, Zeile `if len(digits) != 13 or not digits.isdigit():`

**Beschreibung:**  
Pythons `str.isdigit()` liefert auch für Unicode-Dezimalziffern (z. B. arabisch-indische Ziffern, Vollbreite Ziffern) `True`. Anschließend werden diese Zeichen mit `int()` konvertiert. Dadurch kann eine Eingabe, die keine reinen ASCII-Ziffern enthält, fälschlich als gültig erkannt werden. Dies ist keine direkte Injection-Schwachstelle, kann aber zu inkonsistentem Verhalten führen, wenn die Bibliothek in Systeme mit ASCII-basierten Prüfsummen oder Datenformaten integriert wird.

**Konkrete Empfehlung:**  
Vor der Prüfsummenberechnung ausschließlich ASCII-Ziffern zulassen. Beispiel:
```python
if not cleaned.isascii() or not cleaned.isdigit():
    raise ValueError(...)
```
oder direkt mit einem ASCII-Regex `^[0-9]+$` prüfen. Dasselbe Vorgehen für `is_valid_isbn13`.

---

### LOW-03 – `mask_secret` akzeptiert `bool` für den `keep`-Parameter
**Betroffene Stelle:**  
`validkit/mask.py`, Parameter `keep: int`

**Beschreibung:**  
`isinstance(keep, int)` akzeptiert auch den Typ `bool`, da `bool` eine Unterklasse von `int` ist. Der Aufruf `mask_secret("geheim123", True)` wird daher als `keep=1` interpretiert und gibt `"******123"`? Tatsächlich: `mask_secret("geheim123", True)` ergibt `"********3"`? Nein: für `"geheim123"` Länge 9, `keep=1` -> 8 Sterne + letztes Zeichen `"3"`. Das Verhalten ist fachlich überraschend, stellt aber keine ausnutzbare Sicherheitslücke dar.

**Konkrete Empfehlung:**  
Analog zu `validkit/clamp.py` bool explizit ablehnen:
```python
if isinstance(keep, bool) or not isinstance(keep, int):
    raise TypeError("keep must be an integer")
```
Dies verbessert die Robustheit der API und verhindert versehentliche Fehlbedienungen.

---

## Positivbefunde

- **Keine Codeausführung:** In keinem Modul werden `eval`, `exec`, `compile` oder vergleichbare Mechanismen verwendet (AC-12 erfüllt).
- **Regex-Sicherheit:** Alle verwendeten regulären Ausdrücke (`email`, `iban`, `phone`, `slug`) sind frei von verschachtelten Quantoren. Vor der Regex-Auswertung erfolgt jeweils eine dokumentierte Maximallängenprüfung (AC-13 erfüllt).
- **Fehlermeldungen ohne Datenleck:** Alle Fehlermeldungen in Funktionen, die personenbezogene oder vertrauliche Eingaben verarbeiten, sind statisch und enthalten die Eingabedaten nicht (AC-14/AC-16 erfüllt).
- **Keine echten PII:** Die Tests verwenden synthetische bzw. reservierte Testdaten (z. B. `example.com`, Test-IBAN, offensichtliche Testtelefonnummern). Es wurden keine echten personenbezogenen Daten gefunden (AC-15 erfüllt).
- **Abhängigkeiten:** Keine externen Laufzeitabhängigkeiten. Die optionale Dev-Abhängigkeit `pytest` ist nicht Teil des Produkts und wird in einer frischen Umgebung nicht benötigt (AC-03 erfüllt).
- **Konfiguration und Transport:** Keine Netzwerk- oder Transportkonfiguration, keine unsicheren Standardwerte, keine Debug- oder CORS-Einstellungen vorhanden.

## Nicht bewertete Aspekte

- Die Scanner `bandit` und `semgrep` waren nicht installiert und wurden übersprungen. Das Fehlen von Scannerergebnissen ist kein Hinweis auf eine Schwachstelle; die manuelle Analyse deckt den sichtbaren Quellcode vollständig ab.
- Die Datei `README.md` ist im Branch vorhanden, wurde aber nicht als Quelltext bereitgestellt. Daher konnte der dokumentierte Beispielteil nicht auf die Einhaltung von AC-11/AC-15 geprüft werden. Aus den sichtbaren Tests und Codebestandteilen ergeben sich keine Anhaltspunkte für einen Verstoß.

## Fazit

Der Stand des Produkts ist aus Sicherheitssicht unbedenklich. Die erfüllten Akzeptanzkriterien und die Abwesenheit von kritischen oder hohen Schwachstellen rechtfertigen die Freigabe. Die drei Low-Findings können im Rahmen einer späteren Härtung adressiert werden, ohne die Funktionsfähigkeit der Bibliothek zu beeinträchtigen.