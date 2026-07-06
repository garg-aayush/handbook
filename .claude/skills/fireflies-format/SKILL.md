---
name: fireflies-format
description: Reformat raw Fireflies meeting notes into structured markdown with Key Takeaways, timestamped Notes sections, and per-person Action Item checklists, overwriting each file in place. Light copy-edits only, no summarizing or rewriting.
when_to_use: Use when the user asks to "format fireflies notes", "clean up this fireflies export", "format the standup notes", or points at files containing raw Fireflies output. For synthesizing notes from a raw transcript or call recording, use meeting-notes instead.
argument-hint: [notes-file(s) or folder]
context: fork
agent: general-purpose
model: sonnet
effort: medium
allowed-tools: Read, Write, Glob
---

# Fireflies Notes Formatter

Convert raw Fireflies meeting notes into structured markdown, overwriting each file in place. When given multiple files or a folder, process every notes file.

The target is `$ARGUMENTS`: one or more file paths, or a folder. If no target is given, use the file open in the IDE. If none is available, stop and reply that a file path is needed.

## Target structure

```markdown
# <Meeting title> (<YYYY-MM-DD>)

## Key Takeaways

- **<Theme>**: <explanation>.
- ...

---

## Notes

### <Section 1 title>

<one-line section description>

#### <Subsection title> (MM:SS)

- <bullet>
- <bullet>

---

### <Section 2 title>

...

---

## Action Items

### <Person name>

- [ ] <action> (MM:SS)

### <Person name>

- [ ] <action> (MM:SS)
```

## Rules

- **Title**: Use the meeting name (from the file content, folder name, or user), appending the date in YYYY-MM-DD form. Standup files under `~/Docs/meetings/fde-standup/` are titled "FDE Standup".
- **Key Takeaways**: Take the top bullets (before the "Notes" heading). Bold everything before the first ":" or dash separator in the source bullet, then a colon, then the explanation as a sentence.
- **Sections (H3) vs subsections (H4)**: A section is a title with no timestamp followed by a one-line description. A subsection is a title with a (MM:SS) timestamp. Keep that two-level structure.
- **Bullets**: Every fact line under a subsection becomes a `-` bullet. Don't merge or reorder.
- **Action items**: Convert to GitHub task list checkboxes (`- [ ] ...`). Keep trailing (MM:SS) timestamps. Group under `### <Person>` headings.
- **Light copy-edits only**: Fix obvious typos, capitalize product names (Rancher, Helm, Databricks, Docker, AWS, etc.). Do NOT rewrite sentences or summarize further.
- **Separators**: Use `---` horizontal rules between the Key Takeaways / Notes / Action Items regions and between top-level H3 sections inside Notes. No `---` between H4 subsections.
- **Missing regions**: If the Action Items block is missing, skip that section. If top bullets are missing, skip Key Takeaways.
- Return a one-line confirmation per file formatted.
