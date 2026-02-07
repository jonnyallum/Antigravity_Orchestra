
import os
import requests
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. PRISM ICON (CLEAN VECTOR)
# Focusing on making it a usable LOGO, not just a picture.
PROMPT_1 = "Logo icon for 'JonnyAI'. Concept: Obsidian Prism. A minimalist, perfect black triangle prism on a white background. A single beam of sharp light hits it and refracts into a spectrum of digital blue and violet data streams. Vector style, flat, clean lines, high contrast app icon."

# 2. THE MONOLITH "J" PRISM
# Integrating the Brand Name.
PROMPT_2 = "Logo icon for 'JonnyAI'. Concept: Monolith J. A tall, obsidian black crystal shard shaped like an abstract letter 'J'. It is glowing from within with a faint electric indigo pulse. Cinematic lighting, black background, mysterious, high-tech, futuristic structure."

# 3. DATA REFRACTION (CINEMATIC)
# The "World Class" high-concept art.
PROMPT_3 = "Logo icon for 'JonnyAI'. Concept: Data Prism. A macro close-up of a black glass cube. A beam of white light enters and explodes into thousands of binary code strings and fiber optic glowing lines. Cyberpunk luxury. 8k, photorealistic, octane render."

prompts = [
    {"name": "prism_vector_icon.png", "prompt": PROMPT_1},
    {"name": "prism_monolith_j.png", "prompt": PROMPT_2},
    {"name": "prism_data_stream.png", "prompt": PROMPT_3}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING OBSIDIAN PRISM VARIATIONS ---")
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
