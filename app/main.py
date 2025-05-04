from fastapi import FastAPI, Request
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta

# Banco de dados
from app.database import create_db, save_message

# Modelos de dados
from app.models.fan_interaction import Fan, Interaction
from app.models.message import Message

# Handlers
from app.handlers.telegram_menu import send_menu, handle_loja, handle_redes, handle_sobre_furia, handle_sobre_time_cs, handle_sobre_jogadores_cs, handle_jogador_especifico, handle_rolando_agora
from app.handlers.collect_user import validate_age, validate_city
from app.handlers.match_status import handle_detais_jogo, handle_assistir_online, send_game_status
from app.handlers.hype_news import enviar_hype_news

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

app = FastAPI(
    title="Chatbot FURIA",
    description="Um chatbot para interagir com os torcedores da FURIA.",
    version="1.0.0"
)

create_db()

user_data = {}
user_state = {}

# Variável para controlar o tempo das queries
last_query_time = {}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)

    if update.callback_query:
        query = update.callback_query
        data = query.data
        chat_id = query.message.chat.id
        current_time = datetime.now()

        # Verifica se a última query foi dentro do tempo aceitável (ex: 1 minuto)
        if chat_id in last_query_time and current_time - last_query_time[chat_id] > timedelta(minutes=1):
            return {"ok": True}  # Query antiga, não respondemos

        await bot.answer_callback_query(callback_query_id=query.id)
        last_query_time[chat_id] = current_time  # Atualiza o tempo da última query respondida

        # Lógica para as opções do menu
        if data == "loja":
            await handle_loja(bot, chat_id)
        elif data == "redes":
            await handle_redes(bot, chat_id)
        elif data == "quem_e":
            await handle_sobre_furia(bot, chat_id)
        elif data == "time_cs":
            await handle_sobre_time_cs(bot, chat_id)
        elif data == "jogadores":
            await handle_sobre_jogadores_cs(bot, chat_id)
        elif data in ["FalleN", "KSCERATO", "molodoy", "YEKINDAR", "yuurih", "Treinador-sidde", "Treinador-Hepa"]:
            await handle_jogador_especifico(bot, chat_id, data)
        elif data == "rolando":
            await handle_rolando_agora(bot, chat_id)
        elif data == "hype_news":
            await enviar_hype_news(bot, chat_id)
        elif data == "salve":
            user_state[chat_id] = "salve_msg"
            await bot.send_message(chat_id, "💬 Manda teu salve aqui que a gente entrega pro time! 🔥")
        elif data == "voltar_menu":
            await send_menu(bot, chat_id, welcome=False)
        elif data == "voltar_menu_sobre":
            await handle_sobre_furia(bot, chat_id)
        elif data == "assistir_online":
            await handle_assistir_online(bot, chat_id)
        elif data == "detalhes_jogo":
            await handle_detais_jogo(bot, chat_id)
        elif data == "voltar_rolando":
            await send_game_status(bot, chat_id)

        return {"ok": True}

    if update.message is None or update.message.text is None:
        return {"ok": True}

    message = update.message.text.strip()
    chat_id = update.message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {}
        user_state[chat_id] = "ask_name"
        await bot.send_message(chat_id, "🔥 Fala, torcedor da FURIA! 🦁 Qual é o seu nome, guerreiro? Vamos fazer história juntos! 💥")
        return {"ok": True}

    state = user_state.get(chat_id)

    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id, f"Que massa, {message}! 🎮 Agora me conta: quantos anos de pura adrenalina você tem? 💥")
    elif state == "ask_age":
        if not validate_age(message):
            await bot.send_message(chat_id, "Ops! 😅 Parece que você digitou algo errado. Pode colocar uma idade válida, por favor? 👀")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id, "Legal! 🏙️ Agora me conta: de qual cidade você é? 🌍")
    elif state == "ask_city":
        if not validate_city(message):
            await bot.send_message(chat_id, "Ops! 🤔 Parece que a cidade não é válida. Tente novamente, apenas com letras, beleza? ✨")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id, "Agora, me conta: qual é o seu nick nos games? 🎮👾")
    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(chat_id, f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você é parte da nossa torcida! 🔥 Vamos com tudo, FURIA! 🦁")

        # Mostra o menu principal
        await send_menu(bot, chat_id, welcome=False)
    else:
        if state == "salve_msg":
            salve = message
            reply = f"Salve recebido, {user_data[chat_id]['name']}! 🔥💬 Vamos fazer chegar no time com toda a força! 💪 Valeu demais pela energia e apoio! 🙌 Vamos que vamos, FURIA! 🦁🎮"

            # Zera o estado e salva no banco
            user_state[chat_id] = "completed"
            save_message(chat_id, salve, reply)

            await bot.send_message(chat_id, reply)
            await send_menu(bot, chat_id, welcome=False)

        elif message == "🔙 Voltar ao menu principal":
            await send_menu(bot, chat_id, welcome=False)
        else:
            reply = "Ei, parece que não consegui entender o que você quis dizer. 😅 Pode tentar novamente? Estou aqui para ajudar! 👊"
            save_message(chat_id, message, reply)
            await bot.send_message(chat_id, reply)
            await send_menu(bot, chat_id, welcome=False)

    return {"ok": True}
