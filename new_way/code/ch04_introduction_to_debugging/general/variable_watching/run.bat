@echo off
REM Run variable_watching example
REM Usage: run.bat

echo Running variable_watching example...
echo Command: computo --trace --pretty=2 script.json
echo.

computo --trace --pretty=2 script.json

echo.
echo Expected output:
type expected.json
echo.
pause
