from fastapi import FastAPI
from pydantic import BaseModel
from app.models.fan_interaction import Fan, Interaction  # importa os modelos que você criou
from app.models.message import Message
from datetime import datetime
from typing import List

app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0")

# Lista para armazenar o histórico de mensagens
message_history = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    user_msg = msg.message.lower()
    bot_reply = ""

    # Lógica de resposta
    if "oi" in user_msg:
        bot_reply = "Fala, torcedor da FURIA! 💥"
    elif "seu time favorito" in user_msg:
        bot_reply = "É claro que é a FURIA, né! 🦁"
    elif "quando é o próximo jogo" in user_msg:
        bot_reply = "Fique ligado nas redes da FURIA, tem jogo em breve! 🎮"
    elif "qual seu nome" in user_msg:
        bot_reply = f"Meu nome é Chatbot FURIA! 😎"
    elif "como você está?" in user_msg:
        bot_reply = "Estou bem, obrigado! E você? 😁"
    else:
        bot_reply = "Não entendi muito bem, mas tamo junto, FURIA sempre! 🔥"

    # Salvar a mensagem no histórico
    message_history.append({
        "user": msg.user,
        "message": bot_reply,
        "timestamp": datetime.now()
    })

    response = {
        "user": msg.user,
        "message": bot_reply,
        "timestamp": datetime.now()
    }
    return response

@app.get("/history")
def get_history():
    return {"history": message_history}
