#!/usr/bin/env python3
"""
HTML Generator for ComputoPermutoBook

Converts markdown files to HTML with proper styling.
Designed to be GitHub Actions compatible.

Usage:
    python scripts/generate_html.py
    python scripts/generate_html.py --input-dir new_way --output-dir html
"""

import argparse
import sys
from pathlib import Path

# For now, this is a placeholder that will print what it would do
# In the future, this can use the markdown package or pandoc


def main():
    parser = argparse.ArgumentParser(description="Generate HTML from markdown files")
    parser.add_argument("--input-dir", default="new_way", help="Input directory with markdown files")
    parser.add_argument("--output-dir", default="html", help="Output directory for HTML files")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    # Find markdown files
    md_files = list(input_dir.glob("*.md"))
    
    print(f"HTML Generation (Future Implementation)")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Found {len(md_files)} markdown files:")
    
    for md_file in md_files:
        html_name = md_file.stem + ".html"
        print(f"  {md_file.name} -> {html_name}")
    
    print("\nTo implement:")
    print("1. Install markdown package: pip install markdown[extra]")
    print("2. Convert each .md file to .html with proper CSS styling")
    print("3. Create index.html with navigation")
    print("4. Copy download files")
    print("5. Generate GitHub Pages compatible output")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 