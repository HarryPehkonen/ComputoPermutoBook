#!/bin/bash

# ComputoPermutoBook Build Script
# Converts markdown to HTML (for browser viewing) and PDF

set -e  # Exit on any error

# Configuration
OUTPUT_DIR="output"
HTML_DIR="$OUTPUT_DIR/html"
PDF_DIR="$OUTPUT_DIR/pdf"
BOOK_DIR="book"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if pandoc is installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v pandoc &> /dev/null; then
        print_error "pandoc is not installed. Please install it:"
        echo "  Ubuntu/Debian: sudo apt-get install pandoc"
        echo "  macOS: brew install pandoc"
        echo "  Or visit: https://pandoc.org/installing.html"
        exit 1
    fi
    
    # Check for LaTeX (needed for PDF generation)
    if ! command -v pdflatex &> /dev/null; then
        print_warning "pdflatex not found. PDF generation will be skipped."
        echo "  To install LaTeX:"
        echo "  Ubuntu/Debian: sudo apt-get install texlive-latex-base texlive-latex-recommended"
        echo "  macOS: brew install --cask mactex"
        PDF_ENABLED=false
    else
        PDF_ENABLED=true
    fi
    
    print_status "Dependencies check complete."
}

# Create output directories
setup_directories() {
    print_status "Setting up output directories..."
    rm -rf "$OUTPUT_DIR"
    mkdir -p "$HTML_DIR" "$PDF_DIR"
}

