from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    specialite = Column(String)
    telephone = Column(String)
    email = Column(String)
    role = Column(String)
    photo_path = Column(String)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    nom_patient = Column(String)
    prenom_patient = Column(String)
    telephone_patient = Column(String)
    sexe_patient = Column(String)
    docteur_name = Column(String)
    date = Column(String) # Stored as string for simplicity in this PyQt context
    heure = Column(String)

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    nom_produit = Column(String)
    dose = Column(String)
    quantite = Column(Integer)
    date_prescription = Column(String)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    nom_patient = Column(String)
    prenom_patient = Column(String)
    telephone_patient = Column(String)
    medicaments = Column(String)
    date_debut = Column(String)
    duree = Column(Integer)
    matin = Column(String)
    soir = Column(String)
    type_canal = Column(String) # "SMS" or "WhatsApp"

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    nom_patient = Column(String)
    prenom_patient = Column(String)
    telephone_patient = Column(String)
    sexe_patient = Column(String)
    nom_docteur = Column(String)
    telephone_docteur = Column(String)
    medicaments = Column(String) # Store as JSON string
    date_prescription = Column(String)
    duree_jours = Column(Integer)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # Admin, Patient, Doctor
    is_active = Column(Integer, default=1)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(String) # Formatted as string for consistency with this project

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String) # "user" or "assistant"
    content = Column(String)
    timestamp = Column(String)

    conversation = relationship("Conversation", back_populates="messages")
