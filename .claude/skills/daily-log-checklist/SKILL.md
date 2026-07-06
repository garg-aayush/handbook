---
name: daily-log-checklist
description: Convert a daily log file's bullet points into a structured checklist (checkbox, short title, description, status per item), editing the file in place.
when_to_use: Use when the user asks to "convert my daily log", "turn this log into a checklist", "checklist-ify this file", or wants log bullets restructured into trackable checklist items.
argument-hint: [log-file]
context: fork
agent: general-purpose
model: haiku
effort: medium
allowed-tools: Read, Edit
---

# Daily Log → Checklist Converter

Convert the target file's bullet points into the checklist format below, editing the file in place.

The target file is `$ARGUMENTS` if provided, otherwise the file currently open in the IDE. If neither is available, do not guess: stop and reply that a target file path is needed.

## Format for each item

```
- [ ] **<Short title, max 10 words>**
  Description: <Original content, cleaned up as a concise 1-2 sentence description>
  Status: Pending
  Notes: 
```

Status values: `Pending` | `In Progress` | `Done` | `Blocked`  
Default: `Pending`  
Notes: leave blank, the user fills this in later.

## Rules

- Edit the file in place.
- Do not add items that aren't in the original log.
- Do not reorder items.
- If an item already has the checklist format (checkbox + bold title + Status line), leave it as-is.
- Preserve all date headings and any structure outside the bullets.
- Keep descriptions factual: only tighten loose speech, don't paraphrase.
