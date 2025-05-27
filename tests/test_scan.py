import unittest
import random
from io import StringIO

from find_obviously import (
    scan_text_for_obviously,
    extract_random_snippet,
    scan_text,
)


class TestScan(unittest.TestCase):
    def test_scan_finds_lines(self):
        text = (
            "Obviously this is a test.\n"
            "not obviously here.\n"
            "\tObviously we start with whitespace.\n"
            "This is not the droid.\n"
            "OBVIOUSLY capitals count.\n"
        )
        lines = scan_text_for_obviously(text)
        self.assertEqual(len(lines), 3)
        self.assertIn("Obviously this is a test.", lines)
        self.assertIn("\tObviously we start with whitespace.", lines)
        self.assertIn("OBVIOUSLY capitals count.", lines)

    def test_extract_random_snippet_deterministic(self):
        text = "1234567890" * 10  # 100 chars
        random.seed(0)
        snippet = extract_random_snippet(text, 10)
        random.seed(0)
        snippet2 = extract_random_snippet(text, 10)
        self.assertEqual(snippet, snippet2)
        self.assertEqual(len(snippet), 10)

    def test_scan_text_logs_snippet(self):
        text = "foo bar baz\nObviously line here.\nmore text"
        random.seed(1)
        log = StringIO()
        matches = list(scan_text(text, "Title", ["Author"], log))
        self.assertEqual(len(matches), 1)
        log_content = log.getvalue()
        self.assertIn("Title", log_content)
        self.assertTrue(len(log_content.strip()) > 0)


if __name__ == '__main__':
    unittest.main()
