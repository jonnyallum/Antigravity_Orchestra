
import os
import shutil

agents_dir = r"C:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website\public\agents"

# Mapping: Target Filename -> Current Potential Filenames (best first)
mapping = {
    "keith.png": ["dup3.png"],
    "patrick.png": ["dup2.png", "patrick.png"],
    "pixel.png": ["priya.png", "pixel.png"],
    "devops.png": ["derek.png", "devops.png"],
    "datastore.png": ["diana.png", "datastore.png"],
    "vaultguard.png": ["victor.png", "vaultguard.png"],
    "autoflow.png": ["alex.png", "autoflow.png"],
    "goldie.png": ["grace.png", "goldie.png"],
    "echo.png": ["elena.png", "echo.png"],
    "metric.png": ["maya.png", "metric.png"],
    "helpline.png": ["hannah.png", "helpline.png"],
    "counsel.png": ["luna.png", "counsel.png"],
    "scout.png": ["sophie.png", "scout.png"],
    "clippers.png": ["carlos.png", "clippers.png"],
    "manus.png": ["mason.png", "manus.png"],
    "warehouse.png": ["winston.png", "warehouse.png"],
    "sterling.png": ["julian.png", "sterling.png"],
    "julian.png": ["quinn.png", "julian.png"], # Julian Grave uses the 'Doctor' image (quinn.png)
    "quinn.png": ["dup4.png"], # Give Quinn Masters a distinct look if dup4 is available
    "conductor.png": ["marcus.png", "conductor.png"],
    "deploy.png": ["owen.png", "deploy.png"],
    "sentinel.png": ["sam.png", "sentinel.png"],
    "archivist.png": ["arthur.png", "archivist.png"],
    "female_reserve.png": ["dup1.png"]
}

# Step 1: Quality Check for Marcus
marcus_files = ["marcus 3.png", "marcus.png", "conductor.png"]
best_marcus = None
for f in marcus_files:
    path = os.path.join(agents_dir, f)
    if os.path.exists(path):
        if not best_marcus or os.path.getsize(path) > os.path.getsize(os.path.join(agents_dir, best_marcus)):
            best_marcus = f

if best_marcus:
    print(f"Selecting {best_marcus} as Conductor (Highest quality)")
    shutil.copy2(os.path.join(agents_dir, best_marcus), os.path.join(agents_dir, "conductor.png"))

# Step 2: Quality Check for Other Swaps
for target, sources in mapping.items():
    if target == "conductor.png": continue # Handled above
    
    best_source = None
    for src in sources:
        path = os.path.join(agents_dir, src)
        if os.path.exists(path):
            if not best_source or os.path.getsize(path) > os.path.getsize(os.path.join(agents_dir, best_source)):
                best_source = src
    
    if best_source:
        target_path = os.path.join(agents_dir, target)
        source_path = os.path.join(agents_dir, best_source)
        if target_path.lower() != source_path.lower():
            print(f"Moving {best_source} to {target}")
            shutil.copy2(source_path, target_path)
        else:
            print(f"Skipping identical move: {best_source} -> {target}")

# Step 3: Cleanup
ids = ["conductor", "keith", "quinn", "archivist", "lyra", "pixel", "sebastian", "sentinel", "datastore", "vaultguard", "vigil", "devops", "deploy", "autoflow", "forge", "goldie", "echo", "metric", "helpline", "counsel", "vivienne", "scout", "parser", "clippers", "rowan", "manus", "nina", "genesis", "warehouse", "daniel", "sterling", "gareth", "harry", "pietro", "julian", "terry", "monte"]
final_names = {i + ".png" for i in ids} | {"female_reserve.png"}

# Files to explicitly preserve even if not in IDs (yet)
preserve = {"dup5.png", "dup6.png", "dup7.png", "dup8.png", "dup9.png", "dup10.png"}
final_names |= preserve

print("Final files to keep:", final_names)

for f in os.listdir(agents_dir):
    if f.endswith(".png"):
        if f.lower() not in [n.lower() for n in final_names]:
            print(f"Deleting redundant file: {f}")
            try:
                os.remove(os.path.join(agents_dir, f))
            except Exception as e:
                print(f"Error deleting {f}: {e}")
