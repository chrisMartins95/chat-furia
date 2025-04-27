from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters

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
            "📸 [Instagram](https://www.instagram.com/furiagg/?hl=pt-br)\n"
            "❌ [X](https://x.com/FURIA?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)\n"
            "📘 [Facebook](https://web.facebook.com/furiagg/?locale=pt_BR&_rdc=1&_rdr#)\n"
            "💬 [Discord](https://discord.com/invite/furia)\n\n"
            "📩 Contato: [contato@furia.gg](mailto:contato@furia.gg)"
        ),
        parse_mode="Markdown"
    )

# Textos sobre a FURIA
def falar_sobre_furia():
    return (
        "A FURIA Esports é uma organização brasileira de esports fundada em 2017. "
        "Desde sua criação, a FURIA se destacou em jogos como CS:GO, League of Legends, Rainbow Six e VALORANT. "
        "Com uma equipe de CS:GO agressiva e inovadora, a FURIA conquistou títulos e o coração dos fãs! 🔥"
    )

def falar_sobre_time_cs():
    return (
        "O time de CS:GO da FURIA é um dos mais fortes do Brasil! 🏆 "
        "Com um estilo agressivo e dinâmico, o time brilha em torneios como ESL Pro League, DreamHack e Blast Premier!"
    )

def falar_sobre_jogadores_cs():
    jogadores = {
        "🧢 yuurih": "Um dos pilares da FURIA! Especialista em clutches e mira afiada. É referência no CS:GO mundial!",
        "🎮 arT": "O capitão (IGL) da equipe, mestre das táticas ousadas que definem o estilo único da FURIA!",
        "⚡ kaoz": "O novo talento, versátil e pronto pra surpreender em qualquer posição do mapa!",
        "🔥 VSM": "Um dos melhores entradores do Brasil, com jogadas agressivas que empolgam a torcida!",
        "🛡️ drop": "Suporte sólido, sempre salvando rounds importantes e garantindo a defesa da equipe!"
    }
    return jogadores

# Função para tratar "Quem é a FURIA?" e abrir submenu
async def handle_sobre_furia(bot: Bot, chat_id: int):
    info_furia = falar_sobre_furia()
    await bot.send_message(chat_id=chat_id, text=info_furia)

    submenu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🎯 Falar sobre o time de CS")],
            [KeyboardButton("🎯 Falar de cada jogador do time CS")],
            [KeyboardButton("⬅️ Voltar para o menu principal")]
        ],
        resize_keyboard=True
    )

    await bot.send_message(
        chat_id=chat_id,
        text="Quer saber mais? Escolhe uma opção aqui embaixo 👇",
        reply_markup=submenu
    )

# Função para falar sobre o time de CS
async def handle_sobre_time_cs(bot: Bot, chat_id: int):
    info_time = falar_sobre_time_cs()
    await bot.send_message(chat_id=chat_id, text=info_time)

# Função para falar dos jogadores um por um (carrossel)
async def handle_sobre_jogadores_cs(bot: Bot, chat_id: int):
    jogadores_info = falar_sobre_jogadores_cs()

    await bot.send_message(chat_id=chat_id, text="🎯 Conheça os jogadores do time de CS da FURIA:")

    for nome, descricao in jogadores_info.items():
        await bot.send_message(chat_id=chat_id, text=f"{nome}\n{descricao}")

# Função para processar as mensagens recebidas
async def processar_resposta(update, context):
    user_message = update.message.text
    chat_id = update.message.chat.id

    if user_message == "🐱‍👤 Quem é a FURIA?":
        await handle_sobre_furia(update.bot, chat_id)
    elif user_message == "🎯 Falar sobre o time de CS":
        await handle_sobre_time_cs(update.bot, chat_id)
    elif user_message == "🎯 Falar de cada jogador do time CS":
        await handle_sobre_jogadores_cs(update.bot, chat_id)
    elif user_message == "⬅️ Voltar para o menu principal":
        await send_menu(update.bot, chat_id, welcome=False)
    elif user_message == "🛒 Loja da FURIA":
        await handle_loja(update.bot, chat_id)
    elif user_message == "🌐 Redes da tropa":
        await handle_redes(update.bot, chat_id)
   # elif user_message == "🔥 Rolando agora?":
   #     await handle_rolando_agora(update.bot, chat_id)  # Implementar
    #elif user_message == "📰 Hype News":
   #     await handle_hype_news(update.bot, chat_id)  # Implementar
   # elif user_message == "💬 Manda um salve pro time":
    #    await handle_manda_salves(update.bot, chat_id)  # Implementar
    else:
        await bot.send_message(chat_id=chat_id, text="❓ Não entendi, escolha uma opção do menu! 😅")
