import ftplib
from ftplib import FTP_TLS

HOST = "92.112.189.250"
USER = "u384342620.villagebakeryandcafe.co.uk"
PASS = "Aprilia100!69."

def check():
    try:
        ftp = FTP_TLS(HOST)
        ftp.login(USER, PASS)
        ftp.prot_p()
        print("Connected.")
        
        print(f"PWD: {ftp.pwd()}")
        
        # List public_html
        try:
            files = ftp.nlst("public_html")
            print("\nFiles in public_html:")
            for f in files:
                print(f)
        except Exception as e:
            print(f"Error listing public_html: {e}")

        # List assets
        try:
            assets = ftp.nlst("public_html/assets")
            print("\nFiles in public_html/assets:")
            for f in assets:
                print(f)
        except Exception as e:
            print(f"Error listing assets: {e}")
            
        ftp.quit()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check()
