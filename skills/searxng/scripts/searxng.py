#!/usr/bin/env python3
"""Source-discovery client with SearXNG and Mojeek fallback.

Purpose: Query a reachable SearXNG instance, then fall back to parsed Mojeek HTML results.
Public API: Run this file with a query and optional category, language, time-range, limit, or JSON flags.
Upstream deps: Python 3 standard library, an optional SearXNG endpoint, and Mojeek's public HTML endpoint.
Downstream consumers: The SignalBrief searxng skill and agents gathering sources for a research note.
Failure modes: Returns no results when both network paths fail; does not start services or install dependencies.
Performance: Uses a 5-second SearXNG timeout and a 10-second fallback timeout.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional


SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080").rstrip("/")
SEARXNG_TIMEOUT_SECONDS = 5
FALLBACK_TIMEOUT_SECONDS = 10


def search_searxng(
    query: str,
    limit: int,
    category: str,
    language: str,
    time_range: Optional[str],
) -> List[Dict[str, Any]]:
    """Query the configured SearXNG instance and return its limited result set."""
    params: Dict[str, str] = {"q": query, "format": "json", "categories": category}
    if language != "auto":
        params["language"] = language
    if time_range:
        params["time_range"] = time_range

    url = f"{SEARXNG_URL}/search?{urllib.parse.urlencode(params)}"
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "SignalBrief/1.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=SEARXNG_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload.get("results", [])[:limit]
    except Exception as error:
        print(f"SearXNG error: {error}", file=sys.stderr)
        return []


class MojeekResultsParser(HTMLParser):
    """Extract direct result URLs, titles, and snippets from Mojeek result cards."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.results: List[Dict[str, Any]] = []
        self.current: Optional[Dict[str, str]] = None
        self.collecting: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if tag == "li" and any(re.fullmatch(r"r\d+", css_class) for css_class in classes):
            self.current = {"title": "", "url": "", "content": ""}
        if not self.current:
            return
        if tag == "a" and "title" in classes:
            self.current["url"] = attributes.get("href", "")
            self.collecting = "title"
        elif tag == "p" and "s" in classes:
            self.collecting = "content"

    def handle_data(self, data: str) -> None:
        if self.current and self.collecting:
            self.current[self.collecting] += data

    def handle_endtag(self, tag: str) -> None:
        if tag in {"a", "p"}:
            self.collecting = None
        if tag == "li" and self.current:
            title = " ".join(self.current["title"].split())
            url = self.current["url"]
            content = " ".join(self.current["content"].split())
            if title and url and content:
                self.results.append(
                    {
                        "title": title,
                        "url": url,
                        "content": content,
                        "score": 0.5,
                        "engines": ["mojeek"],
                    }
                )
            self.current = None
            self.collecting = None


def search_web_fallback(query: str, limit: int) -> List[Dict[str, Any]]:
    """Search Mojeek's HTML endpoint when SearXNG is unavailable."""
    url = "https://www.mojeek.com/search?" + urllib.parse.urlencode({"q": query})
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; SignalBrief/1.0)"},
        )
        with urllib.request.urlopen(request, timeout=FALLBACK_TIMEOUT_SECONDS) as response:
            document = response.read().decode("utf-8", "replace")
    except Exception as error:
        print(f"Mojeek fallback error: {error}", file=sys.stderr)
        return []

    parser = MojeekResultsParser()
    parser.feed(document)
    parser.close()
    if not parser.results:
        print("Mojeek fallback returned no parseable web results.", file=sys.stderr)
    return parser.results[:limit]


def search(
    query: str,
    limit: int,
    category: str,
    language: str,
    time_range: Optional[str],
) -> List[Dict[str, Any]]:
    """Search SearXNG first and use Mojeek only when no results are returned."""
    results = search_searxng(query, limit, category, language, time_range)
    if not results:
        print("SearXNG unavailable, falling back to Mojeek web search...", file=sys.stderr)
        results = search_web_fallback(query, limit)
    return results


def format_results(results: List[Dict[str, Any]], query: str) -> str:
    """Format result fields for a readable terminal response."""
    if not results:
        return f"No results found for: {query}"

    lines = [f"Search results for: {query}", "=" * 60, ""]
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. {result.get('title', 'No title')}")
        if result.get("url"):
            lines.append(f"   {result['url']}")
        if result.get("content"):
            lines.append(f"   {result['content'][:250]}...")
        lines.append(f"   {', '.join(result.get('engines', ['unknown']))}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    """Parse command-line arguments and print structured or human-readable results."""
    parser = argparse.ArgumentParser(description="SearXNG source-discovery client with Mojeek fallback")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("-n", "--limit", type=int, default=10, help="Maximum result count")
    parser.add_argument(
        "--category",
        default="general",
        choices=["general", "images", "videos", "news", "map", "music", "files", "it", "science"],
        help="SearXNG category",
    )
    parser.add_argument("--language", default="auto", help="Language code, such as en or de")
    parser.add_argument("--time-range", choices=["day", "week", "month", "year"])
    parser.add_argument("--json", action="store_true", help="Print JSON results")
    args = parser.parse_args()

    query = " ".join(args.query)
    results = search(query, args.limit, args.category, args.language, args.time_range)
    print(json.dumps(results, indent=2) if args.json else format_results(results, query))


if __name__ == "__main__":
    main()
