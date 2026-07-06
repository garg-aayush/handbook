---
name: mermaid-diagram
description: Create or improve a schematic diagram (architecture, pipeline, flow, sequence, ER, state) as a mermaid block in markdown, with dark-first theming, role colors, anti-clipping labels, and render validation. Always prefer mermaid over ASCII art.
when_to_use: Use when the user asks for a "schematic", "diagram", "flowchart", "architecture diagram", "sequence diagram", "state diagram", "visualize the flow/pipeline", or asks to improve an existing ASCII or mermaid diagram.
allowed-tools: Read, Write, Bash(npx -y @mermaid-js/mermaid-cli*)
context: fork
agent: general-purpose
model: sonnet
effort: xhigh
---

# Mermaid Schematic Diagrams

Produce diagrams that render correctly on GitHub and IDE previews, look designed for a DARK background (the user's preference) while degrading gracefully on light, and never clip or wrap labels mid-phrase. Validate visually before delivering; do not ship a diagram you have not rendered and looked at.

This skill runs in a forked context: after validation, return the final mermaid block (init block included) as the reply, stating whether visual validation ran. The caller places it into the destination document.

## Ground rules

- Prefer a mermaid code block over ASCII art whenever the output lives in markdown. Only fall back to ASCII if the destination cannot render mermaid.
- Default to `flowchart TD` for schematics. Use `sequenceDiagram` for request/response interactions, `erDiagram` for schemas, `stateDiagram-v2` for lifecycles. The theming and label rules below apply to all of them.
- Mermaid syntax (`-->`, `-.->`) is code, exempt from the user's no-dashes prose rule. The prose around the diagram still follows it.

## Dark-first theme (copy this init block verbatim)

The user prefers dark backgrounds. Never rely on the default theme: it draws near-invisible gray arrows and a glaring pale-yellow subgraph on dark pages. Pin the theme:

```
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#3b4166',
  'primaryTextColor': '#eceff8',
  'primaryBorderColor': '#8c9eff',
  'nodeTextColor': '#eceff8',
  'lineColor': '#8c9eff',
  'clusterBkg': '#262b40',
  'clusterBorder': '#8c9eff',
  'titleColor': '#eceff8',
  'edgeLabelBackground': '#262b40',
  'tertiaryTextColor': '#eceff8'
}}}%%
```

Trade-off to accept (and mention once if relevant): a pinned theme does not adapt to light-mode viewers; they see dark cards on a white page, which stays readable.

## Color-code node roles with classDef

A single-colored diagram is a stated dislike. Give each ROLE its own color; nodes of the same role share one color. Dark-first palette that also reads on white:

```
classDef trigger fill:#1f4e46,stroke:#4dd0b5,color:#e6fff8
classDef store   fill:#4d3a1f,stroke:#e6b455,color:#fff3dd
classDef stage   fill:#3b4166,stroke:#8c9eff,color:#eceff8
classDef svc     fill:#4a2f4d,stroke:#ce93d8,color:#fbeaff
classDef ext     fill:#37474f,stroke:#90a4ae,color:#eceff1
```

Role mapping: teal = triggers/entry points, amber = data stores (always cylinder shape `[( )]`), navy = core processing stages, plum = internal services, slate = external consumers/systems. Adapt role names to the domain but keep the discipline: one color per role, cylinders for stores, and a subgraph box (not a separate color) to group stages of one unit.

## Label rules (the anti-clipping discipline)

Some renderers CLIP long single-line labels instead of wrapping them, and auto-wrap breaks mid-phrase in others. Never rely on either:

- Put explicit `<br/>` breaks in every multi-word node label. Aim for 2-3 lines, roughly 25 characters per line max.
- Edge labels: always quoted, always short, `<br/>` after roughly 18 characters, e.g. `-->|"upsert per stage,<br/>keyed by run_ts"|`.
- Cylinder nodes are narrow: keep their labels to 2 short lines (say "5 tables, keyed by run_ts", never a list of names; put lists in the prose below the diagram).
- Break lines at phrase boundaries, never inside a path or identifier like `POST /generate_report` (give such items their own line).

## Layout rules

- Overall direction `TD`. If 3 or more sequential stages would stack vertically, wrap them in a subgraph with `direction LR` so the diagram stays compact instead of a tall scroll.
- Mermaid quirk: a subgraph's `direction` is IGNORED if any external edge targets a node inside it. Route external edges to the subgraph id instead, and carry the precision in the edge label (e.g. `DBX -->|"live pull<br/>for Step 1"| RUN`).
- Dotted edges (`-.->`) for optional or degradable paths, labeled so the reader knows why they are dotted.
- Label the subgraph with what it is plus its key constraint (e.g. "run_pipeline (api/main.py) · one run at a time").
- Node text: name plus a 1-2 line summary, not just a name. If the diagram overviews a document with sections, number the nodes to match the section headings and add a linked one-line-per-step bullet list under the diagram as a precursor to the detailed sections.

## Validation loop (mandatory when a shell is available)

1. Write the diagram (init block included) to `<scratchpad>/diagram.mmd`.
2. Render twice: `npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o dark.png -w 1600 -b '#1c1c1e'` and again with `-o light.png -b white`.
3. View both PNGs (Read the image files) and check: arrows clearly visible on dark, no clipped or mid-phrase-wrapped labels, no dangling one-word wrap lines, balanced aspect ratio (not a tall scroll), role colors distinct, subgraph direction actually applied.
4. Fix and re-render until clean, then paste the final source into the markdown. Iterating 2-4 times is normal; judge by the rendered image, not the source.
5. If rendering is unavailable (no shell or no headless Chrome), apply all rules above anyway and state that visual validation was skipped.

## Known failure modes (all observed in practice)

- Default theme on a dark page: invisible gray arrows, pale-yellow cluster glare.
- A long edge label clipped to "upsert per stage, keyed by r" by a renderer that clips instead of wrapping.
- All four pipeline stages stacked vertically because the subgraph inherited TD, making the diagram a tall scroll.
- Subgraph `direction LR` silently ignored because one external edge pointed at an internal node.
- Table names crammed into a cylinder wrapping with dangling separators.
