@echo off
REM Run simple_object_creation example
REM Usage: run.bat

echo Running simple_object_creation example...
echo Command: computo --pretty=2 script.json
echo.

computo --pretty=2 script.json

echo.
echo Expected output:
type expected.json
echo.
pause
