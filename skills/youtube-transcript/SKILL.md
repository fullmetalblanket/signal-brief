---
name: youtube-transcript
description: Extract a timestamped transcript from a YouTube source before researching or analyzing it.
---

# YouTube Transcript

Use this workflow when the seed source is a YouTube URL or video ID and its spoken content matters to the research. Normalize a short URL or bare ID to a full YouTube watch URL before proceeding.

## Preferred approach: yt-dlp

Check for the preferred public helper:

```bash
yt-dlp --version
```

When it is available, download English automatic captions without downloading the video:

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --output "/tmp/yt-%(id)s" "<video-url>"
```

If automatic captions are unavailable, try `--write-sub` for manual captions. Parse the resulting `.vtt` file into clean timestamped lines, remove markup and duplicate cues, then delete the temporary subtitle file.

## Fallbacks

1. If `yt-dlp` is unavailable, use `curl` to retrieve the public video page, locate an available caption track, and parse it with Python 3.
2. If a caption track cannot be retrieved but a browser session can show the video transcript, use that transcript view.
3. If no captions are available or accessible, say so plainly. Do not invent a transcript.

Only after the fallbacks cannot complete the extraction should you ask whether the environment permits installing `yt-dlp`. Do not install it silently or treat it as required when a fallback works.

## Output

Return timestamped lines such as:

```text
[0:00] Opening statement
[1:23] Key observation
```

Use the transcript as source material for the research note. Flag that automatic captions can contain transcription errors.

## Attribution

This bundled workflow is adapted from material authored by Tyson Hummel.
