# Book Generation Scripts

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
- `build_all_chapters.py` - Build all chapters and create ZIP files

## Requirements

- Python 3.11+ (for built-in `tomllib` support)
- Virtual environment already set up at `../venv/`

## Usage

### Quick Start

From the project root directory:

```bash
# Activate the virtual environment
source venv/bin/activate

# Generate a single chapter
python scripts/generate_book_chapter.py book-source/ch03_complete.toml

# Generate HTML from markdown
python scripts/generate_html.py new_way/03_complete.md

# Build all chapters and HTML files
python scripts/build_all_chapters.py
```

### Workflow

1. **Edit TOML files** in `book-source/` - these are your source of truth
2. **Generate markdown** using `generate_book_chapter.py`
3. **Generate HTML** using `generate_html.py` or `build_all_chapters.py`
4. **Review output** in `new_way/` (markdown) and `docs/` (HTML)

### Output Structure

- **Markdown files** → `new_way/`
- **HTML files** → `docs/`
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