from telegram import Bot
from app.utils.validators import validate_age, validate_city

# Função para iniciar a coleta de dados do usuário
async def start_collect_user_data(bot: Bot, chat_id: int, user_data: dict, user_state: dict):
    """
    Inicia o processo de coleta de dados do usuário, como nome, idade, cidade e nickname.
    
    Args:
        bot (Bot): Instância do bot Telegram.
        chat_id (int): ID do chat de destino.
        user_data (dict): Dicionário onde os dados dos usuários serão armazenados.
        user_state (dict): Dicionário para controlar o estado atual do processo de coleta.
    """
    # Inicializa o dicionário para armazenar os dados do usuário
    user_data[chat_id] = {"name": None, "age": None, "city": None, "nickname": None}
    
    # Define o estado inicial do usuário como "ask_name" (pedindo o nome)
    user_state[chat_id] = "ask_name"
    
    # Envia uma mensagem de saudação pedindo o nome do usuário
    await bot.send_message(chat_id=chat_id, text="Fala torcedor da FURIA! 😎 Qual o seu nome?")

# Função para processar as respostas do usuário durante a coleta de dados
async def process_user_data(bot: Bot, chat_id: int, message: str, user_data: dict, user_state: dict):
    """
    Processa as respostas do usuário com base no estado atual e coleta as informações necessárias.
    
    Args:
        bot (Bot): Instância do bot Telegram.
        chat_id (int): ID do chat de destino.
        message (str): A mensagem enviada pelo usuário.
        user_data (dict): Dicionário onde os dados dos usuários são armazenados.
        user_state (dict): Dicionário que controla o estado da coleta de dados.
    """
    state = user_state.get(chat_id)

    # Verifica o estado atual do processo de coleta e age conforme o caso
    if state == "ask_name":
        # Armazena o nome do usuário e pede a idade
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id=chat_id, text=f"Boa, {message}! 🔥 Agora me diz: quantos anos você tem?")

    elif state == "ask_age":
        # Valida a idade e, se válida, pede a cidade
        if not validate_age(message):
            await bot.send_message(chat_id=chat_id, text="Por favor, insira uma idade válida.")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id=chat_id, text="Show! De qual cidade você fala?")

    elif state == "ask_city":
        # Valida a cidade e, se válida, pede o nick
        if not validate_city(message):
            await bot.send_message(chat_id=chat_id, text="Por favor, insira uma cidade válida (apenas letras).")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id=chat_id, text="Legal! E qual o seu nick nos games?")

    elif state == "ask_nick":
        # Armazena o nickname e finaliza a coleta
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(
            chat_id=chat_id,
            text=f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você é parte da nossa torcida! Vamos com tudo, FURIA!"
        )
        return True  # Cadastro finalizado

    return False  # Caso o processo de coleta ainda não tenha sido concluído

# Função para verificar se ainda está em processo de coleta de dados
def is_collecting(chat_id: int, user_state: dict):
    """
    Verifica se o processo de coleta de dados para o usuário ainda está em andamento.
    
    Args:
        chat_id (int): ID do chat de destino.
        user_state (dict): Dicionário que controla o estado da coleta de dados.
    
    Returns:
        bool: Retorna True se a coleta não foi finalizada, False caso contrário.
    """
    return user_state.get(chat_id) != "completed"
