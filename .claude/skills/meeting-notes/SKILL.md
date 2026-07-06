---
name: meeting-notes
description: Generate structured notes from a transcript, Slack summary, huddle recording, or call log. Handles messy auto-generated transcripts, reconstructs meaning from context, and writes the finished notes to a markdown file.
when_to_use: Use when the user says "meeting notes", "summarize this call", "transcribe this", "create summary for this transcript", or uploads a document with timestamped dialogue.
argument-hint: [transcript-file]
---

# Meeting Notes Generator

Generate clean, structured, actionable meeting notes from raw or auto-generated transcripts.

> For raw Fireflies exports that only need reformatting (not synthesis), use the `fireflies-format` skill instead.

## Core Principles

1. **Reconstruct meaning, don't transcribe literally.** Auto-generated transcripts are full of errors. Use context, domain knowledge, and surrounding sentences to infer what was actually said. Flag genuinely ambiguous terms rather than guessing silently.

2. **Separate signal from noise.** Most transcript volume is filler ("yeah, yeah, yeah"), repetition, and crosstalk. Extract the substantive points and discard the rest.

3. **Preserve attribution.** Track who said what, who owns which action, and who raised which concern. This matters for accountability.

4. **Capture decisions AND the reasoning behind them.** A decision without context is useless in 2 weeks. Include why something was decided, not just what.

5. **Surface what the transcript buries.** The most important insight in a meeting is often stated once, casually, between filler. Elevate these.

## Output Structure

Use this structure for every set of meeting notes. Omit sections that don't apply (e.g., no "Scheduling" section if nothing was discussed).

```markdown
# Meeting Notes — [Meeting Title / Participants]

**Date:** [Date]
**Participants:** [Names, noting absent parties who were expected]

---

## Summary
[3-5 sentence executive summary. Lead with the most important outcome or decision.
State what changed as a result of this meeting — what do people know or believe
now that they didn't before?]

---

## Key Discussion Points

### 1. [Topic Title]
[Prose summary of the discussion. Include:
- What was discussed and concluded
- Key data points or evidence cited
- Disagreements or alternative views
- Analogies or examples used to explain concepts (these often clarify intent)]

### 2. [Topic Title]
[...]

---

## Action Items

| # | Owner | Action | Status/Due |
|---|-------|--------|------------|
| 1 | Name | Specific, verifiable action | Open / Due date |

---

## Open Questions / Blockers
- [Question or blocker, with context on why it matters]

---

## Key Takeaway
[Optional. Use when the meeting produced a single insight that reframes
the project or changes the team's direction. Not every meeting has one.]
```

## Processing Rules

### Handling Transcription Errors
- Auto-generated transcripts frequently mangle technical terms. Infer the correct term from context. Examples from real transcripts:
  - "compensation model" → likely "composition model" or another domain term
  - "receive tags" → "tags with sign inconsistencies requiring clarification"
  - "possessions" → "persistence" (baseline model)
  - "ten minutes gardens" → "10-minute windows"
- When genuinely ambiguous, note it: *"[term unclear from transcript — likely refers to X]"*

### Handling Slack/AI Summaries Provided Alongside Transcripts
- If the user provides a pre-generated summary (e.g., from Slack), treat it as a **reference to validate**, not as ground truth.
- Cross-check every claim against the actual transcript.
- Correct errors in the generated summary (wrong terms, missing context, misattributed actions).
- Add points the generated summary missed.
- Don't include claims from the generated summary that aren't supported by the transcript.

### Identifying Action Items
- Explicit commitments: "I will do X", "Can you handle Y", "Let's do Z"
- Implicit commitments: When someone agrees to investigate something or says "let me check"
- Distinguish between: action items (someone will do something), open questions (no one has the answer yet), and blockers (something is preventing progress)

### Handling Multi-Person Meetings
- Track the dynamic: who is explaining, who is asking, who is pushing back
- When someone raises a concern or pushback, capture it even if the group moves past it — it often resurfaces later
- Note when someone is assigned ownership of a workstream

### Tone and Style
- Write in professional prose, not bullet-heavy formatting
- Use technical terms accurately but explain niche domain concepts briefly on first mention
- Keep the summary tight (3-5 sentences) — someone should be able to read just the summary and know what happened
- Action items must be specific enough that someone can verify completion
- Don't editorialize in the main notes — save interpretive comments for the "Key Takeaway" section

## Output Destination

Write the finished notes to a markdown file by default:

- If the transcript came from a file, write `<transcript-name>-notes.md` next to it.
- Otherwise default to `~/Docs/meetings/<meeting-or-project>/<YYYY-MM-DD>.md`, inferring the folder from the meeting context; ask only if genuinely unclear.
- Output notes in chat instead only when the user explicitly asks for them in chat.

## After Generating Notes

Once the notes are generated, briefly flag (outside the document):
- Any transcription errors you corrected and why
- Key points that were buried in the transcript but elevated in the notes
- Anything ambiguous you interpreted — give the user a chance to correct

