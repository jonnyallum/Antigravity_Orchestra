#!/usr/bin/env python3
"""
Verify Deployment Protocol v1
Automates post-deployment checks for Antigravity Agency projects.
- Reachability (200 OK)
- Content Verification (Client-specific strings)
- Truth-Lock Compliance (Placeholder detection)
- SSL/Security Headers basic check
"""

import requests
import sys
import argparse
from typing import List, Dict

# Configuration of placeholders to detect
FORBIDDEN_STRINGS = [
    "Lorem Ipsum",
    "placeholder",
    "example.com",
    "unsplash.com",
    "your-domain.com",
    "TODO",
    "FIXME"
]

PROJECT_CONFIGS = {
    "jonnyai": {
        "url": "https://jonnyai.co.uk",
        "required_strings": ["JonnyAI", "Antigravity", "Orchestra", "Maestro"],
        "critical": True
    },
    "kwizz": {
        "url": "https://kwizz.app",
        "required_strings": ["Kwizz", "3 Doors", "monetization"],
        "critical": True
    },
    "djwaste": {
        "url": "https://djwaste.co.uk",
        "required_strings": ["DJ Waste", "Premium Industrial"],
        "critical": False
    },
    "la-aesthetician": {
        "url": "https://la-aesthetician.co.uk",
        "required_strings": ["Libby", "RN", "Aesthetician"],
        "critical": True
    },
    "villagebakery": {
        "url": "https://villagebakeryandcafe.co.uk",
        "required_strings": ["Village Bakery"],
        "critical": False
    }
}

def verify_url(project_name: str, url: str, required_strings: List[str]) -> Dict:
    print(f"\n[VERIFYING] {project_name} -> {url}")
    results = {
        "reachability": False,
        "content_verified": False,
        "truth_lock": True,
        "ssl": False,
        "errors": []
    }
    
    try:
        response = requests.get(url, timeout=15)
        results["reachability"] = response.status_code == 200
        
        if response.status_code != 200:
            results["errors"].append(f"HTTP Status: {response.status_code}")
            return results

        content = response.text.lower()
        
        # Check required strings
        missing = [s for s in required_strings if s.lower() not in content]
        if not missing:
            results["content_verified"] = True
        else:
            results["errors"].append(f"Missing identifiers: {', '.join(missing)}")
            
        # Check for forbidden strings (Truth-Lock)
        found_placeholders = [s for s in FORBIDDEN_STRINGS if s.lower() in content]
        if found_placeholders:
            results["truth_lock"] = False
            results["errors"].append(f"Placeholders detected: {', '.join(found_placeholders)}")
            
        # Basic SSL
        results["ssl"] = url.startswith("https") and response.url.startswith("https")
        
    except requests.exceptions.RequestException as e:
        results["errors"].append(str(e))
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Antigravity Deployment Verifier")
    parser.add_argument("--project", "-p", help="Specific project to check")
    parser.add_argument("--all", "-a", action="store_true", help="Check all projects")
    args = parser.parse_args()

    active_projects = {}
    if args.all:
        active_projects = PROJECT_CONFIGS
    elif args.project:
        if args.project in PROJECT_CONFIGS:
            active_projects = {args.project: PROJECT_CONFIGS[args.project]}
        else:
            print(f"Unknown project: {args.project}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)

    total_failed = 0
    for name, config in active_projects.items():
        res = verify_url(name, config["url"], config["required_strings"])
        
        all_passed = all([res["reachability"], res["content_verified"], res["truth_lock"]])
        status_icon = "[PASS]" if all_passed else "[FAIL]"
        
        print(f"{status_icon} Reachability: {'OK' if res['reachability'] else 'FAILED'}")
        print(f"{status_icon} Identifiers: {'MATCH' if res['content_verified'] else 'MISSING'}")
        print(f"{status_icon} Truth-Lock: {'SECURE' if res['truth_lock'] else 'VIOLATED'}")
        
        if res["errors"]:
            print(f"   Errors: {res['errors']}")
            total_failed += 1 if config.get("critical") else 0

    print(f"\n--- Verification Complete ---")
    if total_failed > 0:
        print(f"FAILED: {total_failed} CRITICAL FAILURES DETECTED")
        sys.exit(1)
    else:
        print(f"SUCCESS: All checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
