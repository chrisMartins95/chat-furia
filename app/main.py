from fastapi import FastAPI, Request
from telegram import Update, Bot
from dotenv import load_dotenv
import os
import openai

# Banco de dados
from app.database import create_db, save_message

# Modelos de dados
from app.models.fan_interaction import Fan, Interaction
from app.models.message import Message

# Handlers (funções para enviar menus e lidar com interações)
from app.handlers.telegram_menu import send_menu, handle_loja, handle_redes
from app.handlers.collect_user import start_collect_user_data, process_user_data, is_collecting

# Utilitários
from app.utils.validators import validate_age, validate_city
from app.utils.nlp_model import predict_intent
from app.utils.ai_response import gerar_resposta_openai

# Inicializações do ambiente
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Obtém a chave da API da OpenAI
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Obtém o token do Telegram

# Inicializa o bot do Telegram com o token
bot = Bot(token=TELEGRAM_TOKEN)

# Inicia o FastAPI
app = FastAPI(
    title="Chatbot FURIA",  # Título da API
    description="Um chatbot para interagir com os torcedores da FURIA.",  # Descrição da API
    version="1.0.0"  # Versão da API
)

# Criação do banco de dados
create_db()

# Armazenamento temporário dos dados do usuário e controle de estados
user_data = {}  # Dicionário que armazena dados do usuário
user_state = {}  # Dicionário que armazena o estado atual de cada usuário

# Webhook do Telegram: endpoint que o Telegram chama quando há uma nova mensagem
@app.post("/webhook")
async def telegram_webhook(req: Request):
    # Recebe a solicitação do webhook do Telegram
    data = await req.json()
    update = Update.de_json(data, bot)  # Converte o JSON para um objeto Update do Telegram
    
    # Se a mensagem não existir, responde com OK
    if update.message is None:
        return {"ok": True}
    
    # Obtém a mensagem do usuário e seu ID do chat
    message = update.message.text.strip()
    chat_id = update.message.chat.id

    # Se o usuário não foi registrado ainda, inicia o processo de coleta de dados
    if chat_id not in user_data:
        user_data[chat_id] = {}
        user_state[chat_id] = "ask_name"
        await bot.send_message(chat_id, "Fala torcedor da FURIA! 😎 Qual o seu nome?")
        return {"ok": True}
    
    state = user_state.get(chat_id)  # Obtém o estado atual do usuário

    # Fluxo de coleta de dados do usuário
    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id, f"Boa, {message}! 🔥 Agora me diz: quantos anos você tem?")
    elif state == "ask_age":
        if not validate_age(message):  # Valida se a idade fornecida é válida
            await bot.send_message(chat_id, "Por favor, insira uma idade válida.")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id, "Show! De qual cidade você fala?")
    elif state == "ask_city":
        if not validate_city(message):  # Valida se a cidade fornecida é válida
            await bot.send_message(chat_id, "Por favor, insira uma cidade válida (apenas letras).")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id, "Legal! E qual o seu nick nos games?")
    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(chat_id, f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você é parte da nossa torcida! Vamos com tudo, FURIA!")
        await send_menu(bot, chat_id, welcome=False)  # Envia o menu de opções ao usuário
    # Se o usuário já completou o cadastro, interage com o menu
    elif message == "🛒 Loja da FURIA":
        await handle_loja(bot, chat_id)  # Lida com a opção "Loja da FURIA"
        await send_menu(bot, chat_id, welcome=False)
    elif message == "🌐 Redes da tropa":
        await handle_redes(bot, chat_id)  # Lida com a opção "Redes da tropa"
        await send_menu(bot, chat_id, welcome=False)
    else:
        # Caso a mensagem não corresponda a nenhum menu ou comando
        intent = predict_intent(message)  # Tenta prever a intenção da mensagem
        if intent:
            # Se houver uma intenção definida, gera uma resposta personalizada
            reply = gerar_resposta_openai(message)
        else:
            # Caso contrário, gera uma resposta padrão
            reply = gerar_resposta_openai(message)

        # Salva a mensagem e a resposta no banco de dados
        save_message(chat_id, message, reply)
        await bot.send_message(chat_id, reply)  # Envia a resposta para o usuário
        await send_menu(bot, chat_id, welcome=False)

    return {"ok": True}
