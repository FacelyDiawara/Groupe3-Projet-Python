# CAHIER DES CHARGES : Système de Gestion Hospitalière "Hôpital Central"

 Présentation du Projet
Le projet **Hôpital Central** est une solution numérique intégrée conçue pour moderniser la gestion des services hospitaliers. Il vise à simplifier les interactions entre le personnel médical et les patients tout en assurant un suivi rigoureux des traitements grâce à des outils de communication automatisés.

###  Objectifs principaux
*   **Centralisation des données** : Regrouper les informations des patients, docteurs, rendez-vous et prescriptions dans une base de données unique.
*   **Automatisation du suivi** : Mettre en place un système de rappels automatiques (SMS/WhatsApp) pour améliorer l'observance des traitements par les patients.
*   **Amélioration de la communication** : Offrir un canal de discussion en temps réel entre le personnel et les usagers.
*   **Gestion sécurisée** : Garantir que chaque type d'utilisateur accède uniquement aux fonctionnalités qui lui correspondent .

## 2. Analyse Fonctionnelle

### 2.1 Rôles des Utilisateurs
L'application distingue trois types d'utilisateurs clés :
1.  **Administrateur** : Gestion complète des comptes, supervision des docteurs et maintenance du système.
2.  **Docteur** : Consultation des dossiers patients, gestion des rendez-vous, création de prescriptions et validation des traitements.
3.  **Patient** : Prise de rendez-vous, consultation de ses propres informations et réception de rappels.

### 2.2 Fonctionnalités Majeures

#### 2.2.1 Système de Rappels Automatisés (Cœur du projet)
L'élément différenciateur du projet est sa capacité à notifier les patients pour la prise de leur traitement :
*   **Canal SMS** : Utilisation d'une API de messagerie pour envoyer des rappels texte directs sur le mobile du patient.
*   **Canal WhatsApp** : Intégration pour envoyer des notifications enrichies via WhatsApp, favorisant une lecture rapide.
*   **Paramétrage** : Le personnel soignant définit la fréquence (matin, soir), la durée du traitement et le message spécifique.

#### 2.2.2 Flux de Prescription et Médicaments
*   **Gestion de l'inventaire** : Suivi en temps réel des quantités de médicaments disponibles.
*   **Génération de PDF** : Une fois la consultation terminée, le système génère une ordonnance officielle au format PDF incluant le logo de l'hôpital, le nom du docteur, les médicaments prescrits et la durée.
*   **Interconnexion** : Les médicaments ajoutés à la prescription sont automatiquement décomptés du stock et programmés dans le système de rappel.

#### 2.2.3 Module de Chat et Discussion
*   **Communication Directe** : Permet aux patients de poser des questions sur leurs effets secondaires ou de clarifier une posologie sans se déplacer.
*   **Historique** : Les échanges sont conservés pour permettre au docteur de suivre l'évolution du dialogue avec le patient.

#### 2.2.4 Gestion de la Sécurité et Confidentialité (RBAC)
*   **Rôles (RBAC)** : 
    *   *Admin* : Accès au panneau de contrôle total (CRUD utilisateurs).
    *   *Docteur* : Accès aux dossiers médicaux et outils de prescription.
    *   *Patient* : Accès restreint à ses propres rendez-vous et profil.
*   **Comptes Éphémères** : Pour renforcer la protection des données personnelles, les comptes de type "Patient" peuvent être configurés pour être supprimés automatiquement après la session ou le traitement.

## 3. Spécifications Techniques

### 3.1 Architecture du Système
Le projet utilise une architecture **Client-Serveur** découplée :
*   **Backend** : API REST performante utilisant FastAPI.
*   **Frontend** : Double interface :
    *   **Web** : Interface basée sur Jinja2, HTML5/CSS3/JS pour une accessibilité universelle.
    *   **Desktop** : Application lourde développée en PyQt5 pour un usage interne plus fluide.

### 3.2 Stack Technologique
| Composant | Technologie |
| **Langage** | Python 3.10+ |
| **Framework Backend** | FastAPI |
| **Base de Données** | SQLite |
| **GUI Desktop** | PyQt5 |
| **Web UI** | HTML5, CSS3, JavaScript (Vanilla), Jinja2 |
| **Notification** | Services SMS & WhatsApp |

### 3.3 Modèle de Données (Base de données)
La base `hospital.db` est structurée autour des entités suivantes :
*   **Users** : Identifiants, rôles, emails.
*   **Doctors** : Nom, spécialité, téléphone, chemin de photo.
*   **Appointments** : Patient, docteur, date et heure.
*   **Medications** : Nom du produit, dosage, quantité disponible.
*   **Prescriptions** : Détails des médicaments prescrits, durée du traitement.
*   **Reminders** : Planification des notifications (matin/soir, canal choisi).

## 4. Design et Ergonomie
*   **Esthétique** : Design moderne avec une palette de couleurs "Entreprise" (Bleu, Gris ardoise, Blanc).
*   **Responsive** : Les interfaces web s'adaptent aux différents formats d'écran.
*   **Expérience Utilisateur (UX)** : Barre de navigation intuitive, tableaux de données clairs et formulaires avec validation en temps réel.

## 5. Déploiement et Maintenance
*   **Conteneurisation** : Présence de `Procfile` et `runtime.txt` pour un déploiement facilité sur Heroku/Render.
*   **Tests** : Suite de tests automatisés (`test_app.py`, `test_backend.py`) pour vérifier l'intégrité des routes API et de la logique métier.
*   **Logs** : Système de journalisation interne (`backend.log`, `server_log.txt`) pour le monitoring des erreurs.

## 6. Structure du Projet
```text
Groupe3-Projet-Python/
├── backend/            # Cœur logique (FastAPI, CRUD, Modèles)
├── templates/          # Interfaces Web (HTML/Jinja2)
├── static/             # Assets Web (CSS, JS)
├── pages/              # Modules UI PyQt5
├── assets/             # Images et ressources graphiques
├── hospital.db         # Base de données SQLite
├── run_app.py          # Orchestrateur de lancement
└── CAHIER_DES_CHARGES  # Présent document
```

## 7. Workflow Utilisateur Type
1.  **Inscription/Connexion** : Le patient ou le docteur s'authentifie.
2.  **Prise de RDV** : Le patient choisit un docteur et une plage horaire.
3.  **Consultation** : Le docteur saisit les médicaments et la posologie.
4.  **Validation** : Le système génère le PDF de l'ordonnance et décrémente les stocks.
5.  **Programmation** : Les rappels SMS/WhatsApp sont planifiés dans le module `messaging_service`.
6.  **Suivi** : Le patient reçoit ses alertes quotidiennes et peut discuter via le chat si besoin.
**Date de mise à jour** : 27 Février 2026
**Auteurs** : DIAWARA Facely, DIALLO Hassanatou, DIALLO Nene Aissatou, KOUROUMA Solo.


