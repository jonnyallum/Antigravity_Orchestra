
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

# THE HIVE - ITERATIONS
# Focus: Hexagons, Swarms, Orchestration.
# Color: Matte Black & Electric Blue.

# 1. HIVE J
# The shape of the letter J formed by hexagonal cells.
PROMPT_1 = "Logo icon for 'JonnyAI'. Concept: Hive J. The letter 'J' constructed from interconnected black hexagonal cells. The top cell is glowing Electric Cyan. Tech, biological, organized. Minimalist vector on white background. centered"

# 2. THE CORE CELL
# A single, powerful processing unit.
PROMPT_2 = "Logo icon for 'JonnyAI'. Concept: Core Cell. A single, perfect black hexagon with a glowing Electric Blue innovative circuit core being revealed. High-tech, precision, processor. Isometric view. White background. centered"

# 3. THE CLUSTER (Orchestra)
# Agents working together.
PROMPT_3 = "Logo icon for 'JonnyAI'. Concept: The Cluster. Three interlocking hexagons. Two are matte black, one is glowing Electric Blue. Representation of AI agents collaborating. Geometric, flat, vector logo. White background. centered"

# 4. HIVE MIND (Abstract)
# Network density.
PROMPT_4 = "Logo icon for 'JonnyAI'. Concept: Hive Mind. A dense sphere made of small black hexagons, with a bright blue light emanating from within. Digital swarm. Complex but organized. White background. centered"

prompts = [
    {"name": "hive_j_letter.png", "prompt": PROMPT_1},
    {"name": "hive_core_cell.png", "prompt": PROMPT_2},
    {"name": "hive_cluster.png", "prompt": PROMPT_3},
    {"name": "hive_mind_sphere.png", "prompt": PROMPT_4}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING HIVE CONCEPT ITERATIONS ---")

for item in prompts:
    print(f"Generating: {item['name']}...")
    try:
        response = query(API_URL, {"inputs": item['prompt']})
        if response and response.status_code == 200:
             image = Image.open(io.BytesIO(response.content))
             save_path = os.path.join(OUTPUT_DIR, item['name'])
             image.save(save_path)
             # Also save a black BG version for quick check? No need, white bg is better for shape checking.
             print(f"✅ Saved to: {save_path}")
        else:
             print(f"❌ Failed to generate {item['name']}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("Done.")
