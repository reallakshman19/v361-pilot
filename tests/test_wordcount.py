"""Black-box acceptance tests for the standalone word-count CLI."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "wordcount.py"


class WordCountCLITests(unittest.TestCase):
    def run_file(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True, text=True, check=False,
            )

    def assert_count(self, content, expected):
        result = self.run_file(content)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"{expected}\n")
        self.assertEqual(result.stderr, "")

    def test_simple_words(self):
        self.assert_count("one two three", 3)

    def test_spaces_tabs_and_newlines(self):
        self.assert_count("one\ttwo\nthree   four\r\nfive", 5)

    def test_repeated_whitespace(self):
        self.assert_count(" \t alpha  \n\n beta \t gamma \n", 3)

    def test_empty_file(self):
        self.assert_count("", 0)

    def test_whitespace_only_file(self):
        self.assert_count(" \t\r\n  \n", 0)

    def test_unicode_words(self):
        self.assert_count("café naïve 東京", 3)

    def test_single_numeric_stdout(self):
        result = self.run_file("a b")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "2\n")
        self.assertEqual(result.stderr, "")

    def test_missing_file_error(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.txt"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(missing)],
                capture_output=True, text=True, check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing.txt", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
