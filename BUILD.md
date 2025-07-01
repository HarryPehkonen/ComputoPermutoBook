# Building the ComputoPermuto Book

This directory contains a complete build system for converting the markdown book into HTML (for browser viewing) and PDF formats.

## Quick Start

```bash
# Generate HTML for browser viewing
./build_old.sh

# Generate HTML and open in browser
./build_old.sh --open

# Generate HTML + PDF
./build_old.sh --pdf

# Generate everything and open browser
./build_old.sh --all
```

## Prerequisites

### Required
- **pandoc** - Universal document converter
  ```bash
  # Ubuntu/Debian
  sudo apt-get install pandoc
  
  # macOS
  brew install pandoc
  
  # Windows: Download from https://pandoc.org/installing.html
  ```

### Recommended (for PDF generation)
- **LaTeX distribution** - Required for PDF output
  ```bash
  # Ubuntu/Debian (install complete LaTeX packages for PDF generation)
  sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-latex-extra
  
  # macOS
  brew install --cask mactex
  
  # Windows: Install MiKTeX or TeX Live
  ```
  
**Note:** PDF generation requires both pandoc AND a complete LaTeX distribution. Install all three packages for full PDF support:

```bash
# Complete installation for PDF generation
sudo apt-get install pandoc texlive-latex-base texlive-latex-recommended texlive-latex-extra
```

## Output Structure

After running the build script:

```
output/
├── html/
│   ├── index.html          # Main navigation page
│   ├── style.css           # Styling for all pages
│   ├── 00_index.html       # Book table of contents
│   ├── 01_why_transformation_matters.html
│   ├── 02_setting_up_environment.html
│   ├── ...                 # All chapter files
│   └── appendices/
│       └── A_operator_reference.html
├── pdf/
│   ├── ComputoPermutoBook.pdf    # Complete book as PDF
│   └── ComputoPermutoBook.md     # Combined markdown source
└── (README files are linked directly to GitHub repositories)
```

## Features

### HTML Output
- **Clean, readable styling** with syntax highlighting
- **Navigation index** with links to all chapters
- **Responsive design** that works on desktop and mobile
- **Cross-references** between chapters work as links
- **No internet required** - all assets are local

### PDF Output
- **Professional book layout** with table of contents
- **Proper chapter numbering** and page breaks
- **Syntax highlighting** for code blocks
- **Hyperlinked cross-references** within the document
- **Single file** - easy to share or print

## Development Workflow

1. **Edit markdown files** in the `book/` directory
2. **Run build script** to see changes: `./build_old.sh --open`
3. **Refresh browser** to see updates
4. **Generate PDF** when ready: `./build_old.sh --pdf`

## Customization

### Styling
Edit `build_old.sh` and modify the CSS generation section to customize appearance.

### PDF Layout
Modify the pandoc PDF generation options in the `generate_pdf()` function.

### Chapter Order
Update the `chapter_files` array in the build script to change chapter ordering.

## Troubleshooting

### "pandoc: command not found"
Install pandoc using your system's package manager (see Prerequisites above).

### "pdflatex: command not found"
Install a LaTeX distribution. PDF generation will be skipped if LaTeX is not available.

### Permission Denied
Make sure the build script is executable: `chmod +x build_old.sh`

### Browser doesn't open automatically
The script will print the file path. Manually open `output/html/index.html` in your browser.

## File Watching (Optional)

For automatic rebuilds during development, you can use a file watcher:

```bash
# Install inotify-tools (Linux) or fswatch (macOS)
sudo apt-get install inotify-tools  # Linux
brew install fswatch                # macOS

# Watch for changes and rebuild (Linux)
while inotifywait -e modify -r book/; do ./build_old.sh; done

# Watch for changes and rebuild (macOS)
fswatch -o book/ | xargs -n1 -I{} ./build_old.sh
```

This will automatically regenerate the HTML whenever you save changes to any markdown file.
