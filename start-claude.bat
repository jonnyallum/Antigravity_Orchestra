@echo off
REM AgOS 2.0 - Claude Code Launcher (Windows Batch)
echo.
echo ================================
echo  AgOS 2.0 - Claude Code Setup
echo ================================
echo.

set "PATH=C:\Users\Dell\nodejs\node-v24.13.0-win-x64;C:\Users\Dell\npm-global;%PATH%"

cd /d "%~dp0"

echo Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    pause
    exit /b 1
)

echo Checking Claude Code...
claude --version
if %errorlevel% neq 0 (
    echo ERROR: Claude Code not installed!
    pause
    exit /b 1
)

echo.
echo =========================================
echo  Welcome to the AgOS 2.0 Boardroom
echo =========================================
echo.
echo Mission Briefing:
echo Read CLAUDE.md and AGENTS.md for your role.
echo.
echo Starting Claude Code CLI...
echo.

claude

pause
