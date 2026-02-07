"""
Fetch all sheets from the Manor Barn HACCP Logbook Google Spreadsheet.
Downloads each sheet by trying common GID values and saves as CSV.
"""
import urllib.request
import os
import time

SPREADSHEET_ID = "1J3kHdpXVrHanUPpJd_szHxqNHW1GOkyi0mvAf3lnyrc"
OUTPUT_DIR = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.tmp\haccp_sheets"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try to get the HTML page first to find sheet GIDs
html_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit"

# Try common GID patterns - sheets often use sequential or specific GIDs
# GID 0 is always the first sheet
gids_to_try = [0] + list(range(1, 20)) + [
    # Common auto-generated GIDs
    100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
    1234567890, 987654321,
    # Try some larger numbers that Google often uses
    2000, 3000, 4000, 5000,
    111, 222, 333, 444, 555, 666, 777, 888, 999,
    1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999,
    # More common patterns
    123456789, 1234567, 12345678,
    2050, 2051, 2052, 2053, 2054, 2055,
    1050, 1051, 1052, 1053, 1054, 1055,
]

# First, let's try to get the HTML to extract actual GIDs
print("Attempting to fetch spreadsheet HTML to find sheet GIDs...")
try:
    req = urllib.request.Request(
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/pubhtml",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    response = urllib.request.urlopen(req, timeout=15)
    html = response.read().decode('utf-8', errors='replace')
    
    # Save HTML for analysis
    html_path = os.path.join(OUTPUT_DIR, "spreadsheet.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved HTML to {html_path}")
    
    # Extract GIDs from the HTML
    import re
    gid_matches = re.findall(r'gid=(\d+)', html)
    if gid_matches:
        found_gids = list(set(int(g) for g in gid_matches))
        print(f"Found GIDs in HTML: {found_gids}")
        gids_to_try = found_gids
    
    # Also look for sheet names
    sheet_names = re.findall(r'<li[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL)
    if sheet_names:
        print(f"Found sheet names: {sheet_names}")
        
except Exception as e:
    print(f"Could not fetch HTML: {e}")
    print("Falling back to brute-force GID discovery...")

# Now download each sheet as CSV
print(f"\nDownloading sheets for {len(gids_to_try)} GIDs...")
successful = []

for gid in gids_to_try:
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={gid}"
    output_path = os.path.join(OUTPUT_DIR, f"sheet_gid_{gid}.csv")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15)
        data = response.read()
        
        # Check if it's actually CSV data (not an error page)
        text = data.decode('utf-8', errors='replace')
        if len(text) > 10 and not text.startswith('<!DOCTYPE'):
            with open(output_path, 'wb') as f:
                f.write(data)
            # Get first line as preview
            first_line = text.split('\n')[0][:100]
            print(f"  GID {gid}: OK ({len(data)} bytes) - {first_line}")
            successful.append((gid, output_path, first_line))
        else:
            pass  # Skip HTML error pages
    except Exception as e:
        pass  # Skip failed downloads
    
    time.sleep(0.3)  # Be polite

print(f"\n=== Successfully downloaded {len(successful)} sheets ===")
for gid, path, preview in successful:
    print(f"  GID {gid}: {preview}")
