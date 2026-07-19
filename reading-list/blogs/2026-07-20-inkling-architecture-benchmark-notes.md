---
title: "Inkling: A New Open-Weight 975B MoE with a Few Surprises"
url: https://sebastianraschka.com/blog/2026/inkling-architecture-benchmark-notes.html
source: direct
tags: [architecture, mixture-of-experts, open-weights, long-context]
date_saved: 2026-07-20
---

TL;DR:
- Offers a benchmark-honest look at Inkling, a 975B sparse MoE (41B active) with a 1M-token context that trades chart-topping scores for a clean base model to fine-tune.
- Flags its unusual design choices: short kernel-4 convolutions for local token mixing, an extra RMSNorm right after the embeddings, and learned input-dependent relative-position bias instead of RoPE.
- Reads these as signals that architecture experimentation beyond the standard transformer recipe is still very much alive in open-weight models.

Related: [from-gpt-2-to-gpt-oss](2026-07-20-from-gpt-2-to-gpt-oss.md).
