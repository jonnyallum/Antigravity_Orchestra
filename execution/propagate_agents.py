import os, subprocess

WORKSPACE = r"C:\Users\jonny\Desktop\AgOS 3.0 template"
SOURCE = os.path.join(WORKSPACE, "AGENTS.md")
TARGETS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]

with open(SOURCE, encoding="utf-8") as f:
    CANONICAL = f.read()

assert "> **Jai.OS 4.0**" in CANONICAL, "Missing Jai.OS 4.0 tag"
assert "Parallel Learning" in CANONICAL, "Missing Parallel Learning"
assert "Supabase Shared Brain" in CANONICAL, "Missing Supabase Shared Brain"
assert "Betting Ecosystem Tier" in CANONICAL, "Missing Betting Tier"
assert "Shared Brain: ONLINE" in CANONICAL, "Missing Shared Brain ONLINE"
print("Content verified: all required sections present")
print(f"File size: {len(CANONICAL.encode())/1024:.1f}KB")

updated = []
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", ".git"]]
    for filename in files:
        if filename in TARGETS:
            full_path = os.path.join(root, filename)
            rel = full_path.replace(WORKSPACE + "\\", "")
            if full_path == SOURCE:
                print(f"  [SOURCE] {rel}")
                continue
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(CANONICAL)
            print(f"  [OK] {rel}")
            updated.append(rel)

print(f"\nUpdated {len(updated)} files")

os.chdir(WORKSPACE)
subprocess.run(["git", "add", "-A"])
r = subprocess.run(
    ["git", "commit", "-m",
     "[Jai.OS 4.0] Full 45-agent roster, 11 tiers, Parallel Learning, MCP integrations, Supabase Brain | 2026-02-19"],
    capture_output=True, text=True
)
print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip()[:100])

r2 = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if r2.returncode == 0:
    print("[OK] Pushed to GitHub main")
else:
    print(f"[FAIL] {r2.stderr.strip()[:150]}")
    # Try rebase and push
    subprocess.run(["git", "pull", "--rebase", "origin", "main"])
    r3 = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print("[OK] Pushed after rebase" if r3.returncode == 0 else f"[FAIL] {r3.stderr.strip()[:100]}")

print("\nDONE — https://github.com/jonnyallum/Antigravity_Orchestra")
