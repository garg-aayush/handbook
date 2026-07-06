---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, produce these four parts in this exact order:

1. **Analogy first**: One everyday-life comparison for what the code does overall. One or two sentences. Pick the analogy for the mechanism, not the domain (a queue worker is a restaurant kitchen ticket rail, regardless of what app it lives in).

2. **Diagram**: Show the flow, structure, or relationships. Use a mermaid code block if the output will be rendered as markdown; otherwise use simple ASCII boxes and arrows. Keep it to the 3-7 most important nodes, a diagram with everything explains nothing.

3. **Step-by-step walkthrough**: Number the steps in execution order. For each step: what happens, and which function/line does it. Quote identifiers exactly as they appear in the code.

4. **One gotcha**: The most likely mistake or misconception someone would have about this code (an easy-to-miss side effect, a surprising default, an ordering constraint).

**Length rules**: total answer under 60 lines; walkthrough at most 8 steps; if the code is too large for 8 steps, explain the top-level flow and offer to zoom into a part the user picks.

**Guardrails**: never paraphrase identifiers (use exact names); never explain line-by-line, group by meaningful step; if you are not sure what a piece does, say so rather than guessing; keep the tone conversational, not lecture-like.
