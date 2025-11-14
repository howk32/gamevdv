@echo off
chcp 65001 >nul
setlocal

:: Set the specific Python interpreter path
set PYTHON_PATH=D:\Panda3D-1.10.15-x64\python\python.exe

:: Check if the specific Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo Error: Specified Python interpreter not found: %PYTHON_PATH%
    echo Please check the Python interpreter path
    pause
    exit /b 1
)

:: Check if Python is accessible
"%PYTHON_PATH%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python cannot be run. Please check Python installation
    pause
    exit /b 1
)

:: Install required packages using the specific Python interpreter
echo Installing Pygame...
"%PYTHON_PATH%" -m pip install pygame
if %errorlevel% neq 0 (
    echo Error: Failed to install Pygame
    echo Make sure you have internet connection
    pause
    exit /b 1
)

echo.
echo Pygame has been successfully installed!
echo You can now run the game using run_all.bat
echo.
pause