from telegram import Bot
from app.utils.validators import validate_age, validate_city
from app.handlers.telegram_menu import send_menu

# ---------------------------------------------------
# Inicia a coleta de dados do usuário (primeira mensagem)
# ---------------------------------------------------
async def start_collect_user_data(bot: Bot, chat_id: int, user_data: dict, user_state: dict):
    """
    Inicia o processo de coleta de dados do usuário.
    Define os campos padrão e solicita o nome.
    """
    user_data[chat_id] = {
        "name": None,
        "age": None,
        "city": None,
        "nickname": None
    }
    user_state[chat_id] = "ask_name"
    await bot.send_message(chat_id=chat_id, text="🔥 Fala torcedor da FURIA! Qual o seu nome, guerreiro?")

# ---------------------------------------------------
# Processa cada etapa da coleta conforme o estado atual
# ---------------------------------------------------
async def process_user_data(bot: Bot, chat_id: int, message: str, user_data: dict, user_state: dict, send_menu_func=send_menu):
    """
    Processa as respostas do usuário conforme o estado atual da coleta.
    Após concluir os dados, envia o menu principal.
    """
    state = user_state.get(chat_id)

    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id=chat_id, text=f"Boa, {message}! Agora me diz: quantos anos você tem?")

    elif state == "ask_age":
        if not validate_age(message):
            await bot.send_message(chat_id=chat_id, text="Ops! Idade inválida. Pode mandar uma idade certinha?")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id=chat_id, text="Show! Agora me conta de qual cidade você fala?")

    elif state == "ask_city":
        if not validate_city(message):
            await bot.send_message(chat_id=chat_id, text="Hmm... cidade inválida. Tenta só com letras, beleza?")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id=chat_id, text="Legal! E qual é o seu nick nos games? 🎮")

    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"

        await bot.send_message(
            chat_id=chat_id,
            text=f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você faz parte da nossa torcida! Vamos com tudo, FURIA! 🦁"
        )

        # Mostra o menu principal após finalizar a coleta
        if send_menu_func:
            await send_menu_func(bot, chat_id, welcome=False)

        return True  # Indica que a coleta foi finalizada

    return False  # Ainda está no processo de coleta

# ---------------------------------------------------
# Verifica se um usuário está em processo de coleta
# ---------------------------------------------------
def is_collecting(chat_id: int, user_state: dict):
    """
    Retorna True se o usuário ainda não completou a coleta de dados.
    """
    return user_state.get(chat_id) != "completed"
