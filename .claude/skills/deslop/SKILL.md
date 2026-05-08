---
name: deslop
description: Remove AI-generated code slop from files. Use when cleaning up excessive comments, defensive code, or style inconsistencies. Can target specific files or all changes in a branch.
---

When deslopping code:

1. **Determine scope**:
   - **Specific files**: If user provides file paths, clean those files
   - **All changes**: If user says "all" or "all changes", run `git diff <base-branch>...HEAD --name-only` to get changed files
   - **Base branch**: Default to `main`, but use specified branch if mentioned (e.g., "against develop")

2. **Identify AI slop patterns**:
   - Excessive comments that humans wouldn't write or are inconsistent with the file
   - Over-defensive code (unnecessary try/catch, null checks in trusted paths)
   - Type workarounds (`as any` casts instead of proper types)
   - Verbose code that doesn't match codebase style

3. **Clean the code**:
   - Read each file to understand existing patterns
   - Remove slop while preserving functionality
   - Match the existing code style
   - Be conservative - when in doubt, keep it

4. **Report briefly**: Provide a 2-4 sentence summary of what was changed.

**Examples**:

Specific file:
```
User: "deslop src/api.ts"
→ Read file, remove slop, report changes
```

All changes:
```
User: "deslop all changes"
→ Run: git diff main...HEAD --name-only
→ Clean each changed file
→ Report summary
```

Custom base branch:
```
User: "deslop all against develop"
→ Run: git diff develop...HEAD --name-only
→ Clean each changed file
→ Report summary
```
