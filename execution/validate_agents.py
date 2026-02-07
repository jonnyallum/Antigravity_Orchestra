"""
Agent Structure Validator - Ensures all SKILL.md files meet the Jai.OS 4.0 standard.
Part of the AgOS Auto-Sync System.

Usage:
    python validate_agents.py [--fix] [--verbose]
"""

import os
import sys
import re
from pathlib import Path

# Required sections in Jai.OS 4.0 SKILL.md format
REQUIRED_SECTIONS_V2 = [
    "Profile Card",
    "Personality & Collaboration Style",
    "Core Competencies",
    "Key Workflows",
    "Team Interaction",
    "Performance Metrics",
    "Restrictions",
    "Training Day Skills",
    "Learning Log"
]

# Required sections in Jai.OS 4.0 SKILL.md format
REQUIRED_SECTIONS_V3 = [
    "Persona Overview",
    "Core Capabilities",
    "Standard Operating Procedures (SOPs)",
    "Personal Development Plan"
]

# Required sections in Jai.OS 4.0 SKILL.md format
REQUIRED_SECTIONS_V4 = [
    "The Creed",
    "Identity",
    "Personality",
    "Capabilities",
    "Standard Operating Procedures",
    "Collaboration",
    "Learning Log"
]

# Required profile elements for V2
REQUIRED_PROFILE_ELEMENTS_V2 = [
    "Human Name",
    "Nickname",
    "Role",
    "Reports To",
    "Personality",
    "Philosophy"
]

SKILLS_DIR = Path(__file__).parent.parent / ".agent" / "skills"


def validate_skill_file(filepath: Path, verbose: bool = False) -> dict:
    """
    Validate a SKILL.md file against the Jai.OS 4.0 standard.

    Args:
        filepath: Path to the SKILL.md file
        verbose: Whether to print detailed output

    Returns:
        Dict with validation results
    """
    result = {
        "file": str(filepath),
        "valid": True,
        "issues": [],
        "warnings": []
    }

    if not filepath.exists():
        result["valid"] = False
        result["issues"].append(f"File not found: {filepath}")
        return result

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        result["valid"] = False
        result["issues"].append(f"Could not read file: {e}")
        return result

    # Detect Version
    frontmatter = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    version = "2.0" # Default
    
    if frontmatter:
        fm_content = frontmatter.group(1)
        if 'version: "4.0"' in fm_content or "version: 4.0" in fm_content:
            version = "4.0"
        elif 'version: "3.0"' in fm_content or "version: 3.0" in fm_content:
            version = "3.0"

    # Secondary detection if no frontmatter version
    if version == "2.0":
        if "The Creed" in content and "Identity" in content:
            version = "4.0"
        elif "Persona Overview" in content or "Core Capabilities" in content:
            version = "3.0"

    if version == "4.0":
        required_sections = REQUIRED_SECTIONS_V4
    elif version == "3.0":
        required_sections = REQUIRED_SECTIONS_V3
    else:
        required_sections = REQUIRED_SECTIONS_V2

    # Check for Alias line (Jai.OS 4.0 only)
    if version == "2.0" and '**Alias:**' not in content and 'Alias:' not in content:
        result["warnings"].append("Missing Alias line (Jai.OS 4.0 format)")

    # Check for required sections with flexible regex
    # Allows for emojis, numbers, and common variations
    PREFIX = r"##\s+(?:[\d\.\s\w\W]*?)\s*"
    SECTION_RE = {
        "The Creed": PREFIX + r"Creed",
        "Identity": PREFIX + r"(Identity|Persona Overview|Profile Card)",
        "Personality": PREFIX + r"(Personality|Persona Overview)",
        "Capabilities": PREFIX + r"((Core )?Capabilities|Core Competencies)",
        "Standard Operating Procedures": PREFIX + r"(Standard Operating Procedures|SOPs)",
        "Collaboration": PREFIX + r"(Collaboration|Team Interaction|Team Persona)",
        "Learning Log": PREFIX + r"(Learning Log|Feedback Loop)",
        "Persona Overview": PREFIX + r"(Persona Overview|Identity|Profile Card)",
        "Core Capabilities": PREFIX + r"((Core )?Capabilities|Core Competencies)",
        "Standard Operating Procedures (SOPs)": PREFIX + r"(Standard Operating Procedures|SOPs)",
        "Personal Development Plan": PREFIX + r"(Personal Development Plan|Training Day Skills)",
        "Profile Card": PREFIX + r"(Profile Card|Identity)",
        "Personality & Collaboration Style": PREFIX + r"(Personality|Collaboration Style)",
        "Core Competencies": PREFIX + r"((Core )?Capabilities|Core Competencies)",
        "Key Workflows": PREFIX + r"(Key Workflows|SOPs)",
        "Team Interaction": PREFIX + r"(Team Interaction|Collaboration)",
        "Performance Metrics": PREFIX + r"(Performance Metrics|Stats)",
        "Restrictions": PREFIX + r"(Restrictions|Cannot Do)",
        "Training Day Skills": PREFIX + r"(Training Day Skills|Personal Development Plan)"
    }

    for section in required_sections:
        pattern = SECTION_RE.get(section, f"## {section}")
        if not re.search(pattern, content, re.IGNORECASE):
            result["issues"].append(f"Missing section: {section} (AgOS {version} format)")
            result["valid"] = False

    if version == "2.0":
        # Check for profile elements in Profile Card
        profile_section = re.search(r'(Profile Card|Identity).*?(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if profile_section:
            profile_content = profile_section.group(0)
            for element in REQUIRED_PROFILE_ELEMENTS_V2:
                if element not in profile_content:
                    result["warnings"].append(f"Profile Card missing: {element}")
        else:
            result["warnings"].append("Profile Card section not found or malformed")

        # Check for Performance Metrics table
        if "| Metric |" not in content and "| Target |" not in content and "| Attribute |" not in content:
            result["warnings"].append("Performance Metrics may not have proper table format")

        # Check for Learning Log table
        if "| Date |" not in content or ("| Learning |" not in content and "| Learning Log |" not in content):
            result["warnings"].append("Learning Log may not have proper table format")
    elif version == "3.0":
        # V3 specific checks
        if "| Job |" not in content and "| Task |" not in content and "| Metric |" not in content:
             result["warnings"].append("Personal Development Plan may be missing job/task table")
    elif version == "4.0":
        # V4 specific checks (Jai.OS 4.0)
        has_identity_table = "| Attribute |" in content and "| Value |" in content
        if not has_identity_table:
            result["warnings"].append("Identity section missing Attribute/Value table")
        
        has_learning_table = "| Date |" in content and ("| Learning |" in content or "| Learning Log |" in content)
        if not has_learning_table:
            result["warnings"].append("Learning Log missing Date/Learning table")

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"File: {filepath}")
        print(f"Valid: {result['valid']}")
        if result['issues']:
            print("Issues:")
            for issue in result['issues']:
                print(f"  - {issue}")
        if result['warnings']:
            print("Warnings:")
            for warning in result['warnings']:
                print(f"  - {warning}")

    return result


