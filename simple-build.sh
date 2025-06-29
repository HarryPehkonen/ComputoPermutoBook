#!/bin/bash

# Simple ComputoPermutoBook HTML Generator
# Uses Python's markdown library (commonly available) instead of pandoc

set -e

# Configuration
OUTPUT_DIR="output"
HTML_DIR="$OUTPUT_DIR/html"
BOOK_DIR="book"
GITHUB_PAGES_MODE=false

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "python3 is not installed."
        exit 1
    fi
    
    # Try to import markdown
    if ! python3 -c "import markdown" 2>/dev/null; then
        print_warning "Python markdown library not found. Installing..."
        if command -v pip3 &> /dev/null; then
            pip3 install --user markdown
        else
            print_error "pip3 not found. Please install python3-pip and run again."
            exit 1
        fi
    fi
    
    print_status "Dependencies check complete."
}

# Setup directories
setup_directories() {
    print_status "Setting up output directories..."
    rm -rf "$OUTPUT_DIR"
    mkdir -p "$HTML_DIR" "$HTML_DIR/appendices"
    
    # Create .nojekyll file for GitHub Pages
    if [[ "$GITHUB_PAGES_MODE" == true ]]; then
        touch "$OUTPUT_DIR/.nojekyll"
        print_status "Created .nojekyll file for GitHub Pages"
    fi
}

# Create CSS
create_css() {
    cat > "$HTML_DIR/style.css" << 'EOF'
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 2rem;
}

h1 {
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.5rem;
}

h2 {
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 0.3rem;
}

code {
    background-color: #f8f9fa;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: "Monaco", "Menlo", "Ubuntu Mono", monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 1rem;
    overflow-x: auto;
}

pre code {
    background: none;
    padding: 0;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 1rem 0;
    padding-left: 1rem;
    color: #7f8c8d;
}

.navigation {
    background-color: #ecf0f1;
    padding: 1rem;
    border-radius: 5px;
    margin: 2rem 0;
}

.navigation a {
    color: #2980b9;
    text-decoration: none;
    margin-right: 1rem;
}

.navigation a:hover {
    text-decoration: underline;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
}

th, td {
    border: 1px solid #bdc3c7;
    padding: 0.5rem;
    text-align: left;
}

th {
    background-color: #ecf0f1;
}

ul, ol {
    padding-left: 1.5rem;
}

.toc {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}

.back-to-index {
    text-align: center;
    margin: 2rem 0;
    padding: 1rem;
    background-color: #ecf0f1;
    border-radius: 5px;
}
EOF
}

