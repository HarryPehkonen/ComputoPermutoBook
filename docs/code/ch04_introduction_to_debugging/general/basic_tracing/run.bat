@echo off
REM Run basic_tracing example
REM Usage: run.bat

echo Running basic_tracing example...
echo Command: computo --trace --pretty=2 script.json
echo.

computo --trace --pretty=2 script.json

echo.
echo Expected output:
type expected.json
echo.
pause