def validate_all_agents(verbose: bool = False) -> dict:
    """
    Validate all agent SKILL.md files.

    Args:
        verbose: Whether to print detailed output

    Returns:
        Dict with validation results for all agents
    """
    results = {
        "valid": [],
        "invalid": [],
        "warnings": [],
        "total": 0
    }

    if not SKILLS_DIR.exists():
        print(f"Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)

    # Get all agent directories (exclude methodology)
    for agent_dir in sorted(SKILLS_DIR.iterdir()):
        if agent_dir.is_dir() and agent_dir.name != "methodology":
            skill_file = agent_dir / "SKILL.md"
            result = validate_skill_file(skill_file, verbose)
            results["total"] += 1

            if result["valid"]:
                results["valid"].append(agent_dir.name)
            else:
                results["invalid"].append({
                    "agent": agent_dir.name,
                    "issues": result["issues"]
                })

            if result["warnings"]:
                results["warnings"].append({
                    "agent": agent_dir.name,
                    "warnings": result["warnings"]
                })

    return results


def print_summary(results: dict):
    """Print a summary of validation results."""
    print("\n" + "=" * 60)
    print("AGENT VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total agents: {results['total']}")
    print(f"Valid: {len(results['valid'])}")
    print(f"Invalid: {len(results['invalid'])}")
    print(f"With warnings: {len(results['warnings'])}")

    if results['invalid']:
        print("\n--- INVALID AGENTS ---")
        for agent_result in results['invalid']:
            print(f"\n{agent_result['agent']}:")
            for issue in agent_result['issues']:
                print(f"  [ERROR] {issue}")

    if results['warnings']:
        print("\n--- WARNINGS ---")
        for agent_result in results['warnings']:
            print(f"\n{agent_result['agent']}:")
            for warning in agent_result['warnings']:
                print(f"  [WARN] {warning}")

    if not results['invalid']:
        print("\n" + "=" * 60)
        print("ALL AGENTS PASS VALIDATION")
        print("=" * 60)


def main():
    """CLI entry point."""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("Jai.OS 4.0 Agent Validator")
    print(f"Scanning: {SKILLS_DIR}")

    results = validate_all_agents(verbose)
    print_summary(results)

    # Exit with error code if any invalid
    if results['invalid']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
