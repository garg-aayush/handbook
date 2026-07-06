---
name: commit-message
description: Generate commit messages for staged git changes. Use when the user asks to generate a commit message or wants help writing commit messages.
---

When generating commit messages, follow every step in order:

1. **Check for staged changes**: Run `git diff --cached --stat`. If nothing is staged, stop and tell the user to stage changes first with `git add`. Do not invent a message.

2. **Match the repo's convention**: Run `git log --oneline -10`. If recent messages use a prefix convention (`feat:`, `fix:`, `chore:`), use the same convention. If not, use plain sentences.

3. **Review the changes**: Run `git diff --cached`. Base the message ONLY on what this diff actually contains, never on what the user says they intended but did not stage.

4. **Choose the format**:
   - One logical change: single line, max 50 characters.
   - Multiple significant changes: summary line, then blank line, then at most 3 bullets, each a short phrase of 3-6 words prefixed with "- ".

5. **Apply the style rules**: present tense, active voice ("Add X", not "Added X" or "Adds X"), specific ("Fix null check in login handler", not "Fix bug").

6. **Output**: present the message in a fenced code block and nothing else after it. Do not run `git commit` unless the user explicitly asks.

**Examples**

Single-line:
```
feat: add JWT validation to login endpoint
```

Multi-line:
```
refactor: overhaul user authentication

- add JWT validation middleware
- update login and signup endpoints
- hash passwords with bcrypt
```

**Guardrails**: never mention files that are not in the staged diff; never exceed 50 characters on the summary line; never use passive voice; never add a body when one bullet would restate the summary.
