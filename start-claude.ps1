# AgOS 2.0 - Claude Code Launcher
# This script sets up the environment and launches Claude Code CLI

Write-Host "🚀 AgOS 2.0 - Initializing Claude Code..." -ForegroundColor Cyan

# Add Node.js and npm to PATH
$env:PATH = "C:\Users\Dell\nodejs\node-v24.13.0-win-x64;C:\Users\Dell\npm-global;$env:PATH"

# Verify Node.js is available
Write-Host "✓ Node.js version: " -NoNewline -ForegroundColor Green
node --version

# Verify Claude Code is available
Write-Host "✓ Claude Code version: " -NoNewline -ForegroundColor Green
claude --version

Write-Host "`n📋 Mission Briefing:" -ForegroundColor Yellow
Write-Host "You are in the AgOS 2.0 Boardroom. Read CLAUDE.md and AGENTS.md to understand your role as Conductor."
Write-Host "Then read .agent/TEAM_ROSTER.md to identify your specialists.`n" -ForegroundColor Gray

# Launch Claude Code
Write-Host "🎯 Launching Claude Code CLI...`n" -ForegroundColor Magenta
claude
