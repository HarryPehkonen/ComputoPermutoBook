# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **ComputoPermutoBook** - a comprehensive documentation project that creates both HTML and PDF versions of a practical guide for learning Computo and Permuto JSON transformation tools. The project uses markdown source files and build scripts to generate formatted output in multiple formats.

## Build Commands

### HTML Generation (Recommended for Development)

```bash
# Quick HTML build using Python markdown (minimal dependencies)
./simple-build.sh

# Generate HTML and open in browser  
./simple-build.sh --open
```

### Full Build with pandoc (Requires pandoc installation)

```bash
# Generate HTML only
./build.sh

# Generate HTML and open in browser
./build.sh --open

# Generate HTML + PDF (requires LaTeX)
./build.sh --pdf

# Generate everything and open browser
./build.sh --all
```

### Prerequisites

For `simple-build.sh` (recommended):
- Python 3 with `markdown` library (auto-installed if missing)

For `build.sh` (full features):
- pandoc
- LaTeX distribution (for PDF output)

## Project Architecture

### Content Structure

- **`book/`** - Main content as markdown files
  - `00_index.md` - Book table of contents and navigation
  - `01_*.md` through `15_*.md` - Individual chapters
  - `appendices/A_operator_reference.md` - Reference documentation
  
- **Build System**
  - `simple-build.sh` - Lightweight Python-based HTML generator
  - `build.sh` - Full pandoc-based build system (HTML + PDF)
  - `BUILD.md` - Detailed build documentation

- **Output Structure** (`output/` directory)
  - `html/` - Generated HTML files with navigation
  - `pdf/` - Combined PDF book (when using build.sh --pdf)
  - `*.html` - README file conversions

### Documentation Ecosystem

The project documents two related tools:
- **Computo** - JSON transformation engine with Lisp-like syntax
- **Permuto** - Template processing with `${path}` syntax

Content covers practical usage patterns, from basic syntax to complex real-world transformations including JSON Patch operations and multi-document processing.

### Build Script Architecture

**simple-build.sh** features:
- Pure Python markdown conversion with minimal dependencies
- Self-contained CSS generation
- Automatic dependency installation
- Cross-platform browser opening

**build.sh** features:  
- pandoc-based conversion with advanced formatting
- PDF generation via LaTeX
- Professional styling and layout
- Table of contents generation

## Development Workflow

1. Edit markdown files in `book/` directory
2. Run build script to generate output: `./simple-build.sh --open`
3. Refresh browser to see changes
4. For final PDF: `./build.sh --pdf`

## Key Files

- **Content**: Files in `book/` directory are the source of truth
- **Build Config**: Chapter ordering defined in `build.sh` script's `chapter_files` array
- **Styling**: CSS embedded in build scripts (not separate files)
- **Output**: All generated files go to `output/` directory

## Operator Documentation Maintenance

When adding new operators or updating existing ones, you MUST update multiple locations to maintain consistency across the book. This is a critical workflow that ensures complete documentation coverage.

### Adding a New Operator

**Step 1: Determine Placement**
- **Mathematical operators** (`+`, `-`, `*`, `/`) → Chapter 3 (Computo Basics)
- **Comparison operators** (`>`, `<`, `==`, `!=`, `approx`) → Chapter 5 (Control Flow)
- **Logical operators** (`if`, `&&`, `||`) → Chapter 5 (Control Flow)
- **Array operators** (`map`, `filter`, `reduce`, `find`, `some`, `every`, `flatMap`) → Chapter 6 or 8
- **Object operators** (`obj`, `merge`) → Chapter 7 (Object Manipulation)
- **Template operators** (`permuto.apply`) → Chapter 4 (Permuto Basics)
- **Data access operators** (`$input`, `$inputs`, `get`, `let`, `$`) → Chapter 3 or 15
- **JSON Patch operators** (`diff`, `patch`) → Chapter 15
- **List processing operators** (`car`, `cdr`, `count`) → Chapter 15

**Step 2: Add to Primary Chapter**
1. Add comprehensive explanation with syntax
2. Include 2-3 practical examples showing real-world usage
3. Use `/* comment */` syntax to explain complex logic
4. Show both simple and advanced use cases
5. Demonstrate integration with other operators when relevant

**Step 3: Update Chapter Summary**
- Add the new operator to the "In This Chapter" section
- Include a brief description of what the operator does
- Mention key benefits or use cases

**Step 4: Update Index (book/00_index.md)**
- Add operator to the "Operators introduced" bullet point for the appropriate chapter
- Include any important notes (e.g., "with short-circuit evaluation")

**Step 5: Update Appendix A (book/appendices/A_operator_reference.md)**
- Add complete reference entry with:
  - Clear syntax specification
  - Brief description
  - At least one example
  - Important behavioral notes (e.g., short-circuit, error conditions)
- Update the total operator count in the appendix header
- Place in the appropriate category (Logic & Control Flow, Array Operators, etc.)

**Step 6: Update Index Appendix Reference**
- Update the operator count in the appendix description in `book/00_index.md`

### Updating an Existing Operator

**When updating operator behavior or adding new capabilities:**

1. **Update primary chapter** - Modify examples and explanations
2. **Update appendix reference** - Ensure syntax and examples are current
3. **Check cross-references** - Search for mentions in other chapters
4. **Verify examples still work** - Test any code examples that changed

### Consistency Requirements

**Examples must be:**
- **Practical and realistic** - Use real-world scenarios (user management, financial calculations, etc.)
- **Progressive** - Start simple, build to complex
- **Complete** - Show input data, script, and expected output
- **Educational** - Use comments to explain non-obvious logic

**Chapter summaries must:**
- List ALL operators introduced in that chapter
- Include important behavioral notes (truthiness, short-circuit, etc.)
- Mention key integration patterns with other operators

**Index must:**
- Show all operators for each chapter in a single bullet point
- Include total operator count in appendix reference
- Reflect the current state of documentation

### Validation Checklist

When adding/updating operators, verify:
- [ ] Operator appears in appropriate chapter with full explanation
- [ ] Chapter summary includes the operator
- [ ] Index shows operator in correct chapter
- [ ] Appendix A has complete reference entry
- [ ] Appendix A operator count is updated
- [ ] Index appendix reference shows correct count
- [ ] All examples use realistic scenarios
- [ ] Comments explain complex logic
- [ ] Cross-references are updated if needed

### Common Mistakes to Avoid

1. **Forgetting the appendix** - Every operator must have a reference entry
2. **Inconsistent operator counts** - Index and appendix must match
3. **Incomplete chapter summaries** - Must list ALL operators from that chapter
4. **Toy examples** - Use realistic business scenarios, not simple math
5. **Missing integration examples** - Show how operators work together
6. **Outdated cross-references** - Check mentions in other chapters

## File Watching (Optional Development Enhancement)

```bash
# Linux
while inotifywait -e modify -r book/; do ./simple-build.sh; done

# macOS  
fswatch -o book/ | xargs -n1 -I{} ./simple-build.sh
```