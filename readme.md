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

### 3. Der Nextcloud-Tonfall: de (informell) vs. de_DE (formell)
Nextcloud unterscheidet strikt zwischen dem lockeren "du" (`de`) und dem geschäftlichen "Sie" (`de_DE`). KIs mischen das gerne innerhalb eines Satzes, wenn man sie nicht zwingt.
* **KI-Instruktion:** Die Variante wird per System-Prompt fest vorgegeben: für `de` "Verwende ausschließlich 'du' und niemals 'Sie'", für `de_DE` "Verwende ausschließlich 'Sie' und niemals 'du'".
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
* Geschlechtergerechte Sprache: Die bisherige Umsetzung bleibt unverändert. *(M2, M3)* Sie sieht so aus:
  * Personen in einer Rolle werden über die Funktion benannt: `administrator` ➡️ `Administration` (nicht `Administrator`, `Administratorin` oder `Administrator*innen`).
  * Ist ein einzelnes Konto oder eine Liste von Konten gemeint, steht `Administrationskonto`: `Error adding new administrator` ➡️ `Fehler beim Hinzufügen eines neuen Administrationskontos`.
  * `user` ➡️ `Benutzer` (nicht `Nutzer`), wenn ein Konto in Nextcloud (auch LDAP oder SAML) gemeint ist. Partizipformen wie `Benutzende` werden nicht eingeführt.
  * Andere Personen werden nicht zu "Benutzern": `private users` (Privatkundschaft) ➡️ `Privatnutzer`, `Mastodon people` ➡️ `Mastodon-Konten`.

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
| administrator | Administration | einzelnes Konto: "Administrationskonto", siehe 4.1 | M2, M3 |
| user | Benutzer | nicht "Nutzer", nur für Nextcloud-Konten; Ausnahmen siehe 4.1 | M2, M3 |
| group folder | Gruppenordner | eigenes Konzept neben "Team folder" ➡️ "Team-Ordner" (4.3), beide nicht vermischen | Bestand der App `groupfolders` |
| *n* times | `%n-mal`, `3-mal`, ausgeschrieben `dreimal` | nicht `%n Mal`; als Nomen aber `zum %n. Mal`, `zum ersten Mal` | [Duden](https://www.duden.de/rechtschreibung/mal_zu_irgendeiner_Zeit) |

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
| `placeholder` | Fehler | Platzhalter (`%s`, `%1$s`, `%n`, `{user}`) wie in der Quelle (Regel 1); `%n` nur, wenn es in der Quelle steht |
| `nbsp-ellipsis` | Fehler | nbsp vor "…" |
| `nbsp-unit` | Fehler | nbsp zwischen Zahl und `%`, `°`, `€` |
| `z-b` | Fehler | "z.&nbsp;B." mit nbsp |
| `quotes` | Fehler | keine deutschen Anführungszeichen |
| `double-space` | Fehler | keine doppelten Leerzeichen |
| `master-slave` | Fehler | keine Master/Slave-Formulierungen |
| `term` | Fehler | Team-Ordner, Link-Vorschau; "group folder" nicht als "Team-Ordner" |
| `times` | Fehler | `%n-mal` statt `%n Mal` |
| `wording` | Hinweis | "Benutzer" statt "Nutzer", wenn die Quelle "user" enthält; "Administration" bzw. "Administrationskonto" statt "Administrator(in)" |
| `formal-in-informal` | Fehler | "Sie/Ihnen/Ihre" mitten im Satz in `de` |
| `informal-in-formal` | Fehler | "du/dich/dein" in `de_DE` |
| `filler` | Hinweis | "wirklich"/"erfolgreich" ohne Entsprechung in der Quelle |
| `warning` | Hinweis | "Warning" ➡️ "Achtung" |
| `configuration` | Hinweis | "Konfiguration" statt "Einrichtung" |
| `placeholder-spacing` | Fehler | Platzhalter nicht an ein Wort kleben, wenn die Quelle ein Leerzeichen hat (Genitiv `{user}s` erlaubt) |
| `doubled-word` | Fehler | doppeltes Wort ("mit mit"); bei Artikeln und "sie" nur Hinweis, da Relativsätze ("die die") korrekt sein können |
| `old-spelling` | Fehler | alte oder Schweizer Schreibung ("muß", "weiss", "Fusszeile") |
| `soft-hyphen` | Fehler | weiches Trennzeichen (U+00AD), das nicht in der Quelle steht |

Hinweise sind Kandidaten zur manuellen Prüfung. Mit `--strict` führen auch sie zu Exit-Code 1, mit `--no-hints` werden sie ausgeblendet.

## 🧭 Arbeitsanweisung für Agenten
Wie ein KI-Agent mit diesen Regeln übersetzt und bestehende Übersetzungen korrigiert, steht in [agent-guideline.md](agent-guideline.md).
