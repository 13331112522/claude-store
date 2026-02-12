#!/usr/bin/env python3
"""
Targeted Figure Extractor for Academic Papers

Extracts specific figures and tables mentioned in the PDF text,
providing more accurate extraction based on actual content.

Usage:
    python extract_figures_targeted.py <pdf_path> <output_dir>

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
        page_image_path = os.path.join(output_dir, f"page_{page_num:03d}.png")
        pix.save(page_image_path)
        rendered_pages.append((page_num, page_image_path))
        print(f"Rendered page {page_num + 1}/{len(doc)}: {page_image_path}")

    doc.close()
    return rendered_pages


def analyze_pdf_for_figures_tables(pdf_path):
    """Analyze PDF text to identify exact figure and table locations."""
    doc = fitz.open(pdf_path)

    # First, collect all figure and table references with their pages
    figures = []
    tables = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for figures
            if line.lower().startswith(('fig.', 'figure', 'figure')):
                figures.append({
                    'page': page_num + 1,
                    'text': line,
                    'number': extract_figure_number(line),
                    'title': extract_figure_title(line)
                })

            # Check for tables
            elif line.lower().startswith('table'):
                tables.append({
                    'page': page_num + 1,
                    'text': line,
                    'number': extract_table_number(line),
                    'title': extract_table_title(line)
                })

    doc.close()
    return figures, tables


def extract_figure_number(text):
    """Extract figure number from text."""
    import re
    match = re.search(r'(?:fig\.|figure)\s+(\d+)', text, re.IGNORECASE)
    return match.group(1) if match else '1'


def extract_figure_title(text):
    """Extract figure title from text."""
    parts = text.split('.', 1)
    return parts[1].strip() if len(parts) > 1 else 'Untitled Figure'


def extract_table_number(text):
    """Extract table number from text."""
    import re
    match = re.search(r'table\s+(\d+)', text, re.IGNORECASE)
    return match.group(1) if match else '1'


def extract_table_title(text):
    """Extract table title from text."""
    parts = text.split('.', 1)
    return parts[1].strip() if len(parts) > 1 else 'Untitled Table'


def extract_visual_elements_targeted(page_image_path, elements_info):
    """Extract visual elements based on known figure/table information."""
    img = Image.open(page_image_path)
    img_array = img.convert('L')  # Convert to grayscale
    img_array = np.array(img_array)

    h, w = img_array.shape
    extracted_elements = []

    # Create a mapping of elements by page
    page_elements = {}
    for elem in elements_info:
        page = elem['page']
        if page not in page_elements:
            page_elements[page] = []
        page_elements[page].append(elem)

    # For this page, get relevant elements
    current_page_elements = page_elements.get(1, [])  # Default to page 1

    # For each element, try to find its visual content
    for elem in current_page_elements:
        # Typical bounding boxes for figures/tables in academic papers
        if elem['type'] == 'figure':
            # Figures are often centered, taking most of the page
            bbox = {
                'top': 15,
                'left': 10,
                'bottom': 85,
                'right': 90
            }
        else:  # table
            # Tables might be smaller, often in the middle of the page
            bbox = {
                'top': 25,
                'left': 15,
                'bottom': 75,
                'right': 85
            }

        extracted_elements.append({
            'type': elem['type'],
            'page': elem['page'],
            'number': elem['number'],
            'title': elem['title'],
            'text': elem['text'],
            'bbox': bbox,
            'description': elem.get('title', f"{elem['type'].capitalize()} {elem['number']}")
        })

    return extracted_elements


def crop_and_save_elements(page_image_path, elements, output_dir, page_num):
    """Crop identified visual elements from page image and save individually."""
    os.makedirs(output_dir, exist_ok=True)
    page_img = Image.open(page_image_path)
    img_width, img_height = page_img.size
    saved_elements = []

    for element in elements:
        # Set default bounding box if not provided
        if 'bbox' in element:
            bbox = element['bbox']
        else:
            # Use typical bounding boxes for figures/tables
            if element['type'] == 'figure':
                bbox = {
                    'top': 15,
                    'left': 10,
                    'bottom': 85,
                    'right': 90
                }
            else:  # table
                bbox = {
                    'top': 25,
                    'left': 15,
                    'bottom': 75,
                    'right': 85
                }
        left = int(bbox['left'] / 100 * img_width)
        top = int(bbox['top'] / 100 * img_height)
        right = int(bbox['right'] / 100 * img_width)
        bottom = int(bbox['bottom'] / 100 * img_height)

        # Ensure coordinates are within bounds
        left = max(0, min(left, img_width - 1))
        top = max(0, min(top, img_height - 1))
        right = max(left + 1, min(right, img_width))
        bottom = max(top + 1, min(bottom, img_height))

        # Crop and save
        cropped = page_img.crop((left, top, right, bottom))
        fig_type = element['type']
        fig_num = element['number']
        description = element.get('description', element.get('title', ''))[:30].replace(' ', '_').replace('/', '_')
        filename = f"{fig_type}{fig_num}_{description}.png"
        output_path = os.path.join(output_dir, filename)
        cropped.save(output_path)

        # Build metadata
        saved_elements.append({
            'filename': filename,
            'type': fig_type,
            'number': fig_num,
            'page': page_num + 1,
            'description': element.get('description', element.get('title', '')),
            'text_content': element.get('text', ''),
            'bbox': bbox
        })
        print(f"Saved: {output_path}")

    return saved_elements


def extract_figures_targeted(pdf_path, output_dir):
    """Main extraction function with targeted approach."""
    temp_dir = os.path.join(output_dir, 'temp')
    figures_dir = os.path.join(output_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    all_metadata = []

    # Analyze PDF for figures and tables
    print("Analyzing PDF for figures and tables...")
    figures, tables = analyze_pdf_for_figures_tables(pdf_path)
    elements_info = []

    for fig in figures:
        elements_info.append({
            'type': 'figure',
            'page': fig['page'],
            'number': fig['number'],
            'title': fig['title'],
            'text': fig['text']
        })

    for tab in tables:
        elements_info.append({
            'type': 'table',
            'page': tab['page'],
            'number': tab['number'],
            'title': tab['title'],
            'text': tab['text']
        })

    print(f"Found {len(figures)} figures and {len(tables)} tables")

    # Render pages and extract elements
    print("\nRendering PDF pages...")
    rendered_pages = render_pdf_pages(pdf_path, temp_dir)

    # Group elements by page
    page_to_elements = {}
    for elem in elements_info:
        page = elem['page']
        if page not in page_to_elements:
            page_to_elements[page] = []
        page_to_elements[page].append(elem)

    # Extract elements for each page
    for page_num, page_image_path in rendered_pages:
        if page_num + 1 in page_to_elements:
            print(f"\nExtracting from page {page_num + 1}...")
            elements = page_to_elements[page_num + 1]
            print(f"Debug - elements type: {type(elements)}")
            print(f"Debug - first element: {elements[0] if elements else 'None'}")
            print(f"Debug - first element keys: {elements[0].keys() if elements and isinstance(elements[0], dict) else 'N/A'}")
            saved = crop_and_save_elements(page_image_path, elements, figures_dir, page_num)
            all_metadata.extend(saved)

    # Save metadata
    metadata_path = os.path.join(output_dir, 'figures_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)

    print(f"\nSaved metadata to: {metadata_path}")
    print(f"Total elements extracted: {len(all_metadata)}")

    # Cleanup temp files
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    return all_metadata


def main():
    parser = argparse.ArgumentParser(description='Extract figures and tables from academic papers (PDF).')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('output_dir', help='Output directory for extracted figures')
    parser.add_argument('--scale', type=float, default=3.0, help='Rendering scale factor (default: 3.0)')
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    print("Targeted Figure Extractor")
    print("=" * 50)
    print(f"PDF: {args.pdf_path}")
    print(f"Output: {args.output_dir}")
    print(f"Scale: {args.scale}x")

    extract_figures_targeted(args.pdf_path, args.output_dir)


if __name__ == "__main__":
    import numpy as np
    main()