#!/usr/bin/env python3
import os
import sys
import paramiko
from pathlib import Path

def deploy_sftp(host, port, username, password, local_dir, remote_dir):
    """Deploy files via SFTP"""
    print(f"Connecting to {host}:{port}...")

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=port, username=username, password=password, timeout=30)
        print("Connected successfully!")

        # Create SFTP session
        sftp = ssh.open_sftp()

        remote_path = remote_dir
        print(f"Remote path: {remote_path}")

        # Clear existing files (except .htaccess)
        print("Clearing old files...")
        # Be careful here, ensure the path is correct
        stdin, stdout, stderr = ssh.exec_command(f"find {remote_path} -mindepth 1 -not -name '.htaccess' -delete 2>/dev/null; echo 'cleared'")
        stdout.read()

        # Upload files recursively
        local_path = Path(local_dir)
        uploaded = 0

        def upload_directory(local_dir_path, remote_dir_path):
            nonlocal uploaded

            # Create remote directory if needed
            try:
                sftp.stat(remote_dir_path)
            except FileNotFoundError:
                sftp.mkdir(remote_dir_path)
                print(f"  Created directory: {remote_dir_path}")

            for item in os.listdir(local_dir_path):
                local_item = os.path.join(local_dir_path, item)
                remote_item = f"{remote_dir_path}/{item}"

                if os.path.isfile(local_item):
                    # print(f"  Uploading: {item}")
                    sftp.put(local_item, remote_item)
                    uploaded += 1
                elif os.path.isdir(local_item):
                    upload_directory(local_item, remote_item)

        print(f"Uploading files from {local_dir}...")
        upload_directory(str(local_path), remote_path)

        print(f"\nDeployed {uploaded} files successfully!")

        sftp.close()
        ssh.close()
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

if __name__ == "__main__":
    config = {
        "host": "92.112.189.250",
        "port": 65002,
        "username": "u384342620",
        "password": "Aprilia100!69.",
        "local_dir": r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\DJ Waste\dj-waste-app\dist\public",
        "remote_dir": "/home/u384342620/domains/dj-waste.co.uk/public_html"
    }

    success = deploy_sftp(**config)
    sys.exit(0 if success else 1)
