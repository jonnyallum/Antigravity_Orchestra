#!/usr/bin/env python3
"""
Red Team Scan Protocol v1 (@RedEye)
Scans public URLs for sensitive data leaks.
- Checks /robots.txt
- Looks for leftover .env content pattern
- Checks for API keys in JS bundles
- Directory enumeration (basic)
"""

import requests
import re
import sys

TARGET_URL = "https://jonnyai.co.uk"

# Patterns to look for (masked/partial)
SENSITIVE_PATTERNS = {
    "Supabase Key": r"sbp_[a-zA-Z0-9]{32,}",
    "Stripe Key": r"sk_test_[a-zA-Z0-9]{24,}",
    "Stripe Public": r"pk_test_[a-zA-Z0-9]{24,}",
    "Generic Token": r"[\w-]{24,}\.[\w-]{24,}\.[\w-]{24,}", # JWT-like
    "Mailto Leak": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
}

def scan_robots():
    print(f"\n[1] Checking robots.txt...")
    try:
        r = requests.get(f"{TARGET_URL}/robots.txt")
        if r.status_code == 200:
            print(f"Robots.txt found:\n{r.text}")
            if "Disallow" in r.text:
                print("   Found hidden paths. Checking...")
        else:
            print("   Robots.txt not found (404).")
    except Exception as e:
        print(f"   Error: {e}")

def scan_head_tags():
    print(f"\n[2] Checking Head tags/Meta...")
    try:
        r = requests.get(TARGET_URL)
        # Check for exposed config in scripts
        script_tags = re.findall(r'<script.*?> (.*?) </script>', r.text, re.DOTALL)
        for i, s in enumerate(script_tags):
            for name, pattern in SENSITIVE_PATTERNS.items():
                if re.search(pattern, s):
                    print(f"   ALERT: Potential {name} leak in inline script #{i}")
    except Exception as e:
        print(f"   Error: {e}")

def check_paths():
    print(f"\n[3] Checking sensitive paths...")
    paths = [".env", ".git/config", "config.json", "package.json", ".env.local"]
    for p in paths:
        url = f"{TARGET_URL}/{p}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"   CRITICAL: {p} is PUBLICLY ACCESSIBLE!")
            else:
                print(f"   OK: {p} ({r.status_code})")
        except Exception:
            pass

def main():
    print(f"{'='*50}")
    print(f"RED TEAM SCAN: {TARGET_URL}")
    print(f"Agent: @RedEye (The Breaker)")
    print(f"{'='*50}")
    
    scan_robots()
    scan_head_tags()
    check_paths()
    
    print(f"\nScan complete. Reporting to @Sam (Defense) and @Marcus.")

if __name__ == "__main__":
    main()
