# SignalBrief

Every research note is paired with a concise Marp slide deck for rapid comprehension. The note preserves evidence, nuance, and links. The deck turns the same work into an easy-to-scan briefing.

SignalBrief is a reusable, instruction-first workspace for AI-assisted research that remains useful after the chat ends. Start an AI session from this repository directory and paste a seed source, usually a webpage, article, blog post, or YouTube URL. The workspace instructions treat that source as a starting point, gather additional relevant sources, write a research note, and create a companion Marp deck where supported. An open-ended topic or question is also supported when there is no seed source.

## Quick start

1. Clone or copy this repository, then start your preferred AI assistant with this repository as its working directory.
2. Paste a seed source into the session, usually a webpage, article, blog post, or YouTube URL.
3. The assistant reads [AGENTS.md](AGENTS.md), uses the seed source to gather and assess additional relevant sources, and writes a Markdown research note in a topic directory at the repository root.
4. When Marp is supported in that environment, it also creates a concise `*-slides.md` deck beside the note.

You can instead provide an open-ended topic or question when you do not have a seed source.

For example:

> Start with https://example.com/article. Gather additional relevant sources, then create `example-topic/example-topic.md` with the scope, research date, summary, key findings, analysis, and sources. If Marp is available in this environment, also create `example-topic/example-topic-slides.md`. Clearly label uncertainty and distinguish source-backed facts from synthesis.

## Two ways to learn from the same research

**New to the topic:** start with the deck for orientation, then read the full research note and follow its sources for evidence and detail.

**Already familiar with the topic:** use the deck as an efficient update on one specific area, then open the note only where you need context, methodology, or citations.

## Workspace template versus optional capabilities

The repository is the portable workflow and structure. It does not require a particular AI product, extension, skill package, search tool, or hosted service. Optional capabilities can make parts of the workflow faster, but they depend on the AI environment and what its user has installed or configured.

| Capability | What it enables | When it applies | How to obtain it | Fallback |
| --- | --- | --- | --- | --- |
| Marp slides | A companion Markdown slide deck and, where supported, rendered slides | After a research note is ready for a concise briefing | Use Marp support, an extension, or a skill available for your chosen AI environment | Keep a short slide outline in the note, or create a plain Markdown summary |
| YouTube transcripts | Searchable spoken content from a video | When a video is a research source | Use a transcript feature, service, or skill supported by your chosen AI environment | Cite the video and use available captions, notes, or other published sources |

## Workspace layout

```text
topic-name/
  topic-name.md
  topic-name-slides.md
sources/
```

## What to commit

Commit research notes, companion deck source files, and curated bibliographies that can be shared. Keep generated slide exports, downloaded media, caches, local settings, and temporary scratch work untracked unless the repository intentionally needs them.
