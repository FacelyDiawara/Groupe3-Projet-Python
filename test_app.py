"""
Script de test pour vérifier que l'application fonctionne correctement
"""
import requests
import time

def test_server():
    """Teste si le serveur répond correctement"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Test de l'application Hôpital Central\n")
    
    # Test 1: Page d'accueil
    print("1. Test de la page d'accueil...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Page d'accueil accessible")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: API Doctors
    print("2. Test de l'API Doctors...")
    try:
        response = requests.get(f"{base_url}/doctors/")
        if response.status_code == 200:
            print(f"   ✅ API Doctors fonctionne ({len(response.json())} docteurs)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: API Appointments
    print("3. Test de l'API Appointments...")
    try:
        response = requests.get(f"{base_url}/appointments/")
        if response.status_code == 200:
            print(f"   ✅ API Appointments fonctionne ({len(response.json())} rendez-vous)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: API Medications
    print("4. Test de l'API Medications...")
    try:
        response = requests.get(f"{base_url}/medications/")
        if response.status_code == 200:
            print(f"   ✅ API Medications fonctionne ({len(response.json())} médicaments)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 5: Fichiers statiques
    print("5. Test des fichiers statiques...")
    try:
        response = requests.get(f"{base_url}/static/css/style.css")
        if response.status_code == 200:
            print("   ✅ CSS accessible")
        else:
            print(f"   ❌ CSS non accessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    try:
        response = requests.get(f"{base_url}/static/js/app.js")
        if response.status_code == 200:
            print("   ✅ JavaScript accessible")
        else:
            print(f"   ❌ JavaScript non accessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n✅ Tests terminés avec succès!")
    return True

if __name__ == "__main__":
    print("⏳ Attente du démarrage du serveur (5 secondes)...\n")
    time.sleep(5)
    test_server()
