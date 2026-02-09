import sqlite3
import os

def migrate():
    db_path = "hospital.db"
    if not os.path.exists(db_path):
        print(f"Base de données {db_path} introuvable.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check prescriptions table
    cursor.execute("PRAGMA table_info(prescriptions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "telephone_patient" not in columns:
        print("Ajout de la colonne 'telephone_patient' à la table 'prescriptions'...")
        try:
            cursor.execute("ALTER TABLE prescriptions ADD COLUMN telephone_patient TEXT")
            conn.commit()
            print("Colonne ajoutée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout de la colonne : {e}")
    else:
        print("La colonne 'telephone_patient' existe déjà.")

    conn.close()

if __name__ == "__main__":
    migrate()
