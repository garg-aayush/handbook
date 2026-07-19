---
title: "From GPT-2 to gpt-oss: Analyzing the Architectural Advances"
url: https://magazine.sebastianraschka.com/p/from-gpt-2-to-gpt-oss-analyzing-the
source: direct
tags: [architecture, gpt-oss, mixture-of-experts, transformers, quantization]
date_saved: 2026-07-20
---

TL;DR:
- Traces the architectural path from GPT-2 to gpt-oss: dropping dropout, moving to RoPE, SwiGLU, and RMSNorm, then adding mixture-of-experts and grouped-query attention for efficiency.
- Covers deployment-focused touches like sliding-window attention, attention sinks, and MXFP4 quantization that let the 120B model run on a single GPU.
- Compares gpt-oss (wider, fewer but larger experts) against Qwen3 (deeper, more but smaller experts) to illustrate the width-versus-depth trade-off.

Related: [inkling-architecture-benchmark-notes](2026-07-20-inkling-architecture-benchmark-notes.md).
