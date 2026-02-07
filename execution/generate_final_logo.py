
import os
import requests
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. ICON GENERATION
# "Obsidian Prism" + "Electric Blue Core" + "Subtle White Outline Glow"
PROMPT_ICON = "Logo icon for 'JonnyAI'. Concept: Obsidian Prism J. A floating obsidian black crystal shard shaped like an abstract letter 'J'. Glowing Electric Blue neon core. Subtle white outer glow halo. Black background. High contrast. 8k, photorealistic, cinematic lighting. centered"
FILENAME_ICON = "prism_j_glow.png"

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- 1. GENERATING REFINED ICON: {FILENAME_ICON} ---")
image_bytes = None
response = query(API_URL, {"inputs": PROMPT_ICON})
if response and response.status_code == 200:
    image_bytes = response.content
    with open(os.path.join(OUTPUT_DIR, FILENAME_ICON), "wb") as f:
        f.write(image_bytes)
    print("✅ Icon Generated.")
else:
    print("❌ Failed to generate icon. Using previous if available?")

# 2. COMPOSITING WITH "ELECTRIC" TEXT
if image_bytes:
    print("--- 2. COMPOSITING LOGO WITH GLOWING TEXT ---")
    
    # Load Icon
    icon = Image.open(io.BytesIO(image_bytes))
    
    # Create black canvas (since logo is dark/glowing)
    W, H = 1400, 600
    canvas = Image.new("RGB", (W, H), "black")
    
    # Resize Icon
    icon_size = 450
    icon_resized = icon.resize((icon_size, icon_size))
    # Paste icon (centered vertically, left side)
    canvas.paste(icon_resized, (50, (H - icon_size) // 2))
    
    # Setup Fonts
    draw = ImageDraw.Draw(canvas)
    try:
        font_path = r"C:\Windows\Fonts\arialbd.ttf" # Bold sans-serif
        if not os.path.exists(font_path):
             font_path = "arial.ttf"
        font_size = 140
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
    
    # Text positions
    # "Jonny"
    text_x = 500
    text_y = (H - font_size) // 2 - 20 # Optical adjustments
    
    draw.text((text_x, text_y), "Jonny", fill="white", font=font)
    
    # "Ai" - THE ELECTRIC PART
    # We will draw "Ai" with a glow effect manually
    jonny_len = draw.textlength("Jonny", font=font)
    ai_x = text_x + jonny_len + 10
    
    # Create a separate layer for the glow
    glow_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # The "Electric Blue" color from the prompt (Cyan/Blue)
    ELECTRIC_BLUE = "#00FFFF" # Cyan/Electric Blue
    ELECTRIC_CORE = "#FFFFFF" # White hot center
    
    # Draw broad blur (Glow)
    for offset in range(10):
        glow_draw.text((ai_x, text_y), "Ai", fill=ELECTRIC_BLUE, font=font)
    
    # Apply blur to this layer
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))
    
    # Draw distinct "Ai" on top of the blur
    # Slightly bright blue/white center for "Neon" effect
    draw_layer = Image.new("RGBA", (W, H), (0,0,0,0))
    draw_draw = ImageDraw.Draw(draw_layer)
    draw_draw.text((ai_x, text_y), "Ai", fill=ELECTRIC_BLUE, font=font)
    
    # Composite: Canvas + Glow + Text
    canvas.paste(glow_layer, (0,0), mask=glow_layer) # Add Glow
    canvas.paste(draw_layer, (0,0), mask=draw_layer) # Add Text
    
    # Save
    FILENAME_FULL = "jonnyai_final_electric.png"
    save_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
    canvas.save(save_path)
    print(f"✅ SUCCESS! Saved final electric logo to: {save_path}")

else:
    print("Skipping composite due to missing icon.")
