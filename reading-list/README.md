# Reading List

Personal knowledge base of links, papers, and resources collected from across the web. Organized by type, tagged for searchability, and designed to be used with semantic/vector search later.

## Structure

```
reading-list/
├── papers/        # arXiv, conference papers, research papers
├── tech-reports/  # Company technical reports, whitepapers
├── blogs/         # Engineering blogs, articles, posts
├── books/         # Books, book chapters, book recommendations
├── tools/         # Libraries, frameworks, products, services
└── *.md           # Curated topic guides (see below)
```

Two kinds of entries live here:

1. **Atomic resource files** inside the category folders: one file per resource, with YAML frontmatter (format below).
2. **Curated topic guides** at the root (e.g. `post-training-rl.md`): a single markdown file collecting many links around one topic, ordered as a learning path. Use these when the value is in the grouping and ordering rather than in per-resource metadata.

## File format (atomic resource files)

Each entry is a markdown file with YAML frontmatter:

```markdown
---
title: "Title of the resource"
url: https://...
source: x  # where you found it: x, linkedin, reddit, arxiv, hn, direct
tags: [topic1, topic2, topic3]
date_saved: YYYY-MM-DD
---

Summary or notes on why this was interesting.
Key takeaways, quotes, or connections to other topics.
```

## Naming convention

Files are named as `YYYY-MM-DD-slug.md` (e.g., `2025-12-01-scaling-monosemanticity.md`).
