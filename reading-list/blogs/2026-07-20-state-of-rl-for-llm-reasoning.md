---
title: "The State of Reinforcement Learning for LLM Reasoning"
url: https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training
source: direct
tags: [reasoning, reinforcement-learning, grpo, rlvr, deepseek-r1]
date_saved: 2026-07-20
---

TL;DR:
- Traces how RL became central to reasoning, moving from RLHF and PPO to GRPO (which drops the critic model) and RLVR (which rewards verifiable outputs from tools like compilers and calculators).
- Walks the DeepSeek-R1 pipeline across its R1-Zero, R1, and distilled variants to show how pure RL, SFT plus RL, and distillation differ in practice.
- Distills the practical lessons: response-length bias needs mitigating, small models do benefit from RL, and reasoning likely arises through several paths rather than RL alone.

Related: [post-training-rl](../post-training-rl.md).
