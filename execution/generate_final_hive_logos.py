
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

# 5 CONCEPTS: HIVE J VERTICAL + JONNYAI TEXT MERGE
PROMPT_J1 = "Complete logo for 'JonnyAI'. A vertical column of black hexagons forming a 'J' shape positioned to the left. The bottom hexagon glows electric blue. Next to it, modern bold text 'onnyAi' where 'Ai' is electric blue. Professional tech logo. White background. centered"

PROMPT_J2 = "Logo for 'JonnyAI'. The letter 'J' in 'Jonny' is replaced by a vertical stack of black hexagonal cells with the bottom one glowing electric blue. Rest of text 'onnyAi' in sleek black, with 'Ai' in electric blue. White background. centered"

PROMPT_J3 = "Logo for 'JonnyAI'. Text 'JonnyAi' in bold modern font where the 'J' has a honeycomb pattern texture. The bottom of the 'J' glows electric blue. Rest of text black except 'Ai' which is electric blue. White background. centered"

PROMPT_J4 = "Logo for 'JonnyAI'. A vertical hexagon column 'J' icon sits close to the left of text 'JonnyAi'. Tight integration. Icon is black with blue glow at base. Text is bold, 'Ai' in electric blue. Compact design. White background. centered"

PROMPT_J5 = "Logo for 'JonnyAI'. The word 'Jonny' with a vertical hexagon stack forming the descender of the 'y'. Then 'Ai' in electric blue next to it. Hexagons are black with bottom one glowing blue. Seamless merge. White background. centered"

# 5 CONCEPTS: HIVE MIND SPHERE + JONNYAI TEXT MERGE
PROMPT_S1 = "Logo for 'JonnyAI'. A sphere made of small black hexagons with electric blue core positioned left. Text 'JonnyAi' to the right in bold modern font. 'Ai' is electric blue. Professional layout. White background. centered"

PROMPT_S2 = "Logo for 'JonnyAI'. The letter 'o' in 'Jonny' is replaced by a sphere of small hexagons with glowing blue center. Rest of text 'JnnyAi' where 'Ai' is electric blue. Tech branding. White background. centered"

PROMPT_S3 = "Logo for 'JonnyAI'. Text 'JonnyAi' where the dot on the 'i' is a small hexagonal sphere with blue energy core. Bold modern typeface, 'Ai' in electric blue. Minimalist. White background. centered"

PROMPT_S4 = "Logo for 'JonnyAI'. A hexagon sphere icon sits behind text 'JonnyAi', partially visible on the left edge. Creates depth. Text is bold black with 'Ai' in electric blue. Layered design. White background. centered"

PROMPT_S5 = "Logo for 'JonnyAI'. Text 'JonnyAi' with a hexagonal sphere positioned between 'Jonny' and 'Ai', acting as a separator. Sphere is black cells with blue glow. Modern tech logo. White background. centered"

prompts = [
    {"name": "hive_j_v1_classic.png", "prompt": PROMPT_J1},
    {"name": "hive_j_v2_replace_j.png", "prompt": PROMPT_J2},
    {"name": "hive_j_v3_texture.png", "prompt": PROMPT_J3},
    {"name": "hive_j_v4_tight.png", "prompt": PROMPT_J4},
    {"name": "hive_j_v5_descender.png", "prompt": PROMPT_J5},
    {"name": "hive_s_v1_classic.png", "prompt": PROMPT_S1},
    {"name": "hive_s_v2_replace_o.png", "prompt": PROMPT_S2},
    {"name": "hive_s_v3_i_dot.png", "prompt": PROMPT_S3},
    {"name": "hive_s_v4_layered.png", "prompt": PROMPT_S4},
    {"name": "hive_s_v5_separator.png", "prompt": PROMPT_S5}
]

def query(url, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

print(f"--- GENERATING 10 FINAL HIVE LOGO CONCEPTS ---")
print("5x Hive J Vertical + JonnyAI")
print("5x Hive Mind Sphere + JonnyAI")
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
