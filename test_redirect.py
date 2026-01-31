import requests
import json

BASE_URL = "http://192.168.1.69:5000"

def test_flow():
    print(f"Testing backend at {BASE_URL}...")
    
    # 1. Generate QR
    print("Generating QR...")
    try:
        resp = requests.post(f"{BASE_URL}/api/qr/generate", json={
            "name": "Test Redirect",
            "link": "https://example.org"
        })
        if resp.status_code != 200:
            print(f"Generate failed: {resp.text}")
            return
        
        data = resp.json()
        qr_id = data["qr_id"]
        print(f"Generated QR ID: {qr_id}")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Test Redirect
    redirect_url = f"{BASE_URL}/q/{qr_id}"
    print(f"Testing redirect URL: {redirect_url}")
    
    try:
        # allow_redirects=False to see the 302 response
        resp = requests.get(redirect_url, allow_redirects=False)
        print(f"Response Code: {resp.status_code}")
        
        if resp.status_code == 302:
            location = resp.headers.get("Location")
            print(f"Redirect Location: {location}")
            if location == "https://example.org":
                print("SUCCESS: Redirect matches target!")
            else:
                print("FAILURE: Redirect location mismatch.")
        else:
            print(f"FAILURE: Expected 302, got {resp.status_code}")
            print(resp.text)
            
    except Exception as e:
        print(f"Redirect request failed: {e}")

if __name__ == "__main__":
    test_flow()
