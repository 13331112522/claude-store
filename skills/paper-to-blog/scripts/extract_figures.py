#!/usr/bin/env python3
"""
Figure and Table Extractor for Academic Papers

Extracts figures, tables, diagrams, and charts from PDF documents
using PyMuPDF for rendering and AI vision analysis for region detection.

Usage:
    python extract_figures.py <pdf_path> <output_dir>

Requirements:
    pip install pymupdf pillow
"""

import fitz  # PyMuPDF
from PIL import Image
import json
import os
import sys
import argparse


def render_pdf_pages(pdf_path, output_dir, scale=2.0):
    """Render PDF pages to high-resolution images."""
    os.makedirs(output_dir, exist_ok=True)
    rendered_pages = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap(matrix=fitz.Matrix(scale, scale))
        page_image_path = os.path.join(output_dir, f"temp_page_{page_num:03d}.png")
        pix.save(page_image_path)
        rendered_pages.append((page_num, page_image_path))
        print(f"Rendered page {page_num + 1}/{len(doc)}: {page_image_path}")

    doc.close()
    return rendered_pages


def analyze_page_for_figures(page_image_path, mcp_analyze_image_func):
    """Analyze a rendered page to identify figures, tables, and diagrams."""
    if mcp_analyze_image_func:
        prompt = """
        Analyze this academic paper page and identify ALL visual elements (figures, tables, diagrams, charts).

        For each visual element found, provide:
        1. Type: figure/table/diagram/chart
        2. Approximate bounding box as percentages (top, left, bottom, right)
        3. Content description
        4. Figure/table number (if visible)
        5. Key text labels or data

        IGNORE: Plain text, page numbers, headers, footers
        FOCUS ON: Visual data representations and diagrams

        Format your response as a JSON array of objects.
        """
        return mcp_analyze_image_func(page_image_path, prompt)
    else:
        # Fallback: simple detection based on common patterns
        print("Warning: MCP image analysis not available. Using simple fallback detection.")
        return [{
            'type': 'unknown',
            'description': 'Visual element (MCP analysis unavailable)',
            'top': 10,
            'left': 10,
            'bottom': 90,
            'right': 90,
            'text': '',
            'number': 1
        }]


def crop_and_save_elements(page_image_path, elements, output_dir, page_num):
    """Crop identified visual elements from page image and save individually."""
    os.makedirs(output_dir, exist_ok=True)
    page_img = Image.open(page_image_path)
    img_width, img_height = page_img.size
    saved_elements = []

    for idx, element in enumerate(elements):
        # Convert percentage coordinates to pixels
        left = int(element.get('left', 10) / 100 * img_width)
        top = int(element.get('top', 10) / 100 * img_height)
        right = int(element.get('right', 90) / 100 * img_width)
        bottom = int(element.get('bottom', 90) / 100 * img_height)

        # Crop and save
        cropped = page_img.crop((left, top, right, bottom))
        fig_type = element.get('type', 'figure')
        fig_num = element.get('number', idx + 1)
        description = element.get('description', '')[:30].replace(' ', '_').replace('/', '_')
        filename = f"{fig_type}{page_num+1}_{fig_num}_{description}.png"
        output_path = os.path.join(output_dir, filename)
        cropped.save(output_path)

        # Build metadata
        saved_elements.append({
            'filename': filename,
            'type': fig_type,
            'number': fig_num,
            'page': page_num + 1,
            'description': element.get('description', ''),
            'text_content': element.get('text', ''),
            'bbox': {
                'top': element.get('top', 10),
                'left': element.get('left', 10),
                'bottom': element.get('bottom', 90),
                'right': element.get('right', 90)
            }
        })
        print(f"Saved: {output_path}")

    return saved_elements


def extract_figures(pdf_path, output_dir, mcp_analyze_image_func=None):
    """
    Main function to extract figures and tables from PDF.

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save extracted figures
        mcp_analyze_image_func: MCP tool function for image analysis

    Returns:
        List of all extracted figure metadata
    """
    temp_dir = os.path.join(output_dir, 'temp')
    figures_dir = os.path.join(output_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    all_metadata = []

    # Render and analyze PDF pages
    print("Rendering PDF pages...")
    rendered_pages = render_pdf_pages(pdf_path, temp_dir)

    for page_num, page_image_path in rendered_pages:
        print(f"\nAnalyzing page {page_num + 1}...")
        elements = analyze_page_for_figures(page_image_path, mcp_analyze_image_func) if mcp_analyze_image_func else []

        if elements:
            saved = crop_and_save_elements(page_image_path, elements, figures_dir, page_num)
            all_metadata.extend(saved)

    # Save metadata and cleanup
    metadata_path = os.path.join(output_dir, 'figures_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)

    print(f"\nSaved metadata to: {metadata_path}")
    print(f"Total elements extracted: {len(all_metadata)}")

    # Cleanup temp files
    for f in os.listdir(temp_dir):
        if f.startswith("temp_page_"):
            os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    return all_metadata


def main():
    parser = argparse.ArgumentParser(description='Extract figures and tables from academic papers (PDF).')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('output_dir', help='Output directory for extracted figures')
    parser.add_argument('--scale', type=float, default=2.0, help='Rendering scale factor (default: 2.0)')
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    print("Figure Extractor Script")
    print("=" * 50)
    print(f"PDF: {args.pdf_path}")
    print(f"Output: {args.output_dir}")
    print(f"Scale: {args.scale}x")
    print("\nNote: Use from skill workflow with MCP image analysis enabled.")


if __name__ == "__main__":
    main()
