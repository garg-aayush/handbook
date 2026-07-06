# Official Gemini image prompting templates

Source: https://ai.google.dev/gemini-api/docs/image-generation (captured 2026-07-04; re-check the page if outputs drift). Fill-in-the-blank structures from Google's own prompting guide. For battle-tested community patterns (edit invariants, scene density, negation), see `craft.md`.

## 1. Photorealistic scenes

"A photorealistic [type of shot] of a [subject description] in a [setting description]. [Description of the light]. Shot from a [camera angle] with a [lens type]."

## 2. Stylized illustrations

"A [style] of a [subject, with details about accessories or actions] doing [activity]. The design features [visual qualities]."

## 3. Accurate text in images

"Create a [image type] for [brand/concept] with the text '[text to render]' in a [font style]. The design should be [style], with a [color scheme]."

Prefer the `pro` model for text-heavy output.

## 4. Product mockups

Lead with "high-resolution, studio-lit product photograph", then specify the lighting setup (e.g. three-point softbox), camera angle, surface/backdrop, and the focus point.

## 5. Minimalist / negative space

"A minimalist composition featuring a single [subject] positioned in the [location] of the frame. The background is a vast, empty [color] canvas." Useful for slide backgrounds and text overlays; pair with `--aspect wide`.

## 6. Sequential art (comic / storyboard)

"Make a [N] panel comic in a [style]. Put the character in a [type of scene]." Specify the exact panel count and shared art direction so panels stay consistent.

## 7. Search-grounded generation

gemini-3.1-flash-image supports Google Search grounding for current-events/real-world content; mention the real subject and timeframe explicitly in the prompt.

## Editing patterns (official)

The guide covers: element addition/removal, inpainting by description (no mask; describe the region in words), style transfer ("render this photo as [style]"), multi-image composition, and detail preservation ("keep the [element] exactly as in the input"). The invariant-pinning discipline for edits is expanded in `craft.md`.
