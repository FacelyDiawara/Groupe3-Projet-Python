from sqlalchemy.orm import Session
from . import models, schemas

# Doctor Operations
def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
    return db_doctor

def update_doctor(db: Session, doctor_id: int, doctor: schemas.DoctorCreate):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor:
        for key, value in doctor.dict().items():
            setattr(db_doctor, key, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor


# Appointment Operations
def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment

# Medication Operations
def get_medications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Medication).offset(skip).limit(limit).all()

def create_medication(db: Session, medication: schemas.MedicationCreate):
    db_medication = models.Medication(**medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

def delete_medication(db: Session, medication_id: int):
    db_medication = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if db_medication:
        db.delete(db_medication)
        db.commit()
    return db_medication

def delete_all_medications(db: Session):
    db.query(models.Medication).delete()
    db.commit()
    return True

# Reminder Operations
def get_reminders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reminder).offset(skip).limit(limit).all()

def create_reminder(db: Session, reminder: schemas.ReminderCreate):
    db_reminder = models.Reminder(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

def delete_reminder(db: Session, reminder_id: int):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if db_reminder:
        db.delete(db_reminder)
        db.commit()
    return db_reminder

# Prescription Operations
def get_prescriptions(db: Session, skip: int = 0, limit: int = 100):
    # Auto-cleanup before returning the list
    cleanup_expired_prescriptions(db)
    return db.query(models.Prescription).offset(skip).limit(limit).all()

def cleanup_expired_prescriptions(db: Session):
    from datetime import datetime, timedelta
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # We can't easily do timedelta arithmetic in a single SQLite query through SQLAlchemy without more setup,
    # but we can filter better to avoid loading all prescriptions if we have many.
    # For now, let's just make the existing loop slightly cleaner.
    prescriptions = db.query(models.Prescription).all()
    for p in prescriptions:
        try:
            presc_date = datetime.strptime(p.date_prescription, "%d/%m/%Y")
            if today >= presc_date + timedelta(days=p.duree_jours):
                db.delete(p)
        except Exception:
            continue
    db.commit()

def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    db_prescription = models.Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription
