#!/usr/bin/env python3
"""Source-discovery client with SearXNG and DuckDuckGo fallback.

Purpose: Query a reachable SearXNG instance, then transparently fall back to DuckDuckGo.
Public API: Run this file with a query and optional category, language, time-range, limit, or JSON flags.
Upstream deps: Python 3 standard library, an optional SearXNG endpoint, and DuckDuckGo's public endpoint.
Downstream consumers: The SignalBrief searxng skill and agents gathering sources for a research note.
Failure modes: Returns no results when both network paths fail; does not start services or install dependencies.
Performance: Uses a 30-second SearXNG timeout and a 15-second fallback timeout.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080").rstrip("/")


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
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload.get("results", [])[:limit]
    except Exception as error:
        print(f"SearXNG error: {error}", file=sys.stderr)
        return []


def search_duckduckgo(query: str, limit: int) -> List[Dict[str, Any]]:
    """Use DuckDuckGo's instant-answer endpoint when SearXNG is unavailable."""
    params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
    url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        print(f"DuckDuckGo fallback error: {error}", file=sys.stderr)
        return []

    results: List[Dict[str, Any]] = []
    if payload.get("Abstract"):
        results.append(
            {
                "title": payload.get("Heading", "Instant Answer"),
                "url": payload.get("AbstractURL", ""),
                "content": payload["Abstract"],
                "score": 1.0,
                "engines": ["duckduckgo"],
            }
        )
    for topic in payload.get("RelatedTopics", []):
        if len(results) >= limit:
            break
        if isinstance(topic, dict) and topic.get("Text"):
            results.append(
                {
                    "title": topic["Text"].split(" - ", maxsplit=1)[0],
                    "url": topic.get("FirstURL", ""),
                    "content": topic["Text"],
                    "score": 0.5,
                    "engines": ["duckduckgo"],
                }
            )
    return results


def search(
    query: str,
    limit: int,
    category: str,
    language: str,
    time_range: Optional[str],
) -> List[Dict[str, Any]]:
    """Search SearXNG first and use DuckDuckGo only when no results are returned."""
    results = search_searxng(query, limit, category, language, time_range)
    if not results:
        print("SearXNG unavailable, falling back to DuckDuckGo...", file=sys.stderr)
        results = search_duckduckgo(query, limit)
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
    parser = argparse.ArgumentParser(description="SearXNG source-discovery client with DuckDuckGo fallback")
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
