FROM python:3.10-slim

# Crée le dossier de travail dans l'image Docker
WORKDIR /app

# Copie les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le dossier app dans /app/app
COPY app ./app
WORKDIR /app

# Exécute FastAPI depuis app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
