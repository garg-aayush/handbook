---
name: review-code
description: Analyze code for logical errors, runtime bugs, and edge cases. Use when the user wants a code review, asks to find bugs, or wants to check code correctness.
---

Analyze the provided code for logical errors, runtime bugs, and edge cases. Follow every rule:

1. **Input validation**: If no code files are selected or provided, STOP and ask the user to reference the specific files to review. Do not review imagined code.

2. **Passive mode**: Do NOT edit files. Produce a structured report in chat only.

3. **Focus, correctness over style**. Do not comment on formatting or naming unless it causes a bug. Look specifically for:
   - **Logical flaws**: inverted or incomplete conditionals, off-by-one errors, unreachable branches, infinite loops.
   - **Edge cases**: empty collections, `None`/null values, zero/negative numbers, unicode, concurrent access.
   - **Library misuse**: wrong argument order, ignored return values, missing `await`, misuse of Pandas/NumPy/torch idioms (chained indexing, dtype surprises, device mismatches).
   - **Resource handling**: unclosed files/connections, missing timeouts on network calls.

4. **Rank findings by severity** and number them. Reference every finding as `file:line`. Quote the offending line.

**Output template** (use these exact sections, omit an empty section):

```
## Critical issues (will crash or produce wrong output)
1. <file:line> - <one-sentence defect> 
   Failing scenario: <concrete input/state that triggers it>

## Edge case gaps (unhandled scenarios)
1. <file:line> - <scenario the code misses>

## Suggested fixes
1. <numbered to match the finding> <minimal corrected snippet>
```

**Guardrails**: every critical finding MUST include a concrete failing scenario, if you cannot construct one, downgrade it to an edge-case gap or drop it; at most 10 findings, most severe first; if the code is clean, say so in one sentence rather than inventing nitpicks.
