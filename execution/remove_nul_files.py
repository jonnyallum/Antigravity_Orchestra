import os
import shutil

paths = [
    r"c:\Users\jonny\Desktop\AgOS 3.0 template\nul",
    r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\Poundtrades.app-antigravity\poundtrades-v2\nul"
]

for p in paths:
    # Use the extended path prefix for Windows to handle reserved names
    extended_p = "\\\\?\\" + p
    try:
        if os.path.exists(extended_p):
            os.remove(extended_p)
            print(f"Successfully removed {p}")
        else:
            print(f"File {p} does not exist (already gone?)")
    except Exception as e:
        print(f"Error removing {p}: {e}")
