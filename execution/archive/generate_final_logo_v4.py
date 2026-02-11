
import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from dotenv import load_dotenv

load_dotenv()

# PATHS
INPUT_ICON = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts\number_one_icon.png" # Assuming we might want to just re-use the good icon or regenerate a specific "merged" concept
# Actually, since the user wants them MERGED, we need to composites them VERY tightly.

# Let's use the Monolith Icon again as base but position it differently
INPUT_ICON = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts\prism_monolith_j.png"
OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public"
FILENAME_FULL = "jonnyai_logo_merged_v4.png"

# COLORS
ELECTRIC_BLUE = "#00F0FF" # Cyan/Blue
WHITE_GLOW = "#FFFFFF"

if not os.path.exists(INPUT_ICON):
    print(f"❌ Error: Icon file not found at {INPUT_ICON}")
    exit(1)

icon = Image.open(INPUT_ICON).convert("RGBA")

# 2. CREATE CANVAS (Black Background)
W, H = 1600, 600
bg = Image.new("RGB", (W, H), "black") 

# 3. TYPOGRAPHY FIRST (To determine spacing)
draw = ImageDraw.Draw(bg)

try:
    font_path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
    if not os.path.exists(font_path):
         font_path = r"C:\Windows\Fonts\seguiemj.ttf" 
    
    # HUGE FONT
    font_size = 200
    font = ImageFont.truetype(font_path, font_size)
except:
    font = ImageFont.load_default()

# 4. COMPOSITING - THE "MERGE"
# Strategy: The Icon acts as the "J" or sits immediately to the left, touching the text.
# Let's try placing the icon immediately to the left of "onnyAi" (replacing the J?)
# Or just very close.

# Let's keep "Jonny" text intact but move icon close.
# Calculate text size
text_jonny = "Jonny"
text_ai = "Ai"
jonny_w = draw.textlength(text_jonny, font=font)
ai_w = draw.textlength(text_ai, font=font)

# Icon Size
icon_target_h = int(font_size * 1.5) # 1.5x text height
icon_aspect = icon.width / icon.height
icon_target_w = int(icon_target_h * icon_aspect)
icon_resized = icon.resize((icon_target_w, icon_target_h))

# Total Width estimation
gap = 20 # Tight gap
total_w = icon_target_w + gap + jonny_w + ai_w
start_x = (W - total_w) // 2
center_y = (H - icon_target_h) // 2

# DRAW ICON (With Glow)
icon_x = start_x
icon_y = center_y

# Glow behind icon
glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
glow_draw = ImageDraw.Draw(glow_layer)
glow_radius = 60
glow_draw.ellipse((icon_x - glow_radius, icon_y - glow_radius, icon_x + icon_target_w + glow_radius, icon_y + icon_target_h + glow_radius), fill=(255, 255, 255, 40)) # White glow
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=30))
bg.paste(glow_layer, (0,0), mask=glow_layer)

# Paste Icon
bg.paste(icon_resized, (int(icon_x), int(icon_y)), mask=icon_resized)


# DRAW TEXT "Jonny" (White)
text_x = icon_x + icon_target_w + gap
text_y_baseline = icon_y + (icon_target_h - font_size) // 2 # Center vertically with icon
# Adjust for font ascent/descent if needed, usually intuitive centering works for logos

draw.text((text_x, text_y_baseline), text_jonny, fill="white", font=font)

# DRAW TEXT "Ai" (Electric Blue + HEAVY GLOW)
ai_x = text_x + jonny_w
# "Ai" Glow
ai_glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
ai_glow_draw = ImageDraw.Draw(ai_glow_layer)

# Intense Blue Glow
for i in range(15): # More layers = stronger core
    blur = (i+1) * 3
    ai_glow_draw.text((ai_x, text_y_baseline), text_ai, fill=ELECTRIC_BLUE, font=font)

ai_glow_layer = ai_glow_layer.filter(ImageFilter.GaussianBlur(radius=15))
bg.paste(ai_glow_layer, (0,0), mask=ai_glow_layer)

# Sharp "Ai" Text
draw.text((ai_x, text_y_baseline), text_ai, fill=ELECTRIC_BLUE, font=font)

# SAVE
save_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
bg.save(save_path)
print(f"✅ SUCCESS! Saved Merged V4 Logo to: {save_path}")
print(f"   Icon: {icon_target_w}x{icon_target_h} px")
print(f"   Gap: {gap} px")
