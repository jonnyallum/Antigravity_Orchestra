
import paramiko
import os
from dotenv import load_dotenv

def fix_insydetradar_directory():
    host = "92.112.189.250"
    port = 65002
    username = "u384342620"
    password = "Aprilia100!69."
    
    domain_path = "domains/insydetradar.com"
    public_html = f"{domain_path}/public_html"

    print(f"Connecting to {host}:{port} to fix directory structure...")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        
        # 1. Create public_html if it doesn't exist
        print(f"Creating directory: {public_html}")
        ssh.exec_command(f"mkdir -p {public_html}")
        
        # 2. Move files into public_html
        # We'll use mv with a check to avoid moving public_html into itself if glob finds it later
        files_to_move = ["index.html", "script.js", "styles.css", ".htaccess"]
        for file in files_to_move:
            print(f"Moving {file} to public_html...")
            ssh.exec_command(f"mv {domain_path}/{file} {public_html}/")
        
        # 3. Verify
        print("Verifying new structure...")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {public_html}/")
        print("Files in public_html:")
        print(stdout.read().decode())
        
        ssh.close()
        print("Fix applied successfully.")
        return True
    except Exception as e:
        print(f"Fix failed: {e}")
        return False

if __name__ == "__main__":
    fix_insydetradar_directory()
