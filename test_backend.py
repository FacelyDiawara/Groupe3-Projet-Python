import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_create_doctor():
    print("Testing Create Doctor...")
    doctor_data = {
        "nom": "TEST",
        "prenom": "User",
        "specialite": "Testing",
        "telephone": "123456789",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_get_doctors():
    print("Testing Get Doctors...")
    response = requests.get(f"{BASE_URL}/doctors/")
    print(f"Status Code: {response.status_code}")
    print(f"Doctors: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    try:
        if test_create_doctor() and test_get_doctors():
            print("\nBackend Verification SUCCESSFUL!")
    except Exception as e:
        print(f"\nBackend Verification FAILED: {e}")
