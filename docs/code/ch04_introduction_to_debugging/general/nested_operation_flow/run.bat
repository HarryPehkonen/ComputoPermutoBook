@echo off
REM Run nested_operation_flow example
REM Usage: run.bat

echo Running nested_operation_flow example...
echo Command: computo --trace script.json
echo.

computo --trace script.json

echo.
echo Expected output:
type expected.json
echo.
pause
