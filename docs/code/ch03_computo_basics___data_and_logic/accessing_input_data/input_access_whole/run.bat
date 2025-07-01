@echo off
REM Run input_access_whole example
REM Usage: run.bat

echo Running input_access_whole example...
echo Command: computo  script.json input.json
echo.

computo  script.json input.json

echo.
echo Expected output:
type expected.json
echo.
pause
