@echo off
REM Run simple_addition example
REM Usage: run.bat

echo Running simple_addition example...
echo Command: computo  script.json
echo.

computo  script.json

echo.
echo Expected output:
type expected.json
echo.
pause
