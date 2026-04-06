# Prompt Library

Reusable prompts and prompt templates for daily use with LLMs.

## Prompts

| File | Description | Variants |
|------|-------------|----------|
| [proofreading.md](proofreading.md) | Proofread and rewrite messages, posts, and text | Basic, With Context, Posts, Fix & Rewrite |
| [learn-topic.md](learn-topic.md) | Explain a new topic for beginners | Basic, Jeremy Howard Style |
| [meeting-summary.md](meeting-summary.md) | Summarize meeting transcripts | Quick, Structured |
| [youtube-summarizer.md](youtube-summarizer.md) | Summarize YouTube videos from transcripts | Single variant |
| [prompt-fragments.md](prompt-fragments.md) | Reusable prefixes, suffixes, and anecdotes | Clarify Intent |

## Format Guide

Each file follows this structure:

```
# Prompt Category Title

## Variant Name
` `` `
Prompt text here.

<input_section>
{{PLACEHOLDER}}
</input_section>
` `` `
```

- One file per prompt category (e.g., proofreading, meeting summaries)
- Use `## Heading` for each prompt variant within a file
- Wrap prompts in fenced code blocks
- Use XML tags (`<tag>`) to separate input sections and output format
- Use `{{PLACEHOLDER}}` for variable inputs
- Keep descriptions outside code blocks to a minimum
