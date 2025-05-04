from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from app.handlers.match_status import send_game_status,get_current_and_next_game

# --------------------- Menu Principal ---------------------

async def send_menu(bot: Bot, chat_id: int, welcome: bool = True):
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

    text = (
        "🔥 Tá pronto pra interagir com a tropa da FURIA? Escolhe uma opção aí embaixo e vamo que vamo!"
        if welcome else
        "👊 Se liga nas opções e escolhe o que quer fazer agora, tropinha! 🔥"
    )

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=menu)

# --------------------- Handlers de Botões ---------------------

async def handle_loja(bot: Bot, chat_id: int):
    loja_url = "https://www.furia.gg/"
    await bot.send_message(chat_id=chat_id, text=f"🛒 Confira os produtos da FURIA na nossa loja oficial: {loja_url}")

    voltar_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text="Agora que você deu uma olhada nos produtos FURIA, quer saber mais sobre o time ou os jogadores? 🔥💥",
        reply_markup=voltar_menu
    )

async def handle_redes(bot: Bot, chat_id: int):
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

    voltar_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text="Agora que você já conhece as nossas redes sociais FURIA, que tal saber mais sobre o time ou os jogadores? ⚡🔥",
        reply_markup=voltar_menu
    )

async def handle_sobre_furia(bot: Bot, chat_id: int):
    info_furia = (
        "FURIA é muito mais que uma organização de esports! Começamos com um sonho: representar o Brasil no CS. Mas fomos além! 🚀 Expandimos nossas ligas, dominamos os principais campeonatos, conquistamos novos objetivos e, mais importante, encontramos um propósito maior! 💥 Somos a FURIA: um movimento sociocultural que vai além das vitórias. 🏆"
    )
    await bot.send_message(chat_id=chat_id, text=info_furia)

    menu_furia = InlineKeyboardMarkup([
        [InlineKeyboardButton("🐱‍👤 Falar sobre o time de CS", callback_data="time_cs")],
        [InlineKeyboardButton("🎮 Falar sobre os jogadores", callback_data="jogadores")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text="Agora que você já conhece a FURIA, tá na hora de saber mais sobre o nosso time ou os jogadores que fazem a magia acontecer! 🔥💥 O que você escolhe, tropa?",
        reply_markup=menu_furia
    )

async def handle_sobre_time_cs(bot: Bot, chat_id: int):
    info_time = '''💣 O time de CS:GO da FURIA é um dos mais temidos e respeitados no cenário mundial. 
    Com jogadores como FalleN, KSCERATO, molodoy, YEKINDAR e yuurih, a equipe tem conquistado títulos importantes e
    levado o nome do Brasil para o topo do CS:GO. 🇧🇷'''
    await bot.send_message(chat_id=chat_id, text=info_time)

    menu_time_cs = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Falar sobre os jogadores", callback_data="jogadores")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    await bot.send_message(
        chat_id=chat_id,
        text="🎯 Agora que você sabe sobre o time de CS, quer saber mais sobre os jogadores ou voltar? A escolha é sua, guerreiro(a)! 💪",
        reply_markup=menu_time_cs
    )

async def handle_sobre_jogadores_cs(bot: Bot, chat_id: int):
    info_jogadores = "🌟 Escolha um dos nossos craques para saber mais sobre ele! 🌟"

    menu_jogadores_cs = InlineKeyboardMarkup([
        [InlineKeyboardButton("FalleN", callback_data="FalleN")],
        [InlineKeyboardButton("KSCERATO", callback_data="KSCERATO")],
        [InlineKeyboardButton("molodoy", callback_data="molodoy")],
        [InlineKeyboardButton("yuurih", callback_data="yuurih")],
        [InlineKeyboardButton("Treinador-sidde", callback_data="Treinador-sidde")],
        [InlineKeyboardButton("Treinador-Hepa", callback_data="Treinador-Hepa")],
        [InlineKeyboardButton("🐱‍👤 Falar sobre o time de CS", callback_data="time_cs")],
        [InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]
    ])

    await bot.send_message(chat_id=chat_id, text=info_jogadores, reply_markup=menu_jogadores_cs)

async def handle_jogador_especifico(bot: Bot, chat_id: int, jogador: str):
    info_jogadores = {
        "FalleN": '''🔥 FalleN (Gabriel Toledo) - Rifler 🇧🇷
    Idade: 32 anos.
    FalleN é um dos maiores nomes da história do CS:GO, conhecido por sua liderança e habilidades excepcionais. Ele foi parte fundamental na ascensão da FURIA ao topo do cenário mundial, trazendo experiência e estratégia para o time. Além disso, é considerado um dos melhores AWPers do mundo e ajudou a consolidar a FURIA como uma potência internacional no CS:GO.''',
        "KSCERATO": '''💥 KSCERATO (Kaike Cerato) - Rifler 🇧🇷
Idade: 21 anos.
KSCERATO é um talento emergente e uma verdadeira estrela no cenário do CS:GO. Seu jogo agressivo e suas jogadas incríveis o tornaram uma referência no Brasil e no mundo. Com uma mira afiada e reflexos rápidos, ele tem sido um pilar importante para a FURIA, ajudando o time a conquistar grandes vitórias e a brilhar em torneios internacionais.''',
        "molodoy": '''🎯 molodoy (Danil Golubenko) - AWPer 🇰🇿
Idade: 22 anos.
molodoy é um dos jovens talentos da FURIA, com habilidades impressionantes no uso do AWP. Ele se destaca por sua precisão e suas decisões rápidas, características essenciais para dominar com essa arma. Mesmo sendo relativamente novo no cenário, molodoy já mostrou que tem potencial para competir de igual para igual com os melhores do mundo.''',
        "yuurih": '''⚡ yuurih (Yuri Santos) - Rifler 🇧🇷
Idade: 23 anos.
yuurih é um dos jogadores mais técnicos da FURIA. Seu estilo de jogo estratégico e sua habilidade com rifles fazem dele uma peça chave no time. Ele possui uma visão de jogo refinada, o que lhe permite fazer jogadas inteligentes e decisivas, sempre ajudando a FURIA a se destacar em competições de alto nível.''',
        "Treinador-sidde": '''💪 Sidde (Sid Macedo) - Treinador 🇧🇷
Idade: 30 anos.
Sidde é o cérebro por trás das estratégias da FURIA. Como treinador, ele tem a responsabilidade de orientar o time e ajudá-los a alcançar seu potencial máximo. Sua experiência e visão tática são fundamentais para o sucesso da equipe, e ele sempre está em busca de maneiras de otimizar o desempenho do time em todas as partidas.''',
        "Treinador-Hepa": '''🔧 Hepa (Juan Borges) - Assistente Técnico 🇪🇸
Idade: 28 anos.
Hepa é o assistente técnico da FURIA e trabalha de perto com Sidde para garantir que o time esteja sempre preparado e focado. Sua experiência como jogador e seu conhecimento do jogo o tornam uma peça fundamental no suporte aos jogadores. Hepa é o apoio perfeito para as estratégias do time, trazendo um olhar detalhado para o que precisa ser melhorado.'''
    }

    if jogador in info_jogadores:
        await bot.send_message(chat_id=chat_id, text=info_jogadores[jogador])
    else:
        await bot.send_message(chat_id=chat_id, text="Jogador não encontrado.")

    await handle_sobre_jogadores_cs(bot, chat_id)

async def handle_rolando_agora(bot: Bot, chat_id: int):
    await send_game_status(bot, chat_id)
# editando --------------------------------
