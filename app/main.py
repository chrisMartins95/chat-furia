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
from dotenv import load_dotenv

# Carregar configurações seguras da OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Preparação dos dados para o modelo de intenções
intents = {
    "greeting": ["oi", "olá", "bom dia", "boa tarde", "e aí", "oi chatbot", "salve"],
    "favorite_team": ["qual seu time favorito?", "quem é seu time?", "time favorito"],
    "next_game": ["quando é o próximo jogo?", "qual o próximo jogo?", "tem jogo logo?"],
    "bot_name": ["qual seu nome?", "como te chamo?", "qual é o seu nome?"],
    "how_are_you": ["como você está?", "tudo bem?", "como você tá?", "tá bem?"],
}

# Inicializa a API
app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0"
)

nlp = spacy.load("pt_core_news_sm")
create_db()
message_history = []
bot = Bot(token=TELEGRAM_TOKEN)
user_data = {}
user_state = {}

# Funções auxiliares para validações
def validate_age(age):
    try:
        age = int(age)
        return 0 < age <= 120
    except ValueError:
        return False

def validate_city(city):
    return city.isalpha()

# Preparação do modelo de intenções
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

# Função para resposta usando OpenAI
def gerar_resposta_openai(message_text: str) -> str:
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Você é um chatbot super fã da FURIA Esports, sempre com uma energia positiva e vibrante! Responda de maneira empolgante e cheia de energia, como um verdadeiro torcedor apaixonado do CS:GO."},
                      {"role": "user", "content": message_text}]
        )
        return resposta.choices[0].message["content"].strip()
    except Exception as e:
        print("Erro ao chamar a API da OpenAI:", e)
        return "Opa, deu ruim aqui na minha cabeça gamer 😵. Tenta de novo aí!"

# Função para enviar o menu
async def send_menu(chat_id, custom_message=None):
    if custom_message is None:
        custom_message = "🔥 Tá pronto pra interagir com a tropa da FURIA? Escolhe uma opção aí embaixo e vamo que vamo!"
    
    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛒 Loja da FURIA")],
            [KeyboardButton("🌐 Redes da tropa"), KeyboardButton("🐱‍👤 Quem é a FURIA?")],
            [KeyboardButton("🔥 Rolando agora?"), KeyboardButton("📰 Hype News")],
            [KeyboardButton("💬 Manda um salve pro time")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await bot.send_message(
        chat_id=chat_id,
        text=custom_message,
        reply_markup=menu
    )

# Função para lidar com o botão "Loja"
async def handle_loja(chat_id):
    loja_url = "https://www.furia.gg/"  # Link para o site oficial da FURIA
    await bot.send_message(
        chat_id=chat_id,
        text=f"Confira os produtos da FURIA na nossa página oficial: {loja_url} 🛒👕🔥"
    )

# Função para coletar dados do usuário
async def collect_user_data(chat_id):
    user_data[chat_id] = {"name": None, "age": None, "city": None, "nickname": None}
    await bot.send_message(chat_id, "E aí, guerreiro da FURIA! 💥 Qual é o seu nome, futuro campeão?")

# Função para lidar com o webhook do Telegram
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
        await bot.send_message(chat_id, f"Boa, {message}! 🔥 Agora me diz: quantos anos você tem?")
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
        await bot.send_message(chat_id, f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você é parte da nossa torcida! Vamos com tudo, FURIA!")
        # Reexibir o menu após finalizar a coleta de dados
        await send_menu(chat_id, custom_message="🎮 Agora que você já é parte da nossa galera, escolha o que deseja fazer!")
    elif message == "🛒 Loja da FURIA":
        # Direcionar para a página da loja
        await bot.send_message(
            chat_id=chat_id,
            text="Aqui está o link para a nossa loja oficial: [Loja da FURIA](https://www.furia.gg/). Confira nossos produtos incríveis! 🎮🔥",
            parse_mode="Markdown"
        )
        # Reexibir o menu após o link
        await send_menu(chat_id, custom_message="✨ O que mais você gostaria de fazer, guerreiro?")
    elif message == "🌐 Redes da tropa":
        # Exibir links das redes sociais
        await bot.send_message(
            chat_id=chat_id,
            text="Quer falar com a FURIA? Escolha uma das nossas redes sociais para interagir:\n\n"
                 "Instagram: [@FURIAesports](https://www.instagram.com/furiaesports/)\n"
                 "Twitter: [@FURIAesports](https://twitter.com/FURIAesports)\n"
                 "Facebook: [FURIA Esports](https://www.facebook.com/FURIAesports)\n"
                 "Discord: [FURIA Discord](https://discord.gg/FURIA)\n\n"
                 "Ou mande um email para: [contato@furia.gg](mailto:contato@furia.gg) 🎮👊",
            parse_mode="Markdown"
        )
        # Reexibir o menu após os links
        await send_menu(chat_id, custom_message="🔥 Vamos pra próxima interação, o que você quer fazer agora?")
    else:
        reply = gerar_resposta_openai(message)
        save_message(chat_id, message, reply)
        await bot.send_message(chat_id, reply)
        # Reexibir o menu após a resposta do OpenAI
        await send_menu(chat_id, custom_message="⚡ O que mais posso te ajudar? Escolha uma opção!")

    return {"ok": True}
