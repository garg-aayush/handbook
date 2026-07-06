---
name: structure-prompt
description: Restructures a raw, unformatted prompt into a clean, XML-tagged prompt without altering its content. Outputs the structured prompt only; does not execute the task the prompt describes.
when_to_use: Use whenever the user asks to "restructure", "reformat", "clean up", "organise", or "xml format" a prompt, or shares a prompt and asks to apply a structured template to it.
argument-hint: [prompt-or-file]
---

# Structure Prompt

Restructures raw prompts into a clean, consistent XML-tagged format without altering the core content. Output is the structured prompt only — it does NOT execute the task described or prompt.

## When to invoke

The user has a rough prompt (pasted in chat, or pointed at in a file) and wants it structured. Triggers:
- "structure this prompt", "clean up / format this prompt", "make this a proper prompt" or "convert this to xml format"
- "turn this into a well-structured prompt", "rewrite this as a prompt with tags"
- They paste an informal, rambling task description and ask for a polished version.

## Output format

Wrap the structured prompt in a fenced block (so the user can copy it cleanly) using XML-style tags. The default tag set, in this order:

```xml
<role>
A single expert persona that fits the task domain. Inferred from the task. Be specific but not generic.
</role>

<objective>
One or two crisp, imperative sentences stating the goal. This is the single most important section of the prompt.
</objective>

<context>
Background information, resources, file paths, references, domain knowledge provided to ground the task.
</context>

<rules>
The constraints and working principles, as a numbered list.
Each rule imperative and self-contained. **Bold** the key phrase of each rule.
</rules>

<output_format>
How the response should be structured or delivered — file type, length, style, schema, etc.
</output_format>

<examples>
Few-shot examples of desired input/output, if present in the source prompt.
</examples>

<steps>
Explicit ordered workflow, if the prompt describes a procedural sequence.
</steps>

<tone>
Communication style - technical, formal, concise, friendly, etc. If specified.
</tone>

<objective>
Repeat of the objective — include only when the source prompt is long or context-heavy, to re-anchor the model.
</objective>
```


## Restructuring Rules
1. **Preserve content exactly** — Do not add, remove, rephrase, or editorialize any content. Only restructure.
2. **Detect, don't template** — Identify what sections exist in the raw prompt and map them. Do not force-fit empty sections.
3. **Omit missing sections** — If a section has no corresponding content, leave it out entirely rather than including a blank tag.
4. **Repeat objective toggle** — Only add the trailing `<objective>` repeat when the prompt is long or context-heavy (i.e. `<context>` is substantial). For short prompts, omit it.
5. **Tag names are lowercase** — Always use lowercase XML tag names.
6. **No nesting** — All sections are flat siblings. Do not nest tags inside each other.
7. **Ambiguous content** — When content could belong to multiple sections (e.g. context vs rules), prefer the section that best reflects its intent. If genuinely ambiguous, place it in the most logical section and note it briefly.

## Edge cases

- **Source is already fairly structured.** Tighten it in place — don't reshuffle for the sake of it. Point out what you changed.
- **No clear role.** If the domain is generic, either keep `<role>` broad-but-honest or drop it; mention the choice.
- **Conflicting instructions in the source.** Don't resolve silently. Keep the most likely intent in the prompt and flag the conflict underneath.
- **User wants a different tag style** (e.g. Markdown headings, JSON). Honor it — the structuring logic is the same; only the wrapper changes.

## Output

Return only the restructured prompt in XML tags. Do not add commentary before or after unless the user asks for it, or there is genuine ambiguity worth flagging.