from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend import crud, schemas

def create_admin():
    db = SessionLocal()
    try:
        # Check if user already exists
        db_user = crud.get_user_by_username(db, username="Facely Diawara")
        if db_user:
            print("❌ Admin 'Facely Diawara' already exists.")
            return

        admin_data = schemas.UserCreate(
            username="Facely Diawara",
            password="Facely@",
            email="lelemandou626@gmail.com",
            role="Admin"
        )
        crud.create_user(db=db, user=admin_data)
        print("✅ Admin 'Facely Diawara' created successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
