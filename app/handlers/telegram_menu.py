from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from app.handlers.match_status import send_game_status, get_current_and_next_game

# --------------------- Menu Principal ---------------------

async def send_menu(bot: Bot, chat_id: int, welcome: bool = True):
    # Define o menu principal com as opções de interação
    menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Loja da FURIA", callback_data="loja")],
        [
            InlineKeyboardButton("🌐 Redes da tropa", callback_data="redes"),
            InlineKeyboardButton("🐱‍👤 Quem é a FURIA?", callback_data="quem_e")
        ],
        [
            InlineKeyboardButton("🔥 Rolando agora?", callback_data="rolando"),
            InlineKeyboardButton("📰 Hype News", callback_data="hype_news")
        ],
        [InlineKeyboardButton("💬 Manda um salve pro time", callback_data="salve")]
    ])

    # Mensagem de boas-vindas ou de interação com base no parâmetro 'welcome'
    text = (
        "🔥 Tá pronto pra interagir com a tropa da FURIA? Escolhe uma opção aí embaixo e vamo que vamo!"
        if welcome else
        "👊 Se liga nas opções e escolhe o que quer fazer agora, tropinha! 🔥"
    )

    # Envia a mensagem com o menu para o chat
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)

# --------------------- Handlers de Botões ---------------------

async def handle_loja(bot: Bot, chat_id: int):
    loja_url = "https://www.furia.gg/"
    # Envia a mensagem com o link para a loja
    await bot.send_message(chat_id=chat_id, text=f"🛒 Confira os produtos da FURIA na nossa loja oficial: {loja_url}")

    # Menu para voltar ao menu principal
    voltar_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    # Envia a mensagem perguntando se o usuário deseja saber mais sobre o time ou os jogadores
    await bot.send_message(
        chat_id=chat_id,
        text = "🛍️ Agora que você deu uma olhada nos produtos da FURIA, que tal saber mais sobre o time ou os jogadores? 🔥👊",
        reply_markup=voltar_menu
    )

async def handle_redes(bot: Bot, chat_id: int):
    # Envia as redes sociais oficiais da FURIA
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "🌐 Redes oficiais da FURIA:\n\n"
            "📸 [Instagram](https://www.instagram.com/furiagg/?hl=pt-br)\n"
            "❌ [X](https://x.com/FURIA)\n"
            "📘 [Facebook](https://web.facebook.com/furiagg)\n"
            "💬 [Discord](https://discord.com/invite/furia)\n\n"
            "📩 Contato: [contato@furia.gg](mailto:contato@furia.gg)"
        ),
        parse_mode="Markdown"
    )

    # Menu para voltar ao menu principal
    voltar_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    # Envia a mensagem perguntando se o usuário deseja saber mais sobre o time ou os jogadores
    await bot.send_message(
        chat_id=chat_id,
        text = "🌐 Agora que você já conhece as nossas redes sociais da FURIA, que tal saber mais sobre o time ou os jogadores? 🔥👊",
        reply_markup=voltar_menu
    )

