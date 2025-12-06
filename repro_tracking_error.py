import requests

# Try both localhost and the deployed URL if known, but let's start with localhost where we saw it working before
# If user is testing on DEPLOYED env, we should ask for URL or assume it.
# Let's assume user is testing locally first or provide a way to switch.

# API_URL = "http://localhost:3001" 
API_URL = "https://food-delivery-api-r6ih.onrender.com" 
# Verify if creating an order and tracking it works nicely
# If this works locally, then the issue is likely data mismatch on production (e.g. wiped DB)

def test_menu():
    print("Checking Menu Endpoint...")
    try:
        resp = requests.get(f"{API_URL}/menu/")
        if resp.status_code == 200:
            print("SUCCESS: Menu endpoint is working!")
            items = resp.json()
            print(f"Found {len(items)} menu items.")
        else:
            print(f"FAILURE: Menu endpoint returned {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"CRITICAL FAILURE: Could not connect to API. {e}")

if __name__ == "__main__":
    test_menu()
