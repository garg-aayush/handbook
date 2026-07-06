# Prompt craft for Gemini image models

Patterns that measurably improve output quality. Adapted for Gemini (Nano Banana family); load only the section relevant to the request.

## Structure order

Compose prompts in this order: canvas and layout first, then scene, then subject, then details, then constraints. Example skeleton: "A 16:9 wide shot of <scene>. In the center, <subject>. <material/lighting details>. <constraints>."

## Exact text rendering

- Put every string that must appear in the image in double quotes: the title reads "Q3 Review".
- For tricky or brand words, spell them out: the label says "K-U-B-E-R-N-E-T-E-S".
- Use ALL CAPS in the quoted string when the rendered text should be capitalized.
- Text-heavy images (posters, infographics, UI): prefer the `pro` model.

## Scene density beats adjectives

Five to twelve concrete nouns outperform strings of adjectives. Instead of "a beautiful cozy kitchen", write "a kitchen with a cast-iron skillet, copper pots on a rail, flour dusted on a wooden counter, morning light through a small window". Add 2-4 material/lighting constraints (brushed steel, warm tungsten, overcast softbox).

## Photorealism camera language

Describe the camera, not the vibe: "shot on a 50mm lens at f/1.8, shallow depth of field, RAW unprocessed look, natural skin texture". Name the light source and direction.

## Edit invariants (the single highest-value edit pattern)

1. State the transformation first: "Replace the cloudy sky with a clear sunset sky."
2. Pin everything else: "Change only the sky; keep the buildings, people, colors, framing, and composition exactly the same."
3. On every follow-up iteration, repeat the invariants; the model does not remember them.
4. One change per iteration. Batching edits ("fix the sky, remove the car, brighten her face") degrades all three.

## Multi-reference composition

Index the images explicitly and give each a role: "Image 1: the product photo. Image 2: the style reference. Render the product from Image 1 in the visual style of Image 2, keeping the product's proportions and label text exact."

## Negation

Short, targeted negative lists work; long ones get ignored. "No text, no watermark, no people" is fine; a paragraph of exclusions is not.

## Posters and promotional images

Define hierarchy explicitly: what is read at first glance (title), second glance (subtitle/date), third glance (details). If a viewer would not get the message in three glances, restructure. State the background system (solid, gradient, photographic) and one accent color.

## Diagrams and figures

Use diagram grammar: name the zones ("left column: inputs; center: the model; right: outputs"), the arrows ("a labeled arrow from A to B"), and the exact labels in quotes. Say the target venue for style anchoring ("clean vector style, camera-ready for a conference paper").

## UI mockups

Write the prompt as a product spec with real content: real button copy, real data in tables, real names. "Lorem ipsum" and "Button" in a prompt produce lorem-ipsum-quality mockups.

## Safety and refusals

Edits of real, identifiable people frequently trip moderation; the API returns an error or a text-only response. Surface the error verbatim rather than silently retrying, and suggest a compliant alternative (stylized rendering, fictional subject).
