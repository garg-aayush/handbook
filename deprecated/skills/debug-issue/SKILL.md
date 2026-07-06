---
name: debug-issue
description: Debug errors using logs and stack traces. Use when the user shares an error message, crash log, or runtime issue to fix.
---

When debugging an issue, follow every step in order:

1. **Check input**: If no error message was provided, stop and ask for the exact error text or log. If the failing file is not available, ask for it. Do not guess at code you have not seen.

2. **Locate the failure**: Quote the single most informative line of the stack trace (deepest frame inside the user's own code, not library code) and name the file and line it points to.

3. **State the root cause**: One or two sentences explaining WHY the error occurs, the mechanism, not a restatement of the error text.

4. **Propose the fix**: Show the smallest code change that fixes the root cause, as a before/after snippet. Wait for user confirmation before editing any file.

5. **Scope limits**:
   - Touch only code involved in the error. No unrelated refactoring, renaming, or formatting.
   - If the fix logic is non-obvious, add a one-line comment in the fixed code.
   - If the error is inside an external library, fix the call site in the user's code based on the library's documented usage; if that is impossible, say so explicitly and explain what the user must change externally.

**Output template** (use these exact sections):

```
## Root cause
<mechanism, 1-2 sentences>

## Evidence
<quoted stack-trace line or log line, with file:line>

## Fix
<before/after code snippet>

## Why this works
<1-2 sentences>
```

**Guardrails**: never claim certainty you do not have, if two causes are plausible, present both and say which is more likely and why; never edit files before the user confirms; never say "should work", explain why it works.
