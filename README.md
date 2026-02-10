# Hôpital Central - Système de Gestion Hospitalière

Une application web moderne pour la gestion des services hospitaliers, incluant la gestion des patients, des docteurs, des prescriptions et des rappels automatisés.

---

## 💻 Installation Rapide

1. **Cloner le projet**
   ```bash
   git clone https://github.com/FacelyDiawara/Groupe3-Projet-Python.git
   cd Projet
   ```
2. **Dépendances**
   ```bash
   pip install -r requirements.txt
   ```
3. **Lancement**
   ```bash
   python run_app.py
   ```
   L'application est accessible sur : `http://127.0.0.1:8000`

---

## 🌟 Points Forts

- **Admin Facely Diawara** : Compte administrateur avec gestion totale des utilisateurs.
- **Sécurité RBAC** : Accès différencié pour Admins, Docteurs et Patients.
- **Récupération de Compte** : Système de réinitialisation de mot de passe par email.
- **Suppression Automatique** : Les comptes "Patient" sont éphémères et supprimés à la déconnexion.

---

## 📂 Architecture & Rôles des Fichiers

### 📁 Dossiers Principaux

- **`backend/`** : Cœur de l'application. Contient la logique serveur (FastAPI), les modèles SQL (`models.py`), les schémas de validation (`schemas.py`), les opérations de base de données (`crud.py`) et la configuration (`database.py`).
- **`templates/`** : Contient toutes les interfaces utilisateur au format HTML (Jinja2).
- **`static/`** : Fichiers statiques (CSS pour le design et JS pour la logique d'interaction et de sécurité).
- **`prescriptions/`** : Répertoire de stockage ou de gestion des ordonnances générées.
- **`assets/`** : Ressources graphiques et icônes du projet.

### 📄 Fichiers du Backend (Détails)

- **`run_app.py`** : Point d'entrée principal. Configure et lance le serveur FastAPI.
- **`create_admin.py`** : Script utilitaire pour initialiser le compte administrateur principal.
- **`messaging_service.py`** : Service gérant la logique des envois de notifications (SMS/WhatsApp).
- **`config.py`** : Paramètres de configuration globaux de l'application.
- **`hospital.db`** : Base de données SQLite stockant toutes les informations.

### 📄 Interfaces (Templates)

- **`login.html`** : Système d'authentification, inscription et récupération de mot de passe.
- **`index.html`** : Page d'accueil du dashboard après connexion.
- **`appointments.html`** : Interface de gestion et prise de rendez-vous pour les patients.
- **`users.html`** : Gestion des profils et (pour l'admin) gestion de tous les comptes.
- **`medications.html`** : Suivi et gestion des stocks de médicaments.
- **`sms.html` / `whatsapp.html`** : Interfaces d'envoi et de suivi des messages.
- **`chat.html`** : Module de discussion en temps réel entre utilisateurs.
- **`patient_list.html`** : Vue d'ensemble des patients pour le personnel médical.
- **`prescription.html`** : Interface de création et consultation des ordonnances.

### � Tests & Maintenance

- **`test_app.py`**, **`test_backend.py`**, etc. : Scripts de tests automatisés pour garantir la stabilité du code.
- **`requirements.txt`** : Liste des bibliothèques nécessaires au projet.
- **`Procfile` / `runtime.txt`** : Fichiers de configuration pour le déploiement sur des plateformes comme Heroku ou Render.

---

## 📧 Contact

- **Développeur & Admin** : Facely Diawara
- **Email** : contact@hopitalcentral.sn
