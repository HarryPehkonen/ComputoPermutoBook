#!/bin/bash
# Run input_access_whole example
# Usage: ./run.sh

echo "Running input_access_whole example..."
echo "Command: computo  script.json input.json"
echo ""

computo  script.json input.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
