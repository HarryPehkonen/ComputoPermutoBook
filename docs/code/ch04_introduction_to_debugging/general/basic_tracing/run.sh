#!/bin/bash
# Run basic_tracing example
# Usage: ./run.sh

echo "Running basic_tracing example..."
echo "Command: computo --trace --pretty=2 script.json"
echo ""

computo --trace --pretty=2 script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
