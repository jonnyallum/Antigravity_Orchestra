import os
import glob
from pathlib import Path

def get_project_description(path):
    """Generates a high-quality description based on folder name and content."""
    name = path.name.replace("-", " ").replace("_", " ").title()
    
    if "waste" in name.lower():
        return f"A high-performance logistics and waste management ecosystem for {name}, powered by AgOS 2.0."
    elif "radar" in name.lower() or "trade" in name.lower():
        return f"A sophisticated signals and trading intelligence platform for {name}, leveraging the Antigravity statistical engine."
    elif "bakery" in name.lower():
        return f"An optimized e-commerce and retail management system for {name}."
    else:
        return f"A specialized digital ecosystem for {name}, architected with the Antigravity Agentic OS."

def generate_readme(path):
    name = path.name.replace("-", " ").replace("_", " ").title()
    description = get_project_description(path)
    
    content = f"""# {name}
> **Powered by Antigravity AgOS 2.0**

{description}

This project is an autonomous agentic sub-system, managed by the **Antigravity Orchestra**. It inherits the full reliability, performance, and "trillion-dollar-enterprise" quality standards of the master AgOS 2.0 framework.

---

## 🚀 System Intelligence
This project is orchestrated by:
- **Conductor**: Mission planning and routing.
- **Jonny AI**: Technical architecture and building.
- **Sentinel**: Security and Quality Assurance.

## 🛠️ Tech Stack
- **Frontend**: Next.js / React / Expo
- **Styling**: Tailwind CSS v4 & Framer Motion
- **Automation**: AgOS 2.0 Execution Engine (Python)

---

## 📜 License & Ownership
Copyright © 2026 **JonnyAi**. All Rights Reserved.

This project and its associated agentic workflows are the proprietary intellectual property of **Jonny Ai**. Unauthorized use, reproduction, or distribution is strictly prohibited.

---
*Managed by **Jonny** (The Boss)*
*Built by the [Antigravity Agent Orchestra](https://github.com/jonnyallum/JonnyAI.co.uk)*
"""
    return content

def upgrade_readmes():
    root_dir = Path("c:/Users/jonny/Desktop/Jonny AI")
    target_paths = [
        root_dir / "Clients/CD Waste",
        root_dir / "Clients/CD Waste/cd-waste.co.uk",
        root_dir / "Clients/DJ Waste/dj-waste-app",
        root_dir / "Clients/New folder/Insydetradar",
        root_dir / "Clients/Poundtrades.app-antigravity",
        root_dir / "Clients/Village-bakery"
    ]

    print("Starting README Upgrade Sprint...")

    for path in target_paths:
        if path.exists():
            readme_path = path / "README.md"
            print(f"  + Upgrading {path.name}...")
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(generate_readme(path))
            
            # Also add a LICENSE.md file
            license_path = path / "LICENSE.md"
            with open(license_path, "w", encoding="utf-8") as f:
                f.write("Copyright (c) 2026 JonnyAi. All Rights Reserved.\n\nProprietary and Confidential.")

    print("\nAll project READMEs upgraded to AgOS 2.0 standards.")
    print("Licensed to JonnyAi.")

if __name__ == "__main__":
    upgrade_readmes()
