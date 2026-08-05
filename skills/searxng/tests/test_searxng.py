"""Regression tests for the dependency-free web-search fallback."""

import importlib.util
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError


SCRIPT_PATH = Path(
    os.environ.get("SEARXNG_SCRIPT_PATH", Path(__file__).parents[1] / "scripts" / "searxng.py")
)
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

LEGACY_INSTANT_ANSWER_RESPONSE = b'{"Abstract": "", "RelatedTopics": []}'


class Response:
    """Minimal context-managed response fixture for urllib tests."""

    def __init__(self, body=SEARCH_HTML):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self.body


def legacy_instant_answer_results(payload):
    """Model the prior Instant Answer response shape for an ordinary research query."""
    data = json.loads(payload.decode("utf-8"))
    results = []
    if data.get("Abstract"):
        results.append(data)
    for topic in data.get("RelatedTopics", []):
        if isinstance(topic, dict) and topic.get("Text"):
            results.append(topic)
    return results


def unavailable_searxng_then_html(request, **_):
    """Make the preferred path unavailable and return a real-result HTML fixture for fallback."""
    url = getattr(request, "full_url", request)
    if url.startswith(SEARXNG.SEARXNG_URL):
        raise URLError("SearXNG unavailable")
    if url.startswith("https://api.duckduckgo.com/"):
        return Response(LEGACY_INSTANT_ANSWER_RESPONSE)
    return Response()


class SearchFallbackTests(unittest.TestCase):
    """Ensure the fallback extracts ordinary search-result fields from HTML."""

    def test_fallback_extracts_title_url_and_snippet(self):
        with patch.object(SEARXNG.urllib.request, "urlopen", return_value=Response()):
            results = SEARXNG.search_web_fallback("research query", limit=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Research report")
        self.assertEqual(results[0]["url"], "https://example.org/report")
        self.assertEqual(results[0]["content"], "A useful source snippet for research.")

    def test_public_search_returns_usable_results_when_searxng_is_unavailable(self):
        self.assertEqual(legacy_instant_answer_results(LEGACY_INSTANT_ANSWER_RESPONSE), [])

        with patch.object(SEARXNG.urllib.request, "urlopen", side_effect=unavailable_searxng_then_html):
            results = SEARXNG.search(
                "ordinary research query",
                limit=5,
                category="general",
                language="auto",
                time_range=None,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Research report")
        self.assertEqual(results[0]["url"], "https://example.org/report")
        self.assertEqual(results[0]["content"], "A useful source snippet for research.")


if __name__ == "__main__":
    unittest.main()
