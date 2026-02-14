from pydantic import BaseModel
from typing import Optional, List

# Doctor schemas
class DoctorBase(BaseModel):
    nom: str
    prenom: str
    specialite: str
    telephone: str
    email: str
    role: Optional[str] = "Docteur"
    photo_path: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True

# Appointment schemas
class AppointmentBase(BaseModel):
    nom_patient: str
    prenom_patient: str
    telephone_patient: str
    sexe_patient: str
    docteur_name: str
    date: str
    heure: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True

# Medication schemas
class MedicationBase(BaseModel):
    nom_produit: str
    dose: str
    quantite: int
    date_prescription: str

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int

    class Config:
        orm_mode = True

# Reminder schemas
class ReminderBase(BaseModel):
    nom_patient: str
    prenom_patient: str
    telephone_patient: str
    medicaments: str
    date_debut: str
    duree: int
    matin: str
    soir: str
    type_canal: str

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int

    class Config:
        orm_mode = True

# Prescription schemas
class PrescriptionBase(BaseModel):
    nom_patient: str
    prenom_patient: str
    telephone_patient: str
    sexe_patient: str
    nom_docteur: str
    telephone_docteur: str
    medicaments: str
    date_prescription: str
    duree_jours: int

class PrescriptionCreate(PrescriptionBase):
    pass

class Prescription(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True
# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PasswordReset(BaseModel):
    username: str
    new_password: str
    email: str

class PasswordResetRequest(BaseModel):
    email: str

class User(UserBase):
    id: int
    is_active: int

    class Config:
        orm_mode = True

# Chat Schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    role: str

class Message(MessageBase):
    id: int
    role: str
    timestamp: str

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    title: Optional[str] = "Nouvelle Discussion"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: str
    messages: List[Message] = []

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    suggestions: List[str] = []
