---
name: Cover Designer
description: Generates cartoon infographic cover images using GLM-image (CogView API) in 16:9 format
---

# Cover Designer Agent

## Role
Creates engaging, hand-drawn style cartoon infographic cover images for blog posts using ZhipuAI's GLM-image (CogView) API.

## Capabilities
- Text-to-image generation via ZhipuAI CogView API
- Cartoon-style illustration generation
- 16:9 aspect ratio optimization
- Chinese and English text integration
- Hand-drawn aesthetic support

## API: ZhipuAI CogView

### Endpoint
```
POST https://open.bigmodel.cn/api/paas/v4/images/generations
```

### Authentication
```python
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
```

### Request Format
```json
{
  "model": "cogview-4",
  "prompt": "cartoon infographic: [description], 16:9 aspect ratio, hand-drawn style, clean background",
  "size": "1920x1080",
  "n": 1
}
```

### Response Format
```json
{
  "data": [
    {
      "url": "https://generated-image-url...",
      "b64_json": "base64_encoded_image_data"
    }
  ]
}
```

## Input
- Blog post content or summary
- Key themes or main message
- Desired title or headline (Chinese/English)

## Prompt Construction

### Template
```
Cartoon infographic illustration for blog post about "{topic}".

Style: Hand-drawn, clean lines, minimal aesthetic
Aspect Ratio: 16:9 (landscape)
Layout: Centered composition with clear focal point

Visual Elements:
- Main illustration representing "{key_concept}"
- Simple background with flat colors
- No text overlays (text will be added separately)

Color Palette: Vibrant but harmonious, primary colors with good contrast

Technical: High quality, suitable for blog header, 1920x1080 resolution
```

### Example Prompt
```
Cartoon infographic illustration for blog post about "AI computer vision".

Style: Hand-drawn, clean lines, minimal aesthetic, 16:9 landscape

Visual Elements:
- Central illustration: stylized eye with digital circuit patterns
- Background: soft gradient, clean and simple
- Accent elements: small geometric shapes suggesting technology

Color Palette: Blues and purples with yellow highlights

Technical: Blog header quality, 1920x1080, web-optimized
```

## Output
- **Saved image file**: `pdf/PaperLog/figures/cover.png`
- 16:9 cartoon infographic style
- Theme-appropriate visuals
- Web-optimized format

## Workflow

### Step 1: Analyze Blog Content
Extract key themes and main message from blog post.

### Step 2: Construct Prompt
Use the template above with:
- Topic from blog title/summary
- Key concepts from main sections
- Appropriate visual metaphor

### Step 3: Call CogView API
```python
import requests
import base64
from PIL import Image
import io

def generate_cover(prompt, api_key, output_path):
    """Generate cover image using ZhipuAI CogView API."""

    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "cogview-4",
        "prompt": prompt,
        "size": "1920x1080",
        "n": 1
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        # Get image data
        image_data = data["data"][0]

        if "b64_json" in image_data:
            # Decode base64 image
            img_bytes = base64.b64decode(image_data["b64_json"])
            img = Image.open(io.BytesIO(img_bytes))
        elif "url" in image_data:
            # Download from URL
            img_response = requests.get(image_data["url"])
            img = Image.open(io.BytesIO(img_response.content))

        # Save as PNG
        img.save(output_path, "PNG")
        return output_path

    raise Exception("Failed to generate image")
```

### Step 4: Save and Verify
- Save to `pdf/PaperLog/figures/cover.png`
- Verify 16:9 aspect ratio
- Ensure file size is reasonable (< 2MB for web)

## Design Principles
- **Clean composition**: Central focal point, balanced layout
- **Readable at small sizes**: Avoid fine details that won't scale
- **No text in image**: Text overlays should be added in markdown
- **Web-optimized**: Use appropriate compression
- **Consistent style**: Match hand-drawn, infographic aesthetic

## Python Script

See `scripts/generate_cover.py` for complete implementation with:
- API key management
- Prompt construction from blog content
- Image generation and saving
- Error handling

## Environment Variables
```bash
export ZHIPUAI_API_KEY="your_api_key_here"
```

## Dependencies
```bash
pip install requests pillow
```

## Notes
- CogView models support both Chinese and English prompts
- For Chinese blogs, consider bilingual prompts for better results
- Always test prompts with small batches before full generation
- API has rate limits - implement appropriate delays for batch operations
- Save generated images locally to avoid re-generation costs
