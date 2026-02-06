import requests
from bs4 import BeautifulSoup
import re

SITE_URL = "https://la-aesthetician.co.uk"

def deep_verify():
    print(f"Checking {SITE_URL}...")
    headers = {'Cache-Control': 'no-cache'}
    
    try:
        # 1. Check Hero Image Existence
        img_url = f"{SITE_URL}/images/hero-bg-new.jpg"
        r_img = requests.head(img_url, headers=headers)
        if r_img.status_code == 200:
            print(f"✅ Hero Image FOUND: {img_url}")
        else:
            print(f"❌ Hero Image MISSING: {img_url} ({r_img.status_code})")

        # 2. Check HTML for correct references
        r_html = requests.get(SITE_URL, headers=headers)
        html = r_html.text
        
        if "hero-bg-new.jpg" in html:
            print("✅ HTML references new hero image")
        else:
            print("❌ HTML references OLD hero image (or none)")
            
        if "libby.jpg" in html:
            print("✅ HTML references new libby image")
        else:
             print("❌ HTML references OLD libby image")

        if "bg-noise" in html:
            print("✅ HTML has 'bg-noise' class")
        else:
            print("❌ HTML missing 'bg-noise' class")

        # 3. Check CSS for color update
        soup = BeautifulSoup(html, 'html.parser')
        css_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
        
        found_color = False
        for css_link in css_links:
            if css_link.startswith('/'):
                css_url = f"{SITE_URL}{css_link}"
            else:
                css_url = css_link
                
            print(f"Checking CSS: {css_url}")
            r_css = requests.get(css_url, headers=headers)
            # Check for new coffee hex #654321
            if "#654321" in r_css.text:
                print("✅ CSS has NEW color palette (#654321)")
                found_color = True
                break
        
        if not found_color:
            print("❌ CSS still has OLD color palette")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deep_verify()
