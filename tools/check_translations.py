#!/usr/bin/env python3
"""Prüft deutsche Nextcloud-Übersetzungen gegen die Regeln aus readme.md.

Unterstützte Eingaben:
  * Gettext-Dateien (*.po), z. B. aus Transifex heruntergeladen
  * Nextcloud-l10n-Dateien (l10n/*.json)

Die Sprachvariante wird aus dem Dateinamen abgeleitet ("de" = informell/Du,
"de_DE" = formell/Sie) oder mit --variant vorgegeben.

Exit-Code: 0 = keine Fehler, 1 = Fehler gefunden (mit --strict zählen auch
Hinweise), 2 = Aufruffehler.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Iterator

NBSP = " "

ERROR = "error"
HINT = "hint"


@dataclass(frozen=True)
class Entry:
    source: str
    target: str
    line: int
    context: str = ""


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    severity: str
    code: str
    message: str
    target: str

    def format(self) -> str:
        shown = self.target.replace(NBSP, "⍽").replace("\n", "\\n")
        if len(shown) > 100:
            shown = shown[:97] + "..."
        return f"{self.path}:{self.line}: {self.severity} [{self.code}] {self.message}\n    {shown}"


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------

_PO_KEYWORD = re.compile(r'^(msgctxt|msgid|msgid_plural|msgstr(?:\[\d+\])?)\s+(".*")\s*$')
_PO_CONTINUATION = re.compile(r'^(".*")\s*$')


def _po_unquote(literal: str) -> str:
    # PO-Strings verwenden C-Escapes, die mit Python-Literalen kompatibel sind.
    return ast.literal_eval(literal)


def parse_po(text: str) -> list[Entry]:
    entries: list[Entry] = []
    fields: dict[str, str] = {}
    current: str | None = None
    start_line = 0

    def flush() -> None:
        nonlocal fields, current
        source = fields.get("msgid", "")
        if source:  # leerer msgid = Header
            plural_source = fields.get("msgid_plural", "")
            ctx = fields.get("msgctxt", "")
            for key, value in fields.items():
                if not key.startswith("msgstr") or not value:
                    continue
                src = plural_source if key not in ("msgstr", "msgstr[0]") and plural_source else source
                entries.append(Entry(src, value, start_line, ctx))
        fields = {}
        current = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            if fields and current and current.startswith("msgstr"):
                flush()
            continue
        match = _PO_KEYWORD.match(line)
        if match:
            keyword, literal = match.groups()
            if keyword in ("msgctxt", "msgid") and current and current.startswith("msgstr"):
                flush()
            if not fields:
                start_line = lineno
            fields[keyword] = _po_unquote(literal)
            current = keyword
            continue
        match = _PO_CONTINUATION.match(line)
        if match and current:
            fields[current] += _po_unquote(match.group(1))
    if fields:
        flush()
    return entries


def parse_l10n_json(text: str) -> list[Entry]:
    data = json.loads(text)
    translations = data.get("translations", data)
    entries: list[Entry] = []
    lines = text.splitlines()

    def line_of(source: str) -> int:
        needle = json.dumps(source, ensure_ascii=False)
        for idx, line in enumerate(lines, start=1):
            if needle in line:
                return idx
        return 0

    for key, target in translations.items():
        line = line_of(key)
        # Pluralformen: Schlüssel "_%n file_::_%n files_", Wert ist eine Liste.
        plural = re.fullmatch(r"_(.*)_::_(.*)_", key, re.S)
        singular, plural_src = plural.groups() if plural else (key, key)
        targets = target if isinstance(target, list) else [target]
        for index, value in enumerate(targets):
            if isinstance(value, str) and value:
                entries.append(Entry(singular if index == 0 else plural_src, value, line))
    return entries


def load_entries(path: str) -> list[Entry]:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    if path.endswith(".json"):
        return parse_l10n_json(text)
    return parse_po(text)


def detect_variant(path: str) -> str | None:
    """'informal' für de, 'formal' für de_DE / de_DE_formal, sonst None."""
    name = os.path.basename(path)
    stem = name.rsplit(".", 1)[0]
    if re.search(r"(^|[^A-Za-z])de_DE(_formal)?$", stem) or stem.endswith("de_DE"):
        return "formal"
    if re.search(r"(^|[^A-Za-z])de$", stem):
        return "informal"
    parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
    if parent in ("de_DE", "de_DE_formal"):
        return "formal"
    if parent == "de":
        return "informal"
    return None


# --------------------------------------------------------------------------
# Regeln
# --------------------------------------------------------------------------

_PLACEHOLDER = re.compile(r"%(?:\d+\$)?[sdfun]|\{[A-Za-z0-9_.-]+\}")

# Begriffe, die laut Beschluss anders geschrieben werden (falsch -> richtig).
TERMS = {
    r"\bTeamordner": "Team-Ordner",
    r"\bLinkvorschau": "Link-Vorschau",
}


_FORMAL_WORD = re.compile(r"\b(Sie|Ihnen|Ihre[mnrs]?)\b")


def _has_formal_address(text: str) -> bool:
    """Großgeschriebenes Sie/Ihnen/Ihre mitten im Satz.

    Am Satzanfang ist die Großschreibung mehrdeutig ("Sie" = "they") und wird
    deshalb nicht gemeldet.
    """
    for match in _FORMAL_WORD.finditer(text):
        before = text[: match.start()].rstrip(" \"'(" + NBSP)
        if before and before[-1] not in ".!?:\n":
            return True
    return False


def check_entry(entry: Entry, variant: str | None) -> Iterator[tuple[str, str, str]]:
    src, tgt = entry.source, entry.target

    # Regel 1 (readme): Platzhalter 1:1 übernehmen.
    src_ph, tgt_ph = sorted(_PLACEHOLDER.findall(src)), sorted(_PLACEHOLDER.findall(tgt))
    # %n darf in der Singularform fehlen ("eine Datei" für "%n file").
    if src_ph != tgt_ph and [p for p in src_ph if p != "%n"] != [p for p in tgt_ph if p != "%n"]:
        yield ERROR, "placeholder", f"Platzhalter weichen ab: Quelle {src_ph}, Übersetzung {tgt_ph}"

    if "  " in tgt and "  " not in src:
        yield ERROR, "double-space", "Doppeltes Leerzeichen"

    if re.search(r" …", tgt):
        yield ERROR, "nbsp-ellipsis", "Vor \"…\" gehört ein geschütztes Leerzeichen (nbsp)"

    if re.search(r"(?:\d|\}|%(?:\d+\$)?[sdf]) (?:%|°|€)", tgt):
        yield ERROR, "nbsp-unit", "Zwischen Zahl und %, ° oder € gehört ein geschütztes Leerzeichen (nbsp)"

    if re.search(r"\b[zZ]\.[ \u202f]?B\.", tgt):
        yield ERROR, "z-b", "\"z. B.\" mit geschütztem Leerzeichen schreiben: \"z.\\u00a0B.\""

    if re.search(r"[„“”‚‘]", tgt):
        yield ERROR, "quotes", "Anführungszeichen wie im Englischen verwenden: \"Hallo\" statt „Hallo“"

    if re.search(r"(?i)master|slave", tgt):
        yield ERROR, "master-slave", "Keine Formulierungen mit Master/Slave (z. B. \"Hauptpasswort\")"

    for pattern, preferred in TERMS.items():
        if re.search(pattern, tgt):
            yield ERROR, "term", f"Schreibweise laut Beschluss: \"{preferred}\""

    if re.search(r"(?i)\bwirklich", tgt) and not re.search(r"(?i)\breally\b|\btruly\b|\breal\b", src):
        yield HINT, "filler", "\"wirklich\" nicht hinzufügen, wenn es nicht in der Quelle steht"
    if re.search(r"(?i)\berfolgreich", tgt) and not re.search(r"(?i)\bsuccess", src):
        yield HINT, "filler", "\"erfolgreich\" nicht hinzufügen, wenn es nicht in der Quelle steht"

    if (
        re.search(r"(?i)\bwarning\b", src)
        and not re.search(r"(?i)security warning", src)
        and re.search(r"\bWarnung\b", tgt)
    ):
        yield HINT, "warning", "\"Warning\" mit \"Achtung\" übersetzen (Ausnahme: \"Sicherheitswarnung\")"

    if (
        re.search(r"(?i)\bconfigurations?\b", src)
        and not re.search(r"(?i)\bset ?up\b", src)
        and re.search(r"(?i)\beinrichtung\b", tgt)
    ):
        yield HINT, "configuration", "Nomen: \"Konfiguration\" statt \"Einrichtung\""

    if variant == "informal" and _has_formal_address(tgt):
        yield ERROR, "formal-in-informal", "Formelle Anrede in der informellen Variante (de)"
    if variant == "formal" and re.search(r"(?i)(?<![\w@.-])(du|dich|dein(e[mnrs]?)?)(?![\w@-])", tgt):
        yield ERROR, "informal-in-formal", "Informelle Anrede in der formellen Variante (de_DE)"


def check_file(path: str, variant: str | None = None) -> list[Finding]:
    variant = variant or detect_variant(path)
    findings = []
    for entry in load_entries(path):
        for severity, code, message in check_entry(entry, variant):
            findings.append(Finding(path, entry.line, severity, code, message, entry.target))
    return findings


def iter_files(paths: Iterable[str]) -> Iterator[str]:
    for path in paths:
        if os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
                for name in sorted(files):
                    if name.endswith((".po", ".json")):
                        yield os.path.join(root, name)
        else:
            yield path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help=".po-/.json-Dateien oder Verzeichnisse")
    parser.add_argument("--variant", choices=("informal", "formal"), help="Sprachvariante erzwingen")
    parser.add_argument("--strict", action="store_true", help="Hinweise wie Fehler behandeln")
    parser.add_argument("--no-hints", action="store_true", help="Hinweise nicht ausgeben")
    args = parser.parse_args(argv)

    errors = hints = 0
    for path in iter_files(args.paths):
        try:
            findings = check_file(path, args.variant)
        except (OSError, ValueError, SyntaxError) as exc:
            print(f"{path}: kann nicht gelesen werden: {exc}", file=sys.stderr)
            return 2
        for finding in findings:
            if finding.severity == HINT:
                hints += 1
                if args.no_hints:
                    continue
            else:
                errors += 1
            print(finding.format())

    print(f"\n{errors} Fehler, {hints} Hinweise", file=sys.stderr)
    failed = errors + (hints if args.strict else 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
