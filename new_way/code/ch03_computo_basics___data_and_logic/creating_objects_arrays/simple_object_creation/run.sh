#!/bin/bash
# Run simple_object_creation example
# Usage: ./run.sh

echo "Running simple_object_creation example..."
echo "Command: computo --pretty=2 script.json"
echo ""

computo --pretty=2 script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
