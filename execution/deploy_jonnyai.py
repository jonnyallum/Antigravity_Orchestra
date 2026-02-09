#!/usr/bin/env python3
"""
Deploy JonnyAI Protocol v2
Deploys jonnyai.website to Hostinger via SFTP
- Uploads out/ (built pages) 
- Uploads public/ assets (agents, logos, etc.) that Next.js static export misses
- Skips missing/broken files gracefully
"""

import paramiko
import os
import sys
from pathlib import Path

def ensure_remote_dir(sftp, remote_dir):
    """Recursively create remote directories."""
    dirs_to_create = []
    current = remote_dir
    while True:
        try:
            sftp.stat(current)
            break
        except FileNotFoundError:
            dirs_to_create.append(current)
            current = os.path.dirname(current)
            if current == '/' or current == '':
                break
    for d in reversed(dirs_to_create):
        try:
            sftp.mkdir(d)
        except Exception:
            pass  # May already exist

def upload_directory(sftp, local_dir, remote_path, skip_dirs=None):
    """Upload a local directory to remote, skipping missing files."""
    uploaded = 0
    skipped = 0
    skip_dirs = skip_dirs or []
    
    for root, dirs, files in os.walk(local_dir):
        # Skip specified directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        relative_path = os.path.relpath(root, local_dir)
        if relative_path == '.':
            remote_root = remote_path
        else:
            remote_root = remote_path + '/' + relative_path.replace('\\', '/')
        
        ensure_remote_dir(sftp, remote_root)
        
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = remote_root + '/' + file
            
            # Skip files that don't actually exist (broken symlinks etc)
            if not os.path.isfile(local_file):
                print(f"  SKIP (missing): {file}")
                skipped += 1
                continue
                
            try:
                print(f"  Uploading {relative_path}/{file}..." if relative_path != '.' else f"  Uploading {file}...")
                sftp.put(local_file, remote_file)
                uploaded += 1
            except Exception as e:
                print(f"  SKIP (error): {file} - {e}")
                skipped += 1
    
    return uploaded, skipped

def deploy_jonnyai():
    # Configuration
    host = "92.112.189.250"
    port = 65002
    username = "u384342620"
    password = "Aprilia100!69."
    
    # Paths
    base_dir = r"C:\Users\jonny\Desktop\AgOS 3.0 template\Clients\jonnyai.website"
    out_dir = os.path.join(base_dir, "out")
    public_dir = os.path.join(base_dir, "public")
    
    if not os.path.exists(out_dir):
        print(f"ERROR: Build output not found at {out_dir}")
        print("Run 'npm run build' in the jonnyai.website directory first.")
        return False
    
    print(f"Initiating deployment to {host}...")
    print(f"  Build dir: {out_dir}")
    print(f"  Public dir: {public_dir}")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password, timeout=60, banner_timeout=60)
        print("SSH Connection established.")
        
        # Find the jonnyai domain
        stdin, stdout, stderr = ssh.exec_command("ls -F ~/domains/")
        domains = stdout.read().decode().strip().split('\n')
        print(f"Found domains: {domains}")
        
        target_domain = None
        for d in domains:
            d = d.strip('/')
            if 'jonny' in d.lower() and 'ai' in d.lower():
                target_domain = d
                break
        
        if not target_domain:
            print("ERROR: Could not find JonnyAI domain on server.")
            return False
            
        print(f"Targeting domain: {target_domain}")
        remote_path = f"/home/u384342620/domains/{target_domain}/public_html"
        print(f"Remote path: {remote_path}")

        sftp = ssh.open_sftp()
        
        total_uploaded = 0
        total_skipped = 0
        
        # Phase 1: Upload out/ directory (built pages + _next assets)
        print(f"\n--- Phase 1: Deploying built pages from out/ ---")
        u, s = upload_directory(sftp, out_dir, remote_path)
        total_uploaded += u
        total_skipped += s
        print(f"Phase 1 complete: {u} uploaded, {s} skipped")
        
        # Phase 2: Upload public/ assets (agents, logos, etc.)
        # Skip _next and files already in out/ root
        if os.path.exists(public_dir):
            print(f"\n--- Phase 2: Deploying public/ assets ---")
            # Only upload subdirectories from public/ (agents/, etc.)
            for item in os.listdir(public_dir):
                item_path = os.path.join(public_dir, item)
                if os.path.isdir(item_path):
                    print(f"\n  Uploading public/{item}/...")
                    u, s = upload_directory(sftp, item_path, remote_path + '/' + item)
                    total_uploaded += u
                    total_skipped += s
                elif os.path.isfile(item_path):
                    # Upload root-level public files (favicon, logos, etc.)
                    remote_file = remote_path + '/' + item
                    try:
                        print(f"  Uploading {item}...")
                        sftp.put(item_path, remote_file)
                        total_uploaded += 1
                    except Exception as e:
                        print(f"  SKIP: {item} - {e}")
                        total_skipped += 1
            print(f"Phase 2 complete")
        
        print(f"\n{'='*50}")
        print(f"DEPLOYMENT COMPLETE!")
        print(f"  Total uploaded: {total_uploaded} files")
        print(f"  Total skipped: {total_skipped} files")
        print(f"  Target: https://{target_domain}")
        print(f"{'='*50}")
        
        sftp.close()
        ssh.close()
        return True

    except Exception as e:
        print(f"DEPLOYMENT FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    deploy_jonnyai()
