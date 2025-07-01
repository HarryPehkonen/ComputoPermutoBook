#!/bin/bash
# Run nested_operation_flow example
# Usage: ./run.sh

echo "Running nested_operation_flow example..."
echo "Command: computo --trace script.json"
echo ""

computo --trace script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
