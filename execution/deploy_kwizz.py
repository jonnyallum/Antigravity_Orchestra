import paramiko
import os
import sys
from pathlib import Path

def deploy_kwizz():
    host = "92.112.189.250"
    port = 65002
    username = "u384342620"
    password = "Aprilia100!69."
    
    local_dir = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\kwizz\out"
    remote_path = "domains/kwizz.co.uk/public_html"

    print(f"🚀 Deploying Kwizz Fix to {host}:{port}...")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        
        sftp = ssh.open_sftp()
        
        # 1. Clear old files (except .htaccess if we want, but we have a NEW .htaccess in public)
        print("🧹 Clearing old remote files...")
        ssh.exec_command(f"rm -rf {remote_path}/*")
        
        # 2. Upload files recursively
        uploaded_count = 0
        
        def upload_recursive(local_p, remote_p):
            nonlocal uploaded_count
            try:
                sftp.mkdir(remote_p)
            except OSError:
                pass
            
            for item in os.listdir(local_p):
                local_item = os.path.join(local_p, item)
                remote_item = f"{remote_p}/{item}"
                
                if os.path.isfile(local_item):
                    # print(f"  Uploading {item}...")
                    sftp.put(local_item, remote_item)
                    uploaded_count += 1
                elif os.path.isdir(local_item):
                    upload_recursive(local_item, remote_item)

        upload_recursive(local_dir, remote_path)
        
        print(f"✅ Uploaded {uploaded_count} files.")
        
        sftp.close()
        ssh.close()
        print("✨ Kwizz fixes are now LIVE!")
        return True
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_kwizz()
