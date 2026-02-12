#!/usr/bin/env python3
"""
Figure and Table Extractor for Academic Papers - Standalone Version

Extracts figures, tables, diagrams, and charts from PDF documents
using PyMuPDF for rendering and simple heuristics for detection.

Usage:
    python extract_figures_standalone.py <pdf_path> <output_dir>

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


def detect_figures_simple(page_image_path):
    """Simple heuristic-based figure detection using image analysis."""
    import numpy as np

    img = Image.open(page_image_path)
    img_array = np.array(img)

    # Convert to grayscale for analysis
    if len(img_array.shape) == 3:
        gray = np.mean(img_array, axis=2)
    else:
        gray = img_array

    # Find regions with high variance (potential figures/charts)
    h, w = gray.shape
    figures = []

    # Simple heuristic: look for regions with high contrast
    # This is a basic approach - in practice you'd use more sophisticated methods
    for i in range(0, h-100, 100):
        for j in range(0, w-100, 100):
            region = gray[i:i+100, j:j+100]
            if region.size > 0:
                variance = np.var(region)
                if variance > 1000:  # Threshold for high variance
                    # Check if this is likely a figure (not text)
                    # Higher variance might indicate images/charts
                    figures.append({
                        'type': 'figure',
                        'description': 'Detected visual element',
                        'top': i / h * 100,
                        'left': j / w * 100,
                        'bottom': min((i + 150) / h * 100, 95),
                        'right': min((j + 150) / w * 100, 95),
                        'text': '',
                        'number': len(figures) + 1
                    })

    # If no figures detected, extract the main content area
    if not figures:
        figures.append({
            'type': 'figure',
            'description': 'Page content',
            'top': 5,
            'left': 5,
            'bottom': 95,
            'right': 95,
            'text': '',
            'number': 1
        })

    return figures[:3]  # Limit to 3 figures per page


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

        # Ensure coordinates are within bounds
        left = max(0, min(left, img_width - 1))
        top = max(0, min(top, img_height - 1))
        right = max(left + 1, min(right, img_width))
        bottom = max(top + 1, min(bottom, img_height))

        # Crop and save
        cropped = page_img.crop((left, top, right, bottom))
        fig_type = element.get('type', 'figure')
        fig_num = element.get('number', idx + 1)
        description = element.get('description', 'unknown')[:20].replace(' ', '_').replace('/', '_')
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


def extract_figures(pdf_path, output_dir):
    """
    Main function to extract figures and tables from PDF.

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save extracted figures

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
        elements = detect_figures_simple(page_image_path)

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

    print("Figure Extractor Script - Standalone Version")
    print("=" * 50)
    print(f"PDF: {args.pdf_path}")
    print(f"Output: {args.output_dir}")
    print(f"Scale: {args.scale}x")

    extract_figures(args.pdf_path, args.output_dir)


if __name__ == "__main__":
    main()