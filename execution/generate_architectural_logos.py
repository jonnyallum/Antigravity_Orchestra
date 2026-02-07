
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

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# NEW APPROACH: ABSTRACT "INTELLIGENCE STRATA"
# Moving away from "Monolith/Box".
# Focus: LAYERS of intelligence. Construction. Geological strata but digital.
PROMPT_1 = "Logo icon for 'JonnyAI'. Concept: Digital Strata. Three stacked, floating horizontal plates. The bottom is obsidian black, the middle is dark grey, the top is glowing Electric Blue. Minimalist, architectural, structural engineering vibe. Isometric view. White background. No text. centered"

# NEW APPROACH: THE "KEYSTONE"
# Focus: The central piece that holds it all together.
PROMPT_2 = "Logo icon for 'JonnyAI'. Concept: The Keystone. A heavy, black geometric arch with a single glowing Electric Cyan keystone at the center. Architectural, strong, stable. Represents building/structure. Minimalist vector. White background. centered"

# NEW APPROACH: THE "HYPER-CUBE" FRAME
# Focus: Wireframe precision.
PROMPT_3 = "Logo icon for 'JonnyAI'. Concept: Hyperframe. A wireframe cube where the edges are thick matte black, and the internal core is a suspended sphere of glowing Electric Violet light. Technical drawing aesthetic. Precision engineering. White background. centered"

prompts = [
    {"name": "strata_layers.png", "prompt": PROMPT_1},
    {"name": "keystone_arch.png", "prompt": PROMPT_2},
    {"name": "hyperframe_cube.png", "prompt": PROMPT_3}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 3 FRESH ARCHITECTURAL CONCEPTS ---")

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
