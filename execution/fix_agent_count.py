"""Fix all agent count references to 44 across the website."""
import os

BASE = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\src"

replacements = {
    os.path.join(BASE, "components", "sections", "Hero.tsx"): [
        ("39-Agent Orchestra", "44-Agent Orchestra"),
        ('tracking-tight">39</div>', 'tracking-tight">44</div>'),
    ],
    os.path.join(BASE, "app", "layout.tsx"): [
        ("42 specialized AI agents", "44 specialized AI agents"),
        ("42-agent orchestra", "44-agent orchestra"),
    ],
    os.path.join(BASE, "data", "news.ts"): [
        ("All 39 agents", "All 44 agents"),
        ("39-agent orchestra", "44-agent orchestra"),
    ],
}

for filepath, pairs in replacements.items():
    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filepath}")
        continue
    content = open(filepath, "r", encoding="utf-8").read()
    for old, new in pairs:
        if old in content:
            content = content.replace(old, new)
            print(f"  REPLACED: '{old}' -> '{new}'")
        else:
            print(f"  NOT FOUND in file: '{old}'")
    open(filepath, "w", encoding="utf-8").write(content)
    print(f"SAVED: {filepath}")

print("\nDone! All agent counts updated to 44.")
