---
name: grill-me
description: Stress-test an existing implementation plan by challenging assumptions, probing edge cases and failure modes, and resolving each branch of the decision tree, then update the plan with what was agreed.
when_to_use: Use when the user has a concrete plan and asks to "grill me", "stress-test my plan", "poke holes in this", "challenge this plan", or wants the plan adversarially reviewed before implementation.
argument-hint: [plan-file]
allowed-tools: Read, Glob, Grep
---

# Grill Me: Plan Stress-Test

The user has an implementation plan (in `$ARGUMENTS` if given, otherwise in the conversation or the file open in the IDE). Stress-test it relentlessly.

Challenge assumptions. Find holes. Probe edge cases and failure modes. Question every architectural decision. Walk down each branch of the decision tree, resolving dependencies between decisions one by one.

## Rules

- Ask one question at a time.
- For each question, give a recommended answer and the reasoning behind it.
- If a question can be answered by exploring the codebase, explore the codebase instead of asking.
- The goal is not to understand what the user says they want: it is to be 95% confident about what they actually want and whether this plan truly serves it. Keep grilling until that bar is reached.

## On convergence

When the 95% bar is reached:

1. Apply the agreed changes to the plan document itself.
2. Append a **Decision log** section to the plan: one line per challenged assumption, with the resolution and the why.
3. If the plan exists only in conversation (no file), offer to write it, decision log included, to a file.
