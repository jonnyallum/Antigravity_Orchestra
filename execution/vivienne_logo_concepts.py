
"""
@Vivienne - Brand & Logo Design
Mission: Create 3 world-class logo concepts for JonnyAI

Collaborating with: @Priya (UI/UX)
Brief: Professional AI development studio logo with "Hive Mind" concept
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\logo_concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# BRAND COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ELECTRIC_BLUE = (0, 240, 255)  # #00F0FF
DEEP_BLUE = (15, 23, 42)  # Slate-900 for depth

# CANVAS SETTINGS
W, H = 1600, 600
BACKGROUND = WHITE

def load_font(size):
    """Load professional font with fallbacks"""
    try:
        # Prefer Montserrat Bold (geometric sans)
        path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
        if not os.path.exists(path):
            path = r"C:\Windows\Fonts\seguisb.ttf"  # Segoe UI Bold
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

# =============================================================================
# CONCEPT 1: "THE CORE" - Hexagonal sphere with integrated wordmark
# Style: Modern, geometric, cohesive
# =============================================================================

def create_concept_1():
    """Tight integration. Icon + text as one unified mark."""
    canvas = Image.new("RGB", (W, H), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    
    # LOAD FONT
    font = load_font(180)
    
    # CREATE HIVE SPHERE ICON (PRECISE)
    def draw_hex(d, cx, cy, r, fill):
        pts = [(cx + r * math.cos(math.pi/3 * i - math.pi/6), 
                cy + r * math.sin(math.pi/3 * i - math.pi/6)) for i in range(6)]
        d.polygon(pts, fill=fill)
    
    icon_size = 200
    icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    
    cx, cy = icon_size // 2, icon_size // 2
    hex_r = icon_size // 14
    
    # Hexagon positions (honeycomb pattern)
    positions = [
        (0, 0),  # Center (ELECTRIC BLUE)
        (-1.8, 0), (1.8, 0),  # Left/Right
        (-0.9, -1.6), (0.9, -1.6),  # Top
        (-0.9, 1.6), (0.9, 1.6),  # Bottom
    ]
    
    for i, (px, py) in enumerate(positions):
        x = cx + px * hex_r * 1.5
        y = cy + py * hex_r * 1.5
        color = ELECTRIC_BLUE if i == 0 else BLACK
        draw_hex(icon_draw, x, y, hex_r, color)
    
    # LAYOUT
    text_jonny = "Jonny"
    text_ai = "Ai"
    
    jonny_w = draw.textlength(text_jonny, font=font)
    ai_w = draw.textlength(text_ai, font=font)
    
    gap = 25  # Very tight
    total_w = jonny_w + ai_w + gap + icon_size
    start_x = (W - total_w) // 2
    text_y = (H - 180) // 2
    
    # DRAW TEXT
    draw.text((start_x, text_y), text_jonny, fill=BLACK, font=font)
    ai_x = start_x + jonny_w
    draw.text((ai_x, text_y), text_ai, fill=ELECTRIC_BLUE, font=font)
    
    # DRAW ICON (RIGHT SIDE)
    icon_x = int(ai_x + ai_w + gap)
    icon_y = (H - icon_size) // 2
    
    # Subtle glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.paste(icon, (icon_x - 5, icon_y - 5))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.paste(glow, (0, 0), mask=glow)
    
    canvas.paste(icon, (icon_x, icon_y), mask=icon)
    
    # SAVE
    path = os.path.join(OUTPUT_DIR, "concept_1_the_core.png")
    canvas.save(path)
    print(f"[OK] Concept 1 'The Core': {path}")
    print("  Layout: [Jonny][Ai][Sphere]")
    print("  Style: Modern, tight, unified")

# =============================================================================
# CONCEPT 2: "THE SIGNAL" - Icon as the dot on 'i'
# Style: Elegant, integrated typography
# =============================================================================

def create_concept_2():
    """Icon cleverly replaces the dot on 'i' in 'Ai'"""
    canvas = Image.new("RGB", (W, H), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    
    font = load_font(180)
    
    # CREATE MINI HIVE SPHERE (for dot)
    icon_size = 50  # Smaller for dot
    icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    
    # Draw simplified sphere (fewer hexagons for clean look at small size)
    cx, cy = icon_size // 2, icon_size // 2
    
    # Just draw a clean circle with hex pattern suggestion
    icon_draw.ellipse((5, 5, icon_size-5, icon_size-5), fill=ELECTRIC_BLUE)
    # Small black accents to suggest hexagons
    for angle in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(angle)
        x1 = cx + (icon_size//4) * math.cos(rad)
        y1 = cy + (icon_size//4) * math.sin(rad)
        x2 = cx + (icon_size//3) * math.cos(rad)
        y2 = cy + (icon_size//3) * math.sin(rad)
        icon_draw.line((x1, y1, x2, y2), fill=BLACK, width=2)
    
    # TEXT LAYOUT
    text = "JonnyAi"
    text_w = draw.textlength(text, font=font)
    start_x = (W - text_w) // 2
    text_y = (H - 180) // 2
    
    # Draw "Jonny" in black
    draw.text((start_x, text_y), "Jonny", fill=BLACK, font=font)
    
    # Draw "A" in electric blue
    jonny_w = draw.textlength("Jonny", font=font)
    a_x = start_x + jonny_w
    draw.text((a_x, text_y), "A", fill=ELECTRIC_BLUE, font=font)
    
    # Draw "i" stem in electric blue (NO DOT - replaced by icon)
    a_w = draw.textlength("A", font=font)
    i_x = a_x + a_w
    # Draw vertical line for 'i' stem
    draw.rectangle((i_x + 20, text_y + 60, i_x + 40, text_y + 180), fill=ELECTRIC_BLUE)
    
    # Place icon as the dot
    dot_x = int(i_x + 15)
    dot_y = int(text_y + 20)
    canvas.paste(icon, (dot_x, dot_y), mask=icon)
    
    path = os.path.join(OUTPUT_DIR, "concept_2_the_signal.png")
    canvas.save(path)
    print(f"[OK] Concept 2 'The Signal': {path}")
    print("  Layout: [JonnyA[*]i] (dot is icon)")
    print("  Style: Elegant, clever integration")

# =============================================================================
# CONCEPT 3: "THE STACK" - Vertical emphasis, architectural
# Style: Bold, structured, commanding
# =============================================================================

def create_concept_3():
    """Stacked layout - icon above text for vertical impact"""
    canvas = Image.new("RGB", (W, H), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    
    font_large = load_font(200)
    
    # CREATE HEXAGONAL ICON (LARGER, MORE DETAILED)
    icon_size = 280
    icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    
    def draw_hex(d, cx, cy, r, fill, outline=None):
        pts = [(cx + r * math.cos(math.pi/3 * i - math.pi/6), 
                cy + r * math.sin(math.pi/3 * i - math.pi/6)) for i in range(6)]
        d.polygon(pts, fill=fill, outline=outline, width=2)
    
    cx, cy = icon_size // 2, icon_size // 2
    hex_r = icon_size // 12
    
    # More complex honeycomb
    positions = [
        (0, 0),  # Center (BLUE)
        # Inner ring (BLACK)
        (-2, 0), (2, 0), (-1, -1.73), (1, -1.73), (-1, 1.73), (1, 1.73),
        # Outer ring (BLACK with blue outlines)
        (-3, -1.73), (0, -3.46), (3, -1.73), (3, 1.73), (0, 3.46), (-3, 1.73),
    ]
    
    for i, (px, py) in enumerate(positions):
        x = cx + px * hex_r * 1.1
        y = cy + py * hex_r * 1.1
        
        if i == 0:
            fill = ELECTRIC_BLUE
            outline = None
        elif i < 7:
            fill = BLACK
            outline = None
        else:
            fill = BLACK
            outline = ELECTRIC_BLUE
        
        draw_hex(icon_draw, x, y, hex_r, fill, outline)
    
    # Add glow to icon
    glow_layer = Image.new("RGBA", (icon_size + 40, icon_size + 40), (0, 0, 0, 0))
    glow_layer.paste(icon, (20, 20))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=10))
    
    # LAYOUT (STACKED)
    icon_x = (W - icon_size) // 2
    icon_y = 80
    
    canvas.paste(glow_layer, (icon_x - 20, icon_y - 20), mask=glow_layer)
    canvas.paste(icon, (icon_x, icon_y), mask=icon)
    
    # TEXT BELOW
    text = "JonnyAi"
    text_w = draw.textlength(text, font=font_large)
    text_x = (W - text_w) // 2
    text_y = icon_y + icon_size + 40
    
    # Draw with split color
    jonny_w = draw.textlength("Jonny", font=font_large)
    draw.text((text_x, text_y), "Jonny", fill=BLACK, font=font_large)
    draw.text((text_x + jonny_w, text_y), "Ai", fill=ELECTRIC_BLUE, font=font_large)
    
    path = os.path.join(OUTPUT_DIR, "concept_3_the_stack.png")
    canvas.save(path)
    print(f"[OK] Concept 3 'The Stack': {path}")
    print("  Layout: [[*]Icon[*]]")
    print("          [JonnyAi]")
    print("  Style: Bold, architectural, vertical impact")

# =============================================================================
# GENERATE ALL CONCEPTS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("@VIVIENNE - LOGO CONCEPT GENERATION")
    print("Collaborating with @Priya for UI Integration")
    print("=" * 60)
    print()
    
    create_concept_1()
    print()
    create_concept_2()
    print()
    create_concept_3()
    print()
    
    print("=" * 60)
    print("COMPLETED: 3 Professional Logo Concepts")
    print(f"Location: {OUTPUT_DIR}")
    print()
    print("NEXT STEPS:")
    print("1. Review all 3 concepts")
    print("2. Select preferred direction")
    print("3. @Priya will test in actual UI (nav, hero, favicon)")
    print("4. Final refinement to pixel perfection")
    print("=" * 60)
