@echo off
chcp 65001 >nul
setlocal

:: Set the specific Python interpreter path
set PYTHON_PATH=D:\Panda3D-1.10.15-x64\python\python.exe

:: Check if the specific Python interpreter exists
if not exist "%PYTHON_PATH%" (
    echo Ошибка: Указанный интерпретатор Python не найден: %PYTHON_PATH%
    echo Пожалуйста, проверьте путь к интерпретатору Python
    pause
    exit /b 1
)

:: Check if Python is accessible
"%PYTHON_PATH%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не может быть запущен. Пожалуйста, проверьте установку Python
    pause
    exit /b 1
)

:: Check if necessary files exist
echo Проверка наличия необходимых файлов...
if not exist "space_shooter_russian.py" (
    echo Ошибка: space_shooter_russian.py не найден в текущей директории
    echo Убедитесь, что вы запускаете этот скрипт из директории игры
    pause
    exit /b 1
)

:: Install required packages using the specific Python interpreter
echo Установка требований...
"%PYTHON_PATH%" -m pip install pygame
if %errorlevel% neq 0 (
    echo Ошибка: Не удалось установить требования
    echo Убедитесь, что у вас есть подключение к интернету и установлен pip
    pause
    exit /b 1
)

:: Run the game client using the specific Python interpreter
echo Запуск игры Space Shooter...
title Space Shooter Game
"%PYTHON_PATH%" space_shooter_russian.py

if %errorlevel% neq 0 (
    echo.
    echo Произошла ошибка при запуске игры
    echo Проверьте сообщение об ошибке выше
    pause
    exit /b %errorlevel%
)

echo.
echo Игра закрыта. Нажмите любую клавишу для выхода...
pause >nul
exit /b 0