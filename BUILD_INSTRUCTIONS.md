# Building ComputoPermutoBook Locally

This guide helps contributors set up and build the ComputoPermutoBook documentation locally.

## Prerequisites

### Required Software

1. **Python 3.11+** (for built-in `tomllib` support)
   - Alternative: Python 3.7+ with `tomli` package
2. **Git** (for cloning repositories)
3. **C++17 compiler** (GCC, Clang, or MSVC)
4. **CMake 3.15+**
5. **nlohmann/json development headers**

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake git nlohmann-json3-dev python3 python3-pip
```

**macOS:**
```bash
brew install cmake nlohmann-json python3
```

**Windows:**
- Install Visual Studio with C++ support
- Install CMake
- Install Python 3.11+

## Step 1: Install Computo and Permuto

The book generation requires both Computo and Permuto to be installed and available in your PATH.

### Install Permuto

```bash
# Clone and build Permuto
git clone https://github.com/HarryPehkonen/Permuto.git
cd Permuto
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
sudo cmake --install build
cd ..
```

### Install Computo

```bash
# Clone and build Computo (depends on Permuto)
git clone https://github.com/HarryPehkonen/Computo.git
cd Computo
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
sudo cmake --install build
cd ..
```

### Verify Installation

```bash
# Test that both tools are available
computo --version
permuto --version

# Test basic functionality
echo '["obj", ["message", "Hello World"]]' > test_script.json
echo '{}' > test_input.json
computo test_script.json test_input.json
rm test_script.json test_input.json
```

## Step 2: Set Up Python Environment

### Clone the Book Repository

```bash
git clone https://github.com/HarryPehkonen/ComputoPermutoBook.git
cd ComputoPermutoBook
```

### Create Virtual Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# Or on Windows: venv\Scripts\activate
```

### Install Python Dependencies

```bash
# Install required packages
pip install tomli markdown

# For Python 3.11+, tomli is optional (uses built-in tomllib)
# For older Python versions, tomli is required
```

## Step 3: Build the Book

### Quick Build (Recommended)

Build everything with validation:

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Build all chapters with example validation
python scripts/build_all_chapters.py --validate
```

### Build Options

**Full build with validation:**
```bash
python scripts/build_all_chapters.py --validate --html
```

**Build without validation (faster):**
```bash
python scripts/build_all_chapters.py --no-html
```

**Build only markdown (skip HTML):**
```bash
python scripts/build_all_chapters.py --no-html
```

**Specify custom paths:**
```bash
python scripts/build_all_chapters.py \
  --source-dir book-source \
  --output-dir new_way \
  --computo-path /usr/local/bin/computo
```

### Individual Chapter Build

Build a single chapter:

```bash
python scripts/generate_book_chapter.py book-source/ch03_computo_basics.toml --validate
```

### HTML-Only Generation

Generate HTML from existing markdown:

```bash
python scripts/generate_html.py --input-dir new_way --output-dir docs
```

## Expected Output Structure

After a successful build:

```
ComputoPermutoBook/
├── new_way/                    # Generated markdown files
│   ├── 01_why_transformation_matters.md
│   ├── 02_setting_up_environment.md
│   ├── ...
│   ├── code/                   # Organized code examples
│   │   ├── ch02_setting_up_your_environment/
│   │   ├── ch03_computo_basics___data_and_logic/
│   │   └── ...
│   ├── download_all_examples.zip
│   └── build_summary.md
├── docs/                       # Generated HTML website
│   ├── index.html
│   ├── 01_why_transformation_matters.html
│   ├── ...
│   └── code/                   # Copy of code examples
└── book-source/                # Source TOML files (input)
```

## Validation and Testing

### Example Validation

The build system validates every code example by:

1. **Execution Test**: Running each script through Computo
2. **Output Verification**: Comparing actual vs expected output
3. **CLI Flag Testing**: Verifying flags like `--interpolation`, `--trace`, `--profile`
4. **Cross-Platform Scripts**: Generating `run.sh` and `run.bat` for each example

### Test Reports

Validation generates detailed reports:

- `new_way/ch{NN}_test_report.md` - Per-chapter test results
- `new_way/build_summary.md` - Overall build status

### Manual Testing

Test individual examples:

```bash
# Navigate to any example directory
cd new_way/code/ch03_computo_basics___data_and_logic/first_transformation/simple_addition/

# Run the example
./run.sh          # Linux/Mac
# or
run.bat           # Windows
# or
computo script.json input.json
```

## Troubleshooting

### Common Issues

**"computo command not found":**
- Ensure Computo is installed and in PATH
- Try specifying full path: `--computo-path /usr/local/bin/computo`

**"tomli package not found":**
- Install with: `pip install tomli`
- Or upgrade to Python 3.11+ to use built-in tomllib

**Build fails during validation:**
- Check that all examples in TOML files are correct
- Run individual chapters to isolate issues
- Check test reports in `new_way/ch{NN}_test_report.md`

**Permission errors during installation:**
- Use `sudo` for system-wide installation of Computo/Permuto
- Or install to user directory with `--prefix=~/.local`

### Debug Mode

Run with verbose output:

```bash
# Build with detailed output
python scripts/build_all_chapters.py --validate --verbose

# Test single example with tracing
computo --trace --pretty=2 script.json input.json
```

## Development Workflow

### Editing Chapters

1. Edit TOML files in `book-source/`
2. Run validation: `python scripts/build_all_chapters.py --validate`
3. Check output in `new_way/` and `docs/`
4. Review test reports for any failures

### Adding New Examples

1. Add example to appropriate TOML file
2. Include all required fields: `name`, `description`, `script`, `expected`
3. Add `input` if needed, `cli_flags` if using special flags
4. Run validation to ensure example works

### Local Development Server

For HTML preview:

```bash
# Simple HTTP server for local testing
cd docs
python3 -m http.server 8000
# Open http://localhost:8000 in browser
```

## Contributing

When contributing:

1. **Test your changes**: Always run `--validate` before submitting
2. **Update examples**: Ensure all examples actually work with current Computo/Permuto
3. **Cross-platform**: Test on multiple operating systems if possible
4. **Documentation**: Update this file if you change build requirements

## GitHub Actions (Future)

When CI/CD is set up, the build will automatically:

1. Install Computo and Permuto from source
2. Run full validation on all examples
3. Generate and deploy HTML to GitHub Pages
4. Create downloadable releases with code examples

The current scripts are designed to be GitHub Actions compatible. 