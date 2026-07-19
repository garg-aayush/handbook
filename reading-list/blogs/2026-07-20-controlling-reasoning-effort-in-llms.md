---
title: "Controlling Reasoning Effort in LLMs"
url: https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms
source: direct
tags: [reasoning, test-time-compute, think-tokens, inference-time-scaling]
date_saved: 2026-07-20
---

TL;DR:
- Frames reasoning effort as a controllable knob: models are trained to support on/off thinking or graded low-to-high effort, trading inference cost against answer quality.
- Clarifies that the think delimiters are just formatting learned via SFT and RL rewards; they organise the trace but are not what creates the reasoning ability.
- Highlights that a smaller model run at higher effort can sometimes rival a larger model at lower effort, which matters for cost-aware deployment.

Related: [understanding-reasoning-llms](2026-07-20-understanding-reasoning-llms.md).
