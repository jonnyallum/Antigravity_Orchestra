import ftplib
from ftplib import FTP_TLS
import os

HOST = "92.112.189.250"
USER = "u384342620.villagebakeryandcafe.co.uk"
PASS = "Aprilia100!69."
LOCAL_FILE = r"c:\Users\jonny\Antigravity-new\villagebakeryandcafe.co.uk\source_code\dist\index.html"
REMOTE_FILE = "public_html/v2.html"

def upload():
    try:
        ftp = FTP_TLS(HOST)
        ftp.login(USER, PASS)
        ftp.prot_p()
        print("Connected.")
        
        with open(LOCAL_FILE, "rb") as f:
            ftp.storbinary(f"STOR {REMOTE_FILE}", f)
        print(f"Uploaded {LOCAL_FILE} to {REMOTE_FILE}")
            
        ftp.quit()
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    upload()
