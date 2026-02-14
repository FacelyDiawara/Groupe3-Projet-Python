from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine
from .ai_assistant.service import HealthBotService

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hôpital Central API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure static files and templates
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= WEB ROUTES =================
@app.get("/")
async def home(request: Request):
    """Page d'accueil"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/appointments")
async def appointments_page(request: Request):
    """Page des rendez-vous"""
    return templates.TemplateResponse("appointments.html", {"request": request})

@app.get("/users")
async def users_page(request: Request):
    """Page des docteurs"""
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/medications")
async def medications_page(request: Request):
    """Page des médicaments"""
    return templates.TemplateResponse("medications.html", {"request": request})

@app.get("/sms")
async def sms_page(request: Request):
    """Page SMS"""
    return templates.TemplateResponse("sms.html", {"request": request})

@app.get("/prescription")
async def prescription_page(request: Request):
    """Page d'ordonnance professionnelle"""
    return templates.TemplateResponse("prescription.html", {"request": request})

@app.get("/whatsapp")
async def whatsapp_page(request: Request):
    """Page WhatsApp"""
    return templates.TemplateResponse("whatsapp.html", {"request": request})

@app.get("/chat")
async def chat_page(request: Request):
    """Page de chat"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/patients_list")
async def patients_list_page(request: Request):
    """Page de liste des patients avec ordonnances"""
    return templates.TemplateResponse("patient_list.html", {"request": request})

# ================= API ROUTES =================

@app.post("/doctors/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db=db, doctor=doctor)

@app.get("/doctors/", response_model=List[schemas.Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud.get_doctors(db, skip=skip, limit=limit)
    return doctors

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = crud.delete_doctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}

@app.put("/doctors/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(doctor_id: int, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = crud.update_doctor(db, doctor_id=doctor_id, doctor=doctor)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor


@app.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)

@app.get("/appointments/", response_model=List[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.delete_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

@app.post("/medications/", response_model=schemas.Medication)
def create_medication(medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    return crud.create_medication(db=db, medication=medication)

@app.get("/medications/", response_model=List[schemas.Medication])
def read_medications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medications = crud.get_medications(db, skip=skip, limit=limit)
    return medications

@app.delete("/medications/{medication_id}")
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    db_medication = crud.delete_medication(db, medication_id=medication_id)
    if db_medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": "Medication deleted successfully"}

@app.delete("/medications/")
def delete_all_medications(db: Session = Depends(get_db)):
    crud.delete_all_medications(db)
    return {"message": "All medications deleted successfully"}

@app.post("/reminders/", response_model=schemas.Reminder)
def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    return crud.create_reminder(db=db, reminder=reminder)

@app.get("/reminders/", response_model=List[schemas.Reminder])
def read_reminders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reminders(db, skip=skip, limit=limit)

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    db_reminder = crud.delete_reminder(db, reminder_id=reminder_id)
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder deleted successfully"}

@app.get("/prescriptions/", response_model=List[schemas.Prescription])
def read_prescriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_prescriptions(db, skip=skip, limit=limit)

@app.post("/prescriptions/", response_model=schemas.Prescription)
def create_prescription(prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_prescription(db=db, prescription=prescription)
@app.post("/api/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"📩 Requête d'inscription reçue pour : {user.username}")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        print(f"❌ Utilisateur {user.username} existe déjà")
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")
    result = crud.create_user(db=db, user=user)
    print(f"✅ Utilisateur {user.username} créé avec succès")
    return result

@app.post("/api/login")
async def api_login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"id": db_user.id, "username": db_user.username, "role": db_user.role}
@app.delete("/api/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Account deleted successfully"}

@app.get("/api/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.post("/api/password-recovery")
def recover_password(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    # This simulates finding the user and sending an email
    db_user = db.query(models.User).filter(models.User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email non trouvé")
    return {"message": f"Un lien de récupération a été envoyé à {request.email}", "username": db_user.username}

@app.post("/api/password-reset")
def reset_password(reset: schemas.PasswordReset, db: Session = Depends(get_db)):
    db_user = crud.update_user_password(db, email=reset.email, new_password=reset.new_password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Erreur lors de la réinitialisation")
    return {"message": "Mot de passe mis à jour avec succès"}

# ================= CHAT ROUTES =================

@app.get("/api/chat/conversations", response_model=List[schemas.Conversation])
def get_conversations(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_conversations(db, user_id=user_id)

@app.post("/api/chat/", response_model=schemas.ChatResponse)
async def chat_with_bot(request: schemas.ChatRequest, user_id: int, db: Session = Depends(get_db)):
    # 1. Obtenir ou créer la conversation
    if not request.conversation_id:
        # Créer un titre basé sur le début du message
        title = request.message[:30] + "..." if len(request.message) > 30 else request.message
        conv = crud.create_conversation(db, user_id=user_id, title=title)
        conv_id = conv.id
    else:
        conv_id = request.conversation_id
        conv = crud.get_conversation(db, conversation_id=conv_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")

    # 2. Sauvegarder le message de l'utilisateur
    crud.create_message(db, conversation_id=conv_id, role="user", content=request.message)

    # 3. Récupérer l'historique pour l'IA
    history = []
    for msg in conv.messages:
        history.append({"role": msg.role, "content": msg.content})

    # 4. Appeler le service IA
    ai_result = await HealthBotService.get_ai_response(db, user_id, request.message, history)

    # 5. Sauvegarder la réponse de l'IA
    crud.create_message(db, conversation_id=conv_id, role="assistant", content=ai_result["content"])

    return {
        "response": ai_result["content"],
        "conversation_id": conv_id,
        "suggestions": ai_result["suggestions"]
    }

@app.delete("/api/chat/conversations/{conversation_id}")
def delete_chat(conversation_id: int, db: Session = Depends(get_db)):
    crud.delete_conversation(db, conversation_id=conversation_id)
    return {"message": "Discussion supprimée"}
