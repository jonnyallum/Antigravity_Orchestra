"""
Simplified GA4 Property Setup - Debug Version
"""

import json
from google.analytics.admin import AnalyticsAdminServiceClient
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = r"C:\Users\jonny\Downloads\splendid-light-451420-a0-bfc0747dc627.json"

def check_access():
    """Check what access the service account has."""
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/analytics.edit"]
    )
    
    client = AnalyticsAdminServiceClient(credentials=credentials)
    
    print("Checking service account access...")
    print("=" * 60)
    
    try:
        # List accounts
        print("\nFetching accounts...")
        accounts = list(client.list_accounts())
        
        if not accounts:
            print("❌ No accounts found!")
            print("\nThe service account has been added to GA4, but may need:")
            print("1. Wait a few minutes for permissions to propagate")
            print("2. Ensure 'Editor' or 'Administrator' role at ACCOUNT level")
            return None
        
        for account in accounts:
            print(f"\n✓ Found account: {account.display_name}")
            print(f"  Account ID: {account.name}")
            
            # List existing properties
            print(f"\n  Existing properties:")
            try:
                properties = list(client.list_properties(filter=f"parent:{account.name}"))
                if properties:
                    for prop in properties:
                        print(f"    - {prop.display_name} ({prop.name})")
                else:
                    print(f"    (No properties yet)")
            except Exception as e:
                print(f"    Error listing properties: {str(e)}")
            
            return account.name
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nThis usually means:")
        print("1. Service account not added to GA4 account")
        print("2. Insufficient permissions (needs Administrator role)")
        print("3. API not enabled in Google Cloud project")
        return None

if __name__ == "__main__":
    check_access()
