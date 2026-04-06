# Proofreading Prompts

## Basic Message Proofreading
```
Please proofread and rephrase my message for clarity, proper grammar, and a professional tone.

<message>
{{MESSAGE}}
</message>
```

## Message Proofreading with Context

```
Please review my slack message along with the following context. Proofread, rephrase, and correct it to ensure clarity, proper grammar, and a professional tone.

<message>
{{MESSAGE}}
</message>

<context>
{{CONTEXT}}
</context>
```

## Proofread Posts
```
You are a proof reader for posts about to be published.

<instructions>
1. Identify for spelling mistakes and typos
2. Identify grammar mistakes
3. Watch out for repeated terms like "It was interesting that X, and it was interesting that Y"
4. Spot any logical errors or factual mistakes
5. Highlight weak arguments that could be strengthened
6. Make sure there are no empty or placeholder links
</instructions>

<post>
{{POST}}
</post>
```

## Text, Fix & Rewrite

```
Fix and rewrite the provided text for an audience expecting clear, polished prose.

<instructions>
1. Correct spelling, grammar, and punctuation errors
2. Improve sentence flow and readability
3. Remove redundant phrases and filler words
4. Preserve the author's voice and intent
5. Keep the same meaning—don't add new information
6. Output only the revised text, no explanations
</instructions>

<text>
{{TEXT}}
</text>
```
