# 🤖 Arbeitsanweisung für Übersetzungs-Agenten (EN ➡️ DE)

Diese Datei sagt einem KI-Agenten, **wie** er Nextcloud-Strings übersetzt oder bestehende Übersetzungen korrigiert. **Was** gilt, steht in der [readme.md](readme.md): Die dort beschlossenen Regeln haben immer Vorrang. Steht hier etwas im Widerspruch zur readme, gilt die readme.

---

## 1. Eingaben

Ohne diese Angaben übersetzt der Agent nicht, sondern fragt nach:

| Eingabe | Beispiel | Wozu |
|---|---|---|
| Sprachvariante | `de` oder `de_DE` | Anrede (Abschnitt 2) |
| App bzw. Ressource | `spreed`, `files_sharing`, `user_manual` | Bedeutung und Fachbegriffe (readme, Regel 2) |
| Quelltext mit Kontext | `msgctxt`, Kommentare, Fundstelle | Mehrdeutige Wörter wie "Share" |
| Pluralformen | `msgid_plural` | `%n` steht oft nur in der Pluralform |
| Vorhandene Übersetzungen der Ressource | heruntergeladene `.po`-Datei | Begriffe einheitlich halten |

## 2. Sprachvarianten

| | `de` (informell) | `de_DE` (formell) |
|---|---|---|
| Anrede | du, dich, dir, dein | Sie, Ihnen, Ihr |
| Aufforderung | Infinitiv oder neutral: `Datei auswählen` | Infinitiv oder neutral: `Datei auswählen` |
| Frage | `Soll diese Datei gelöscht werden?` | `Soll diese Datei gelöscht werden?` |
| Verboten | jede formelle Anrede | jede informelle Anrede |

* Die direkte Anrede wird wo sinnvoll möglich vermieden (readme 4.1). Infinitiv- und Passivformen sind in beiden Varianten identisch und deshalb die erste Wahl.
* Eine Übersetzung wird nie aus der anderen Variante kopiert und nur "umgestellt". Bei längeren Texten (App-Beschreibungen, Store-Einträge) nach dem Umstellen den ganzen Text auf Reste der anderen Anrede durchsuchen, auch Deklinationen wie `auf Ihren Server` ➡️ `auf deinem Server`.
* Großschreibung von "du" in `de` ist **nicht beschlossen** (siehe Abschnitt 6). Der Agent schreibt neue Texte klein (`du`), wie in rund 98 % der vorhandenen Übersetzungen, ändert aber bestehendes "Du" nicht eigenmächtig.

## 3. Harte Regeln (Fehler blockieren die Übernahme)

### 3.1 Platzhalter
* Jeder Platzhalter der Quelle steht genau so in der Übersetzung: `%s`, `%1$s`, `%n`, `{user}`, `{{strength}}`. Keine Umbenennung (`{name}` ≠ `{Name}`), keine Übersetzung (`{benutzer}`), nichts weglassen.
* `%n` darf nur in der **Singularform** fehlen (`Eine Datei`). In der Pluralform bleibt es. Steht `%n` nicht in der Quelle, steht es auch nicht in der Übersetzung.
* Leerzeichen um Platzhalter wie in der Quelle: `{count} aktiven`, nicht `{count}aktiven`. Ein angeklebtes Wort wird zur Laufzeit zu `5aktiven`.
* Ausnahme: englischer Genitiv `{user}'s` ➡️ deutscher Genitiv `{user}s` ist richtig.

### 3.2 Markup
* HTML-Tags, Markdown, reStructuredText-Rollen (`:ref:`, `:doc:`, `:kbd:`, `:guilabel:`, `:menuselection:`), Link-Ziele `<…>` und URLs bleiben unverändert.
* Text **in** Rollen und `` ``…`` `` wird übersetzt, wenn er sichtbarer UI-Text ist (dann mit dem tatsächlichen deutschen UI-String), und bleibt englisch, wenn er Code, ein Befehl, ein Pfad oder ein Konfigurationsschlüssel ist.
* Markdown-Einrückungen (Listen, Codeblöcke) und zwei Leerzeichen vor einem Zeilenumbruch sind Syntax, keine doppelten Leerzeichen.

### 3.3 Beschlossene Regeln der readme
Typografie (4.2), Bindestriche (4.3), Wortwahl (4.4) und Anrede (4.1) gelten ohne Ausnahme. Insbesondere:
* Anführungszeichen `"…"` statt `„…“`, auch wenn die Quelle `“…”` verwendet.
* Geschütztes Leerzeichen in `z. B.`, vor `…` und zwischen Zahl und `%`, `°`, `€`.
* `Achtung` statt `Warnung`, `einrichten` statt `konfigurieren` (außer beim technischen Vorgang), keine Füllwörter wie `wirklich` oder `erfolgreich`, die nicht in der Quelle stehen.
* `Administration` statt `Administrator`/`Administratorin`, für ein einzelnes Konto `Administrationskonto`. `Benutzer` statt `Nutzer` und nicht `Benutzende`, aber nur für Nextcloud-Konten: `Privatnutzer`, `Mastodon-Konten` (readme 4.1).
* `Gruppenordner` für "group folder" und `Team-Ordner` für "Team folder": zwei verschiedene Dinge.
* `%n-mal`, `3-mal` statt `%n Mal`.

