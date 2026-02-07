
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public"
ICON_PATH = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts\hive_mind_sphere.png"

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
    font_path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = r"C:\Windows\Fonts\seguisb.ttf"
    
    font_size = 180
    font = ImageFont.truetype(font_path, font_size)
except:
    print("Using default font")
    font = ImageFont.load_default()

# LOAD THE AI-GENERATED HIVE SPHERE
if not os.path.exists(ICON_PATH):
    print(f"Error: Icon not found at {ICON_PATH}")
    exit(1)

icon = Image.open(ICON_PATH).convert("RGBA")

# Resize icon to appropriate size
icon_size = 220
icon = icon.resize((icon_size, icon_size))

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
output_path = os.path.join(OUTPUT_DIR, "jonnyai_logo_final.png")
bg.save(output_path)
print(f"Created professional logo: {output_path}")
print(f"Layout: [Jonny] [Ai] [Hive Mind Sphere]")
print(f"Using AI-generated sphere from: {ICON_PATH}")
