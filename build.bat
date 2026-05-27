@echo off
REM Build script for InkPen
REM This script builds the InkPen executable using PyInstaller

echo ========================================
echo    InkPen Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Install/upgrade pip
echo [2/4] Installing dependencies...
pip install --upgrade pip setuptools wheel --quiet
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    exit /b 1
)

REM Install PyInstaller and other dependencies
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Build the executable
echo [3/4] Building executable...
pyinstaller build.spec --noconfirm --distpath=dist --buildpath=build --specpath=. >nul 2>&1
if errorlevel 1 (
    echo Error: PyInstaller failed to build executable
    exit /b 1
)

echo Executable built successfully
echo.

REM Create ZIP archive
echo [4/4] Creating ZIP archive...
cd dist
if exist InkPen.zip del InkPen.zip
powershell -Command "Compress-Archive -Path InkPen -DestinationPath InkPen.zip -Force" >nul 2>&1
if errorlevel 1 (
    echo Warning: Failed to create ZIP archive
) else (
    echo ZIP archive created successfully
)
cd ..

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Output location: dist\InkPen\
echo ZIP archive: dist\InkPen.zip
echo.
echo To run: dist\InkPen\InkPen.exe
echo.
pause
