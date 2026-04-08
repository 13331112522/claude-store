#!/usr/bin/env python3
"""
Cover Image Generator for PaperDog Podcast
Supports: PIL (local) or CogView API (Zhipu AI)
"""

import os
import sys
from datetime import datetime

def generate_cover_with_pil(output_path, date_str):
    """Generate cover image using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io

        # Image dimensions (square for podcast cover)
        width, height = 1080, 1080

        # Create gradient background (deep blue to purple)
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        # Draw gradient
        for y in range(height):
            r = int(30 + (50 - 30) * y / height)
            g = int(30 + (40 - 30) * y / height)
            b = int(80 + (120 - 80) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw decorative elements (neural network pattern)
        import random
        random.seed(42)  # For reproducibility

        # Draw nodes and connections
        nodes = []
        for _ in range(15):
            x = random.randint(100, width - 100)
            y = random.randint(100, height - 100)
            nodes.append((x, y))

        # Draw connections
        for i, (x1, y1) in enumerate(nodes):
            for j, (x2, y2) in enumerate(nodes[i+1:], i+1):
                if ((x1-x2)**2 + (y1-y2)**2) < 40000:  # Distance threshold
                    draw.line([(x1, y1), (x2, y2)], fill=(100, 150, 255, 50), width=1)

        # Draw nodes
        for x, y in nodes:
            draw.ellipse([x-5, y-5, x+5, y+5], fill=(150, 200, 255), outline=(255, 255, 255))

        # Add text
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
            date_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            date_font = ImageFont.load_default()

        # Title
        title = "PaperDog"
        draw.text((width//2, 200), "PaperDog", fill=(255, 255, 255), font=title_font, anchor="mm")

        # Subtitle
        subtitle = "AI Papers Daily Podcast"
        draw.text((width//2, 280), subtitle, fill=(200, 200, 255), font=subtitle_font, anchor="mm")

        # Date
        date_text = datetime.strptime(date_str, "%Y%m%d").strftime("%B %d, %Y")
        draw.text((width//2, height - 150), date_text, fill=(180, 180, 220), font=date_font, anchor="mm")

        # Save
        img.save(output_path)
        print(f"✅ Cover image saved to: {output_path}")
        return True

    except ImportError:
        print("❌ PIL not installed. Run: pip3 install Pillow")
        return False
    except Exception as e:
        print(f"❌ Error generating cover: {e}")
        return False


def generate_cover_with_cogview(api_key, prompt, output_path):
    """Generate cover image using CogView API (Zhipu AI)"""
    try:
        import requests

        url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "cogview-4",
            "prompt": prompt,
            "size": "1080x1080"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)

        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']

            # Download image
            img_response = requests.get(image_url)
            with open(output_path, 'wb') as f:
                f.write(img_response.content)

            print(f"✅ Cover image saved to: {output_path}")
            print(f"🔗 Generated via CogView-4")
            return True
        else:
            print(f"❌ CogView API error: {response.status_code}")
            print(response.text)
            return False

    except ImportError:
        print("❌ requests library not installed. Run: pip3 install requests")
        return False
    except Exception as e:
        print(f"❌ Error calling CogView: {e}")
        return False


if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")
    output_path = f"paper-podcast-{date_str}-cover.png"

    # Cover image prompt for CogView
    prompt = """A futuristic podcast cover for AI research papers about Transformer architecture,
AI Agents, and Multi-language Safety. Abstract neural network patterns with attention mechanisms
visualized as glowing connection pathways, digital brain circuitry with multilingual text fragments
floating in holographic space, symbolic representation of safety shields and survival pressure.
Deep blue and purple color scheme with cyan accent highlights, professional tech style,
modern and clean design, 3D render, sci-fi aesthetic suitable for academic AI research podcast."""

    # Check for CogView API key
    api_key = os.environ.get("ZHIPU_API_KEY") or os.environ.get("COGVIEW_API_KEY")

    if api_key:
        print(f"🎨 Generating cover with CogView-4...")
        success = generate_cover_with_cogview(api_key, prompt, output_path)
    else:
        print(f"🎨 No CogView API key found, using PIL...")
        print(f"💡 Set ZHIPU_API_KEY environment variable for AI-generated covers")
        success = generate_cover_with_pil(output_path, date_str)

    sys.exit(0 if success else 1)
