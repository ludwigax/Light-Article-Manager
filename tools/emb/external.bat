@echo off
if "%~1"=="" (
    echo "To Use: embed.bat {embed|similarity} Param_B"
    exit /b 1
)

if "%~2"=="" (
    echo "Please provide a second parameter (Param_B)"
    exit /b 1
)

call activate lang

if "%~1"=="embed" (
    python embed.py %2
) else if "%~1"=="similarity" (
    python similarity.py %2
) else if "%~1"=="inference" (
    python inference.py %2
) else (
    echo Invalid first parameter. Use either 'embed' or 'similarity'.
    exit /b 1
)