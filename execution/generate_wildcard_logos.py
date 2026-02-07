
import os
import requests
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# THE NEW VISION: "THE QUANTUM ARCHITECT"
# We're going DEEP. Dark. Mysterious. Highly technical.
# Color: ELECTRIC VIOLET / CYBER TINT.
PROMPT_1 = "Logo icon for 'JonnyAI'. Concept: Quantum Architect. A floating, impossible geometric cube or hyper-shape in the center. Glowing Electric Violet core. Matte black outer shell. Levitating above a surface. Cinematic lighting. 8k, photorealistic, octane render, unreal engine 5 style. No text. centered"

# THE NEW VISION: "THE LIQUID NEURAL NETWORK"
# Organic but metallic. T-1000 vibes.
# Color: LIQUID SILVER / QUICKSILVER.
PROMPT_2 = "Logo icon for 'JonnyAI'. Concept: Liquid Neural Network. A drop of liquid silver or chrome that is morphing into a digital grid pattern as it hits the ground. High-speed photography. Metallic sheen. Black background. centered, photorealistic, 8k"

# THE NEW VISION: "THE OBSIDIAN PRISM"
# Light refraction. Beams.
# Color: DARK GLASS / RAINBOW REFRACTION.
PROMPT_3 = "Logo icon for 'JonnyAI'. Concept: Obsidian Prism. A sharp, black triangular prism refracting a single beam of pure white light into a digital data stream. Pink floyd vibes but cyberpunk. High contrast. Black background. centered, 8k"

prompts = [
    {"name": "quantum_architect.png", "prompt": PROMPT_1},
    {"name": "liquid_neural.png", "prompt": PROMPT_2},
    {"name": "obsidian_prism.png", "prompt": PROMPT_3}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 3 NEW HIGH-IMAGINATION CONCEPTS ---")

for item in prompts:
    print(f"Generating: {item['name']}...")
    try:
        response = query(API_URL, {"inputs": item['prompt']})
        if response and response.status_code == 200:
             image = Image.open(io.BytesIO(response.content))
             save_path = os.path.join(OUTPUT_DIR, item['name'])
             image.save(save_path)
             print(f"✅ Saved to: {save_path}")
        else:
             print(f"❌ Failed to generate {item['name']}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("Done.")
