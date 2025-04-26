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
import openai

# Configurações seguras da OpenAI
from dotenv import load_dotenv
load_dotenv()
# Carregar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Definir as intenções
intents = {
    "greeting": ["oi", "olá", "bom dia", "boa tarde", "e aí", "oi chatbot", "salve"],
    "favorite_team": ["qual seu time favorito?", "quem é seu time?", "time favorito"],
    "next_game": ["quando é o próximo jogo?", "qual o próximo jogo?", "tem jogo logo?"],
    "bot_name": ["qual seu nome?", "como te chamo?", "qual é o seu nome?"],
    "how_are_you": ["como você está?", "tudo bem?", "como você tá?", "tá bem?"],
}

# Preparação dos dados para modelo simples de intenções
X = []
y = []
for intent, examples in intents.items():
    for example in examples:
        X.append(example)
        y.append(intent)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X, y)

def predict_intent(message: str):
    message_vectorized = vectorizer.transform([message])
    intent = model.predict(message_vectorized)[0]
    return intent

# Inicializa a API
app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0"
)

nlp = spacy.load("pt_core_news_sm")
create_db()

message_history = []
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

user_data = {}
user_state = {}

def validate_age(age):
    try:
        age = int(age)
        return 0 < age <= 120
    except ValueError:
        return False

def validate_city(city):
    return city.isalpha()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(msg: Message):
    user_msg = msg.message.lower()
    bot_reply = gerar_resposta_openai(user_msg)
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

# Resposta usando GPT da OpenAI

def gerar_resposta_openai(message_text: str) -> str:
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um chatbot divertido e fã da FURIA Esports. Responda de forma descontraída e voltada para gamers brasileiros."},
                {"role": "user", "content": message_text}
            ]
        )
        return resposta.choices[0].message["content"].strip()
    except Exception as e:
        print("Erro ao chamar a API da OpenAI:", e)
        return "Opa, deu ruim aqui na minha cabeça gamer 😵. Tenta de novo aí!"

# Função para enviar menu

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

# Coleta de dados do usuário
async def collect_user_data(chat_id):
    bot.send_message(chat_id, "Qual o seu nome, gamer? 😎")
    user_data[chat_id] = {"name": None, "age": None, "city": None, "nickname": None}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    message = update.message.text.strip()
    chat_id = update.message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {}
        user_state[chat_id] = "ask_name"
        await bot.send_message(chat_id, "Fala torcedor da FURIA! 😎 Qual o seu nome?")
        return {"ok": True}

    state = user_state.get(chat_id)

    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id, f"Top, {message}! Agora me diz: quantos anos você tem?")
    elif state == "ask_age":
        if not validate_age(message):
            await bot.send_message(chat_id, "Por favor, insira uma idade válida.")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id, "Show! De qual cidade você fala?")
    elif state == "ask_city":
        if not validate_city(message):
            await bot.send_message(chat_id, "Por favor, insira uma cidade válida (apenas letras).")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id, "Legal! E qual o seu nick nos games?")
    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(chat_id, f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você pode interagir comigo. Manda ver no menu abaixo:")
        send_menu(chat_id)
    else:
        reply = gerar_resposta_openai(message)
        save_message(chat_id, message, reply)
        await bot.send_message(chat_id, reply)

    return {"ok": True}