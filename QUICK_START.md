# 🚀 AgOS 2.0 Quick Start Guide

## ✅ Installation Complete!

### What's Installed

- **Node.js v24.13.0 LTS** - Extracted to `C:\Users\Dell\nodejs\node-v24.13.0-win-x64`
- **Claude Code CLI v2.1.29** - Installed globally via npm
- **AgOS 2.0 Template** - Complete ecosystem at `C:\Users\Dell\Desktop\AgOS-Template`

### How to Use Claude Code

#### Option 1: Use the Launcher Script (Easiest)
```powershell
# From the template directory
cd C:\Users\Dell\Desktop\AgOS-Template
.\start-claude.ps1
```

#### Option 2: Direct Command (After reopening terminal)
```powershell
# Open a new PowerShell window (to load updated PATH)
cd C:\Users\Dell\Desktop\AgOS-Template
claude
```

### First-Time Setup

When you run Claude Code for the first time, you'll need to:

1. **Authenticate** with your Anthropic API key (already in `.env` file)
2. **Give the Mission Briefing**:
   ```
   I am Jonny. This is the AgOS 2.0 Boardroom. Read CLAUDE.md and AGENTS.md to 
   understand your role as Conductor. Then read .agent/TEAM_ROSTER.md to 
   identify your specialists.
   ```

### Key Files in Your Template

- **CLAUDE.md** - Your role as Conductor
- **AGENTS.md** - Overview of the 24 specialist agents
- **.agent/TEAM_ROSTER.md** - Detailed roster of specialists
- **.env** - All your API keys (Gemini, GitHub, Brave, Linear, Stripe, Supabase)
- **execution/** - Python scripts for validation and automation

### Verification Scripts

Run these to check ecosystem health:

```powershell
# Validate all 24 specialists
python execution/validate_agents.py

# Check system health
python execution/feedback_engine.py report
```

### Environment Variables Configured

✓ GitHub Personal Access Token
✓ Gemini API Key
✓ Brave Search API Key
✓ Linear API Key
✓ Stripe Secret Key (Live)
✓ Supabase URL

---

**Need Help?**
- Read the documentation in `docs/`
- Check workflows in `.agent/workflows/`
- Review skills in `.agent/skills/`
