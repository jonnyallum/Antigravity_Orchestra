
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

# ICON ON THE RIGHT - CLOSER INTEGRATION
# Both Hive J and Hive Sphere variations with icon positioned RIGHT of text

# Hive J Vertical - RIGHT SIDE
PROMPT_J1 = "Logo for 'JonnyAI'. Bold modern text 'JonnyAi' on the left where 'Ai' is electric blue. A vertical column of black hexagons forming a 'J' shape positioned very close to the right side. Bottom hexagon glows electric blue. Tight compact design. White background. centered"

PROMPT_J2 = "Logo for 'JonnyAI'. Text 'JonnyAi' in bold font with 'Ai' in electric blue, followed immediately by a vertical hexagon stack icon. Very close spacing, almost touching. Icon is black with bottom glowing blue. Professional tech logo. White background. centered"

PROMPT_J3 = "Logo for 'JonnyAI'. The text 'JonnyAi' where 'i' has a vertical hexagon column attached to its right side as the dot and stem. Hexagons are black with bottom one electric blue. Seamless integration. White background. centered"

# Hive Mind Sphere - RIGHT SIDE  
PROMPT_S1 = "Logo for 'JonnyAI'. Bold text 'JonnyAi' on the left with 'Ai' in electric blue. A sphere of small black hexagons with glowing blue core positioned very close to the right. Tight spacing. Professional tech branding. White background. centered"

PROMPT_S2 = "Logo for 'JonnyAI'. Text 'JonnyAi' in bold modern font where 'Ai' is electric blue, immediately followed by a small hexagonal sphere icon with blue energy core. Almost touching. Compact design. White background. centered"

prompts = [
    {"name": "hive_j_right_v1.png", "prompt": PROMPT_J1},
    {"name": "hive_j_right_v2.png", "prompt": PROMPT_J2},
    {"name": "hive_j_right_v3.png", "prompt": PROMPT_J3},
    {"name": "hive_s_right_v1.png", "prompt": PROMPT_S1},
    {"name": "hive_s_right_v2.png", "prompt": PROMPT_S2}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 5 RIGHT-SIDE LOGO CONCEPTS ---")
print("Icon positioned to the RIGHT of JonnyAi text")
print("Closer, tighter spacing")
print()

for item in prompts:
    print(f"Generating: {item['name']}...")
    try:
        response = query(API_URL, {"inputs": item['prompt']})
        if response and response.status_code == 200:
             image = Image.open(io.BytesIO(response.content))
             save_path = os.path.join(OUTPUT_DIR, item['name'])
             image.save(save_path)
             print(f"[OK] Saved to: {save_path}")
        else:
             print(f"[FAIL] Failed to generate {item['name']}")
    except Exception as e:
        print(f"[ERROR] {e}")

print("\nDone! Check the concepts folder.")
