
import os
import requests
import time
import io
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. GENERATE THE ICON AGAIN (or could load existing, but let's regenerate for variations)
PROMPT = "Logo design for high-end AI studio 'JonnyAI'. Ultra-minimalist geometric abstract 'J' monogram icon. Matte black and gloss white only. High contrast. Architectural, sharp angles, fashion-tech aesthetic. White background. Vector style. No text. centered, 2d, flat"
FILENAME_ICON = "monolith_icon.png"
FILENAME_FULL = "monolith_full.png"

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def attempt_generation():
    response = query(API_URL, {"inputs": PROMPT})
    if response and response.status_code == 200:
        return response.content
    return None

print(f"--- RE-GENERATING ICON FOR COMPOSITION: {FILENAME_ICON} ---")
image_bytes = attempt_generation()

if image_bytes:
    # Save Icon
    icon = Image.open(io.BytesIO(image_bytes))
    save_path = os.path.join(OUTPUT_DIR, FILENAME_ICON)
    icon.save(save_path)
    
    # 2. COMPOSITE WITH TEXT 'JonnyAI'
    print("--- COMPOSITING TEXT ---")
    
    # Create canvas
    canvas_width = 1200
    canvas_height = 600
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    
    # Resize and paste icon on left
    icon_size = 400
    icon_resized = icon.resize((icon_size, icon_size))
    # Center vertically, left aligned with padding
    canvas.paste(icon_resized, (100, (canvas_height - icon_size) // 2))
    
    # Add Text on right
    draw = ImageDraw.Draw(canvas)
    
    # Try to load a font, otherwise default
    try:
        # Looking for a bold/modern font on Windows
        font_path = "arialbd.ttf" # Fallback
        # Just trying common paths
        possible_fonts = [
             r"C:\Windows\Fonts\arialbd.ttf",
             r"C:\Windows\Fonts\seguiemj.ttf", # Segoe UI
             r"C:\Windows\Fonts\Roboto-Bold.ttf"
        ]
        for p in possible_fonts:
            if os.path.exists(p):
                font_path = p
                break
                
        font_main = ImageFont.truetype(font_path, 120)
    except:
        font_main = ImageFont.load_default()

    # Draw "Jonny" in Black
    text_x = 550
    text_y = (canvas_height // 2) - 60
    draw.text((text_x, text_y), "Jonny", fill="black", font=font_main)
    
    # Measure 'Jonny' width approx to place 'AI'
    jonny_width = draw.textlength("Jonny", font=font_main)
    
    # Draw "AI" in Black (Monochrome theme means NO orange)
    draw.text((text_x + jonny_width, text_y), "AI", fill="black", font=font_main)

    # Save Composite
    full_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
    canvas.save(full_path)
    print(f"✅ SUCCESS! Saved composite logo to: {full_path}")

else:
    print("❌ Failed to generate icon image.")
