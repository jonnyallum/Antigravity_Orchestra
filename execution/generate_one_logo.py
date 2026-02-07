
import os
import requests
import time
import io
from PIL import Image
from dotenv import load_dotenv
import json

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# TRYING FLUX.1 SCHNELL ON ROUTER
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}" # Trying common router path var
# Backup URL if above fails
API_URL_2 = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# CONCEPT 2: ELECTRIC ARCHITECT - REFINED (More Definition)
PROMPT = "Logo icon for high-end AI studio 'JonnyAI', concept Electric Architect. Deep Midnight Blue background with a Cyan laser line forming an abstract 'J'. Cyberpunk 2077 high end. Glowing nodes. Ultra-sharp definition, crisp edges, intricate circuitry details, precision engineering, high fidelity, 8k resolution, vector style, sleek, neon. centered."
FILENAME = "electric_v2.png"

def query(url, payload):
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def attempt_generation():
    # Try Router First
    response = query(API_URL, {"inputs": PROMPT})
    
    if response and response.status_code != 200:
        print(f"Router failed ({response.status_code}), trying standard API...")
        response = query(API_URL_2, {"inputs": PROMPT})

    if not response:
        return None

    if response.status_code == 200:
        return response.content
    else:
        print(f"Final error: {response.text[:300]}")
        return None

print(f"--- GENERATING LOGO: {FILENAME} ---")
print(f"Prompt: {PROMPT}")

image_bytes = attempt_generation()

if image_bytes:
    try:
        # Check if it's actually JSON (error) disguised as 200 or just bytes
        try:
             # Look for common error json structure
             json_check = json.loads(image_bytes)
             if 'error' in json_check:
                 print(f"API Error JSON: {json_check['error']}")
                 image_bytes = None
        except:
             pass # Its valid bytes if json loads fails usually

        if image_bytes:
            image = Image.open(io.BytesIO(image_bytes))
            save_path = os.path.join(OUTPUT_DIR, FILENAME)
            image.save(save_path)
            print(f"✅ SUCCESS! Saved image to: {save_path}")
    except Exception as e:
        print(f"❌ Failed to parse image bytes: {e}")
else:
    print("❌ Failed to generate image.")
