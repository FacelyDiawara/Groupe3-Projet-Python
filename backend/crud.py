from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# User Operations
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=1
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
    from datetime import datetime
    today = datetime.now().strftime("%d/%m/%Y")
    
    # In SQLite, we can't easily do date math in strings, but we can filter
    # For simplicity and reliability, we'll keep the logic but make it more efficient if possible.
    # Actually, the previous logic was parsing EVERY date. 
    # Let's optimize it by only fetching what we need to check, or doing a bulk delete if possible.
    
    prescriptions = db.query(models.Prescription).all()
    current_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    to_delete = []
    for p in prescriptions:
        try:
            presc_date = datetime.strptime(p.date_prescription, "%d/%m/%Y")
            expiry_date = presc_date + timedelta(days=p.duree_jours)
            if current_time >= expiry_date:
                to_delete.append(p.id)
        except Exception:
            continue
            
    if to_delete:
        db.query(models.Prescription).filter(models.Prescription.id.in_(to_delete)).delete(synchronize_session=False)
        db.commit()

def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    db_prescription = models.Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def delete_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_password(db: Session, email: str, new_password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(db_user)
    return db_user

# Chat CRUD
def create_conversation(db: Session, user_id: int, title: str = "Nouvelle Discussion"):
    from datetime import datetime
    db_conv = models.Conversation(
        user_id=user_id,
        title=title,
        created_at=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: int):
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).order_by(models.Conversation.id.desc()).all()

def create_message(db: Session, conversation_id: int, role: str, content: str):
    from datetime import datetime
    db_msg = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        timestamp=datetime.now().strftime("%H:%M")
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def delete_conversation(db: Session, conversation_id: int):
    db_conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if db_conv:
        db.delete(db_conv)
        db.commit()
    return db_conv
