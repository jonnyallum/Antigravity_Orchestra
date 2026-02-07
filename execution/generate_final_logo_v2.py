
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# PATHS
INPUT_ICON = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts\prism_monolith_j.png"
OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public"
FILENAME_FULL = "jonnyai_logo_final.png"

# COLORS
ELECTRIC_BLUE = "#00F0FF" # High-energy Cyan/Blue from the "Electric" concept
WHITE_GLOW = "#FFFFFF"

# 1. LOAD THE CHOSEN ICON
if not os.path.exists(INPUT_ICON):
    print(f"❌ Error: Icon file not found at {INPUT_ICON}")
    exit(1)

icon = Image.open(INPUT_ICON)
print(f"✅ Loaded Icon: {INPUT_ICON}")

# 2. CREATE CANVAS (Black Background)
W, H = 1600, 600
canvas = Image.new("RGBA", (W, H), (0,0,0,0)) # Transparent first for png
bg = Image.new("RGB", (W, H), "black") # Black BG version

# 3. PROCESS ICON (Add White Glow)
# Resize
icon_size = 500
icon_resized = icon.resize((icon_size, icon_size)) # Quality?

# Create a glow layer for the icon
# Since the icon is likely on black, we can mask it? Or just place it.
# The user asked for a "slight white outline glow".
# If the icon is rectangular (black bg), the glow will be a box. 
# We'll assume the icon has a black background. We can try to blend it or just add a radial glow behind it.

# Let's add a radial white glow BEHIND the icon position
glow_behind = Image.new("RGBA", (W, H), (0,0,0,0))
draw_glow = ImageDraw.Draw(glow_behind)
# Center of icon
icon_x = 50
icon_y = (H - icon_size) // 2
center_x = icon_x + icon_size//2
center_y = icon_y + icon_size//2

# Draw radial gradient simulation (concentric circles fading out)
# White glow...
radius = 300
for r in range(radius, 0, -5):
    alpha = int((1 - r/radius) * 40) # Low opacity
    draw_glow.ellipse((center_x-r, center_y-r, center_x+r, center_y+r), fill=(255, 255, 255, alpha))

# Composite Icon on top of glow
bg.paste(glow_behind, (0,0), mask=glow_behind)
bg.paste(icon_resized, (icon_x, icon_y))

# 4. TYPOGRAPHY
draw = ImageDraw.Draw(bg)

# Load Font
try:
    # Trying for a modern, tech font. Arial Bold is safe fallback.
    font_path = r"C:\Windows\Fonts\seguiemj.ttf" # Segoe UI?
    if not os.path.exists(font_path):
         font_path = r"C:\Windows\Fonts\arialbd.ttf"
    
    font_size = 180
    font = ImageFont.truetype(font_path, font_size)
except:
    font = ImageFont.load_default()

# "Jonny" (White)
text_x = icon_x + icon_size + 40
text_y = (H - font_size) // 2 - 20 

draw.text((text_x, text_y), "Jonny", fill="white", font=font)
jonny_w = draw.textlength("Jonny", font=font)

# "Ai" (Electric Blue + Glow)
ai_x = text_x + jonny_w
ai_y = text_y

# Create "Ai" Glow
# Draw multiple blurred layers
for i in range(5):
    blur_amount = (i+1) * 3
    # Draw text on temp layer
    temp = Image.new("RGBA", (W, H), (0,0,0,0))
    d_temp = ImageDraw.Draw(temp)
    d_temp.text((ai_x, ai_y), "Ai", fill=ELECTRIC_BLUE, font=font)
    temp = temp.filter(ImageFilter.GaussianBlur(radius=blur_amount))
    # Paste with additive blend? or just alpha composite
    bg.paste(temp, (0,0), mask=temp)

# Draw Sharp "Ai" on top
draw.text((ai_x, ai_y), "Ai", fill=ELECTRIC_BLUE, font=font)

# SAVE
save_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
bg.save(save_path)
print(f"✅ SUCCESS! Saved Final Logo to: {save_path}")
