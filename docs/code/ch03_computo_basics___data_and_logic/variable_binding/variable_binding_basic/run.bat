@echo off
REM Run variable_binding_basic example
REM Usage: run.bat

echo Running variable_binding_basic example...
echo Command: computo  script.json
echo.

computo  script.json

echo.
echo Expected output:
type expected.json
echo.
pause
