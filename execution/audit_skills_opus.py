"""
audit_skills_opus.py - Audit all agent SKILL.md files against Opus spec (SKILL_TEMPLATE.md)
Built by @Cline for the Antigravity Orchestra.

Checks for required sections from the Opus template and scores each agent.

Usage:
    python execution/audit_skills_opus.py
"""

import os
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / ".agent" / "skills"

# Required sections from SKILL_TEMPLATE.md (Opus spec)
OPUS_SECTIONS = {
    "The Creed": ["I am part of the Antigravity Orchestra", "I don't work alone", "I don't guess", "I don't ship garbage", "I learn constantly", "I am world-class", "I am connected"],
    "Identity Table": ["Agent Handle", "Human Name", "Nickname", "Role", "Authority Level"],
    "Personality": ["Vibe:", "Communication Style:", "Working Style:"],
    "Capabilities": ["Can Do", "Cannot Do"],
    "SOPs": ["SOP-001:", "SOP-002:"],
    "Collaboration": ["Inner Circle", "Reports To"],
    "Feedback Loop": ["Before Every Task", "After Every Task"],
    "Performance Metrics": ["Metric", "Target"],
    "Restrictions": ["Do NOT", "ALWAYS"],
    "Learning Log": ["Learning", "Source"],
    "Tools & Resources": ["Primary Tools"],
}

# Skip methodology folder
SKIP = {"methodology", "SKILL_TEMPLATE.md"}


def audit_agent(agent_dir: Path) -> dict:
    """Audit a single agent's SKILL.md against Opus spec."""
    skill_file = agent_dir / "SKILL.md"
    if not skill_file.exists():
        return {"name": agent_dir.name, "exists": False, "score": 0, "total": len(OPUS_SECTIONS), "missing": list(OPUS_SECTIONS.keys()), "has_legacy": False, "file_size": 0}
    
    content = skill_file.read_text(encoding='utf-8', errors='replace')
    file_size = len(content)
    
    # Check for legacy format indicator
    has_legacy = "Knowledge Base / Context (Legacy)" in content or "Persona Overview" in content
    
    found = {}
    missing = []
    
    for section_name, markers in OPUS_SECTIONS.items():
        # Check if ANY of the markers exist
        section_found = any(marker in content for marker in markers)
        found[section_name] = section_found
        if not section_found:
            missing.append(section_name)
    
    score = sum(1 for v in found.values() if v)
    
    return {
        "name": agent_dir.name,
        "exists": True,
        "score": score,
        "total": len(OPUS_SECTIONS),
        "missing": missing,
        "has_legacy": has_legacy,
        "file_size": file_size,
        "found": found,
    }


def main():
    print("=" * 70)
    print("OPUS SPEC AUDIT - All Agent SKILL.md Files")
    print("=" * 70)
    
    results = []
    
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.name in SKIP:
            continue
        if item.is_dir():
            result = audit_agent(item)
            results.append(result)
    
    # Sort by score (worst first)
    results.sort(key=lambda r: r["score"])
    
    # Summary
    opus_ready = [r for r in results if r["score"] >= 9]
    needs_work = [r for r in results if 5 <= r["score"] < 9]
    critical = [r for r in results if r["score"] < 5]
    legacy_format = [r for r in results if r.get("has_legacy")]
    
    print(f"\nTotal Agents: {len(results)}")
    print(f"Opus Ready (9+/11): {len(opus_ready)}")
    print(f"Needs Work (5-8/11): {len(needs_work)}")
    print(f"Critical (<5/11): {len(critical)}")
    print(f"Legacy Format: {len(legacy_format)}")
    
    # Detailed results
    print(f"\n{'='*70}")
    print(f"{'Agent':<15} {'Score':>5} {'Size':>6} {'Legacy':>7} {'Missing Sections'}")
    print(f"{'-'*15} {'-'*5} {'-'*6} {'-'*7} {'-'*30}")
    
    for r in results:
        if not r["exists"]:
            print(f"{r['name']:<15} {'N/A':>5} {'0':>6} {'N/A':>7} FILE MISSING")
            continue
        
        pct = f"{r['score']}/{r['total']}"
        size = f"{r['file_size']//1024}K" if r['file_size'] >= 1024 else f"{r['file_size']}B"
        legacy = "YES" if r["has_legacy"] else "no"
        missing = ", ".join(r["missing"][:4])
        if len(r["missing"]) > 4:
            missing += f" +{len(r['missing'])-4} more"
        
        # Grade
        if r["score"] >= 9:
            grade = "A"
        elif r["score"] >= 7:
            grade = "B"
        elif r["score"] >= 5:
            grade = "C"
        else:
            grade = "F"
        
        print(f"{r['name']:<15} {pct:>5} {size:>6} {legacy:>7} [{grade}] {missing}")
    
    # Save report
    report_path = ROOT / ".tmp" / "OPUS_AUDIT_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Opus Spec Audit Report\n")
        f.write(f"**Date:** 2026-02-07\n")
        f.write(f"**Total Agents:** {len(results)}\n\n")
        
        f.write("## Summary\n")
        f.write(f"| Grade | Count | Agents |\n")
        f.write(f"|:------|:------|:-------|\n")
        f.write(f"| **A** (Opus Ready) | {len(opus_ready)} | {', '.join(r['name'] for r in opus_ready)} |\n")
        f.write(f"| **B-C** (Needs Work) | {len(needs_work)} | {', '.join(r['name'] for r in needs_work)} |\n")
        f.write(f"| **F** (Critical) | {len(critical)} | {', '.join(r['name'] for r in critical)} |\n")
        f.write(f"| Legacy Format | {len(legacy_format)} | {', '.join(r['name'] for r in legacy_format)} |\n\n")
        
        f.write("## Detailed Scores\n\n")
        f.write(f"| Agent | Score | Grade | Legacy | Missing |\n")
        f.write(f"|:------|:------|:------|:-------|:--------|\n")
        for r in results:
            if not r["exists"]:
                f.write(f"| {r['name']} | N/A | N/A | N/A | FILE MISSING |\n")
                continue
            grade = "A" if r["score"] >= 9 else "B" if r["score"] >= 7 else "C" if r["score"] >= 5 else "F"
            legacy = "YES" if r["has_legacy"] else "no"
            missing = ", ".join(r["missing"])
            f.write(f"| {r['name']} | {r['score']}/{r['total']} | {grade} | {legacy} | {missing} |\n")
        
        f.write("\n## Opus Spec Sections Checked\n\n")
        for section, markers in OPUS_SECTIONS.items():
            f.write(f"- **{section}**: Looks for: `{markers[0]}`...\n")
    
    print(f"\nReport saved to: .tmp/OPUS_AUDIT_REPORT.md")


if __name__ == "__main__":
    main()
