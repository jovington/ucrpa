from fastapi import FastAPI

app = FastAPI(title="Gestión de Documentos PDF")

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Documentos PDF funcionando correctamente"}
