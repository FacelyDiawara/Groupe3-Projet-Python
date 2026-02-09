"""
Test script to verify navigation from appointments to medications page
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from fich_accueil import HospitalUI

def test_navigation():
    app = QApplication(sys.argv)
    window = HospitalUI()
    window.show()
    
    print("Application démarrée")
    print(f"Page actuelle: {window.pages.currentIndex()}")
    
    # Navigate to appointments page (index 1)
    window.change_page(1)
    print(f"Navigué vers Rendez-vous (page {window.pages.currentIndex()})")
    
    # Simulate clicking the medications button
    def click_medications_button():
        print("Simulation du clic sur le bouton 'Aller à Prise de Médicament'")
        window.appointments_page.go_to_medications()
        print(f"Page après clic: {window.pages.currentIndex()}")
        
        if window.pages.currentIndex() == 2:
            print("✅ SUCCESS: Navigation vers la page Médicaments réussie!")
        else:
            print("❌ ERREUR: La navigation n'a pas fonctionné")
        
        # Close after test
        QTimer.singleShot(1000, app.quit)
    
    # Wait a bit then click
    QTimer.singleShot(500, click_medications_button)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_navigation()
