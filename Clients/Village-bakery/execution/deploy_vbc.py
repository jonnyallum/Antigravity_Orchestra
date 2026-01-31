import os
import ftplib
import argparse
from ftplib import FTP_TLS

# Configuration Defaults
DEFAULT_HOST = "92.112.189.250"
DEFAULT_USER = "u384342620.villagebakeryandcafe.co.uk"

# Dynamically find the dist folder relative to this script
# Assuming script is in /execution/ and we want /villagebakeryandcafe.co.uk/source_code/dist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOCAL_DIR = os.path.join(BASE_DIR, "villagebakeryandcafe.co.uk", "source_code", "dist")

# CHANGE: Default to "." because the FTP user is chrooted to public_html
DEFAULT_REMOTE_DIR = "."

def upload_directory(ftp, local_dir, remote_dir):
    """Recursively uploads a directory to the FTP server."""
    if not os.path.isdir(local_dir):
        print(f"Error: Local directory '{local_dir}' not found.")
        return

    # Try to create remote directory only if it's not root/current
    if remote_dir and remote_dir != ".":
        try:
            ftp.mkd(remote_dir)
            print(f"Created remote directory: {remote_dir}")
        except ftplib.error_perm:
            # Directory likely exists
            pass

    # Walk through the local directory
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        
        # Construct remote path
        if remote_dir and remote_dir != ".":
            remote_path = f"{remote_dir}/{item}"
        else:
            remote_path = item

        if os.path.isfile(local_path):
            print(f"Uploading {item} to {remote_path}...")
            try:
                with open(local_path, "rb") as f:
                    ftp.storbinary(f"STOR {remote_path}", f)
            except Exception as e:
                print(f"Failed to upload {item}: {e}")
        elif os.path.isdir(local_path):
            upload_directory(ftp, local_path, remote_path)

def main():
    parser = argparse.ArgumentParser(description="Deploy VBC website to Hostinger via FTP/TLS")
    parser.add_argument("--password", required=True, help="FTP Password")
    parser.add_argument("--user", default=DEFAULT_USER, help="FTP Username")
    parser.add_argument("--host", default=DEFAULT_HOST, help="FTP Host")
    parser.add_argument("--remote", default=DEFAULT_REMOTE_DIR, help="Remote directory (default: '.')")
    
    args = parser.parse_args()

    print(f"Connecting to {args.host} as {args.user}...")
    
    try:
        ftp = FTP_TLS(args.host)
        ftp.login(user=args.user, passwd=args.password)
        ftp.prot_p()  # Switch to secure data connection
        print("Connected and authenticated securely.")
        
        print(f"Current PWD: {ftp.pwd()}")
        print(f"Deploying from {DEFAULT_LOCAL_DIR} to {args.remote}...")
        
        upload_directory(ftp, DEFAULT_LOCAL_DIR, args.remote)
        
        print("Deployment complete!")
        ftp.quit()
        
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    main()
