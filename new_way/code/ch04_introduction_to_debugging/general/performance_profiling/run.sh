#!/bin/bash
# Run performance_profiling example
# Usage: ./run.sh

echo "Running performance_profiling example..."
echo "Command: computo --profile --pretty=2 script.json"
echo ""

computo --profile --pretty=2 script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
