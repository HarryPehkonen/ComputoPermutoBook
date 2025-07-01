#!/bin/bash
# Run error_demonstration example
# Usage: ./run.sh

echo "Running error_demonstration example..."
echo "Command: computo --pretty=2 script.json"
echo ""

computo --pretty=2 script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
