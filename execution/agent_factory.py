e#!/usr/bin/env python3
"""
Antigravity Orchestra - Dynamic Agent Factory
Creates new agents on-the-fly from a skill library and templates.

The Conductor can dynamically assemble new, temporary or permanent agents
by combining skill modules from the library to tackle novel problems.

Usage:
  python execution/agent_factory.py create --name "Agent Name" --handle "handle" --nickname "The Title" --role "Role Description" --skills "skill1,skill2,skill3"
  python execution/agent_factory.py list-skills
  python execution/agent_factory.py list-agents
  python execution/agent_factory.py preview --name "Agent Name" --handle "handle" --role "Role" --skills "skill1,skill2"

@Owner: @Marcus (The Maestro) + @Coordinator-L (The Catalyst)
@Created: 2026-02-11
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS_DIR = BASE / ".agent" / "skills"
TEMPLATE_PATH = SKILLS_DIR / "SKILL_TEMPLATE.md"
HEALTH_PATH = BASE / ".agent" / "memory" / "agent-health.json"

# ============================================================
# SKILL LIBRARY - Composable skill modules
# Each module is a block of SOP text that can be mixed & matched
# ============================================================
SKILL_LIBRARY = {
    # --- Engineering Skills ---
    "frontend": {
        "category": "Engineering",
        "description": "Frontend development (React, Next.js, TypeScript, Tailwind)",
        "sops": [
            ("Component Architecture", "Design reusable, type-safe React components with proper prop interfaces, error boundaries, and loading states. Follow atomic design principles."),
            ("Responsive Implementation", "Implement mobile-first responsive layouts using Tailwind CSS v4 breakpoints. Test across 5 viewport sizes (320px, 768px, 1024px, 1440px, 1920px)."),
            ("Performance Optimization", "Achieve Lighthouse score >90. Use dynamic imports, image optimization (WebP/AVIF), and proper caching headers."),
        ]
    },
    "backend": {
        "category": "Engineering",
        "description": "Backend development (APIs, databases, server logic)",
        "sops": [
            ("API Design", "Design RESTful or tRPC endpoints with proper error handling, input validation, and rate limiting. Document all endpoints."),
            ("Database Operations", "Write efficient SQL queries. Use parameterized queries to prevent injection. Implement proper indexing and connection pooling."),
            ("Authentication & Authorization", "Implement secure auth flows (OAuth, JWT). Enforce RLS policies. Never expose secrets in client code."),
        ]
    },
    "devops": {
        "category": "Engineering",
        "description": "Deployment, CI/CD, infrastructure management",
        "sops": [
            ("Deployment Pipeline", "Configure GitHub Actions workflows for automated build, test, and deploy. Use environment-specific secrets."),
            ("Server Management", "Manage Hostinger/Vercel deployments. SSH access, file permissions, domain configuration."),
            ("Monitoring & Rollback", "Set up health checks and error monitoring. Maintain rollback procedures for every deployment."),
        ]
    },
    "mobile": {
        "category": "Engineering",
        "description": "Mobile-first development and optimization",
        "sops": [
            ("Touch UX Design", "All interactive elements minimum 48px touch targets. Map thumb zones for one-handed use."),
            ("Core Web Vitals", "LCP < 2.5s, FID < 100ms, CLS < 0.1. Test on real devices across network conditions."),
            ("PWA Implementation", "Service workers, offline-first patterns, install prompts, push notifications."),
        ]
    },
    # --- Creative Skills ---
    "ui_design": {
        "category": "Creative",
        "description": "UI/UX design, visual polish, brand compliance",
        "sops": [
            ("Visual Design System", "Maintain consistent spacing, typography, and color usage per brand guide. Use design tokens."),
            ("Animation & Motion", "Implement Framer Motion animations with purpose. Respect prefers-reduced-motion. Keep animations under 300ms."),
            ("Accessibility", "WCAG 2.1 AA compliance. Proper contrast ratios, ARIA labels, keyboard navigation, screen reader testing."),
        ]
    },
    "copywriting": {
        "category": "Creative",
        "description": "Brand voice, sales copy, UI microcopy",
        "sops": [
            ("Brand Voice", "Write in the client's established tone. Reference brand guide for vocabulary, formality level, and personality."),
            ("Conversion Copy", "CTAs must be action-oriented and specific. Headlines follow AIDA framework. Test variations."),
            ("Microcopy", "Error messages are helpful, not technical. Loading states are informative. Empty states guide next action."),
        ]
    },
    "video_content": {
        "category": "Creative",
        "description": "Video editing, short-form content, retention hooks",
        "sops": [
            ("Hook Engineering", "First 3 seconds must arrest attention. Use pattern interrupts, bold claims, or visual surprises."),
            ("Platform Optimization", "Format for each platform (9:16 TikTok/Reels, 16:9 YouTube, 1:1 Feed). Respect safe zones."),
            ("Retention Analysis", "Track audience retention curves. Identify drop-off points. A/B test hooks and pacing."),
        ]
    },
    # --- Intelligence Skills ---
    "research": {
        "category": "Intelligence",
        "description": "Deep web research, competitor analysis, data gathering",
        "sops": [
            ("Deep Research", "Use Brave Search + Playwright for comprehensive research. Cross-reference 3+ sources. Document methodology."),
            ("Competitor Analysis", "Map competitor features, pricing, positioning. Identify gaps and opportunities. Update quarterly."),
            ("Data Verification", "All claims must be sourced. No hallucinated statistics. Flag uncertainty explicitly."),
        ]
    },
    "seo": {
        "category": "Intelligence",
        "description": "Search engine optimization, meta tags, schema markup",
        "sops": [
            ("Technical SEO", "Proper heading hierarchy (single H1), meta descriptions, canonical URLs, sitemap.xml, robots.txt."),
            ("Schema Markup", "Implement schema.org structured data (Organization, LocalBusiness, Product, FAQ). Validate with Google's tool."),
            ("Content Strategy", "Target long-tail keywords. Internal linking strategy. Content freshness signals."),
        ]
    },
    "analytics": {
        "category": "Intelligence",
        "description": "Performance tracking, conversion data, ROI attribution",
        "sops": [
            ("Metrics Framework", "Define KPIs per project. Track conversion funnels, bounce rates, session duration."),
            ("ROI Attribution", "Multi-touch attribution modeling. Track cost per acquisition across channels."),
            ("Reporting", "Weekly automated reports. Highlight anomalies and trends. Actionable recommendations."),
        ]
    },
    # --- Security Skills ---
    "security_audit": {
        "category": "Security",
        "description": "Security auditing, vulnerability scanning, penetration testing",
        "sops": [
            ("Security Scan", "Run OWASP Top 10 checks. Verify no exposed secrets, SQL injection, XSS, CSRF vulnerabilities."),
            ("RLS Verification", "Verify Row Level Security policies on all Supabase tables. Test with different user roles."),
            ("Incident Response", "Document and triage security incidents. Immediate containment, root cause analysis, prevention."),
        ]
    },
    "secrets_management": {
        "category": "Security",
        "description": "API keys, encryption, certificate management",
        "sops": [
            ("Key Rotation", "Rotate API keys monthly. Use environment variables, never hardcode. Audit .env files."),
            ("Encryption", "TLS everywhere. Encrypt sensitive data at rest. Use proper hashing for passwords (bcrypt/argon2)."),
            ("Access Control", "Principle of least privilege. Audit access logs. Revoke unused credentials immediately."),
        ]
    },
    # --- Business Skills ---
    "monetization": {
        "category": "Business",
        "description": "Pricing strategy, funnel design, market testing",
        "sops": [
            ("Pricing Strategy", "Research competitor pricing. Design tiered pricing (Free/Pro/Enterprise). A/B test price points."),
            ("Funnel Design", "Map customer journey from awareness to purchase. Optimize each stage for conversion."),
            ("Revenue Tracking", "Track MRR, churn rate, LTV, CAC. Set up Stripe webhooks for real-time revenue data."),
        ]
    },
    "compliance": {
        "category": "Business",
        "description": "GDPR, legal compliance, privacy, terms of service",
        "sops": [
            ("GDPR Compliance", "Cookie consent banners, data processing agreements, right to deletion, privacy policy."),
            ("Terms of Service", "Draft and maintain ToS. Cover liability, IP, user conduct, termination clauses."),
            ("Data Protection", "Data minimization, purpose limitation, storage limitation. Document data flows."),
        ]
    },
    # --- Domain Skills ---
    "betting": {
        "category": "Domain",
        "description": "Sports betting analysis, statistical edge engineering",
        "sops": [
            ("Statistical Analysis", "Use historical data for probability modeling. Calculate expected value. Track ROI by market type."),
            ("Algorithm Design", "Deterministic analysis only - no random selections. Every pick must have explicit reasoning and conviction score."),
            ("Risk Management", "Kelly criterion for stake sizing. Maximum exposure limits. Bankroll management protocols."),
        ]
    },
    "trading": {
        "category": "Domain",
        "description": "Financial trading systems, risk management, backtesting",
        "sops": [
            ("Signal Generation", "Technical + fundamental analysis. Backtest all strategies against historical data before live deployment."),
            ("Risk Controls", "Position sizing, stop-loss automation, maximum drawdown limits, circuit breakers."),
            ("Market Analysis", "Track whale movements, order flow, sentiment indicators. Cross-reference multiple data sources."),
        ]
    },
    "ecommerce": {
        "category": "Domain",
        "description": "Dropshipping, marketplace, product management",
        "sops": [
            ("Product Sourcing", "Vet suppliers (minimum 3 quotes). Verify quality, shipping times, return policies."),
            ("Inventory Management", "Track stock levels, reorder points, lead times. Automate low-stock alerts."),
            ("Margin Optimization", "Calculate true margins (including shipping, returns, fees). Target minimum 30% net margin."),
        ]
    },
}


def list_skills():
    """Display all available skill modules."""
    print("\n=== ANTIGRAVITY SKILL LIBRARY ===\n")
    categories = {}
    for key, skill in SKILL_LIBRARY.items():
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, skill))

    for cat, skills in sorted(categories.items()):
        print(f"  [{cat}]")
        for key, skill in skills:
            sop_count = len(skill["sops"])
            print(f"    {key:20s} - {skill['description']} ({sop_count} SOPs)")
        print()

    print(f"  Total: {len(SKILL_LIBRARY)} skill modules available")
    print(f"  Total SOPs: {sum(len(s['sops']) for s in SKILL_LIBRARY.values())}")


def list_agents():
    """List all existing agents."""
    print("\n=== EXISTING AGENTS ===\n")
    excludes = {"methodology", "SKILL_TEMPLATE.md"}
    count = 0
    if SKILLS_DIR.exists():
        for item in sorted(SKILLS_DIR.iterdir()):
            if item.is_dir() and item.name not in excludes:
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    # Extract first line for name
                    try:
                        first_lines = skill_file.read_text(encoding="utf-8").split("\n")[:5]
                        name = next((l for l in first_lines if l.startswith("# ")), f"# @{item.name}")
                        print(f"  @{item.name:20s} {name.replace('# ', '')}")
                    except Exception:
                        print(f"  @{item.name:20s} (could not read)")
                    count += 1
    print(f"\n  Total: {count} agents")


def generate_skill_md(name, handle, nickname, role, skill_keys, permanent=True):
    """Generate a SKILL.md from selected skill modules."""
    now = datetime.now().strftime("%Y-%m-%d")
    agent_type = "Permanent" if permanent else "Temporary (auto-generated)"

    # Collect selected skills
    selected = []
    for key in skill_keys:
        if key in SKILL_LIBRARY:
            selected.append((key, SKILL_LIBRARY[key]))
        else:
            print(f"  [WARN] Unknown skill: {key} (skipped)")

    if not selected:
        print("[ERROR] No valid skills selected. Aborting.")
        return None

    # Build the SKILL.md content
    md = f"""# @{handle} — {name} "{nickname}"

