#!/usr/bin/env python3
"""
Cover Image Generator using ZhipuAI CogView API

Generates cartoon infographic cover images for blog posts
using the ZhipuAI GLM-image (CogView) text-to-image API.

Usage:
    python generate_cover.py --blog-content <content> --output <path>

Environment:
    ZHIPUAI_API_KEY - Your ZhipuAI API key (get from https://open.bigmodel.cn/)

Requirements:
    pip install requests pillow
"""

import os
import sys
import argparse
import requests
from PIL import Image
import io


# API Configuration
ZHIPUAI_API_URL = "https://open.bigmodel.cn/api/paas/v4/images/generations"
DEFAULT_MODEL = "glm-image"
DEFAULT_SIZE = "1024x1024"  # ZhipuAI API supports square format

# Theme keywords and visual elements
THEMES = {
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'neural', 'model'],
    'vision': ['vision', 'image', 'visual', 'recognition', 'detection'],
    'nlp': ['language', 'text', 'nlp', 'transformer', 'bert', 'gpt'],
    'data': ['data', 'analysis', 'analytics', 'statistics', 'graph'],
    'code': ['code', 'programming', 'algorithm', 'software'],
}

VISUAL_ELEMENTS = {
    'ai': 'stylized brain with circuit patterns, neural network visualization',
    'vision': 'eye with digital overlay, camera lens with data streams',
    'nlp': 'speech bubbles with binary code, document with symbols',
    'data': 'charts and graphs merging into abstract shapes, data visualization',
    'code': 'code snippets forming geometric patterns, algorithm flowchart',
    'tech': 'abstract geometric shapes suggesting technology and innovation'
}


def get_api_key():
    """Get ZhipuAI API key from environment variable."""
    api_key = os.environ.get("ZHIPUAI_API_KEY")
    if not api_key:
        raise ValueError(
            "ZHIPUAI_API_KEY environment variable not set. "
            "Get your API key from https://open.bigmodel.cn/"
        )
    return api_key


def detect_theme(content):
    """Detect visual theme from blog content keywords."""
    content_lower = content.lower()
    for theme, keywords in THEMES.items():
        if any(kw in content_lower for kw in keywords):
            return theme
    return 'tech'


def construct_prompt(blog_content, blog_title=None):
    """Construct a prompt for CogView based on blog content."""
    theme = detect_theme(blog_content)
    main_element = VISUAL_ELEMENTS[theme]

    return f"""Cartoon infographic illustration for a blog post.

Style: Hand-drawn, clean lines, minimal aesthetic, flat colors
Layout: Centered composition with clear focal point

Visual Elements:
- Central illustration: {main_element}
- Background: simple gradient, clean and uncluttered
- Accent elements: small geometric shapes, subtle tech motifs

Color Palette: Professional and modern, blues with accent colors

Technical: Blog header quality, high resolution, web-optimized"""


def generate_cover_image(prompt, output_path, api_key=None):
    """Generate cover image using ZhipuAI CogView API."""
    api_key = api_key or get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEFAULT_MODEL,
        "prompt": prompt,
        "size": DEFAULT_SIZE,
        "n": 1
    }

    print(f"Generating image with prompt: {prompt[:80]}...")
    print(f"Model: {DEFAULT_MODEL}, Size: {DEFAULT_SIZE}")

    response = requests.post(ZHIPUAI_API_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()

    if "data" not in data or not data["data"]:
        raise ValueError("No image data in response")

    # Download image from URL
    image_url = data["data"][0]["url"]
    print(f"Downloading image from: {image_url}")
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()
    img = Image.open(io.BytesIO(img_response.content))

    # Save as PNG
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    img.save(output_path, "PNG")

    width, height = img.size
    print(f"Saved: {output_path}")
    print(f"Dimensions: {width}x{height} (ratio: {width/height:.2f})")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate cover images using ZhipuAI CogView API.'
    )
    parser.add_argument('--blog-content', '-c',
                        help='Blog post content or summary')
    parser.add_argument('--blog-title', '-t',
                        help='Blog post title (optional)')
    parser.add_argument('--prompt', '-p',
                        help='Direct prompt (overrides --blog-content)')
    parser.add_argument('--output', '-o',
                        default='cover.png',
                        help='Output path for generated image (default: cover.png)')
    parser.add_argument('--api-key',
                        help='ZhipuAI API key (uses ZHIPUAI_API_KEY env var if not provided)')

    args = parser.parse_args()

    # Determine prompt
    if args.prompt:
        prompt = args.prompt
    elif args.blog_content:
        prompt = construct_prompt(args.blog_content, args.blog_title)
        print("Generated prompt for blog content")
    else:
        parser.error("Either --prompt or --blog-content must be provided")

    try:
        generate_cover_image(prompt, args.output, args.api_key)
        print("\n✓ Cover image generated successfully!")
        return 0
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
