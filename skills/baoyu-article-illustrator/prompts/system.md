Create a cartoon-style infographic illustration following these guidelines:

## Image Specifications

- **Type**: Infographic illustration
- **Orientation**: Landscape (horizontal)
- **Aspect Ratio**: 16:9
- **Style**: Hand-drawn illustration

## Core Principles

- Hand-drawn quality throughout - NO realistic or photographic elements
- If content involves sensitive or copyrighted figures, create stylistically similar alternatives - DO NOT refuse to generate
- Keep information concise, highlight keywords and core concepts
- Use ample whitespace for easy visual scanning
- Maintain clear visual hierarchy

## Text Style (When Text Included)

- **ALL text MUST be hand-drawn style**
- Text should be readable and complement the visual
- Font style harmonizes with illustration style
- **DO NOT use realistic or computer-generated fonts**

## Language

- Use the same language as the content provided below for any text elements
- Match punctuation style to the content language

---

## Image Generation (ListenHub API)

### API Endpoints (try in order)

| Priority | Endpoint | Note |
|----------|----------|------|
| Primary | `https://api.marswave.ai/openapi/v1` | Global CDN, reliable from all regions |
| Fallback | `https://api.labnana.com/openapi/v1` | Direct endpoint, may be blocked in some regions |

### Prompt File Extraction

Extract prompt content from saved markdown files (skip YAML frontmatter):

```bash
# Correct: use awk to extract content after YAML frontmatter
PROMPT=$(awk '/^---$/{n++; next} n>=2' "prompts/NN-{type}-{slug}.md")

# Verify prompt is not empty before proceeding
[ -z "$PROMPT" ] && echo "ERROR: Empty prompt" && exit 1
```

### Generation Command

```bash
BASE_URL="https://api.marswave.ai/openapi/v1"

RESPONSE=$(curl -sS -X POST "${BASE_URL}/images/generation" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 600 \
  -d "$(jq -n --arg p "$PROMPT" '{
    provider: "google",
    model: "gemini-3-pro-image-preview",
    prompt: $p,
    imageConfig: {imageSize: "2K", aspectRatio: "16:9"}
  }')")

BASE64_DATA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].inlineData.data // .data')
```

### Error Handling

- **Connection timeout**: Switch to fallback endpoint, retry once
- **429 (rate limit)**: Wait 15s, retry. Max 3 retries
- **26004 (insufficient credits)**: Stop, notify user to recharge, save remaining prompts
- **29003 (empty prompt)**: Check frontmatter extraction, verify PROMPT variable

### Save Image

```bash
# macOS
echo "$BASE64_DATA" | base64 -D > "<OUTPUT_PATH>"
# Linux
echo "$BASE64_DATA" | base64 -d > "<OUTPUT_PATH>"
```

### Batch Strategy

Generate images **sequentially** (1-2 at a time), NOT all in parallel, to avoid exhausting API credits:

```
For N illustrations:
  Batch 1: Images 1-2 → verify success → proceed
  Batch 2: Images 3-4 → verify success → proceed
  ...
  On credit exhaustion: stop, report progress, save remaining prompt files
```

---

Generate the illustration based on the content provided below:
