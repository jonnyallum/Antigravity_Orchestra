import sys
import io

# Force UTF-8 for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import re

def audit_diff(filename):
    print(f"🔍 AUDITING CHANGES: {filename}")
    
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return False

    try:
        content = open(filename, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    score = 100
    violations = []

    # 1. Look for Placeholder Text
    placeholders = ["lorem ipsum", "todo", "fixme", "pending initialization", "[REPLACE]", "[PLACEHOLDER]"]
    for p in placeholders:
        if p.lower() in content.lower():
            score -= 20
            violations.append(f"Placeholder detected: '{p}'")

    # 2. Look for hardcoded style strings (should use tokens)
    if filename.endswith(".css") or filename.endswith(".tsx"):
        if 'color: "#' in content or "background: '#" in content:
            score -= 10
            violations.append("Hardcoded hex color detected. Use design tokens (HSL) instead.")

    # 3. Look for large file sizes (>500 lines) without complexity comments
    line_count = len(content.splitlines())
    if line_count > 500:
        score -= 10
        violations.append(f"Large file ({line_count} lines) without modular decomposition.")

    # 4. Check for console.logs left in production code
    if filename.endswith(".js") or filename.endswith(".ts") or filename.endswith(".tsx"):
        if "console.log" in content:
            score -= 5
            violations.append("Console.log detected. Ensure debugging statements are removed.")

    print(f"📊 QUALITY SCORE: {max(0, score)}/100")
    if violations:
        print("Violations:")
        for v in violations:
            print(f"  - {v}")
    
    return score >= 80

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python execution/diff_audit.py [filename]")
        sys.exit(1)
        
    success = audit_diff(sys.argv[1])
    sys.exit(0 if success else 1)
