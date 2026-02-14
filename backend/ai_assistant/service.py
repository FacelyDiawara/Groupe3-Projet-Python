import os
import json
from datetime import datetime
from typing import List, Dict, Optional
try:
    from groq import Groq
except ImportError:
    # Si groq n'est pas installé, on pourra utiliser le mode fallback
    Groq = None
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .. import models, crud

load_dotenv()

# Configuration Groq (Alternative gratuite à OpenAI)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = None

if GROQ_API_KEY and Groq:
    print(f"🔑 Tentative d'initialisation Groq avec la clé : {GROQ_API_KEY[:10]}...")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Client Groq initialisé.")
    except Exception as e:
        print(f"Erreur d'initialisation Groq: {e}")
else:
    print("⚠️ Aucune clé Groq valide trouvée ou bibliothèque 'groq' manquante.")

class HealthBotService:
    SYSTEM_PROMPT = """
    Tu es HealthBot, l'assistant intelligent de l'application HealthReminder.
    Ton rôle est d'aider les patients à gérer leurs médicaments, leurs rendez-vous et à rester motivés.
    
    RÈGLES CRUCIALES :
    1. Tu ne REPLACES PAS un professionnel de santé. Ne donne JAMAIS de diagnostic médical.
    2. Ajoute TOUJOURS la mention : "Ce conseil ne remplace pas l'avis d'un professionnel de santé." à la fin de tes réponses si elles concernent la santé.
    3. Sois empathique, professionnel et encourageant.
    4. Réponds en français de manière claire et concise.
    5. Utilise les données fournies sur le patient pour personnaliser tes réponses.
    """

    @staticmethod
    def detect_intent(message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ["médicament", "cachet", "dose", "prise", "ordonnance"]):
            return "medications"
        if any(w in msg for w in ["rendez-vous", "rdv", "docteur", "visite", "consultation"]):
            return "appointments"
        if any(w in msg for w in ["fatigué", "moral", "motivation", "triste", "peur", "aider"]):
            return "motivation"
        return "general"

    @staticmethod
    def get_user_context(db: Session, user_id: int) -> str:
        # Récupérer les infos du patient
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return "Utilisateur invité (Données limitées)."

        context = f"Utilisateur: {user.username} (Rôle: {user.role})\n"
        
        # Récupérer les médicaments
        meds = db.query(models.Medication).all()
        if meds:
            context += "\nPRODUITS/MÉDICAMENTS ACTUELS :\n"
            for m in meds:
                context += f"- {m.nom_produit}: {m.dose} (Quantité: {m.quantite})\n"
        
        # Récupérer les rendez-vous
        appts = db.query(models.Appointment).all()
        if appts:
            context += "\nRENDEZ-VOUS PRÉVUS :\n"
            for a in appts:
                context += f"- Avec Dr {a.docteur_name} le {a.date} à {a.heure}\n"
        
        return context

    @staticmethod
    async def get_ai_response(db: Session, user_id: int, message: str, history: List[Dict]) -> Dict:
        intent = HealthBotService.detect_intent(message)
        
        # Suggestions par défaut basées sur l'intention
        suggestions = []
        if intent == "medications":
            suggestions = ["Comment prendre ma dose ?", "Quels sont mes rappels ?"]
        elif intent == "appointments":
            suggestions = ["Qui est mon docteur ?", "Modifier mon RDV"]
        elif intent == "motivation":
            suggestions = ["Donne-moi un conseil santé", "Comment rester en forme ?"]
        else:
            suggestions = ["Mes médicaments", "Mes rendez-vous", "Besoin d'aide"]

        # Si pas de client configuré, utiliser des réponses prédéfinies
        if client is None:
            user_context = HealthBotService.get_user_context(db, user_id)
            mock_response = "Désolé, l'assistant IA n'est pas encore configuré. "
            mock_response += "\n\nCependant, je détecte que vous demandez des informations sur : " + intent.upper()
            return {
                "content": mock_response + "\n\nCe conseil ne remplace pas l'avis d'un professionnel de santé.",
                "suggestions": suggestions
            }

        user_context = HealthBotService.get_user_context(db, user_id)
        
        # Construction des messages
        messages = [
            {"role": "system", "content": HealthBotService.SYSTEM_PROMPT},
            {"role": "system", "content": f"CONTEXTE PATIENT ACTUEL :\n{user_context}"}
        ]
        
        # Limiter l'historique aux 5 derniers messages
        messages.extend(history[-5:])
        messages.append({"role": "user", "content": message})
        
        try:
            # Utilisation de Groq avec le modèle Llama 3
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content
            
            return {
                "content": ai_content,
                "suggestions": suggestions
            }
        except Exception as e:
            print(f"Erreur Groq: {e}")
            return {
                "content": "Désolé, je rencontre une petite difficulté technique avec Groq. Veuillez réessayer.\n\nCe conseil ne remplace pas l'avis d'un professionnel de santé.",
                "suggestions": ["Réessayer"]
            }
