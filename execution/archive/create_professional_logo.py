
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# CORRECT PATH
OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\Logo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# COLORS
WHITE = (255, 255, 255)
EMBER_ORANGE = (232, 117, 26) # #e8751a
VIBRANT_GREEN = (34, 197, 94) # #22c55e
VOID_BLACK = (2, 2, 5)

# CANVAS
W, H = 2400, 1000

def create_logo_assets():
    # 1. Generate Full Brand Logo (Hero)
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)

    try:
        # Load premium font
        font_path = r"C:\Windows\Fonts\Montserrat-Bold.ttf"
        if not os.path.exists(font_path):
            font_path = r"C:\Windows\Fonts\outfit-bold.ttf"
            if not os.path.exists(font_path):
                font_path = r"C:\Windows\Fonts\seguisb.ttf"
        
        font_size = 280
        font = ImageFont.truetype(font_path, font_size)
        sub_font_size = 60
        sub_font = ImageFont.truetype(font_path, sub_font_size)
    except:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    text_jonny = "Jonny"
    text_ai = "Ai"

    # Calculate widths
    jonny_w = draw.textlength(text_jonny, font=font)
    ai_w = draw.textlength(text_ai, font=font)
    total_w = jonny_w + ai_w
    
    start_x = (W - total_w) // 2
    text_y = (H - font_size) // 2 - 40

    # Draw Jonny (White)
    draw.text((start_x, text_y), text_jonny, fill=WHITE, font=font)

    # Draw Ai (Orange)
    ai_x = start_x + jonny_w
    draw.text((ai_x, text_y), text_ai, fill=EMBER_ORANGE, font=font)

    # Draw Green Dot
    dot_radius = 16
    # Find position based on 'i' in the 'Ai' string
    # We'll just offset from ai_x
    i_offset = draw.textlength("A", font=font)
    dot_cx = ai_x + i_offset + (draw.textlength("i", font=font) / 2) + 2
    dot_cy = text_y + (font_size * 0.28)
    
    # Outer glow for dot
    for r in range(dot_radius + 4, dot_radius, -1):
        alpha = int(40 * (1 - (r - dot_radius) / 4))
        draw.ellipse([dot_cx - r, dot_cy - r, dot_cx + r, dot_cy + r], fill=(34, 197, 94, alpha))
    
    draw.ellipse([dot_cx - dot_radius, dot_cy - dot_radius, dot_cx + dot_radius, dot_cy + dot_radius], fill=VIBRANT_GREEN)

    # Draw subtitle "JONNY ALLUM INNOVATIONS LTD"
    subtitle = "JONNY ALLUM INNOVATIONS LTD"
    sub_w = draw.textlength(subtitle, font=sub_font)
    sub_x = (W - sub_w) // 2
    sub_y = text_y + font_size + 20
    draw.text((sub_x, sub_y), subtitle, fill=(200, 200, 200, 200), font=sub_font)

    # Save Hero
    hero_path = os.path.join(OUTPUT_DIR, "jonnyai-hero-fixed.png")
    bg.save(hero_path)
    print(f"Created Hero Logo: {hero_path}")

    # 2. Generate Navigation Icon (JAI)
    icon_w, icon_h = 512, 512
    icon_bg = Image.new("RGBA", (icon_w, icon_h), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon_bg)
    
    icon_font_size = 280
    icon_font = ImageFont.truetype(font_path, icon_font_size)
    
    icon_text = "JAI"
    it_w = icon_draw.textlength(icon_text, font=icon_font)
    it_x = (icon_w - it_w) // 2
    it_y = (icon_h - icon_font_size) // 2 - 40
    
    # Draw shadow
    # icon_draw.text((it_x+4, it_y+4), icon_text, fill=(0,0,0,100), font=icon_font)
    icon_draw.text((it_x, it_y), icon_text, fill=WHITE, font=icon_font)
    
    icon_path = os.path.join(OUTPUT_DIR, "jonnyai-icon.png")
    icon_bg.save(icon_path)
    print(f"Created Icon: {icon_path}")

    # 3. Generate Logo/Logo version (if components depend on it)
    logo_logo_dir = os.path.join(OUTPUT_DIR, "Logo")
    os.makedirs(logo_logo_dir, exist_ok=True)
    bg.save(os.path.join(logo_logo_dir, "JonnyAI_Logo_Transparent_Complete.png"))

if __name__ == "__main__":
    create_logo_assets()
