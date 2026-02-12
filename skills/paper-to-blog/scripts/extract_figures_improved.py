#!/usr/bin/env python3
"""
Figure and Table Extractor for Academic Papers - Improved Version

Extracts figures, tables, diagrams, and charts from PDF documents
using PyMuPDF for rendering and improved heuristics for detection.

Usage:
    python extract_figures_improved.py <pdf_path> <output_dir>

Requirements:
    pip install pymupdf pillow
"""

import fitz  # PyMuPDF
from PIL import Image
import json
import os
import sys
import argparse
import numpy as np


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


def analyze_pdf_text(page):
    """Analyze PDF text to find figure and table references."""
    text = page.get_text()
    lines = text.split('\n')

    figures = []
    tables = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Check for figure references
        if line.lower().startswith(('fig.', 'figure ', 'figure ')):
            # Extract figure number
            parts = line.split()
            if len(parts) >= 2:
                fig_num = parts[1].rstrip(':').rstrip('.')
                figures.append({
                    'type': 'figure',
                    'number': fig_num,
                    'description': f'Figure {fig_num}',
                    'text': line,
                    'position': i
                })

        # Check for table references
        elif line.lower().startswith(('table ', 'table ')):
            # Extract table number
            parts = line.split()
            if len(parts) >= 2:
                table_num = parts[1].rstrip(':').rstrip('.')
                tables.append({
                    'type': 'table',
                    'number': table_num,
                    'description': f'Table {table_num}',
                    'text': line,
                    'position': i
                })

    return figures, tables


def detect_visual_elements_with_text_guidance(page_path, text_elements):
    """Use text positions to guide figure detection."""
    img = Image.open(page_path)
    img_array = np.array(img)

    if len(img_array.shape) == 3:
        gray = np.mean(img_array, axis=2)
    else:
        gray = img_array

    h, w = gray.shape
    visual_elements = []

    # Create a map of text positions
    text_positions = {}
    for elem in text_elements:
        if hasattr(elem, 'position'):
            text_positions[elem['position']] = elem

    # Look for visual elements in areas not dominated by text
    # This is a simplified approach - in practice you'd use more sophisticated methods

    # If we have figure references, try to find them visually
    for elem in text_elements:
        if elem['type'] in ['figure', 'table']:
            # Look for visual content around the text
            # This is a heuristic - adjust based on typical layouts
            visual_elements.append({
                'type': elem['type'],
                'number': elem['number'],
                'description': elem['description'],
                'text': elem['text'],
                'top': 10,  # Default positions - would need layout analysis
                'left': 10,
                'bottom': 80,
                'right': 90
            })

    # If no text-guided elements found, use basic detection
    if not visual_elements:
        # Basic variance-based detection
        for i in range(0, h-150, 150):
            for j in range(0, w-150, 150):
                region = gray[i:i+150, j:j+150]
                if region.size > 0:
                    variance = np.var(region)
                    if variance > 1500:  # Threshold for high variance
                        visual_elements.append({
                            'type': 'figure',
                            'number': len(visual_elements) + 1,
                            'description': 'Detected visual element',
                            'text': '',
                            'top': i / h * 100,
                            'left': j / w * 100,
                            'bottom': min((i + 200) / h * 100, 95),
                            'right': min((j + 200) / w * 100, 95)
                        })

    # Limit to 3 elements per page
    return visual_elements[:3]


def extract_figures_with_text_guidance(pdf_path, output_dir):
    """Extract figures using both text analysis and visual detection."""
    temp_dir = os.path.join(output_dir, 'temp')
    figures_dir = os.path.join(output_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    all_metadata = []
    doc = fitz.open(pdf_path)

    # First pass: collect all figure/table references
    all_text_elements = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        figures, tables = analyze_pdf_text(page)
        all_text_elements.extend(figures)
        all_text_elements.extend(tables)

    # Second pass: render pages and extract visual elements
    print("Rendering PDF pages...")
    rendered_pages = render_pdf_pages(pdf_path, temp_dir)

    for page_num, page_image_path in rendered_pages:
        print(f"\nAnalyzing page {page_num + 1}...")

        # Get text elements for this page
        page_text_elements = [elem for elem in all_text_elements
                            if hasattr(elem, 'position') and
                            abs(elem['position'] // 50) == page_num]

        elements = detect_visual_elements_with_text_guidance(page_image_path, page_text_elements)

        if elements:
            saved = crop_and_save_elements(page_image_path, elements, figures_dir, page_num)
            all_metadata.extend(saved)

    doc.close()

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
        description = element.get('description', 'unknown')[:30].replace(' ', '_').replace('/', '_')
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


def main():
    parser = argparse.ArgumentParser(description='Extract figures and tables from academic papers (PDF).')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('output_dir', help='Output directory for extracted figures')
    parser.add_argument('--scale', type=float, default=2.0, help='Rendering scale factor (default: 2.0)')
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    print("Figure Extractor Script - Improved Version")
    print("=" * 50)
    print(f"PDF: {args.pdf_path}")
    print(f"Output: {args.output_dir}")
    print(f"Scale: {args.scale}x")

    extract_figures_with_text_guidance(args.pdf_path, args.output_dir)


if __name__ == "__main__":
    main()