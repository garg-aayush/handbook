---
name: debug-issue
description: Debug errors using logs and stack traces. Use when the user shares an error message, crash log, or runtime issue to fix.
---

When debugging an issue:

1. **Check input**: If no error message or context files provided, ask the user to share logs and reference relevant files.

2. **Analyze root cause**: Briefly explain the issue based on stack trace and execution context. State your fix plan.

3. **Propose the fix**: Present the solution with code snippets. Wait for user confirmation before editing files.

4. **Scope limits**:
   - Only edit code causing the error—no unrelated refactoring
   - Add a one-line comment if the fix logic is non-obvious

5. **Handle missing context**:
   - **User file not in context**: Request the file
   - **External library error**: Fix the invocation in user code based on standard usage; if unfixable, explain and ask user to address it
