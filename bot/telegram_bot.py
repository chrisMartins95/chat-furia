# app/handlers/telegram_menu.py
'''
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from app.match_status import get_game_status  # Se tiver essa função implementada

# Função para enviar o menu principal
async def send_menu(bot: Bot, chat_id: int, welcome: bool = True):
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

    if welcome:
        text = "🔥 Tá pronto pra interagir com a tropa da FURIA? Escolhe uma opção aí embaixo e vamo que vamo!"
    else:
        text = "👊 Se liga nas opções e escolhe o que quer fazer agora, tropinha!"

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)

# Função para tratar a opção "Loja da FURIA"
async def handle_loja(bot: Bot, chat_id: int):
    loja_url = "https://www.furia.gg/"
    await bot.send_message(
        chat_id=chat_id,
        text=f"🛒 Confira os produtos da FURIA na nossa loja oficial: {loja_url}"
    )

# Função para tratar a opção "Redes da tropa"
async def handle_redes(bot: Bot, chat_id: int):
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "🌐 Redes oficiais da FURIA:\n\n"
            "[Instagram](https://www.instagram.com/furiagg/?hl=pt-br)\n"
            "[X](https://x.com/FURIA)\n"
            "[Facebook](https://web.facebook.com/furiagg)\n"
            "[Discord](https://discord.com/invite/furia)\n\n"
            "📩 Contato: contato@furia.gg"
        ),
        parse_mode="Markdown"
    )

# Função para mostrar status de jogos
async def handle_rolando_agora(bot: Bot, chat_id: int):
    game_status = get_game_status()
    await bot.send_message(chat_id=chat_id, text=game_status)

# Funções para sobre a FURIA
async def handle_sobre_furia(bot: Bot, chat_id: int):
    info = (
        "🔥 A FURIA Esports é uma organização brasileira de esports fundada em 2017.\n"
        "Com presença em CS:GO, League of Legends, Rainbow Six e VALORANT, a FURIA é conhecida "
        "pelo seu estilo agressivo e pelo impacto cultural no cenário esportivo! 🇧🇷🎮"
    )
    submenu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🎯 Falar sobre o time de CS")],
            [KeyboardButton("🎯 Falar de cada jogador do time CS")],
            [KeyboardButton("⬅️ Voltar para o menu principal")]
        ],
        resize_keyboard=True
    )
    await bot.send_message(chat_id=chat_id, text=info)
    await bot.send_message(chat_id=chat_id, text="Quer saber mais? Escolhe uma opção 👇", reply_markup=submenu)

async def handle_sobre_time_cs(bot: Bot, chat_id: int):
    info = (
        "O time de CS:GO da FURIA é um dos mais fortes do Brasil!\n"
        "Estilo agressivo e tático, competindo nas principais ligas do mundo. 🏆"
    )
    await bot.send_message(chat_id=chat_id, text=info)

async def handle_sobre_jogadores_cs(bot: Bot, chat_id: int):
    jogadores = {
        "🧢 yuurih": "Especialista em clutches e mira afiada.",
        "⚡ KSCERATO": "Um dos melhores riflers do mundo!",
        "🎯 FalleN": "Lenda viva do CS, AWP e líder estratégico.",
        "🔥 molodoy": "A nova geração mostrando força!"
    }
    await bot.send_message(chat_id=chat_id, text="🎯 Conheça os jogadores do time de CS da FURIA:")
    for nome, desc in jogadores.items():
        await bot.send_message(chat_id=chat_id, text=f"{nome}\n{desc}")
'''