---
name: signalbrief-setup
description: Diagnose and safely prepare SignalBrief source discovery, Marp decks, and YouTube transcripts.
---

# Set up SignalBrief

Use this workflow only when the user says **“Set up SignalBrief”** or explicitly invokes `signalbrief-setup`.

## Diagnose first

From the repository root, run:

```bash
./skills/signalbrief-setup/scripts/check-capabilities.sh
```

Report the diagnostic output before changing anything. It checks the three core capabilities:

- Source discovery: a reachable SearXNG endpoint is enhanced support. Mojeek web search is the fallback when it is available.
- Marp decks: an installed Marp CLI is ready. npm can support the existing approval-gated, on-demand Marp path.
- YouTube transcripts: `yt-dlp` is preferred. `curl` plus Python 3 or a browser transcript view remain valid fallbacks.

## Authorized setup actions

Only after the user has asked to run setup and the active environment allows package installation:

1. Prefer the smallest useful action. Do not install `yt-dlp` when the available fallbacks meet the user's needs.
2. For Marp, prefer the repository's approval-gated on-demand runner instead of a permanent global installation.
3. Treat Docker-hosted SearXNG as optional enhanced search. Never install Docker, start a container, or modify service configuration without a separate explicit user direction.
4. If approval or network access is unavailable, report the ready fallback and the exact remaining limitation.

The setup workflow must not silently change machine-wide configuration.
