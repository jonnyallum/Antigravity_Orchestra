import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Config
TMP_DIR = Path(r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\La-Aesthetician.co.uk\.tmp")
ASSETS_DIR = Path(r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\La-Aesthetician.co.uk\website\public\images\gallery")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def extracts_images():
    print(f"Scanning {TMP_DIR} for .htm files...")
    
    files = list(TMP_DIR.glob("*.htm"))
    if not files:
        print("No .htm files found!")
        return

    count = 0
    for file_path in files:
        print(f"Processing {file_path.name}...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try to find the main image (OpenGraph or first large image)
            img_url = None
            
            # 1. Try OG image
            og_image = soup.find("meta", property="og:image")
            if og_image:
                img_url = og_image.get("content")
                
            # 2. If no OG, try main image class (Instagram specific)
            if not img_url:
                # Common instagram image classes or structure
                img = soup.find("img", class_="x5yr21d") # Example class, likely unstable
                if img:
                    img_url = img.get("src")
            
            # 3. Fallback: First generic image that looks like a photo
            if not img_url:
                images = soup.find_all("img")
                for img in images:
                    src = img.get("src")
                    if src and "fbcdn" in src and "s150x150" not in src: # Filter out tiny thumbnails
                        img_url = src
                        break
            
            if img_url:
                print(f"Found image URL: {img_url[:50]}...")
                
                # Download
                try:
                    # Handle local file paths vs info
                    if img_url.startswith("data:"):
                        print("Skipping base64 for now")
                        continue
                        
                    response = requests.get(img_url, timeout=10)
                    if response.status_code == 200:
                        count += 1
                        ext = "jpg"
                        if "png" in img_url: ext = "png"
                        
                        save_path = ASSETS_DIR / f"insta-real-{count}.{ext}"
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        print(f"✅ Saved to {save_path.name}")
                    else:
                        print(f"❌ Failed to download (Status {response.status_code})")
                except Exception as e:
                    print(f"❌ Error downloading: {e}")
            else:
                print("No suitable image found in file.")

        except Exception as e:
            print(f"Error processing file: {e}")

    print(f"\nDone! Extracted {count} images.")

if __name__ == "__main__":
    extracts_images()
