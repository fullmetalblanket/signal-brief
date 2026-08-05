#!/usr/bin/env bash
# Purpose: Diagnose SignalBrief source discovery, deck rendering, and transcript extraction without changing the environment.
# Public API: ./skills/signalbrief-setup/scripts/check-capabilities.sh
# Upstream deps: Standard shell utilities; optional Python, curl, Marp, npm, yt-dlp, and Docker commands.
# Downstream consumers: The signalbrief-setup skill and agents responding to an explicit setup request.
# Failure modes: Reports unavailable tools and fallbacks; exits successfully unless shell execution itself fails.
# Performance: Uses a bounded three-second SearXNG health probe and does not install or start anything.

set -u

searxng_url="${SEARXNG_URL:-http://localhost:8080}"

status() {
  printf '%-18s %s\n' "$1" "$2"
}

printf 'SignalBrief capability diagnostics\n\n'

if command -v python3 >/dev/null 2>&1; then
  status 'Python 3' 'ready for bundled source-discovery client'
else
  status 'Python 3' 'missing - SearXNG client cannot run'
fi

if command -v curl >/dev/null 2>&1 && curl --connect-timeout 1 --max-time 3 --silent --fail \
  "${searxng_url%/}/search?q=signalbrief&format=json" >/dev/null; then
  status 'SearXNG' "ready at ${searxng_url}"
else
  status 'SearXNG' "unavailable at ${searxng_url} - DuckDuckGo fallback remains available"
fi

if command -v marp >/dev/null 2>&1; then
  status 'Marp CLI' 'ready'
elif command -v npm >/dev/null 2>&1; then
  status 'Marp CLI' 'not installed - approved on-demand npm path is available'
else
  status 'Marp CLI' 'missing - npm or an installed Marp CLI is needed for rendering'
fi

if command -v yt-dlp >/dev/null 2>&1; then
  status 'yt-dlp' 'ready for preferred YouTube transcript extraction'
elif command -v curl >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  status 'yt-dlp' 'not installed - curl and Python fallback is available'
else
  status 'yt-dlp' 'not installed - use a browser transcript view or install only if needed'
fi

if command -v docker >/dev/null 2>&1; then
  status 'Docker' 'available for optional user-directed SearXNG hosting'
else
  status 'Docker' 'not required - no local service will be started'
fi

printf '\nNo packages, containers, or configuration were changed.\n'