async def handle_sobre_furia(bot: Bot, chat_id: int):
    # Informações sobre a FURIA
    info_furia = (
    "🔥 FURIA é muito mais que uma organização de esports! Começamos com um sonho: representar o Brasil no CS. "
    "Mas fomos além! Expandimos nossas ligas, dominamos os principais campeonatos, conquistamos novos objetivos "
    "e, mais importante, encontramos um propósito maior! Somos a FURIA: um movimento sociocultural que vai além das vitórias. 🌍🎮"
    )

    # Envia as informações sobre a FURIA
    await bot.send_message(chat_id=chat_id, text=info_furia)

    # Menu para escolher entre falar sobre o time ou os jogadores
    menu_furia = InlineKeyboardMarkup([
        [InlineKeyboardButton("🐱‍👤 Falar sobre o time de CS", callback_data="time_cs")],
        [InlineKeyboardButton("🎮 Falar sobre os jogadores", callback_data="jogadores")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    # Envia a mensagem perguntando o que o usuário quer saber mais
    await bot.send_message(
        chat_id=chat_id,
        text = "🔥 Agora que você já conhece a FURIA, tá na hora de saber mais sobre o nosso time ou os jogadores que fazem a magia acontecer! ✨ O que você escolhe, tropa? 🎯",
        reply_markup=menu_furia
    )

async def handle_sobre_time_cs(bot: Bot, chat_id: int):
    # Informações sobre o time de CS2 da FURIA
    info_time = '''💣 O time de CS2 da FURIA é um dos mais temidos e respeitados no cenário mundial. 
Com jogadores como FalleN, KSCERATO, molodoy, YEKINDAR e yuurih, a equipe tem conquistado títulos importantes e
levado o nome do Brasil para o topo do CS:GO. 🇧🇷'''
    # Envia as informações sobre o time
    await bot.send_message(chat_id=chat_id, text=info_time)

    # Menu para escolher entre saber mais sobre os jogadores ou voltar
    menu_time_cs = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Falar sobre os jogadores", callback_data="jogadores")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    # Envia a mensagem perguntando o que o usuário quer fazer
    await bot.send_message(
        chat_id=chat_id,
        text="🎯 Agora que você sabe sobre o time de CS, quer saber mais sobre os jogadores ou voltar? A escolha é sua!",
        reply_markup=menu_time_cs
    )

async def handle_sobre_jogadores_cs(bot: Bot, chat_id: int):
    # Mensagem informando sobre os jogadores
    info_jogadores = "🌟 Escolha um dos nossos craques para saber mais sobre ele! 🌟"

    # Menu com os jogadores disponíveis para escolher
    menu_jogadores_cs = InlineKeyboardMarkup([
        [InlineKeyboardButton("FalleN", callback_data="FalleN")],
        [InlineKeyboardButton("KSCERATO", callback_data="KSCERATO")],
        [InlineKeyboardButton("molodoy", callback_data="molodoy")],
        [InlineKeyboardButton("yuurih", callback_data="yuurih")],
        [InlineKeyboardButton("YEKINDAR", callback_data="YEKINDAR")],
        [InlineKeyboardButton("Treinador-sidde", callback_data="Treinador-sidde")],
        [InlineKeyboardButton("Treinador-Hepa", callback_data="Treinador-Hepa")],
        [InlineKeyboardButton("🐱‍👤 Falar sobre o time de CS", callback_data="time_cs")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    # Envia a mensagem com as opções de jogadores
    await bot.send_message(chat_id=chat_id, text=info_jogadores, reply_markup=menu_jogadores_cs)

async def handle_jogador_especifico(bot: Bot, chat_id: int, jogador: str):
    # Informações específicas sobre cada jogador
    info_jogadores = {
        "FalleN": '''🔥 FalleN (Gabriel Toledo) - Rifler 🇧🇷
Idade: 32 anos.
FalleN é um dos maiores nomes da história do CS:GO, conhecido por sua liderança e habilidades excepcionais. Ele foi parte fundamental na ascensão da FURIA ao topo do cenário mundial, trazendo experiência e estratégia para o time. Além disso, é considerado um dos melhores AWPers do mundo.''',
        "KSCERATO": '''💥 KSCERATO (Kaike Cerato) - Rifler 🇧🇷
Idade: 21 anos.
KSCERATO é um talento emergente e uma verdadeira estrela no cenário do CS:GO. Seu jogo agressivo e suas jogadas incríveis o tornaram uma referência no Brasil e no mundo.''',
        "molodoy": '''🎯 molodoy (Danil Golubenko) - AWPer 🇰🇿
Idade: 22 anos.
molodoy é um dos jovens talentos da FURIA, com habilidades impressionantes no uso do AWP.''',
        "yuurih": '''⚡ yuurih (Yuri Santos) - Rifler 🇧🇷
Idade: 23 anos.
yuurih é um dos jogadores mais técnicos da FURIA. Seu estilo de jogo estratégico e sua habilidade com rifles fazem dele uma peça chave no time.''',
        "YEKINDAR": '''🚀 YEKINDAR (Mareks Gaļinskis) - Entry Fragger 🇱🇻
Idade: 24 anos.
YEKINDAR é conhecido por seu estilo de jogo agressivo e por abrir espaços essenciais para o time. Seu desempenho consistente o colocou entre os melhores Entry Fraggers do mundo, sendo uma grande adição à FURIA.''',
        "Treinador-sidde": '''💪 Sidde (Sid Macedo) - Treinador 🇧🇷
Idade: 30 anos.
Sidde é o cérebro por trás das estratégias da FURIA. Como treinador, ele tem a responsabilidade de orientar o time e ajudá-los a alcançar seu potencial máximo.''',
        "Treinador-Hepa": '''🔧 Hepa (Juan Borges) - Assistente Técnico 🇪🇸
Idade: 28 anos.
Hepa é o assistente técnico da FURIA e trabalha de perto com Sidde para garantir que o time esteja sempre preparado e focado.'''
    }

    # Envia as informações do jogador escolhido
    if jogador in info_jogadores:
        await bot.send_message(chat_id=chat_id, text=info_jogadores[jogador])
    else:
        await bot.send_message(chat_id=chat_id, text="Jogador não encontrado.")

    # Volta para o menu de jogadores
    await handle_sobre_jogadores_cs(bot, chat_id)

async def handle_rolando_agora(bot: Bot, chat_id: int):
    # Chama a função para enviar o status do jogo atual
    await send_game_status(bot, chat_id)
