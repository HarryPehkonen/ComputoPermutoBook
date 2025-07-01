# Build Generation Scripts

This directory contains Python scripts for generating the ComputoPermutoBook from TOML source files.

## Overview

The book uses a single-source-of-truth approach where all content is stored in structured TOML files in `book-source/`, then generated into multiple output formats.

## Directory Structure

```
./book/           - Original markdown files (keep as reference)
./book-source/    - TOML source files (single source of truth)
./new_way/        - Generated markdown files  
./docs/           - Generated HTML files
./scripts/        - Generation scripts (this directory)
```

## Available Scripts

- `generate_book_chapter.py` - Generate markdown chapter from TOML source
- `generate_html.py` - Convert markdown to HTML with styling
- `build_all_chapters.py` - Build all chapters and create HTML files (recommended)

## Requirements

- Python 3.11+ (for built-in `tomllib` support)
- Virtual environment already set up at `../venv/`

## Usage

### Quick Start (Recommended)

From the project root directory:

```bash
# Activate the virtual environment
source venv/bin/activate

# Build everything (markdown + HTML + downloads)
python scripts/build_all_chapters.py

# Build with example validation
python scripts/build_all_chapters.py --validate

# Build only markdown (skip HTML)
python scripts/build_all_chapters.py --no-html
```

### Individual Commands

```bash
# Generate a single chapter
python scripts/generate_book_chapter.py book-source/ch03_complete.toml

# Generate HTML from existing markdown
python scripts/generate_html.py

# Generate HTML to custom directory
python scripts/generate_html.py --input-dir new_way --output-dir docs
```

### Workflow

1. **Edit TOML files** in `book-source/` - these are your source of truth
2. **Run build script**: `python scripts/build_all_chapters.py`
3. **Review output** in `new_way/` (markdown) and `docs/` (HTML)
4. **Open in browser**: `docs/index.html`

### Output Structure

- **Markdown files** → `new_way/`
- **HTML files** → `docs/` (with navigation and styling)
- **Example code** → `new_way/code/` and `new_way/examples/`
- **ZIP downloads** → `new_way/*.zip`

## TOML File Structure

Each chapter TOML file contains:

- **Metadata** - title, chapter number, operators introduced
- **Content sections** - introduction, concepts, examples
- **Examples** - with input/output data and test scripts
- **Code samples** - inline and downloadable examples

See existing files in `book-source/` for examples.

## Benefits

- **Single Source of Truth**: Edit content in one place
- **Verified Examples**: All code examples are tested
- **Multiple Formats**: Generate markdown, HTML, and more
- **Consistent Structure**: Standardized chapter layout
- **Easy Maintenance**: Changes propagate automatically 