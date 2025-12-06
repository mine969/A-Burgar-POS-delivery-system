import requests
import sys

BASE_URL = "https://food-delivery-api-r6ih.onrender.com"
LOGIN_URL = f"{BASE_URL}/auth/login"
MENU_URL = f"{BASE_URL}/menu/"

def test_admin_crud():
    # 1. Login
    print(f"Logging in as admin...")
    try:
        response = requests.post(
            LOGIN_URL,
            data={"username": "admin123@gmail.com", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        token = response.json()["access_token"]
        print("Login successful. Token received.")
    except Exception as e:
        print(f"Login failed: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")
        sys.exit(1)

    # 2. Create Menu Item
    print(f"Creating menu item...")
    item_data = {
        "name": "Debug Burger",
        "description": "Created by debug script",
        "price": 12.50,
        "category": "Main"
    }
    try:
        response = requests.post(
            MENU_URL,
            json=item_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            print("Menu item created successfully.")
            print(response.json())
        else:
            print(f"Failed to create menu item. Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_admin_crud()
