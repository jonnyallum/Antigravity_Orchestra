
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

# THE 5 VECTORS OF "INTELLIGENCE"
# We need to find the shape of "Intelligence Amplified".

# 1. THE ASCENSION STAIRS
# Building upwards. Progress.
PROMPT_1 = "Logo icon for 'JonnyAI'. Concept: Ascension. Three black abstract steps or blocks rising diagonally. The top step is glowing Electric Blue. Minimalist vector. Growth. Progress. White background. centered"

# 2. THE CIRCUIT NODE
# Connection. Central point.
PROMPT_2 = "Logo icon for 'JonnyAI'. Concept: The Node. A central black sphere connected to three orbiting smaller spheres by thin lines. One connection is glowing Electric Blue. Network. System. White background. centered"

# 3. THE INFINITY LOOP (Technical)
# Endless capability.
PROMPT_3 = "Logo icon for 'JonnyAI'. Concept: Technical Infinity. A sharp, angular infinity symbol (figure 8). One half is matte black, the other half is wireframe Electric Blue. Continuous loop. Engineering. White background. centered"

# 4. THE HEXAGON HIVE
# The Agent Orchestra.
PROMPT_4 = "Logo icon for 'JonnyAI'. Concept: The Hive. A hexagon made of smaller triangles. One triangle is missing/popped out and glowing Electric Blue. Modular. Organized. White background. centered"

# 5. THE SPARK GAP
# Energy jumping between points.
PROMPT_5 = "Logo icon for 'JonnyAI'. Concept: Spark Gap. Two black vertical monoliths with a bright Electric Blue lightning bolt arcing between them. Energy. Transmission. Power. White background. centered"


prompts = [
    {"name": "concept_ascension.png", "prompt": PROMPT_1},
    {"name": "concept_node.png", "prompt": PROMPT_2},
    {"name": "concept_infinity.png", "prompt": PROMPT_3},
    {"name": "concept_hive.png", "prompt": PROMPT_4},
    {"name": "concept_spark.png", "prompt": PROMPT_5}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 5 NEW LOGO DIRECTIONS ---")

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
