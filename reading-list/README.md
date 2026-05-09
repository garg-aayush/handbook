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
```

## File format

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
