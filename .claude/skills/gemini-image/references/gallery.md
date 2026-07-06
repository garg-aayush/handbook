# Curated prompt gallery (Gemini / Nano Banana)

These entries are starting points to adapt (swap the bracketed or `{...}` slots and adjust flags to your case); load only the category section you need instead of the whole file.

## Photorealistic scenes

### 2005 digicam mall snapshot
- Source: [Marky @ Easy-Peasy.AI](https://x.com/easy_peasy_ai/status/1996232508162310472) via [dahaltn/awesome-nano-banana-pro-prompts](https://github.com/dahaltn/awesome-nano-banana-pro-prompts)
- Suggested flags: `--model flash --aspect 4:3 --resolution 1K`
- Pattern: Name a specific camera, era, and processing artifacts (flash, noise, date stamp) to force believable amateur realism instead of glossy AI perfection.

```
A low-resolution digital photo taken on a 2005 Sony CyberShot. A group of teenagers hanging out in a mall food court. Harsh on-camera flash, slightly blown-out highlights, digital noise in the shadows. The skin texture looks slightly waxy due to early digital processing. An orange date stamp appears in the bottom right corner reading "{argument name="date stamp in english" default="04/12/2005"}". Candid, awkward angles, Myspace photo aesthetic.
```

### Structured JSON landscape spec (alpine village)
- Source: [Emily](https://x.com/IamEmily2050/status/1984628556262228365) via [antifragile0/Awesome-Nano-Banana-Prompts](https://github.com/antifragile0/Awesome-Nano-Banana-Prompts)
- Suggested flags: `--model pro --aspect 9:16 --resolution 2K`
- Pattern: Full JSON scene spec that separates environment, lighting, camera, style, and negative prompt into keyed sections you can swap independently.

```
{
  "prompt_name": "High Alpine Sanctuary Village",
  "aesthetic_goal": "epic fantasy realism, ultra clear daylight, cinematic natural beauty, impossibly pristine and peaceful",
  "scene": {
    "environment": "steep emerald-green mountain terraces with bright mossy grass and scattered pink alpine flowers, layered with old trees and cliffs",
    "architecture": "small wooden highland houses and temples built on stone foundations, handcrafted timber, weathered roofs, clustered on ledges and plateaus",
    "background_scale": "towering icy mountain peak with dramatic ridgelines and snow, sharp sunlight hitting glacier edges, long depth all the way to the summit",
    "atmosphere": "thin mountain air, cool blue clarity, low drifting clouds and mist wrapping around the slopes, untouched sacred place",
    "tone": "utopian, peaceful, ancient, safe"
  },
  "lighting": {
    "style": "bright clean midday sunlight from upper right, high-elevation alpine light",
    "shadow_behavior": "soft but defined terrain shadows, gentle falloff into the valleys",
    "color_temperature": "cool sky blue mixed with fresh spring green bounce light from grass",
    "mood": "fresh, crisp, holy air feeling"
  },
  "camera": {
    "framing": "cinematic aerial wide shot looking slightly downward across the terraces toward the snow mountain in the distance",
    "lens": "full-frame equivalent ~18mm ultra wide landscape lens, deep depth of field",
    "focus": "sharp across entire frame, no blur, extreme detail in foliage, stone, wood, and snow texture",
    "composition_notes": "village in lower/mid frame leading the eye up the valley toward the sacred peak in the top of frame"
  },
  "style": {
    "keywords": [
      "fantasy landscape realism",
      "4K cinematic environment",
      "photoreal terrain detail",
      "lush micro-detail vegetation",
      "studio-grade color grading"
    ],
    "color_palette": "saturated alpine greens, icy whites, sky-deep cobalt blues"
  },
  "output_settings": {
    "aspect_ratio": "9:16",
    "format": "high detail still image",
    "quality_target": "ultra high resolution, sharp, no noise"
  },
  "negative_prompt": [
    "blurry, low detail, washed out, haze blocking the mountain",
    "cartoon, anime, game UI, infographic style",
    "text, captions, watermarks, logos, interface elements",
    "distorted perspective, warped buildings, melted terrain",
    "oversaturated neon color, unnatural purple grass, plastic look"
  ]
}
```

## Posters and typography

### City vector travel poster with exact title text
- Source: [@michaelrabone](https://x.com/michaelrabone/status/1913865394139316291) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model pro --aspect 2:3 --resolution 1K`
- Pattern: Minimal poster one-liner that pins the exact display text in quotes plus its placement; swap city/country for any subject (food, movies, music).

```
Barcelona Spain colourful summer vector art poster with big "BARCELONA" title at the top and smaller "SPAIN" title under
```

### Vintage patent document
- Source: [Alexandra Aisling](https://x.com/AllaAisling/status/2004212035333365763) via [YouMind-OpenLab/awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- Suggested flags: `--model pro --aspect 3:4 --resolution 2K`
- Pattern: Aged-document mockup where numbered figures, handwritten annotations, paper wear, and official seals sell the artifact for any invention slot.

```
A vintage patent document for {argument name="invention" default="INVENTION"}, styled after late 1800s United States Patent Office filings. The page features precise technical drawings with numbered callouts (Fig. 1, Fig. 2, Fig. 3) showing front, side, and exploded views. Handwritten annotations in fountain-pen ink describe mechanisms. The paper is aged ivory with foxing stains and soft fold creases. An official embossed seal and red wax stamp appear in the corner. A hand-signed inventor's name and date appear at the bottom. The entire image feels like a recovered archival document—authoritative, historic, and slightly mysterious.
```

### Minimalist ad with real object and hand-drawn doodle
- Source: [@azed_ai](https://x.com/azed_ai/status/1923016036120658122) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model pro --aspect 1:1 --resolution 1K`
- Pattern: Bracketed slots ([Real Object], [Doodle Concept], [Ad Copy], [Brand Logo]) turn one ad-layout scaffold into an endlessly reusable template.

```
A minimalist and creative advertisement set on a clean white background.
A real [Real Object] is integrated into a hand-drawn black ink doodle, using loose, playful lines. The [Doodle Concept] interacts with the object in a clever, imaginative way. Include bold black [Ad Copy] text at the top or center. Place the [Brand Logo] clearly at the bottom. The visual should be clean, fun, high-contrast, and conceptually smart.
```

## Product photography and mockups

### Branded mechanical keycaps
- Source: [@egeberkina](https://x.com/egeberkina/status/1918291652210311278) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model pro --aspect 1:1 --resolution 2K`
- Pattern: Curly-brace slots for brand, words, and colors inside a fixed studio-render scaffold; exact printed text makes this a pro-tier job.

```
ultra-realistic 3D render of four mechanical keyboard keycaps in a tight 2x2 grid, all keys touching. View from an isometric angle. One key is transparent with the word “{just}” printed in {white}. The other three colors are: {black, purple, and white}. One key features the {Github} logo. The other two say "{fork}" and "{it}". Realistic plastic texture, rounded sculpted keycaps, soft shadows, clean light-gray background.
```

### Miniature product held between fingers
- Source: [@azed_ai](https://x.com/azed_ai/status/1962878353784066342) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model flash --aspect 1:1 --resolution 1K`
- Pattern: A [PRODUCT] placeholder inside a fixed luxury ad-photography scaffold; the tiny-scale trick makes any product read as premium and hero-lit.

```
A high-resolution advertising photograph of a realistic, miniature [PRODUCT] held delicately between a person's thumb and index finger.  clean and white background, studio lighting, soft shadows. The hand is well-groomed, natural skin tone, and positioned to highlight the product’s shape and details. The product appears extremely small but hyper-detailed and brand-accurate, centered in the frame with a shallow depth of field. Emulates luxury product photography and minimalist commercial style.
```

## Diagrams and infographics

### Liquid glass Bento grid product infographic
- Source: [Mansi Sanghani](https://x.com/MansiSanghani1/status/2013550795224961492) via [YouMind-OpenLab/awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- Suggested flags: `--model pro --aspect 16:9 --resolution 2K`
- Pattern: Modular card-by-card infographic spec with per-category data slots; change only the input variable and the whole layout regenerates coherently.

```
Input Variable: [insert product name]
Language: [insert language]

System Instruction:
Create an image of premium liquid glass Bento grid product infographic with 8 modules (card 2 to 8 show text titles only).
1) Product Analysis:
→ Identify product's dominant natural color → "hero color"
→ Identify category: FOOD / MEDICINE / TECH
2) Color Palette (derived from hero):
→ Product + accents: full saturation hero color
→ Icons, borders: muted hero (30-40% saturation, never black)
3) Visual Style:
→ Hero product: real photography (authentic, premium), 3D Glass version [choose one]
→ Cards: Apple liquid glass (85-90% transparent) with Whisper-thin borders and Subtle drop shadow for floating depth and reflecting the background color
→ Background stays behind cards and high blur where cards are [choose one]:
  - Ethereal: product essence, light caustics, abstract glow
  - Macro: product texture close-up, heavily blurred
  - Pattern: product repeated softly at 10-15% opacity
  - Context: relevant environment, blurred + desaturated
→ Add subtle motion effect
→ Asymmetric Bento grid, 16:9 landscape
→ Hero card: 28-30% | Info modules: 70-72%
4) Module Content (8 Cards):
M1 — Hero: Product displayed as real photo / 3D glass / stylized interpretation (choose one)in beautiful form + product name label
M2 — Core Benefits: 4 unique benefits + hero-color icons
M3 — How to Use: 4 usage methods + icons
M4 — Key Metrics: 5 EXACT data points
Format: [icon] [Label] [Bold Value] [Unit]
FOOD: Calories: [X] kcal/100g, Carbs: [X]g (fiber [X]g, sugar [X]g), Protein: [X]g, [Key Vitamin]: [X]mg ([X]% DV), [Key Mineral]: [X]mg ([X]% DV)
MEDICINE:Active: [name], Strength: [X] mg, Onset: [X] min, Duration: [X] hrs, Half-life: [X] hrs 
TECH:Chip: [model], Battery: [X] hrs, Weight: [X]g,[Key spec]: [value], Connectivity: [protocols]
M5 — Who It's For: 4 recommended groups with green checkmark icons | 3 caution groups with amber warning icons
M6 — Important Notes: 4 precautions + warning icons
M7 — Quick Reference:
→ FOOD: Glycemic Index + dietary tags with icons
→ MEDICINE: Side effects + severity with icons
→ TECH: Compatibility + certifications with icons
M8 — Did You Know: 3 facts (origin, science, global stat) + icons
Output: 1 image, 16:9 landscape, ultra-premium liquid glass infographic.
```

### Glowing-line anatomy diagram
- Source: [@umesh_ai](https://x.com/umesh_ai/status/1914644426334314545) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model flash --aspect 4:3 --resolution 1K`
- Pattern: [SUBJECT] and [PART] slots in a consistent x-ray visual language, with a single red-glow accent to direct attention to the point of interest.

```
A digital illustration of a [SUBJECT], portrayed with a network of glowing clean pristine blue lines outlining its anatomy. The image is set against a dark background, highlighting the [SUBJECT] form and features. A specific area such as [PART] is emphasized with a red glow to indicate a point of interest or significance. The style is both educational and visually captivating, designed to resemble an advanced imaging technique
```

### Flowchart from a source document
- Source: [@anderssandberg](https://x.com/anderssandberg/status/1992259420118724677) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model pro --aspect 16:9 --resolution 2K`
- Pattern: Point the model at real source material (a cited paper or pasted text) and let it design the diagram; the model handles layout and labels itself.

```
The diagram illustrates the process of constructing a Dyson swarm based on the paper Armstrong, S., & Sandberg, A. (2013). Eternity in six hours: Intergalactic spreading of intelligent life and sharpening the Fermi paradox. Acta Astronautica, 89, 1-13.
```

## Character and portrait design

### RPG collectible character card
- Source: [@berryxia_ai](https://x.com/berryxia_ai/status/1911334046724165905) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model pro --aspect 2:3 --resolution 1K`
- Pattern: A profession slot plus fixed card furniture (stat bars, title banner, nameplate) yields a consistent series across any set of roles.

```
Create a digital character card in RPG collectible style.
The subject is a {Programmer}, standing confidently with tools or symbols relevant to their job.
Render it in 3D cartoon style, soft lighting, vivid personality.
Include skill bars or stats like [Skill1 +x], [Skill2 +x, e.g., Creativity +10, UI/UX +8].
Add a title banner on top and a nameplate on the bottom.
Frame the card with clean edges like a real figure box.
Make the background fit the profession's theme.
Colors: warm highlights, profession-matching hues.
```

### Character design sheet from one reference
- Source: [@ZHO_ZHO_ZHO](https://x.com/ZHO_ZHO_ZHO/status/1960669234276753542) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model pro --aspect 16:9 --resolution 2K`
- Pattern: Checklist of standard sheet components (proportions, turnarounds, expressions, poses, costumes) applied to one uploaded character reference image.

```
Generate character design for me (Character Design)

Proportion design (different height comparisons, head-to-body ratio, etc.)

Three views (front, side, back)

Expression design (Expression Sheet) → like the image you sent

Pose design (Pose Sheet) → various common poses

Costume design (Costume Design)
```

## Image editing (input image + instruction)

### Photo to character figurine
- Source: [@ZHO_ZHO_ZHO](https://x.com/ZHO_ZHO_ZHO/status/1958539464994959715) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model flash --aspect 1:1 --resolution 1K`
- Pattern: The classic "turn this photo into X" edit, made convincing by meta-props (packaging box, modeling software on screen) that reference the source subject.

```
turn this photo into a character figure. Behind it, place a box with the character's image printed on it, and a computer showing the Blender modeling process on its screen. In front of the box, add a round plastic base with the character figure standing on it. set the scene indoors if possible
```

### Map screenshot to ancient treasure map
- Source: [@umesh_ai](https://x.com/umesh_ai/status/1919701229363466328) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model flash --aspect 4:3 --resolution 1K`
- Pattern: "Transform the image to <style>" plus an explicit list of style-native elements to add; works on any uploaded map or screenshot.

```
Transform the image to an ancient treasure map drawn on aged parchment. The map includes detailed elements like sailing ships on the ocean, old ports or castles on the coastline, a dotted path leading to a large 'X' marking the treasure spot, mountains, palm trees, and a decorative compass rose. The overall style is reminiscent of old pirate adventure films.
```

### Floor plan to isometric 3D render
- Source: [@op7418](https://x.com/op7418/status/1961329148271513695) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model flash --aspect 1:1 --resolution 2K`
- Pattern: One-sentence domain conversion (schematic to photoreal 3D) that relies on the model reading the uploaded diagram's structure faithfully.

```
Convert this residential floor plan into an isometric, photo-realistic 3D rendering of the house.
```

## Multi-image composition

### Multi-reference scene assembly
- Source: [@MrDavids1](https://x.com/MrDavids1/status/1960783672665128970) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model pro --aspect 3:4 --resolution 1K`
- Pattern: Name every uploaded reference object and state its spatial relation to the others so they merge into one coherent scene.

```
A model is posing and leaning against a pink bmw. She is wearing the following items, the scene is against a light grey background. The green alien is a keychain and it's attached to the pink handbag. The model also has a pink parrot on her shoulder. There is a pug sitting next to her wearing a pink collar and gold headphones.
```

### OOTD outfit transfer (person + clothing images)
- Source: [302.AI](https://medium.com/%40302.AI/google-nano-banana-vs-qwen-gpt-flux-topping-the-image-editing-leaderboard-96038b01bdcd) via [PicoTrex/Awesome-Nano-Banana-images](https://github.com/PicoTrex/Awesome-Nano-Banana-images)
- Suggested flags: `--model pro --aspect 2:3 --resolution 1K`
- Pattern: Address inputs as "Image 1" / "Image 2" and state explicitly what to keep (identity, pose) versus what to take (clothing, accessories).

```
Choose the person in Image 1 and dress them in all the clothing and accessories from Image 2. Shoot a series of realistic OOTD-style photos outdoors, using natural lighting, a stylish street style, and clear full-body shots. Keep the person's identity and pose from Image 1, but show the complete outfit and accessories from Image 2 in a cohesive, stylish way.
```

## 3D, miniature and stylized art

### Chibi brand concept store
- Source: [@dotey](https://x.com/dotey/status/1995190286775881780) via [antifragile0/Awesome-Nano-Banana-Prompts](https://github.com/antifragile0/Awesome-Nano-Banana-Prompts)
- Suggested flags: `--model flash --aspect 2:3 --resolution 1K`
- Pattern: Brand-parameterized miniature diorama where the building exterior is derived from the brand's most iconic product; fill the slots, keep the scaffold.

```
{Brand Name}

--- Prompt ---

3D chibi-style miniature concept store of {Brand Name}, creatively designed with an exterior inspired by the brand's most iconic product or packaging (such as a giant {brand's core product, e.g., chicken bucket/hamburger/donut/roast duck}). The store features two floors with large glass windows clearly showcasing the cozy and finely decorated interior: {brand's primary color}-themed decor, warm lighting, and busy staff dressed in outfits matching the brand. Adorable tiny figures stroll or sit along the street, surrounded by benches, street lamps, and potted plants, creating a charming urban scene. Rendered in a miniature cityscape style using Cinema 4D, with a blind-box toy aesthetic, rich in details and realism, and bathed in soft lighting that evokes a relaxing afternoon atmosphere. --ar 2:3

Brand name: Starbucks
```

### Isometric city weather card
- Source: [@dotey](https://x.com/dotey/status/1917988595228438771) via [JimmyLv/awesome-nano-banana](https://github.com/JimmyLv/awesome-nano-banana)
- Suggested flags: `--model pro --aspect 1:1 --resolution 1K`
- Pattern: Data-display hybrid: a miniature landmark city, a weather effect blended into it, and exact overlay text; swap city, weather, and temperature.

```
Show a clear 45-degree bird’s-eye view of an isometric miniature city scene featuring Shanghai’s iconic buildings, such as the Oriental Pearl Tower and the Bund. The weather effect—cloudy—blends softly into the city, interacting gently with the architecture. Use physically based rendering (PBR) and realistic lighting. Solid color background, crisp and clean. Centered composition to highlight the precision and detail of the 3D model. Display “Shanghai Cloudy 20°C” and a cloudy weather icon at the top of the image.
```

### Ukiyo-e reinterpretation of a modern scene
- Source: [VoxcatAI](https://x.com/VoxcatAI/status/1995497350543110411) via [YouMind-OpenLab/awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)
- Suggested flags: `--model pro --aspect 3:4 --resolution 2K`
- Pattern: Style-transformation ruleset: explicit mapping rules for how each modern element becomes a period equivalent, plus physical-print texture constraints.

```
A Japanese Edo-period Ukiyo-e woodblock print. The overall feeling is a surreal collaboration between masters like Hokusai and Hiroshige, reimagining modern technology through an ancient lens.

**The scene:** {argument name="modern scene" default="a busy Shibuya scramble crossing"}

**Edo transformation logic:**
Characters wear Edo-era kimono but perform modern actions. All technology is transformed into surreal Edo equivalents:
* Smartphones are glowing, illustrated paper scrolls being read intently.
* Metro stations and trains are giant articulated wooden centipede carriages shuffling through crowds.
* Skyscrapers are reimagined as endless, towering wooden pagodas reaching into dramatic clouds.
* Robots and mecha appear as giant, armored woodblock golems.

The composition uses a flattened perspective with large, bold, hand-carved ink outlines. The background features heavily stylized Ukiyo-e wave patterns and dramatic, swirling clouds, with a distant Mt. Fuji visible on the horizon.

The image must look like a physical print, not a digital painting.
* Texture: strong visible wood grain texture and rough paper fibers throughout the piece.
* Printing imperfections: pigment bleeding is evident. Simulate hand-pressed plates with slight color misalignment for authenticity.
* Color palette: strictly limited to traditional mineral pigments, with dominant use of Prussian blue, vermilion red, and muted yellow ochre.
* Lighting: soft, flat, shadow-free lighting with no digital gradients.

Aspect ratio is 3:4 vertical poster. Include vertical Japanese calligraphy describing the scene and a traditional red artist seal stamp in a corner.
```
