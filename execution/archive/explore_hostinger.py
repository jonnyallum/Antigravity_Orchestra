
import paramiko
import os
from dotenv import load_dotenv

def explore_hostinger():
    host = "92.112.189.250"
    port = 65002
    username = "u384342620"
    password = "Aprilia100!69."
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        
        # List all domains and their structures
        stdin, stdout, stderr = ssh.exec_command("ls -R domains/")
        print("--- DOMAINS STRUCTURE ---")
        print(stdout.read().decode())
        
        # Check for Node.js or PM2
        stdin, stdout, stderr = ssh.exec_command("pm2 list || echo 'pm2 not found'")
        print("--- PM2 STATUS ---")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_hostinger()
