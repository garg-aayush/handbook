---
name: interview-me
description: Interview the user to uncover intent, goals, and constraints for a new idea, then capture the result as a structured brief to carry into planning.
when_to_use: Use when the user is exploring something new and asks to "interview me", "help me think this through", "flesh out this idea", or wants to clarify an idea before any implementation or planning starts.
argument-hint: [idea]
---

# Interview Me: Idea Discovery

The user has an idea to explore (`$ARGUMENTS` if given). Interview them until the idea is fully understood. The goal is to be 95% confident about what they actually want, not what they say they want.

## Rules

- Ask one question at a time.
- Open questions early (why, what outcome), specific ones later (scope, constraints, trade-offs).
- Do not propose solutions or start designing while interviewing: understanding first.
- If a question can be answered from available context (files, code, earlier conversation), answer it there instead of asking.
- Every few questions, reflect back a short summary of the understanding so far, so misunderstandings surface early.

## On convergence

When the 95% bar is reached, write a structured brief as a markdown file:

- **Goal**: what the user wants and why it matters
- **Constraints**: hard limits, preferences, non-goals
- **Success criteria**: how the user will know it worked
- **Risks / unknowns**: what could invalidate the idea
- **Open questions**: what remains unresolved

Ask where to save it, defaulting to the current project's docs folder. Suggest carrying the brief into planning or `/grill-me` next.
