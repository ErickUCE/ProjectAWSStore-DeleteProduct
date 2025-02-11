from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
from dotenv import load_dotenv, find_dotenv
import os

# 📌 Forzar la carga del archivo `.env`
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    print("⚠️ No se encontró el archivo .env")

# 📌 Imprimir las variables para verificar
print("🔍 DB_HOST:", os.getenv("DB_HOST"))
print("🔍 DB_USER:", os.getenv("DB_USER"))
print("🔍 DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("🔍 DB_NAME:", os.getenv("DB_NAME"))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")  # ✅ Evitar None
DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)  # ✅ Codificar contraseña

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Crear la URL de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
