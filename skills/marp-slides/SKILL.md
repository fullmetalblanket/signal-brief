---
name: marp-slides
description: Create a concise companion Marp deck from a SignalBrief research note when Marp support is available.
---

# Marp Slides

Use this workflow after completing a research note, or when asked to turn a Markdown note into a concise presentation. Do not use it for video or MP4 creation.

## First-use capability check

Use the bundled runner to check for Marp and render a deck:

```bash
./skills/marp-slides/scripts/run-marp.sh <deck-file>
```

The runner uses an installed `marp` command when present. Otherwise it requires explicit agent or environment approval before it runs the public [`@marp-team/marp-cli`](https://github.com/marp-team/marp-cli) through `npm exec`. After approval, use:

```bash
SIGNALBRIEF_APPROVE_PACKAGE_INSTALL=1 ./skills/marp-slides/scripts/run-marp.sh <deck-file>
```

This is on demand and does not make a permanent global installation. If npm or network access is unavailable, create the deck source and explain that rendering could not run.

## Workflow

1. Use the completed research note as the authoritative source. Keep its evidence and caveats intact.
2. Read [`references/marp-style-guide.md`](references/marp-style-guide.md).
3. Save the deck beside the note as `<note-name>-slides.md`.
4. Create 5-8 slides: title, overview, focused findings, and a closing takeaway. Keep each slide readable in about 15 seconds.
5. Use `./skills/marp-slides/scripts/run-marp.sh --preview <deck>` only when the environment supports a local preview. Otherwise, render or export only when requested and supported.
6. Check the slide line budget in the style guide before reporting completion. Split or simplify crowded slides.

## Output

The deck must be valid Marp Markdown with `marp: true`, `theme: default`, and `paginate: true` in its front matter. It is a concise briefing, not a replacement for the research note.

## Attribution

This bundled workflow is adapted from material authored by Tyson Hummel.