# Convert markdown to HTML using Python
convert_md_to_html() {
    local md_file="$1"
    local html_file="$2"
    local title="$3"
    
    python3 << EOF
import markdown
import sys

# Read markdown file
with open('$md_file', 'r', encoding='utf-8') as f:
    content = f.read()

# Convert to HTML
md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc'])
html_content = md.convert(content)

# Create full HTML document
full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title</title>
    <link rel="stylesheet" href="$(if [[ "$GITHUB_PAGES_MODE" == true ]]; then echo "style.css"; else echo "../style.css"; fi)">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="back-to-index">
        <a href="$(if [[ "$GITHUB_PAGES_MODE" == true ]]; then echo "index.html"; else echo "../index.html"; fi)">← Back to Table of Contents</a>
    </div>
    
    {html_content}
    
    <div class="back-to-index">
        <a href="$(if [[ "$GITHUB_PAGES_MODE" == true ]]; then echo "index.html"; else echo "../index.html"; fi)">← Back to Table of Contents</a>
    </div>
</body>
</html>'''

# Write HTML file
with open('$html_file', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Converted: $md_file -> $html_file")
EOF
}

# Generate HTML files
generate_html() {
    print_status "Generating HTML files..."
    
    create_css
    
    # Convert each markdown file
    for md_file in "$BOOK_DIR"/*.md "$BOOK_DIR"/appendices/*.md; do
        if [[ -f "$md_file" ]]; then
            basename=$(basename "$md_file" .md)
            
            # Determine output path
            if [[ "$md_file" == *"/appendices/"* ]]; then
                html_file="$HTML_DIR/appendices/$basename.html"
                title="ComputoPermuto Book - Appendix $basename"
            else
                html_file="$HTML_DIR/$basename.html"
                title="ComputoPermuto Book - $basename"
            fi
            
            convert_md_to_html "$md_file" "$html_file" "$title"
        fi
    done
    
    # Create main index
    create_index_html
    
    # Note: README files are linked directly to GitHub repositories for latest information
    
    print_status "HTML generation complete!"
}

# Create main index.html
create_index_html() {
    cat > "$HTML_DIR/index.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ComputoPermuto Book</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>ComputoPermuto Book$(if [[ "$GITHUB_PAGES_MODE" == true ]]; then echo ""; else echo " - Local Preview"; fi)</h1>
    
    <div class="toc">
        <h2>Table of Contents</h2>
        
        <p><strong><a href="00_index.html">Book Index & Navigation</a></strong></p>
        
        <h3>Chapters</h3>
        <ol>
            <li><a href="01_why_transformation_matters.html">Why JSON Transformation Matters</a></li>
            <li><a href="02_setting_up_environment.html">Setting Up Your Environment</a></li>
            <li><a href="03_computo_basics.html">Computo Basics - Data and Logic</a></li>
            <li><a href="04_permuto_basics.html">Permuto Basics - Templates</a></li>
            <li><a href="05_control_flow.html">Control Flow and Logic</a></li>
            <li><a href="06_working_with_arrays.html">Working with Arrays</a></li>
            <li><a href="07_object_manipulation.html">Object Manipulation</a></li>
            <li><a href="08_advanced_array_ops.html">Advanced Array Operations</a></li>
            <li><a href="09_template_driven_transformations.html">Template-Driven Transformations</a></li>
            <li><a href="10_data_pipeline_patterns.html">Data Pipeline Patterns</a></li>
            <li><a href="11_complex_real-world_examples.html">Complex Real-World Examples</a></li>
            <li><a href="12_performance_and_optimization.html">Performance and Optimization</a></li>
            <li><a href="13_error_handling_and_debugging.html">Error Handling and Debugging</a></li>
            <li><a href="14_best_practices_and_patterns.html">Best Practices and Patterns</a></li>
            <li><a href="15_multiple_inputs_and_json_patch.html">Multiple Inputs and JSON Patch</a></li>
        </ol>
        
        <h3>Appendices</h3>
        <ul>
            <li><a href="appendices/A_operator_reference.html">Complete Operator Reference</a></li>
        </ul>
        
        <h3>Reference Documents</h3>
        <ul>
            <li><a href="https://github.com/HarryPehkonen/Computo/blob/main/README.md" target="_blank">Computo Technical README</a></li>
            <li><a href="https://github.com/HarryPehkonen/Permuto/blob/main/README.md" target="_blank">Permuto Technical README</a></li>
        </ul>
    </div>
    
    <div class="navigation">
        <p><strong>Quick Start:</strong> New to Computo? Start with <a href="01_why_transformation_matters.html">Chapter 1</a></p>
        <p><strong>Looking for something specific?</strong> Check the <a href="appendices/A_operator_reference.html">Operator Reference</a></p>
        <p><strong>New Features:</strong> Learn about multiple inputs and JSON Patch in <a href="15_multiple_inputs_and_json_patch.html">Chapter 15</a></p>
    </div>
    
    <hr>
    <p><em>Generated: $(date)</em></p>
    <p><em>Browse locally without internet connection - all content is self-contained.</em></p>
</body>
</html>
EOF
}

# Open browser
open_browser() {
    local index_file="$HTML_DIR/index.html"
    if command -v xdg-open &> /dev/null; then
        xdg-open "$index_file"
    elif command -v open &> /dev/null; then
        open "$index_file"
    else
        print_status "Please open $index_file in your browser"
    fi
}

# Main function
main() {
    # Parse arguments
    OPEN_BROWSER=false
    for arg in "$@"; do
        case $arg in
            --github-pages)
                GITHUB_PAGES_MODE=true
                OUTPUT_DIR="docs"
                HTML_DIR="$OUTPUT_DIR"
                print_status "GitHub Pages mode enabled - outputting to docs/"
                ;;
            --open)
                OPEN_BROWSER=true
                ;;
        esac
    done
    
    print_status "Starting simple HTML build..."
    
    check_dependencies
    setup_directories
    generate_html
    
    if [[ "$OPEN_BROWSER" == true ]]; then
        open_browser
    fi
    
    print_status "Build complete!"
    echo ""
    if [[ "$GITHUB_PAGES_MODE" == true ]]; then
        echo "GitHub Pages files ready in: $(realpath "$OUTPUT_DIR")"
        echo "Commit and push to deploy to GitHub Pages"
    else
        echo "Open in browser: file://$(realpath "$HTML_DIR/index.html")"
    fi
    echo ""
    echo "Usage:"
    echo "  ./simple-build.sh                    # Generate HTML locally"
    echo "  ./simple-build.sh --open             # Generate HTML and open browser"
    echo "  ./simple-build.sh --github-pages     # Generate for GitHub Pages"
    echo "  ./simple-build.sh --github-pages --open # GitHub Pages + open browser"
}

main "$@"