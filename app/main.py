# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Inisialisasi FastAPI
app = FastAPI(title="Klasifikasi Teks API", 
              description="API untuk klasifikasi teks sederhana",
              version="1.0.0")

# Model dan data kelas
MODEL_PATH = os.environ.get("MODEL_PATH", "model/")
CLASSES = ["positif", "negatif", "netral"]

# Cek apakah model sudah ada, jika tidak buat model dummy
if not os.path.exists(f"{MODEL_PATH}model.joblib") or not os.path.exists(f"{MODEL_PATH}vectorizer.joblib"):
    # Buat direktori model jika belum ada
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    # Data training sederhana
    texts = [
        "saya sangat senang hari ini", 
        "produk ini sangat bagus", 
        "pelayanan yang memuaskan",
        "saya tidak suka dengan produk ini", 
        "pelayanan yang buruk", 
        "pengalaman yang mengecewakan",
        "barang ini biasa saja", 
        "tidak ada komentar", 
        "standar saja"
    ]
    
    labels = [0, 0, 0, 1, 1, 1, 2, 2, 2]  # 0: positif, 1: negatif, 2: netral
    
    # Training model sederhana
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X, labels)
    
    # Simpan model dan vectorizer
    joblib.dump(model, f"{MODEL_PATH}model.joblib")
    joblib.dump(vectorizer, f"{MODEL_PATH}vectorizer.joblib")
else:
    # Muat model dan vectorizer jika sudah ada
    model = joblib.load(f"{MODEL_PATH}model.joblib")
    vectorizer = joblib.load(f"{MODEL_PATH}vectorizer.joblib")

# Definisikan model request
class TextRequest(BaseModel):
    text: str

# Definisikan model response
class PredictionResponse(BaseModel):
    text: str
    predicted_class: str
    confidence: float

# Route untuk health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Route untuk prediksi
@app.post("/predict", response_model=PredictionResponse)
def predict(request: TextRequest):
    try:
        # Transformasi teks
        text_vectorized = vectorizer.transform([request.text])
        
        # Prediksi
        prediction = model.predict(text_vectorized)[0]
        confidence = np.max(model.predict_proba(text_vectorized)[0])
        
        # Return hasil
        return {
            "text": request.text,
            "predicted_class": CLASSES[prediction],
            "confidence": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes dokumentasi akan tersedia di /docs secara otomatis (Swagger UI)