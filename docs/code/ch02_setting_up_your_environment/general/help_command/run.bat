@echo off
REM Run help_command example
REM Usage: run.bat

echo Running help_command example...
echo Command: computo --help script.json
echo.

computo --help script.json

echo.
echo Expected output:
type expected.json
echo.
pause
