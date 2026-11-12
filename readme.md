# 🤖 Nextcloud AI-Übersetzungsrichtlinien (EN ➡️ DE)

Willkommen in unserem Repo! Wir sind drei deutsche Entwickler, die es sich zur Aufgabe gemacht haben, die Übersetzung des Nextcloud-Source-Codes durch Künstliche Intelligenz zu automatisieren und zu optimieren. 

KI ist großartig im Übersetzen, aber sie halluziniert gerne mal, zerschießt Variablen oder übersetzt "Share" in einer Dateiverwaltung mit "Aktie". Damit unsere Nextcloud-Instanzen (und die der Community) nicht durch kaputte Sprachdateien crashen, haben wir dieses Manifest für KI-Prompts und automatisierte Übersetzungs-Pipelines aufgesetzt.

Dieses Repository dient als "Single Source of Truth" für unsere KI-System-Prompts (LLMs wie GPT-4, Claude, etc.) im Nextcloud-Kontext.

---

## 📜 Die 5 Goldenen Regeln für Nextcloud KI-Übersetzungen

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
