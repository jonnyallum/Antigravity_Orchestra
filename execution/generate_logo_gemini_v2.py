
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)

OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\jonnyai.website\public\concepts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

prompts = [
    {
        "name": "concept_1_monolith",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI'. Concept: The Monolith. Ultra-minimalist geometric abstract 'J' monogram. Matte black and gloss white only. High contrast. Architectural, sharp angles, fashion-tech aesthetic. White background. Vector style. No text."
    },
    {
        "name": "concept_2_electric",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI'. Concept: The Electric Architect. Deep Midnight Blue background with a single Cyan laser line forming an abstract 'J'. Cyberpunk 2077 high end. Glowing nodes. Minimalist."
    },
    {
        "name": "concept_3_platinum",
        "prompt": "Logo icon for high-end AI studio 'JonnyAI'. Concept: Platinum Standard. Liquid Silver chrome 3D abstract 'J' shape on black background. Industrial luxury, Rolex aesthetic. Brushed metal texture. Macro photography."
    }
]

print("Attempting generation with Gemini Imagen 3...")

try:
    # Try getting the model (this class might not exist in older versions of the SDK)
    # If this fails, we catch it.
    model = genai.ImageGenerationModel("imagen-3.0-generate-001")
    
    for item in prompts:
        print(f"Generating {item['name']}...")
        try:
            response = model.generate_images(
                prompt=item['prompt'],
                number_of_images=1,
            )
            save_path = os.path.join(OUTPUT_DIR, f"{item['name']}.png")
            response[0].save(save_path)
            print(f"Saved to {save_path}")
        except Exception as e:
            print(f"Failed to generate {item['name']}: {e}")

except AttributeError:
    print("genai.ImageGenerationModel not found. SDK might be too old or not support this.")
except Exception as e:
    print(f"Model initialization failed: {e}")

print("Done.")
