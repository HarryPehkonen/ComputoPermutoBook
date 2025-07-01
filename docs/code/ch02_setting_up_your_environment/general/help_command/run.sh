#!/bin/bash
# Run help_command example
# Usage: ./run.sh

echo "Running help_command example..."
echo "Command: computo --help script.json"
echo ""

computo --help script.json

echo ""
echo "Expected output:"
cat expected.json
echo ""
