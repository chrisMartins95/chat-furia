from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.models.fan_interaction import Fan, Interaction
from app.models.message import Message
from datetime import datetime
from typing import List
from app.database import create_db, save_message
import spacy
from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
import os
import asyncio
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Definir as intenções
intents = {
    "greeting": ["oi", "olá", "bom dia", "boa tarde", "e aí", "oi chatbot", "salve"],
    "favorite_team": ["qual seu time favorito?", "quem é seu time?", "time favorito"],
    "next_game": ["quando é o próximo jogo?", "qual o próximo jogo?", "tem jogo logo?"],
    "bot_name": ["qual seu nome?", "como te chamo?", "qual é o seu nome?"],
    "how_are_you": ["como você está?", "tudo bem?", "como você tá?", "tá bem?"],
}

# Preparação dos dados
X = []
y = []
for intent, examples in intents.items():
    for example in examples:
        X.append(example)
        y.append(intent)

# Vetoriza as mensagens para usar como input no modelo
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

# Treinando o modelo
model = LogisticRegression()
model.fit(X, y)

# Função para prever a intenção
def predict_intent(message: str):
    message_vectorized = vectorizer.transform([message])
    intent = model.predict(message_vectorized)[0]
    return intent

# INICIA A API
app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0"
)

# Carrega o modelo de NLP em português
nlp = spacy.load("pt_core_news_sm")

# Cria o banco de dados se ainda não existir
create_db()

# Lista para armazenar o histórico de mensagens
message_history = []

# SEU TOKEN DO TELEGRAM (substitua pelo seu)
TELEGRAM_TOKEN = "7808482091:AAGCW7FlKrh_eXgWHRKKADDCRJJtKpW1R70"
bot = Bot(token=TELEGRAM_TOKEN)

# Armazenando dados do usuário
user_data = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    user_msg = msg.message.lower()
    bot_reply = gerar_resposta(user_msg)

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

# Função para gerar resposta com NLP
def gerar_resposta(message_text: str) -> str:
    # Prever a intenção da mensagem
    intent = predict_intent(message_text)

    # Respostas baseadas na intenção
    if intent == "greeting":
        reply = "Fala, torcedor da FURIA! 💥 Vamos nos conhecer melhor! Qual seu nome?"
    elif intent == "favorite_team":
        reply = "É claro que é a FURIA, né! 🦁"
    elif intent == "next_game":
        reply = "Fique ligado nas redes da FURIA, tem jogo em breve! 🎮"
    elif intent == "bot_name":
        reply = "Meu nome é Chatbot FURIA! 😎"
    elif intent == "how_are_you":
        reply = "Estou bem, obrigado! E você? 😁"
    else:
        reply = "Não entendi muito bem, mas tamo junto, FURIA sempre! 🔥"

    return reply

# Função para enviar o menu de opções
def send_menu(chat_id):
    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Qual seu time favorito?"), KeyboardButton("Quando é o próximo jogo?")],
            [KeyboardButton("Fale sobre a FURIA"), KeyboardButton("Quem são os jogadores da FURIA?")],
            [KeyboardButton("Quais torneios a FURIA está participando?")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    bot.send_message(
        chat_id=chat_id,
        text="Agora que já te conheço melhor, vamos começar a conversa! Escolha uma opção abaixo:",
        reply_markup=menu
    )

# Função para coletar as informações do usuário
async def collect_user_data(chat_id):
    # Pergunta o nome
    bot.send_message(chat_id, "Qual o seu nome, gamer? 😎")
    
    user_data[chat_id] = {"name": None, "age": None, "city": None, "social_network": None, "nickname": None, "preferred_name": None}

# Dicionário para guardar o progresso de cada usuário
user_state = {}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    message = update.message.text.strip()
    chat_id = update.message.chat.id

    # Inicia dados do usuário se ainda não existir
    if chat_id not in user_data:
        user_data[chat_id] = {}
        user_state[chat_id] = "ask_name"
        await bot.send_message(chat_id, "Fala torcedor da FURIA! 😎 Qual o seu nome?")
        return {"ok": True}

    state = user_state.get(chat_id)

    # Pergunta o nome
    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id, f"Top, {message}! Agora me diz: quantos anos você tem?")
        return {"ok": True}

    # Pergunta a idade
    elif state == "ask_age":
        user_data[chat_id]["age"] = message
        user_state[chat_id] = "ask_city"
        await bot.send_message(chat_id, "Show! De qual cidade você fala?")
        return {"ok": True}

    # Pergunta a cidade
    elif state == "ask_city":
        user_data[chat_id]["city"] = message
        user_state[chat_id] = "ask_social"
        await bot.send_message(chat_id, "Massa! Qual rede social você mais usa?")
        return {"ok": True}

    # Pergunta a rede social
    elif state == "ask_social":
        user_data[chat_id]["social_network"] = message
        user_state[chat_id] = "ask_nick"
        await bot.send_message(chat_id, "Legal! E qual o seu nick nessa rede ou nos games?")
        return {"ok": True}

    # Pergunta o nick
    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "ask_preference"
        await bot.send_message(chat_id, "Última pergunta! Prefere que eu te chame pelo nome ou pelo nick?")
        return {"ok": True}

    # Pergunta como prefere ser chamado
    elif state == "ask_preference":
        user_data[chat_id]["preferred_name"] = message
        user_state[chat_id] = "completed"
        nome_final = user_data[chat_id]["nickname"] if message.lower() == "nick" else user_data[chat_id]["name"]
        await bot.send_message(chat_id, f"Fechou, {nome_final}! 🚀 Agora você pode interagir comigo. Manda ver no menu abaixo:")
        send_menu(chat_id)
        return {"ok": True}

    # Conversa normal depois da coleta de dados
    else:
        reply = gerar_resposta(message)
        save_message(chat_id, message, reply)
        await bot.send_message(chat_id, reply)
        return {"ok": True}


    # Se o usuário já tiver completado os dados, segue com o menu de interação
    reply = gerar_resposta(message_text)

    # Salva no banco
    save_message(
        user_id=chat_id,
        message=message_text,
        response=reply if reply != "foto" else "📷 Foto da FURIA enviada"
    )

    # Envia resposta
    if reply == "foto":
        await bot.send_photo(
            chat_id=chat_id,
            photo="https://upload.wikimedia.org/wikipedia/commons/2/2c/FURIA_Esports_logo.png",
            caption="Aqui está a FURIA! 🖤"
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=reply
        )

    return {"ok": True}
