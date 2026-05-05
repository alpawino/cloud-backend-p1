from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import models
from passlib.context import CryptContext
fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"])
# Crear las tablas si no existen
print("🔨 Creando tablas si no existen...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas listas")
db: Session = SessionLocal()
def hash_password(password):
    return pwd_context.hash(password)
# OPTIMIZACIÓN: Hashear la contraseña UNA SOLA VEZ fuera del bucle
hashed_pwd = hash_password("123456")
for i in range(20000):
    user = models.User(
        name=fake.name(),
        email=fake.unique.email(),
        password=hashed_pwd
    )
    db.add(user)
    # Guardar en lotes de 1000 para no perder todo si falla
    if (i + 1) % 1000 == 0:
        db.commit()
        print(f"✅ {i + 1} usuarios insertados...")
db.commit()
db.close()
print("🎉 20,000 usuarios insertados")