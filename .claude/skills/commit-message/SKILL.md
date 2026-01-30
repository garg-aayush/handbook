---
name: commit-message
description: Generate commit messages for staged git changes. Use when the user asks to generate a commit message or wants help writing commit messages.
---

When generating commit messages:

1. **Check for staged changes first**: Run `git diff --cached --stat`. If nothing is staged, inform the user to stage changes first with `git add`.

2. **Review the changes**: Use `git diff --cached` to understand what changed.

3. **Choose the format**:
   - **Simple changes**: Single-line message (max 50 characters) for simple changes
   - **Complex changes**: Multi-line format (max 4 lines) for complex changes ONLY when there are multiple significant updates

4. **Multi-line structure**:
   - Line 1: Summary of all changes (high-level overview)
   - Lines 2-4: Bullet points with "- " prefix
     - Short phrases (3-6 words each)
     - Maximum 3 bullet points
     - Focus on most significant changes

5. **Present in a code block** for easy copying.

**Style rules**: Present tense, active voice, concise, specific.

**Examples**:

Single-line:
```
Add user authentication to login endpoint
```

Multi-line:
```
Refactor user authentication system
- Add JWT token validation middleware
- Update login and signup endpoints
- Implement password hashing with bcrypt
```
