@echo off
REM Run performance_profiling example
REM Usage: run.bat

echo Running performance_profiling example...
echo Command: computo --profile --pretty=2 script.json
echo.

computo --profile --pretty=2 script.json

echo.
echo Expected output:
type expected.json
echo.
pause
