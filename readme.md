# 🤖 Nextcloud AI-Übersetzungsrichtlinien (EN ➡️ DE)

Dieses Repository soll als "Single Source of Truth" für KI-Übersetzungen im Nextcloud-Kontext dienen..

---

## 📜 Die Regeln für Nextcloud KI-Übersetzungen

### 1. Variablen, Platzhalter & Code sind heilig
Nextcloud nutzt in seinen `.json`-, `.po`- und `.js`/`.vue`-Dateien verschiedenste Platzhalter (z. B. `%s`, `%1$s`, `{user}`, `{0}`). KIs neigen dazu, diese "mitzuübersetzen" oder im Satzbau so zu verschieben, dass der Code bricht.
* **KI-Instruktion:** Alle Platzhalter, HTML-Tags und Formatierungen müssen exakt 1:1 in die Ziel-Zeichenkette übernommen werden. 
* **Falsch:** `The file %s was deleted` ➡️ `Die Datei % s wurde gelöscht` (Leerzeichen hinzugefügt -> Syntax-Fehler!)
* **Richtig:** `Die Datei %s wurde gelöscht.`

### 2. Kontext mitgeben: Die App bestimmt die Bedeutung
Eine KI ohne Kontext rät. Das englische Wort "Share" bedeutet in *Nextcloud Talk* etwas anderes als in *Nextcloud Files*.
* **KI-Instruktion:** Der System-Prompt muss **immer** den Namen der Nextcloud-App (z. B. `deck`, `calendar`, `files_sharing`) als Kontextparameter enthalten.
* **Beispiel-Prompt-Zusatz:** *"Du übersetzt Strings für die Nextcloud-App 'Deck' (Kanban-Projektmanagement). Übersetze 'Board' nicht mit 'Brett', sondern behalte 'Board' bei."*

### 3. Der Nextcloud-Tonfall: de_DE (Informell) vs. de_DE_formal
Nextcloud unterscheidet strikt zwischen dem lockeren "Du" (`de`) und dem geschäftlichen "Sie" (`de_DE_formal`). KIs mischen das gerne innerhalb eines Satzes, wenn man sie nicht zwingt.
* **KI-Instruktion:** Wir generieren standardmäßig für `de` (informell). Der KI muss per System-Prompt ein striktes "Verwende ausschließlich das respektvolle 'Du' und niemals 'Sie'" vorgegeben werden.
* **Regel:** Keine passiv-aggressiven oder zu roboterhaften Formulierungen.
* **Hinweis:** Laut Beschluss der Übersetzer-Treffen wird die direkte Anrede ("du"/"Sie") wo sinnvoll möglich ganz vermieden (siehe Regel 4.1).

### 4. Beschlüsse der deutschen Übersetzer-Treffen
Die folgenden Regeln wurden in den Online-Treffen der deutschen Übersetzer beschlossen und gelten für **beide** Varianten (`de` und `de_DE`). Die Quelle steht jeweils in Klammern.

