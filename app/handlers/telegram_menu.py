from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

# Função para enviar o menu principal
async def send_menu(bot: Bot, chat_id: int, welcome: bool = True):
    """
    Envia o menu principal para o usuário com as opções interativas.
    
    Args:
        bot (Bot): Instância do bot Telegram.
        chat_id (int): ID do chat de destino.
        welcome (bool): Se True, envia uma mensagem de boas-vindas.
    """
    # Define os botões do menu com ícones e texto
    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛒 Loja da FURIA")],  # Botão para acessar a loja
            [KeyboardButton("🌐 Redes da tropa"), KeyboardButton("🐱‍👤 Quem é a FURIA?")],  # Botões para redes sociais e sobre a FURIA
            [KeyboardButton("🔥 Rolando agora?"), KeyboardButton("📰 Hype News")],  # Botões para notícias e eventos ao vivo
            [KeyboardButton("💬 Manda um salve pro time")]  # Botão para mandar uma mensagem para o time
        ],
        one_time_keyboard=True,  # Esconde o teclado após a interação
        resize_keyboard=True  # Ajusta o tamanho do teclado para caber na tela
    )

    # Mensagem de boas-vindas ou mensagem normal, dependendo do parâmetro `welcome`
    if welcome:
        text = "🔥 Tá pronto pra interagir com a tropa da FURIA? Escolhe uma opção aí embaixo e vamo que vamo!"
    else:
        text = "👊 Se liga nas opções e escolhe o que quer fazer agora, tropinha!"

    # Envia a mensagem com o menu
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)

# Função para tratar a opção "Loja da FURIA"
async def handle_loja(bot: Bot, chat_id: int):
    """
    Envia a URL da loja oficial da FURIA quando o usuário escolhe a opção "Loja da FURIA".
    
    Args:
        bot (Bot): Instância do bot Telegram.
        chat_id (int): ID do chat de destino.
    """
    loja_url = "https://www.furia.gg/"
    # Envia a mensagem com o link para a loja
    await bot.send_message(
        chat_id=chat_id,
        text=f"🛒 Confira os produtos da FURIA na nossa loja oficial: {loja_url}"
    )

# Função para tratar a opção "Redes da tropa"
async def handle_redes(bot: Bot, chat_id: int):
    """
    Envia as redes sociais da FURIA quando o usuário escolhe a opção "Redes da tropa".
    
    Args:
        bot (Bot): Instância do bot Telegram.
        chat_id (int): ID do chat de destino.
    """
    # Mensagem com os links das redes sociais da FURIA
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "🌐 Redes oficiais da FURIA:\n\n"
            "📸 [Instagram](https://www.instagram.com/furiaesports/)\n"
            "🐦 [Twitter](https://twitter.com/FURIAesports)\n"
            "📘 [Facebook](https://www.facebook.com/FURIAesports)\n"
            "💬 [Discord](https://discord.gg/FURIA)\n\n"
            "📩 Contato: [contato@furia.gg](mailto:contato@furia.gg)"
        ),
        parse_mode="Markdown"  # Formatação em Markdown para links
    )

# (Em breve) Funções para:
# - handle_sobre_furia(bot, chat_id)
# - handle_rolando_agora(bot, chat_id)
# - handle_hype_news(bot, chat_id)
# - handle_manda_salve(bot, chat_id)
