import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import check_translations as ct  # noqa: E402

NBSP = " "


def codes(source, target, variant=None):
    return {code for _sev, code, _msg in ct.check_entry(ct.Entry(source, target, 1), variant)}


class RuleTests(unittest.TestCase):
    def test_clean_string_has_no_findings(self):
        self.assertEqual(codes("Loading …", f"Lade{NBSP}…"), set())

    def test_placeholder_mismatch(self):
        self.assertIn("placeholder", codes("The file %s was deleted", "Die Datei % s wurde gelöscht"))
        self.assertIn("placeholder", codes("Hello {user}", "Hallo {benutzer}"))
        self.assertNotIn("placeholder", codes("{a} and {b}", "{b} und {a}"))

    def test_nbsp_before_ellipsis(self):
        self.assertIn("nbsp-ellipsis", codes("Loading …", "Lade …"))
        self.assertNotIn("nbsp-ellipsis", codes("Loading …", f"Lade{NBSP}…"))

    def test_nbsp_before_units(self):
        for unit in ("%", "°", "€"):
            self.assertIn("nbsp-unit", codes("x", f"50 {unit}"))
            self.assertNotIn("nbsp-unit", codes("x", f"50{NBSP}{unit}"))
        self.assertIn("nbsp-unit", codes("{percent}%", "{percent} %"))

    def test_z_b(self):
        self.assertIn("z-b", codes("e.g. Foo", "z.B. Foo"))
        self.assertIn("z-b", codes("e.g. Foo", "z. B. Foo"))
        self.assertNotIn("z-b", codes("e.g. Foo", f"z.{NBSP}B. Foo"))

    def test_quotes(self):
        self.assertIn("quotes", codes('"Hello"', "„Hallo“"))
        self.assertNotIn("quotes", codes('"Hello"', '"Hallo"'))

    def test_master_slave(self):
        self.assertIn("master-slave", codes("Master password", "Masterpasswort"))
        self.assertNotIn("master-slave", codes("Master password", "Hauptpasswort"))

    def test_terms(self):
        self.assertIn("term", codes("Team folder", "Teamordner"))
        self.assertIn("term", codes("Link preview", "Linkvorschau"))
        self.assertNotIn("term", codes("Team folder", "Team-Ordner"))

    def test_filler_words(self):
        self.assertIn("filler", codes("Delete file?", "Datei wirklich löschen?"))
        self.assertNotIn("filler", codes("Really delete file?", "Datei wirklich löschen?"))
        self.assertIn("filler", codes("File saved", "Datei erfolgreich gespeichert"))
        self.assertNotIn("filler", codes("File saved successfully", "Datei erfolgreich gespeichert"))

    def test_warning(self):
        self.assertIn("warning", codes("Warning", "Warnung"))
        self.assertNotIn("warning", codes("Warning", "Achtung"))
        self.assertNotIn("warning", codes("Security warning", "Sicherheitswarnung"))

    def test_configuration_noun(self):
        self.assertIn("configuration", codes("Configuration", "Einrichtung"))
        self.assertNotIn("configuration", codes("Not configured. Continue setup.", "Nicht konfiguriert. Einrichtung fortsetzen."))

    def test_double_space(self):
        self.assertIn("double-space", codes("a b", "a  b"))

    def test_formal_in_informal(self):
        self.assertIn("formal-in-informal", codes("x", "Bitte geben Sie Ihr Passwort ein", "informal"))
        self.assertIn("formal-in-informal", codes("x", "Wir senden Ihnen eine E-Mail", "informal"))
        # Satzanfang ist mehrdeutig ("Sie" = "they")
        self.assertNotIn("formal-in-informal", codes("x", "Sie haben die Datei geteilt.", "informal"))
        self.assertNotIn("formal-in-informal", codes("x", "Gib dein Passwort ein", "informal"))

    def test_informal_in_formal(self):
        self.assertIn("informal-in-formal", codes("x", "Gib dein Passwort ein", "formal"))
        self.assertNotIn("informal-in-formal", codes("x", "App deinstallieren", "formal"))
        self.assertNotIn("informal-in-formal", codes("x", "benutzer@deine-nextcloud.org", "formal"))


class ParserTests(unittest.TestCase):
    PO = (
        'msgid ""\n'
        'msgstr ""\n'
        '"Language: de_DE\\n"\n'
        "\n"
        "#: lib/foo.php:1\n"
        'msgid "Loading …"\n'
        'msgstr "Lade …"\n'
        "\n"
        'msgid "%n file"\n'
        'msgid_plural "%n files"\n'
        'msgstr[0] "%n Datei"\n'
        'msgstr[1] ""\n'
        '"%n Dateien"\n'
        "\n"
        'msgid "Untranslated"\n'
        'msgstr ""\n'
    )

    def test_parse_po(self):
        entries = ct.parse_po(self.PO)
        self.assertEqual(
            [(e.source, e.target, e.line) for e in entries],
            [("Loading …", "Lade …", 6), ("%n file", "%n Datei", 9), ("%n files", "%n Dateien", 9)],
        )

    def test_parse_json(self):
        text = json.dumps(
            {"translations": {"Loading …": "Lade …", "_%n file_::_%n files_": ["Eine Datei", "%n Dateien"], "x": ""}},
            ensure_ascii=False,
            indent=4,
        )
        entries = ct.parse_l10n_json(text)
        self.assertEqual(
            [(e.source, e.target) for e in entries],
            [("Loading …", "Lade …"), ("%n file", "Eine Datei"), ("%n files", "%n Dateien")],
        )
        self.assertEqual([c for e in entries for c in codes(e.source, e.target)], ["nbsp-ellipsis"])
        self.assertEqual(entries[0].line, 3)

    def test_detect_variant(self):
        self.assertEqual(ct.detect_variant("l10n/de.json"), "informal")
        self.assertEqual(ct.detect_variant("l10n/de_DE.json"), "formal")
        self.assertEqual(ct.detect_variant("translationfiles/de_DE/files.po"), "formal")
        self.assertEqual(ct.detect_variant("translationfiles/de/files.po"), "informal")
        self.assertIsNone(ct.detect_variant("l10n/fr.json"))

    def test_main_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "de.po")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(self.PO)
            self.assertEqual(ct.main([path]), 1)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(self.PO.replace("Lade …", f"Lade{NBSP}…"))
            self.assertEqual(ct.main([path]), 0)


if __name__ == "__main__":
    unittest.main()
