---
name: signalbrief-setup
description: Safely diagnose SignalBrief source discovery, Marp decks, and YouTube transcripts when a source needs readiness checks.
---

# SignalBrief readiness diagnostic

Use this internal safe readiness diagnostic automatically when a pasted source or requested output needs a capability check. It can also be run when the user says **“Set up SignalBrief”** or explicitly invokes `signalbrief-setup`.

For a source URL, assess only the relevant capabilities before research: source discovery for all research, transcript extraction for supported video sources, and Marp support when a companion deck is requested or expected. Use the available project-local workflow and its fallback before considering an environment change.

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

Only after an available fallback cannot satisfy the source or requested output, the user approves the needed environment change, and the active environment allows it:

1. Prefer the smallest useful action. Do not install `yt-dlp` when the available fallbacks meet the user's needs.
2. For Marp, prefer the repository's approval-gated on-demand runner instead of a permanent global installation.
3. Treat Docker-hosted SearXNG as optional enhanced search. Never install Docker, start a container, or modify service configuration without a separate explicit user direction.
4. If approval or network access is unavailable, report the ready fallback and the exact remaining limitation.

This diagnostic may run automatically, but it must not install packages, start Docker, modify services, or silently change machine-wide configuration.
