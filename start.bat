@echo off
chcp 65001 >nul
title RedXTools Starter
setlocal EnableDelayedExpansion

reg add "HKCU\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "BLUE=%ESC%[94m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "DIM=%ESC%[2m"
set "BOLD=%ESC%[1m"
set "RESET=%ESC%[0m"

cls
echo.
echo %CYAN%  ╔══════════════════════════════════════════════════╗%RESET%
echo %CYAN%  ║%RESET%              %BOLD%%WHITE%  R e d X T o o l s  %RESET%%CYAN%               ║%RESET%
echo %CYAN%  ║%RESET%  %DIM%          Automated Toolkit Launcher            %RESET%%CYAN%║%RESET%
echo %CYAN%  ╚══════════════════════════════════════════════════╝%RESET%
echo.

echo  %DIM%Checking environment...%RESET%
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo  %RED%[-]%RESET% Python is not installed on this system.
    echo.
    set /p "INSTALL=  %YELLOW%→%RESET% Download and install Python 3.11 silently? [Y/n]: "
    if /i "!INSTALL!"=="Y" (
        echo.
        echo  %YELLOW%[↓]%RESET% Downloading Python 3.11.8 ...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile '%TEMP%\python_installer.exe' -UseBasicParsing" >nul 2>&1
        if exist "%TEMP%\python_installer.exe" (
            echo  %YELLOW%[/]%RESET% Installing Python silently...
            "%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
            del "%TEMP%\python_installer.exe" >nul 2>&1
            echo  %GREEN%[+]%RESET% Python installed successfully.
            echo.
            echo  %YELLOW%  Please restart this script to continue.%RESET%
            echo.
            pause
            exit /b 0
        ) else (
            echo  %RED%[-]%RESET% Download failed. Check your internet connection.
            echo.
            echo  %DIM%  Manual download: https://www.python.org/downloads/%RESET%
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo  %DIM%  Manual download: https://www.python.org/downloads/%RESET%
        echo.
        pause
        exit /b 1
    )
)

for /f "delims=" %%i in ('python --version 2^>^&1') do set "PYVER=%%i"
echo  %GREEN%[+]%RESET% %BLUE%%PYVER%%RESET% detected

echo.
echo  %YELLOW%[/]%RESET% Upgrading pip...
python -m pip install --upgrade pip -q 2>nul
if %errorlevel% neq 0 (
    echo  %RED%[-]%RESET% Failed to upgrade pip.
    echo.
    pause
    exit /b 1
)

echo  %YELLOW%[/]%RESET% Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt -q 2>nul
if %errorlevel% neq 0 (
    echo  %RED%[-]%RESET% Dependency installation failed.
    echo  %DIM%      Run manually: pip install -r requirements.txt%RESET%
    echo.
    pause
    exit /b 1
)

echo  %GREEN%[+]%RESET% All dependencies installed successfully.

echo.
echo  %DIM%  ─────────────────────────────────────────────────%RESET%
echo.
echo  %CYAN%[→]%RESET% Launching %BOLD%RedXTools%RESET%...
echo.

python main.py

echo.
echo  %DIM%  ─────────────────────────────────────────────────%RESET%
echo.
echo  %DIM%  Session ended. Press any key to close.%RESET%
echo.
pause >nul