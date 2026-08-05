"""Regression tests for the dependency-free web-search fallback."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "searxng.py"
SPEC = importlib.util.spec_from_file_location("signalbrief_searxng", SCRIPT_PATH)
assert SPEC and SPEC.loader
SEARXNG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEARXNG)


SEARCH_HTML = b"""
<ul class="results-standard">
  <li class="r7">
    <h2><a class="title" href="https://example.org/report">Research report</a></h2>
    <p class="s">A useful source snippet for research.</p>
  </li>
</ul>
"""


class Response:
    """Minimal context-managed response fixture for urllib tests."""

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return SEARCH_HTML


class SearchFallbackTests(unittest.TestCase):
    """Ensure the fallback extracts ordinary search-result fields from HTML."""

    def test_fallback_extracts_title_url_and_snippet(self):
        with patch.object(SEARXNG.urllib.request, "urlopen", return_value=Response()):
            results = SEARXNG.search_web_fallback("research query", limit=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Research report")
        self.assertEqual(results[0]["url"], "https://example.org/report")
        self.assertEqual(results[0]["content"], "A useful source snippet for research.")


if __name__ == "__main__":
    unittest.main()
