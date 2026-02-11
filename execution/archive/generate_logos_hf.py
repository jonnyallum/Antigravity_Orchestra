
import os
import requests
import io
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# Using SDXL Base 1.0 which is usually reliable on Inference API
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

prompts = [
    {
        "name": "concept_1_monolith",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI', concept The Monolith. Ultra-minimalist geometric abstract 'J' monogram. Matte black and gloss white only. High contrast. Architectural, sharp angles, fashion-tech aesthetic. White background. Vector style. No text. centered, 2d, flat"
    },
    {
        "name": "concept_2_electric",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI', concept The Electric Architect. Deep Midnight Blue background with a single Cyan laser line forming an abstract 'J'. Cyberpunk 2077 high end. Glowing nodes. Minimalist. centered, 8k resolution"
    },
    {
        "name": "concept_3_platinum",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI', concept Platinum Standard. Liquid Silver chrome 3D abstract 'J' shape on black background. Industrial luxury, Rolex aesthetic. Brushed metal texture. Macro photography. centered, photorealistic"
    }
]

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

print(f"Generating {len(prompts)} logo concepts using SDXL-base-1.0...")

for item in prompts:
    print(f"Generating: {item['name']}...")
    try:
        image_bytes = query({"inputs": item['prompt']})
        # Check if error or wait time
        try:
            import json
            err = json.loads(image_bytes)
            if 'error' in err:
                print(f"Error generating {item['name']}: {err['error']}")
                import time
                if 'estimated_time' in err:
                    wait_time = err['estimated_time']
                    print(f"Model loading, waiting {wait_time}s...")
                    time.sleep(wait_time + 5)
                    # Retry once
                    image_bytes = query({"inputs": item['prompt']})
        except:
            pass # Not JSON, likely image data

        image = Image.open(io.BytesIO(image_bytes))
        save_path = os.path.join(OUTPUT_DIR, f"{item['name']}.png")
        image.save(save_path)
        print(f"Saved to {save_path}")
    except Exception as e:
        print(f"Failed to process {item['name']}: {e}")

print("Done.")
