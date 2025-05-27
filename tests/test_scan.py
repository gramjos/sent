import unittest
from find_obviously import scan_text_for_obviously


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
        self.assertEqual(len(lines), 4)
        self.assertIn("Obviously this is a test.", lines)
        self.assertIn("not obviously here.", lines)
        self.assertIn("\tObviously we start with whitespace.", lines)
        self.assertIn("OBVIOUSLY capitals count.", lines)


if __name__ == '__main__':
    unittest.main()
