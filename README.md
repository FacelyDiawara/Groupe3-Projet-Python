# 🏥 Hôpital Central - Système de Gestion Hospitalière

Une application web complète de gestion hospitalière avec système de rappel automatique pour les patients.

## 🌐 Utiliser l'Application

**Accès direct en ligne** http://127.0.0.1:8000
Cliquez sur le lien et commencez à utiliser l'application. **Aucune installation requise !**

---

## 📂 Code Source

Le code source est disponible sur ce repository pour consultation, étude et contribution.

### Technologies Utilisées

- **Backend** : Python (FastAPI, SQLAlchemy)
- **Frontend** : Jinja2 Templates, HTML5, CSS3, JavaScript
- **Base de données** : SQLite
- **Messagerie** : Twilio (SMS/WhatsApp)
- **Génération PDF** : ReportLab

---

## ✨ Fonctionnalités

- ✅ **Gestion des Patients** : Enregistrement et suivi des patients
- ✅ **Gestion des Docteurs** : Base de données des médecins disponibles
- ✅ **Rendez-vous** : Planification et gestion des rendez-vous
- ✅ **Prescriptions** : Gestion des médicaments et prescriptions
- ✅ **Rappels Automatiques** : Envoi de SMS et WhatsApp aux patients
- ✅ **Discussion** : Interface de chat patient-docteur
- ✅ **Interface Moderne** : Design responsive et professionnel

---

## 🚀 Installation Locale (Pour Développeurs)

Si vous souhaitez exécuter l'application localement pour le développement :

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le repository**

   ```bash
   git clone https://github.com/FacelyDiawara/Groupe3-Projet-Python.git
   cd hopital-central
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv .venv
   ```

3. **Activer l'environnement virtuel**
   - Windows :
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac :
     ```bash
     source .venv/bin/activate
     ```

4. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

5. **Lancer l'application**
   ```bash
   python run_app.py
   ```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://127.0.0.1:8000`

---

## 📁 Structure du Projet

```
hopital-central/
├── backend/              # API FastAPI
│   ├── main.py          # Routes et configuration
│   ├── models.py        # Modèles de base de données
│   ├── schemas.py       # Schémas Pydantic
│   ├── crud.py          # Opérations CRUD
│   └── database.py      # Configuration DB
├── templates/           # Templates Jinja2
│   ├── base.html       # Template de base
│   ├── index.html      # Page d'accueil
│   ├── appointments.html
│   ├── users.html
│   ├── medications.html
│   ├── sms.html
│   ├── whatsapp.html
│   └── chat.html
├── static/             # Fichiers statiques
│   ├── css/
│   │   └── style.css   # Styles CSS
│   └── js/
│       └── app.js      # JavaScript
├── assets/             # Images et ressources
├── run_app.py          # Script de lancement
└── requirements.txt    # Dépendances Python
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👨‍💻 Auteur

**Bintou** - Projet Académique

---

## 📞 Contact

Pour toute question ou suggestion :

- Email : contact@hopitalcentral.sn
- Urgences : 15

---

## 🙏 Remerciements

Merci à tous ceux qui ont contribué à ce projet et aux technologies open source utilisées.
