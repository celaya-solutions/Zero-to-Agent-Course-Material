import unittest

from watch import extract_value


class ExtractValueTest(unittest.TestCase):
    def test_extracts_marked_text(self):
        page = '<p>Status: <strong id="watch-value">OPEN</strong></p>'
        self.assertEqual(extract_value(page), "OPEN")

    def test_removes_nested_markup(self):
        page = '<span id="watch-value"><b>PAUSED</b></span>'
        self.assertEqual(extract_value(page), "PAUSED")

    def test_requires_marker(self):
        with self.assertRaisesRegex(ValueError, "watch-value"):
            extract_value("<p>OPEN</p>")


if __name__ == "__main__":
    unittest.main()
