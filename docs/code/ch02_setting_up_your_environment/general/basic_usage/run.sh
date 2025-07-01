#!/bin/bash
# Run basic_usage example
# Usage: ./run.sh

echo "Running basic_usage example..."
echo "Command: computo --pretty=2 script.json input.json"
echo ""

computo --pretty=2 script.json input.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
