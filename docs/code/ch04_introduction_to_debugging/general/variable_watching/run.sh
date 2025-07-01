#!/bin/bash
# Run variable_watching example
# Usage: ./run.sh

echo "Running variable_watching example..."
echo "Command: computo --trace --pretty=2 script.json"
echo ""

computo --trace --pretty=2 script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
