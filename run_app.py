import subprocess
import webbrowser
import time
import sys
import os

def start_application():
    """
    Démarre l'application web Hôpital Central
    - Lance le serveur FastAPI
    - Ouvre automatiquement le navigateur
    """
    print("=" * 60)
    print("🏥  HÔPITAL CENTRAL - Système de Gestion Hospitalière")
    print("=" * 60)
    print()
    
    # Déterminer l'exécutable Python
    python_exe = sys.executable
    
    print("🚀 Démarrage du serveur FastAPI...")
    print("📍 URL: http://127.0.0.1:8000")
    print()
    
    # Lancer le serveur FastAPI
    backend_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "backend.main:app", 
         "--host", "127.0.0.1", "--port", "8000", "--no-access-log"]
    )
    
    # Attendre que le serveur démarre
    print("⌛ Initialisation du serveur...")
    time.sleep(3)
    
    # Ouvrir le navigateur automatiquement
    print("🌐 Ouverture dans le navigateur...")
    webbrowser.open("http://127.0.0.1:8000")
    
    print()
    print("✅ Application lancée avec succès !")
    print("💡 L'application est maintenant accessible dans votre navigateur")
    print("⚠️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print()
    
    try:
        # Garder le processus en vie
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n")
        print("🛑 Arrêt du serveur...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print("✅ Application fermée proprement.")
        print()

if __name__ == "__main__":
    start_application()
