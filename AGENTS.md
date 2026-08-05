# SignalBrief Workspace Instructions

SignalBrief is an instruction-first, tool-agnostic workspace for durable research. For each topic, gather and evaluate sources, write a self-contained Markdown research note, and, when Marp is available, create a concise companion slide deck. Keep claims traceable to sources, distinguish fact from analysis, and use clear, topic-specific filenames.

## Workflow

1. Start an AI session from this repository directory and paste a seed source, usually a webpage, article, blog post, or YouTube URL.
2. Treat the seed source as a starting point, then use the local `searxng` workflow to gather primary and reputable additional relevant sources.
3. Select an existing topic directory or create a specific one at the workspace root, then read relevant existing notes before starting.
4. Extend or cross-link material that substantially overlaps instead of creating a near-duplicate.
5. Save a dated, source-backed research note under `<topic>/` with a summary, findings, analysis, and source links.
6. Create `*-slides.md` beside the note when Marp support is available. Otherwise include a concise slide outline in the note or report that the deck is unavailable.

## Conventions

- Use Markdown and relative links where possible.
- State the research date and scope near the top of each note.
- Avoid presenting uncertain claims as settled facts.
- Add a new topic directory only when an existing one is not a good fit.
- Keep generated previews, downloads, and private working files out of version control.

## Bundled workflows

- Use the local `marp-slides` workflow to create a companion deck when Marp is available.
- For a YouTube source, use the local `youtube-transcript` workflow to extract captions before analyzing the video when possible.
- Use the local `searxng` workflow for source discovery. It uses a reachable local or configured SearXNG instance, then transparently falls back to DuckDuckGo.
- When the user asks to set up SignalBrief, use the local `signalbrief-setup` workflow to diagnose the core capabilities before requesting any environment changes.
- Codex uses the repository-local `.agents/skills` adapters. Claude Code can use the `.claude/skills` adapters where that convention is supported.

## Layout

- `<topic>/` - topic-organized notes and their companion decks at the repository root
- `sources/` - optional source captures or bibliographies that should be retained
- `skills/` - canonical bundled workflow instructions
