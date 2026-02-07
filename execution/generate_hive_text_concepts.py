
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

# 5 MORE HIVE CONCEPTS - FOCUSED ON "MERGED WITH JONNYAI"
# Not just icons, but wordmark integrations.

# 1. HIVE REPLACEMENT FOR "O"
PROMPT_1 = "Logo concept for 'JonnyAI', where the letter 'O' in 'Jonny' is replaced by a glowing blue hexagon hive icon. Minimalist, modern sans serif font in black. Tech company branding. White background. centered"

# 2. HIVE DOT ON "i"
PROMPT_2 = "Logo concept for 'JonnyAI', where the dot on the 'i' in 'Ai' is a glowing blue hexagon. The rest of the text is sleek black. Minimalist. White background. centered"

# 3. HIVE BRIDGE
# Connecting Jonny and Ai.
PROMPT_3 = "Logo concept for 'JonnyAI'. The word 'Jonny' connects to 'Ai' via a bridge of small blue hexagonal cells. Digital transformation. Data flow. Black text. White background. centered"

# 4. HIVE CONTAINER
# "Jonny" inside a honeycomb structure.
PROMPT_4 = "Logo concept for 'JonnyAI'. The text 'JonnyAI' is encased within a long hexagonal frame. The frame is matte black with electric blue edges. Futuristic badge style. White background. centered"

# 5. ABSTRACT HIVE "J" (Refined)
# Trying again for a strong standalone icon that looks like a J made of cells.
PROMPT_5 = "Logo icon for 'JonnyAI'. Concept: Digital Hive J. A vertical column of black hexagons that curves at the bottom to form a J. The bottom-most hexagon is glowing cyan. Data structure. White background. centered"

prompts = [
    {"name": "hive_text_o_replace.png", "prompt": PROMPT_1},
    {"name": "hive_text_i_dot.png", "prompt": PROMPT_2},
    {"name": "hive_text_bridge.png", "prompt": PROMPT_3},
    {"name": "hive_text_container.png", "prompt": PROMPT_4},
    {"name": "hive_j_vertical.png", "prompt": PROMPT_5}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 5 MORE HIVE/TEXT INTEGRATIONS ---")

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
