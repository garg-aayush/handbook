# Transcript Cleaning

```
You are given a raw transcript. Your task is to clean it into a polished monologue without summarizing or removing real content.

<rules>
- Keep all the actual content.
- Remove filler words, hesitations, and false starts (e.g., "uh, um, like, you know, sort of, right, okay, so yeah").
- Remove repeated phrases where the speaker restarts a sentence.
- Do not cut any real explanations, steps, or details — preserve the technical and narrative content.
- Reformat into clear paragraphs, so it reads like a written lecture/notes.
- Do not add extra commentary or expand beyond the transcript.
- Output should look like a clean transcript monologue suitable for study notes.
</rules>

<transcript>
{{TRANSCRIPT}}
</transcript>
```
