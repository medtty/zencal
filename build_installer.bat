@echo off
echo ========================================
echo ZenCal Installer Builder
echo ========================================
echo.

REM Step 1: Build the executable
echo [1/2] Building executable...
python build_windows.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to build executable!
    pause
    exit /b 1
)
echo.

REM Step 2: Create installer
echo [2/2] Creating installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_windows.iss
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create installer!
    echo Make sure Inno Setup is installed.
    pause
    exit /b 1
)
echo.

echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your installer is ready:
echo   installer_output\ZenCal-Setup-1.0.0.exe
echo.
echo You can now distribute this file!
echo.
pause
