FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicacion
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