### 3.4 Prüfskript
Vor jeder Übernahme läuft `tools/check_translations.py` mit der richtigen Variante. Jeder **Fehler** wird behoben. Jeder **Hinweis** wird entweder behoben oder in der Übergabe begründet (z. B. "die die" in einem Relativsatz ist korrekt).

## 4. Rechtschreibung

Die Prüfberichte vom 13.11.2026 (de: 252, de_DE: 197 Fundstellen) zeigen, wo Übersetzungen tatsächlich falsch sind. Über 80 % davon sind Tippfehler, die kein Regelwerk verhindert, sondern nur sorgfältiges Prüfen. Der Agent liest deshalb jede Übersetzung vor der Übergabe noch einmal Wort für Wort. Er prüft dabei besonders:

| Fehlerart | Falsch | Richtig |
|---|---|---|
| Alte Rechtschreibung (ß nach kurzem Vokal) | `muß`, `mußt`, `umfaßte`, `Ausschlußmaske` | `muss`, `musst`, `umfasste`, `Ausschlussmaske` |
| Schweizer Schreibung (ss statt ß) | `weiss`, `Ausserdem`, `Fusszeile` | `weiß`, `Außerdem`, `Fußzeile` |
| Getrennt-/Zusammenschreibung | `Jedesmal`, `Wieviele`, `so lange` (Konjunktion), `zusammenmit` | `Jedes Mal`, `Wie viele`, `solange`, `zusammen mit` |
| Durchkopplung bei Namen | `Google Drive-Import` | `Google-Drive-Import` |
| Doppelte Wörter | `mit mit`, `an an`, `kann die die Verwaltung` | `mit`, `an`, `kann die Verwaltung` |
| Deklination | `die häufigsten geplante Zeiten`, `nicht unterstützen Syntax` | `die am häufigsten geplanten Zeiten`, `nicht unterstützten Syntax` |
| Fremdwörter | `Resourcen`, `lizensiert`, `Kontigent`, `Transskription`, `Websiten` | `Ressourcen`, `lizenziert`, `Kontingent`, `Transkription`, `Websites` |
| Client | `den Desktop-Clienten` | `den Desktop-Client` (Plural: `Clients`) |
| Fachbegriffe ohne gängige Übersetzung | `Entität-ID` | `Entity-ID` |
| Weiche Trennzeichen (U+00AD) | `syn­chro­ni­sie­rt` | keine einfügen, die nicht in der Quelle stehen |
| Kleinschreibung nach Klammer | `TOTP (Zeitbasiert)` | `TOTP (zeitbasiert)` |
| Nominalisierung | `Importierung` | `Import` |
| Interjektion | `Upps` | `Ups` |

Produkt- und App-Namen werden wie im Original geschrieben (`Nextcloud`, `Zammad`, `Discourse`, `Recognize`).

## 5. Bestehende Übersetzungen korrigieren

1. **Aktuelle Fassung laden.** Berichte und Listen veralten: Vor jeder Änderung die aktuelle Übersetzung von Transifex holen. Ist ein Fehler schon behoben oder der Text inzwischen anders, wird nichts geändert.
2. **Fremde Korrekturvorschläge prüfen, nicht übernehmen.** Ein Vorschlag ist ein Hinweis, keine Vorgabe. Im Bericht vom 13.11.2026 waren unter anderem diese Vorschläge falsch:
   * `%nkonfigurierten` ➡️ `konfigurierten` hätte einen Platzhalter gelöscht. Die Pluralquelle enthält `%n`, richtig ist `%n eingerichteten`.
   * `"name"` ➡️ `„{name}“` widerspricht Regel 4.2. Richtig ist `"{name}"`.
   * `Geplantzeiten` ➡️ `geplante Zeiten` und `Importierung` ➡️ `Import` ergeben im Satz ungrammatische Texte. Den **ganzen** String lesen, nicht nur das Wort ersetzen.
3. **Wortgrenzen beachten.** Ein Tippfehler kann Teil eines längeren Worts sein (`Kontigent` in `Speicherkontigents`), und ein Suchbegriff kann ein richtiges Wort treffen (`Singl` in `Single`).
4. **Umfang.** Geändert werden der gemeldete Fehler und Verstöße gegen beschlossene Regeln **im selben String** (Anführungszeichen, geschützte Leerzeichen, doppelte Leerzeichen, Anrede). Andere Strings werden nicht "nebenbei" überarbeitet.
5. **Pluralformen** immer gemeinsam ansehen und einheitlich halten.
6. **Übergabe:** Jede Änderung mit alter Fassung, neuer Fassung und Grund auflisten. Hochgeladene Agenten-Übersetzungen bleiben ungeprüft (unreviewed), bis ein Mensch sie freigibt.

## 6. Was der Agent nicht entscheidet

Diese Punkte sind offen (readme 4.5) oder nicht beschlossen. Der Agent übernimmt die vorhandene Schreibweise der Ressource und meldet den Fall, statt selbst zu entscheiden:

* "Remote", z. B. `Remote folder`
* App-Namen wie *Collectives*
* "forbidden" (*unzulässig* oder *verboten*)
* "Federation" / "föderiert"
* Großschreibung von "du" in `de` (Vorschlag: klein, wie in rund 98 % der vorhandenen Übersetzungen)
* Wiederholungen, die gewollt sein können, z. B. `Diese Regeln regeln den Zugriff`
