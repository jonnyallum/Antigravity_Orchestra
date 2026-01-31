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
        
        # Walk and list depth 2
        print("\nRoot Listing:")
        ftp.cwd(".")
        root_files = ftp.nlst(".")
        print(root_files)
        
        for item in root_files:
            try:
                # Try to list assuming it is a dir
                sub = ftp.nlst(item)
                if sub:
                    print(f"\nListing of {item}:")
                    print(sub)
            except:
                pass

        ftp.quit()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check()
