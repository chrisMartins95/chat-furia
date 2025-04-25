from fastapi import FastAPI
from pydantic import BaseModel
from app.models.fan_interaction import Fan, Interaction  # importa os modelos que você criou
from app.models.message import Message
from datetime import datetime

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    response = {
        "user": "Chatbot FURIA",
        "message": f"Oi {msg.user}, recebi sua mensagem: '{msg.message}'. GG!",
        "timestamp": datetime.now()
    }
    return response
