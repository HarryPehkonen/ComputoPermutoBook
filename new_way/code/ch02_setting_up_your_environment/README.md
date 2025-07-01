# Chapter 2: Setting Up Your Environment - Code Examples

This directory contains all runnable code examples from Chapter 2.

## Quick Start

Each example directory contains:
- `script.json` - The Computo script
- `input.json` - Input data for the script (when needed)
- `expected.json` - Expected output
- `run.sh` - Linux/Mac script to run the example
- `run.bat` - Windows script to run the example
- `metadata.json` - Example metadata and description

## Running Examples

### Linux/Mac:
```bash
cd example_name/
./run.sh
```

### Windows:
```cmd
cd example_name
run.bat
```

### Manual:
```bash
# For examples with input data:
computo script.json input.json

# For examples without input data:
computo script.json
```

## Examples by Section

### General

- **help_command**: Display help information to verify CLI is working
- **version_check**: Check Computo version to verify installation
- **basic_usage**: Basic script execution to verify end-to-end functionality

## Requirements

- Computo installed and available in PATH
- All examples have been validated to work correctly

## Download

- [Download this chapter's examples](ch02_examples.zip)
- [Download all book examples](../download_all_examples.zip)

---
*Generated automatically from Chapter 2 source*
