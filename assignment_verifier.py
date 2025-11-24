import os
import requests
import subprocess
import sys
import time

def print_pass(message):
    print(f"✅ PASS: {message}")

def print_fail(message):
    print(f"❌ FAIL: {message}")

def check_file_exists(filepath):
    if os.path.exists(filepath):
        print_pass(f"File found: {filepath}")
        return True
    else:
        print_fail(f"File missing: {filepath}")
        return False

def check_docker_containers():
    try:
        result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], capture_output=True, text=True)
        running_containers = result.stdout.splitlines()
        
        required_services = ['backend', 'frontend', 'db']
        all_running = True
        
        for service in required_services:
            found = False
            for container in running_containers:
                if service in container:
                    found = True
                    break
            
            if found:
                print_pass(f"Container running for service: {service}")
            else:
                print_fail(f"Container NOT running for service: {service}")
                all_running = False
        return all_running
    except Exception as e:
        print_fail(f"Error checking Docker: {e}")
        return False

def check_endpoint(url, description):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print_pass(f"{description} is accessible ({url})")
            return True
        else:
            print_fail(f"{description} returned status {response.status_code} ({url})")
            return False
    except requests.exceptions.ConnectionError:
        print_fail(f"{description} is unreachable ({url})")
        return False
    except Exception as e:
        print_fail(f"Error checking {description}: {e}")
        return False

def main():
    print("=== 📋 Assignment Verification Script ===\n")
    
    # 1. Check Required Files
    print("--- 1. Checking Required Files ---")
    files_to_check = [
        "Jenkinsfile",
        "docker-compose.yml",
        "backend/Dockerfile",
        "frontend-demo/Dockerfile",
        ".env.example"
    ]
    files_ok = all([check_file_exists(f) for f in files_to_check])
    print("")

    # 2. Check Docker Containers
    print("--- 2. Checking Docker Containers ---")
    docker_ok = check_docker_containers()
    print("")

    # 3. Check API and Frontend
    print("--- 3. Checking Services ---")
    # Assuming standard ports from previous context
    api_ok = check_endpoint("http://localhost:8000/docs", "Backend API Docs")
    frontend_ok = check_endpoint("http://localhost:3001", "Frontend Application")
    print("")

    # 4. Functional Tests
    print("--- 4. Functional Tests ---")
    
    # Test 4.1: Check Menu Data
    menu_data_ok = False
    try:
        response = requests.get("http://localhost:8000/menu/", timeout=5)
        if response.status_code == 200:
            items = response.json()
            if len(items) > 0:
                print_pass(f"Menu API returned {len(items)} items")
                # Check for specific seeded item
                if any(i['name'] == "Classic Burger" for i in items):
                    print_pass("Found 'Classic Burger' in menu")
                    menu_data_ok = True
                else:
                    print_fail("'Classic Burger' not found in menu data")
            else:
                print_fail("Menu API returned empty list")
        else:
            print_fail(f"Menu API returned status {response.status_code}")
    except Exception as e:
        print_fail(f"Error checking menu data: {e}")

    # Test 4.2: Authentication (Login)
    auth_ok = False
    token = None
    try:
        # Using credentials from seed_data.py
        login_data = {
            "username": "admin@example.com",
            "password": "admin123"
        }
        # Note: OAuth2PasswordRequestForm expects form data, not JSON usually, but let's check auth.py
        # If it uses standard FastAPI OAuth2, it needs data=...
        response = requests.post("http://localhost:8000/auth/login", data=login_data, timeout=5)
        
        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                token = token_data["access_token"]
                print_pass("Authentication successful (Admin Login)")
                auth_ok = True
            else:
                print_fail("Login response missing access_token")
        else:
            print_fail(f"Login failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print_fail(f"Error checking authentication: {e}")

    # Test 4.3: Create Order (if auth worked)
    order_ok = False
    if auth_ok and token:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            # Need a valid customer_id or just create order as admin? 
            # Looking at schemas, order creation might be open or require auth.
            # Let's try creating a simple order.
            # We need a menu item ID first.
            menu_response = requests.get("http://localhost:8000/menu/")
            first_item = menu_response.json()[0]
            
            order_payload = {
                "delivery_address": "123 Test St",
                "notes": "Test Order",
                "items": [
                    {
                        "menu_item_id": first_item['id'],
                        "quantity": 1
                    }
                ]
            }
            
            response = requests.post("http://localhost:8000/orders/", json=order_payload, headers=headers, timeout=5)
            if response.status_code in [200, 201]:
                print_pass(f"Order creation successful (Order ID: {response.json().get('id')})")
                order_ok = True
            else:
                print_fail(f"Order creation failed: {response.status_code} - {response.text}")
        except Exception as e:
            print_fail(f"Error creating order: {e}")
    else:
        print_fail("Skipping Order Test due to Auth failure")

    print("")

    # Summary
    print("=== 🏁 Verification Summary ===")
    if files_ok and docker_ok and api_ok and frontend_ok and menu_data_ok and auth_ok and order_ok:
        print("\n🎉 CONGRATULATIONS! All checks passed. Your assignment is FULLY FUNCTIONAL.")
        sys.exit(0)
    else:
        print("\n⚠️  SOME CHECKS FAILED. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