# Generate HTML for browser viewing
generate_html() {
    print_status "Generating HTML files..."
    
    # Create CSS for better styling
    cat > "$HTML_DIR/style.css" << EOF
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
EOF
    
    # Convert each markdown file to HTML
    for md_file in "$BOOK_DIR"/*.md; do
        if [[ -f "$md_file" ]]; then
            basename=$(basename "$md_file" .md)
            html_file="$HTML_DIR/$basename.html"
            
            print_status "Converting $md_file -> $html_file"
            
            pandoc "$md_file" \
                --from markdown-yaml_metadata_block \
                --to html5 \
                --standalone \
                --css="style.css" \
                --metadata title="ComputoPermuto Book - $basename" \
                --output "$html_file"
        fi
    done
    
    # Convert appendices separately
    if [[ -d "$BOOK_DIR/appendices" ]]; then
        mkdir -p "$HTML_DIR/appendices"
        for md_file in "$BOOK_DIR"/appendices/*.md; do
            if [[ -f "$md_file" ]]; then
                basename=$(basename "$md_file" .md)
                html_file="$HTML_DIR/appendices/$basename.html"
                
                print_status "Converting $md_file -> $html_file"
                
                pandoc "$md_file" \
                    --from markdown-yaml_metadata_block \
                    --to html5 \
                    --standalone \
                    --css="../style.css" \
                    --metadata title="ComputoPermuto Book - Appendix $basename" \
                    --output "$html_file"
            fi
        done
    fi
    
    # Create main index.html
    print_status "Creating main index.html..."
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
    <h1>ComputoPermuto Book - Local Preview</h1>
    
    <div class="navigation">
        <h2>Table of Contents</h2>
        <p><a href="00_index.html">Book Index</a></p>
        
        <h3>Chapters</h3>
        <ul>
            <li><a href="01_why_transformation_matters.html">Chapter 1: Why JSON Transformation Matters</a></li>
            <li><a href="02_setting_up_environment.html">Chapter 2: Setting Up Your Environment</a></li>
            <li><a href="03_computo_basics.html">Chapter 3: Computo Basics</a></li>
            <li><a href="04_permuto_basics.html">Chapter 4: Permuto Basics</a></li>
            <li><a href="05_control_flow.html">Chapter 5: Control Flow</a></li>
            <li><a href="06_working_with_arrays.html">Chapter 6: Working with Arrays</a></li>
            <li><a href="07_object_manipulation.html">Chapter 7: Object Manipulation</a></li>
            <li><a href="08_advanced_array_ops.html">Chapter 8: Advanced Array Operations</a></li>
            <li><a href="09_template_driven_transformations.html">Chapter 9: Template-Driven Transformations</a></li>
            <li><a href="10_data_pipeline_patterns.html">Chapter 10: Data Pipeline Patterns</a></li>
            <li><a href="11_complex_real-world_examples.html">Chapter 11: Complex Real-World Examples</a></li>
            <li><a href="12_performance_and_optimization.html">Chapter 12: Performance and Optimization</a></li>
            <li><a href="13_error_handling_and_debugging.html">Chapter 13: Error Handling and Debugging</a></li>
            <li><a href="14_best_practices_and_patterns.html">Chapter 14: Best Practices and Patterns</a></li>
            <li><a href="15_multiple_inputs_and_json_patch.html">Chapter 15: Multiple Inputs and JSON Patch</a></li>
        </ul>
        
        <h3>Appendices</h3>
        <ul>
            <li><a href="appendices/A_operator_reference.html">Appendix A: Complete Operator Reference</a></li>
        </ul>
        
        <h3>Reference Documents</h3>
        <ul>
            <li><a href="https://github.com/HarryPehkonen/Computo/blob/main/README.md" target="_blank">Computo Technical README</a></li>
            <li><a href="https://github.com/HarryPehkonen/Permuto/blob/main/README.md" target="_blank">Permuto Technical README</a></li>
        </ul>
    </div>
    
    <p><strong>Generated:</strong> $(date)</p>
    <p><strong>Browse locally:</strong> Open this file in your web browser to navigate the book.</p>
</body>
</html>
EOF

    # README files are now linked directly to GitHub repositories for latest information
    # No longer converting local README files
    
    print_status "HTML generation complete!"
    print_status "Open $HTML_DIR/index.html in your browser to view the book."
}

# Generate combined PDF
generate_pdf() {
    if [[ "$PDF_ENABLED" != true ]]; then
        print_warning "Skipping PDF generation (LaTeX not available)"
        return
    fi
    
    print_status "Generating PDF..."
    
    # Create a combined markdown file
    combined_md="$PDF_DIR/ComputoPermutoBook.md"
    
    print_status "Creating combined markdown file..."
    
    # Add title page
    cat > "$combined_md" << 'EOF'
---
title: "ComputoPermuto: A Practical Guide to JSON Transformations"
author: ""
date: ""
documentclass: book
geometry: margin=1in
fontsize: 11pt
colorlinks: true
linkcolor: blue
urlcolor: blue
toccolor: black
---

\newpage
\tableofcontents
\newpage

EOF
    
    # Combine all markdown files in order
    chapter_files=(
        "book/00_index.md"
        "book/01_why_transformation_matters.md"
        "book/02_setting_up_environment.md"
        "book/03_computo_basics.md"
        "book/04_permuto_basics.md"
        "book/05_control_flow.md"
        "book/06_working_with_arrays.md"
        "book/07_object_manipulation.md"
        "book/08_advanced_array_ops.md"
        "book/09_template_driven_transformations.md"
        "book/10_data_pipeline_patterns.md"
        "book/11_complex_real-world_examples.md"
        "book/12_performance_and_optimization.md"
        "book/13_error_handling_and_debugging.md"
        "book/14_best_practices_and_patterns.md"
        "book/15_multiple_inputs_and_json_patch.md"
        "book/appendices/A_operator_reference.md"
    )
    
    for chapter in "${chapter_files[@]}"; do
        if [[ -f "$chapter" ]]; then
            print_status "Adding $(basename "$chapter")"
            echo "" >> "$combined_md"
            echo '\newpage' >> "$combined_md"
            echo "" >> "$combined_md"
            # Filter out problematic YAML-like lines that aren't real YAML
            sed 's/^---$/\\rule{\\textwidth}{0.4pt}/' "$chapter" >> "$combined_md"
            echo "" >> "$combined_md"
            echo "" >> "$combined_md"
        fi
    done
    
    # Generate PDF using pandoc
    print_status "Converting to PDF..."
    pandoc "$combined_md" \
        --from markdown \
        --to pdf \
        --pdf-engine=pdflatex \
        --variable=geometry:margin=1in \
        --variable=fontsize:11pt \
        --variable=documentclass:article \
        --table-of-contents \
        --number-sections \
        --output "$PDF_DIR/ComputoPermutoBook.pdf"
    
    print_status "PDF generated: $PDF_DIR/ComputoPermutoBook.pdf"
}

# Open browser function
open_browser() {
    if command -v xdg-open &> /dev/null; then
        xdg-open "$HTML_DIR/index.html"
    elif command -v open &> /dev/null; then
        open "$HTML_DIR/index.html"
    else
        print_status "Please open $HTML_DIR/index.html in your browser"
    fi
}

# Main execution
main() {
    print_status "Starting ComputoPermutoBook build..."
    
    check_dependencies
    setup_directories
    generate_html
    
    if [[ "$1" == "--pdf" ]] || [[ "$1" == "--all" ]]; then
        generate_pdf
    fi
    
    if [[ "$1" == "--open" ]] || [[ "$1" == "--all" ]]; then
        open_browser
    fi
    
    print_status "Build complete!"
    echo ""
    echo "HTML Book: file://$(realpath "$HTML_DIR/index.html")"
    if [[ "$PDF_ENABLED" == true ]] && ([[ "$1" == "--pdf" ]] || [[ "$1" == "--all" ]]); then
        echo "PDF Book: $(realpath "$PDF_DIR/ComputoPermutoBook.pdf")"
    fi
    echo ""
    echo "Usage:"
    echo "  ./build.sh           # Generate HTML only"
    echo "  ./build.sh --pdf     # Generate HTML + PDF"
    echo "  ./build.sh --open    # Generate HTML and open browser"
    echo "  ./build.sh --all     # Generate everything and open browser"
}

# Run main function with all arguments
main "$@"