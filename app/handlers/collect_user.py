from telegram import Bot
from app.utils.validators import validate_age, validate_city
from app.handlers.telegram_menu import send_menu

# Função para iniciar a coleta de dados do usuário
async def start_collect_user_data(bot: Bot, chat_id: int, user_data: dict, user_state: dict):
    user_data[chat_id] = {"name": None, "age": None, "city": None, "nickname": None}
    user_state[chat_id] = "ask_name"
    await bot.send_message(chat_id=chat_id, text="Fala torcedor da FURIA! Qual o seu nome?")

# Função para processar as respostas do usuário durante a coleta de dados
async def process_user_data(bot: Bot, chat_id: int, message: str, user_data: dict, user_state: dict, send_menu_func=send_menu):
    state = user_state.get(chat_id)

    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id=chat_id, text=f"Boa, {message}! Agora me diz: quantos anos você tem?")

    elif state == "ask_age":
        if not validate_age(message):
            await bot.send_message(chat_id=chat_id, text="Por favor, insira uma idade válida.")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id=chat_id, text="Show! De qual cidade você fala?")

    elif state == "ask_city":
        if not validate_city(message):
            await bot.send_message(chat_id=chat_id, text="Por favor, insira uma cidade válida (apenas letras).")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id=chat_id, text="Legal! E qual o seu nick nos games?")

    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(
            chat_id=chat_id,
            text=f"Fechou, {user_data[chat_id]['name']}! Agora você é parte da nossa torcida! Vamos com tudo, FURIA!"
        )

        # Chama o menu principal, se a função foi passada
        if send_menu_func:
            await send_menu_func(bot, chat_id, welcome=False)

        return True  # Finalizado

    return False  # Ainda em coleta

# Função para verificar se ainda está em processo de coleta de dados
def is_collecting(chat_id: int, user_state: dict):
    return user_state.get(chat_id) != "completed"
