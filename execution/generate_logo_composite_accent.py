
import os
import requests
import io
from PIL import Image, ImageDraw, ImageFont, ImageOps
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ACCENT COLOR: ELECTRIC COBALT / INDIGO
ACCENT_COLOR = "#4F46E5" # Indigo-600
ACCENT_NAME = "Cobalt"

PROMPT = f"Logo icon for high-end AI studio 'JonnyAI'. Concept: The Electric Monolith. Ultra-minimalist geometric abstract 'J' monogram. Matte black and {ACCENT_NAME} blue accent. High contrast. Architectural, sharp angles, fashion-tech aesthetic. White background. Vector style. No text. centered, 2d, flat"
FILENAME_ICON = "monolith_accent.png"
FILENAME_FULL = "monolith_full_accent.png"

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

print(f"--- RE-GENERATING ICON WITH ACCENT: {FILENAME_ICON} ---")
image_bytes = attempt_generation()

if image_bytes:
    # Save Icon
    icon = Image.open(io.BytesIO(image_bytes))
    save_path = os.path.join(OUTPUT_DIR, FILENAME_ICON)
    icon.save(save_path)
    
    # 2. COMPOSITE WITH ACCENT TEXT
    print("--- COMPOSITING TEXT ---")
    
    canvas_width = 1200
    canvas_height = 600
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    
    icon_size = 400
    icon_resized = icon.resize((icon_size, icon_size))
    canvas.paste(icon_resized, (100, (canvas_height - icon_size) // 2))
    
    draw = ImageDraw.Draw(canvas)
    
    try:
        font_path = "arialbd.ttf"
        possible_fonts = [
             r"C:\Windows\Fonts\arialbd.ttf",
             r"C:\Windows\Fonts\seguiemj.ttf",
             r"C:\Windows\Fonts\Roboto-Bold.ttf"
        ]
        for p in possible_fonts:
            if os.path.exists(p):
                font_path = p
                break
        font_main = ImageFont.truetype(font_path, 120)
    except:
        font_main = ImageFont.load_default()

    text_x = 550
    text_y = (canvas_height // 2) - 60
    
    # Draw "Jonny" in Black
    draw.text((text_x, text_y), "Jonny", fill="black", font=font_main)
    jonny_width = draw.textlength("Jonny", font=font_main)
    
    # Draw "AI" in New Accent Color
    draw.text((text_x + jonny_width, text_y), "AI", fill=ACCENT_COLOR, font=font_main)

    # Save Composite
    full_path = os.path.join(OUTPUT_DIR, FILENAME_FULL)
    canvas.save(full_path)
    print(f"✅ SUCCESS! Saved composite logo to: {full_path}")
else:
    print("❌ Failed to generate icon image.")
