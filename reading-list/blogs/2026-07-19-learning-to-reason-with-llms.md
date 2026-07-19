---
title: "Learning to Reason with LLMs"
url: https://openai.com/index/learning-to-reason-with-llms/
source: direct
tags: [reasoning, chain-of-thought, reinforcement-learning, test-time-compute, o1]
date_saved: 2026-07-19
---

OpenAI's announcement of o1, a model trained with large-scale reinforcement learning to reason via a long internal chain of thought before answering.

Key points:
- Trained with RL to produce a chain of thought; it learns to break problems into steps, recognize and correct its own mistakes, and try alternative approaches.
- Performance scales along two axes: more train-time RL compute and more test-time "thinking" compute both reliably improve accuracy.
- Headline results: 89th percentile on Codeforces competitive programming, among the top 500 students in the US on the AIME qualifier, and above PhD-level human accuracy on the GPQA Diamond science benchmark.
- Large jump over GPT-4o on hard math, coding, and science reasoning.
- The raw chain of thought is kept hidden from users in the product; only a summary is surfaced.
- Introduced alongside o1-mini, a cheaper reasoning-focused variant.

Foundational reference for the test-time-compute / reasoning-model line of work. Related: [post-training-rl](../post-training-rl.md).
