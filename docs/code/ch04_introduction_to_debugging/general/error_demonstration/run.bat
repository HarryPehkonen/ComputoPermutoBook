@echo off
REM Run error_demonstration example
REM Usage: run.bat

echo Running error_demonstration example...
echo Command: computo --pretty=2 script.json
echo.

computo --pretty=2 script.json

echo.
echo Expected output:
type expected.json
echo.
pause
