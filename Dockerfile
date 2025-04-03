FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Buat folder model
RUN mkdir -p /app/model

# Copy semua kode aplikasi
COPY app/ /app/

# Port untuk FastAPI
EXPOSE 8000

# Lingkungan (development/production)
ENV ENVIRONMENT=production
ENV MODEL_PATH=/app/model/

# Jalankan FastAPI dengan uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]