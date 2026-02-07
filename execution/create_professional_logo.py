
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ELECTRIC_BLUE = (0, 240, 255)

# CANVAS
W, H = 1600, 600
bg = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(bg)

# LOAD PROFESSIONAL FONTS
try:
    # Try Montserrat Bold (geometric sans)
    font_path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
    if not os.path.exists(font_path):
        # Fallback to Segoe UI Bold
        font_path = r"C:\Windows\Fonts\seguisb.ttf"
    
    font_size = 180
    font = ImageFont.truetype(font_path, font_size)
except:
    print("Using default font - install Montserrat for best results")
    font = ImageFont.load_default()

# DRAW PRECISE HEXAGONAL SPHERE ICON
def draw_hexagon(draw, cx, cy, radius, fill):
    """Draw a perfect hexagon centered at (cx, cy)"""
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6  # Start from top
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=fill)

def create_hive_sphere(size):
    """Create a clean hexagonal sphere icon"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    hex_radius = size // 12
    
    # Draw hexagons in a spherical pattern
    positions = [
        (0, 0),  # Center
        (-1.5, -0.87), (-1.5, 0.87),  # Left
        (1.5, -0.87), (1.5, 0.87),    # Right
        (0, -1.74), (0, 1.74),        # Top/Bottom
    ]
    
    for i, (px, py) in enumerate(positions):
        x = cx + px * hex_radius * 2
        y = cy + py * hex_radius * 2
        
        # Center hexagon is ELECTRIC_BLUE (the core)
        if i == 0:
            draw_hexagon(d, x, y, hex_radius, ELECTRIC_BLUE)
        else:
            draw_hexagon(d, x, y, hex_radius, BLACK)
    
    return img

# CREATE THE ICON
icon_size = 220
icon = create_hive_sphere(icon_size)

# LAYOUT CALCULATION
text_jonny = "Jonny"
text_ai = "Ai"

jonny_w = draw.textlength(text_jonny, font=font)
ai_w = draw.textlength(text_ai, font=font)

# Tight spacing
gap = 30

total_w = jonny_w + ai_w + gap + icon_size
start_x = (W - total_w) // 2
text_y = (H - font_size) // 2

# DRAW TEXT
draw.text((start_x, text_y), text_jonny, fill=BLACK, font=font)
ai_x = start_x + jonny_w
draw.text((ai_x, text_y), text_ai, fill=ELECTRIC_BLUE, font=font)

# DRAW ICON (to the right)
icon_x = int(ai_x + ai_w + gap)
icon_y = (H - icon_size) // 2

# Add subtle glow to icon
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow.paste(icon, (icon_x - 10, icon_y - 10))
glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
bg.paste(glow, (0, 0), mask=glow)

# Paste sharp icon
bg.paste(icon, (icon_x, icon_y), mask=icon)

# SAVE
output_path = os.path.join(OUTPUT_DIR, "jonnyai_logo_programmatic.png")
bg.save(output_path)
print(f"Created professional logo: {output_path}")
print(f"Layout: [Jonny] [Ai] [Hive Sphere]")
print(f"Colors: Black, Electric Blue (#00F0FF)")