* [Meeting 2 – 25.02.2025](https://help.nextcloud.com/t/online-meeting-2-der-deutschen-ubersetzer-2025-02-24/216334)
* [Meeting 3 – 14.10.2025](https://help.nextcloud.com/t/online-meeting-3-der-deutschen-ubersetzer-2025-10-14/218613)
* [Meeting 4 – 10.03.2026](https://help.nextcloud.com/t/online-meeting-4-der-deutschen-ubersetzer-2026-03-10/234034)
* [Meeting 5 – 01.10.2026](https://help.nextcloud.com/t/online-meeting-5-der-deutschen-ubersetzer-2026-10-01/241604)

#### 4.1 Anrede & Sprachvarianten
* Es bleibt bei zwei Varianten: informell (`de`, "du") und formell (`de_DE`, "Sie"). *(M2)*
* Die direkte Anrede wird wo sinnvoll möglich vermieden. *(M3, M5)*
  * `Do you want to delete this file?` ➡️ `Soll diese Datei gelöscht werden?` statt `Willst du …`/`Wollen Sie …`
* Der Platzhalter "Hier wird nur de_DE verwendet" bleibt dem Übersetzer überlassen. Wird eine informelle Übersetzung angefertigt, darf sie **keine** formelle Anrede enthalten – kein Copy & Paste aus `de_DE`. *(M3)*
* Geschlechtergerechte Sprache: Die bisherige Umsetzung bleibt unverändert. *(M2, M3)*

#### 4.2 Typografie
* **Anführungszeichen** wie im Englischen: `"Hallo"` statt `„Hallo“`. *(M3)*
* **Geschütztes Leerzeichen (nbsp, `U+00A0`)**
  * vor der Ellipse: `Lade …` ➡️ `Lade` + nbsp + `…` *(M3, M4)*
  * zwischen Zahl und Einheit bzw. Zeichen – immer, egal ob `%`, `°` oder `€`: `50` + nbsp + `%` *(M4)*
  * in "z. B.": `z.` + nbsp + `B.` – weder `z.B.` noch `z. B.` mit normalem Leerzeichen. *(M5)*
* Keine doppelten Leerzeichen. Tipp: Leerzeichen im Editor anzeigen lassen. *(M3)*
* Sonderzeichen wie `` ` `` aus der Quelle kopieren statt abtippen – besonders wichtig in der Dokumentation (Sphinx). *(M3)*

#### 4.3 Bindestriche
* Ein Bindestrich wird immer dann verwendet, wenn er das Wort schneller und besser erfassbar macht. *(M4)*
  * `Team folder` ➡️ `Team-Ordner` (nicht `Teamordner`)
  * `Link preview` ➡️ `Link-Vorschau` (nicht `Linkvorschau`)

#### 4.4 Wortwahl
| Englisch | Deutsch | Anmerkung | Quelle |
|---|---|---|---|
| *(nicht in der Quelle)* | ~~wirklich~~, ~~erfolgreich~~ | Füllwörter nicht hinzufügen. `File saved` ➡️ `Datei gespeichert` | M4 |
| Warning | Achtung | nicht "Warnung"; Ausnahme: `Security warning` ➡️ `Sicherheitswarnung` | M5 |
| configure (Verb) | einrichten | "konfigurieren" nur beim technischen Vorgang, z. B. Konfigurationsdatei oder Datenbank | M5 |
| configuration (Nomen) | Konfiguration | nicht "Einrichtung" | M5 |
| master / slave | – | keine Master/Slave-Formulierungen; `Master password` ➡️ `Hauptpasswort` | M5 |
| restrict | einschränken / beschränken | Entscheidung im Einzelfall, der Duden gibt keine klare Vorgabe | M4 |
| paused | angehalten / pausiert | kein fester Begriff; bei Musik "pausiert" | M5 |
| Smart Picker | Smart Picker | bleibt vorerst als Eigenname unübersetzt | M4 |

#### 4.5 Offene Punkte
Noch nicht entschieden, siehe [Meeting 6 – 19.01.2027](https://help.nextcloud.com/t/online-meeting-6-der-deutschen-ubersetzer-2027-01-19/250506):
* "Remote", z. B. `Remote folder` – *Entfernter Ordner*, *Externer Ordner* oder *Remote-Ordner*?
* App-Namen, z. B. *Collectives* – einheitlich *Kollektiv(e)*?
* "forbidden" – *unzulässig* statt *verboten*? (`is a forbidden name` ➡️ `ist ein unzulässiger Name`)
* "Federation" / "föderiert" – Abstimmung mit der Nextcloud GmbH (M4)

---

## 🔧 Automatische Prüfung
`tools/check_translations.py` prüft Übersetzungen auf die Regeln oben. Benötigt nur Python 3.9+ ohne weitere Pakete.

```bash
# Nextcloud-l10n-Dateien (Variante wird aus dem Dateinamen erkannt: de = informell, de_DE = formell)
python3 tools/check_translations.py path/to/server/apps/files/l10n/de.json path/to/server/apps/files/l10n/de_DE.json

# .po-Dateien aus Transifex oder ganze Verzeichnisse
python3 tools/check_translations.py --variant formal translations/

# Tests
python3 -m unittest discover -s tests
```

| Code | Stufe | Regel |
|---|---|---|
| `placeholder` | Fehler | Platzhalter (`%s`, `%1$s`, `%n`, `{user}`) wie in der Quelle (Regel 1) |
| `nbsp-ellipsis` | Fehler | nbsp vor "…" |
| `nbsp-unit` | Fehler | nbsp zwischen Zahl und `%`, `°`, `€` |
| `z-b` | Fehler | "z.&nbsp;B." mit nbsp |
| `quotes` | Fehler | keine deutschen Anführungszeichen |
| `double-space` | Fehler | keine doppelten Leerzeichen |
| `master-slave` | Fehler | keine Master/Slave-Formulierungen |
| `term` | Fehler | Team-Ordner, Link-Vorschau |
| `formal-in-informal` | Fehler | "Sie/Ihnen/Ihre" mitten im Satz in `de` |
| `informal-in-formal` | Fehler | "du/dich/dein" in `de_DE` |
| `filler` | Hinweis | "wirklich"/"erfolgreich" ohne Entsprechung in der Quelle |
| `warning` | Hinweis | "Warning" ➡️ "Achtung" |
| `configuration` | Hinweis | "Konfiguration" statt "Einrichtung" |

Hinweise sind Kandidaten zur manuellen Prüfung. Mit `--strict` führen auch sie zu Exit-Code 1, mit `--no-hints` werden sie ausgeblendet.
