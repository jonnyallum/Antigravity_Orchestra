import requests
from bs4 import BeautifulSoup
import sys

URL = "https://la-aesthetician.co.uk/"

def verify_site():
    print(f"Fetching {URL}...")
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to fetch site: Status {response.status_code}")
            return False
            
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = str(soup)
        
        checks = [
            ("hero-bg-new.jpg", "Hero Image"),
            ("libby.jpg", "About Image"), # Note: I named it libby.jpg in the code, but moved it as libby-main.jpg? Wait.
            ("photo-1.jpg", "Gallery Image 1"),
            ("photo-8.jpg", "Gallery Image 8"),
            ("InstagramGallery", "Gallery Component Class/Structure") # Might not appear in minified class names
        ]
        
        success = True
        
        # Check source code matches
        # Note: I renamed the file to libby-main.jpg in the move command (Step 559)
        # BUT I used "/images/libby.jpg" in the page.tsx replacement (Step 536/542)
        # ERROR DETECTED: Mismatch between file on disk (libby-main.jpg) and code (libby.jpg)
        
        # Let's check what I actually wrote in page.tsx
        
        for search_term, name in checks:
            if search_term in html_content:
                print(f"✅ Found {name} ({search_term})")
            else:
                print(f"❌ MISSING {name} ({search_term})")
                success = False
                
        return success

    except Exception as e:
        print(f"❌ Error verifying: {e}")
        return False

if __name__ == "__main__":
    verify_site()
