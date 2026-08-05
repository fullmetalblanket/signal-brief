---
name: searxng
description: Discover current web sources with a reachable SearXNG instance or DuckDuckGo fallback.
---

# Source Discovery

Use this workflow after receiving a seed source to find relevant primary and reputable secondary material. It can also be used to verify time-sensitive facts before writing or extending a research note.

## First use

Run the bundled standard-library client from the repository root:

```bash
python3 skills/searxng/scripts/searxng.py "research query" --json -n 10
```

The client first queries `http://localhost:8080`. Set `SEARXNG_URL` to use an accessible SearXNG instance elsewhere. If the instance cannot be reached or returns no results, the client reports the condition and falls back to DuckDuckGo. It does not start Docker, install packages, or create a local service.

## Search guidance

1. Derive focused queries from the seed source and research question.
2. Prefer primary sources, official documentation, and reputable reporting.
3. Read the relevant sources before making claims. Search results are leads, not evidence by themselves.
4. Record source links and dates in the research note.

Useful options:

```bash
python3 skills/searxng/scripts/searxng.py "query" -n 5
python3 skills/searxng/scripts/searxng.py "query" --category news --time-range week
SEARXNG_URL=https://search.example.org python3 skills/searxng/scripts/searxng.py "query"
```

## Optional self-hosting

If the user already operates SearXNG, use `settings/searxng-settings.yml.example` as a localhost-safe reference and set `SEARXNG_URL` to its address. Do not start, configure, or expose a local service without the user's explicit direction.

## Attribution

This bundled workflow is adapted from material authored by Tyson Hummel.
