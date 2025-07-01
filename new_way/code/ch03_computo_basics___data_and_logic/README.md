# Chapter 3: Computo Basics - Data and Logic - Code Examples

This directory contains all runnable code examples from Chapter 3.

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

### Your First Transformation: Simple Arithmetic

- **simple_addition**: Basic addition demonstrating core Computo syntax
- **nested_arithmetic**: Nested arithmetic operations showing operator composition

### Mathematical Operations

- **modulo_remainder**: Basic modulo operation for remainder calculation

### Creating Objects and Arrays

- **simple_object_creation**: Creating a JSON object with computed values

### Accessing Input Data with `$input` and `get`

- **input_access_whole**: Access entire input document using $input

### Storing Intermediate Values with `let` and `$`

- **variable_binding_basic**: Simple variable binding with let for reuse

## Requirements

- Computo installed and available in PATH
- All examples have been validated to work correctly

## Download

- [Download this chapter's examples](ch03_examples.zip)
- [Download all book examples](../download_all_examples.zip)

---
*Generated automatically from Chapter 3 source*
