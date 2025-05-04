from datetime import datetime, timedelta
import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Lista de jogos programados
scheduled_games = [
    {"opponent": "Cloud9", "date": datetime(2025, 5, 3, 23, 0)},
    {"opponent": "G2", "date": datetime(2025, 5, 6, 20, 0)},
]

def get_game_status():
    now = datetime.now()

    # Verifica se algum jogo está rolando agora
    for game in scheduled_games:
        start = game["date"]
        end = start + timedelta(hours=2)

        if start <= now <= end:
            return f"A FURIA está jogando agora contra {game['opponent']}!"

    # Filtra apenas os jogos futuros
    future_games = [g for g in scheduled_games if g["date"] > now]
    future_games.sort(key=lambda x: x["date"])  # Garante que está ordenado por data

    if future_games:
        next_game = future_games[0]
        return f"Próximo jogo: FURIA vs {next_game['opponent']} em {next_game['date'].strftime('%d/%m/%Y às %H:%M')}."

    return "Nenhum jogo agendado no momento."

def get_current_and_next_game():
    now = datetime.now()
    current_game = None
    next_game = None

    for game in scheduled_games:
        start = game["date"]
        end = start + timedelta(hours=2)

        if start <= now <= end:
            current_game = game
            break
        elif start > now and next_game is None:
            next_game = game

    return current_game, next_game

# Função principal para ser chamada no handler /rolando
async def send_game_status(bot, chat_id):
    current_game, next_game = get_current_and_next_game()

    # Mensagem sobre as transmissões ao vivo
    texto = "🔥 A FURIA tá bombando ao vivo em várias plataformas! 💥 Escolha o que você quer fazer e bora lá, tropinha! 🎮🎧"

    botoes = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Assistir Online Agora", callback_data="assistir_online")],
        [InlineKeyboardButton("📅 Detalhes do Próximo Jogo", callback_data="detalhes_jogo")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])  

    await bot.send_message(chat_id=chat_id, text=texto, reply_markup=botoes)

# Função que lida com o botão "Assistir Online Agora"
async def handle_assistir_online(bot, chat_id):
    texto = "🎥 Você pode assistir aos jogos da FURIA ao vivo nas seguintes plataformas:"

    botoes = InlineKeyboardMarkup([
        [InlineKeyboardButton("📺 Assistir no YouTube", url="https://www.youtube.com/@FURIAggCS")],
        [InlineKeyboardButton("🎮 Assistir na Twitch", url="https://www.twitch.tv/furiatv?lang=pt-br")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="voltar_rolando")]
    ])

    await bot.send_message(chat_id=chat_id, text=texto, reply_markup=botoes)

# Função que lida com o botão "Detalhes do Próximo Jogo"
async def handle_detais_jogo(bot, chat_id):
    current_game, next_game = get_current_and_next_game()

    if next_game:
        texto = f"🔥 Próximo jogo confirmado, tropa! 📅 💥 FURIA vai enfrentar o {next_game['opponent']} em {next_game['date'].strftime('%d/%m/%Y às %H:%M')}! 🚀 Não perde essa, vamos juntos! 🔥"
        botoes = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Assistir Online Agora", callback_data="assistir_online")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="voltar_rolando")]
        ])
        await bot.send_message(chat_id=chat_id, text=texto, reply_markup=botoes)
    else:
        texto = "😴 Nenhum jogo agendado no momento. A tropa tá recarregando!"
        botoes = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Voltar", callback_data="voltar_rolando")]
        ])
        await bot.send_message(chat_id=chat_id, text=texto, reply_markup=botoes)

# Função de retorno (voltar ao menu "Rolando agora?")
async def handle_voltar_rolando(bot, chat_id):
    await send_game_status(bot, chat_id)
