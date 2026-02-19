
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_alpaca_connection():
    print("--- [BROKER PROTOCOL] Testing Alpaca Connectivity ---")
    
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")
    base_url = "https://paper-api.alpaca.markets/v2"
    
    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }
    
    try:
        response = requests.get(f"{base_url}/account", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] CONNECTION SUCCESSFUL")
            print(f"Account ID: {data.get('id')}")
            print(f"Status: {data.get('status')}")
            print(f"Buying Power: ${data.get('buying_power')}")
            print(f"Cash: ${data.get('cash')}")
            print(f"Portfolio Value: ${data.get('portfolio_value')}")
            return True
        else:
            print(f"[ERROR] CONNECTION FAILED (Status: {response.status_code})")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"[CRITICAL] ERROR: {e}")
        return False

if __name__ == "__main__":
    # Point to the specific .env file if needed, but load_dotenv should find it in CWD if we run from the project root
    # However, since we are in the AgOS root, let's target the file explicitly
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\Insydetradar\Insydetradar\.env"
    load_dotenv(dotenv_path=env_path, override=True)
    test_alpaca_connection()
