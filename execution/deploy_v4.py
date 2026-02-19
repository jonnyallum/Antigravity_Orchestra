
import paramiko
import os
from dotenv import load_dotenv

def deploy_insydetradar_v4():
    host = "92.112.189.250"
    port = 65002
    username = "u384342620"
    password = "Aprilia100!69."
    
    local_dir = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\Insydetradar\Web"
    remote_path = "domains/insydetradar.com/public_html"

    print(f"Deploying v4.0 to {host}:{port}...")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        
        sftp = ssh.open_sftp()
        
        # 1. Ensure remote directory exists (already did in previous step but being safe)
        try:
            sftp.mkdir(remote_path)
        except OSError:
            pass # Already exists
            
        # 2. Upload files
        files_to_deploy = ["index.html", "script.js", "styles.css", ".htaccess"]
        for file in files_to_deploy:
            local_file = os.path.join(local_dir, file)
            remote_file = f"{remote_path}/{file}"
            if os.path.exists(local_file):
                print(f"Uploading {file}...")
                sftp.put(local_file, remote_file)
            else:
                print(f"Warning: Local file {local_file} not found.")

        sftp.close()
        
        # 3. Final listing
        print("Deployment complete. Verifying...")
        stdin, stdout, stderr = ssh.exec_command(f"ls -l {remote_path}")
        print(stdout.read().decode())
        
        ssh.close()
        print("v4.0 Live Deployment: SUCCESS")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_insydetradar_v4()
