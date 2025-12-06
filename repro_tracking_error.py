import requests

# Try both localhost and the deployed URL if known, but let's start with localhost where we saw it working before
# If user is testing on DEPLOYED env, we should ask for URL or assume it.
# Let's assume user is testing locally first or provide a way to switch.

# API_URL = "http://localhost:3001" 
API_URL = "https://food-delivery-api-r6ih.onrender.com" 
# Verify if creating an order and tracking it works nicely
# If this works locally, then the issue is likely data mismatch on production (e.g. wiped DB)

def test_tracking():
    # Check specifically for Order ID 1 as reported by user
    target_id = 1
    print(f"Checking Order ID: {target_id}")
    track_resp = requests.get(f"{API_URL}/guest/track/{target_id}")
    
    if track_resp.status_code == 200:
        print("SUCCESS: Found order!")
        print(track_resp.json())
    else:
        print(f"FAILURE: {track_resp.status_code} {track_resp.text}")

if __name__ == "__main__":
    test_tracking()
