import sys
import io

# Force UTF-8 for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import json
from pathlib import Path

ROOT = Path(r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0")
CONTEXT_DIR = ROOT / ".agent" / "context"

def create_context_template(project_name, metadata):
    """Creates a standardized context file for a project."""
    if not CONTEXT_DIR.exists():
        CONTEXT_DIR.mkdir(parents=True)
        
    context_file = CONTEXT_DIR / f"{project_name}.json"
    
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ CONTEXT TEMPLATE CREATED: {context_file}")

def get_current_context(project_name):
    """Loads context for the current active project."""
    context_file = CONTEXT_DIR / f"{project_name}.json"
    if context_file.exists():
        return json.load(open(context_file, 'r', encoding='utf-8'))
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python inject_context.py [create|load] [project_name]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    name = sys.argv[2]
    
    if cmd == "create":
        # Example metadata if none provided
        meta = {
            "client_name": name,
            "tech_stack": ["Next.js 15", "Tailwind v4", "Supabase"],
            "deployment_target": "Vercel",
            "active_specialists": ["@Sebastian", "@Priya", "@Diana"]
        }
        create_context_template(name, meta)
    elif cmd == "load":
        ctx = get_current_context(name)
        if ctx:
            print(json.dumps(ctx, indent=2))
        else:
            print(f"❌ No context found for {name}")
