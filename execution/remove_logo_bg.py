"""
Remove background from JonnyAI logo images using rembg (AI-powered).
Produces proper RGBA PNG files with true transparency.

@Agent: @Priya (The Perfectionist)
@Purpose: Fix the checkerboard background issue on hero logo
"""

import os
import sys
from pathlib import Path

def main():
    try:
        from rembg import remove
        from PIL import Image
    except ImportError:
        print("ERROR: rembg not installed. Run: python -m pip install rembg[cpu]")
        sys.exit(1)

    base = Path(__file__).parent.parent / "Clients" / "jonnyai.website"
    public_logo = base / "public" / "Logo"
    
    # === 1. HERO LOGO: Remove background from brand-hero.png ===
    hero_src = public_logo / "jonnyai-brand-hero.png"
    hero_out = public_logo / "jonnyai-hero-transparent.png"
    
    if not hero_src.exists():
        print(f"ERROR: Source not found: {hero_src}")
        sys.exit(1)
    
    print(f"Processing hero logo: {hero_src}")
    print(f"  Input mode: {Image.open(hero_src).mode}, Size: {Image.open(hero_src).size}")
    
    with open(hero_src, "rb") as f:
        input_data = f.read()
    
    output_data = remove(input_data)
    
    with open(hero_out, "wb") as f:
        f.write(output_data)
    
    result = Image.open(hero_out)
    print(f"  Output mode: {result.mode}, Size: {result.size}")
    assert result.mode == "RGBA", f"Expected RGBA, got {result.mode}"
    
    # Verify alpha channel has actual transparency
    alpha = result.split()[3]
    alpha_stats = alpha.getextrema()
    print(f"  Alpha range: {alpha_stats[0]}-{alpha_stats[1]} (0=transparent, 255=opaque)")
    assert alpha_stats[0] < 50, "Background not removed - alpha min too high"
    print(f"  [OK] Hero logo saved: {hero_out}")
    
    # === 2. ICON: Remove background from icon ===
    icon_src = public_logo / "Jonny Ai - Icon.png"
    icon_out = public_logo / "jonnyai-icon-transparent.png"
    
    if icon_src.exists():
        print(f"\nProcessing icon: {icon_src}")
        with open(icon_src, "rb") as f:
            icon_data = f.read()
        
        icon_output = remove(icon_data)
        
        with open(icon_out, "wb") as f:
            f.write(icon_output)
        
        icon_result = Image.open(icon_out)
        print(f"  Output mode: {icon_result.mode}, Size: {icon_result.size}")
        icon_alpha = icon_result.split()[3]
        icon_stats = icon_alpha.getextrema()
        print(f"  Alpha range: {icon_stats[0]}-{icon_stats[1]}")
        print(f"  [OK] Icon saved: {icon_out}")
    else:
        print(f"  [WARN] Icon not found: {icon_src}")
    
    # === 3. Delete the broken checkerboard webp ===
    broken_webp = public_logo / "jonnyai-hero-transparent.webp"
    if broken_webp.exists():
        os.remove(broken_webp)
        print(f"\n  [DELETED] Broken checkerboard file: {broken_webp}")
    
    print("\n[OK] ALL DONE. Logo files are now truly transparent (RGBA with alpha channel).")
    print("\nFiles to use in code:")
    print(f"  Hero: /Logo/jonnyai-hero-transparent.png")
    print(f"  Icon: /Logo/jonnyai-icon-transparent.png")

if __name__ == "__main__":
    main()
