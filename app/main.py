from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.models.fan_interaction import Fan, Interaction
from app.models.message import Message
from datetime import datetime
from typing import List
from app.database import create_db, save_message



from telegram import Update, Bot
import os
import asyncio

# INICIA A API
app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0"
)

# Cria o banco de dados se ainda não existir
create_db()


# Lista para armazenar o histórico de mensagens
message_history = []

# SEU TOKEN DO TELEGRAM (substitua aqui pelo token NOVO)
TELEGRAM_TOKEN = "7808482091:AAGCW7FlKrh_eXgWHRKKADDCRJJtKpW1R70"
bot = Bot(token=TELEGRAM_TOKEN)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    user_msg = msg.message.lower()
    bot_reply = ""

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

    message_history.append({
        "user": msg.user,
        "message": bot_reply,
        "timestamp": datetime.now()
    })

    return {
        "user": msg.user,
        "message": bot_reply,
        "timestamp": datetime.now()
    }

@app.get("/history")
def get_history():
    return {"history": message_history}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    # Recebe os dados do Telegram
    data = await req.json()
    update = Update.de_json(data, bot)
    
    message_text = update.message.text.lower()

    # Lógica do chatbot
    reply = ""
    if "oi" in message_text:
        reply = "Fala, torcedor da FURIA! 💥"
    elif "seu time favorito" in message_text:
        reply = "É claro que é a FURIA, né! 🦁"
    elif "quando é o próximo jogo" in message_text:
        reply = "Fique ligado nas redes da FURIA, tem jogo em breve! 🎮"
    elif "qual seu nome" in message_text:
        reply = "Meu nome é Chatbot FURIA! 😎"
    elif "como você está?" in message_text:
        reply = "Estou bem, obrigado! E você? 😁"
    else:
        reply = "Não entendi muito bem, mas tamo junto, FURIA sempre! 🔥"

    # Salva no banco
    save_message(
        user_id=update.message.chat.id,
        message=message_text,
        response=reply
    )

    # Envia a resposta para o Telegram
    await bot.send_message(chat_id=update.message.chat.id, text=reply)


    return {"ok": True}
    
