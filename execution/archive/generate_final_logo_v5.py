
import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from dotenv import load_dotenv

load_dotenv()

# PATHS
INPUT_ICON = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts\prism_monolith_j.png"
OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public"
FILENAME_FULL = "jonnyai_logo_final_v5.png"

# COLORS
ELECTRIC_BLUE = "#00F0FF"
WHITE = "#FFFFFF"

if not os.path.exists(INPUT_ICON):
    print(f"❌ Error: Icon file not found at {INPUT_ICON}")
    exit(1)

icon = Image.open(INPUT_ICON).convert("RGBA")

# 2. CREATE CANVAS
W, H = 1600, 600
bg = Image.new("RGB", (W, H), "black") 
draw = ImageDraw.Draw(bg)

# 3. TYPOGRAPHY - THICKER JONNY
try:
    # "Slightly Thick" -> Arial Bold was used. User wants "Slightly Thicker".
    # Try Arial Black or Segoe UI Black.
    font_path_thick = r"C:\Windows\Fonts\ariblk.ttf" # Arial Black
    if not os.path.exists(font_path_thick):
         font_path_thick = r"C:\Windows\Fonts\seguiemj.ttf" # Fallback
    
    font_size = 200
    font_jonny = ImageFont.truetype(font_path_thick, font_size)
    font_ai = ImageFont.truetype(font_path_thick, font_size) # AI matches style
except:
    font_jonny = ImageFont.load_default()
    font_ai = ImageFont.load_default()

# 4. LAYOUT CALCULATIONS
# Text "Jonny"
text_jonny = "Jonny"
jonny_w = draw.textlength(text_jonny, font=font_jonny)
gap = 40 # Space between Jonny and the Box

# THE BOX / MONOLITH COMPOSITION
# The Monolith IS the box background.
# Resizing icon to be the container.
box_h = int(font_size * 1.6) # Taller than text
# Maintain aspect ratio of icon
icon_aspect = icon.width / icon.height 
box_w = int(box_h * icon_aspect) 

# Ensure "Ai" fits inside box_w?
ai_w = draw.textlength("Ai", font=font_ai)
if box_w < ai_w + 40:
    # Scale up box if text doesn't fit? Or scale text down?
    # User said "Ai inside the box". Let's scale box up slightly if needed.
    # But Monolith shape is fixed.
    pass 

# Positioning
total_w = jonny_w + gap + box_w
start_x = (W - total_w) // 2
text_baseline_y = (H - font_size) // 2 

# DRAW "Jonny"
draw.text((start_x, text_baseline_y), text_jonny, fill=WHITE, font=font_jonny)

# DRAW THE BOX (MONOLITH) TO THE RIGHT
box_x = start_x + jonny_w + gap
box_y = (H - box_h) // 2

# Process Icon/Box
# "Monolith just behind the Ai"
# We place the icon at box_x, box_y
icon_resized = icon.resize((box_w, box_h))

# Add Glow BEHIND the Monolith?
glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
glow_draw = ImageDraw.Draw(glow_layer)
# Electric Blue Glow behind the "Box"
glow_draw.ellipse((box_x-40, box_y-40, box_x+box_w+40, box_y+box_h+40), fill=(0, 240, 255, 60))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=20))
bg.paste(glow_layer, (0,0), mask=glow_layer)

# DIm the icon slightly so text pops?
# icon_dim = ImageEnhance.Brightness(icon_resized).enhance(0.7) 
# Actually user said "Monolith behind Ai". Monolith is usually black/dark. 
# If "Ai" is Electric Blue, it should pop on black.
bg.paste(icon_resized, (int(box_x), int(box_y)), mask=icon_resized)

# DRAW "Ai" INSIDE THE BOX
# Center "Ai" within the Box (Monolith) bounds
ai_x = box_x + (box_w - ai_w) // 2
ai_y = text_baseline_y # Align baseline with Jonny? Or center in box?
# Usually visual adjustment needed vertical center of box
ai_y_centered = box_y + (box_h - font_size) // 2 - 10 # -10 Visual adjustment

# "Ai" Glow (Electric Blue)
ai_glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
aig_draw = ImageDraw.Draw(ai_glow_layer)
for i in range(10):
    aig_draw.text((ai_x, ai_y_centered), "Ai", fill=ELECTRIC_BLUE, font=font_ai)
ai_glow_layer = ai_glow_layer.filter(ImageFilter.GaussianBlur(radius=10))
bg.paste(ai_glow_layer, (0,0), mask=ai_glow_layer)

# Sharp "Ai"
draw.text((ai_x, ai_y_centered), "Ai", fill=ELECTRIC_BLUE, font=font_ai)

# SAVE
save_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
bg.save(save_path)
print(f"✅ SUCCESS! Saved V5 Logo to: {save_path}")
