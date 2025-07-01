#!/usr/bin/env python3
"""
HTML Generator for ComputoPermutoBook

Converts markdown files to HTML with proper styling.
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: markdown package not found. Please install with: pip install markdown")
    sys.exit(1)


def create_css():
    """Generate CSS styling for the HTML files."""
    return """
/* ComputoPermutoBook Styling */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
    background-color: #fff;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 2em;
    margin-bottom: 0.5em;
}

h1 {
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.3em;
}

h2 {
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 0.2em;
}

code {
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    margin: 1em 0;
}

pre code {
    background: none;
    padding: 0;
    font-size: 0.85em;
}

.navigation {
    background-color: #ecf0f1;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 2em;
}

.navigation h3 {
    margin-top: 0;
    color: #2c3e50;
}

.navigation ul {
    list-style-type: none;
    padding-left: 0;
}

.navigation li {
    margin: 0.5em 0;
}

.navigation a {
    color: #3498db;
    text-decoration: none;
}

.navigation a:hover {
    text-decoration: underline;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #bdc3c7;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #ecf0f1;
    font-weight: bold;
}

.footer {
    margin-top: 3em;
    padding-top: 2em;
    border-top: 1px solid #bdc3c7;
    text-align: center;
    color: #7f8c8d;
    font-size: 0.9em;
}

@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    pre {
        padding: 10px;
        font-size: 0.8em;
    }
}
"""


def create_html_template(title, content, navigation_links=None):
    """Create a complete HTML document."""
    nav_section = ""
    if navigation_links:
        nav_section = f"""
        <div class="navigation">
            <h3>📖 Book Navigation</h3>
            <ul>
                {navigation_links}
            </ul>
        </div>
        """
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ComputoPermutoBook</title>
    <style>{create_css()}</style>
</head>
<body>
    {nav_section}
    <main>
        {content}
    </main>
    <div class="footer">
        <p>Generated from <strong>ComputoPermutoBook</strong> | <a href="index.html">📖 Table of Contents</a></p>
    </div>
</body>
</html>"""


def create_index_html(md_files, output_dir):
    """Create an index.html file with navigation to all chapters."""
    chapters = []
    
    for md_file in sorted(md_files):
        if md_file.stem == "index" or md_file.stem.startswith("build_") or md_file.stem.startswith("ch03_"):
            continue
            
        # Extract title from first line of markdown file
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('#'):
                    title = first_line.lstrip('#').strip()
                else:
                    title = md_file.stem.replace('_', ' ').title()
        except:
            title = md_file.stem.replace('_', ' ').title()
        
        html_name = md_file.stem + ".html"
        chapters.append((title, html_name))
    
    # Create index content
    chapter_list = "\n".join([
        f'<li><a href="{html_name}">{title}</a></li>'
        for title, html_name in chapters
    ])
    
    index_content = f"""
    <h1>📖 ComputoPermutoBook</h1>
    <p><em>A comprehensive guide to mastering JSON transformation with Computo and Permuto</em></p>
    
    <div class="navigation">
        <h2>📚 Chapters</h2>
        <ul>
            {chapter_list}
        </ul>
    </div>
    
    <h2>🚀 Quick Start</h2>
    <p>Welcome to the ComputoPermutoBook! This guide teaches you how to transform JSON data using Computo and Permuto tools.</p>
    
    <ul>
        <li><strong>New to JSON transformation?</strong> Start with the introduction chapters</li>
        <li><strong>Want to jump in?</strong> Check out the practical examples</li>
        <li><strong>Need a reference?</strong> Use the operator documentation</li>
    </ul>
    """
    
    html_content = create_html_template("Table of Contents", index_content)
    
    index_file = output_dir / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created index: {index_file}")
    return chapters


def convert_markdown_to_html(md_file, output_dir, navigation_links):
    """Convert a single markdown file to HTML."""
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Configure markdown with extensions
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        'toc'
    ])
    
    # Convert to HTML
    html_content = md.convert(md_content)
    
    # Extract title from first heading
    title = md_file.stem.replace('_', ' ').title()
    if html_content.startswith('<h1>'):
        title_end = html_content.find('</h1>')
        if title_end > 0:
            title = html_content[4:title_end]
    
    # Create complete HTML document
    full_html = create_html_template(title, html_content, navigation_links)
    
    # Write HTML file
    html_file = output_dir / f"{md_file.stem}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Converted: {md_file.name} -> {html_file.name}")


def copy_assets(input_dir, output_dir):
    """Copy any additional assets like zip files, images, etc."""
    # Copy zip files
    for zip_file in input_dir.glob("*.zip"):
        dest = output_dir / zip_file.name
        shutil.copy2(zip_file, dest)
        print(f"Copied asset: {zip_file.name}")
    
    # Copy code directory if it exists
    code_dir = input_dir / "code"
    if code_dir.exists():
        dest_code = output_dir / "code"
        if dest_code.exists():
            shutil.rmtree(dest_code)
        shutil.copytree(code_dir, dest_code)
        print(f"Copied code directory")


def main():
    parser = argparse.ArgumentParser(description="Generate HTML from markdown files")
    parser.add_argument("--input-dir", default="new_way", help="Input directory with markdown files")
    parser.add_argument("--output-dir", default="docs", help="Output directory for HTML files")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist")
        return 1
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Find markdown files
    md_files = list(input_dir.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return 1
    
    print(f"HTML Generation for ComputoPermutoBook")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Found {len(md_files)} markdown files")
    
    # Create index and get navigation structure
    chapters = create_index_html(md_files, output_dir)
    
    # Create navigation links for all pages
    navigation_links = "\n".join([
        f'<li><a href="{html_name}">{title}</a></li>'
        for title, html_name in chapters
    ])
    
    # Convert each markdown file to HTML
    for md_file in md_files:
        if md_file.stem == "index" or md_file.stem.startswith("build_") or md_file.stem.startswith("ch03_"):
            continue
        convert_markdown_to_html(md_file, output_dir, navigation_links)
    
    # Copy additional assets
    copy_assets(input_dir, output_dir)
    
    print(f"\n✅ HTML generation completed!")
    print(f"📁 Output directory: {output_dir}")
    print(f"🌐 Open {output_dir}/index.html in your browser")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 