> **Role:** {role}
> **Type:** {agent_type}
> **Created:** {now} by Agent Factory
> **Skills:** {', '.join(k for k, _ in selected)}

---

## The Creed

```
I don't work alone.
I don't guess.
I don't ship garbage.
I learn constantly.
I am world-class.
I am connected.
```

---

## Identity

| Field | Value |
|:------|:------|
| **Handle** | @{handle} |
| **Human Name** | {name} |
| **Nickname** | "{nickname}" |
| **Role** | {role} |
| **Authority** | L2 (Operational) |
| **Created** | {now} |

---

## Core Capabilities

| Domain | Skills |
|:-------|:-------|
"""

    for key, skill in selected:
        md += f"| **{skill['category']}** | {skill['description']} |\n"

    md += "\n---\n\n## Standard Operating Procedures\n\n"

    sop_num = 1
    for key, skill in selected:
        md += f"### [{skill['category']}] {key.replace('_', ' ').title()}\n\n"
        for sop_name, sop_desc in skill["sops"]:
            md += f"#### SOP {sop_num}: {sop_name}\n{sop_desc}\n\n"
            sop_num += 1

    md += """---

## Collaboration Protocol

**Before Every Task:**
1. Check `.tmp/message4[ai].md` for pending handoffs
2. Read `chatroom.md` for recent context
3. Verify no sync locks on target files

