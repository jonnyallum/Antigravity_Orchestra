#!/usr/bin/env python3
"""
Antigravity Orchestra — Health Dashboard Generator
Generates an HTML dashboard visualizing agent health, project status,
and system metrics from the memory layer.

@Owner: @Maya (The Oracle) + @Vigil (The Eye)
@Created: 2026-02-11
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MEMORY = BASE / ".agent" / "memory"
SKILLS = BASE / ".agent" / "skills"
EXECUTION = BASE / "execution"
CLIENTS = BASE / "Clients"
ECOSYSTEMS = BASE / "Ecosystems"
OUTPUT = BASE / "docs" / "dashboard.html"


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def count_agents():
    """Count agent SKILL.md files (excluding non-agent dirs)."""
    excludes = {"methodology", "SKILL_TEMPLATE.md"}
    count = 0
    if SKILLS.exists():
        for item in SKILLS.iterdir():
            if item.is_dir() and item.name not in excludes:
                if (item / "SKILL.md").exists():
                    count += 1
    return count


def count_sops():
    """Count SOP sections across all SKILL.md files."""
    total = 0
    if SKILLS.exists():
        for skill_file in SKILLS.rglob("SKILL.md"):
            try:
                content = skill_file.read_text(encoding="utf-8")
                total += content.lower().count("### sop")
            except Exception:
                pass
    return total


def count_learnings():
    """Count learning log entries across all SKILL.md files."""
    total = 0
    if SKILLS.exists():
        for skill_file in SKILLS.rglob("SKILL.md"):
            try:
                content = skill_file.read_text(encoding="utf-8")
                in_learning = False
                for line in content.split("\n"):
                    if "learning log" in line.lower() or "learning_log" in line.lower():
                        in_learning = True
                    if in_learning and line.strip().startswith("- "):
                        total += 1
            except Exception:
                pass
    return total


def count_scripts():
    """Count active execution scripts (excluding archive)."""
    active = 0
    archived = 0
    if EXECUTION.exists():
        for f in EXECUTION.glob("*.py"):
            active += 1
        archive = EXECUTION / "archive"
        if archive.exists():
            for f in archive.glob("*.py"):
                archived += 1
    return active, archived


def get_agent_health():
    """Load agent health data."""
    return load_json(MEMORY / "agent-health.json")


def get_task_history():
    """Load task history."""
    return load_json(MEMORY / "task-history.json")


def get_clients():
    """List client projects with basic status."""
    clients = []
    if CLIENTS.exists():
        for item in sorted(CLIENTS.iterdir()):
            if item.is_dir() and item.name != "DELETEME_LATER":
                has_readme = (item / "README.md").exists() or any(item.rglob("README.md"))
                clients.append({
                    "name": item.name,
                    "has_readme": has_readme,
                    "path": str(item.relative_to(BASE))
                })
    return clients


def get_ecosystems():
    """List ecosystems."""
    ecos = []
    if ECOSYSTEMS.exists():
        for item in sorted(ECOSYSTEMS.iterdir()):
            if item.is_dir():
                ecos.append(item.name)
    return ecos


def generate_html():
    """Generate the full HTML dashboard."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    agent_count = count_agents()
    sop_count = count_sops()
    learning_count = count_learnings()
    active_scripts, archived_scripts = count_scripts()
    health_data = get_agent_health()
    task_data = get_task_history()
    clients = get_clients()
    ecosystems = get_ecosystems()

    # Extract agent health for table
    agents_list = health_data.get("agents", health_data) if isinstance(health_data, dict) else []
    if isinstance(agents_list, dict):
        # Handle {agent_name: {metrics}} format
        agent_rows = []
        for name, metrics in sorted(agents_list.items()):
            if isinstance(metrics, dict):
                agent_rows.append({
                    "name": name,
                    "tasks": metrics.get("tasks_completed", metrics.get("total_tasks", 0)),
                    "success": metrics.get("success_rate", metrics.get("quality_avg", "N/A")),
                    "last_active": metrics.get("last_active", metrics.get("last_task", "—"))
                })
    else:
        agent_rows = []

    # Task stats
    tasks = task_data.get("tasks", task_data) if isinstance(task_data, dict) else []
    if isinstance(tasks, list):
        total_tasks = len(tasks)
        success_tasks = sum(1 for t in tasks if isinstance(t, dict) and t.get("status") == "success")
    else:
        total_tasks = 0
        success_tasks = 0

    # Health score calculation
    health_score = 9.0  # From latest audit

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity Orchestra — Health Dashboard</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #030308;
    color: #e0e0e0;
    min-height: 100vh;
    padding: 2rem;
  }}
  .header {{
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, #0c1225 0%, #1a0a2e 50%, #0c1225 100%);
    border-radius: 16px;
    border: 1px solid rgba(232, 117, 26, 0.3);
  }}
  .header h1 {{
    font-size: 2.5rem;
    background: linear-gradient(135deg, #e8751a, #f59e0b, #e84393);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }}
  .header .subtitle {{ color: #888; font-size: 1rem; }}
  .header .timestamp {{ color: #666; font-size: 0.85rem; margin-top: 0.5rem; }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
  }}
  .metric-card {{
    background: linear-gradient(135deg, #0f1a3a, #1a0a2e);
    border: 1px solid rgba(232, 117, 26, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .metric-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(232, 117, 26, 0.5);
  }}
  .metric-value {{
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e8751a, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .metric-label {{ color: #999; font-size: 0.85rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; }}

  .health-bar {{
    width: 100%;
    height: 12px;
    background: #1a1a2e;
    border-radius: 6px;
    overflow: hidden;
    margin-top: 1rem;
  }}
  .health-fill {{
    height: 100%;
    border-radius: 6px;
    transition: width 1s ease;
  }}
  .health-green {{ background: linear-gradient(90deg, #10b981, #34d399); }}
  .health-yellow {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
  .health-red {{ background: linear-gradient(90deg, #ef4444, #f87171); }}

  .section {{ margin-bottom: 3rem; }}
  .section h2 {{
    font-size: 1.5rem;
    color: #e8751a;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(232, 117, 26, 0.2);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    background: #0a0a1a;
    border-radius: 12px;
    overflow: hidden;
  }}
  th {{
    background: #0f1a3a;
    color: #e8751a;
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  td {{
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #1a1a2e;
    font-size: 0.9rem;
  }}
  tr:hover td {{ background: rgba(232, 117, 26, 0.05); }}

  .status-live {{ color: #10b981; font-weight: 600; }}
  .status-dev {{ color: #f59e0b; font-weight: 600; }}
  .status-planned {{ color: #6366f1; font-weight: 600; }}

  .eco-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }}
  .eco-card {{
    background: linear-gradient(135deg, #0f1a3a, #0a0a1a);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 1.25rem;
  }}
  .eco-card h3 {{ color: #818cf8; margin-bottom: 0.5rem; }}
  .eco-card p {{ color: #888; font-size: 0.85rem; }}

  .footer {{
    text-align: center;
    color: #444;
    font-size: 0.8rem;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #1a1a2e;
  }}
</style>
</head>
<body>

<div class="header">
  <h1>🛸 Antigravity Orchestra</h1>
  <div class="subtitle">Jai.OS 4.0 — Health Dashboard</div>
  <div class="timestamp">Generated: {now} | Last Audit: 2026-02-11</div>
  <div class="health-bar">
    <div class="health-fill health-green" style="width: {health_score * 10}%"></div>
  </div>
  <div style="color: #10b981; margin-top: 0.5rem; font-weight: 600;">System Health: {health_score}/10</div>
</div>

<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-value">{agent_count}</div>
    <div class="metric-label">Agents</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{sop_count}+</div>
    <div class="metric-label">SOPs</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{learning_count}+</div>
    <div class="metric-label">Learnings</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{active_scripts}</div>
    <div class="metric-label">Active Scripts</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{archived_scripts}</div>
    <div class="metric-label">Archived Scripts</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">10</div>
    <div class="metric-label">MCP Servers</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{len(clients)}</div>
    <div class="metric-label">Client Projects</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{len(ecosystems)}</div>
    <div class="metric-label">Ecosystems</div>
  </div>
</div>

<div class="section">
  <h2>🏢 Client Portfolio</h2>
  <table>
    <thead>
      <tr><th>Client</th><th>Path</th><th>Documentation</th></tr>
    </thead>
    <tbody>
"""

    for c in clients:
        doc_status = '<span class="status-live">✅ Has README</span>' if c["has_readme"] else '<span class="status-dev">⚠️ Missing</span>'
        html += f'      <tr><td>{c["name"]}</td><td><code>{c["path"]}</code></td><td>{doc_status}</td></tr>\n'

    html += """    </tbody>
  </table>
</div>

<div class="section">
  <h2>🌐 Ecosystems</h2>
  <div class="eco-grid">
"""

    eco_descriptions = {
        "Betting": ("🎰", "Sports betting algorithms & statistical edge engineering", "Active"),
        "Trading-Floor": ("📈", "Stock/crypto trading systems & risk management", "Planned"),
        "Media-House": ("🎬", "Content production & YouTube automation", "Planned"),
        "Red-Team-Lab": ("🛡️", "Security research & penetration testing", "Planned"),
    }

    for eco in ecosystems:
        icon, desc, status = eco_descriptions.get(eco, ("📁", "Specialized vertical", "Planned"))
        status_class = "status-live" if status == "Active" else "status-planned"
        html += f"""    <div class="eco-card">
      <h3>{icon} {eco}</h3>
      <p>{desc}</p>
      <p class="{status_class}">{status}</p>
    </div>
"""

    html += f"""  </div>
</div>

"""

    # Agent health table if data exists
    if agent_rows:
        html += """<div class="section">
  <h2>🎻 Agent Health</h2>
  <table>
    <thead>
      <tr><th>Agent</th><th>Tasks</th><th>Success Rate</th><th>Last Active</th></tr>
    </thead>
    <tbody>
"""
        for a in agent_rows[:20]:  # Top 20
            html += f'      <tr><td>@{a["name"]}</td><td>{a["tasks"]}</td><td>{a["success"]}</td><td>{a["last_active"]}</td></tr>\n'
        html += """    </tbody>
  </table>
</div>
"""

    html += f"""
<div class="footer">
  <p>Antigravity Orchestra — Jai.OS 4.0 Health Dashboard</p>
  <p>Generated by <code>execution/generate_health_dashboard.py</code> | {now}</p>
</div>

</body>
</html>"""

    return html


def main():
    html = generate_html()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Dashboard generated: {OUTPUT}")
    print(f"     Open in browser to view.")


if __name__ == "__main__":
    main()
