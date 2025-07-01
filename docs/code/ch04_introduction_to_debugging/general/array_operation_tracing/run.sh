#!/bin/bash
# Run array_operation_tracing example
# Usage: ./run.sh

echo "Running array_operation_tracing example..."
echo "Command: computo --trace script.json"
echo ""

computo --trace script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
