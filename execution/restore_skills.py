
import shutil
import os
from pathlib import Path

SOURCE = Path(r"C:\Users\jonny\Desktop\AgOS 3.0 template\.agent\skills")
DEST = Path(r"c:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0\.agent\skills")

def restore_skills():
    print(f"Restoring skills from {SOURCE} to {DEST}...")
    for item in SOURCE.iterdir():
        if item.is_dir():
            source_skill = item / "SKILL.md"
            dest_skill_dir = DEST / item.name
            dest_skill = dest_skill_dir / "SKILL.md"
            
            if source_skill.exists():
                if not dest_skill_dir.exists():
                    dest_skill_dir.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(source_skill, dest_skill)
                print(f"  [OK] Restored {item.name}/SKILL.md")

if __name__ == "__main__":
    restore_skills()
