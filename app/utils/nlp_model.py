# nlp_model.py
import os
import pickle
from app.utils.train_model import train_model

model = None
vectorizer = None

def load_model():
    global model, vectorizer

    model_path = "model.pkl"
    vectorizer_path = "vectorizer.pkl"

    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(vectorizer_path, "rb") as f:
            vectorizer = pickle.load(f)
    else:
        # Se não existir ainda, treina e salva
        model, vectorizer = train_model()

def predict_intent(message: str) -> str | None:
    global model, vectorizer

    if not message:
        return None

    if model is None or vectorizer is None:
        load_model()

    message_vectorized = vectorizer.transform([message])
    intent = model.predict(message_vectorized)[0]
    return intent
