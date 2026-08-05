# SignalBrief Marp Style Guide

Use a light editorial deck that prioritizes source-backed clarity over decoration.

## Front matter

```yaml
---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: Arial, sans-serif;
    background: #faf8f3;
    color: #1a1a1f;
    font-size: 24px;
    padding: 40px 50px;
  }
  section.lead {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
  section.lead h1, section h2 { color: #224466; }
  .callout {
    background: #faf0e8;
    border-left: 4px solid #b5451f;
    padding: 0.8em 1.2em;
  }
---
```

## Structure

- Use `<!-- _class: lead -->` for the first and final slides.
- Put one idea on each slide. Prefer brief bullets, simple tables, or small comparison cards.
- Cite or attribute claims in speaker-note comments when the deck compresses a source-heavy point.

## Line budget

Keep every slide at or below 16 line-equivalents:

| Element | Cost |
| --- | --- |
| Title | 2 lines |
| Short bullet | 1.5 lines |
| Wrapping bullet | 2.5 lines |
| Paragraph | 2 lines |
| Callout | 3 lines |
| Table row | 1.5 lines |

Split or simplify a slide that exceeds the budget. Overflow makes a deck unusable.
