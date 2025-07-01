@echo off
REM Run basic_usage example
REM Usage: run.bat

echo Running basic_usage example...
echo Command: computo --pretty=2 script.json input.json
echo.

computo --pretty=2 script.json input.json

echo.
echo Expected output:
type expected.json
echo.
pause
