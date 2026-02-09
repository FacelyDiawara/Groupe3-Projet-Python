# Guide de Déploiement - Hôpital Central

Ce guide explique comment déployer l'application Hôpital Central sur différentes plateformes cloud gratuites.

## Option 1 : Render.com (Recommandé)

Render offre un hébergement gratuit pour les applications web Python.

### Étapes :

1. **Créer un compte sur Render**
   - Allez sur [render.com](https://render.com)
   - Inscrivez-vous avec votre compte GitHub

2. **Connecter votre repository GitHub**
   - Créez un repository sur GitHub avec votre code
   - Connectez Render à votre compte GitHub

3. **Créer un nouveau Web Service**
   - Cliquez sur "New +" → "Web Service"
   - Sélectionnez votre repository
   - Configurez :
     - **Name** : `hopital-central`
     - **Environment** : `Python 3`
     - **Build Command** : `pip install -r requirements.txt`
     - **Start Command** : `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
     - **Plan** : Free

4. **Déployer**
   - Cliquez sur "Create Web Service"
   - Attendez quelques minutes
   - Votre application sera accessible à : `https://hopital-central.onrender.com`

---

## Option 2 : Railway.app

Railway est une autre excellente option gratuite.

### Étapes :

1. **Créer un compte sur Railway**
   - Allez sur [railway.app](https://railway.app)
   - Inscrivez-vous avec GitHub

2. **Nouveau Projet**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

3. **Configuration**
   - Railway détecte automatiquement Python
   - Ajoutez une variable d'environnement :
     - `PORT` = `8000`

4. **Déployer**
   - Le déploiement se fait automatiquement
   - Votre URL sera : `https://hopital-central.up.railway.app`

---

## Option 3 : PythonAnywhere

Spécialisé pour les applications Python.

### Étapes :

1. **Créer un compte**
   - Allez sur [pythonanywhere.com](https://www.pythonanywhere.com)
   - Créez un compte gratuit

2. **Télécharger le code**
   - Ouvrez un bash console
   - Clonez votre repository :
     ```bash
     git clone https://github.com/votre-username/hopital-central.git
     cd hopital-central
     ```

3. **Installer les dépendances**

   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configurer Web App**
   - Allez dans l'onglet "Web"
   - Créez une nouvelle web app
   - Choisissez "Manual configuration"
   - Python 3.10

5. **Configurer WSGI**
   - Éditez le fichier WSGI
   - Ajoutez :

     ```python
     import sys
     path = '/home/yourusername/hopital-central'
     if path not in sys.path:
         sys.path.append(path)

     from backend.main import app as application
     ```

6. **Recharger**
   - Cliquez sur "Reload"
   - Votre app sera à : `https://yourusername.pythonanywhere.com`

---

## Variables d'Environnement (Optionnel)

Pour les fonctionnalités SMS/WhatsApp, ajoutez ces variables :

- `TWILIO_ACCOUNT_SID` : Votre Twilio Account SID
- `TWILIO_AUTH_TOKEN` : Votre Twilio Auth Token
- `TWILIO_PHONE_NUMBER` : Votre numéro Twilio

---

## Mise à Jour de l'Application

### Sur Render/Railway :

- Poussez vos changements sur GitHub
- Le déploiement se fait automatiquement

### Sur PythonAnywhere :

```bash
cd hopital-central
git pull
# Rechargez l'application depuis le dashboard
```

---

## Dépannage

### L'application ne démarre pas

- Vérifiez les logs de déploiement
- Assurez-vous que `requirements.txt` est à jour
- Vérifiez que le port est correctement configuré

### Base de données vide

- SQLite crée automatiquement la base au premier lancement
- Les tables sont créées automatiquement par SQLAlchemy

### Erreur CORS

- Vérifiez que CORS est activé dans `backend/main.py`
- Les origines sont configurées pour accepter toutes les requêtes

---

## Support

Pour toute question, ouvrez une issue sur GitHub.
