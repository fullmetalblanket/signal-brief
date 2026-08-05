# SignalBrief Workspace Instructions

SignalBrief is an instruction-first, tool-agnostic workspace for durable research. For each topic, gather and evaluate sources, write a self-contained Markdown research note, and, when Marp is available, create a concise companion slide deck. Keep claims traceable to sources, distinguish fact from analysis, and use clear, topic-specific filenames.

## Workflow

1. Start an AI session from this repository directory and paste a seed source, usually a webpage, article, blog post, or YouTube URL.
2. Treat the seed source as a starting point, then gather primary and reputable additional relevant sources appropriate to it.
3. Use an open-ended topic or question when there is no seed source.
4. Read existing material in the closest topic directory before starting.
5. Save the research note under `<topic>/` with a summary, findings, analysis, and source links.
6. Create `*-slides.md` beside the note when Marp support is available. Otherwise include a concise slide outline in the note or report that the deck is unavailable.
7. Keep generated previews, downloads, recordings, and private working files out of version control.

## Conventions

- Use Markdown and relative links where possible.
- State the research date and scope near the top of each note.
- Avoid presenting uncertain claims as settled facts.
- Add a new topic directory only when an existing one is not a good fit.

## Layout

- `<topic>/` - topic-organized notes and their companion decks at the repository root
- `sources/` - optional source captures or bibliographies that should be retained
