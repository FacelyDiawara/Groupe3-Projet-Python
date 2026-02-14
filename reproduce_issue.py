import requests
import sys

URL = "http://127.0.0.1:8000"
LOG_FILE = "repro_log.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def test_health():
    try:
        log(f"Testing connection to {URL}...")
        response = requests.get(f"{URL}/")
        log(f"Root endpoint status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        log("❌ Could not connect to server. Is it running?")
        return False
    except Exception as e:
        log(f"❌ Error connecting: {e}")
        return False

def test_registration():
    try:
        log("\nTesting Registration...")
        payload = {
            "username": "testuser_final_v1",
            "email": "test_final@example.com",
            "password": "password123",
            "role": "Patient"
        }
        response = requests.post(f"{URL}/api/register", json=payload)
        log(f"Registration status: {response.status_code}")
        log(f"Response body: {response.text}")
        
        if response.status_code == 200:
            log("✅ Registration successful")
            return True
        elif response.status_code == 400:
            log("⚠️ Registration failed (expected if user exists)")
            return True
        else:
            log("❌ Registration failed with unexpected error")
            return False

    except Exception as e:
        log(f"❌ Error during registration: {e}")
        return False

if __name__ == "__main__":
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("--- Repro Log ---\n")
    if test_health():
        test_registration()
    else:
        sys.exit(1)
