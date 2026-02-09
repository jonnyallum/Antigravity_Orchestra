
import os

agents_dir = r"C:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\agents"
output_file = os.path.join(agents_dir, "audit_gallery.html")

files = [f for f in os.listdir(agents_dir) if f.endswith(".png")]
files.sort()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent Avatar Audit</title>
    <style>
        body { background: #030308; color: white; font-family: sans-serif; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; padding: 20px; }
        .card { background: #0a0b14; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #1e3a5f; }
        img { width: 100%; border-radius: 4px; height: 180px; object-fit: cover; }
        .filename { margin-top: 10px; font-size: 14px; word-break: break-all; color: #3b82f6; }
    </style>
</head>
<body>
    <h1>Agent Avatar Audit Gallery</h1>
    <div class="grid">
"""

for f in files:
    html += f"""
        <div class="card">
            <img src="{f}" alt="{f}">
            <div class="filename">{f}</div>
        </div>
    """

html += """
    </div>
</body>
</html>
"""

with open(output_file, "w") as f:
    f.write(html)

print(f"Gallery created at: {output_file}")
