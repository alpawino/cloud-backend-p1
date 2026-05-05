import time
import pymysql

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import SessionLocal, Base, engine
from app import crud, schemas, models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔁 Esperar a MySQL (clave en Docker)
def wait_for_db():
    while True:
        try:
            conn = pymysql.connect(
                host="mysql",   # 👈 nombre del servicio en docker-compose
                user="root",
                password="root",
                database="usersdb"
            )
            conn.close()
            print("✅ MySQL listo")
            break
        except Exception as e:
            print("⏳ Esperando MySQL...", e)
            time.sleep(3)


@app.on_event("startup")
def startup_event():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    print("🚀 API lista")


# 📦 Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🧪 ROOT
@app.get("/")
def read_root():
    return {"message": "API funcionando 🚀"}


# 👤 REGISTER
@app.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya existe")

    db_user = crud.create_user(db, user)

    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email
    }


# 🔐 LOGIN
@app.post("/auth/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user or not crud.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "message": "Login exitoso",
        "user_id": db_user.id
    }


# 📋 GET USERS
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# 👤 GET USER BY ID
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }