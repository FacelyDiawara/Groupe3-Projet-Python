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
