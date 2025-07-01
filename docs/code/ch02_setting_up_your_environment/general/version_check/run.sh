#!/bin/bash
# Run version_check example
# Usage: ./run.sh

echo "Running version_check example..."
echo "Command: computo --version script.json"
echo ""

computo --version script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
