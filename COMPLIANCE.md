VERDICT: CHANGES_REQUESTED

Projekttyp: `python-backend` — reine, eigenständige Python-Bibliothek ohne Netzwerkzugriff, CLI, UI oder externe Laufzeitabhängigkeiten. Die Prüfung erfolgt als Gesamtbild des merged Stands gegen DSGVO, CRA sowie die übrigen relevanten Pflichten.

## 1. DSGVO / Datenschutz

### 1.1 `mask_secret` gibt bei `keep == len(text)` die Originaleingabe unverändert zurück
- **Schweregrad:** hoch
- **Fundstelle:** `validkit/mask.py`, insbesondere die Bedingung  
  `if keep > len(text): raise ValueError("keep must not exceed the length of the text")`  
  sowie die Rückgabe  
  `return "*" * (len(text) - keep) + text[len(text) - keep :]`
- **Problem:** Für `keep == len(text)` entsteht `"*" * 0 + text[0:]`, also exakt die Originaleingabe. Die Funktion ist ausdrücklich als Geheimnis-Maskierungsfunktion vorgesehen. AC-14 verlangt wörtlich, dass die Originaleingabe **nicht** zurückgegeben wird. Der bestehende Test `tests/test_mask.py::test_mask_secret_keep_equal_to_length_masks_nothing` zementiert dieses Verhalten sogar als erwartetes Ergebnis. Damit kann ein vertrauliches Datum bei einem nur leicht falsch gewählten `keep` vollständig unverändert zurückgegeben werden. Das ist ein Datenschutz- und Sicherheitsdefekt in einer Funktion, deren Zweck genau der Schutz solcher Eingaben ist.
- **Konkrete Abhilfe:**
  - In `validkit/mask.py` die Prüfung ändern auf:
    ```python
    if keep >= len(text):
        raise ValueError("keep must be smaller than the length of the text")
    ```
    Für den Sonderfall `text == ""` und `keep == 0` kann weiterhin ein leerer String zurückgegeben werden; relevant ist der Schutz nichtleerer Geheimnisse.
  - In `tests/test_mask.py` den Test `test_mask_secret_keep_equal_to_length_masks_nothing` so ändern, dass er einen `ValueError` erwartet, z. B.:
    ```python
    with pytest.raises(ValueError):
        mask_secret("abc", keep=3)
    ```
  - README-Beispiel und Docstring in `mask_secret` entsprechend präzisieren: `keep` muss `0 <= keep < len(text)` sein. AC-08 bleibt erfüllt.

### 1.2 Positiv geprüft, kein Befund
- Kein Logging, kein `print`, keine Persistenz, keine Netzwerkzugriffe der Bibliothek.
- Fehlermeldungen der vertraulichkeitsrelevanten Funktionen `is_valid_email`, `luhn_check`, `is_valid_iban`, `normalize_phone` und `mask_secret` enthalten die Eingabe nicht.
- Die Test- und Beispieldaten sind synthetisch bzw. reserviert: `example.com`, Luhn-Testnummer `4111 …`, synthetische IBAN, synthetische Telefonnummern. Es fallen keine echten personenbezogenen Daten an.
- Die Bibliothek selbst ist kein Verantwortlicher; DSGVO-Pflichten entstehen erst bei Integratoren. Der oben behobene `mask_secret`-Punkt ist die relevante Schutzmaßnahme im Code.

## 2. EU Cyber Resilience Act (CRA)

### 2.1 Hersteller- und Lizenzangaben fehlen
- **Schweregrad:** hoch
- **Fundstelle:** `pyproject.toml`, `[project]` enthält `name`, `version`, `description`, `readme`, `requires-python`, `dependencies` — aber **keine** Lizenz und **keine** Hersteller-/Pflegeangaben. Eine eigene `LICENSE`-Datei ist auf dem Branch nicht vorhanden.
- **Problem:** Für das Inverkehrbringen eines Produkts mit digitalen Elementen muss der Hersteller identifizierbar sein. Ohne Lizenz ist die Nutzung und Weitergabe der Bibliothek rechtlich unklar; das ist ein Marktreife-Mangel und zugleich ein CRA-Formalmangel hinsichtlich Herstellerkennzeichnung.
- **Konkrete Abhilfe:**
  - Eine `LICENSE`-Datei hinzufügen (z. B. MIT, BSD-3-Clause, Apache-2.0).
  - In `pyproject.toml` unter `[project]` ergänzen:
    ```toml
    license = { file = "LICENSE" }   # oder SPDX-Ausdruck: license = "MIT"
    authors = [{ name = "…", email = "…" }]
    maintainers = [{ name = "…", email = "…" }]
    ```
  - Optional `[project.urls]` mit `Repository = "…"` und `Documentation = "…"` ergänzen.

