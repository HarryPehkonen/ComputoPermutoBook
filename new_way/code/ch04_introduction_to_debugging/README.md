# Chapter 4: Introduction to Debugging - Code Examples

This directory contains all runnable code examples from Chapter 4.

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

- **basic_tracing**: Basic execution tracing to see operation flow
- **array_operation_tracing**: Trace array operations to understand iteration
- **performance_profiling**: Basic performance profiling to identify slow operations
- **variable_watching**: Watch variable creation and usage in complex expressions
- **error_demonstration**: Demonstrate clear error messages for common mistakes
- **nested_operation_flow**: Trace complex nested operations to understand execution order

## Requirements

- Computo installed and available in PATH
- All examples have been validated to work correctly

## Download

- [Download this chapter's examples](ch04_examples.zip)
- [Download all book examples](../download_all_examples.zip)

---
*Generated automatically from Chapter 4 source*
