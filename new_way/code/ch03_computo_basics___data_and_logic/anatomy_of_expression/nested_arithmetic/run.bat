@echo off
REM Run nested_arithmetic example
REM Usage: run.bat

echo Running nested_arithmetic example...
echo Command: computo  script.json
echo.

computo  script.json

echo.
echo Expected output:
type expected.json
echo.
pause
