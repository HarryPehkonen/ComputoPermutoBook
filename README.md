# ComputoPermutoBook

**Professional documentation for Computo and Permuto JSON transformation tools**

📖 **[Read the Book Online](https://harrypehkonen.github.io/ComputoPermutoBook/)**

## What is this?

This repository generates comprehensive documentation for:

- **[Computo](https://github.com/HarryPehkonen/Computo)** - A safe, sandboxed JSON transformation engine with Lisp-like syntax
- **[Permuto](https://github.com/HarryPehkonen/Permuto)** - A lightweight JSON templating engine for declarative data transformation

The book teaches JSON transformation through practical examples, from basic operations to advanced enterprise patterns.

## Features

✅ **Single Source of Truth** - All content in structured TOML files  
✅ **Validated Examples** - Every code example is tested automatically  
✅ **Multiple Formats** - Generates both Markdown and HTML  
✅ **Downloadable Code** - Organized examples with cross-platform run scripts  
✅ **Professional Styling** - Clean, navigable HTML documentation  

## Quick Start

**Read the documentation:** [ComputoPermutoBook](https://harrypehkonen.github.io/ComputoPermutoBook/)

**Build locally:** See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## Repository Structure

```
ComputoPermutoBook/
├── book-source/          # Source TOML files (single source of truth)
├── scripts/              # Python build scripts
├── new_way/             # Generated markdown files
├── docs/                # Generated HTML website
├── BUILD_INSTRUCTIONS.md # Detailed setup guide
└── README.md            # This file
```

## Chapter Overview

1. **Why JSON Transformation Matters** - Problem space and solution overview
2. **Setting Up Your Environment** - Installation and verification
3. **Computo Basics** - Core syntax and fundamental operations
4. **Introduction to Debugging** - Essential debugging techniques
5. **Control Flow and Conditionals** - Decision-making logic
6. **Working with Arrays** - Array processing and transformations
7. **Object Construction and Manipulation** - Building and reshaping JSON objects
8. **Advanced Array Operations** - Filter, reduce, and specialized array operators
9. **Template-Driven Transformations** - Introduction to Permuto templating
10. **Data Pipeline Patterns** - Real-world transformation patterns
11. **Advanced Permuto Techniques** - Enterprise-grade templating

## Building the Book

**Prerequisites:** Computo and Permuto installed, Python 3.11+

**Quick build:**
```bash
# Clone and setup
git clone https://github.com/HarryPehkonen/ComputoPermutoBook.git
cd ComputoPermutoBook
python3 -m venv venv && source venv/bin/activate
pip install tomli markdown

# Build with validation
python scripts/build_all_chapters.py --validate
```

**Output:** 
- Markdown files in `new_way/`
- HTML website in `docs/`
- Downloadable code examples organized by chapter

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for complete setup details.

## Contributing

Contributions welcome! Please:

1. Read [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
2. Test your changes with `--validate` 
3. Ensure all examples work with current Computo/Permuto versions
4. Submit pull requests against the main branch

## Architecture

This project uses a sophisticated documentation generation system:

- **TOML Sources** - Structured chapter content with embedded examples
- **Validation Pipeline** - Every example is executed and verified
- **Multi-Format Output** - Clean markdown and styled HTML
- **Example Distribution** - Organized code with cross-platform scripts

The build system ensures 100% accuracy by testing every code example against the actual Computo and Permuto tools.

## License

This documentation project is in the public domain. See individual Computo and Permuto repositories for their respective licenses.

## Related Projects

- **[Computo](https://github.com/HarryPehkonen/Computo)** - The transformation engine
- **[Permuto](https://github.com/HarryPehkonen/Permuto)** - The templating engine
