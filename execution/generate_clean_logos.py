
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# COLORS
BLACK_BG = (0, 0, 0)
WHITE = (255, 255, 255)
ELECTRIC_BLUE = (0, 240, 255) # Cyan/Electric
DEEP_BLUE = (20, 20, 40)

# CANVAS
W, H = 1600, 600

# FONT LOADING - Target "Outfit" / "Inter" style (Geometric Sans)
def load_font(size):
    try:
        # Montserrat or Segoe UI are good geometric sans proxies
        return ImageFont.truetype(r"C:\Windows\Fonts\Montserrat-Bold.ttf", size)
    except:
        try:
             return ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf", size)
        except:
             return ImageFont.load_default()

# V6: PURE TYPOGRAPHY (The "Stripe" approach)
# Clean "Jonny" + Electric "Ai". No icons. Just perfect type.
def generate_v6():
    img = Image.new("RGB", (W, H), BLACK_BG)
    draw = ImageDraw.Draw(img)
    
    font = load_font(220)
    
    # Text
    text = "Jonny"
    w = draw.textlength(text, font=font)
    
    # Center X calculation
    total_w = w + draw.textlength("Ai", font=font)
    start_x = (W - total_w) // 2
    y = (H - 220) // 2
    
    # Jonny
    draw.text((start_x, y), text, fill=WHITE, font=font)
    
    # Ai (Electric)
    ai_x = start_x + w
    # Glow
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(10):
        gdraw.text((ai_x, y), "Ai", fill=ELECTRIC_BLUE, font=font)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=15))
    img.paste(glow, (0,0), mask=glow)
    
    draw.text((ai_x, y), "Ai", fill=ELECTRIC_BLUE, font=font)
    
    path = os.path.join(OUTPUT_DIR, "jonnyai_logo_v6_clean.png")
    img.save(path)
    print(f"✅ Generated V6: {path}")

# V7: THE INTEGRATED SPARK
# "Jonny" + [⚡] + "Ai". 
# Uses a simple vector spark/slash instead of a heavy icon.
def generate_v7():
    img = Image.new("RGB", (W, H), BLACK_BG)
    draw = ImageDraw.Draw(img)
    font = load_font(200)
    
    # Draw Spark (Manual Vector)
    spark_w = 60
    spark_h = 180
    
    text1 = "Jonny"
    text2 = "Ai"
    w1 = draw.textlength(text1, font=font)
    w2 = draw.textlength(text2, font=font)
    
    gap = 40
    total_w = w1 + gap + spark_w + gap + w2
    start_x = (W - total_w) // 2
    y = (H - 200) // 2
    
    # Jonny
    draw.text((start_x, y), text1, fill=WHITE, font=font)
    
    # Spark (Electric Blue Polygon)
    spark_x = start_x + w1 + gap
    spark_y = y + 20
    # Lightning shape
    points = [
        (spark_x + 40, spark_y), # Top Right
        (spark_x, spark_y + 80), # Middle Left
        (spark_x + 60, spark_y + 80), # Middle Right
        (spark_x + 20, spark_y + 160) # Bottom Left
    ]
    
    # Glow for spark
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.polygon(points, fill=ELECTRIC_BLUE)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=10))
    img.paste(glow, (0,0), mask=glow)
    
    draw.polygon(points, fill=ELECTRIC_BLUE)
    
    # Ai
    draw.text((spark_x + spark_w + gap, y), text2, fill=WHITE, font=font)
    
    path = os.path.join(OUTPUT_DIR, "jonnyai_logo_v7_spark.png")
    img.save(path)
    print(f"✅ Generated V7: {path}")

# V8: THE UNDERSCORE
# "JonnyAi" with a glowing electric underline under "Ai".
def generate_v8():
    img = Image.new("RGB", (W, H), BLACK_BG)
    draw = ImageDraw.Draw(img)
    font = load_font(200)
    
    text = "JonnyAi"
    w = draw.textlength(text, font=font)
    start_x = (W - w) // 2
    y = (H - 200) // 2
    
    # Draw all text White first
    draw.text((start_x, y), "Jonny", fill=WHITE, font=font)
    jonny_w = draw.textlength("Jonny", font=font)
    draw.text((start_x + jonny_w, y), "Ai", fill=WHITE, font=font)
    
    # Draw Underline under "Ai"
    ai_w = draw.textlength("Ai", font=font)
    line_x = start_x + jonny_w
    line_y = y + 210 # slightly below text
    line_h = 15
    
    # Glow Line
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rectangle((line_x, line_y, line_x + ai_w, line_y + line_h), fill=ELECTRIC_BLUE)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
    img.paste(glow, (0,0), mask=glow)
    
    draw.rectangle((line_x, line_y, line_x + ai_w, line_y + line_h), fill=ELECTRIC_BLUE)
    
    path = os.path.join(OUTPUT_DIR, "jonnyai_logo_v8_underline.png")
    img.save(path)
    print(f"✅ Generated V8: {path}")

if __name__ == "__main__":
    generate_v6()
    generate_v7()
    generate_v8()
