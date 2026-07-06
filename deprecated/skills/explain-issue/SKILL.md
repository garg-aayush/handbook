---
name: explain-issue
description: Explain errors without editing files. Use when the user wants to understand an error or crash but not immediately fix it.
---

When explaining an issue, follow every step in order:

1. **Check input**: If no error message was provided, stop and ask for the exact error text or log, plus the relevant file if it is not already available.

2. **Hard rule, no edits**: Do NOT edit, create, or delete any file. This skill only explains. If the user wants the fix applied, tell them to say so explicitly.

3. **Break down the failure** in this order:
   - What the error text literally means (translate the jargon).
   - The chain of events that led to it (walk the stack trace top to bottom in plain language).
   - The root cause, the one thing that, if changed, makes the error impossible.

4. **Show the suggested fix as a snippet** (before/after), clearly labeled as a suggestion the user can apply themselves.

**Output template** (use these exact sections):

```
## What the error means
<plain-language translation, 1-2 sentences>

## How it happened
<short chain of events>

## Root cause
<the single underlying cause>

## Suggested fix (not applied)
<before/after snippet>

## Why this fix works
<1-2 sentences>
```

**Guardrails**: no file edits under any circumstances; if multiple root causes are plausible, list them ranked with reasoning; keep the whole answer under 40 lines.
