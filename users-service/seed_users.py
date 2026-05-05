from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from passlib.context import CryptContext

fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"])

db: Session = SessionLocal()

def hash_password(password):
    return pwd_context.hash(password)

for i in range(20000):
    user = models.User(
        name=fake.name(),
        email=fake.unique.email(),
        password=hash_password("123456")
    )
    db.add(user)

    if i % 1000 == 0:
        print(f"{i} usuarios insertados...")

db.commit()
db.close()

print("✅ 20,000 usuarios insertados")