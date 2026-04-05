import os
import shutil
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict
from bson import ObjectId

app = FastAPI(title="Gestión de Documentos PDF")

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

# Cliente MongoDB (Motor)
client = AsyncIOMotorClient(MONGO_URI)
db = client.pdf_manager_db
documents_collection = db.get_collection("documents")

# === Modelos de Pydantic ===
class DocumentOut(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    size_bytes: int

    model_config = ConfigDict(populate_by_name=True)

# Función de ayuda para serializar el _id de Mongo a string
def document_helper(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "upload_date": doc["upload_date"],
        "size_bytes": doc["size_bytes"],
    }

# === Endpoints Principales ===

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Documentos PDF funcionando correctamente."}

@app.post("/upload", response_model=DocumentOut)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solamente se permiten archivos PDF.")

    file_location = os.path.join(STORAGE_PATH, file.filename)
    
    # 1. Guardar archivo físico en el volumen
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    # 2. Registrar en la base de datos
    file_size = os.path.getsize(file_location)
    document_data = {
        "filename": file.filename,
        "upload_date": datetime.utcnow(),
        "size_bytes": file_size,
    }
    
    # Insertar y devolver el mismo objeto con su nuevo ID
    new_doc = await documents_collection.insert_one(document_data)
    created_doc = await documents_collection.find_one({"_id": new_doc.inserted_id})
    
    return document_helper(created_doc)


@app.get("/documents", response_model=List[DocumentOut])
async def list_documents():
    docs = []
    cursor = documents_collection.find()
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
