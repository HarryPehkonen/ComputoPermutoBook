@echo off
REM Run modulo_remainder example
REM Usage: run.bat

echo Running modulo_remainder example...
echo Command: computo  script.json
echo.

computo  script.json

echo.
echo Expected output:
type expected.json
echo.
pause
