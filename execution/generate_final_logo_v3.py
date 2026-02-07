
import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from dotenv import load_dotenv

load_dotenv()

# PATHS
INPUT_ICON = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts\prism_monolith_j.png"
OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public"
FILENAME_FULL = "jonnyai_logo_final_v3.png"

# COLORS
ELECTRIC_BLUE = "#00F0FF" # High-energy Cyan
WHITE_GLOW = "#FFFFFF"

# 1. LOAD THE CHOSEN ICON
if not os.path.exists(INPUT_ICON):
    print(f"❌ Error: Icon file not found at {INPUT_ICON}")
    exit(1)

icon = Image.open(INPUT_ICON).convert("RGBA")

# 2. CREATE CANVAS (Black Background)
W, H = 1600, 600
bg = Image.new("RGB", (W, H), "black") 

# 3. ICON PROCESSING (GLOW + SEPARATION)
icon_size = 500
icon_resized = icon.resize((icon_size, icon_size))

# Add Glow to Icon
icon_glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
glow_draw = ImageDraw.Draw(icon_glow_layer)

icon_x = 50
icon_y = (H - icon_size) // 2
center_x = icon_x + icon_size//2
center_y = icon_y + icon_size//2

# Draw radial white glow for icon
radius = 320
for r in range(radius, 0, -10):
    alpha = int((1 - r/radius) * 30) 
    glow_draw.ellipse((center_x-r+10, center_y-r+10, center_x+r-10, center_y+r-10), fill=(255, 255, 255, alpha))

bg.paste(icon_glow_layer, (0,0), mask=icon_glow_layer)
bg.paste(icon_resized, (icon_x, icon_y), mask=icon_resized)

# 4. TYPOGRAPHY (MATCHING OUTFIT/INTER FONT)
draw = ImageDraw.Draw(bg)

try:
    # Use a Variable Font if available or standard sans-serif
    # Outfit is close to Geometric Sans like Montserrat or Futura
    font_path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
    if not os.path.exists(font_path):
         font_path = r"C:\Windows\Fonts\seguiemj.ttf" 
    
    # "Jonny" - Thicker
    font_size_jonny = 180
    font_jonny = ImageFont.truetype(font_path, font_size_jonny)
    
    # "Ai" - Matching style
    font_size_ai = 180
    font_ai = ImageFont.truetype(font_path, font_size_ai)

except:
    font_jonny = ImageFont.load_default()
    font_ai = ImageFont.load_default()

# POSITIONING (Moved further right as requested)
text_x_start = icon_x + icon_size + 80 # Increased gap
text_y = (H - font_size_jonny) // 2 - 25

# DRAW "Jonny" (White)
draw.text((text_x_start, text_y), "Jonny", fill="white", font=font_jonny)
jonny_w = draw.textlength("Jonny", font=font_jonny)

# DRAW "Ai" (Electric Blue + Glow)
ai_x = text_x_start + jonny_w
# Adjust "Ai" font to be same as "Jonny" but colored
# Draw Glow for "Ai"
ai_glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
ai_glow_draw = ImageDraw.Draw(ai_glow_layer)

for i in range(8):
    blur = (i+1) * 2
    ai_glow_draw.text((ai_x, text_y), "Ai", fill=ELECTRIC_BLUE, font=font_ai)

ai_glow_layer = ai_glow_layer.filter(ImageFilter.GaussianBlur(radius=10))
bg.paste(ai_glow_layer, (0,0), mask=ai_glow_layer)

# Sharp "Ai" on top
draw.text((ai_x, text_y), "Ai", fill=ELECTRIC_BLUE, font=font_ai)

# SAVE
save_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
bg.save(save_path)
print(f"✅ SUCCESS! Saved V3 Logo to: {save_path}")
