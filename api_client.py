import requests

BASE_URL = "http://127.0.0.1:8000"

def get_doctors():
    try:
        response = requests.get(f"{BASE_URL}/doctors/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching doctors: {e}")
        return []

def create_doctor(doctor_data):
    try:
        response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating doctor: {e}")
        return None

def delete_doctor(doctor_id):
    try:
        response = requests.delete(f"{BASE_URL}/doctors/{doctor_id}")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error deleting doctor: {e}")
        return False

def get_appointments():
    try:
        response = requests.get(f"{BASE_URL}/appointments/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        return []

def create_appointment(appointment_data):
    try:
        response = requests.post(f"{BASE_URL}/appointments/", json=appointment_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating appointment: {e}")
        return None

def delete_appointment(appointment_id):
    try:
        response = requests.delete(f"{BASE_URL}/appointments/{appointment_id}")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error deleting appointment: {e}")
        return False

def get_medications():
    try:
        response = requests.get(f"{BASE_URL}/medications/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching medications: {e}")
        return []

def create_medication(medication_data):
    try:
        response = requests.post(f"{BASE_URL}/medications/", json=medication_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating medication: {e}")
        return None

def delete_medication(medication_id):
    try:
        response = requests.delete(f"{BASE_URL}/medications/{medication_id}")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error deleting medication: {e}")
        return False

def clear_medications():
    try:
        response = requests.delete(f"{BASE_URL}/medications/")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error clearing medications: {e}")
        return False

# Reminder Functions
def create_reminder(reminder_data):
    """Save a recurring reminder to the backend"""
    try:
        response = requests.post(f"{BASE_URL}/reminders/", json=reminder_data)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error creating reminder: {e}")
        return None

def get_reminders():
    """Fetch all active reminders from the backend"""
    try:
        response = requests.get(f"{BASE_URL}/reminders/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reminders: {e}")
        return []

def delete_reminder(reminder_id):
    """Delete a reminder by ID"""
    try:
        response = requests.delete(f"{BASE_URL}/reminders/{reminder_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error deleting reminder: {e}")
        return False
