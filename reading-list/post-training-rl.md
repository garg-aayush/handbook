# Post-training and Reinforcement Learning approaches

A curated learning path for RL-based LLM post-training (RLHF, DPO, PPO, GRPO), ordered roughly foundations to frontier.

## Books
- [RLHF Book by Nathan Lambert](https://rlhfbook.com/): A short introduction to RLHF and post-training focused on language models

## Blogs
- [Introduction to LLMs post training](https://tokens-for-thoughts.notion.site/post-training-101): Guide to understanding the basics of LLM post-training
- [KL Divergence Approximations by John Schulman](http://joschu.net/blog/kl-approx.html): Practical insights on approximating KL divergence in policy optimization
- [Understanding GRPO by Cameron R. Wolfe](https://substack.com/home/post/p-177823868): Deep dive into GRPO mechanics and implementation
- [SAPO: Soft Adaptive Policy Optimization](https://qwen.ai/blog?id=sapo): Introduction to SAPO by the Qwen team

### My Posts
- [Deriving the PPO Loss](https://aayushgarg.dev/posts/2025-12-25-deriving-ppo-loss.html): First principles derivation of the PPO loss function
- [Deriving the DPO Loss](https://aayushgarg.dev/posts/2025-12-30-deriving-dpo-loss.html): First principles derivation of the DPO loss function
- [Understanding GRPO](https://aayushgarg.dev/posts/2026-01-01-understanding-grpo.html): First principles derivation of the GRPO loss function

## Papers

### PPO
- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) ([HF Paper](https://huggingface.co/papers/1707.06347)): The foundational PPO paper introducing the clipped surrogate objective
- [Training language models to follow instructions with human feedback](https://arxiv.org/pdf/2203.02155) ([HF Paper](https://huggingface.co/papers/2203.02155)): The InstructGPT paper demonstrating PPO with KL penalty to mitigate reward hacking in LLM fine-tuning
- [Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477) ([HF Paper](https://huggingface.co/papers/1502.05477)): The TRPO paper that motivates the trust region constraints used in PPO
- [High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) ([HF Paper](https://huggingface.co/papers/1506.02438)): GAE paper introducing the exponentially-weighted advantage estimator for variance reduction in policy gradients

### DPO
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) ([HF Paper](https://huggingface.co/papers/2305.18290)): The original DPO paper
- [Rank analysis of incomplete block designs: I. The method of paired comparisons](https://www.jstor.org/stable/2334029): The Bradley-Terry model for pairwise comparisons

### GRPO
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300) ([HF Paper](https://huggingface.co/papers/2402.03300)): The original GRPO paper
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) ([HF Paper](https://huggingface.co/papers/2501.12948)): DeepSeek's reasoning model trained with GRPO

### Other Papers
- [RLVR: Reinforcement Learning with Verifiable Rewards](https://arxiv.org/abs/2506.14245) ([HF Paper](https://huggingface.co/papers/2506.14245)): RL method using verifiable rewards
- [Soft Adaptive Policy Optimization (SAPO)](https://arxiv.org/abs/2511.20347) ([HF Paper](https://huggingface.co/papers/2511.20347)): SAPO offers a more scalable and reliable foundation for RL-tuning large language and multimodal models by replacing hard clipping with smooth, temperature-controlled gating

## Videos
- [Umar Jamil's video on RLHF and PPO](https://www.youtube.com/watch?v=qGyFrqc34yc): Comprehensive and must-watch video covering RLHF and PPO concepts
- [Umar Jamil's video on DPO](https://www.youtube.com/watch?v=hvGa5Mba4c8): Excellent walkthrough of the DPO derivation
