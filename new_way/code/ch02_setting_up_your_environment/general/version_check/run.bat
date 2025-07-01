@echo off
REM Run version_check example
REM Usage: run.bat

echo Running version_check example...
echo Command: computo --version script.json
echo.

computo --version script.json

echo.
echo Expected output:
type expected.json
echo.
pause
