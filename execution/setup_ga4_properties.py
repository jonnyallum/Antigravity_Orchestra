"""
Google Analytics 4 Property Setup Script

This script uses the Google Analytics Admin API to:
1. Create 6 GA4 properties (one for each website)
2. Create data streams for each property
3. Extract and save the Measurement IDs

Requirements:
- google-analytics-admin package
- Service account JSON key with Analytics Admin permissions
"""

import json
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import (
    Property,
    DataStream,
)
from google.oauth2 import service_account

# Configuration
SERVICE_ACCOUNT_FILE = r"C:\Users\jonny\Downloads\splendid-light-451420-a0-bfc0747dc627.json"

# Website configurations
WEBSITES = [
    {
        "name": "Jonny AI",
        "domain": "jonnyai.co.uk",
        "url": "https://jonnyai.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    },
    {
        "name": "BL Motorcycles",
        "domain": "blmotorcyclesltd.co.uk",
        "url": "https://blmotorcyclesltd.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    },
    {
        "name": "Village Bakery & Cafe",
        "domain": "villagebakeryandcafe.co.uk",
        "url": "https://villagebakeryandcafe.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    },
    {
        "name": "LA Aesthetician",
        "domain": "la-aesthetician.co.uk",
        "url": "https://la-aesthetician.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    },
    {
        "name": "CD Waste & Recycling",
        "domain": "cd-waste.co.uk",
        "url": "https://cd-waste.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    },
    {
        "name": "DJ Waste & Demolition",
        "domain": "dj-waste.co.uk",
        "url": "https://dj-waste.co.uk",
        "timezone": "Europe/London",
        "currency": "GBP"
    }
]


def create_ga4_properties():
    """Create GA4 properties and data streams for all websites."""
    
    # Load service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/analytics.edit"]
    )
    
    # Initialize the Analytics Admin API client
    client = AnalyticsAdminServiceClient(credentials=credentials)
    
    results = []
    
    # Get the account (we need to find the account ID first)
    print("Fetching Google Analytics accounts...")
    accounts = client.list_accounts()
    
    account_name = None
    for account in accounts:
        print(f"Found account: {account.name} - {account.display_name}")
        account_name = account.name
        break  # Use the first account
    
    if not account_name:
        print("ERROR: No Google Analytics account found for this service account.")
        print("Please ensure the service account has been granted access to a GA4 account.")
        return []
    
    print(f"\nUsing account: {account_name}\n")
    
    # Create properties for each website
    for website in WEBSITES:
        try:
            print(f"Creating property for {website['name']}...")
            
            # Create property
            property_obj = Property(
                display_name=website['name'],
                time_zone=website['timezone'],
                currency_code=website['currency'],
                industry_category="OTHER"
            )
            
            property_response = client.create_property(
                property=property_obj,
                parent=account_name
            )
            
            print(f"✓ Property created: {property_response.name}")
            
            # Create web data stream
            print(f"  Creating data stream for {website['url']}...")
            
            stream = DataStream(
                display_name=f"{website['name']} - Web",
                type_=DataStream.DataStreamType.WEB_DATA_STREAM,
            )
            
            stream_response = client.create_data_stream(
                parent=property_response.name,
                data_stream=stream
            )
            
            # Set the default URI after creation
            stream_response.web_stream_data.default_uri = website['url']
            
            measurement_id = stream_response.web_stream_data.measurement_id
            
            print(f"✓ Data stream created")
            print(f"✓ Measurement ID: {measurement_id}\n")
            
            results.append({
                "domain": website['domain'],
                "name": website['name'],
                "property_id": property_response.name.split('/')[-1],
                "measurement_id": measurement_id,
                "stream_id": stream_response.name.split('/')[-1]
            })
            
        except Exception as e:
            print(f"✗ Error creating property for {website['name']}: {str(e)}\n")
            results.append({
                "domain": website['domain'],
                "name": website['name'],
                "error": str(e)
            })
    
    return results


def save_results(results):
    """Save the results to a JSON file."""
    output_file = r"C:\Users\jonny\.gemini\antigravity\brain\82d66afe-b71d-4cf9-9fda-3d20a909429a\ga4_measurement_ids.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    # Also create a simple text file with just the measurement IDs
    text_file = r"C:\Users\jonny\.gemini\antigravity\brain\82d66afe-b71d-4cf9-9fda-3d20a909429a\measurement_ids.txt"
    
    with open(text_file, 'w') as f:
        f.write("GA4 Measurement IDs\n")
        f.write("=" * 50 + "\n\n")
        for result in results:
            if 'measurement_id' in result:
                f.write(f"{result['domain']}: {result['measurement_id']}\n")
            else:
                f.write(f"{result['domain']}: ERROR - {result.get('error', 'Unknown error')}\n")
    
    print(f"Measurement IDs saved to: {text_file}")


if __name__ == "__main__":
    print("=" * 60)
    print("Google Analytics 4 Property Setup")
    print("=" * 60)
    print()
    
    results = create_ga4_properties()
    
    if results:
        save_results(results)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        for result in results:
            if 'measurement_id' in result:
                print(f"✓ {result['name']}: {result['measurement_id']}")
            else:
                print(f"✗ {result['name']}: FAILED")
        
        print("\nSetup complete!")
    else:
        print("\nNo properties were created. Please check the errors above.")
