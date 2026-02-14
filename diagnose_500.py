import bcrypt
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Test bcrypt and passlib
try:
    print("Testing bcrypt and passlib...")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = "test_password"
    hashed = pwd_context.hash(password)
    print(f"Hash successful: {hashed[:20]}...")
    verified = pwd_context.verify(password, hashed)
    print(f"Verification successful: {verified}")
except Exception as e:
    print(f"❌ Error with bcrypt/passlib: {e}")

# Test database connection
try:
    print("\nTesting database connection...")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./hospital.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # Try a simple query
    from sqlalchemy import text
    result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = [row[0] for row in result]
    print(f"Tables found: {tables}")
    db.close()
except Exception as e:
    print(f"❌ Error with database: {e}")

if __name__ == "__main__":
    print("\nDiagnostic complete.")
