import os
import secrets
import shutil
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict, EmailStr
from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI(title="Gestión de Documentos PDF - UCRPA")

# --- Configuración de Seguridad ---
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-ucrpa-key-2026") # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 # 30 días para facilidad de uso inicial

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Configurar CORS (Para permitir la conexión desde el frontend de Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se debe restringir al dominio de la web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Entorno
MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/")
STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/data/documents")

# Asegurarse de que el directorio existe
os.makedirs(STORAGE_PATH, exist_ok=True)

# Clientes MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.pdf_manager_db
documents_collection = db.get_collection("documents")
users_collection = db.get_collection("users")

# Ayuda para serialización
def document_helper(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "upload_date": doc["upload_date"],
        "size_bytes": doc["size_bytes"],
        "agrupacion": doc.get("agrupacion", "General")
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "agrupacion": user["agrupacion"],
        "is_verified": user["is_verified"]
    }

# --- Modelos de Usuario ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    agrupacion: str # Nombre de agrupación o "Personal"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserVerify(BaseModel):
    email: EmailStr
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str
    agrupacion: str

class UserOut(BaseModel):
    email: str
    agrupacion: str
    is_verified: bool

# --- Modelos de Documentos ---
class DocumentOut(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    size_bytes: int
    agrupacion: str

    model_config = ConfigDict(populate_by_name=True)

# --- Utilidades de Seguridad ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la sesión.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await users_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
    if not user.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Usuario no verificado.")
    return user

# --- Endpoints de Autenticación ---

@app.post("/auth/register")
async def register(user_in: UserRegister):
    # Ver si ya existe
    existing_user = await users_collection.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    
    # Generar código de validación (Simulado)
    verification_code = str(secrets.randbelow(899999) + 100000)
    
    user_dict = {
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "agrupacion": user_in.agrupacion,
        "is_verified": False,
        "verification_code": verification_code,
        "created_at": datetime.utcnow()
    }
    
    await users_collection.insert_one(user_dict)
    
    # SIMULACIÓN: Imprimir código en el log del servidor
    print("\n" + "="*50)
    print(f"📧 CÓDIGO DE VERIFICACIÓN PARA {user_in.email}: {verification_code}")
    print("="*50 + "\n")
    
    return {"message": "Registro exitoso. Revise su código de verificación."}

@app.post("/auth/verify")
async def verify(data: UserVerify):
    user = await users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if user.get("verification_code") == data.code:
        await users_collection.update_one(
            {"email": data.email},
            {"$set": {"is_verified": True}, "$unset": {"verification_code": ""}}
        )
        return {"message": "Cuenta verificada con éxito."}
    
    raise HTTPException(status_code=400, detail="Código de verificación incorrecto.")

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    
    if not user.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Verifique su cuenta antes de entrar.")
        
    access_token = create_access_token(data={"sub": user["email"], "agrupacion": user["agrupacion"]})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "agrupacion": user["agrupacion"]
    }

# --- Endpoints Principales Protegidos ---

@app.get("/")
def read_root():
    return {"message": "API Institucional UCRPA funcionando correctamente."}

@app.post("/upload", response_model=DocumentOut)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solamente se permiten archivos PDF.")

    file_location = os.path.join(STORAGE_PATH, file.filename)
    
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    file_size = os.path.getsize(file_location)
    document_data = {
        "filename": file.filename,
        "upload_date": datetime.utcnow(),
        "size_bytes": file_size,
        "agrupacion": current_user["agrupacion"],
        "owner_email": current_user["email"]
    }
    
    new_doc = await documents_collection.insert_one(document_data)
    created_doc = await documents_collection.find_one({"_id": new_doc.inserted_id})
    
    return document_helper(created_doc)


@app.get("/documents", response_model=List[DocumentOut])
async def list_documents(current_user: dict = Depends(get_current_user)):
    docs = []
    # Filtrar por agrupación (Un usuario solo ve lo de su agrupación)
    cursor = documents_collection.find({"agrupacion": current_user["agrupacion"]})
    async for doc in cursor:
        docs.append(document_helper(doc))
    return docs


@app.get("/download/{document_id}")
async def download_document(document_id: str):
    # Buscar el documento en la base de datos
    doc = await documents_collection.find_one({"_id": ObjectId(document_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado en base de datos.")

    file_location = os.path.join(STORAGE_PATH, doc["filename"])
    
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="El archivo físico no existe en el almacenamiento.")
        
    return FileResponse(path=file_location, filename=doc["filename"], media_type='application/pdf')