### 2.2 SBOM und dokumentierte Sicherheitseigenschaften fehlen als explizite Artefakte
- **Schweregrad:** mittel
- **Fundstelle:** Es existiert keine `SECURITY.md`, keine maschinenlesbare SBOM-Datei und kein sichtbarer Sicherheits-/Datenschutzabschnitt. Die Laufzeitabhängigkeiten sind zwar leer (`dependencies = []`), die CRA-SBOM-Anforderung ist damit faktisch trivial, aber nicht formal dokumentiert.
- **Konkrete Abhilfe:**
  - `SECURITY.md` mit den Sicherheitseigenschaften ergänzen: keine Ausführung von Code (`eval`/`exec`/`compile` nicht verwendet), Eingabelängenprüfungen vor allen regulären Ausdrücken, keine Ausgabe übergebener Eingaben in Fehlermeldungen, keine Logs/Persistenz/Netzwerk, keine externen Laufzeitabhängigkeiten.
  - Optional eine SBOM-Datei (z. B. `sbom.spdx.json`) erzeugen, die `validkit` in Version `0.1.0` und keine Laufzeitabhängigkeiten ausweist.
  - In `README.md` einen kurzen Abschnitt „Sicherheit & Datenschutz“ aufnehmen.

### 2.3 Fehlende obere Eingabegrenzen bei `luhn_check`, `is_valid_isbn13` und der IBAN-Roheingabe
- **Schweregrad:** niedrig
- **Fundstelle:** `validkit/luhn.py`, `validkit/isbn.py`, `validkit/iban.py`
- **Problem:** `luhn_check` und `is_valid_isbn13` verarbeiten Eingaben ohne jede Längengrenze; `is_valid_iban` begrenzt erst nach `text.replace(" ", "")`, nicht die Roheingabe. Ein sehr großer String kann unnötigen CPU-/Speicheraufwand verursachen. Das widerspricht dem CRA-Grundsatz „security by design/default“, ist aber mangels Netzwerkzugriff und Logging kein hohes Risiko.
- **Konkrete Abhilfe:**
  - In `validkit/luhn.py` eine dokumentierte Konstante wie `_MAX_LUHN_INPUT_LENGTH = 64` einführen und vor `replace`/Schleife prüfen; Fehlermeldung ohne Eingabe, z. B. `ValueError("Eingabe ist zu lang")`.
  - In `validkit/isbn.py` eine Konstante wie `_MAX_ISBN_INPUT_LENGTH = 32` einführen und vor den `replace`-Aufrufen prüfen; zu lange Eingaben mit `return False` ablehnen.
  - In `validkit/iban.py` eine Roheingabelänge wie `_MAX_IBAN_RAW_LENGTH = 100` vor `replace(" ", "")` prüfen; zu lange Eingaben mit `return False` ablehnen.
  - Die gewählten Grenzen sind großzügig und erlauben alle legitimen Anwendungsfälle der Bibliothek.

## 3. EU AI Act

- **Nicht einschlägig:** Es ist keine KI-Funktion vorhanden. Die Bibliothek enthält ausschließlich deterministische Prüf- und Normalisierungsfunktionen ohne Modell, Training, Inferenz oder Entscheidungsautonomie.

## 4. Mandatorische Texte, UI, Cookies, Barrierefreiheit

- **Nicht einschlägig:** Reine Python-Bibliothek ohne öffentliche Web-UI, CLI oder Endnutzer-Oberfläche. Es bestehen keine Pflichten zu Impressum, Datenschutzerklärung, Cookie-Banner, Widerrufsbelehrung oder EAA-/WCAG-Anforderungen. Ein README-Abschnitt zu Sicherheit und Datenschutz ist dennoch als CRA-Dokumentation sinnvoll (siehe 2.2).

## Gesamtbewertung

Der Stand ist technisch weitgehend sauber: Die neun Funktionen sind typisiert, es gibt keine externen Laufzeitabhängigkeiten, keine Code-Ausführung durch `eval`/`exec`/`compile`, keine PII in Logs oder Fehlermeldungen, und die ReDoS-Schutzmaßnahmen für Regex-basierte Funktionen sind umgesetzt.

Offen sind jedoch zwei substanzielle Punkte: die Rückgabe der Originaleingabe durch `mask_secret` bei `keep == len(text)` und die fehlenden Hersteller-/Lizenz-/Sicherheitsdokumente. Beides ist behebbar, daher `CHANGES_REQUESTED`.