@echo off
REM Run array_operation_tracing example
REM Usage: run.bat

echo Running array_operation_tracing example...
echo Command: computo --trace script.json
echo.

computo --trace script.json

echo.
echo Expected output:
type expected.json
echo.
pause