**After Every Task:**
1. Log outcome to task history
2. Update learning log below
3. Notify @Marcus of completion

---

## Quality Gates

- [ ] Code compiles / no syntax errors
- [ ] Truth-Lock verified (no false claims)
- [ ] Mobile responsive (if UI)
- [ ] Security scan passed (if backend)
- [ ] Brand compliance (if client-facing)

---

## Learning Log

*Auto-generated agent. Learning log starts empty.*

- (No entries yet — will populate as agent completes tasks)

---

"""
    md += f"*Generated by Agent Factory | {now} | Jai.OS 4.0*\n"

    return md


def create_agent(name, handle, nickname, role, skill_keys, permanent=True):
    """Create a new agent with the given skills."""
    handle_lower = handle.lower().replace(" ", "-")
    agent_dir = SKILLS_DIR / handle_lower

    if agent_dir.exists():
        print(f"[ERROR] Agent @{handle_lower} already exists at {agent_dir}")
        return False

    # Generate SKILL.md
    md = generate_skill_md(name, handle_lower, nickname, role, skill_keys, permanent)
    if md is None:
        return False

    # Create directory and write file
    agent_dir.mkdir(parents=True, exist_ok=True)
    skill_path = agent_dir / "SKILL.md"
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(md)

    # Update agent-health.json
    try:
        health = {}
        if HEALTH_PATH.exists():
            with open(HEALTH_PATH, "r", encoding="utf-8") as f:
                health = json.load(f)

        if "agents" not in health:
            health["agents"] = health if isinstance(health, dict) and "agents" not in health else health.get("agents", {})

        agents = health if not isinstance(health.get("agents"), dict) else health["agents"]
        agents[handle_lower] = {
            "tasks_completed": 0,
            "success_rate": "N/A",
            "last_active": "never",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "skills": skill_keys,
            "type": "permanent" if permanent else "temporary"
        }

        with open(HEALTH_PATH, "w", encoding="utf-8") as f:
            json.dump(health, f, indent=2)
    except Exception as e:
        print(f"  [WARN] Could not update agent-health.json: {e}")

    print(f"\n[OK] Agent created successfully!")
    print(f"     Handle:   @{handle_lower}")
    print(f"     Name:     {name} \"{nickname}\"")
    print(f"     Role:     {role}")
    print(f"     Skills:   {', '.join(skill_keys)}")
    print(f"     SOPs:     {sum(len(SKILL_LIBRARY[k]['sops']) for k in skill_keys if k in SKILL_LIBRARY)}")
    print(f"     Location: {skill_path}")
    print(f"     Type:     {'Permanent' if permanent else 'Temporary'}")
    return True


def preview_agent(name, handle, nickname, role, skill_keys):
    """Preview what an agent would look like without creating it."""
    md = generate_skill_md(name, handle, nickname, role, skill_keys)
    if md:
        print("\n=== AGENT PREVIEW ===\n")
        print(md)
        print("=== END PREVIEW ===")
        print(f"\nTo create this agent, add --confirm to the command.")


def main():
    parser = argparse.ArgumentParser(description="Antigravity Agent Factory")
    subparsers = parser.add_subparsers(dest="command")

    # list-skills
    subparsers.add_parser("list-skills", help="List all available skill modules")

    # list-agents
    subparsers.add_parser("list-agents", help="List all existing agents")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new agent")
    create_parser.add_argument("--name", required=True, help="Human name (e.g., 'Alex Torres')")
    create_parser.add_argument("--handle", required=True, help="Agent handle (e.g., 'alex')")
    create_parser.add_argument("--nickname", required=True, help="Nickname (e.g., 'The Machine')")
    create_parser.add_argument("--role", required=True, help="Role description")
    create_parser.add_argument("--skills", required=True, help="Comma-separated skill keys")
    create_parser.add_argument("--temporary", action="store_true", help="Mark as temporary agent")

    # preview
    preview_parser = subparsers.add_parser("preview", help="Preview agent without creating")
    preview_parser.add_argument("--name", required=True)
    preview_parser.add_argument("--handle", required=True)
    preview_parser.add_argument("--nickname", default="The Specialist")
    preview_parser.add_argument("--role", required=True)
    preview_parser.add_argument("--skills", required=True)

    args = parser.parse_args()

    if args.command == "list-skills":
        list_skills()
    elif args.command == "list-agents":
        list_agents()
    elif args.command == "create":
        skill_keys = [s.strip() for s in args.skills.split(",")]
        create_agent(args.name, args.handle, args.nickname, args.role, skill_keys, not args.temporary)
    elif args.command == "preview":
        skill_keys = [s.strip() for s in args.skills.split(",")]
        preview_agent(args.name, args.handle, args.nickname, args.role, skill_keys)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
