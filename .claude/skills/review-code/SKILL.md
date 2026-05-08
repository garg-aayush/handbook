---
name: review-code
description: Analyze code for logical errors, runtime bugs, and edge cases. Use when the user wants a code review, asks to find bugs, or wants to check code correctness.
---

Analyze the provided code for logical and code errors, potential runtime bugs, and edge cases.

## Rules

- **Input Validation**: If no code files are selected or provided in context, STOP and ask the user to reference the specific files they want reviewed.
- **Focus Area**: Prioritize **Correctness** over **Style**. Do not nitpick formatting (PEP8) unless it impacts readability. Focus on:
    - **Logical Flaws**: Incorrect conditional logic, off-by-one errors, or infinite loops.
    - **Edge Cases**: Handling of empty lists, `None` values, or unexpected data types.
    - **Library Usage**: Correct implementation of external libraries (e.g., Pandas, NumPy, OpenCV, torch, etc.) functions.
- **Passive Mode**: Do **NOT** edit the files directly. Provide a structured text-based report in the chat.
- **Output Structure**:
    1.  **Critical Issues**: Bugs that will definitely cause a crash or wrong output.
    2.  **Edge Case Gaps**: Scenarios the code currently misses.
    3.  **Suggested Fixes**: Code snippets showing how to correct the logic.